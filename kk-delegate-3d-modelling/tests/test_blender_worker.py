import argparse
import importlib.util
import json
import multiprocessing
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/blender_worker.py'
spec = importlib.util.spec_from_file_location('blender_worker', SCRIPT)
w = importlib.util.module_from_spec(spec)
spec.loader.exec_module(w)


def reserve(root, token, first, queue):
    try:
        def bind(sock, address):
            if address[1] == first: raise OSError('listener')
        with mock.patch.object(w.socket.socket, 'bind', bind):
            p, _ = w.reserve_port(Path(root), token, first, 4)
        queue.put(p)
    except Exception as e:
        queue.put(str(e))


def reserve_scope(root, out, token, gate, queue):
    gate.wait()
    try:
        w.reserve_output(Path(root), Path(out), token)
        queue.put('ok')
    except RuntimeError:
        queue.put('rejected')


class WorkerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='worker path ')
        self.root = Path(self.tmp.name).resolve()
        (self.root / 'ports').mkdir()
        (self.root / 'outputs').mkdir()
        self.out = self.root / 'my output'
        self.out.mkdir()
        self.token = 'a' * 32
        self.runroot = self.root / self.token
        self.runroot.mkdir()
        self.session = self.runroot / 'session.json'
        self.lease = self.root / 'ports/19876.json'
        self.ol = w.output_lease(self.root, self.out)
        self.s = dict(token=self.token, state_root=str(self.root), run_root=str(self.runroot), session_file=str(self.session), output_directory=str(self.out), port=19876, lease_file=str(self.lease), output_lease_file=str(self.ol), status='ready', host='127.0.0.1', background=False, process_id=123, process_started_utc='birth', blender_executable='/A Blender')
        w.write(self.session, self.s)
        w.write(self.lease, self.s)
        w.write(self.ol, {'token': self.token, 'output_directory': str(self.out)})

    def tearDown(self):
        self.tmp.cleanup()

    def test_reservations_concurrent_and_stale(self):
        base = 22000
        w.write(self.root / 'ports' / f'{base+1}.json', {'token':'stale'})
        q = multiprocessing.Queue()
        ps = [multiprocessing.Process(target=reserve, args=(str(self.root), str(i), base, q)) for i in range(2)]
        for p in ps: p.start()
        for p in ps: p.join(10)
        values = [q.get(timeout=2) for _ in ps]
        self.assertEqual(set(values), {base+2, base+3})

    def test_no_hundred_port_cap(self):
        for p in range(20000, 20110):
            w.write(self.root / 'ports' / f'{p}.json', {'token':'stale'})
        with mock.patch.object(w.socket.socket, 'bind'):
            port, _ = w.reserve_port(self.root, self.token, 20000, 120)
        self.assertEqual(port, 20110)

    def test_untrusted_paths_tokens_and_birth_rejected(self):
        for field, value in [('token', 'bad'), ('lease_file', str(self.root / 'wrong')), ('session_file', str(self.root / 'wrong')), ('run_root', str(self.root))]:
            bad = dict(self.s); bad[field] = value; w.write(self.session, bad)
            with self.assertRaises((RuntimeError, FileNotFoundError)): w.validate(self.session)
        w.write(self.session, self.s)
        with mock.patch.object(w, 'started', return_value='different'):
            with self.assertRaises(RuntimeError): w.process_identity(self.s)
        bad = dict(self.s); bad['token'] = 'b' * 32; w.write(self.lease, bad)
        with self.assertRaises(RuntimeError): w.validate(self.session)

    def test_lock_and_orphan(self):
        with w.lock(self.s):
            with self.assertRaises(RuntimeError): w.lock(self.s)
        w.write(self.runroot / 'modeller.json', {'process_id':456, 'process_started_utc':'birth'})
        with mock.patch.object(w, 'alive', return_value=True):
            with self.assertRaises(RuntimeError): w.child_check(self.s)

    def test_run_argv_and_logs(self):
        prompt = self.root / 'prompt file'; prompt.write_text('build')
        ref = self.root / 'reference file.png'; ref.touch()
        proc = mock.Mock(pid=456, returncode=0)
        def spawn(args, **kwargs):
            w.write(args[4], {'process_id': 456, 'process_started_utc': 'birth'})
            return proc
        for complexity, model, tier in [
            ('simple', 'gpt-6.1-terra', 'priority'),
            ('complex', 'gpt-6.2-sol', 'default'),
            ('toughest', 'gpt-6.2-astra', 'default'),
        ]:
            with self.subTest(complexity=complexity):
                with mock.patch.object(w, 'verify'), mock.patch.object(w, 'alive', return_value=False), mock.patch.object(w.subprocess, 'Popen', side_effect=spawn):
                    w.run(argparse.Namespace(session_file=str(self.session), prompt_file=str(prompt), reference_image=str(ref), complexity=complexity, resume_thread=None))
                config = w.read(w.read(self.out / 'model-run.json')['run_config'])
                args = config['args']
                self.assertEqual(args[args.index('-m') + 1], model)
                self.assertIn(f'service_tier="{tier}"', args)
                self.assertIn('model_reasoning_effort="high"', args)
                self.assertEqual(config['complexity'], complexity)
                self.assertIn(str(ref), args)
                self.assertTrue(any('BLENDER_PORT="19876"' in x for x in args))
                worker_prompt = proc.communicate.call_args.args[0]
                self.assertIn(f'{model}, high reasoning effort and service tier {tier}', worker_prompt)
                self.assertIn("'background':False", worker_prompt)
        self.assertEqual(len(list(self.runroot.glob('attempt-*/run-config.json'))), 3)

    def test_stop_validates_and_releases(self):
        a = argparse.Namespace(session_file=str(self.session), exports_validated=True)
        with mock.patch.object(w, 'verify'), mock.patch.object(w, 'process_identity') as identity, mock.patch.object(w.os, 'kill') as kill, mock.patch.object(w, 'alive', return_value=False):
            w.stop(a)
        identity.assert_called_once(); kill.assert_called_once()
        self.assertFalse(self.lease.exists()); self.assertFalse(self.ol.exists())
        self.assertEqual(w.read(self.session)['status'], 'stopped')

    def test_stop_failure_never_signals(self):
        a = argparse.Namespace(session_file=str(self.session), exports_validated=True)
        with mock.patch.object(w, 'verify', side_effect=RuntimeError('wrong process')), mock.patch.object(w.os, 'kill') as kill:
            with self.assertRaises(RuntimeError): w.stop(a)
        kill.assert_not_called()
        self.assertTrue(self.lease.exists())

    def test_output_parent_child_race(self):
        self.ol.unlink()
        child = self.out / 'child'; child.mkdir()
        gate = multiprocessing.Event(); q = multiprocessing.Queue()
        processes = [multiprocessing.Process(target=reserve_scope, args=(str(self.root), str(path), token * 32, gate, q)) for path, token in [(self.out, 'a'), (child, 'b')]]
        for p in processes: p.start()
        gate.set()
        for p in processes: p.join(10)
        self.assertEqual(sorted(q.get(timeout=2) for _ in processes), ['ok', 'rejected'])

    def test_inherited_lock_survives_parent_close(self):
        handle = w.lock(self.s)
        child = subprocess.Popen([sys.executable, '-c', 'import sys; sys.stdin.read()'], stdin=subprocess.PIPE, pass_fds=(handle.fileno(),))
        handle.close()
        try:
            with self.assertRaises(RuntimeError): w.lock(self.s)
        finally:
            child.stdin.close()
            child.wait(timeout=5)
        with w.lock(self.s): pass

    def test_shim_records_before_exec(self):
        config = self.runroot / 'config.json'
        ready = self.runroot / 'ready.json'
        w.write(config, {'session_file': str(self.session), 'args': ['codex', 'exec']})
        def fake_exec(executable, args):
            self.assertEqual(w.read(self.runroot / 'modeller.json')['process_id'], os.getpid())
            self.assertEqual(w.read(ready)['process_id'], os.getpid())
            raise RuntimeError('exec observed')
        with w.lock(self.s) as handle, mock.patch.object(w, 'verify'), mock.patch.object(w, 'started', return_value='birth'), mock.patch.object(w.os, 'execvp', side_effect=fake_exec):
            with self.assertRaisesRegex(RuntimeError, 'exec observed'):
                w.exec_modeller(str(config), str(ready), str(handle.fileno()))

    def test_shim_startup_failure_no_prompt(self):
        prompt = self.root / 'prompt'; prompt.write_text('build')
        ref = self.root / 'reference'; ref.touch()
        proc = mock.Mock(pid=456, returncode=7)
        proc.poll.return_value = 7
        with mock.patch.object(w, 'verify'), mock.patch.object(w.subprocess, 'Popen', return_value=proc):
            with self.assertRaisesRegex(RuntimeError, 'startup failed'):
                w.run(argparse.Namespace(session_file=str(self.session), prompt_file=str(prompt), reference_image=str(ref), complexity='simple', resume_thread=None))
        proc.communicate.assert_not_called()

    def test_overlapping_outputs_rejected(self):
        child = self.out / 'child'; child.mkdir()
        with self.assertRaisesRegex(RuntimeError, 'overlaps'):
            w.reserve_output(self.root, child, 'b' * 32)
        with self.assertRaisesRegex(RuntimeError, 'overlaps'):
            w.reserve_output(self.root, self.root, 'b' * 32)

    def test_case_alias_and_its_children_are_rejected(self):
        alias = self.out.with_name(self.out.name.upper())
        if not alias.exists():
            self.skipTest('requires a case-insensitive filesystem')
        child = alias / 'child'
        child.mkdir()
        for first, second in [(self.out, alias), (self.out, child), (child, self.out)]:
            with self.subTest(first=first, second=second):
                self.ol.unlink(missing_ok=True)
                lease = w.reserve_output(self.root, first.resolve(strict=True), 'a' * 32)
                try:
                    with self.assertRaisesRegex(RuntimeError, 'overlaps reserved'):
                        w.reserve_output(self.root, second.resolve(strict=True), 'b' * 32)
                finally:
                    lease.unlink()

    def test_recover_releases_crashed_session_without_signalling(self):
        self.out.rmdir()
        a = argparse.Namespace(session_file=self.session)
        with mock.patch.object(w, 'started', side_effect=ProcessLookupError), \
             mock.patch.object(w.socket.socket, 'bind') as bind, \
             mock.patch.object(w.os, 'kill') as kill:
            w.recover(a)
            w.recover(a)
        bind.assert_called_once_with(('127.0.0.1', self.s['port']))
        kill.assert_not_called()
        self.assertEqual(w.read(self.session)['status'], 'recovered')
        self.assertFalse(self.ol.exists())
        self.assertFalse(self.lease.exists())
        self.out.mkdir()
        self.assertEqual(w.reserve_output(self.root, self.out, 'b' * 32), self.ol)

    def test_recover_preserves_leases_when_process_or_endpoint_is_live(self):
        a = argparse.Namespace(session_file=self.session)
        with mock.patch.object(w, 'started', return_value='birth'), \
             mock.patch.object(w.socket.socket, 'bind') as bind:
            with self.assertRaisesRegex(RuntimeError, 'Blender PID is still live'):
                w.recover(a)
            bind.assert_not_called()
        with mock.patch.object(w, 'started', side_effect=ProcessLookupError), \
             mock.patch.object(w.socket.socket, 'bind', side_effect=OSError):
            with self.assertRaisesRegex(RuntimeError, 'endpoint is unavailable'):
                w.recover(a)
        self.assertEqual(w.read(self.session)['status'], 'ready')
        self.assertTrue(self.ol.exists())
        self.assertTrue(self.lease.exists())

    def test_recover_refuses_wrong_leases_or_uncertain_process_state(self):
        a = argparse.Namespace(session_file=self.session)
        with mock.patch.object(w, 'started', side_effect=PermissionError), \
             mock.patch.object(w.socket.socket, 'bind') as bind:
            with self.assertRaises(PermissionError):
                w.recover(a)
            bind.assert_not_called()
        w.write(self.lease, dict(self.s, process_id=321))
        with self.assertRaisesRegex(RuntimeError, 'Lease ownership mismatch'):
            w.recover(a)
        self.assertTrue(self.ol.exists())
        self.assertTrue(self.lease.exists())

    def test_recover_refuses_active_modeller(self):
        a = argparse.Namespace(session_file=self.session)
        w.write(self.runroot / 'modeller.json', {'process_id': 456, 'process_started_utc': 'modeller birth'})
        with mock.patch.object(w, 'started', return_value='modeller birth'), \
             mock.patch.object(w.socket.socket, 'bind') as bind:
            with self.assertRaisesRegex(RuntimeError, 'Live modeller'):
                w.recover(a)
            bind.assert_not_called()

    def test_recover_retries_interrupted_cleanup_and_keeps_new_lease(self):
        a = argparse.Namespace(session_file=self.session)
        w.write(self.session, dict(self.s, status='cleanup_pending', cleanup_result='recovered'))
        self.ol.unlink()
        w.reserve_output(self.root, self.out, 'b' * 32)
        with mock.patch.object(w.os, 'kill') as kill:
            w.recover(a)
        kill.assert_not_called()
        self.assertEqual(w.read(self.ol)['token'], 'b' * 32)
        self.assertFalse(self.lease.exists())
        self.assertEqual(w.read(self.session)['status'], 'recovered')

    def test_wrap_and_shared_port_exclusion(self):
        w.write(self.root / 'ports/65535.json', {'token': 'occupied'})
        with mock.patch.object(w.socket.socket, 'bind'):
            port, _ = w.reserve_port(self.root, self.token, 65535, 3)
        self.assertEqual(port, 1024)
        w.write(self.root / 'ports/9875.json', {'token': 'occupied'})
        with mock.patch.object(w.socket.socket, 'bind'):
            port, _ = w.reserve_port(self.root, self.token, 9875, 3)
        self.assertEqual(port, 9877)

    def test_duplicate_output_rejected_before_spawn(self):
        blender = self.root / 'Blender'; blender.touch()
        addon = self.root / 'addon.py'; addon.touch()
        a = argparse.Namespace(output_directory=str(self.out), state_root=str(self.root), blender_executable=str(blender), addon_path=str(addon), first_port=25000, port_count=5)
        with mock.patch.object(w.subprocess, 'Popen') as popen:
            with self.assertRaisesRegex(RuntimeError, 'overlaps reserved'): w.allocate(a)
        popen.assert_not_called()

    def test_wrong_listener_rejected(self):
        with mock.patch.object(w, 'process_identity'), mock.patch.object(w.subprocess, 'check_output', return_value='999\n'):
            with self.assertRaisesRegex(RuntimeError, 'Listener ownership'): w.verify(self.s)

    def test_live_modeller_prevents_stop(self):
        w.write(self.runroot / 'modeller.json', {'process_id':456, 'process_started_utc':'birth'})
        a = argparse.Namespace(session_file=str(self.session), exports_validated=True)
        with mock.patch.object(w, 'alive', return_value=True), mock.patch.object(w.os, 'kill') as kill:
            with self.assertRaisesRegex(RuntimeError, 'Live modeller'): w.stop(a)
        kill.assert_not_called()

    def test_resume_arguments_and_attempt_metadata(self):
        prompt = self.root / 'prompt file'; prompt.write_text('build')
        ref = self.root / 'reference file.png'; ref.touch()
        proc = mock.Mock(pid=456, returncode=0)
        def spawn(args, **kwargs):
            w.write(args[4], {'process_id': 456, 'process_started_utc': 'birth'})
            return proc
        with mock.patch.object(w, 'verify'), mock.patch.object(w, 'started', return_value='birth'), mock.patch.object(w.subprocess, 'Popen', side_effect=spawn) as popen:
            w.run(argparse.Namespace(session_file=str(self.session), prompt_file=str(prompt), reference_image=str(ref), complexity='toughest', resume_thread='thread-123'))
        args = w.read(w.read(self.out / 'model-run.json')['run_config'])['args']
        self.assertEqual(args[args.index('resume')+1], '--skip-git-repo-check')
        self.assertEqual(args[-2:], ['thread-123', '-'])
        self.assertEqual(args[args.index('-m') + 1], 'gpt-6.2-astra')
        self.assertIn('service_tier="default"', args)
        self.assertIn('model_reasoning_effort="high"', args)
        self.assertNotEqual(popen.call_args.kwargs['stdout'], popen.call_args.kwargs['stderr'])
        pointer = w.read(self.out / 'model-run.json')
        self.assertEqual(w.read(pointer['run_config'])['args'], args)
        self.assertIn(str(SCRIPT.parent.parent / 'SKILL.md'), proc.communicate.call_args.args[0])

    def test_startup_failure_releases_leases(self):
        self.ol.unlink()
        blender = self.root / 'Blender'; blender.touch()
        addon = self.root / 'addon.py'; addon.touch()
        a = argparse.Namespace(output_directory=str(self.out), state_root=str(self.root), blender_executable=str(blender), addon_path=str(addon), first_port=25000, port_count=5)
        with mock.patch.object(w.socket.socket, 'bind'), mock.patch.object(w.subprocess, 'Popen', side_effect=OSError('launch failed')):
            with self.assertRaisesRegex(RuntimeError, 'leases released'): w.allocate(a)
        self.assertFalse(w.output_lease(self.root, self.out).exists())
        self.assertFalse((self.root / 'ports/25000.json').exists())


if __name__ == '__main__': unittest.main()

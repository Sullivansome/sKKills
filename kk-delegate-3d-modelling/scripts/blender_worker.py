#!/usr/bin/env python3
"""Allocate, use and stop isolated interactive macOS Blender MCP workers."""
import argparse
import datetime
import contextlib
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import signal
import socket
import subprocess
import sys
import time

DEFAULT_ROOT = Path.home() / '.codex/blender-workers'
BOOT = Path(__file__).resolve().with_name('blender_worker_bootstrap.py')
WORKER_PROFILES = {
    'simple': ('gpt-6.1-terra', 'priority'),
    'complex': ('gpt-6.2-sol', 'default'),
    'toughest': ('gpt-6.2-astra', 'default'),
}


def write(path, data):
    path = Path(path)
    tmp = path.with_name(path.name + '.' + secrets.token_hex(8) + '.tmp')
    try:
        tmp.write_text(json.dumps(data, indent=2), encoding='utf-8')
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def started(pid):
    # Include state: a zombie cannot own a socket and must not block cleanup forever.
    result = subprocess.run(['ps', '-p', str(pid), '-o', 'state=', '-o', 'lstart='],
                            capture_output=True, text=True)
    if result.returncode == 1 and not (result.stdout.strip() or result.stderr.strip()):
        raise ProcessLookupError(pid)
    result.check_returncode()
    state, birth = result.stdout.strip().split(None, 1)
    if state.startswith('Z'):
        raise ProcessLookupError(pid)
    return birth


def alive(pid, stamp):
    try:
        return bool(stamp) and started(pid) == stamp
    except ProcessLookupError:
        return False


def output_lease(root, output):
    return root / 'outputs' / (hashlib.sha256(str(output).encode()).hexdigest() + '.json')


def directory_identity(path):
    info = path.stat()
    return info.st_dev, info.st_ino


def output_ancestors(path):
    for parent in (path, *path.parents):
        try:
            yield directory_identity(parent)
        except FileNotFoundError:
            continue


def exclusive(path, data):
    fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    with os.fdopen(fd, 'w') as f:
        json.dump(data, f)


def release(path, token):
    path = Path(path)
    if read(path).get('token') != token:
        raise RuntimeError('Lease token changed; retained: ' + str(path))
    path.unlink()


@contextlib.contextmanager
def registry_lock(root):
    with open(root / 'outputs.lock', 'a+') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        yield


def reserve_output(root, out, token):
    lease = output_lease(root, out)
    with registry_lock(root):
        identity = directory_identity(out)
        ancestors = set(output_ancestors(out))
        for existing in (root / 'outputs').glob('*.json'):
            try:
                record = read(existing)
                other = Path(record['output_directory'])
                if not other.is_absolute() or not re.fullmatch(r'[0-9a-f]{32}', record['token']) or output_lease(root, other) != existing:
                    raise ValueError('invalid lease')
            except (OSError, ValueError, KeyError, TypeError) as e:
                raise RuntimeError('Malformed output lease; inspect ' + str(existing)) from e
            try:
                other_identity = directory_identity(other)
            except FileNotFoundError:
                other_identity = None
            if (out == other or out in other.parents or other in out.parents or
                other_identity in ancestors or identity in output_ancestors(other)):
                raise RuntimeError('Output directory overlaps reserved scope: ' + str(existing))
        exclusive(lease, {'token': token, 'output_directory': str(out)})
    return lease


def release_output(root, path, token):
    with registry_lock(root):
        release(path, token)


def reserve_port(root, token, first, count):
    if not 1024 <= first <= 65535 or not 1 <= count <= 64512:
        raise ValueError('Invalid port range')
    for offset in range(count):
        port = 1024 + ((first - 1024 + offset) % 64512)
        if port == 9876:
            continue
        lease = root / 'ports' / f'{port}.json'
        try:
            exclusive(lease, {'token': token})
        except FileExistsError:
            continue
        try:
            with socket.socket() as sock:
                sock.bind(('127.0.0.1', port))
        except OSError:
            release(lease, token)
            continue
        return port, lease
    raise RuntimeError('No free unleased port in requested range')


def lock(s):
    f = open(Path(s['run_root']) / 'worker.lock', 'a+')
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BaseException:
        f.close()
        raise RuntimeError('Session is already in use')
    return f


def child_check(s):
    p = Path(s['run_root']) / 'modeller.json'
    if p.exists():
        c = read(p)
        if alive(c['process_id'], c['process_started_utc']):
            raise RuntimeError('Live modeller owns session: ' + str(p))


def validate(path, *, cleanup=False):
    path = Path(path).expanduser().resolve(strict=True)
    s = read(path)
    token = s.get('token', '')
    if not re.fullmatch(r'[0-9a-f]{32}', token):
        raise RuntimeError('Invalid session token')
    root = Path(s['state_root']).expanduser().resolve(strict=True)
    run = root / token
    out = Path(s['output_directory'])
    port = s['port']
    if (Path(s['run_root']) != run or path != run / 'session.json' or
        Path(s['session_file']) != path or not isinstance(port, int) or
        not 1024 <= port <= 65535 or port == 9876 or
        Path(s['lease_file']) != root / 'ports' / f'{port}.json' or
        not out.is_absolute() or Path(s['output_lease_file']) != output_lease(root, out)):
        raise RuntimeError('Session path or lease mismatch')
    if not cleanup and out.resolve(strict=True) != out:
        raise RuntimeError('Session output directory no longer resolves to its recorded path')
    cleanup_started = cleanup and s.get('status') in ('cleanup_pending', 'stopped', 'recovered')
    for lease, expected in (
        (s['lease_file'], {'token': token, 'process_id': s['process_id'],
                           'process_started_utc': s.get('process_started_utc')}),
        (s['output_lease_file'], {'token': token, 'output_directory': str(out)}),
    ):
        try:
            record = read(lease)
        except FileNotFoundError:
            if cleanup_started:
                continue
            raise
        if cleanup_started and record.get('token') != token:
            # A completed unlink may already have been followed by a new reservation.
            continue
        if any(record.get(key) != value for key, value in expected.items()):
            raise RuntimeError('Lease ownership mismatch: ' + lease)
    return s


def process_identity(s):
    pid = s['process_id']
    if not alive(pid, s.get('process_started_utc')):
        raise RuntimeError('Blender PID or creation time mismatch')
    cmd = subprocess.check_output(['ps', '-p', str(pid), '-o', 'command='], text=True)
    for part in (s['blender_executable'], str(BOOT), s['session_file']):
        if part not in cmd:
            raise RuntimeError('Blender command mismatch')


def verify(s):
    if s.get('status') != 'ready' or s.get('host') != '127.0.0.1' or s.get('background') is not False:
        raise RuntimeError('Session is not ready and interactive')
    lease = read(s['lease_file'])
    if lease.get('process_id') != s['process_id'] or lease.get('process_started_utc') != s['process_started_utc']:
        raise RuntimeError('Port lease process mismatch')
    process_identity(s)
    try:
        listeners = subprocess.check_output(['lsof', '-nP', '-iTCP:' + str(s['port']), '-sTCP:LISTEN', '-t'], text=True).split()
    except subprocess.CalledProcessError as e:
        raise RuntimeError('No owned MCP listener') from e
    if set(listeners) != {str(s['process_id'])}:
        raise RuntimeError('Listener ownership mismatch')


def discover_blender(value):
    candidates = [Path(value).expanduser()] if value else [Path('/Applications/Blender.app/Contents/MacOS/Blender'), Path.home() / 'Applications/Blender.app/Contents/MacOS/Blender']
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    raise RuntimeError('Blender executable not found; specify --blender-executable')


def discover_addon(value, blender):
    if value:
        p = Path(value).expanduser().resolve(strict=True)
        if not p.is_file():
            raise RuntimeError('Addon is not a file')
        return p
    resources = blender.parent.parent / 'Resources'
    versions = sorted((p.name for p in resources.iterdir() if p.is_dir() and re.fullmatch(r'\d+\.\d+', p.name)), key=lambda x: tuple(map(int, x.split('.'))), reverse=True) if resources.is_dir() else []
    for version in versions:
        p = Path.home() / 'Library/Application Support/Blender' / version / 'scripts/addons/blender_mcp.py'
        if p.is_file():
            return p.resolve()
    raise RuntimeError('Matching installed Blender MCP addon not found; specify --addon-path')


def allocate(a):
    out = Path(a.output_directory).expanduser().resolve(strict=True)
    if not out.is_dir():
        raise RuntimeError('Output directory must exist')
    blender = discover_blender(a.blender_executable)
    addon = discover_addon(a.addon_path, blender)
    if not BOOT.is_file():
        raise RuntimeError('Missing bootstrap: ' + str(BOOT))
    root = Path(a.state_root).expanduser().resolve()
    for name in ('ports', 'outputs'):
        (root / name).mkdir(parents=True, exist_ok=True)
    token = secrets.token_hex(16)
    runroot = root / token
    outlease = reserve_output(root, out, token)
    lease = None
    proc = None
    stamp = None
    try:
        port, lease = reserve_port(root, token, a.first_port, a.port_count)
        for sub in ('config', 'scripts', 'datafiles'):
            (runroot / sub).mkdir(parents=True, exist_ok=True)
        session = runroot / 'session.json'
        s = dict(host='127.0.0.1', port=port, token=token, state_root=str(root), platform='macos', run_root=str(runroot), session_file=str(session), output_directory=str(out), output_lease_file=str(outlease), status='starting', process_id=None, reservation_process_id=os.getpid(), lease_file=str(lease), blender_executable=str(blender), addon_path=str(addon), started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
        write(lease, s)
        write(session, s)
        env = os.environ.copy()
        env.update({f'BLENDER_USER_{name.upper()}': str(runroot / name) for name in ('config', 'scripts', 'datafiles')})
        env.update(DISABLE_TELEMETRY='true', PYTHONUTF8='1')
        with open(runroot / 'blender.stdout.log', 'w') as stdout, open(runroot / 'blender.stderr.log', 'w') as stderr:
            proc = subprocess.Popen([str(blender), '--factory-startup', '--python', str(BOOT), '--', str(session)], env=env, stdout=stdout, stderr=stderr, start_new_session=True)
        stamp = started(proc.pid)
        write(runroot / 'launch.json', dict(process_id=proc.pid, process_started_utc=stamp))
        deadline = time.monotonic() + 60
        while time.monotonic() < deadline:
            if proc.poll() is not None:
                raise RuntimeError('Blender exited before readiness')
            s = read(session)
            if s['status'] == 'failed':
                raise RuntimeError(s.get('error', 'Bootstrap failed'))
            if s['status'] == 'ready':
                if s['process_id'] != proc.pid or s['process_started_utc'] != stamp:
                    raise RuntimeError('Bootstrap process mismatch')
                verify(validate(session))
                print('SESSION_FILE=' + str(session))
                print(json.dumps({'session_file': str(session), 'run_root': str(runroot), 'port': port, 'output_directory': str(out)}))
                return
            time.sleep(.2)
        raise RuntimeError('Timed out waiting for Blender MCP')
    except BaseException as e:
        safe = proc is None or proc.poll() is not None
        if not safe and stamp:
            try:
                process_identity(dict(process_id=proc.pid, process_started_utc=stamp, blender_executable=str(blender), session_file=str(runroot / 'session.json')))
                proc.terminate()
                proc.wait(timeout=15)
                safe = True
            except (OSError, RuntimeError, subprocess.SubprocessError):
                pass
        session_path = runroot / 'session.json'
        if session_path.exists():
            try:
                failed = read(session_path)
                failed.update(status='failed', error=str(e))
                write(session_path, failed)
            except (OSError, ValueError):
                pass
        if safe:
            if lease and lease.exists():
                release(lease, token)
            if outlease.exists():
                release_output(root, outlease, token)
        raise RuntimeError(f'Allocation failed: {e}; diagnostics: {runroot}; leases {"released" if safe else "retained due to uncertain process ownership"}') from e


def run(a):
    model, service_tier = WORKER_PROFILES[a.complexity]
    reasoning_effort = 'high'
    s = validate(a.session_file)
    with lock(s) as session_lock:
        child_check(s)
        s = validate(a.session_file)
        verify(s)
        out = Path(s['output_directory'])
        prompt = Path(a.prompt_file).expanduser().resolve(strict=True)
        ref = Path(a.reference_image).expanduser().resolve(strict=True)
        attempt = Path(s['run_root']) / ('attempt-' + str(time.time_ns()))
        attempt.mkdir()
        config_path = attempt / 'run-config.json'
        identity = f'''You are the assigned modeller. Use the captured launcher argv in {config_path} to confirm the requested model {model}, {reasoning_effort} reasoning effort and service tier {service_tier}. Read the deployed skill at {Path(__file__).resolve().parents[1] / 'SKILL.md'}. Do not recursively delegate. Use kk-delegate-3d-modelling and blender-skills. Before ANY Blender mutation, call Blender MCP get_addon_status and then execute_blender_code with:
import bpy, os, json
server = getattr(bpy.types, 'blendermcp_server', None)
identity = {{'pid':os.getpid(), 'token':bpy.app.driver_namespace.get('codex_worker_token'), 'port':getattr(server,'port',None), 'background':bpy.app.background}}
assert identity == {{'pid':{s['process_id']}, 'token':'{s['token']}', 'port':{s['port']}, 'background':False}}, identity
print(json.dumps(identity))
Save the returned identity in the output directory. If it fails, STOP; never fall back to port 9876. Use only the configured MCP server. Do not reset Blender, open another file, or alter existing scenes, objects, worlds or preferences. Build in isolated scenes and save separate asset files. All source and asset writes must stay under {out}. Session metadata: {s['session_file']}. Report incomplete work explicitly.\n\n'''
        override = 'mcp_servers.blender.env={BLENDER_HOST="127.0.0.1",BLENDER_PORT="' + str(s['port']) + '",DISABLE_TELEMETRY="true"}'
        common = [
            '--approve-for-me', '-C', str(out),
            '-c', f'model_reasoning_effort="{reasoning_effort}"',
            '-c', f'service_tier="{service_tier}"', '-c', override,
        ]
        args = ['codex'] + common + ['exec']
        if a.resume_thread:
            args += ['resume', '--skip-git-repo-check', '-m', model, '-o', str(attempt / 'last-model.md'), '--', a.resume_thread, '-']
        else:
            args += ['--skip-git-repo-check', '-m', model, '-o', str(attempt / 'last-model.md'), '-i', str(ref), '--', '-']
        write(config_path, dict(
            args=args, complexity=a.complexity, model=model, reasoning_effort=reasoning_effort,
            service_tier=service_tier, session_file=s['session_file'], token=s['token'],
            blender_process_id=s['process_id'], reference_image=str(ref),
        ))
        write(out / 'model-run.json', dict(attempt_directory=str(attempt), run_config=str(config_path), session_file=s['session_file']))
        with open(attempt / 'stdout.log', 'w') as stdout, open(attempt / 'stderr.log', 'w') as stderr:
            ready = attempt / 'shim-ready.json'
            shim_args = [sys.executable, str(Path(__file__).resolve()), '_exec-modeller', str(config_path), str(ready), str(session_lock.fileno())]
            p = subprocess.Popen(shim_args, stdin=subprocess.PIPE, stdout=stdout, stderr=stderr, text=True, pass_fds=(session_lock.fileno(),))
            deadline = time.monotonic() + 15
            while not ready.exists():
                if p.poll() is not None:
                    raise RuntimeError(f'Modeller startup failed ({p.returncode}); logs: {attempt}')
                if time.monotonic() >= deadline:
                    p.terminate()
                    p.wait()
                    raise RuntimeError(f'Modeller startup timed out; logs: {attempt}')
                time.sleep(.05)
            record = read(ready)
            if record.get('process_id') != p.pid:
                p.terminate()
                p.wait()
                raise RuntimeError('Modeller shim ownership mismatch')
            p.communicate(identity + prompt.read_text(encoding='utf-8'))
            record.update(status='exited', exit_code=p.returncode)
            write(Path(s['run_root']) / 'modeller.json', record)
            if p.returncode:
                raise RuntimeError(f'Modeller failed ({p.returncode}); logs: {attempt}')
        print('ATTEMPT_DIRECTORY=' + str(attempt))


def stop(a):
    if not a.exports_validated:
        raise RuntimeError('Exports must be validated before stopping')
    s = validate(a.session_file)
    with lock(s):
        child_check(s)
        s = validate(a.session_file)
        verify(s)
        process_identity(s)
        os.kill(s['process_id'], signal.SIGTERM)
        deadline = time.monotonic() + 15
        while alive(s['process_id'], s['process_started_utc']) and time.monotonic() < deadline:
            time.sleep(.2)
        if alive(s['process_id'], s['process_started_utc']):
            raise RuntimeError('Owned Blender did not exit; leases retained')
        finish_cleanup(validate(a.session_file), 'stopped')
    print('SESSION_FILE=' + s['session_file'])


def finish_cleanup(s, result):
    # Record that ownership and process exit were verified before either unlink.
    s.update(status='cleanup_pending', cleanup_result=result)
    write(s['session_file'], s)
    with registry_lock(Path(s['state_root'])):
        for path in (Path(s['output_lease_file']), Path(s['lease_file'])):
            try:
                owner = read(path).get('token')
            except FileNotFoundError:
                continue
            if owner == s['token']:
                release(path, s['token'])
    s['status'] = result
    write(s['session_file'], s)


def recover(a):
    s = validate(a.session_file, cleanup=True)
    with lock(s):
        s = validate(a.session_file, cleanup=True)
        child_check(s)
        status = s['status']
        if status == 'cleanup_pending':
            result = s['cleanup_result']
            if result not in ('stopped', 'recovered'):
                raise RuntimeError('Invalid pending cleanup result')
            finish_cleanup(s, result)
        elif status not in ('stopped', 'recovered'):
            pid, birth = s.get('process_id'), s.get('process_started_utc')
            if status != 'ready' or s.get('host') != '127.0.0.1' or s.get('background') is not False:
                raise RuntimeError('Recovery requires a previously ready interactive session')
            if not isinstance(pid, int) or pid <= 0 or not isinstance(birth, str) or not birth:
                raise RuntimeError('Recovery requires a recorded Blender PID and creation time')
            try:
                started(pid)
            except ProcessLookupError:
                pass
            else:
                raise RuntimeError('Recorded Blender PID is still live; leases retained')
            with socket.socket() as probe:
                try:
                    probe.bind((s['host'], s['port']))
                except OSError as e:
                    raise RuntimeError('MCP endpoint is unavailable; leases retained') from e
                finish_cleanup(s, 'recovered')
    print('SESSION_FILE=' + s['session_file'])


def exec_modeller(config_path, ready_path, lock_fd):
    # The inherited flock remains held even if the coordinating wrapper dies.
    os.set_inheritable(int(lock_fd), True)
    config = read(config_path)
    s = validate(config['session_file'])
    child_check(s)
    verify(s)
    record = dict(process_id=os.getpid(), process_started_utc=started(os.getpid()), status='running', session_file=s['session_file'])
    write(Path(s['run_root']) / 'modeller.json', record)
    write(ready_path, record)
    os.execvp(config['args'][0], config['args'])


def main():
    if len(sys.argv) > 1 and sys.argv[1] == '_exec-modeller':
        exec_modeller(*sys.argv[2:])
        return
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    q = sub.add_parser('allocate')
    q.add_argument('--output-directory', required=True)
    q.add_argument('--state-root', default=str(DEFAULT_ROOT))
    q.add_argument('--blender-executable')
    q.add_argument('--addon-path')
    q.add_argument('--first-port', type=int, default=19876)
    q.add_argument('--port-count', type=int, default=64512)
    q.set_defaults(fn=allocate)
    q = sub.add_parser('run')
    q.add_argument('--session-file', required=True)
    q.add_argument('--prompt-file', required=True)
    q.add_argument('--reference-image', required=True)
    q.add_argument('--complexity', choices=WORKER_PROFILES, required=True)
    q.add_argument('--resume-thread')
    q.set_defaults(fn=run)
    q = sub.add_parser('stop')
    q.add_argument('--session-file', required=True)
    q.add_argument('--exports-validated', action='store_true')
    q.set_defaults(fn=stop)
    q = sub.add_parser('recover', help='Release leases for a crashed worker without signalling a process')
    q.add_argument('--session-file', required=True)
    q.set_defaults(fn=recover)
    a = p.parse_args()
    try:
        a.fn(a)
    except (OSError, ValueError, KeyError, RuntimeError, subprocess.SubprocessError) as e:
        print('Error:', e, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

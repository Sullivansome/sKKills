"""Exercise the actual shell installer with local release fixtures; never network."""
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / 'kk-project-bootstrap/assets/install.sh'


class InstallerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.keydir = tempfile.TemporaryDirectory(prefix='kk-test-signing-')
        cls.addClassCleanup(cls.keydir.cleanup)
        cls.private_key = Path(cls.keydir.name) / 'test-private.pem'
        cls.other_key = Path(cls.keydir.name) / 'untrusted-private.pem'
        for key in (cls.private_key, cls.other_key):
            subprocess.run(['openssl', 'genpkey', '-algorithm', 'RSA', '-pkeyopt',
                            'rsa_keygen_bits:2048', '-out', str(key)], check=True,
                           capture_output=True, timeout=30)
        cls.public_key = subprocess.check_output(
            ['openssl', 'pkey', '-in', str(cls.private_key), '-pubout'], text=True)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='skkills-installer-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.release = self.root / 'release'
        self.release.mkdir()
        self.mockbin = self.root / 'tools'
        self.mockbin.mkdir()
        self.dest = self.root / 'install with spaces'
        self.dest.mkdir()
        self.installed = self.dest / 'myapp'
        self.installed.write_bytes(b'previous working version')
        self.script = self.root / 'install.sh'
        self.script.write_text(TEMPLATE.read_text()
                               .replace('REPO="OWNER/REPO"', 'REPO="fixture/example"')
                               .replace('REPLACE_WITH_TRUSTED_PUBLISHER_PUBLIC_KEY_PEM', self.public_key.strip()))
        self.env = dict(os.environ, PATH=f'{self.mockbin}:{os.environ["PATH"]}',
                        INSTALL_DIR=str(self.dest), VERSION='v1.2.3',
                        FIXTURE_RELEASE=str(self.release), FIXTURE_ARCH='x86_64',
                        FIXTURE_OS='Linux')
        (self.mockbin / 'python3').symlink_to(sys.executable)
        self.make_tool('uname', '''import os, sys
print(os.environ['FIXTURE_OS'] if sys.argv[1] == '-s' else os.environ['FIXTURE_ARCH'])
''')
        self.make_tool('curl', '''import os, pathlib, shutil, sys
args=sys.argv[1:]
url=next(a for a in args if a.startswith('https://'))
dest=pathlib.Path(args[args.index('-o')+1])
if url == 'https://api.github.com/repos/fixture/example/releases/latest':
    dest.write_text(os.environ.get('FIXTURE_RELEASE_JSON', '{"tag_name": "v1.2.3"}'))
else:
    prefix='https://github.com/fixture/example/releases/download/v1.2.3/'
    if not url.startswith(prefix): sys.exit(22)
    source=pathlib.Path(os.environ['FIXTURE_RELEASE']) / url[len(prefix):]
    if not source.is_file(): sys.exit(22)
    shutil.copyfile(source,dest)
''')
        self.asset = 'myapp-Linux-x86_64.tar.gz'
        self.payload = b'#!/bin/sh\nprintf "working fixture\\n"\n'
        self.archive()

    def make_tool(self, name, body):
        path = self.mockbin / name
        path.write_text(f'#!{sys.executable}\n{body}')
        path.chmod(0o755)

    def archive(self, entries=None):
        if entries is None:
            entries = [('myapp', self.payload, tarfile.REGTYPE)]
        with tarfile.open(self.release / self.asset, 'w:gz') as archive:
            for name, content, kind in entries:
                info = tarfile.TarInfo(name)
                info.type = kind
                if kind == tarfile.SYMTYPE:
                    info.linkname = '../outside'
                    archive.addfile(info)
                else:
                    info.size = len(content)
                    archive.addfile(info, io.BytesIO(content))
        self.checksum()

    def checksum(self):
        self.digest = hashlib.sha256((self.release / self.asset).read_bytes()).hexdigest()
        self.write_manifest(f'{self.digest}  {self.asset}\n')
        self.sign(self.release / self.asset)

    def sign(self, path, key=None):
        subprocess.run(['openssl', 'dgst', '-sha256', '-sign', str(key or self.private_key),
                        '-out', str(path) + '.sig', str(path)], check=True,
                       capture_output=True, timeout=10)

    def write_manifest(self, body, version='v1.2.3'):
        path = self.release / 'checksums.txt'
        path.write_text(f'# version {version}\n' + body)
        self.sign(path)

    def run_installer(self):
        return subprocess.run(['sh', str(self.script)], env=self.env,
                              text=True, capture_output=True, timeout=10)

    def assert_rejected(self):
        result = self.run_installer()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.installed.read_bytes(), b'previous working version')
        self.assertEqual(sorted(p.name for p in self.dest.iterdir()), ['myapp'])
        return result

    def test_verified_install_replaces_existing_binary(self):
        result = self.run_installer()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.installed.read_bytes(), self.payload)
        self.assertTrue(os.access(self.installed, os.X_OK))

    def test_latest_version_resolution(self):
        self.env.pop('VERSION')
        result = self.run_installer()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.installed.read_bytes(), self.payload)

    def test_latest_version_with_realistic_json(self):
        self.env.pop('VERSION')
        response = {
            'url': 'https://api.github.com/repos/fixture/example/releases/123',
            'author': {'login': 'fixture', 'tag_name': 'not-the-release'},
            'body': 'Release notes mentioning "tag_name": "not-the-release"',
            'tag_name': 'v1.2.3',
            'assets': [],
        }
        responses = [json.dumps(response), json.dumps(response, indent=2),
                     json.dumps(response).replace('v1.2.3', r'v1\u002e2.3')]
        for raw in responses:
            with self.subTest(response=raw):
                self.env['FIXTURE_RELEASE_JSON'] = raw
                self.installed.write_bytes(b'previous working version')
                result = self.run_installer()
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(self.installed.read_bytes(), self.payload)

    def test_latest_rejects_invalid_response(self):
        self.env.pop('VERSION')
        responses = ['not JSON', '{}', '[]', 'null', '{"tag_name": "v1.2.3"',
                     '{"tag_name": "v1.2.3"} trailing']
        responses.extend(json.dumps({'tag_name': tag}) for tag in
                         [None, 123, True, [], {}, '', '../escape', 'v1.2.3\n'])
        for raw in responses:
            with self.subTest(response=raw):
                self.env['FIXTURE_RELEASE_JSON'] = raw
                result = self.assert_rejected()
                self.assertIn('valid tag_name string', result.stderr)

    def hide_python_from_installer_path(self):
        (self.mockbin / 'python3').unlink()
        # Mock downloads still use their absolute interpreter; only the installer's
        # PATH lacks Python. Provision every other installer dependency explicitly.
        for tool in ('sh', 'awk', 'tar', 'mktemp', 'cp', 'chmod', 'mv', 'openssl',
                     'cat', 'rm', 'mkdir', 'basename', 'sha256sum', 'shasum'):
            source = shutil.which(tool)
            if source:
                (self.mockbin / tool).symlink_to(source)
        self.env['PATH'] = str(self.mockbin)

    def test_latest_requires_json_parser(self):
        self.env.pop('VERSION')
        self.hide_python_from_installer_path()
        result = self.assert_rejected()
        self.assertIn('python3 is required for latest-release discovery', result.stderr)

    def test_explicit_version_does_not_require_json_parser(self):
        self.hide_python_from_installer_path()
        result = self.run_installer()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.installed.read_bytes(), self.payload)

    def test_missing_checksum_file_preserves_existing_install(self):
        (self.release / 'checksums.txt').unlink()
        self.assert_rejected()

    def test_mismatched_checksum(self):
        self.write_manifest(f'{"0" * 64}  {self.asset}\n')
        self.assert_rejected()

    def test_missing_matching_checksum(self):
        self.write_manifest(f'{self.digest}  another.tar.gz\n')
        self.assert_rejected()

    def test_duplicate_checksum(self):
        self.write_manifest(f'{self.digest}  {self.asset}\n' * 2)
        self.assert_rejected()

    def test_malformed_checksum(self):
        self.write_manifest(f'not-a-digest  {self.asset}\n')
        self.assert_rejected()

    def test_binary_marker_checksum(self):
        self.write_manifest(f'{self.digest.upper()} *{self.asset}\n')
        result = self.run_installer()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_path_traversal_member(self):
        self.archive([('../outside', self.payload, tarfile.REGTYPE)])
        self.assert_rejected()
        self.assertFalse((self.root / 'outside').exists())

    def test_symbolic_link_member(self):
        self.archive([('myapp', b'', tarfile.SYMTYPE)])
        self.assert_rejected()

    def test_duplicate_archive_member(self):
        self.archive([('myapp', self.payload, tarfile.REGTYPE)] * 2)
        self.assert_rejected()

    def test_empty_binary(self):
        self.archive([('myapp', b'', tarfile.REGTYPE)])
        self.assert_rejected()

    def test_corrupt_archive_with_matching_checksum(self):
        (self.release / self.asset).write_bytes(b'not an archive')
        self.checksum()
        self.assert_rejected()

    def test_unsupported_architecture(self):
        self.env['FIXTURE_ARCH'] = 'unsupported'
        self.assert_rejected()

    def test_invalid_version(self):
        self.env['VERSION'] = '../../escape'
        self.assert_rejected()

    def test_unconfigured_template(self):
        self.script.write_text(TEMPLATE.read_text())
        self.assert_rejected()

    def test_missing_artifact_signature(self):
        (self.release / (self.asset + '.sig')).unlink()
        self.assert_rejected()

    def test_missing_manifest_signature(self):
        (self.release / 'checksums.txt.sig').unlink()
        self.assert_rejected()

    def test_untrusted_artifact_signer(self):
        self.sign(self.release / self.asset, self.other_key)
        self.assert_rejected()

    def test_untrusted_manifest_signer(self):
        self.sign(self.release / 'checksums.txt', self.other_key)
        self.assert_rejected()

    def test_tampered_payload_with_updated_checksum(self):
        asset = self.release / self.asset
        asset.write_bytes(asset.read_bytes() + b'tampered')
        digest = hashlib.sha256(asset.read_bytes()).hexdigest()
        self.write_manifest(f'{digest}  {self.asset}\n')
        # A matching signed digest cannot substitute for the required artifact signature.
        self.assert_rejected()

    def test_tampered_manifest(self):
        path = self.release / 'checksums.txt'
        path.write_text(path.read_text() + '# changed after signing\n')
        self.assert_rejected()

    def test_signed_wrong_release_version(self):
        self.write_manifest(f'{self.digest}  {self.asset}\n', version='v0.9.0')
        self.assert_rejected()

    def test_missing_trusted_public_key(self):
        self.script.write_text(self.script.read_text().replace(
            self.public_key.strip(), 'REPLACE_WITH_TRUSTED_PUBLISHER_PUBLIC_KEY_PEM'))
        self.assert_rejected()


if __name__ == '__main__':
    unittest.main()

"""Exercise the actual shell installer with local release fixtures; never network."""
import hashlib
import io
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / 'project-bootstrap/assets/install.sh'


class InstallerTests(unittest.TestCase):
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
        self.script.write_text(TEMPLATE.read_text().replace('REPO="OWNER/REPO"', 'REPO="fixture/example"'))
        self.env = dict(os.environ, PATH=f'{self.mockbin}:{os.environ["PATH"]}',
                        INSTALL_DIR=str(self.dest), VERSION='v1.2.3',
                        FIXTURE_RELEASE=str(self.release), FIXTURE_ARCH='x86_64',
                        FIXTURE_OS='Linux')
        self.make_tool('uname', '''import os, sys
print(os.environ['FIXTURE_OS'] if sys.argv[1] == '-s' else os.environ['FIXTURE_ARCH'])
''')
        self.make_tool('curl', '''import os, pathlib, shutil, sys
args=sys.argv[1:]
url=next(a for a in args if a.startswith('https://'))
dest=pathlib.Path(args[args.index('-o')+1])
if url == 'https://api.github.com/repos/fixture/example/releases/latest':
    dest.write_text('{"tag_name": "v1.2.3"}')
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
        (self.release / 'checksums.txt').write_text(f'{self.digest}  {self.asset}\n')

    def run_installer(self):
        return subprocess.run(['sh', str(self.script)], env=self.env,
                              text=True, capture_output=True, timeout=10)

    def assert_rejected(self):
        result = self.run_installer()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.installed.read_bytes(), b'previous working version')
        self.assertEqual(sorted(p.name for p in self.dest.iterdir()), ['myapp'])

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

    def test_missing_checksum_file_preserves_existing_install(self):
        (self.release / 'checksums.txt').unlink()
        self.assert_rejected()

    def test_mismatched_checksum(self):
        (self.release / 'checksums.txt').write_text(f'{"0" * 64}  {self.asset}\n')
        self.assert_rejected()

    def test_missing_matching_checksum(self):
        (self.release / 'checksums.txt').write_text(f'{self.digest}  another.tar.gz\n')
        self.assert_rejected()

    def test_duplicate_checksum(self):
        (self.release / 'checksums.txt').write_text(f'{self.digest}  {self.asset}\n' * 2)
        self.assert_rejected()

    def test_malformed_checksum(self):
        (self.release / 'checksums.txt').write_text(f'not-a-digest  {self.asset}\n')
        self.assert_rejected()

    def test_binary_marker_checksum(self):
        (self.release / 'checksums.txt').write_text(f'{self.digest.upper()} *{self.asset}\n')
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


if __name__ == '__main__':
    unittest.main()

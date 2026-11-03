import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/skill_release.py'
spec = importlib.util.spec_from_file_location('skill_release', SCRIPT)
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / 'skill'
        self.root.mkdir()
        self.registry = self.base / 'registry'
        (self.root / 'VERSION').write_text('1.1.0-dev.1\n')
        (self.root / 'SKILL.md').write_text('original guidance\n')
        (self.root / 'PACKAGE_FILES.json').write_text(json.dumps(['VERSION', 'SKILL.md', 'PACKAGE_FILES.json']))

    def test_fingerprint_detects_edits_but_ignores_cache(self):
        original, _ = release.collect(self.root)
        cache = self.root / '__pycache__'
        cache.mkdir()
        (cache / 'module.pyc').write_bytes(b'cache')
        self.assertEqual(original, release.collect(self.root)[0])
        (self.root / 'SKILL.md').write_text('changed')
        self.assertNotEqual(original['skill_sha256'], release.collect(self.root)[0]['skill_sha256'])

    def test_unexpected_private_files_rejected_before_packaging(self):
        for name in ('.env', 'private-export.csv'):
            with self.subTest(name=name):
                path = self.root / name
                path.write_text('SYNTHETIC ONLY')
                with self.assertRaisesRegex(ValueError, 'unexpected'):
                    release.snapshot(self.root, self.base / 'private.zip')
                self.assertFalse((self.base / 'private.zip').exists())
                path.unlink()

    def test_snapshot_reproduces_bytes_and_original_identity(self):
        first, second = self.base / 'a.zip', self.base / 'b.zip'
        manifest = release.snapshot(self.root, first)
        release.snapshot(self.root, second)
        self.assertEqual(first.read_bytes(), second.read_bytes())
        with zipfile.ZipFile(first) as z:
            z.extractall(self.base / 'restored')
        self.assertEqual(manifest, release.collect(self.base / 'restored/kk-seo-growth')[0])

    def test_publish_verify_rejects_modified_release_and_reused_version(self):
        (self.root / 'VERSION').write_text('1.1.0\n')
        with self.assertRaisesRegex(ValueError, 'unregistered'):
            release.snapshot(self.root, self.base / 'unknown.zip')
        manifest = release.publish(self.root, self.registry)
        self.assertEqual('released', release.verify(self.root, self.registry)['release_status'])
        release.snapshot(self.root, self.base / 'copy.zip', self.registry)
        before = (self.registry / '1.1.0.zip').read_bytes()
        (self.root / 'SKILL.md').write_text('modified')
        with self.assertRaisesRegex(ValueError, 'modified-release'):
            release.verify(self.root, self.registry)
        with self.assertRaisesRegex(ValueError, 'already exists'):
            release.publish(self.root, self.registry)
        self.assertEqual(before, (self.registry / '1.1.0.zip').read_bytes())
        self.assertEqual(manifest, release.verify_registry(self.registry)['1.1.0'])

    def test_archive_corruption_and_missing_pair_rejected(self):
        (self.root / 'VERSION').write_text('1.1.0\n')
        release.publish(self.root, self.registry)
        archive = self.registry / '1.1.0.zip'
        with zipfile.ZipFile(archive, 'a') as z:
            z.writestr('unlisted.txt', 'wrong')
        with self.assertRaisesRegex(ValueError, 'contents mismatch'):
            release.verify_registry(self.registry)
        archive.unlink()
        with self.assertRaisesRegex(ValueError, 'matching manifest'):
            release.verify_registry(self.registry)

    def test_development_is_explicit_and_not_publishable(self):
        self.registry.mkdir()
        self.assertEqual('development', release.verify(self.root, self.registry, True)['release_status'])
        with self.assertRaises(ValueError):
            release.verify(self.root, self.registry)
        with self.assertRaises(ValueError):
            release.publish(self.root, self.registry)

    def test_overwrite_inside_package_symlink_and_bad_listing_rejected(self):
        archive = self.base / 'release.zip'
        release.snapshot(self.root, archive)
        with self.assertRaises(FileExistsError):
            release.snapshot(self.root, archive)
        with self.assertRaises(ValueError):
            release.snapshot(self.root, self.root / 'release.zip')
        (self.root / 'linked.txt').symlink_to(self.root / 'SKILL.md')
        with self.assertRaises(ValueError):
            release.collect(self.root)
        (self.root / 'linked.txt').unlink()
        (self.root / 'PACKAGE_FILES.json').write_text('["../outside"]')
        with self.assertRaises(ValueError):
            release.collect(self.root)

    def test_cli_and_current_registry(self):
        result = subprocess.run([sys.executable, str(SCRIPT), 'identity'], capture_output=True, text=True, check=True)
        identity = json.loads(result.stdout)
        self.assertIn(identity.pop('release_status'), {'released', 'development'})
        self.assertEqual(release.collect(SCRIPT.parents[1])[0], identity)


if __name__ == '__main__':
    unittest.main()

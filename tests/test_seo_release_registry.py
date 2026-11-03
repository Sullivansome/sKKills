"""Repository validation must reject edits hidden behind a released SEO version."""
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest
from scripts.validate_skills import validate

ROOT = Path(__file__).resolve().parents[1]


class RegistryIntegrationTests(unittest.TestCase):
    def test_repo_validator_rejects_changed_release(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            skill = root/'kk-seo-growth'
            shutil.copytree(ROOT/'kk-seo-growth', skill, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            (skill/'VERSION').write_text('9.8.7\n')
            spec = importlib.util.spec_from_file_location('registry_integration', skill/'scripts/skill_release.py')
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            registry = root/'releases/kk-seo-growth'
            module.publish(skill,registry)
            self.assertFalse(any('SEO release verification:' in e for e in validate(root)[0]))
            p = skill/'SKILL.md'
            p.write_text(p.read_text()+'\nSynthetic unversioned edit.\n')
            self.assertTrue(any('modified-release' in e for e in validate(root)[0]))
            (skill/'VERSION').write_text('9.8.8-dev.1\n')
            self.assertFalse(any('SEO release verification:' in e for e in validate(root)[0]))

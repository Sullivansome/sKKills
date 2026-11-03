"""Discover SEO release helper checks in the repository test command."""

import importlib.util
from pathlib import Path


def load_tests(loader, tests, pattern):
    path = Path(__file__).resolve().parents[1] / "kk-seo-growth/tests/test_skill_release.py"
    spec = importlib.util.spec_from_file_location("seo_release_tests", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return loader.loadTestsFromModule(module)

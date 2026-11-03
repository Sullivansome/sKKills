"""Discover SEO traffic validator checks in the repository test command."""

import importlib.util
from pathlib import Path


def load_tests(loader, tests, pattern):
    path = Path(__file__).resolve().parents[1] / "kk-seo-growth/tests/test_validate_traffic.py"
    spec = importlib.util.spec_from_file_location("seo_traffic_tests", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return loader.loadTestsFromModule(module)

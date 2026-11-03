"""Include the independently runnable SEO helper tests in repository CI."""

import importlib.util
from pathlib import Path


def load_tests(loader, tests, pattern):
    path = Path(__file__).resolve().parents[1] / "kk-seo-growth/tests/test_page_inventory.py"
    spec = importlib.util.spec_from_file_location("seo_inventory_tests", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return loader.loadTestsFromModule(module)

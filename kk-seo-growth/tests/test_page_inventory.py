"""Observable HTML inventory and CLI regression checks; no network or browser."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/page_inventory.py"
SPEC = importlib.util.spec_from_file_location("seo_page_inventory", SCRIPT)
inventory = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(inventory)


def parse(html):
    parser = inventory.InventoryParser()
    parser.feed(html)
    parser.close()
    return parser.data


class ParserTests(unittest.TestCase):
    def test_optional_row_and_cell_endings_match_explicit_tags(self):
        expected = [{"table": 0, "text": "Alpha One"}, {"table": 0, "text": "Beta Two"}]
        for html in (
            "<table><tr><td>Alpha</td><td>One</td></tr><tr><td>Beta</td><td>Two</td></tr></table>",
            "<table><tr><td>Alpha</td><td>One</td><tr><td>Beta</td><td>Two</td></table>",
            "<table><tr><td>Alpha<td>One<tr><td>Beta<td>Two</table>",
        ):
            with self.subTest(html=html):
                self.assertEqual(parse(html)["table_rows"], expected)

    def test_table_end_does_not_capture_following_copy(self):
        result = parse("<table><tr><td>Price</td></table><p>Buy now</p>")
        self.assertEqual(result["table_rows"], [{"table": 0, "text": "Price"}])

    def test_row_groups_close_the_previous_row(self):
        for separator in ("</thead><tbody>", "<tbody>"):
            with self.subTest(separator=separator):
                result = parse("<table><thead><tr><th>Plan" + separator + "<tr><td>Basic</tbody></table>")
                self.assertEqual(result["table_rows"], [
                    {"table": 0, "text": "Plan"}, {"table": 0, "text": "Basic"}])

    def test_nested_table_closure_does_not_close_outer_row(self):
        result = parse("<table><tr><td>Outer<table><tr><td>Inner</table>Tail</td></table><p>Outside</p>")
        self.assertEqual(result["table_rows"], [
            {"table": 1, "text": "Inner"}, {"table": 0, "text": "Outer Inner Tail"}])

    def test_inline_markup_preserves_text_boundaries(self):
        result = parse('<h1>micro<strong>phone</strong> &amp; audio</h1><a href="/">down<span>load</span></a>')
        self.assertEqual(result["headings"], [{"level": "h1", "text": "microphone & audio"}])
        self.assertEqual(result["links"][0]["text"], "download")

    def test_block_and_line_breaks_separate_words(self):
        result = parse("<h1>First<br>Second</h1><table><tr><td><p>Alpha</p><p>Beta</p></td><td>Gamma</td></tr></table>")
        self.assertEqual(result["headings"][0]["text"], "First Second")
        self.assertEqual(result["table_rows"][0]["text"], "Alpha Beta Gamma")

    def test_scripts_are_not_visible_text_and_json_ld_remains_exact(self):
        result = parse('<table><tr><td>A<script>ignored()</script><style>.x {color:red}</style><script type="application/ld+json">{"name":"A  B"}</script>B</td></tr></table>')
        self.assertEqual(result["table_rows"], [{"table": 0, "text": "AB"}])
        self.assertEqual(result["json_ld"], [{"name": "A  B"}])
        self.assertEqual(result["json_ld_errors"], [])
        self.assertEqual(len(parse('<script type="application/ld+json">{broken}</script>')["json_ld_errors"]), 1)

    def test_svg_title_is_not_a_document_title(self):
        result = parse('<title>Page</title><svg><title>Logo</title><path/></svg><h1>Hi</h1>')
        self.assertEqual(result["titles"], ["Page"])
        self.assertEqual(result["headings"], [{"level": "h1", "text": "Hi"}])

    def test_json_ld_cdata_and_comment_wrappers_are_stripped(self):
        for body in ('//<![CDATA[\n{"a":1}\n//]]>', '<!--{"a":1}-->', '/*<![CDATA[*/{"a":1}/*]]>*/', ' <!-- <![CDATA[ {"a":1} ]]> --> '):
            with self.subTest(body=body):
                result = parse('<script type="application/ld+json">' + body + '</script>')
                self.assertEqual((result["json_ld"], result["json_ld_errors"]), ([{"a": 1}], []))

    def test_lang_and_hreflang_alternates_are_captured(self):
        result = parse('<html lang="en-GB"><head><link rel="alternate" hreflang="fr" href="/fr/">'
                       '<link rel="alternate" type="application/rss+xml" href="/feed">'
                       '<link rel="alternate" hreflang="x-default" href="/"></head></html>')
        self.assertEqual(result["lang"], ["en-GB"])
        self.assertEqual(result["hreflang"], [{"hreflang": "fr", "href": "/fr/"}, {"hreflang": "x-default", "href": "/"}])

    def test_new_anchor_closes_unclosed_anchor(self):
        result = parse('<a href="/a">One<a href="/b">Two</a> tail')
        self.assertEqual([(l["href"], l["text"]) for l in result["links"]], [("/a", "One"), ("/b", "Two")])


class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="seo-inventory-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def snapshot(self, name, html):
        folder = self.root / name
        folder.mkdir()
        (folder / "index.html").write_text(html, encoding="utf-8")
        output = self.root / f"{name}.json"
        output.write_text(json.dumps(inventory.inventory(folder, 100_000)), encoding="utf-8")
        return output

    def test_formatting_change_preserves_headings_but_word_change_is_flagged(self):
        before = self.snapshot("before", "<h1>micro<strong>phone</strong></h1>")
        same_text = self.snapshot("same", "<h1>microphone</h1>")
        changed = self.snapshot("changed", "<h1>micro phone</h1>")
        self.assertEqual(inventory.compare(before, same_text)["changed_pages"][0]["removed_elements"], {})
        self.assertEqual(inventory.compare(before, changed)["changed_pages"][0]["removed_elements"]["headings"], [
            {"item": {"level": "h1", "text": "microphone"}, "count": 1}])

    def test_removing_one_optional_end_row_reports_only_that_row(self):
        before = self.snapshot("before", "<table><tr><td>Alpha<tr><td>Beta</table>")
        after = self.snapshot("after", "<table><tr><td>Alpha</table>")
        self.assertEqual(inventory.compare(before, after)["changed_pages"][0]["removed_elements"]["table_rows"], [
            {"item": {"table": 0, "text": "Beta"}, "count": 1}])

    def test_cli_metadata_removals_and_invalid_input(self):
        before = self.snapshot("before", '<title>Old</title><a href="/buy">Buy</a><img src="hero.png" alt="Demo">')
        self.snapshot("after", "<title>New</title>")
        generated = self.root / "cli-after.json"
        result = subprocess.run([sys.executable, str(SCRIPT), "inventory", str(self.root / "after"), "--out", str(generated)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        result = subprocess.run([sys.executable, str(SCRIPT), "diff", str(before), str(generated)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        change = json.loads(result.stdout)["changed_pages"][0]
        self.assertEqual(change["metadata_changes"]["titles"], {"before": ["Old"], "after": ["New"]})
        self.assertEqual(set(change["removed_elements"]), {"links", "images"})
        result = subprocess.run([sys.executable, str(SCRIPT), "inventory", str(self.root / "missing")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("Input does not exist", result.stderr)

    def test_declared_charset_is_honoured_and_invalid_bytes_warn(self):
        folder = self.root / "legacy"
        folder.mkdir()
        (folder / "latin.html").write_bytes('<meta charset="iso-8859-1"><title>Café</title>'.encode("latin-1"))
        (folder / "broken.html").write_bytes(b"<title>Caf\xe9</title>")
        pages = inventory.inventory(folder, 100_000)["pages"]
        self.assertEqual((pages["latin.html"]["titles"], pages["latin.html"]["encoding"], pages["latin.html"]["decode_warnings"]),
                         (["Café"], "cp1252", []))
        self.assertEqual(pages["broken.html"]["encoding"], "utf-8")
        self.assertIn("not valid utf-8", pages["broken.html"]["decode_warnings"][0])

    def test_older_snapshot_schema_requires_regeneration(self):
        before = self.snapshot("before", "<title>A</title>")
        data = json.loads(before.read_text(encoding="utf-8"))
        data["schema_version"] = 1
        before.write_text(json.dumps(data), encoding="utf-8")
        after = self.snapshot("after", "<title>B</title>")
        with self.assertRaisesRegex(ValueError, "regenerate both snapshots"):
            inventory.compare(before, after)


if __name__ == "__main__":
    unittest.main()

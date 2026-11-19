#!/usr/bin/env python3
"""Offline static HTML inventory and semantic comparison; performs no network I/O."""

import argparse
import codecs
from collections import Counter
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys

SCHEMA_VERSION = 2
DECLARED_CHARSET = re.compile(rb"<meta[^>]*?charset\s*=\s*[\"']?\s*([A-Za-z0-9_.:-]+)", re.I)
# WHATWG Encoding: these labels decode as windows-1252 in browsers.
WINDOWS_1252_LABELS = {"ascii", "us-ascii", "iso-8859-1", "iso8859-1", "latin1", "latin-1", "l1"}
JSON_LD_OPEN = re.compile(r"\A\s*(?://|/\*)?\s*(?:<!\[CDATA\[|<!--)\s*(?:\*/)?")
JSON_LD_CLOSE = re.compile(r"(?://|/\*)?\s*(?:\]\]>|-->)\s*(?:\*/)?\s*\Z")


def clean(value):
    return " ".join(value.split())


def decode_html(raw):
    """Decode like a browser would for static files: BOM, then declared charset, then UTF-8."""
    warnings = []
    for bom, name in ((codecs.BOM_UTF8, "utf-8-sig"), (codecs.BOM_UTF16_LE, "utf-16"), (codecs.BOM_UTF16_BE, "utf-16")):
        if raw.startswith(bom):
            encoding = name
            break
    else:
        match = DECLARED_CHARSET.search(raw[:4096])
        encoding = match.group(1).decode("ascii").lower() if match else "utf-8"
        if encoding in WINDOWS_1252_LABELS:
            encoding = "cp1252"
        try:
            codecs.lookup(encoding)
        except LookupError:
            warnings.append(f"Unknown declared charset {encoding!r}; decoded as UTF-8")
            encoding = "utf-8"
    try:
        text = raw.decode(encoding)
    except UnicodeDecodeError as error:
        warnings.append(f"Bytes are not valid {encoding} (first at offset {error.start}); undecodable bytes replaced")
        text = raw.decode(encoding, errors="replace")
    return text, encoding, warnings


def json_ld_text(raw):
    """Strip CDATA/comment wrappers that CMSs put around JSON-LD script bodies."""
    text, previous = raw, None
    while text != previous:
        previous = text
        text = JSON_LD_CLOSE.sub("", JSON_LD_OPEN.sub("", text, count=1), count=1)
    return text


class InventoryParser(HTMLParser):
    # Structural boundaries separate words; inline elements preserve adjacency.
    # This is a text inventory, not a CSS-aware HTML5 rendering implementation.
    TEXT_BOUNDARIES = frozenset({
        "address", "article", "aside", "blockquote", "br", "dd", "div", "dl", "dt",
        "fieldset", "figcaption", "figure", "footer", "form", "h1", "h2", "h3",
        "h4", "h5", "h6", "header", "hr", "li", "main", "nav", "ol", "p", "pre",
        "section", "table", "tbody", "td", "tfoot", "th", "thead", "tr", "ul",
    })

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.data = {
            "titles": [], "descriptions": [], "canonicals": [], "robots": [],
            "headings": [], "links": [], "images": [], "table_rows": [],
            "table_count": 0, "json_ld": [], "json_ld_errors": [],
            "lang": [], "hreflang": [],
        }
        self.captures = []
        self.tables = []
        self.suppressed = 0
        self.svg_depth = 0

    def finish_current_row(self):
        """Apply optional row endings within the current table only."""
        table = self.tables[-1] if self.tables else None
        for index in range(len(self.captures) - 1, -1, -1):
            capture = self.captures[index]
            if capture["tag"] == "tr" and capture["table"] == table:
                self.finish(self.captures.pop(index))
                break

    def text_boundary(self, tag):
        if not self.suppressed and tag in self.TEXT_BOUNDARIES:
            for capture in self.captures:
                if capture["tag"] != "script":
                    capture["parts"].append(" ")

    def handle_starttag(self, tag, attrs):
        if tag in ("tr", "thead", "tbody", "tfoot"):
            self.finish_current_row()
        self.text_boundary(tag)
        attrs = dict(attrs)
        if tag == "svg":
            self.svg_depth += 1
        elif tag == "a":
            # Anchors cannot nest; a new <a> ends any open one, as browsers do.
            for index in range(len(self.captures) - 1, -1, -1):
                if self.captures[index]["tag"] == "a":
                    self.finish(self.captures.pop(index))
                    break
        if tag == "html" and attrs.get("lang") is not None:
            self.data["lang"].append(attrs["lang"])
        if tag == "meta":
            name = (attrs.get("name") or "").lower()
            if name == "description":
                self.data["descriptions"].append(attrs.get("content", ""))
            if name in ("robots", "googlebot", "bingbot"):
                self.data["robots"].append({"name": name, "content": attrs.get("content", "")})
        elif tag == "link" and "canonical" in (attrs.get("rel") or "").lower().split():
            self.data["canonicals"].append(attrs.get("href", ""))
        elif (tag == "link" and "alternate" in (attrs.get("rel") or "").lower().split()
              and attrs.get("hreflang")):
            self.data["hreflang"].append({"hreflang": attrs["hreflang"], "href": attrs.get("href", "")})
        elif tag == "img":
            self.data["images"].append({
                key: attrs.get(key) for key in ("src", "srcset", "alt", "width", "height")
            })
        elif tag == "table":
            self.tables.append(self.data["table_count"])
            self.data["table_count"] += 1

        is_ld = tag == "script" and (attrs.get("type") or "").lower().strip() == "application/ld+json"
        if tag in ("script", "style") and not is_ld:
            self.suppressed += 1
        # An SVG <title> is an image tooltip, not the document title.
        captured = ("h1", "h2", "h3", "h4", "h5", "h6", "a", "tr") + (() if self.svg_depth else ("title",))
        if tag in captured or is_ld:
            self.captures.append({
                "tag": tag, "attrs": attrs, "parts": [],
                "table": self.tables[-1] if self.tables else None,
            })

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_data(self, value):
        if not self.suppressed:
            # JSON-LD belongs to its own capture, never surrounding visible text.
            captures = (self.captures[-1:] if self.captures and self.captures[-1]["tag"] == "script"
                        else self.captures)
            for capture in captures:
                capture["parts"].append(value)

    def handle_endtag(self, tag):
        if tag in ("table", "thead", "tbody", "tfoot"):
            self.finish_current_row()
        self.text_boundary(tag)
        index = next((i for i in range(len(self.captures) - 1, -1, -1)
                      if self.captures[i]["tag"] == tag), None)
        if index is not None:
            capture = self.captures.pop(index)
            self.finish(capture)
        elif tag in ("script", "style") and self.suppressed:
            self.suppressed -= 1
        if tag == "table" and self.tables:
            self.tables.pop()
        if tag == "svg" and self.svg_depth:
            self.svg_depth -= 1

    def finish(self, capture):
        tag, attrs = capture["tag"], capture["attrs"]
        text = clean("".join(capture["parts"]))
        if tag == "title":
            self.data["titles"].append(text)
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.data["headings"].append({"level": tag, "text": text})
        elif tag == "a":
            self.data["links"].append({
                "href": attrs.get("href"), "text": text,
                "rel": attrs.get("rel"), "aria_label": attrs.get("aria-label"),
            })
        elif tag == "tr":
            self.data["table_rows"].append({"table": capture["table"], "text": text})
        elif tag == "script":
            raw = json_ld_text("".join(capture["parts"]))
            try:
                self.data["json_ld"].append(json.loads(raw))
            except (ValueError, TypeError) as error:
                self.data["json_ld_errors"].append(str(error))

    def close(self):
        super().close()
        # Preserve observable text from unfinished capture tags, without claiming valid HTML.
        for capture in self.captures:
            self.finish(capture)
        self.captures.clear()


def inventory(path, max_bytes):
    root = Path(path).resolve()
    if not root.exists():
        raise ValueError(f"Input does not exist: {root}")
    if root.is_file():
        files = [root]
        parent = root.parent
    else:
        files = sorted(p for p in root.rglob("*")
                       if p.is_file() and not p.is_symlink()
                       and p.suffix.lower() in (".html", ".htm")
                       and p.resolve().is_relative_to(root))
        parent = root
    if not files:
        raise ValueError("No .html or .htm files found")
    pages = {}
    for file in files:
        if file.stat().st_size > max_bytes:
            raise ValueError(f"HTML exceeds --max-bytes: {file}")
        raw = file.read_bytes()
        text, encoding, warnings = decode_html(raw)
        parser = InventoryParser()
        parser.feed(text)
        parser.close()
        pages[file.relative_to(parent).as_posix()] = {
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw), "encoding": encoding, "decode_warnings": warnings, **parser.data,
        }
    return {"schema_version": SCHEMA_VERSION, "kind": "static-html-inventory", "pages": pages,
            "limitations": "Static HTML files only (BOM or declared charset, else UTF-8); no HTTP Content-Type, network, rendering, indexing, truth or conversion verification."}


def removed_values(old, new):
    encode = lambda item: json.dumps(item, ensure_ascii=False, sort_keys=True)
    removed = Counter(map(encode, old)) - Counter(map(encode, new))
    return [{"item": json.loads(item), "count": count} for item, count in sorted(removed.items())]


def read_snapshot(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("kind") != "static-html-inventory" or not isinstance(data.get("pages"), dict):
        raise ValueError(f"Not a supported inventory: {path}")
    if data.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(f"Inventory schema {data.get('schema_version')} != {SCHEMA_VERSION}: regenerate both snapshots with this helper version: {path}")
    return data["pages"]


def compare(before, after):
    old, new = read_snapshot(before), read_snapshot(after)
    changes = []
    for page in sorted(old.keys() & new.keys()):
        a, b = old[page], new[page]
        if a["sha256"] == b["sha256"]:
            continue
        change = {"page": page, "metadata_changes": {}, "removed_elements": {},
                  "json_ld_errors_after": b["json_ld_errors"],
                  "decode_warnings_after": b["decode_warnings"]}
        for key in ("titles", "descriptions", "canonicals", "robots", "lang", "hreflang"):
            if a[key] != b[key]:
                change["metadata_changes"][key] = {"before": a[key], "after": b[key]}
        for key in ("headings", "links", "images", "table_rows", "json_ld"):
            missing = removed_values(a[key], b[key])
            if missing:
                change["removed_elements"][key] = missing
        if a["table_count"] != b["table_count"]:
            change["table_count_change"] = {"before": a["table_count"], "after": b["table_count"]}
        changes.append(change)
    return {"schema_version": 1, "kind": "static-html-diff",
            "pages_removed": sorted(old.keys() - new.keys()),
            "pages_added": sorted(new.keys() - old.keys()), "changed_pages": changes,
            "limitations": "Review flags, not an automatic pass/fail. Reworded elements can appear removed. Inspect source diff and rendered page."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    inv = commands.add_parser("inventory", help="Inventory a local HTML file or tree")
    inv.add_argument("path")
    inv.add_argument("--max-bytes", type=int, default=4 * 1024 * 1024)
    inv.add_argument("--out")
    diff = commands.add_parser("diff", help="Compare two inventory JSON files")
    diff.add_argument("before")
    diff.add_argument("after")
    diff.add_argument("--out")
    args = parser.parse_args()
    try:
        result = inventory(args.path, args.max_bytes) if args.command == "inventory" else compare(args.before, args.after)
        output = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        if args.out:
            destination = Path(args.out)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(output, encoding="utf-8")
        else:
            sys.stdout.write(output)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

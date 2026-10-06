#!/usr/bin/env python3
"""Inline shared CSS/JS into each page so every output HTML file is self-contained.

Source pages live in src/ and contain markers such as

    <style>/*@include shared/base.css*/ /*@include ostep/theme.css*/</style>
    <script>/*@include shared/base.js*/</script>

Paths are relative to src/. Output mirrors src/ under docs/.
Usage: python3 tools/build.py            # build every page
       python3 tools/build.py ostep/chapter-01.html
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
OUT = ROOT / "docs"
MARKER = re.compile(r"/\*@include\s+([\w./-]+)\s*\*/")


def build(page: pathlib.Path) -> pathlib.Path:
    html = page.read_text(encoding="utf-8")
    html = MARKER.sub(lambda m: (SRC / m.group(1)).read_text(encoding="utf-8"), html)
    dest = OUT / page.relative_to(SRC)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html, encoding="utf-8")
    return dest


def main() -> None:
    pages = [SRC / p for p in sys.argv[1:]] or sorted(
        p for p in SRC.rglob("*.html") if "shared" not in p.parts
    )
    for p in pages:
        print("built", build(p).relative_to(ROOT))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Point photoviewer.ashx references at the production host (not static). Run: python3 scripts/fix_photoviewer_urls.py"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "docs"
ABS = "https://www.pacificdentalalliance.com/photoviewer.ashx"


def fix(text: str) -> str:
    text = re.sub(
        r"url\(\s*/photoviewer\.ashx",
        f"url({ABS}",
        text,
        flags=re.I,
    )
    text = re.sub(
        r'(["\'])(?:\.\./)+photoviewer\.ashx([^"\']*)',
        rf"\1{ABS}\2",
        text,
        flags=re.I,
    )
    text = re.sub(
        r'(["\'])/photoviewer\.ashx([^"\']*)',
        rf"\1{ABS}\2",
        text,
        flags=re.I,
    )
    return text


def main() -> None:
    for p in ROOT.rglob("*.html"):
        raw = p.read_text(encoding="utf-8", errors="replace")
        new = fix(raw)
        if new != raw:
            p.write_text(new, encoding="utf-8")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Recover static files from the live Pacific Dental Alliance site into docs/
for GitHub Pages. Run from repo root: python3 scripts/recover_site.py
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import ssl
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://www.pacificdentalalliance.com"
ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
# Allow crawled paths (same host only)
FETCHED: dict[str, tuple[int, str]] = {}  # path -> (status, content_type or "binary")

CTX = ssl.create_default_context()

ATTR_RE = re.compile(
    r"""(?P<attr>href|src)\s*=\s*(?P<q>['"])(?P<val>.*?)(?P=q)""",
    re.I | re.S,
)
CSS_URL_RE = re.compile(r"""url\(\s*(?P<q>['"]?)(?P<u>[^)'"]+)(?P=q)\s*\)""", re.I)


def norm_path(path: str) -> str:
    if not path or path.startswith(("mailto:", "tel:", "javascript:", "#")):
        return ""
    p = urllib.parse.urlparse(path)
    if p.scheme and p.netloc:
        if p.netloc.replace("www.", "") != "pacificdentalalliance.com":
            return ""
        path = p.path or "/"
    if not path.startswith("/"):
        return ""
    path = urllib.parse.unquote(path)
    if ".." in path:
        return ""
    return path.rstrip("/") or "/"


def is_probably_html(path: str, content_type: str) -> bool:
    if "text/html" in content_type:
        return True
    if path in ("/", "/about", "/locations", "/group-programs", "/contact"):
        return True
    if path.endswith("/"):
        return True
    ext = Path(path).suffix.lower()
    return ext in (".html", ".htm", ".php", ".aspx")


def url_path_to_doc_relpath(url_path: str) -> str:
    """Map site path to path under docs/ (posix)."""
    p = url_path.rstrip("/") or "/"
    if p == "/":
        return "index.html"
    if p.startswith("/_assets/") or p == "/favicon.ico":
        return p.lstrip("/")
    # section pages -> section/index.html
    name = p.lstrip("/")
    if "." in name.split("/")[-1]:
        return name
    return f"{name}/index.html"


def fetch(path: str) -> tuple[int, bytes, str]:
    raw = path if path.startswith("/") else "/" + path
    parts = raw.split("/")
    encoded = "/".join(urllib.parse.quote(p, safe="") if p else "" for p in parts)
    if not encoded.startswith("/"):
        encoded = "/" + encoded
    url = BASE + encoded
    req = urllib.request.Request(url, headers={"User-Agent": "PDA-site-recovery/1.0"})
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=60) as resp:
            status = resp.status
            ct = resp.headers.get("Content-Type", "").split(";")[0].strip()
            return status, resp.read(), ct
    except urllib.error.HTTPError as e:
        return e.code, e.read() if e.fp else b"", ""
    except urllib.error.URLError as e:
        return 0, str(e).encode(), ""


def write_doc(rel: str, data: bytes, binary: bool) -> None:
    out = DOCS / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    if binary:
        out.write_bytes(data)
    else:
        text = data.decode("utf-8", errors="replace")
        out.write_text(text, encoding="utf-8")


def rel_href(from_doc: str, target_url_path: str) -> str:
    """Relative link from one doc file to another URL path on site."""
    from_p = Path(from_doc)
    to_rel = url_path_to_doc_relpath(target_url_path)
    target = Path(to_rel)
    r = os.path.relpath(target, from_p.parent)
    return Path(r).as_posix()


def normalize_page_path(np: str) -> str:
    """Normalize internal page paths to canonical form with trailing slash."""
    if np == "/":
        return "/"
    if np in ("/about", "/about/"):
        return "/about/"
    if np in ("/locations", "/locations/"):
        return "/locations/"
    if np in ("/group-programs", "/group-programs/"):
        return "/group-programs/"
    if np in ("/contact", "/contact/"):
        return "/contact/"
    if np.endswith("/") or Path(np).suffix:
        return np
    if np.count("/") == 1:
        return np + "/"
    return np


def rewrite_html(html: str, from_doc: str) -> str:
    def sub(m: re.Match) -> str:
        attr, q, val = m.group("attr"), m.group("q"), m.group("val")
        raw = val.strip()
        if raw.startswith("#"):
            return m.group(0)
        # Same-dir links from production bug e.g. href="locations/"
        if attr.lower() == "href" and re.match(r"^[a-z0-9_-]+/", raw, re.I):
            return m.group(0)
        np = norm_path(raw)
        if not np:
            return m.group(0)
        if np.startswith("/_assets/") or np == "/favicon.ico":
            new = rel_href(from_doc, np)
            return f'{attr}={q}{new}{q}'
        if is_probably_html(np, "text/html"):
            np = normalize_page_path(np)
            new = rel_href(from_doc, np)
            return f'{attr}={q}{new}{q}'
        return m.group(0)

    return ATTR_RE.sub(sub, html)


def extract_paths_from_html(html: str) -> set[str]:
    out: set[str] = set()
    for m in ATTR_RE.finditer(html):
        val = m.group("val").strip()
        np = norm_path(val)
        if np:
            out.add(np if np != "/" else "/")
    return out


def skip_crawl_path(path: str) -> bool:
    """Skip server-only or non-static URLs (robots.txt also disallows some of these)."""
    p = path.split("?")[0].lower()
    if "photoviewer.ashx" in p:
        return True
    if p.startswith("/_review/") or p.startswith("/secure/") or p.startswith("/account/"):
        return True
    if p.startswith("/error/"):
        return True
    return False


def extract_paths_from_css(css: str, css_url_path: str) -> set[str]:
    out: set[str] = set()
    base_dir = str(Path(css_url_path).parent.as_posix())
    if not base_dir.startswith("/"):
        base_dir = "/" + base_dir

    for m in CSS_URL_RE.finditer(css):
        u = m.group("u").strip().strip("'\"")
        if u.startswith("data:") or u.startswith("#"):
            continue
        if u.startswith("http"):
            continue
        if u.startswith("/"):
            out.add(urllib.parse.unquote(u.split("?")[0]))
        else:
            joined = urllib.parse.urljoin(BASE + css_url_path, u)
            p = urllib.parse.urlparse(joined)
            if p.netloc.endswith("pacificdentalalliance.com"):
                out.add(urllib.parse.unquote(p.path.split("?")[0]))
    return out


def main() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")

    queue: list[str] = []
    seen: set[str] = set()
    html_paths: set[str] = set()
    asset_paths: set[str] = set()

    seeds = [
        "/",
        "/about/",
        "/locations/",
        "/group-programs/",
        "/contact/",
        "/favicon.ico",
    ]
    for s in seeds:
        if s not in seen:
            seen.add(s)
            queue.append(s)

    # BFS pages + collect assets
    while queue:
        path = queue.pop(0)
        status, data, ct = fetch(path)
        FETCHED[path] = (status, ct or "unknown")

        if status != 200:
            continue

        ct_low = ct.lower()
        text_like = (
            "text/" in ct_low
            or "javascript" in ct_low
            or "json" in ct_low
            or path.endswith((".css", ".js", ".svg", ".html", ".htm", ".xml", ".txt"))
        )
        is_bin = not text_like

        if is_probably_html(path, ct):
            html_paths.add(path)
            text = data.decode("utf-8", errors="replace")
            for np in extract_paths_from_html(text):
                if skip_crawl_path(np):
                    continue
                if np.startswith("/_assets/") or np == "/favicon.ico":
                    if np not in seen:
                        seen.add(np)
                        queue.append(np)
                elif np.startswith("/") and not np.startswith("//"):
                    if np not in seen:
                        seen.add(np)
                        queue.append(np)
            doc_rel = url_path_to_doc_relpath(path)
            write_doc(doc_rel, data, binary=False)
        else:
            doc_rel = url_path_to_doc_relpath(path)
            write_doc(doc_rel, data, binary=is_bin)

    # CSS url() assets (repeat until stable — nested font references)
    while True:
        extra: set[str] = set()
        for cf in DOCS.glob("_assets/**/*.css"):
            rel_site = "/" + cf.relative_to(DOCS).as_posix()
            text = cf.read_text(encoding="utf-8", errors="replace")
            extra |= extract_paths_from_css(text, rel_site)
        new_paths = [p for p in extra if p not in FETCHED and not skip_crawl_path(p)]
        if not new_paths:
            break
        for p in new_paths:
            status, data, ct = fetch(p)
            FETCHED[p] = (status, ct or "unknown")
            if status != 200:
                continue
            ct_low = (ct or "").lower()
            text_like = "text/" in ct_low or "javascript" in ct_low or p.endswith(
                (".css", ".js", ".svg", ".html", ".htm")
            )
            write_doc(url_path_to_doc_relpath(p), data, binary=not text_like)

    # Rewrite all HTML
    for html_file in DOCS.rglob("*.html"):
        from_doc = html_file.relative_to(DOCS).as_posix()
        raw = html_file.read_text(encoding="utf-8", errors="replace")
        html_file.write_text(rewrite_html(raw, from_doc), encoding="utf-8")

    subprocess.run([sys.executable, str(ROOT / "scripts/fix_photoviewer_urls.py")], check=True)

    # Log
    log_lines = ["# Fetch log (path, status, content-type)\n"]
    for k in sorted(FETCHED.keys()):
        st, ct = FETCHED[k]
        log_lines.append(f"- `{k}` → {st} ({ct})\n")
    (ROOT / "SITE_RECOVERY_LOG.md").write_text("".join(log_lines), encoding="utf-8")


if __name__ == "__main__":
    main()

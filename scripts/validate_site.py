#!/usr/bin/env python3
"""
validate_site.py — local structural/SEO checks for the SYJ Mining Platform
static site. No network access, no external dependencies beyond the
standard library. Exits non-zero if any check fails.

Usage:
    python3 scripts/validate_site.py
"""
import re
import sys
import json
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAILS = []
WARNS = []


def fail(msg):
    FAILS.append(msg)


def warn(msg):
    WARNS.append(msg)


def read(path):
    p = ROOT / path
    if not p.exists():
        fail(f"missing file: {path}")
        return ""
    return p.read_text(encoding="utf-8")


def check_index():
    html = read("index.html")
    if not html:
        return

    if not re.search(r"<title>.*?</title>", html, re.S):
        fail("index.html: <title> missing")

    if 'name="description"' not in html:
        fail("index.html: meta description missing")

    if 'rel="canonical"' not in html:
        fail("index.html: canonical link missing")

    h1_matches = re.findall(r"<h1[\s>]", html)
    if len(h1_matches) == 0:
        fail("index.html: no <h1> found")
    elif len(h1_matches) > 1:
        fail(f"index.html: multiple <h1> tags found ({len(h1_matches)}) — should be exactly one")

    if 'property="og:title"' not in html:
        fail("index.html: Open Graph title missing")
    if 'property="og:description"' not in html:
        fail("index.html: Open Graph description missing")

    if 'name="twitter:card"' not in html:
        fail("index.html: Twitter/X card metadata missing")

    if 'rel="icon"' not in html:
        fail("index.html: favicon link missing")

    if 'rel="manifest"' not in html:
        fail("index.html: web manifest link missing")

    if "application/ld+json" not in html:
        fail("index.html: JSON-LD structured data missing")
    else:
        ld_blocks = re.findall(
            r'<script type="application/ld\+json">(.*?)</script>', html, re.S
        )
        for block in ld_blocks:
            try:
                json.loads(block)
            except json.JSONDecodeError as e:
                fail(f"index.html: invalid JSON-LD ({e})")

    if 'lang="en"' not in html.split(">")[0] and "<html lang=" not in html[:200]:
        warn("index.html: <html lang> attribute not found near top of file")

    if 'name="viewport"' not in html:
        fail("index.html: viewport meta missing")

    required_sections = [
        "hero", "platform", "technology", "status", "randomx",
        "verification", "security", "performance", "power",
        "architecture", "roadmap", "source", "faq",
    ]
    for sec in required_sections:
        if f'id="{sec}"' not in html:
            fail(f"index.html: required section id missing: #{sec}")

    ids = re.findall(r'\bid="([^"]+)"', html)
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        fail(f"index.html: duplicate element IDs found: {sorted(dupes)}")

    placeholder_markers = ["lorem ipsum", "TODO", "FIXME", "XXX", "TBD"]
    for marker in placeholder_markers:
        if marker.lower() in html.lower():
            fail(f"index.html: placeholder/TODO marker found: {marker}")

    fake_claim_markers = [
        "world's fastest", "most profitable", "guaranteed profit",
        "industry-leading", "revolutionary",
    ]
    for marker in fake_claim_markers:
        if marker.lower() in html.lower():
            fail(f"index.html: unsupported marketing claim found: '{marker}'")

    # internal anchor link sanity check
    anchors = re.findall(r'href="#([a-zA-Z0-9\-_]+)"', html)
    for a in anchors:
        if f'id="{a}"' not in html:
            fail(f"index.html: internal link points to missing anchor #{a}")


def check_robots():
    txt = read("robots.txt")
    if not txt:
        return
    if "sitemap" not in txt.lower():
        fail("robots.txt: does not reference sitemap.xml")
    if "disallow: /" in txt.lower().replace(" ", ""):
        warn("robots.txt: broad Disallow rule detected — confirm this is intentional")


def check_sitemap():
    txt = read("sitemap.xml")
    if not txt:
        return
    try:
        root = ET.fromstring(txt)
    except ET.ParseError as e:
        fail(f"sitemap.xml: invalid XML ({e})")
        return
    locs = [el.text for el in root.iter() if el.tag.endswith("loc")]
    if not locs:
        fail("sitemap.xml: no <loc> entries found")
    for loc in locs:
        if loc and "example.com" in loc:
            fail(f"sitemap.xml: placeholder domain left in URL: {loc}")


def check_manifest_and_icons():
    manifest = read("site.webmanifest")
    if manifest:
        try:
            json.loads(manifest)
        except json.JSONDecodeError as e:
            fail(f"site.webmanifest: invalid JSON ({e})")
    if not (ROOT / "favicon.svg").exists():
        fail("favicon.svg missing")


def check_no_placeholder_urls():
    for path in ["index.html", "robots.txt", "sitemap.xml", "SEO/structured-data.json", "README.md"]:
        content = read(path)
        if "example.com" in content and path != "CNAME.example":
            fail(f"{path}: placeholder 'example.com' URL left in production file")


def main():
    check_index()
    check_robots()
    check_sitemap()
    check_manifest_and_icons()
    check_no_placeholder_urls()

    print(f"Checked project at: {ROOT}\n")

    if WARNS:
        print(f"WARNINGS ({len(WARNS)}):")
        for w in WARNS:
            print(f"  - {w}")
        print()

    if FAILS:
        print(f"FAILURES ({len(FAILS)}):")
        for f in FAILS:
            print(f"  - {f}")
        print("\nvalidate_site.py: FAILED")
        sys.exit(1)

    print("validate_site.py: all checks passed")
    sys.exit(0)


if __name__ == "__main__":
    main()

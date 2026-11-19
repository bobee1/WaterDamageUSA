#!/usr/bin/env python3
"""Site audit for DryBeacon: run after build.py. Exits 1 if any check fails.

Checks: internal links resolve, unique titles/metas/H1s, length limits, one H1,
no skipped heading levels, image alt + width/height + WebP + size, banned wording,
single phone number, valid JSON-LD, unreplaced template tokens, page weight.
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / "public"
SITE = json.loads((ROOT / "src" / "site.json").read_text())

# Own-business site: 24/7 and years in business are approved claims. Everything else stays banned.
BANNED = ["certified", "iicrc-certified", "licensed technician", "insured and bonded", "5-star", "five-star",
          "award-winning", "minutes away", "60 minutes", "free estimate", "based in", "home base",
          "placeholder", "lorem", "coming soon", "example.com", "[placeholder]", "guaranteed arrival"]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.imgs, self.heads, self.ld = [], [], [], []
        self.title, self.meta, self._in, self._buf, self.text = "", "", None, "", []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "img":
            self.imgs.append(a)
        if tag == "meta" and a.get("name") == "description":
            self.meta = a.get("content", "")
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.heads.append(int(tag[1]))
        if tag == "title":
            self._in = "title"
        if tag == "script" and a.get("type") == "application/ld+json":
            self._in, self._buf = "ld", ""
        if tag in ("script", "style"):
            self._skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self._skip -= 1
        if self._in == "ld" and tag == "script":
            self.ld.append(self._buf)
        if tag in ("title", "script"):
            self._in = None

    def handle_data(self, data):
        if self._in == "title":
            self.title += data
        elif self._in == "ld":
            self._buf += data
        elif not self._skip:
            self.text.append(data)


WORDS = {}


def main():
    # Pages scheduled for a later build (see STATUS.md). Links to them are reported, not failed.
    pending_file = ROOT / "docs" / "pending-pages.txt"
    pending = {l.strip() for l in pending_file.read_text().splitlines() if l.strip() and not l.startswith("#")} \
        if pending_file.exists() else set()
    pending_hits = set()
    problems, titles, metas, h1s = [], {}, {}, {}
    files = sorted(PUB.rglob("*.html"))
    for f in files:
        rel = "/" + str(f.relative_to(PUB)).replace("index.html", "")
        raw = f.read_text()
        p = Page()
        p.feed(raw)
        text = " ".join(p.text)
        low = (text + " " + " ".join(i.get("alt", "") for i in p.imgs)).lower()
        is404 = rel == "/404.html"

        if "{{" in raw:
            problems.append((rel, "unreplaced template token"))
        if len(p.title) > 60:
            problems.append((rel, f"title {len(p.title)} chars > 60"))
        if not 70 <= len(p.meta) <= 155:
            problems.append((rel, f"meta description {len(p.meta)} chars (want 70-155)"))
        titles.setdefault(p.title, []).append(rel)
        metas.setdefault(p.meta, []).append(rel)
        if p.heads.count(1) != 1:
            problems.append((rel, f"{p.heads.count(1)} H1 tags"))
        for a, b in zip(p.heads, p.heads[1:]):
            if b > a + 1:
                problems.append((rel, f"heading jumps h{a} -> h{b}"))
        h1 = re.search(r"<h1>(.*?)</h1>", raw, re.S)
        if h1:
            h1s.setdefault(h1.group(1), []).append(rel)
        for href in p.links:
            if href.startswith(("http", "tel:", "mailto:", "#")):
                if href.startswith("tel:") and href != "tel:" + SITE["phone_e164"]:
                    problems.append((rel, f"unexpected phone link {href}"))
                continue
            path = href.split("#")[0]
            target = PUB / path.lstrip("/")
            if not (target.is_file() or (target / "index.html").is_file()):
                if path in pending:
                    pending_hits.add(path)
                else:
                    problems.append((rel, f"broken link {href}"))
        for img in p.imgs:
            if not img.get("alt"):
                problems.append((rel, f"img missing alt {img.get('src')}"))
            if not (img.get("width") and img.get("height")):
                problems.append((rel, f"img missing width/height {img.get('src')}"))
            src = img.get("src", "")
            if not (src.endswith(".webp") or src.startswith("/img/brand/") and src.endswith(".svg")):
                problems.append((rel, f"img not WebP (or brand SVG) {src}"))
            imgf = PUB / src.lstrip("/")
            if not imgf.is_file():
                problems.append((rel, f"img file missing {src}"))
            elif imgf.stat().st_size > 200_000:
                problems.append((rel, f"img over 200 KB {src}"))
        for word in BANNED:
            if word in low:
                problems.append((rel, f"banned wording: '{word}'"))
        phones = set(re.findall(r"1-\d{3}-\d{3}-\d{4}|\(\d{3}\) ?\d{3}-\d{4}", text))
        if phones - {SITE["phone_display"]}:
            problems.append((rel, f"other phone numbers {phones}"))
        for block in p.ld:
            try:
                json.loads(block)
            except json.JSONDecodeError as e:
                problems.append((rel, f"invalid JSON-LD {e}"))
        main = re.search(r'<div class="wrap content[^"]*">(.*?)</div>\s*(?:<section class="cta-band"|</main>)', raw, re.S)
        hero = re.search(r'<section class="hero.*?</section>', raw, re.S)
        words = len(re.sub(r"<[^>]+>", " ", (hero.group(0) if hero else "") + (main.group(1) if main else "")).split())
        kind = re.search(r'<meta name="x-page-type" content="(\w+)">', raw)
        kind = kind.group(1) if kind else "other"
        limits = {"home": (1200, 1800), "service": (1000, 1700), "hub": (300, 1200)}
        if kind in limits and not limits[kind][0] <= words <= limits[kind][1]:
            problems.append((rel, f"{kind} page has {words} words (want {limits[kind][0]}-{limits[kind][1]})"))
        WORDS[rel] = (kind, words)
        if len(raw.encode()) > 100_000:
            problems.append((rel, f"HTML {len(raw)//1024} KB > 100 KB"))
        if not is404 and 'rel="canonical"' not in raw:
            problems.append((rel, "missing canonical"))

    for label, d in (("title", titles), ("meta", metas), ("H1", h1s)):
        for k, v in d.items():
            if len(v) > 1:
                problems.append((", ".join(v), f"duplicate {label}"))

    print(f"Audited {len(files)} pages")
    for r, (k, w) in sorted(WORDS.items()):
        if k in ("home", "service", "hub"):
            print(f"  words {w:5d}  {k:8s} {r}")
    for path in sorted(pending_hits):
        print(f"PENDING link target (scheduled in a later build): {path}")
    for where, what in problems:
        print(f"FAIL {where}: {what}")
    if problems:
        sys.exit(1)
    print("PASS: 0 issues")


if __name__ == "__main__":
    main()

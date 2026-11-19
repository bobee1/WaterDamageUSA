#!/usr/bin/env python3
"""Location-page uniqueness: 5-word shingles, each page vs every other page of the same type.
Unique % = share of a page's shingles that do not appear in the compared page. Rule: worst pair >= 60%.
Auto sections (service cards, pills, state grid, source list) are excluded; they are navigation."""
import glob, re, sys
from pathlib import Path

PUB = Path(__file__).resolve().parent.parent / "public"
TYPE = sys.argv[1] if len(sys.argv) > 1 else "state"

def shingles(html):
    m = re.search(r'<div class="content[^"]*">(.*?)</div>\s*<aside class="sidebar"', html, re.S)
    hero = re.search(r'<section class="hero.*?</section>', html, re.S)
    body = (hero.group(0) if hero else "") + (m.group(1) if m else "")
    for pat in (r'<div class="card">[\s\S]*?</div>', r'<ul class="pills[\s\S]*?</ul>', r'<ul class="state-grid[\s\S]*?</ul>',
                r'<ul class="sources">[\s\S]*?</ul>', r'<div class="cta-box">[\s\S]*?</div>'):
        body = re.sub(pat, " ", body)
    words = re.findall(r"[a-z0-9']+", re.sub(r"<[^>]+>", " ", body).lower())
    return {" ".join(words[i:i + 5]) for i in range(len(words) - 4)}

pages = {}
for f in glob.glob(str(PUB / "**/index.html"), recursive=True):
    raw = open(f).read()
    if f'content="{TYPE}"' in raw:
        pages["/" + str(Path(f).relative_to(PUB)).replace("index.html", "")] = shingles(raw)
worst = []
for a, sa in pages.items():
    w = min(((1 - len(sa & sb) / len(sa)) * 100, b) for b, sb in pages.items() if b != a)
    worst.append((w[0], a, w[1]))
worst.sort()
for u, a, b in worst[:8]:
    print(f"{u:5.1f}% unique  {a}  (closest: {b})")
avg = sum(x[0] for x in worst) / len(worst)
print(f"{len(worst)} {TYPE} pages; average worst-pair uniqueness {avg:.1f}%")
bad = [x for x in worst if x[0] < 60]
print("PASS" if not bad else f"FAIL: {len(bad)} pages under 60%")
sys.exit(1 if bad else 0)

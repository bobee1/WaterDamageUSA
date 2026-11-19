#!/usr/bin/env python3
"""Readability and duplicate-paragraph check for built pages (no external data needed).
Flesch-Kincaid grade uses a vowel-group syllable estimate; good enough to flag pages above grade 9."""
import collections, glob, re, sys
from pathlib import Path

PUB = Path(__file__).resolve().parent.parent / "public"

def syllables(w):
    w = w.lower().strip(".,;:!?()\"'")
    if not w: return 0
    groups = re.findall(r"[aeiouy]+", w)
    n = len(groups)
    if w.endswith("e") and not w.endswith(("le", "ee")) and n > 1: n -= 1
    return max(n, 1)

def fk(text):
    sents = max(len(re.findall(r"[.!?](\s|$)", text)), 1)
    words = re.findall(r"[A-Za-z][A-Za-z'-]*", text)
    if not words: return 0
    syl = sum(syllables(w) for w in words)
    return 0.39 * len(words) / sents + 11.8 * syl / len(words) - 15.59

def main():
    paras = collections.defaultdict(set); fails = []
    for f in sorted(glob.glob(str(PUB / "**/index.html"), recursive=True)):
        raw = open(f).read(); rel = "/" + str(Path(f).relative_to(PUB)).replace("index.html", "")
        m = re.search(r'<div class="content[^"]*">(.*?)</div>\s*<aside class="sidebar"', raw, re.S)
        if not m: continue
        body = re.sub(r"<(svg|table)[\s\S]*?</\1>", " ", m.group(1))
        # link lists (pills, service cards, source lists) are navigation, not prose
        body = re.sub(r'<ul class="pills[\s\S]*?</ul>', " ", body)
        body = re.sub(r'<ul class="state-grid[\s\S]*?</ul>', " ", body)
        body = re.sub(r'<div class="card">[\s\S]*?</div>', " ", body)
        body = re.sub(r'<ul class="sources">[\s\S]*?</ul>', " ", body)
        # fixed components: guide cards (navigation) and the standard author box
        body = re.sub(r'<article class="post-card">[\s\S]*?</article>', " ", body)
        body = re.sub(r'<aside class="author-box">[\s\S]*?</aside>', " ", body)
        for p in re.findall(r"<(?:p|li)(?![^>]*class=\"reviewed\")[^>]*>(.*?)</(?:p|li)>", body, re.S):
            t = re.sub(r"<[^>]+>", "", p).strip()
            if len(t.split()) >= 14: paras[t].add(rel)
        # each list item and heading counts as a sentence
        text = re.sub(r"</(li|h\d|p|td|th)>", ". ", body)
        text = re.sub(r"<[^>]+>", " ", text)
        g = fk(text)
        legal = rel.strip("/") in ("privacy-policy", "terms", "disclaimer", "accessibility", "editorial-policy")
        print(f"FK {g:4.1f}  {rel}{'  (legal, exempt)' if legal else ''}")
        if g > 9 and not legal: fails.append(f"{rel} grade {g:.1f} > 9")
    dups = {t: v for t, v in paras.items() if len(v) > 1}
    for t, v in dups.items(): fails.append(f"duplicate paragraph on {sorted(v)}: {t[:70]}...")
    for x in fails: print("FAIL", x)
    print("PASS" if not fails else f"{len(fails)} issue(s)")
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main()

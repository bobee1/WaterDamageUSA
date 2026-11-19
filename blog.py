"""Guides (blog posts), the guides hub and the glossary for DryBeacon.

Posts live in src/pages/blog/<slug>.html with "type": "post" front matter:
  category, published, updated, card, related [2 slugs], image {webp, jpg, alt}, money (path of the page it supports).
The glossary lives in src/glossary.json: [{term, slug, def, link, match: [phrases]}].
"""
import html
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).parent
GLOSSARY = json.loads((ROOT / "src" / "glossary.json").read_text()) if (ROOT / "src" / "glossary.json").exists() else []
CATEGORIES = ["Restoration Basics", "Leaks & Prevention", "Storms & Flooding", "Sewage & Mold", "Insurance & Claims"]


def esc(s):
    return html.escape(s, quote=True)


def posts_of(pages):
    return sorted((p for p in pages if p.get("type") == "post"), key=lambda p: (p["published"], p["title"]), reverse=True)


def word_count(h):
    return len(re.sub(r"<[^>]+>", " ", h).split())


def read_minutes(meta):
    return max(1, math.ceil(word_count(meta["body"]) / 230))


def nice_date(iso):
    import datetime
    d = datetime.date.fromisoformat(iso)
    return d.strftime("%B %-d, %Y")


def post_header(meta, brand):
    img = meta["image"]
    return f"""<section class="post-head"><div class="wrap">
<p class="post-cat">{esc(meta['category'])}</p>
<h1>{esc(meta['h1'])}</h1>
<p class="byline">By {brand} Editorial · Published <time datetime="{meta['published']}">{nice_date(meta['published'])}</time> · Updated <time datetime="{meta['updated']}">{nice_date(meta['updated'])}</time> · {read_minutes(meta)} min read</p>
<figure class="post-img"><img src="{img['webp']}" width="1200" height="630" alt="{esc(img['alt'])}" fetchpriority="high" decoding="async"></figure>
</div></section>"""


def post_card(p, heading="h3"):
    img = p["image"]
    return (f'<article class="post-card"><a href="{p["path"]}"><img src="{img["webp"]}" width="1200" height="630" '
            f'alt="{esc(img["alt"])}" loading="lazy" decoding="async"></a>'
            f'<p class="post-cat">{esc(p["category"])}</p><{heading}><a href="{p["path"]}">{esc(p["h1"])}</a></{heading}>'
            f'<p>{esc(p["card"])}</p></article>')


def cards(slugs, by_path, heading="h3"):
    out = [post_card(by_path[f"/blog/{s}/"], heading) for s in slugs if f"/blog/{s}/" in by_path]
    return f'<div class="post-grid">{"".join(out)}</div>' if out else ""


def author_box(meta, brand):
    return (f'<aside class="author-box"><p><strong>About this article.</strong> Written by {brand} Editorial and checked '
            f'against the sources listed above. Last updated {nice_date(meta["updated"])}. General information, not legal, '
            f'insurance or professional advice. Read our <a href="/editorial-policy/">editorial policy</a> and '
            f'<a href="/disclaimer/">disclaimer</a>.</p></aside>')


def blog_grid(pages):
    posts = posts_of(pages)
    by_path = {p["path"]: p for p in posts}
    out = []
    for cat in CATEGORIES:
        inc = [p for p in posts if p["category"] == cat]
        if inc:
            out.append(f'<h2>{esc(cat)}</h2><div class="post-grid">{"".join(post_card(p) for p in inc)}</div>')
    return "\n".join(out)


def glossary_html():
    terms = sorted(GLOSSARY, key=lambda t: t["term"].lower())
    letters = sorted({t["term"][0].upper() for t in terms})
    jump = '<nav class="az" aria-label="Glossary letters">' + "".join(f'<a href="#letter-{l}">{l}</a>' for l in letters) + "</nav>"
    out = [jump]
    for l in letters:
        items = [t for t in terms if t["term"][0].upper() == l]
        dl = "".join(f'<div class="term" id="{t["slug"]}"><dt>{esc(t["term"])}</dt><dd>{t["def"]} '
                     f'<a href="{t["link"][1]}">{esc(t["link"][0])}</a></dd></div>' for t in items)
        out.append(f'<h2 id="letter-{l}">{l}</h2><dl class="glossary">{dl}</dl>')
    return "\n".join(out)


def glossary_schema(base):
    return {"@type": "DefinedTermSet", "@id": base + "/glossary/#terms", "name": "DryBeacon water damage glossary",
            "hasDefinedTerm": [{"@type": "DefinedTerm", "@id": f"{base}/glossary/#{t['slug']}", "name": t["term"],
                                "description": re.sub(r"<[^>]+>", "", t["def"]),
                                "url": f"{base}/glossary/#{t['slug']}"} for t in GLOSSARY]}


def autolink_glossary(body, path, limit=4):
    """Link the first mention of up to `limit` glossary terms, inside <p> text only, never inside links or headings."""
    if not GLOSSARY:
        return body
    used = 0
    done = set()
    pats = []
    for t in GLOSSARY:
        if t["link"][1].rstrip("/") == path.rstrip("/"):
            continue  # don't send readers to a term whose best page is this page
        for m in t["match"]:
            pats.append((t, re.compile(r"(?<![\w-])(" + re.escape(m) + r")(?![\w-])", re.I)))

    def do_para(mo):
        nonlocal used
        para = mo.group(0)
        if used >= limit:
            return para
        parts = re.split(r"(<a\b.*?</a>|<[^>]+>)", para, flags=re.S)
        for i, part in enumerate(parts):
            if used >= limit:
                break
            if not part or part.startswith("<"):
                continue
            for t, rx in pats:
                if t["slug"] in done or used >= limit:
                    continue
                m = rx.search(part)
                if m:
                    part = part[:m.start()] + f'<a href="/glossary/#{t["slug"]}" class="gl">{m.group(1)}</a>' + part[m.end():]
                    done.add(t["slug"])
                    used += 1
                    # stop scanning this text chunk for more terms to keep links sparse
                    break
            parts[i] = part
        return "".join(parts)

    return re.sub(r"<p(?: [^>]*)?>.*?</p>", lambda mo: do_para(mo) if 'class="quick"' not in mo.group(0)[:30] and 'class="reviewed"' not in mo.group(0)[:30] else mo.group(0), body, flags=re.S)


def blogposting(meta, base, brand, org_id):
    return {"@type": "BlogPosting", "@id": base + meta["path"] + "#article", "headline": meta["h1"],
            "description": meta["description"], "image": base + meta["image"]["jpg"],
            "datePublished": meta["published"], "dateModified": meta["updated"],
            "author": {"@type": "Organization", "name": f"{brand} Editorial", "url": base + "/editorial-policy/"},
            "publisher": {"@id": org_id}, "inLanguage": "en-US", "wordCount": word_count(meta["body"]),
            "articleSection": meta["category"], "mainEntityOfPage": {"@id": base + meta["path"] + "#webpage"},
            "citation": [u for _, u in meta.get("sources", [])]}

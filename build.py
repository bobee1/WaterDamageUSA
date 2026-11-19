#!/usr/bin/env python3
"""DryBeacon static site generator.

Reads src/site.json and src/pages/**/*.html (JSON front matter + HTML body),
wraps each page in the shared layout, and writes the finished site to public/.
Run: python3 build.py
"""
import html
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "public"
SITE = json.loads((SRC / "site.json").read_text())
BASE = SITE["base_url"]
SERVICES = json.loads((SRC / "services.json").read_text())
SVC = {x["slug"]: x for x in SERVICES}
import states  # noqa: E402  state hub pages

# ---------------------------------------------------------------- helpers

def read_page(path: Path) -> dict:
    raw = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    if not m:
        raise SystemExit(f"Missing front matter: {path}")
    meta = json.loads(m.group(1))
    meta["body"] = m.group(2)
    meta["source"] = str(path.relative_to(ROOT))
    return meta


def tokens(text: str) -> str:
    rep = {
        "{{brand}}": SITE["brand"],
        "{{phone}}": SITE["phone_display"],
        "{{tel}}": "tel:" + SITE["phone_e164"],
        "{{owner}}": SITE["owner"],
        "{{effective}}": SITE["legal_effective_date"],
        "{{years}}": SITE["years_in_business"],
        "{{availability}}": SITE["availability"],
        "{{editorial_byline}}": SITE["editorial_byline"],
        "{{domain}}": SITE["domain"],
        "{{base}}": BASE,
    }
    for k, v in rep.items():
        text = text.replace(k, v)
    return text


def esc(s: str) -> str:
    return html.escape(s, quote=True)


ICON_PHONE = ('<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="currentColor">'
              '<path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.6a1 1 0 0 1-.25 1z"/></svg>')


def call_button(cls="btn btn-call", label=None):
    label = label or f"Call {SITE['phone_display']}"
    return f'<a class="{cls}" href="tel:{SITE["phone_e164"]}">{ICON_PHONE}<span>{esc(label)}</span></a>'



# ---------------------------------------------------------------- content components

def svc_cards(slugs, pages_by_path, heading_level=3):
    out = []
    for slug in slugs:
        x = SVC[slug]
        path = f"/services/{slug}/"
        title = esc(x["name"])
        h = f'<a href="{path}">{title}</a>' if path in pages_by_path else title
        out.append(f'<div class="card"><h{heading_level}>{h}</h{heading_level}><p>{esc(x["card"])}</p></div>')
    return '<div class="cards">' + "".join(out) + "</div>"


def cta_box(text):
    return (f'<aside class="cta-box" aria-label="Call {SITE["brand"]}"><p>{text}</p>'
            f'{call_button("btn btn-call")}</aside>')


def faq_html(meta):
    items = meta.get("faq", [])
    if not items:
        return ""
    title = meta.get("faq_title", "Frequently asked questions")
    qa = "".join(f'<h3>{esc(f["q"])}</h3><p>{f["a"]}</p>' for f in items)
    return f'<h2 id="faq">{esc(title)}</h2><div class="faq">{qa}</div>'


def sources_html(meta):
    src = meta.get("sources", [])
    if not src:
        return ""
    lis = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{esc(t)}</a></li>' for t, u in src)
    return (f'<h2 id="sources">Sources</h2><ul class="sources">{lis}</ul>'
            f'<p class="reviewed">Last reviewed {esc(meta.get("reviewed", SITE["legal_effective_date"]))} by {SITE["editorial_byline"]}. '
            f'General information, not legal, insurance or professional advice. '
            f'Read our <a href="/editorial-policy/">editorial policy</a>.</p>')


def expand_components(body, meta, pages_by_path):
    body = body.replace("{{services_grid}}", svc_cards([x["slug"] for x in SERVICES], pages_by_path))
    body = re.sub(r"\{\{related:([\w,-]+)\}\}",
                  lambda m: svc_cards(m.group(1).split(","), pages_by_path), body)
    body = re.sub(r"\{\{cta:(.+?)\}\}", lambda m: cta_box(m.group(1)), body)
    body = body.replace("{{states_grid}}", states.states_grid())
    body = body.replace("{{state_pills}}", states.state_pills())
    if "{{near_you}}" in body:
        body = body.replace("{{near_you}}", f'<h2>{esc(meta["service"]["name"])} near you</h2>\n' + states.state_pills())
    body = body.replace("{{faq}}", faq_html(meta))
    body = body.replace("{{sources}}", sources_html(meta))
    return body


def strip_tags(h):
    return re.sub(r"<[^>]+>", "", h)

# ---------------------------------------------------------------- layout pieces

def nav_html(pages_by_path):
    items = []
    for label, path in NAV:
        if path in pages_by_path:
            items.append(f'<li><a href="{path}">{esc(label)}</a></li>')
    return "".join(items)


NAV = [("Services", "/services/"), ("Locations", "/locations/"), ("Guides", "/blog/"),
       ("About", "/about/"), ("Contact", "/contact/")]

FOOTER_COLS = [
    ("Services", [(x["name"], f"/services/{x['slug']}/") for x in SERVICES]),
    ("Company", [("About DryBeacon", "/about/"), ("Locations", "/locations/"), ("Contact", "/contact/"),
                 ("Editorial policy", "/editorial-policy/"), ("Water damage guides", "/blog/"),
                 ("Glossary", "/glossary/")]),
    ("Legal", [("Privacy policy", "/privacy-policy/"), ("Terms of service", "/terms/"),
               ("Disclaimer", "/disclaimer/"), ("Accessibility", "/accessibility/")]),
]


def footer_html(pages_by_path):
    cols = []
    for title, links in FOOTER_COLS:
        lis = "".join(f'<li><a href="{p}">{esc(l)}</a></li>' for l, p in links if p in pages_by_path)
        cols.append(f'<div><h2 class="f-title">{title}</h2><ul>{lis}</ul></div>')
    return f"""
<footer class="site-footer">
  <div class="wrap f-grid">
    <div class="f-brand">
      <a class="logo" href="/"><img src="/img/brand/drybeacon-logo-reversed.svg" width="198" height="40" alt="{SITE['brand']} home" loading="lazy"></a>
      <p>{SITE['brand']} handles water damage restoration calls from homeowners, renters and businesses across the United States, {SITE['availability']}. {SITE['years_in_business']} years in business.</p>
      <p class="f-call">{call_button('btn btn-call btn-sm')}</p>
    </div>
    {''.join(cols)}
  </div>
  <div class="wrap f-legal">
    <p>&copy; 2026 {SITE['brand']}. All rights reserved. Content on this site is general information, not legal, insurance or professional advice. Restoration work is performed by trained local crews; check that any contractor holds the licenses your state and city require.</p>
  </div>
</footer>"""


def breadcrumb(meta):
    if meta["path"] == "/" or meta.get("noindex_404"):
        return "", None
    trail = [("Home", "/")] + [tuple(x) for x in meta.get("parents", [])] + [(meta["crumb"], meta["path"])]
    lis = []
    for i, (name, url) in enumerate(trail):
        if i == len(trail) - 1:
            lis.append(f'<li aria-current="page">{esc(name)}</li>')
        else:
            lis.append(f'<li><a href="{url}">{esc(name)}</a></li>')
    html_ = f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(lis)}</ol></nav>'
    schema = {"@type": "BreadcrumbList", "@id": BASE + meta["path"] + "#breadcrumb",
              "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + u}
                                  for i, (n, u) in enumerate(trail)]}
    return html_, schema


def schema_graph(meta, crumb_schema):
    org_id = BASE + "/#organization"
    graph = [
        {"@type": "Organization", "@id": org_id, "name": SITE["brand"], "url": BASE + "/",
         "logo": {"@type": "ImageObject", "url": BASE + "/img/logo-512.png", "width": 512, "height": 512},
         "telephone": SITE["phone_e164"],
         "publishingPrinciples": BASE + "/editorial-policy/",
         "areaServed": {"@type": "Country", "name": "United States",
                        "sameAs": "https://en.wikipedia.org/wiki/United_States"}},
        {"@type": "WebSite", "@id": BASE + "/#website", "url": BASE + "/", "name": SITE["brand"],
         "publisher": {"@id": org_id}, "inLanguage": "en-US"},
    ]
    page = {"@type": meta.get("schema_type", "WebPage"), "@id": BASE + meta["path"] + "#webpage",
            "url": BASE + meta["path"], "name": meta["title"], "description": meta["description"],
            "isPartOf": {"@id": BASE + "/#website"}, "about": {"@id": org_id},
            "inLanguage": "en-US", "dateModified": meta.get("updated", SITE["build_date"])}
    if meta.get("about"):
        page["about"] = [{"@id": org_id}] + [{"@type": "Thing", "name": a[0], "sameAs": a[1]} for a in meta["about"]]
    if meta.get("mentions"):
        page["mentions"] = [{"@type": "Thing", "name": a[0], "sameAs": a[1]} for a in meta["mentions"]]
    if meta.get("sources"):
        page["citation"] = [u for _, u in meta["sources"]]
    if meta.get("service"):
        sv = meta["service"]
        graph.append({"@type": "Service", "@id": BASE + meta["path"] + "#service", "name": sv["name"],
                      "serviceType": sv.get("serviceType", sv["name"]), "description": meta["description"],
                      "provider": {"@id": BASE + "/#business"}, "url": BASE + meta["path"],
                      "areaServed": sv.get("areaServed", {"@type": "Country", "name": "United States"}),
                      "availableChannel": {"@type": "ServiceChannel", "servicePhone": {"@type": "ContactPoint",
                          "telephone": SITE["phone_e164"], "contactType": "customer service", "areaServed": "US"}}})
        page["mainEntity"] = {"@id": BASE + meta["path"] + "#service"}
    if meta.get("faq"):
        graph.append({"@type": "FAQPage", "@id": BASE + meta["path"] + "#faq", "mainEntity": [
            {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": strip_tags(f["a"])}}
            for f in meta["faq"]]})
    if meta.get("home") or meta.get("service"):
        graph.append({"@type": "HomeAndConstructionBusiness", "@id": BASE + "/#business", "name": SITE["brand"],
                      "url": BASE + "/", "telephone": SITE["phone_e164"], "image": BASE + "/img/logo-512.png",
                      "description": "Water damage restoration company taking calls 24/7 from homes and businesses across the United States.",
                      "parentOrganization": {"@id": org_id},
                      "areaServed": {"@type": "Country", "name": "United States", "sameAs": "https://en.wikipedia.org/wiki/United_States"},
                      "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Water damage services", "itemListElement": [
                          {"@type": "Offer", "itemOffered": {"@type": "Service", "name": x["name"], "url": f"{BASE}/services/{x['slug']}/"}}
                          for x in SERVICES]}})
    if meta.get("hero"):
        page["primaryImageOfPage"] = {"@type": "ImageObject", "url": BASE + meta["hero"]["src"]}
    if crumb_schema:
        page["breadcrumb"] = {"@id": crumb_schema["@id"]}
        graph.append(crumb_schema)
    graph.append(page)
    graph.extend(meta.get("extra_schema", []))
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, separators=(",", ":"))


def hero_html(meta):
    lead = f'<p class="lead">{meta["lead"]}</p>' if meta.get("lead") else ""
    chips = ""
    if meta.get("chips"):
        chips = '<ul class="chips">' + "".join(f"<li>{esc(c)}</li>" for c in meta["chips"]) + "</ul>"
    cta = f'<div class="hero-cta">{call_button()}</div>' if meta.get("hero_call", True) else ""
    img = ""
    if meta.get("hero"):
        h = meta["hero"]
        srcset = f'{h["src_small"]} 800w, {h["src"]} {h["w"]}w' if h.get("src_small") else ""
        img = (f'<figure class="hero-img"><img src="{h["src"]}" '
               + (f'srcset="{srcset}" sizes="(max-width: 900px) 100vw, 45vw" ' if srcset else "")
               + f'width="{h["w"]}" height="{h["h"]}" alt="{esc(h["alt"])}" fetchpriority="high" decoding="async"></figure>')
    cls = "hero has-img" if img else "hero"
    return f"""<section class="{cls}"><div class="wrap hero-grid"><div class="hero-text">
<h1>{esc(meta['h1'])}</h1>{lead}{chips}{cta}</div>{img}</div></section>"""


CTA_BAND = f"""<section class="cta-band" aria-label="Call {SITE['brand']}"><div class="wrap">
<p class="cta-title">Water where it shouldn't be?</p>
<p>Call {SITE['brand']} {SITE['availability']} to get water damage help started.</p>
{call_button('btn btn-call btn-lg')}</div></section>"""


def page_html(meta, pages_by_path, css):
    crumbs, crumb_schema = breadcrumb(meta)
    url = BASE + meta["path"]
    robots = "noindex,follow" if meta.get("noindex") else "index,follow,max-image-preview:large"
    og_img = BASE + (meta["hero"]["src_og"] if meta.get("hero", {}).get("src_og") else "/img/og-default.jpg")
    body = tokens(expand_components(tokens(meta["body"]), meta, pages_by_path))
    return f"""<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(meta['title'])}</title>
<meta name="description" content="{esc(meta['description'])}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="{SITE['theme_color']}">
<meta name="x-page-type" content="{meta.get('type', 'other')}">
<meta property="og:type" content="{meta.get('og_type', 'website')}">
<meta property="og:site_name" content="{SITE['brand']}">
<meta property="og:title" content="{esc(meta['title'])}">
<meta property="og:description" content="{esc(meta['description'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<style>{css}</style>
<script type="application/ld+json">{tokens(schema_graph(meta, crumb_schema))}</script>
<script src="/js/site.js" defer></script>
</head>
<body class="{meta.get('body_class', '')}">
<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap h-row">
<a class="logo" href="/"><img src="/img/brand/drybeacon-logo.svg" width="198" height="40" alt="{SITE['brand']} home"></a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
<nav id="site-nav" class="site-nav" aria-label="Main"><ul>{nav_html(pages_by_path)}</ul></nav>
{call_button('btn btn-call btn-sm h-call')}
</div></header>
<main id="main">
{crumbs and f'<div class="wrap">{crumbs}</div>'}
{hero_html(meta)}
<div class="wrap content {meta.get('content_class', 'prose')}">
{body}
</div>
{CTA_BAND if meta.get('cta_band', True) else ''}
</main>
{footer_html(pages_by_path)}
<div class="mobile-call">{call_button('btn btn-call btn-block', f"Call {SITE['brand']} {SITE['phone_display']}")}</div>
</body>
</html>
"""


# ---------------------------------------------------------------- build

def minify_css(css: str) -> str:
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{};:,>])\s*", r"\1", css)
    return css.replace(";}", "}").strip()


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(SRC / "static", OUT)
    css = minify_css((SRC / "css" / "site.css").read_text())

    pages = [read_page(p) for p in sorted((SRC / "pages").rglob("*.html"))]
    pages += states.all_state_pages()
    by_path = {p["path"]: p for p in pages}
    for meta in pages:
        if meta["path"] == "/404.html":
            dest = OUT / "404.html"
        else:
            dest = OUT / meta["path"].strip("/") / "index.html" if meta["path"] != "/" else OUT / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(page_html(meta, by_path, css))

    # sitemap
    urls = []
    for m in pages:
        if m.get("noindex"):
            continue
        urls.append(f"<url><loc>{BASE}{m['path']}</loc><lastmod>{m.get('updated', SITE['build_date'])}</lastmod>"
                    f"<priority>{m.get('priority', '0.5')}</priority></url>")
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
                                     '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                     + "\n".join(urls) + "\n</urlset>\n")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {BASE}/sitemap.xml\n")
    print(f"Built {len(pages)} pages into {OUT}")
    return pages


if __name__ == "__main__":
    build()

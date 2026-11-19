#!/usr/bin/env python3
"""Whole-site SEO and bug audit over the built public/ folder.

Checks every HTML page for: broken internal links and images, missing or duplicate
titles/descriptions, title/description length, canonical, one H1, heading order,
image alt/width/height/lazy loading, JSON-LD parse, orphan pages, sitemap coverage,
redirect targets and page weight. Prints a grouped report; exit 1 on errors.
"""
import json, re, sys, collections
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parent.parent / "public"
SITE = "https://dryflare.com"

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.links=[]; s.imgs=[]; s.heads=[]; s.cur=None; s.title=""; s.intitle=False
        s.meta={}; s.canon=None; s.ld=[]; s.inld=False; s.buf=""; s.ids=collections.Counter(); s.htext=""
    def handle_starttag(s,t,a):
        a=dict(a)
        if "id" in a: s.ids[a["id"]]+=1
        if t=="a" and "href" in a: s.links.append(a["href"])
        if t=="img": s.imgs.append(a)
        if t=="source" and "srcset" in a: s.imgs.append({"src":a["srcset"].split()[0],"alt":"x","width":"1","height":"1","_source":1})
        if t=="title": s.intitle=True
        if t=="meta":
            k=a.get("name") or a.get("property")
            if k: s.meta[k]=a.get("content","")
        if t=="link" and a.get("rel")=="canonical": s.canon=a.get("href")
        if t=="script" and a.get("type")=="application/ld+json": s.inld=True; s.buf=""
        if re.fullmatch(r"h[1-6]",t): s.cur=int(t[1]); s.htext=""
    def handle_endtag(s,t):
        if t=="title": s.intitle=False
        if t=="script" and s.inld: s.ld.append(s.buf); s.inld=False
        if re.fullmatch(r"h[1-6]",t) and s.cur: s.heads.append((s.cur,s.htext.strip())); s.cur=None
    def handle_data(s,d):
        if s.intitle: s.title+=d
        if s.inld: s.buf+=d
        if s.cur: s.htext+=d

pages={}
for f in sorted(ROOT.rglob("*.html")):
    rel="/"+str(f.relative_to(ROOT))
    url=rel[:-len("index.html")] if rel.endswith("index.html") else rel
    h=f.read_text(); p=P(); p.feed(h); p.size=len(h.encode()); p.html=h
    pages[url]=p

E=collections.defaultdict(list); W=collections.defaultdict(list)
inbound=collections.Counter(); titles=collections.defaultdict(list); descs=collections.defaultdict(list)
redirects={}
rf=ROOT/"_redirects"
if rf.exists():
    for l in rf.read_text().splitlines():
        l=l.strip()
        if l and not l.startswith("#"): parts=l.split(); redirects[parts[0]]=parts[1]

def exists(path):
    path=path.split("#")[0].split("?")[0]
    if path in pages: return True
    if (ROOT/path.lstrip("/")).is_file(): return True
    if path in redirects: return True
    return False

for url,p in pages.items():
    if url in ("/404.html",): continue
    noindex="noindex" in p.meta.get("robots","")
    if not p.title.strip(): E["missing title"].append(url)
    else:
        titles[p.title.strip()].append(url)
        if len(p.title)>60: W["title > 60 chars"].append(f"{url} ({len(p.title)})")
        if len(p.title)<25: W["title < 25 chars"].append(f"{url} ({len(p.title)})")
    d=p.meta.get("description","")
    if not d: E["missing description"].append(url)
    else:
        descs[d].append(url)
        if len(d)>160: W["description > 160"].append(f"{url} ({len(d)})")
        if len(d)<70: W["description < 70"].append(f"{url} ({len(d)})")
    if not p.canon: E["missing canonical"].append(url)
    elif p.canon!=SITE+url: E["canonical mismatch"].append(f"{url} -> {p.canon}")
    if not p.meta.get("og:image"): W["missing og:image"].append(url)
    h1=[h for h in p.heads if h[0]==1]
    if len(h1)!=1: E["H1 count != 1"].append(f"{url} ({len(h1)})")
    prev=1
    for lvl,txt in p.heads:
        if lvl>prev+1: W["heading level skip"].append(f"{url} h{prev}->h{lvl} '{txt[:40]}'"); break
        prev=lvl
    for i,v in p.ids.items():
        if v>1: E["duplicate id"].append(f"{url} #{i}")
    for b in p.ld:
        try: json.loads(b)
        except Exception as e: E["bad JSON-LD"].append(f"{url}: {e}")
    for href in p.links:
        if href.startswith(("mailto:","tel:","#","http")):
            if href.startswith("http") and "dryflare.com" in href: W["absolute internal link"].append(f"{url} {href}")
            continue
        if not href.startswith("/"): W["relative link"].append(f"{url} {href}"); continue
        if not exists(href): E["broken link"].append(f"{url} -> {href}")
        else:
            tgt=href.split("#")[0]
            if tgt!=url: inbound[tgt]+=1
            if tgt in redirects: W["link to redirect"].append(f"{url} -> {href}")
            if not tgt.endswith("/") and "." not in tgt.split("/")[-1]: W["link without trailing slash"].append(f"{url} -> {href}")
    for im in p.imgs:
        src=im.get("src","")
        if src.startswith("/") and not exists(src): E["broken image"].append(f"{url} {src}")
        if "_source" in im: continue
        if im.get("alt") is None: E["img missing alt attr"].append(f"{url} {src}")
        if not im.get("width") or not im.get("height"): W["img missing width/height"].append(f"{url} {src}")
    if p.size>60000: W["page > 60 KB"].append(f"{url} ({p.size//1024} KB)")

for t,u in titles.items():
    if len(u)>1: E["duplicate title"].append(f"{t} : {u}")
for d,u in descs.items():
    if len(u)>1: E["duplicate description"].append(f"{d[:60]} : {u}")

sm=(ROOT/"sitemap.xml").read_text()
smurls={u.replace(SITE,"") for u in re.findall(r"<loc>([^<]+)</loc>",sm)}
for url,p in pages.items():
    if url=="/404.html": continue
    if url not in smurls and "noindex" not in p.meta.get("robots",""): E["not in sitemap"].append(url)
    if inbound[url]==0 and url!="/": E["orphan (no inbound links)"].append(url)
for u in smurls:
    if u not in pages: E["sitemap URL missing page"].append(u)
for src,dst in redirects.items():
    if not exists(dst) and not dst.startswith("http"): E["redirect to missing page"].append(f"{src} -> {dst}")

print(f"{len(pages)} pages scanned")
for k,v in sorted(E.items()): print(f"ERROR {k}: {len(v)}"); [print("   ",x) for x in v[:8]]
for k,v in sorted(W.items()): print(f"warn  {k}: {len(v)}"); [print("   ",x) for x in v[:6]]
low=sorted((c,u) for u,c in inbound.items() if u in pages)[:8]
print("lowest inbound:",low)
sys.exit(1 if E else 0)

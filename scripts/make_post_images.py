#!/usr/bin/env python3
"""Render 1200x630 featured images for guides (WebP for the page, JPG for social) from the post front matter."""
import json, re, sys, html
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "src" / "static" / "img" / "blog"; OUT.mkdir(parents=True, exist_ok=True)
BRAND = ROOT / "src" / "static" / "img" / "brand"
TEMPLATE = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0}*{box-sizing:border-box}
.c{width:1200px;height:630px;position:relative;overflow:hidden;background:#1d2329;font-family:Inter,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:#fff;padding:64px 72px}
.arc{position:absolute;right:-180px;top:-180px;width:640px;height:640px;border-radius:50%;border:2px solid rgba(255,122,26,.35)}
.arc.b{right:-100px;top:-100px;width:480px;height:480px;border-color:rgba(255,122,26,.55)}
.arc.c2{right:-20px;top:-20px;width:320px;height:320px;border:none;background:radial-gradient(circle,rgba(255,122,26,.9) 0,rgba(255,122,26,.25) 45%,rgba(255,122,26,0) 70%)}
.cat{display:inline-block;background:#ff7a1a;color:#2a1200;font-weight:800;font-size:22px;letter-spacing:.08em;text-transform:uppercase;padding:9px 18px;border-radius:999px}
h1{font-size:FS;line-height:1.08;margin:34px 0 0;max-width:900px;font-weight:800;letter-spacing:-.01em}
.f{position:absolute;left:72px;right:72px;bottom:54px;display:flex;align-items:center;justify-content:space-between}
.f img{height:46px}.f span{font-size:22px;color:#c9d1d9;font-weight:600}
</style></head><body><div class="c"><div class="arc"></div><div class="arc b"></div><div class="arc c2"></div>
<span class="cat">CAT</span><h1>TITLE</h1>
<div class="f"><img src="drybeacon-logo-reversed.svg"><span>Water damage guide</span></div></div></body></html>"""
posts = []
for f in sorted((ROOT / "src" / "pages" / "blog").glob("*.html")):
    m = re.match(r"^---\n(.*?)\n---\n", f.read_text(), re.S); meta = json.loads(m.group(1))
    if meta.get("type") == "post": posts.append(meta)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
    pg = b.new_page(viewport={"width": 1200, "height": 630})
    for meta in posts:
        slug = meta["path"].strip("/").split("/")[-1]
        t = meta["h1"]; fs = "68px" if len(t) < 38 else "58px" if len(t) < 60 else "50px"
        page = TEMPLATE.replace("TITLE", html.escape(t)).replace("CAT", html.escape(meta["category"])).replace("FS", fs)
        tmp = BRAND / "_post_tmp.html"; tmp.write_text(page)
        pg.goto(tmp.as_uri()); pg.wait_for_timeout(150)
        png = OUT / f"{slug}.png"; pg.screenshot(path=str(png))
        im = Image.open(png).convert("RGB")
        im.save(OUT / f"{slug}.webp", "WEBP", quality=82, method=6)
        im.save(OUT / f"{slug}.jpg", "JPEG", quality=84, optimize=True, progressive=True)
        png.unlink(); tmp.unlink()
        print(slug, (OUT / f"{slug}.webp").stat().st_size // 1024, "KB webp", (OUT / f"{slug}.jpg").stat().st_size // 1024, "KB jpg")
    b.close()

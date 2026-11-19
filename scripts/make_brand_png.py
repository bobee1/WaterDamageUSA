"""Renders PNG icons and the default social image from the brand SVGs (needs Chrome + Playwright)."""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parent.parent
S = ROOT / "src" / "static"
B = S / "img" / "brand"
jobs = [("drybeacon-app-icon-small.svg", 32, S / "favicon-32.png"), ("drybeacon-app-icon.svg", 180, S / "apple-touch-icon.png"),
        ("drybeacon-app-icon.svg", 192, S / "img" / "logo-192.png"), ("drybeacon-app-icon.svg", 512, S / "img" / "logo-512.png")]
og = f"""<html><body style="margin:0;width:1200px;height:630px;background:#0b2545;font-family:'Inter Display',sans-serif;position:relative;overflow:hidden">
<img src="file://{B}/drybeacon-logo-reversed.svg" style="position:absolute;left:96px;top:150px;height:120px">
<p style="position:absolute;left:100px;top:330px;margin:0;color:#e9f0f8;font-size:52px;font-weight:700;line-height:1.15">Water damage restoration<br>across the United States</p>
<div style="position:absolute;left:0;right:0;bottom:0;height:22px;background:#f5b301"></div>
<svg style="position:absolute;right:-40px;top:40px" width="520" height="520" viewBox="0 0 64 64"><path d="M32 3C32 3 11 25.5 11 40.5a21 21 0 0 0 42 0C53 25.5 32 3 32 3z" fill="#13315c"/><path d="M23.5 36.5a12 12 0 0 1 17 0M18 31a19.5 19.5 0 0 1 28 0" fill="none" stroke="#0b2545" stroke-width="3.6" stroke-linecap="round"/><circle cx="32" cy="44" r="5.5" fill="#f5b301"/></svg>
</body></html>"""
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
    for svg, size, out in jobs:
        pg = b.new_page(viewport={"width": size, "height": size})
        tmp = B / "_render.html"
        tmp.write_text(f'<html><body style="margin:0;background:transparent"><img src="{svg}" width="{size}" height="{size}"></body></html>')
        pg.goto(tmp.as_uri())
        pg.wait_for_timeout(100)
        pg.screenshot(path=str(out), omit_background=True)
    pg = b.new_page(viewport={"width": 1200, "height": 630})
    tmp = B / "_render.html"; tmp.write_text(og.replace(f"file://{B}/", ""))
    pg.goto(tmp.as_uri()); pg.wait_for_timeout(200)
    pg.screenshot(path=str(S / "img" / "og-default.jpg"), type="jpeg", quality=88)
    b.close()
    (B / "_render.html").unlink()
print("done")

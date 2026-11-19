"""Builds DryBeacon logo SVGs. Wordmark: Inter Display ExtraBold (SIL OFL) converted to outlines."""
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

NAVY, BLUE, AMBER, WHITE, LIGHTBLUE = "#1d2329", "#d9540b", "#ff7a1a", "#ffffff", "#ff9a4d"  # brand-dark, logo accent, beacon, white, brand-accent-soft
font = TTFont("/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf")
gs, cmap, hmtx = font.getGlyphSet(), font.getBestCmap(), font["hmtx"]
upm = font["head"].unitsPerEm

def text_paths(text, size, x0, baseline, tracking=-0.02):
    """Return list of (char, path_d) and the end x, scaled to font size."""
    s = size / upm
    out, x = [], x0
    for ch in text:
        g = cmap[ord(ch)]
        pen = SVGPathPen(gs)
        gs[g].draw(TransformPen(pen, (s, 0, 0, -s, x, baseline)))
        out.append(pen.getCommands())
        x += hmtx[g][0] * s + tracking * size
    return out, x - tracking * size

# ---- the mark: water drop holding a beacon light with two signal arcs (viewBox 64x64)
DROP = "M32 3C32 3 11 25.5 11 40.5a21 21 0 0 0 42 0C53 25.5 32 3 32 3z"
def mark(drop_fill, arc, dot, small=False):
    arcs = "" if small else (
        f'<path d="M23.5 36.5a12 12 0 0 1 17 0" fill="none" stroke="{arc}" stroke-width="3.6" stroke-linecap="round"/>'
        f'<path d="M18 31a19.5 19.5 0 0 1 28 0" fill="none" stroke="{arc}" stroke-width="3.6" stroke-linecap="round"/>')
    r = 7.5 if small else 5.5
    return f'<path d="{DROP}" fill="{drop_fill}"/>{arcs}<circle cx="32" cy="{44 if not small else 41}" r="{r}" fill="{dot}"/>'

def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{title}">'
            f'<title>{title}</title>{body}</svg>\n')

import os, sys
OUT = sys.argv[1] if len(sys.argv) > 1 else "."
files = {}
files["drybeacon-mark.svg"] = svg(64, 64, mark(NAVY, WHITE, AMBER), "DryBeacon")
files["drybeacon-mark-small.svg"] = svg(64, 64, mark(NAVY, WHITE, AMBER, small=True), "DryBeacon")
# single ink: drop in currentColor, arcs and light cut out with a mask
files["drybeacon-mark-mono.svg"] = svg(64, 64,
    '<defs><mask id="m"><rect width="64" height="64" fill="#fff"/>'
    '<path d="M23.5 36.5a12 12 0 0 1 17 0M18 31a19.5 19.5 0 0 1 28 0" fill="none" stroke="#000" stroke-width="3.6" stroke-linecap="round"/>'
    '<circle cx="32" cy="44" r="5.5" fill="#000"/></mask></defs>'
    f'<path d="{DROP}" fill="currentColor" mask="url(#m)"/>', "DryBeacon")
# app icon / favicon tile
files["drybeacon-app-icon.svg"] = svg(64, 64,
    f'<rect width="64" height="64" rx="14" fill="{NAVY}"/><g transform="translate(6.4 5.2) scale(.8)">{mark(WHITE, NAVY, AMBER)}</g>', "DryBeacon")

files["drybeacon-app-icon-small.svg"] = svg(64, 64,
    f'<rect width="64" height="64" rx="14" fill="{NAVY}"/><g transform="translate(6.4 5.2) scale(.8)">{mark(WHITE, NAVY, AMBER, small=True)}</g>', "DryBeacon")

# ---- horizontal lockups: mark 64 tall, wordmark cap height aligned
def lockup(dry_c, beacon_c, drop, arc, dot, title="DryBeacon"):
    size, base = 46, 48
    dry, x = text_paths("Dry", size, 78, base)
    beacon, x2 = text_paths("Beacon", size, x + 0.5, base)
    w = int(x2 + 4)
    body = f'{mark(drop, arc, dot)}<g fill="{dry_c}">' + "".join(f'<path d="{d}"/>' for d in dry) + \
           f'</g><g fill="{beacon_c}">' + "".join(f'<path d="{d}"/>' for d in beacon) + "</g>"
    return svg(w, 64, body, title), w

files["drybeacon-logo.svg"], W = lockup(NAVY, BLUE, NAVY, WHITE, AMBER)
files["drybeacon-logo-reversed.svg"], _ = lockup(WHITE, LIGHTBLUE, WHITE, NAVY, AMBER)
files["drybeacon-logo-mono.svg"], _ = lockup("currentColor", "currentColor", "currentColor", "#fff", "#fff")
# mono lockup should use the masked mark instead of white cut-ins
mono_mark = files["drybeacon-mark-mono.svg"].split("<title>DryBeacon</title>")[1].replace("</svg>\n", "")
mono = files["drybeacon-logo-mono.svg"]
start = mono.index("<path d=\"M32 3C"); end = mono.index("<g fill=")
files["drybeacon-logo-mono.svg"] = mono[:start] + mono_mark + mono[end:]

for name, data in files.items():
    open(os.path.join(OUT, name), "w").write(data)
print("lockup width", W)

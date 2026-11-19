# DryBeacon — Record Register

A dated log of every step. Newest entries at the bottom of each build. Status: Done / In progress / Planned.

| # | Date | Build | Step | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| 1 | 2026-11-16 | Plan | Nationwide build plan written and revised | Done | Toll-free number, all states and cities with demand, Cloudflare free plan |
| 2 | 2026-11-18 | 1 | Read site criteria and blog criteria docs | Done | Rules applied to all pages |
| 3 | 2026-11-18 | 1 | Checked brand domains in the .com registry (RDAP) | Done | Free: drybeacon, ameridrypros, dryrevive, waterlosspros and others |
| 4 | 2026-11-18 | 1 | Owner decisions recorded | Done | DryBeacon; own-business routing; 24/7; 10+ years; owner Anjam Javed; toll-free 1-800-555-0199 |
| 5 | 2026-11-18 | 1 | GitHub repo connected | Done | github.com/bobee1/WaterDamageUSA (was empty) |
| 6 | 2026-11-18 | 1 | Pexels photos downloaded and converted to WebP | Done | IDs 28447774, 30499666, 15206136, 18302377; 800 px + full size; all under 200 KB |
| 7 | 2026-11-18 | 1 | Site generator, design system, layout, schema | Done | `build.py`, `src/css/site.css`, `src/static/` |
| 8 | 2026-11-18 | 1 | Trust and legal pages written | Done | About, Contact, Privacy, Terms, Disclaimer, Editorial policy, Accessibility, 404 |
| 9 | 2026-11-18 | 1 | Contact form endpoint | Done | `functions/api/lead.js` (Resend; needs env vars) |
| 10 | 2026-11-18 | 1 | Audit script + run | Done | 0 issues; home page `/` pending (Build 3) |
| 11 | 2026-11-18 | 1 | Responsive check 360/768/1280 | Done | No horizontal scroll, no console errors |
| 12 | 2026-11-18 | 1 | Committed and pushed to GitHub | Done | Branch `main` |
| 13 | 2026-11-18 | 1b | Logo designed: drop + beacon light + signal arcs; Inter Display ExtraBold wordmark outlined | Done | 8 SVGs in `src/static/img/brand/`, built by `scripts/make_logo.py` |
| 14 | 2026-11-18 | 1b | Favicon, app icons, social image regenerated from the logo | Done | `scripts/make_brand_png.py` |
| 15 | 2026-11-18 | 1b | Design tokens: site CSS variables renamed to match the design system | Done | One source of truth for colors, radius, shadow, font |
| 16 | 2026-11-18 | 1b | Contrast fixes: focus ring (dark blue on light grounds), form borders #73859a | Done | Both now pass 3:1 |
| 17 | 2026-11-18 | 1b | DryBeacon Design System artifact published | Done | Tokens, brand book, logos, 9 components, cover |
| 18 | — | 2 | Semrush keyword research + site plan for approval | Planned | Next build |

## Image register
| File | Source | Used on |
| --- | --- | --- |
| flooded-home-yard-after-heavy-rain(.webp, -800) | Pexels photo 28447774 | About hero |
| flooded-room-standing-water(.webp, -800) | Pexels photo 18302377 | Contact hero |
| leaking-pipe-dripping-water(.webp, -800) | Pexels photo 15206136 | About (figure) |
| collapsed-ceiling-after-water-leak(.webp, -800) | Pexels photo 30499666 | Reserved for ceiling/roof leak service page |

Pexels license: free to use, no attribution required. Credits are not shown on the site.

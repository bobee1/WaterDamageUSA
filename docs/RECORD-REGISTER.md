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
| 18 | 2026-11-18 | 1c | Palette changed to Graphite + Signal Orange (owner chose B of 4 options) | Done | Navy/amber looked like the owner's city sites; tokens renamed by role (brand-dark, brand-accent, tint) |
| 19 | 2026-11-18 | 1c | Logo, favicon, icons, social image recolored; contrast re-checked | Done | All text pairs at least 4.5:1; borders and focus at least 3:1 |
| 20 | 2026-11-19 | 2 | Semrush: 60 service keywords (volume, CPC, intent, KD) | Done | `research/01-service-keywords.csv` |
| 21 | 2026-11-19 | 2 | Semrush: 100 city terms, 11 state terms, Denver/Frisco/Gilbert clusters | Done | `research/02-city-demand.csv`, `03-state-and-cluster.csv` |
| 22 | 2026-11-19 | 2 | Semrush: question keywords for guides | Done | `research/04-guide-keywords.csv` |
| 23 | 2026-11-19 | 2 | SERP and competitor analysis (3 SERPs, 2 domains' top pages) | Done | `research/05-competitors.csv` |
| 24 | 2026-11-19 | 2 | Site plan written for owner approval | Done | Claude doc "DryBeacon Site Plan — Build 2 Keyword Research" |
| 25 | 2026-11-19 | 3 | Owner approved the Build 2 plan | Done | "Build 3" go-ahead; no doc comments or edits |
| 26 | 2026-11-19 | 3 | Semrush top-10 SERPs for 10 service keywords | Done | Burst pipe SERP is plumber/DIY intent, so the page targets "burst pipe water damage" + "frozen pipe burst" |
| 27 | 2026-11-19 | 3 | Competitor benchmarks (SERVPRO ~240 words, BELFOR ~600, 1-800 Water Damage ~1,400) | Done | Term gaps: IICRC categories/classes, equipment, insurance, DIY vs pro |
| 28 | 2026-11-19 | 3 | Primary sources verified | Done | EPA (mold, flood cleanup), FEMA/FloodSmart, American Red Cross (frozen pipes), ANSI/IICRC S500 by name |
| 29 | 2026-11-19 | 3 | 6 more Pexels photos converted to WebP; 2 SVG illustrations | Done | Drying setup diagram; water categories diagram |
| 30 | 2026-11-19 | 3 | Generator: service registry, cards, CTA boxes, FAQ + Service + business schema, sources, footer services | Done | `src/services.json`, `build.py` |
| 31 | 2026-11-19 | 3 | Home page (1,506 words), services hub, 10 service pages (1,040–1,343 words) | Done | Keyword map from the approved plan |
| 32 | 2026-11-19 | 3 | Audit 0 issues; readability FK 5.7–8.2 on money pages; no repeated paragraphs; responsive 360/768/1280 clean | Done | `scripts/audit.py`, `scripts/readability.py` |
| 33 | 2026-11-19 | 4 | STATUS.md restructured: Builds 1–3 moved to Previous | Done | Owner asked whether records are kept up to date |
| 34 | 2026-11-19 | 4 | Census ACS 2020–2024 state housing data + top 12 places per state | Done | Census Reporter API via browser (api.census.gov now needs a key); `research/06-state-data.json` |
| 35 | 2026-11-19 | 4 | OpenFEMA major disaster declarations 2000–2026 by state and type | Done | 1,645 declarations; water-related subset per state |
| 36 | 2026-11-19 | 4 | State insurance regulators, contractor boards, mold licensing states | Done | NAIC directory blocked by bot check; used agency sites, CT Corporation contractor chart and searches |
| 37 | 2026-11-19 | 4 | Generator `states.py`, CSS for state cards and pills, audit type `state` | Done | |
| 38 | 2026-11-19 | 4 | 51 hand-written state content files + `/locations/` hub | Done | Verified local events only; no invented statutes |
| 39 | 2026-11-19 | 4 | Local notes and "near you" links on 10 service pages; state links on home, menu, footer | Done | Each state has 3+ in-text inbound links |
| 40 | 2026-11-19 | 4 | Audit 0 issues; readability ≤ 9; uniqueness 71–79% (rule ≥ 60%); responsive clean | Done | New `scripts/uniqueness.py` |
| 41 | 2026-11-19 | 5 | Semrush questions + top-8 SERPs for 10 guide keywords | Done | ~4,100 API units; `research/07-guide-briefs.csv` |
| 42 | 2026-11-19 | 5 | Primary sources gathered (NAIC, FloodSmart, CDC, EPA lead/mold/flood, Red Cross, A. O. Smith) | Done | Competitor pages blocked from fetch; lengths set from Build 3 benchmarks |
| 43 | 2026-11-19 | 5 | Generator: `blog.py` (post layout, cards, author box, BlogPosting, glossary, auto-links) | Done | |
| 44 | 2026-11-19 | 5 | 10 guides written (1,230–1,642 words, FK 5.0–7.2) + guides hub | Done | No prices published (approved plan) |
| 45 | 2026-11-19 | 5 | 10 branded 1200×630 featured images (WebP + JPG) | Done | `scripts/make_post_images.py` |
| 46 | 2026-11-19 | 5 | Glossary: 55 terms, DefinedTermSet, auto-links (max 4 per page) | Done | |
| 47 | 2026-11-19 | 5 | Helpful guides on 10 service pages; home page guide links | Done | Every guide has 4+ in-text inbound links |
| 48 | 2026-11-19 | 5 | Audit 0 issues (84 pages); readability, duplicates, responsive clean | Done | |
| 49 | 2026-11-19 | 6 | Semrush: 80 more city keywords (820 units) | Done | `research/08-city-demand-batch2.csv` |
| 50 | 2026-11-19 | 6 | Top 50 metros ranked by searches × CPC; suburbs held for Build 7 | Done | Dallas, Austin and LA lead |
| 51 | 2026-11-19 | 6 | Census ACS housing data for 50 principal cities | Done | `research/09-metro-acs.json` |
| 52 | 2026-11-19 | 6 | Generator `metros.py`; metro metadata (county, ZIPs, neighborhoods, nearby) | Done | `src/metros/meta.json` |
| 53 | 2026-11-19 | 6 | 50 hand-written metro content files | Done | Verified local events only |
| 54 | 2026-11-19 | 6 | State pages, Locations hub, guides and storm page link to metros | Done | |
| 55 | 2026-11-19 | 6 | Audit 0 issues (134 pages); FK ≤ 9; uniqueness 75–80%; responsive clean | Done | |
| 56 | — | 7 | First 100 city pages (suburbs + next metros) | Planned | Next build |

## Image register
| File | Source | Used on |
| --- | --- | --- |
| flooded-home-yard-after-heavy-rain(.webp, -800) | Pexels photo 28447774 | About hero |
| flooded-room-standing-water(.webp, -800) | Pexels photo 18302377 | Contact hero |
| leaking-pipe-dripping-water(.webp, -800) | Pexels photo 15206136 | About (figure) |
| collapsed-ceiling-after-water-leak(.webp, -800) | Pexels photo 30499666 | Ceiling water damage page |
| flooded-neighborhood-flood-barrier(.webp, -800) | Pexels photo 28447806 | Home hero, flood page |
| floodwater-inside-building-stairs(.webp, -800) | Pexels photo 7924140 | Flood damage restoration hero |
| drywall-repair-after-water-damage(.webp, -800) | Pexels photo 6474308 | Water damage repair |
| mold-spots-on-wall-after-leak(.webp, -800) | Pexels photo 18063447 | Mold remediation |
| storm-damaged-roof-and-window(.webp, -800) | Pexels photo 36237047 | Storm damage restoration |
| commercial-office-floor(.webp, -800) | Pexels photo 5483233 | Commercial water damage |
| Inline SVG: drying setup, water categories | Original illustrations | Water mitigation, sewage cleanup |
| blog/*.webp, blog/*.jpg (10 guides) | Original branded graphics | Guide featured images and social cards |
| Existing photos reused on state pages | Same Pexels IDs as above | Chosen by each state's main risk, with state-specific alt text and captions |

Pexels license: free to use, no attribution required. Credits are not shown on the site.

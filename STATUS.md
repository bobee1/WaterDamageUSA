# DryBeacon — Build Status

Nationwide water damage restoration site. Brand **DryBeacon**, domain **drybeacon.com** (available on 2026-11-18, not yet purchased).
Plan: "Nationwide Water Damage Local Services Site — Build Plan" (Claude doc). Rules: "Local Service Site SEO Criteria & AI Prompt" and "Blog Post Criteria & SEO Writing Prompt".

Last updated: 2026-11-19

## Previous
- Build 5 — Guides hub, 10 guides (1,230–1,642 words, FK 5.0–7.2), 55-term glossary with auto-links, branded featured images, helpful guides on service pages.
- Build 4 — Locations hub + 51 state pages (Census ACS + FEMA data, insurance and licensing notes, 71–79% unique); service-page local notes and near-you links.
- Build 1 — Foundation, trust and legal pages: generator (`build.py`), design system, header/footer, mobile call bar, breadcrumbs, base JSON-LD; About, Contact (form → Pages Function → Resend), Privacy, Terms, Disclaimer, Editorial Policy, Accessibility, 404; robots, sitemap, `_headers`, `_redirects`, manifest, icons; 4 Pexels WebP photos; audit 0 issues.
- Build 1b — Logo set and design system (Design System artifact "DryBeacon"); contrast fixes.
- Build 1c — Palette B "Graphite + Signal Orange" (brand-dark #1d2329, beacon orange #ff7a1a, accent text #c2410c) to set DryBeacon apart from the owner's city sites.
- Build 2 — Semrush keyword research (`research/`) and site plan doc "DryBeacon Site Plan — Build 2 Keyword Research"; approved by owner on 2026-11-19.
- Build 3 — Home page, services hub and 10 service pages (1,040–1,343 words each); FAQ, Service and business schema; audit 0 issues; reading grade 5.7–8.2; responsive clean. Guide cards and glossary links wait for Build 5.
- Plan approved: one national brand, state → metro → city structure, all 50 states + DC, one toll-free number, Cloudflare free plan.
- Owner decisions: brand DryBeacon; own-business call routing; 24/7; 10+ years in business; legal owner Anjam Javed; toll-free 1-800-555-0199; email added after the domain is bought.

## Current — Build 6: City scoring + first 50 metro pages (done)
- Semrush: 80 more city keywords scored (820 units; 39,180 left), merged with the Build 2 sample of 100 (`research/02-city-demand.csv`, `research/08-city-demand-batch2.csv`). Ranked by value score = searches × CPC (floor $20); suburbs held for Build 7 city pages.
- 50 metro pages at `/locations/<state>/<city>/` (Dallas, Austin, LA, Las Vegas, San Diego, Atlanta, Houston … Omaha, San Francisco), 800–1,050 words each.
- Each page: Census ACS housing table for the city (`research/09-metro-acs.json`), county and sample ZIP codes, hand-written "why water damage here is different" with verified local events and landmarks, local problems table linked to services, tips, neighborhoods and suburbs, insurance note linked to the state page, 4 FAQs, service cards, nearby metros.
- Schema: Service with areaServed City (sameAs Wikipedia, containedInPlace county), FAQPage, BreadcrumbList (Home › Locations › State › City).
- Links: state pages list their metro pages in text; Locations hub has a "Top metro areas" list; each metro links 3 nearby metros in text; every metro has 2+ in-text inbound links plus its state page.
- Checks: audit 0 issues (134 pages); readability ≤ 9; uniqueness 75–80% per metro page vs its closest (rule ≥ 60%); responsive clean on all 52 checked pages.

## Coming
| Build | Scope | Needs from owner |
| --- | --- | --- |
| 7 | First 100 city pages | — |
| Launch | Buy domain, Cloudflare Pages project, env vars, real toll-free number, email, Search Console + analytics | Domain, number, email, Resend key |

## Deployment
- Host: Cloudflare Pages, project `drybeacon`, Git-connected to `bobee1/WaterDamageUSA` (branch `main`). Live at https://drybeacon.pages.dev/ since 2026-11-19; pushes to `main` redeploy automatically (confirmed).
- Settings: framework preset None, no build command, build output directory `public`, root directory blank. `functions/` is picked up automatically for the contact form.
- Live checks (2026-11-19): all 133 sitemap URLs return 200; 404 page returns 404 with noindex; security headers (CSP, HSTS, X-Frame-Options) present; images served as WebP with a 1-year cache; `/services` redirects to `/services/`; contact form endpoint answers (validation works; email sending waits for Resend keys).
- Staging address `drybeacon.pages.dev` sends `X-Robots-Tag: noindex` (set in `_headers`) so it stays out of search until drybeacon.com is connected.

## Open items
- **Phone number:** 1-800-555-0199 is in the 555-01xx range reserved for fiction and cannot receive calls. Replace `phone_display` / `phone_e164` in `src/site.json` before launch.
- **Email:** add to `src/site.json` once the domain is bought.
- **Resend env vars** for the contact form: `RESEND_API_KEY`, `LEAD_TO_EMAIL`, `LEAD_FROM_EMAIL`.

## How to build
```
python3 build.py          # writes public/
python3 scripts/audit.py  # must print "PASS: 0 issues"
python3 scripts/readability.py   # reading grade <= 9, no repeated paragraphs
python3 scripts/uniqueness.py    # state pages >= 60% unique
python3 scripts/make_post_images.py  # after adding or retitling a guide
```
Cloudflare Pages: build output directory `public`, no build command needed (output is committed); `functions/` holds the form endpoint.

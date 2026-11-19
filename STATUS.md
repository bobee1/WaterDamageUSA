# DryBeacon — Build Status

Nationwide water damage restoration site. Brand **DryBeacon**, domain **drybeacon.com** (available on 2026-11-18, not yet purchased).
Plan: "Nationwide Water Damage Local Services Site — Build Plan" (Claude doc). Rules: "Local Service Site SEO Criteria & AI Prompt" and "Blog Post Criteria & SEO Writing Prompt".

Last updated: 2026-11-19

## Previous
- Build 1 — Foundation, trust and legal pages: generator (`build.py`), design system, header/footer, mobile call bar, breadcrumbs, base JSON-LD; About, Contact (form → Pages Function → Resend), Privacy, Terms, Disclaimer, Editorial Policy, Accessibility, 404; robots, sitemap, `_headers`, `_redirects`, manifest, icons; 4 Pexels WebP photos; audit 0 issues.
- Build 1b — Logo set and design system (Design System artifact "DryBeacon"); contrast fixes.
- Build 1c — Palette B "Graphite + Signal Orange" (brand-dark #1d2329, beacon orange #ff7a1a, accent text #c2410c) to set DryBeacon apart from the owner's city sites.
- Build 2 — Semrush keyword research (`research/`) and site plan doc "DryBeacon Site Plan — Build 2 Keyword Research"; approved by owner on 2026-11-19.
- Build 3 — Home page, services hub and 10 service pages (1,040–1,343 words each); FAQ, Service and business schema; audit 0 issues; reading grade 5.7–8.2; responsive clean. Guide cards and glossary links wait for Build 5.
- Plan approved: one national brand, state → metro → city structure, all 50 states + DC, one toll-free number, Cloudflare free plan.
- Owner decisions: brand DryBeacon; own-business call routing; 24/7; 10+ years in business; legal owner Anjam Javed; toll-free 1-800-555-0199; email added after the domain is bought.

## Current — Build 4: Locations hub + 51 state pages (done)
- `/locations/` hub (state cards grouped by Census region) and 51 state pages at `/locations/<state>/` (50 states + DC), 950–1,150 words each.
- Each state page: hand-written lead, "why water damage here is different" (verified local events), local problems table linked to services, homeowner tips, insurance and licensing notes, areas served, 4 FAQs, service cards, nearby-state links, sources.
- Data on every page ("at a glance" table): Census ACS 2020–2024 housing figures (homes built before 1980/1940, median build year, ownership, mobile homes), top places, and FEMA major disaster declarations 2000–Nov 2026. Raw data in `research/06-state-data.json`.
- Agencies: state insurance regulator, contractor licensing board (or "no statewide license" where true), and mold licensing in TX, FL, NY, LA and DC (`src/states/meta.json`).
- Generator: `states.py` builds the pages from `src/states/content/<AB>.json`; schema adds Service with `areaServed` State, FAQPage, BreadcrumbList.
- Internal links: "Locations" in the menu and footer, state links on the home page, a "Local note" plus "near you" state links on every service page; every state page has 3+ in-text links from other pages.
- Checks: audit 0 issues (72 pages); reading grade ≤ 9 on every page; uniqueness 71–79% per state page vs its closest page (rule ≥ 60%, `scripts/uniqueness.py`); no horizontal scroll at 360/768/1280 on all 54 checked pages; no console errors.

## Coming
| Build | Scope | Needs from owner |
| --- | --- | --- |
| 5 | Glossary (50+ terms) + Guides hub + first 10 guides | — |
| 6 | Master city dataset (Census, NOAA, FEMA, EPA) + 50 metro hub pages | Data files (the workspace can't reach Census/NOAA directly) |
| 7 | First 100 city pages | — |
| Launch | Buy domain, Cloudflare Pages project, env vars, real toll-free number, email, Search Console + analytics | Domain, number, email, Resend key |

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
```
Cloudflare Pages: build output directory `public`, no build command needed (output is committed); `functions/` holds the form endpoint.

# DryBeacon — Build Status

Nationwide water damage restoration site. Brand **DryBeacon**, domain **drybeacon.com** (available on 2026-11-18, not yet purchased).
Plan: "Nationwide Water Damage Local Services Site — Build Plan" (Claude doc). Rules: "Local Service Site SEO Criteria & AI Prompt" and "Blog Post Criteria & SEO Writing Prompt".

Last updated: 2026-11-19

## Previous
- Build 4 — Locations hub + 51 state pages (Census ACS + FEMA data, insurance and licensing notes, 71–79% unique); service-page local notes and near-you links.
- Build 1 — Foundation, trust and legal pages: generator (`build.py`), design system, header/footer, mobile call bar, breadcrumbs, base JSON-LD; About, Contact (form → Pages Function → Resend), Privacy, Terms, Disclaimer, Editorial Policy, Accessibility, 404; robots, sitemap, `_headers`, `_redirects`, manifest, icons; 4 Pexels WebP photos; audit 0 issues.
- Build 1b — Logo set and design system (Design System artifact "DryBeacon"); contrast fixes.
- Build 1c — Palette B "Graphite + Signal Orange" (brand-dark #1d2329, beacon orange #ff7a1a, accent text #c2410c) to set DryBeacon apart from the owner's city sites.
- Build 2 — Semrush keyword research (`research/`) and site plan doc "DryBeacon Site Plan — Build 2 Keyword Research"; approved by owner on 2026-11-19.
- Build 3 — Home page, services hub and 10 service pages (1,040–1,343 words each); FAQ, Service and business schema; audit 0 issues; reading grade 5.7–8.2; responsive clean. Guide cards and glossary links wait for Build 5.
- Plan approved: one national brand, state → metro → city structure, all 50 states + DC, one toll-free number, Cloudflare free plan.
- Owner decisions: brand DryBeacon; own-business call routing; 24/7; 10+ years in business; legal owner Anjam Javed; toll-free 1-800-555-0199; email added after the domain is bought.

## Current — Build 5: Guides hub, first 10 guides and glossary (done)
- `/blog/` guides hub (cards grouped by 5 categories, Blog schema) and 10 guides from the approved plan, 1,230–1,642 words each, reading grade 5.0–7.2.
- Each guide: SERP brief (Semrush questions + top 8 rankers, `research/07-guide-briefs.csv`), short-answer box, money-page link in the first 150 words, question H2s, comparison tables, numbered steps, CTA, prevention, Local note (4–5 state links), Related reading, "When should you call…" close, 4 FAQs, 4–5 primary sources (EPA, CDC, FEMA/FloodSmart, NAIC, Red Cross; one manufacturer figure credited by name), author box, 2 related guide cards.
- Branded 1200×630 featured images (WebP on page, JPG for social), rendered from the post titles by `scripts/make_post_images.py`.
- Schema: BlogPosting (headline, dates, wordCount, citation), WebPage about/mentions, FAQPage, BreadcrumbList (Home › Guides › post).
- `/glossary/`: 55 terms, A–Z jump links, DefinedTermSet schema; each term links to its best guide or service. First mention of up to 4 terms auto-links on service, state and guide pages.
- Internal links: "Helpful guides" (3 cards) on every service page, guide links in the home page process and cost sections, Guides and Glossary in the menu/footer; every guide has 4+ in-text links from other pages.
- Checks: audit 0 issues (84 pages); readability ≤ 9 everywhere; no repeated paragraphs; responsive clean at 360/768/1280; no console errors.
- Note: competitor pages couldn't be opened from this workspace for exact word counts, so lengths were set against the Build 3 benchmarks (SERVPRO ~1,250, BELFOR ~600, 1-800 Water Damage ~1,400). Dehumidifier SERP is shopping-heavy, so that guide targets the question searches.

## Coming
| Build | Scope | Needs from owner |
| --- | --- | --- |
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
python3 scripts/make_post_images.py  # after adding or retitling a guide
```
Cloudflare Pages: build output directory `public`, no build command needed (output is committed); `functions/` holds the form endpoint.

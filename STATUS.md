# DryFlare — Build Status

Nationwide water damage restoration site. Brand **DryFlare**, domain **dryflare.com** (available on 2026-11-18, not yet purchased).
Plan: "Nationwide Water Damage Local Services Site — Build Plan" (Claude doc). Rules: "Local Service Site SEO Criteria & AI Prompt" and "Blog Post Criteria & SEO Writing Prompt".

Last updated: 2026-11-19

## Previous
- Build 5 — Guides hub, 10 guides (1,230–1,642 words, FK 5.0–7.2), 55-term glossary with auto-links, branded featured images, helpful guides on service pages.
- Build 4 — Locations hub + 51 state pages (Census ACS + FEMA data, insurance and licensing notes, 71–79% unique); service-page local notes and near-you links.
- Build 1 — Foundation, trust and legal pages: generator (`build.py`), design system, header/footer, mobile call bar, breadcrumbs, base JSON-LD; About, Contact (form → Pages Function → Resend), Privacy, Terms, Disclaimer, Editorial Policy, Accessibility, 404; robots, sitemap, `_headers`, `_redirects`, manifest, icons; 4 Pexels WebP photos; audit 0 issues.
- Build 1b — Logo set and design system (Design System artifact "DryFlare"); contrast fixes.
- Build 1c — Palette B "Graphite + Signal Orange" (brand-dark #1d2329, beacon orange #ff7a1a, accent text #c2410c) to set DryFlare apart from the owner's city sites.
- Build 2 — Semrush keyword research (`research/`) and site plan doc "DryFlare Site Plan — Build 2 Keyword Research"; approved by owner on 2026-11-19.
- Build 3 — Home page, services hub and 10 service pages (1,040–1,343 words each); FAQ, Service and business schema; audit 0 issues; reading grade 5.7–8.2; responsive clean. Guide cards and glossary links wait for Build 5.
- Plan approved: one national brand, state → metro → city structure, all 50 states + DC, one toll-free number, Cloudflare free plan.
- Owner decisions: brand DryFlare; own-business call routing; 24/7; 10+ years in business; legal owner Anjam Javed; toll-free 1-800-555-0199; email added after the domain is bought.

## Current — Build 7 Part 2: 25 city pages (done)
- Live: Fresno, Naperville, Joliet, Daytona Beach, Clearwater, Louisville, Des Moines, Albuquerque, Boulder, Castle Rock, Cape Coral, Naples, Akron, Baton Rouge, New Orleans, Arlington TX, Boca Raton, Ann Arbor, Richmond, Missoula, Ogden, Madison, Lakeland, Springfield MO, Albany NY.
- Same build rules as Part 1: Census ACS housing table, checked ZIPs, hand-written local risks with verified events (Ian 2022 in Cape Coral, Naples and Daytona; Helene 2024 in Clearwater; Milton 2024 in Lakeland; the 2016 Baton Rouge flood; the 2013 Boulder flood), local problems table, tips, neighborhoods, insurance notes and a city-specific FAQ. Claims I couldn't confirm were cut or softened.
- Suburbs linked to their hubs: Naperville and Joliet → Chicago; Clearwater → Tampa; Boulder and Castle Rock → Denver; Cape Coral → Fort Myers; Arlington → Dallas; Ogden → Salt Lake City.
- Each page has its own photo. A review sheet caught near-duplicates from the same shoot (four pages showing the same flooded house, two the same creek), so those photos were swapped out.
- Checks: audit 0 issues (184 pages); FK ≤ 8.7; uniqueness ≥ 74.4% vs closest (avg 77.1%); 834–891 words; 3+ in-text inbound links each; no overflow at 1440/1024/768/360; pages ≤ 39 KB.
- Photo library: 245 photos, 89 unused (flood 6, rain 3, repair 8, others more). Parts 3–4 need about 15 more flood/interior photos sourced first.

## Previous — No repeated photos (done)
- Every page now has its own photo. 126 state and city pages each have a different Pexels photo matched to their main risk (storm, flood, frozen pipes, mold, ceiling leaks, repairs), with alt text that describes what the photo actually shows.
- The home, about, contact, water extraction and flood pages no longer share photos.
- 230 photos in the library (`src/photos.json`); 104 are unused and held for Parts 2–4, so new city pages also get unique photos.
- The audit now fails the build if any photo appears on two pages.

## Previous — Build 7 Part 1: 25 city pages (done)
- Build 7 = 100 city pages in 4 parts of 25, ranked by search value. Part 1 (live): Frisco, Plano, Fort Collins, Tacoma, Bellevue, Everett, Mesa, Gilbert, Chandler, Scottsdale, Irvine, Anaheim, Long Beach, Sarasota, Miami, Wichita, Tulsa, Baltimore, Greensboro, Columbia SC, Grand Rapids, Knoxville, Lexington, Reno, Provo.
- Each page: Census ACS housing table, checked ZIP codes, a hand-written "why water damage here is different" built on that city's own risks and a verified local event, a local problems table, tips, neighborhoods, insurance notes and an FAQ specific to that city. Same-metro suburbs take different angles (e.g. Mesa mobile homes, Gilbert tile roofs, Chandler copper pinholes, Scottsdale empty seasonal homes).
- Linking: metro hubs now list their suburbs; nearby links run both ways; every new page has 3–6 in-text inbound links.
- Checks: audit 0 issues (159 pages); readability 6.2–8.4; uniqueness ≥ 75.2% vs closest page; valid schema; no overflow at 4 widths; pages ≤ 38 KB.

## Previous — Rename to DryFlare (done)
- DryBeacon was already in use by a nationwide water damage site (drybeacon.us), so the brand is now **DryFlare**, domain **dryflare.com** (unregistered as of 2026-11-19; buy it soon).
- Changed everywhere: page text, titles, schema, canonical URLs, logo and wordmark, favicon and app icons, social image, guide header images, manifest, lead email template.
- Kept: the drop-and-light icon, colors, layout and all URLs. The owner created a new Cloudflare Pages project `dryflare`; preview is now dryflare.pages.dev (noindexed).
- Checks: audit 0 issues; readability and uniqueness pass; no old-name text left in the built site.

## Previous — Layout fix (done)
- Content was indented past the header and capped at 820px, leaving an empty right band on desktop. Now: content lines up with the logo and hero on every page.
- Desktop (above 1024px): two columns, content plus a sticky 300px sidebar with a call card, the services list (current page marked), "More locations" on state/city pages, and popular guides.
- Tablet and phone: single full-width column; sidebar hidden (the footer and in-text links already cover it).
- Audit, readability and uniqueness checks now read only the content column, so the sidebar doesn't count toward word counts.
- Checked all 133 pages at 1440/1280/1024/768/360: no overflow, content edge aligned with the header on every page.

## Previous — Build 6: City scoring + first 50 metro pages (done)
- Semrush: 80 more city keywords scored (820 units; 39,180 left), merged with the Build 2 sample of 100 (`research/02-city-demand.csv`, `research/08-city-demand-batch2.csv`). Ranked by value score = searches × CPC (floor $20); suburbs held for Build 7 city pages.
- 50 metro pages at `/locations/<state>/<city>/` (Dallas, Austin, LA, Las Vegas, San Diego, Atlanta, Houston … Omaha, San Francisco), 800–1,050 words each.
- Each page: Census ACS housing table for the city (`research/09-metro-acs.json`), county and sample ZIP codes, hand-written "why water damage here is different" with verified local events and landmarks, local problems table linked to services, tips, neighborhoods and suburbs, insurance note linked to the state page, 4 FAQs, service cards, nearby metros.
- Schema: Service with areaServed City (sameAs Wikipedia, containedInPlace county), FAQPage, BreadcrumbList (Home › Locations › State › City).
- Links: state pages list their metro pages in text; Locations hub has a "Top metro areas" list; each metro links 3 nearby metros in text; every metro has 2+ in-text inbound links plus its state page.
- Checks: audit 0 issues (134 pages); readability ≤ 9; uniqueness 75–80% per metro page vs its closest (rule ≥ 60%); responsive clean on all 52 checked pages.

## Coming
| Build | Scope | Needs from owner |
| --- | --- | --- |
| 7 | Parts 3–4: 50 more city pages (25 each), starting with Durham, Augusta, Rochester, Birmingham | — |
| Launch | Buy domain, Cloudflare Pages project, env vars, real toll-free number, email, Search Console + analytics | Domain, number, email, Resend key |

## Deployment
- Host: Cloudflare Pages, project `dryflare`, Git-connected to `bobee1/WaterDamageUSA` (branch `main`). Live at https://dryflare.pages.dev/ (new project created 2026-11-19 after the rename; the old drybeacon project can be deleted); pushes to `main` redeploy automatically (confirmed).
- Settings: framework preset None, no build command, build output directory `public`, root directory blank. `functions/` is picked up automatically for the contact form.
- Live checks (2026-11-19): all 133 sitemap URLs return 200; 404 page returns 404 with noindex; security headers (CSP, HSTS, X-Frame-Options) present; images served as WebP with a 1-year cache; `/services` redirects to `/services/`; contact form endpoint answers (validation works; email sending waits for Resend keys).
- Staging address `dryflare.pages.dev` sends `X-Robots-Tag: noindex` (set in `_headers`) so it stays out of search until dryflare.com is connected.

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

# DryBeacon — Build Status

Nationwide water damage restoration site. Brand **DryBeacon**, domain **drybeacon.com** (available on 2026-11-18, not yet purchased).
Plan: "Nationwide Water Damage Local Services Site — Build Plan" (Claude doc). Rules: "Local Service Site SEO Criteria & AI Prompt" and "Blog Post Criteria & SEO Writing Prompt".

Last updated: 2026-11-18

## Previous
- Plan approved: one national brand, state → metro → city structure, all 50 states + DC, one toll-free number, Cloudflare free plan.
- Owner decisions: brand DryBeacon; own-business call routing; 24/7; 10+ years in business; legal owner Anjam Javed; toll-free 1-800-555-0199; email added after the domain is bought.

## Current — Build 1: Foundation + trust and legal pages (done)
- Static site generator (`build.py`) → `public/`, design system, header/footer, mobile call bar, breadcrumbs, JSON-LD (Organization, WebSite, WebPage, BreadcrumbList).
- Pages: About, Contact (form → Cloudflare Pages Function → Resend), Privacy Policy, Terms of Service, Disclaimer, Editorial Policy, Accessibility, 404.
- Utility: `robots.txt`, `sitemap.xml`, `_headers` (security headers + CSP + caching), `_redirects`, web manifest, favicon/app icons, default social image.
- Images: 4 Pexels photos converted to WebP (2 sizes each, all under 200 KB).
- Audit (`scripts/audit.py`): 0 issues. One pending link target: `/` (home page ships in Build 3).
- Responsive check at 360 / 768 / 1280 px: no horizontal scroll, no console errors.

## Current — Build 1b: Logo and design system (done)
- Logo set (`src/static/img/brand/`): full-color lockup, reversed, one-color, mark, small mark, app icons. Header and footer use the lockups.
- Favicon, apple-touch icon, PWA icons and default social image regenerated from the new logo.
- Design system published as the "DryBeacon" Design System artifact (tokens, brand book, logo rules, 9 components). Site CSS variables use the same token names.
- Accessibility fixes: focus outline and form field borders now meet 3:1 contrast.

## Coming
| Build | Scope | Needs from owner |
| --- | --- | --- |
| 2 | Keyword research + site plan in Semrush: keyword map, clusters, competitors, service list, guide list, state/metro priority list. **Presented for approval before any money page is built.** | Approve the plan |
| 3 | Home page + Services hub + 8 service pages | — |
| 4 | Locations hub + 51 state hub pages | — |
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
```
Cloudflare Pages: build output directory `public`, no build command needed (output is committed); `functions/` holds the form endpoint.

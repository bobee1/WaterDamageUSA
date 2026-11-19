# DryFlare (dryflare.com)

Static website for DryFlare, a nationwide water damage restoration brand. See `STATUS.md` for progress and `docs/RECORD-REGISTER.md` for the step log.

- `src/site.json`: brand, phone, owner and other site-wide settings (change the phone here only)
- `src/pages/`: page content (JSON front matter + HTML)
- `src/css/site.css`: design system (inlined into each page)
- `src/static/`: images, JS, icons, `_headers`, `_redirects`
- `functions/api/lead.js`: contact form endpoint (Cloudflare Pages Function + Resend)
- `build.py`: builds `public/`
- `scripts/audit.py`: SEO, link, compliance and performance checks

Build: `python3 build.py && python3 scripts/audit.py`

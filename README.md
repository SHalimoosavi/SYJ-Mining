# SYJ Mining Platform

Engineering-first mining software by **SAYANJALI NEXUS PRIVATE LIMITED**.

Repository: https://github.com/SHalimoosavi/SYJ-Mining

This repository contains the static, GitHub Pages–compatible landing website
for SYJ Mining Platform. It is HTML/CSS/vanilla JS only — no backend, no
database, no Node.js runtime requirement, no build step.

## What this is

SYJ Mining Platform is an engineering-focused mining software project. It
emphasizes controlled execution, benchmark verification, hardware telemetry,
artifact integrity, and evidence-driven qualification — with measurement
qualification kept intentionally separate from economic and execution
authorization. See the live page for full detail: `#platform`,
`#verification`, `#security`, `#architecture`.

No performance, hardware/OS support, licensing, or release claims are made
beyond what is explicitly stated on the page as verified.

## Project structure

```
/
├── index.html                  Main landing page
├── 404.html                    Not-found page
├── robots.txt
├── sitemap.xml
├── site.webmanifest
├── favicon.svg
├── CNAME.example               Notes on custom-domain setup (inactive)
├── assets/
│   ├── css/styles.css
│   ├── js/main.js
│   └── images/og-image.svg     Locally generated social preview (no external image service)
├── .github/workflows/pages.yml GitHub Pages deployment workflow
├── SEO/structured-data.json    Reference copy of the JSON-LD in index.html
└── scripts/validate_site.py    Local structural/SEO validation script
```

## Local preview

```bash
python -m http.server 8000
```

Then open `http://localhost:8000/` in a browser.

## Validation

```bash
python3 scripts/validate_site.py
```

This checks: required meta tags, canonical URL, single H1, Open Graph and
Twitter/X metadata, favicon/manifest links, valid JSON-LD, presence of
required section IDs, no duplicate IDs, no dangling internal anchors, no
leftover placeholder/TODO markers, no unverified superlative marketing
claims, robots.txt referencing the sitemap, and valid sitemap XML.

It exits non-zero on any failure.

## SITE_URL — read before deploying

Every canonical/OG/sitemap/robots reference in this repository currently
points to:

```
SITE_URL = "https://shalimoosavi.github.io/SYJ-Mining/"
```

This is the standard GitHub Pages URL pattern for this repository
(`SHalimoosavi/SYJ-Mining` → `https://shalimoosavi.github.io/SYJ-Mining/`),
**but it has not been verified as live.** Before or immediately after your
first deploy, confirm the actual URL at:

`GitHub repository → Settings → Pages`

If it differs (for example, if a custom domain is later configured via a
real `CNAME` file — see `CNAME.example`), update `SITE_URL` in all of the
following:

- `index.html` — `<link rel="canonical">`, `og:url`, `og:image`, `twitter:image`
- `robots.txt` — `Sitemap:` line
- `sitemap.xml` — `<loc>`
- `SEO/structured-data.json` — `@id` and `url` fields

## Publish to GitHub

```bash
git init
git add .
git commit -m "Initial commit: SYJ Mining Platform landing site"
git branch -M main
git remote add origin https://github.com/SHalimoosavi/SYJ-Mining.git
git push -u origin main
```

## Enable GitHub Pages

1. Push to `main` (workflow at `.github/workflows/pages.yml` runs automatically).
2. In the repository: **Settings → Pages → Build and deployment → Source** → select **GitHub Actions**.
3. Wait for the `Deploy to GitHub Pages` workflow to complete under the **Actions** tab.
4. Confirm the live URL shown on the **Settings → Pages** screen.

## Google Search Console

1. Deploy GitHub Pages (above) and confirm the live URL.
2. Add and verify that URL as a property in Google Search Console.
3. Submit `sitemap.xml` from the **Sitemaps** panel.
4. Use **URL Inspection** on the homepage and request indexing if desired.
5. Monitor the **Indexing** and **Core Web Vitals** reports over time.
6. Address any crawl or indexing errors Search Console reports.

Submitting a sitemap does not guarantee indexing, and no SEO work guarantees
ranking. This repository is built for technical crawl/indexing readiness;
actual indexing and ranking remain controlled by search-engine systems.

## Deployment status

- Technically optimized and prepared for Google crawling/indexing; actual
  indexing and ranking remain controlled by search-engine systems.
- The site is **not** currently claimed to be live, indexed, or served on a
  custom domain. Verify each of these independently after deployment.

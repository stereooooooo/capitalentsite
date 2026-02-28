# Capital ENT & Sinus Center — Website

## Overview
Marketing website for Capital ENT & Sinus Center, Austin TX's top-rated ENT practice. Static HTML/CSS/JS — no build tools, no framework.

**Live site:** https://www.capitalent.com
**Repo:** github.com/stereooooooo/capitalentsite (branch: main)

## Tech Stack
- Static HTML pages (40+ pages)
- Single shared stylesheet: `style.css`
- Single shared script: `main.js`
- Fonts: Google Fonts (Instrument Serif, Inter)
- No build step — files served as-is
- Dev server: `python3 -m http.server 8082` (configured in `.claude/launch.json`)

## Project Structure
```
/                       Root — all HTML pages live here (flat, no subdirectories)
├── index.html          Homepage
├── style.css           All styles (shared across every page)
├── main.js             All JS (mobile nav, booking modal, FAQ accordion, etc.)
├── sitemap.xml         SEO sitemap
├── robots.txt          Crawl rules
├── reviews.html        Patient reviews with filterable categories
├── ask-the-ent.html    AI Q&A feature
├── *.html              Service pages (balloon-sinuplasty, hearing-aids, etc.)
├── *.png / *.webp      Images (logos, doctor photos) — WebP preferred
└── .claude/
    └── launch.json     Dev server config
```

## Key Conventions

### HTML Pages
- Every page links `style.css` and `main.js`
- Content Security Policy meta tag on every page
- Open Graph + Twitter Card meta tags for social sharing
- JSON-LD structured data (schema.org) for SEO
- Shared nav bar and footer across all pages (inline, not templated)

### Reviews Page (reviews.html)
- Review cards use `data-topic` attribute for filtering: `sinus`, `ear`, `throat`, `allergy`, `pediatric`, `staff`
- Filter buttons use `data-filter` attribute matching topic values
- Author names: first name + last initial (e.g., "JC J.", "Tim C.")
- All reviews sourced from real Google Business Profile — never fabricated
- Google rating: 4.8 stars, 1,340+ reviews

### Images
- Use WebP format when possible (with PNG/JPG fallbacks)
- Logo: `CENT-Horizontal-Color.webp`

## Content Rules — CRITICAL
This is a well-respected ENT medical practice in Austin, TX. All information on this website must be valid and accurate. **NEVER fabricate or make up any data**, including but not limited to:
- **Patient reviews or testimonials** — only use real reviews sourced from Google Business Profile
- **Doctor names, credentials, or bios** — must reflect actual staff
- **Medical claims, statistics, or treatment outcomes** — must be factually accurate
- **Insurance providers, office hours, or contact info** — must match real practice data
- **Ratings, review counts, or awards** — must come from verified sources

When in doubt, ask rather than guess. Medical content should be accurate but written for patients, not clinicians.

## Git Workflow
- Single branch: `main`
- Push directly to `main` (no PR workflow currently)
- Commit messages: short imperative summary, optional detail paragraph

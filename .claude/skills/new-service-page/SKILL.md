---
name: new-service-page
description: Create a new service or procedure page following Capital ENT's template
---

Create a new service/procedure page for: $ARGUMENTS

## Before writing

1. Read an existing service page as a template (e.g., `ear-care.html` or `balloon-sinuplasty.html`)
2. Read `style.css` to understand available CSS classes
3. Read `our-doctors.html` to reference correct doctor names and credentials

## Required page structure

Every service page must include, in order:

1. **`<head>`** with:
   - CSP meta tag (copy exactly from existing pages)
   - Title: `Service Name | Capital ENT & Sinus Center — Austin, TX`
   - Meta description (~160 chars)
   - Canonical URL: `https://www.capitalent.com/filename.html`
   - Open Graph tags (og:title, og:description, og:url, og:image)
   - Twitter Card tags
   - Favicon links (copy from existing page)
   - Google Fonts preconnect + stylesheet link
   - `<link rel="stylesheet" href="style.css">`
   - JSON-LD structured data (MedicalOrganization + relevant schema)

2. **Shared navbar** — copy from an existing page, update `active` class if needed

3. **Mobile nav drawer** — copy from an existing page

4. **Breadcrumb**: Home > Service Name

5. **Hero section**: heading + subtitle

6. **Content sections** using existing CSS classes (`section`, `section-inner`, `section-head`, etc.)

7. **CTA section**: "Schedule Your Appointment" with phone number 512-339-4040

8. **Shared footer** — copy from an existing page

9. **`<script src="main.js"></script>`** before `</body>`

## After creating the page

1. Add navigation links to the new page in ALL existing HTML files (navbar + mobile nav)
2. Add the page to `sitemap.xml`
3. Verify with preview tools that the page renders correctly

## Content accuracy

All medical content must be factually accurate. Never fabricate procedure details, recovery times, or outcomes. When in doubt, ask the user.

---
name: seo-audit
description: Audit SEO elements across all pages — meta tags, structured data, Open Graph, sitemap
---

Run a full SEO audit of the Capital ENT website.

## Checks to perform

### 1. Meta tags (every page)
- `<title>` — present, unique, under 60 chars
- `<meta name="description">` — present, unique, under 160 chars
- `<meta name="robots" content="index, follow">` — present
- `<link rel="canonical">` — present and correct

### 2. Open Graph tags (every page)
- `og:title`, `og:description`, `og:url`, `og:image`, `og:type`, `og:site_name`
- All should be present and unique per page

### 3. Twitter Card tags (every page)
- `twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`

### 4. JSON-LD structured data (every page)
- MedicalOrganization schema with name, phone, address
- Service pages should have relevant MedicalProcedure or MedicalCondition schema
- FAQ page should have FAQPage schema

### 5. Sitemap (sitemap.xml)
- Every public HTML page should be listed
- No pages listed that don't exist
- `<lastmod>` dates should be reasonably current

### 6. robots.txt
- Allows crawling of all public pages
- Blocks dev/draft files (mockup.html, etc.)
- Points to sitemap

### 7. Images
- All images have `alt` attributes
- WebP format used where possible

## How to check

Use Grep to search across all HTML files:
- Missing titles: search for files lacking `<title>`
- Missing descriptions: search for files lacking `meta name="description"`
- Missing OG tags: search for files lacking `og:title`
- Duplicate descriptions: compare description content across pages

## Output format

Report findings grouped by severity:
- **Critical**: Missing title or description (hurts rankings)
- **High**: Missing Open Graph tags (hurts social sharing)
- **Medium**: Missing structured data, duplicate content
- **Low**: Minor formatting, missing alt text

Include specific file names and recommended fixes for each issue.

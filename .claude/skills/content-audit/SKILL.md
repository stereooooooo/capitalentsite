---
name: content-audit
description: Analyze website content for gaps, outdated info, and maintenance needs
---

Generate a content audit report for the Capital ENT website.

## Analysis areas

### 1. Page inventory
- List all HTML pages and their purpose
- Identify any pages that seem incomplete or outdated
- Flag dev/draft files that shouldn't be public (mockup.html, etc.)

### 2. Service coverage
- Compare services listed in the navbar against dedicated service pages
- Identify conditions/procedures mentioned on the homepage but lacking their own page
- Check that all procedures listed on `our-doctors.html` have corresponding service pages

### 3. Reviews distribution
Read `reviews.html` and count reviews per `data-topic`:
- `sinus`, `ear`, `throat`, `allergy`, `pediatric`, `staff`
- Flag any category with fewer than 3 reviews as underrepresented

### 4. Doctor coverage
- Verify all doctors in `our-doctors.html` are mentioned on relevant service pages
- Check that doctor names/credentials are consistent across all pages they appear on

### 5. Content freshness
- Check for any dates, statistics, or claims that may be outdated
- Look for references to specific years that may need updating
- Review the sitemap `<lastmod>` dates

### 6. Internal linking
- Service pages should cross-link to related services
- Doctor profiles should link to their specialties
- FAQ should cover topics from all major service areas

### 7. Missing content opportunities
- Are there common ENT procedures not yet covered?
- Could existing pages be expanded with more detail?
- Are patient resources comprehensive?

## Output format

**Capital ENT Website — Content Audit Report**

**Summary**: X pages, X service pages, X reviews

**Strengths**: What's working well

**Gaps**: Missing pages, underrepresented topics, incomplete content

**Outdated**: Content that needs refreshing

**Opportunities**: High-value additions that would improve the site

**Priority actions**: Top 5 things to address first

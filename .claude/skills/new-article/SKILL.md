---
name: new-article
description: Add a new article to the Ask the ENT section with a standalone page and hub card
---

Create a new Ask the ENT article about: $ARGUMENTS

## Before writing

1. Read `mouth-taping.html` as the article page template (first standalone article — use as the canonical reference)
2. Read `ask-the-ent.html` to see the current article cards and count
3. Read `cpap.html` as a secondary reference for section patterns (info-split, conditions-grid, why-grid, bsp-faq)
4. Read `sitemap.xml` to find the insertion point for the new URL

## Step 1: Create the article page

Create a new HTML file at the root (e.g., `article-slug.html`). Follow the exact structure of `mouth-taping.html`:

### Head section
- CSP meta tag — use `'unsafe-inline'` in `style-src` (needed for page-specific `<style>` block)
- Title format: `Article Title | Capital ENT`
- Meta description (~160 chars, patient-focused)
- Canonical URL: `https://www.capitalent.com/article-slug.html`
- Open Graph tags (og:type should be `article`)
- Twitter Card tags
- Favicon links (copy from template)
- Google Fonts preconnect + stylesheet
- Page-specific `<style>` block for `.references` section (copy from `mouth-taping.html`)
- JSON-LD structured data: MedicalOrganization, MedicalWebPage (with `lastReviewed` set to today), BreadcrumbList, FAQPage

### Body structure (in order)
1. Skip link
2. Utility bar (copy from template)
3. Navbar — no `active` class on any nav item (articles aren't in the nav)
4. Mobile nav drawer (copy from template)
5. `<main id="main-content">`
6. **Page Hero** (`.page-hero`) — eyebrow matching the article category, H1, intro paragraph, hero buttons
7. **Breadcrumb** — Home > [Category page] > Article Title
8. **Content sections** — use 4-7 sections mixing these patterns:
   - `.info-split` / `.info-split.reverse` — two-column text + visual stat card
   - `.conditions-grid` + `.cond-card` — card grid for comparing findings/conditions
   - `.why-grid` — 3-column feature/step cards
   - `.bsp-faq` — accordion Q&A (always include 4-6 FAQs)
   - Alternate `.section` and `.section.bg-off` for visual rhythm
9. **References** (`.references` in a tight-padding section) — numbered list of citations
10. **Physician Attribution** (`.physician-attr`) — ask user which doctor to credit, default to Dr. Brown
11. **CTA Band** (`.cta-band`) — relevant headline + appointment/call buttons
12. Footer (copy from template)
13. Sticky CTA button
14. Booking modal — pre-select the relevant service type
15. `<script src="main.js" defer></script>` + inline nav dropdown JS

### Category-to-eyebrow mapping
| Category | Eyebrow text | Breadcrumb parent | Booking pre-select |
|----------|-------------|-------------------|-------------------|
| sleep    | Sleep Medicine | Sleep (sleep.html) | Sleep Medicine / Sleep Apnea |
| sinus    | Nasal & Sinus | Nose & Sinus (nose-sinus.html) | Nose & Sinus |
| throat   | Throat & Voice | Throat (throat.html) | Throat & Voice |
| allergy  | Allergy | Allergy (allergy.html) | Allergy Treatment |
| ear      | Ear & Hearing | Ear Care (ear-care.html) | Ear Care & Hearing |

## Step 2: Add article card to ask-the-ent.html

Insert a new `.art-card` in the matching category section's `.articles-grid`. Use this template:

```html
<a href="article-slug.html" class="art-card" data-cat="CATEGORY">
  <div class="art-img CATEGORY">
    <span class="art-tag">TAG</span>
    <svg class="art-img-icon" viewBox="0 0 24 24">ICON_SVG</svg>
  </div>
  <div class="art-body">
    <h3>Article Title</h3>
    <p>1-2 sentence teaser description.</p>
    <div class="art-footer">
      <span class="art-read">Read More <svg viewBox="0 0 24 24"><polyline points="9 18 15 12 9 6"/></svg></span>
      <span class="art-min">X min read</span>
    </div>
  </div>
</a>
```

### Category icons (copy from existing cards in that section)
| Category | art-tag | Icon SVG path |
|----------|---------|---------------|
| sleep | Sleep | `<path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/>` |
| throat | Throat | `<path d="M12 2C6 2 2 6.5 2 12s4 10 10 10 10-4.5 10-10-4-10-10-10z"/><path d="M12 6v5m-2 4h4"/>` |
| sinus | Sinus | `<path d="M12 20c4.4 0 8-1.8 8-4v-2c0 2.2-3.6 4-8 4s-8-1.8-8-4v2c0 2.2 3.6 4 8 4z"/><ellipse cx="12" cy="12" rx="8" ry="3" fill="none"/>` |
| allergy | Allergy | `<path d="M12 2C7 2 3 6 3 11c0 5 2 9 9 11 7-2 9-6 9-11 0-5-4-9-9-9z"/><circle cx="12" cy="11" r="2" fill="white"/>` |
| ear | Ear | `<path d="M6 8.5a6.5 6.5 0 1113 0c0 6.5-6.5 9.5-6.5 9.5"/><path d="M10 14a4 4 0 004-4"/>` |

### Update the article count
In the hero meta section, find the `X articles` span and increment the number by 1.

## Step 3: Add to sitemap.xml

Add before `</urlset>`:

```xml
<url>
  <loc>https://www.capitalent.com/article-slug.html</loc>
  <lastmod>YYYY-MM-DD</lastmod>
  <changefreq>monthly</changefreq>
  <priority>0.7</priority>
</url>
```

## Content rules

- All medical content must be factually accurate — never fabricate statistics, outcomes, or claims
- Write for patients, not clinicians — use plain language with medical terms explained in parentheses
- If the user provides source material (e.g., from OpenEvidence), use only those statistics
- Include a References section with full citations when source material is provided
- Maintain a balanced, evidence-based tone — the practice's credibility depends on accuracy
- When in doubt about medical facts, ask the user rather than guessing

## After creating

1. Verify the new article page renders correctly with preview tools
2. Verify the article card appears in the correct category on ask-the-ent.html
3. Test the category filter on ask-the-ent.html to ensure the new card shows/hides correctly
4. Confirm the article count updated

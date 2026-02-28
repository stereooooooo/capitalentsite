---
name: pre-deploy-check
description: Run validation checks before pushing changes to the live site
---

Run pre-deployment validation on the Capital ENT website.

## Checks

### 1. Broken internal links
Search all HTML files for `href="*.html"` references and verify each target file exists. Flag any links pointing to missing pages.

### 2. Placeholder or draft content
Search all HTML files for:
- `TODO`, `FIXME`, `XXX`, `PLACEHOLDER`, `DRAFT`, `Lorem ipsum`
- These should never appear on the live site

### 3. Contact info consistency
- Phone number should be `512-339-4040` (or `(512) 339-4040`) everywhere
- Verify all pages show the same number
- Check footer contact info matches across all pages

### 4. Shared nav consistency
- Every page should have the same navbar links and mobile nav drawer
- Check a sample of pages to confirm nav structure matches

### 5. Required assets
Verify these files exist:
- `style.css`, `main.js`
- `CENT-Horizontal-Color.webp` (and .png fallback)
- `favicon.ico`, `favicon.png`, `favicon-16.png`, `favicon-32.png`

### 6. Script and stylesheet references
- Every HTML page should link `style.css` in `<head>`
- Every HTML page should include `main.js` before `</body>`

### 7. CSP headers
- Every page should have the Content-Security-Policy meta tag

### 8. Git status
- Check for uncommitted changes
- Confirm we're on the `main` branch

## Output format

```
Pre-Deploy Check Results
========================
[PASS/FAIL] Internal links
[PASS/FAIL] No placeholder content
[PASS/FAIL] Contact info consistent
[PASS/FAIL] Nav consistency
[PASS/FAIL] Required assets present
[PASS/FAIL] Script/style references
[PASS/FAIL] CSP headers
[PASS/FAIL] Git status clean

Issues found: N
```

List specific issues for any FAIL items with file names and line numbers.

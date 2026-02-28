---
name: add-review
description: Add a real patient review from Google Business Profile to reviews.html
---

Add a new patient review to reviews.html. The review MUST come from a real Google Business Profile review — never fabricate reviews.

## How to source the review

Use Claude in Chrome or web search to find the review on Capital ENT's Google Business Profile. If the user provides the review text and author directly, confirm it's from Google before adding.

## Review card HTML template

Each review card follows this exact structure. Insert new cards before `</div><!-- /#reviewsGrid -->`:

```html
<!-- Review N -->
<div class="review-card" data-topic="TOPIC">
  <div class="review-top">
    <div class="review-stars">
      <svg viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
      <svg viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
      <svg viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
      <svg viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
      <svg viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
    </div>
    <span class="review-date">Mon YYYY</span>
  </div>
  <div class="topic-badge">Badge Label</div>
  <p class="review-text">Exact review text from Google.</p>
  <div class="review-footer">
    <div class="review-author">FirstName L.<span>City, TX</span></div>
    <div class="review-source"><span class="g-dot"></span> Google</div>
  </div>
</div>
```

## Rules

- **data-topic** must be one of: `sinus`, `ear`, `throat`, `allergy`, `pediatric`, `staff`
- **topic-badge** labels: "Sinus Care", "Balloon Sinuplasty", "Ear Care", "Hearing Care", "Hearing Aids", "Throat Care", "Sleep Study", "Sleep & Breathing", "Allergy Care", "Pediatric ENT", "Staff & Office"
- **Author names**: first name + last initial (e.g., "Sarah M.", "JC J.")
- **Location**: Use "Austin, TX" unless the review specifies another city
- **Star SVGs**: Use 5 star SVGs for 5-star reviews. Omit stars for fewer (rare — most are 5-star)
- **Review number**: Increment the comment `<!-- Review N -->` from the last existing review
- Add `featured` class only to the first 2 review cards on the page

## After adding

1. Verify the filter buttons still show correct counts
2. Check the page renders correctly with preview tools

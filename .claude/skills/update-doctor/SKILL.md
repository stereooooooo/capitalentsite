---
name: update-doctor
description: Update a doctor or provider's profile, credentials, or specialties
---

Update the profile for: $ARGUMENTS

## Where doctor info appears

Doctor/provider information may appear in multiple files:
- `our-providers.html` — main profile cards with bio, credentials, specialties
- Service pages — doctor recommendation cards on relevant procedure pages
- `index.html` — homepage provider highlights
- JSON-LD structured data — schema.org Person/Physician entries

Search all HTML files for the doctor's name to find every reference.

## Profile fields

- **Name and credentials** (MD, DO, PA-C, AuD, FACS, etc.)
- **Title/role** (Otolaryngologist, Physician Assistant, Audiologist, etc.)
- **Specialties** (should match service pages where they're recommended)
- **Education** (medical school, residency, fellowships)
- **Board certifications**
- **Bio** (2-3 sentences, patient-friendly tone)
- **Photo** (if updating, use WebP with PNG fallback)

## Steps

1. Search all HTML files for the doctor's name to find every occurrence
2. Read `our-providers.html` for their current profile
3. Make the requested updates consistently across ALL files where they appear
4. Verify name and credentials match exactly everywhere

## Rules

- Never fabricate credentials, education, or certifications
- Doctor names must match their official professional listing
- If unsure about any credential or detail, ask the user to confirm
- Keep bios in patient-friendly language, not overly clinical

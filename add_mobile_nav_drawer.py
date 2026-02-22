#!/usr/bin/env python3
"""
add_mobile_nav_drawer.py  v2
Inserts the missing mobile nav drawer HTML into all Capital ENT subpages.
Also adds .hamburger{display:flex} and .util-bar{display:none} to 600px
media query where missing.
"""

import re
import os

BASE_DIR = "/Users/raymondbrown/Documents/Capital ENT Website"

PAGES = [
    "allergy.html",
    "balloon-sinuplasty.html",
    "ear-care.html",
    "ent-urgent-care.html",
    "faq.html",
    "hearing-aids.html",
    "insurance.html",
    "locations.html",
    "nose-sinus.html",
    "our-doctors.html",
    "patient-resources.html",
    "pediatric-ent.html",
    "reviews.html",
    "throat-sleep.html",
    "videos.html",
]

ACTIVE_LINKS = {
    "allergy.html":            ("allergy.html",            "Allergy"),
    "balloon-sinuplasty.html": ("balloon-sinuplasty.html", "Balloon Sinuplasty"),
    "ear-care.html":           ("ear-care.html",           "Ear Care &amp; Hearing"),
    "ent-urgent-care.html":    ("ent-urgent-care.html",    "ENT Urgent Care"),
    "faq.html":                ("faq.html",                "FAQ"),
    "hearing-aids.html":       ("hearing-aids.html",       "Hearing Aids"),
    "insurance.html":          ("insurance.html",          "Insurance &amp; Billing"),
    "locations.html":          ("locations.html",          "Locations"),
    "nose-sinus.html":         ("nose-sinus.html",         "Nose &amp; Sinus"),
    "our-doctors.html":        ("our-doctors.html",        "Our Doctors"),
    "reviews.html":            ("reviews.html",            "Patient Reviews"),
    "throat-sleep.html":       ("throat-sleep.html",       "Throat &amp; Sleep"),
    "videos.html":             ("videos.html",             "Videos"),
}


def build_mobile_nav_html(filename):
    active_info = ACTIVE_LINKS.get(filename)

    def link(href, text):
        if active_info and active_info[0] == href:
            return f'      <a href="{href}" class="active">{text}</a>'
        return f'      <a href="{href}">{text}</a>'

    lines = [
        '<div class="mobile-nav" id="mobileNav" role="dialog" aria-modal="true" aria-label="Navigation menu">',
        '  <div class="mobile-nav-overlay" id="mobileNavOverlay"></div>',
        '  <div class="mobile-nav-drawer">',
        '    <div class="mobile-nav-header">',
        '      <img src="CENT-Horizontal-Color.png" alt="Capital ENT &amp; Sinus Center" />',
        '      <button class="mobile-nav-close" id="mobileNavClose" aria-label="Close menu">&times;</button>',
        '    </div>',
        '    <nav class="mobile-nav-links">',
        link("index.html",             "Home"),
        link("ear-care.html",          "Ear Care &amp; Hearing"),
        link("hearing-aids.html",      "Hearing Aids"),
        link("nose-sinus.html",        "Nose &amp; Sinus"),
        link("balloon-sinuplasty.html","Balloon Sinuplasty"),
        link("throat-sleep.html",      "Throat &amp; Sleep"),
        link("allergy.html",           "Allergy"),
        link("our-doctors.html",       "Our Doctors"),
        link("locations.html",         "Locations"),
        link("ent-urgent-care.html",   "ENT Urgent Care"),
        link("reviews.html",           "Patient Reviews"),
        link("videos.html",            "Videos"),
        link("faq.html",               "FAQ"),
        link("insurance.html",         "Insurance &amp; Billing"),
        '    </nav>',
        '    <div class="mobile-nav-footer">',
        '      <a href="tel:5123394040">&#128222; Call 512-339-4040</a>',
        '    </div>',
        '  </div>',
        '</div>',
    ]
    return "\n".join(lines)


def find_navbar_closing_div_end(html):
    """Return the index just after the closing </div> of the navbar div."""
    navbar_match = re.search(
        r'<div[^>]+class=["\'][^"\']*navbar[^"\']*["\']',
        html, re.IGNORECASE
    )
    if not navbar_match:
        return None

    # Start after the opening tag; depth=1 because we've consumed one <div>
    pos = navbar_match.end()
    depth = 1

    while pos < len(html) and depth > 0:
        next_open  = re.search(r'<div\b', html[pos:], re.IGNORECASE)
        next_close = re.search(r'</div\s*>', html[pos:], re.IGNORECASE)

        if next_close is None:
            return None

        if next_open is not None and next_open.start() < next_close.start():
            depth += 1
            pos += next_open.end()
        else:
            depth -= 1
            if depth == 0:
                return pos + next_close.end()
            pos += next_close.end()

    return None


def add_mobile_nav_drawer(html, filename):
    if 'id="mobileNav"' in html:
        return html, None  # already present

    mobile_nav_html = "\n" + build_mobile_nav_html(filename) + "\n"

    # Prefer inserting after </header>
    header_close = re.search(r'</header>', html, re.IGNORECASE)
    if header_close:
        pos = header_close.end()
        return html[:pos] + mobile_nav_html + html[pos:], "after </header>"

    # Fallback: after navbar div closing </div>
    end_pos = find_navbar_closing_div_end(html)
    if end_pos is not None:
        return html[:end_pos] + mobile_nav_html + html[end_pos:], "after navbar closing </div>"

    return html, None


def update_600px_media(html):
    changes = []

    # Add .hamburger { display: flex; } after nav.main-nav hide
    pattern_nav = r'(nav\.main-nav\s*\{\s*display\s*:\s*none\s*!important\s*;\s*\})'
    nav_match = re.search(pattern_nav, html)
    if nav_match:
        after = html[nav_match.end():nav_match.end()+100]
        if '.hamburger' not in after:
            html = html[:nav_match.end()] + '\n    .hamburger { display: flex; }' + html[nav_match.end():]
            changes.append("added .hamburger{display:flex} in 600px media query")

    # Add .util-bar { display: none !important; } if missing
    media_600 = re.search(r'@media\s*\(max-width\s*:\s*600px\s*\)\s*\{', html)
    if media_600:
        block_start = media_600.end()
        depth = 1
        pos = block_start
        while pos < len(html) and depth > 0:
            if html[pos] == '{':
                depth += 1
            elif html[pos] == '}':
                depth -= 1
            pos += 1
        block_end = pos - 1  # position of block's closing }
        block_content = html[block_start:block_end]

        if '.util-bar' not in block_content:
            html = html[:block_end] + '    .util-bar { display: none !important; }\n  ' + html[block_end:]
            changes.append("added .util-bar{display:none} in 600px media query")

    return html, changes


def process_file(filename):
    filepath = os.path.join(BASE_DIR, filename)
    if not os.path.exists(filepath):
        print(f"  [SKIP] {filename} — file not found")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    actions = []

    html, drawer_loc = add_mobile_nav_drawer(html, filename)
    if drawer_loc:
        actions.append(f"added mobile nav drawer {drawer_loc}")

    html, media_changes = update_600px_media(html)
    actions.extend(media_changes)

    if not actions:
        print(f"  [NO CHANGE] {filename}")
        return

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  [DONE] {filename}")
    for action in actions:
        print(f"         - {action}")


def main():
    print("=" * 60)
    print("Capital ENT — Fixing Mobile Nav Drawer (v2)")
    print("=" * 60)
    for page in PAGES:
        process_file(page)
    print("=" * 60)
    print("Done.")


if __name__ == "__main__":
    main()

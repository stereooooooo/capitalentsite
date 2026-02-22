#!/usr/bin/env python3
"""
add_hamburger_menu.py
Adds a hamburger menu to all Capital ENT subpages.
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

# Active link mapping: filename -> (href, link_text)
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
    # patient-resources.html and pediatric-ent.html have no active match
}

HAMBURGER_CSS = """    /* ── HAMBURGER MENU ──────────────────────────────────────────── */
    .hamburger { display: none; flex-direction: column; justify-content: center; gap: 5px; width: 40px; height: 40px; background: none; border: none; cursor: pointer; padding: 4px; }
    .hamburger span { display: block; height: 2px; width: 24px; background: var(--navy); border-radius: 2px; transition: transform .25s, opacity .25s; }
    .hamburger.open span:nth-child(1) { transform: translateY(7px) rotate(45deg); }
    .hamburger.open span:nth-child(2) { opacity: 0; }
    .hamburger.open span:nth-child(3) { transform: translateY(-7px) rotate(-45deg); }
    /* Mobile drawer */
    .mobile-nav { display: none; position: fixed; inset: 0; z-index: 999; }
    .mobile-nav-overlay { position: absolute; inset: 0; background: rgba(0,0,0,.45); }
    .mobile-nav-drawer { position: absolute; top: 0; right: 0; width: 280px; max-width: 90vw; height: 100%; background: var(--white); display: flex; flex-direction: column; box-shadow: -4px 0 24px rgba(0,0,0,.2); overflow-y: auto; }
    .mobile-nav-header { display: flex; align-items: center; justify-content: space-between; padding: 18px 20px; border-bottom: 2px solid var(--red); }
    .mobile-nav-header img { height: 36px; width: auto; }
    .mobile-nav-close { background: none; border: none; cursor: pointer; font-size: 24px; color: var(--navy); line-height: 1; padding: 4px; }
    .mobile-nav-links { display: flex; flex-direction: column; padding: 16px 0; flex: 1; }
    .mobile-nav-links a { padding: 13px 24px; font-size: 15px; font-weight: 600; color: var(--navy); border-bottom: 1px solid var(--border); transition: background .15s, color .15s; }
    .mobile-nav-links a:hover { background: rgba(183,28,28,.05); color: var(--red); }
    .mobile-nav-footer { padding: 20px; }
    .mobile-nav-footer a { display: flex; align-items: center; justify-content: center; gap: 9px; background: var(--red); color: var(--white); padding: 14px; border-radius: 8px; font-size: 15px; font-weight: 700; }
    .mobile-nav.open { display: block; }
"""

HAMBURGER_BTN_HTML = """  <button class="hamburger" id="hamburgerBtn" aria-label="Open menu" aria-expanded="false">
    <span></span><span></span><span></span>
  </button>"""

def build_mobile_nav_html(filename):
    """Build the mobile nav drawer HTML with the correct active class."""
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
        link("index.html",            "Home"),
        link("ear-care.html",         "Ear Care &amp; Hearing"),
        link("hearing-aids.html",     "Hearing Aids"),
        link("nose-sinus.html",       "Nose &amp; Sinus"),
        link("balloon-sinuplasty.html","Balloon Sinuplasty"),
        link("throat-sleep.html",     "Throat &amp; Sleep"),
        link("allergy.html",          "Allergy"),
        link("our-doctors.html",      "Our Doctors"),
        link("locations.html",        "Locations"),
        link("ent-urgent-care.html",  "ENT Urgent Care"),
        link("reviews.html",          "Patient Reviews"),
        link("videos.html",           "Videos"),
        link("faq.html",              "FAQ"),
        link("insurance.html",        "Insurance &amp; Billing"),
        '    </nav>',
        '    <div class="mobile-nav-footer">',
        '      <a href="tel:5123394040">&#128222; Call 512-339-4040</a>',
        '    </div>',
        '  </div>',
        '</div>',
    ]
    return "\n".join(lines)

HAMBURGER_JS = """<script>
  /* ── HAMBURGER MENU ── */
  const hamburgerBtn = document.getElementById('hamburgerBtn');
  const mobileNav = document.getElementById('mobileNav');
  const mobileNavClose = document.getElementById('mobileNavClose');
  const mobileNavOverlay = document.getElementById('mobileNavOverlay');
  function openMobileNav() {
    mobileNav.classList.add('open');
    hamburgerBtn.classList.add('open');
    hamburgerBtn.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
  }
  function closeMobileNav() {
    mobileNav.classList.remove('open');
    hamburgerBtn.classList.remove('open');
    hamburgerBtn.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }
  hamburgerBtn.addEventListener('click', openMobileNav);
  mobileNavClose.addEventListener('click', closeMobileNav);
  mobileNavOverlay.addEventListener('click', closeMobileNav);
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeMobileNav(); });
</script>"""


def already_has_hamburger(html):
    return 'hamburgerBtn' in html


def insert_css(html):
    """Insert hamburger CSS before the first @media rule inside a <style> block."""
    # Find the <style> block
    style_match = re.search(r'(<style[^>]*>)(.*?)(</style>)', html, re.DOTALL | re.IGNORECASE)
    if not style_match:
        return html, False

    style_open  = style_match.group(1)
    style_body  = style_match.group(2)
    style_close = style_match.group(3)

    # Find first @media in style body
    media_match = re.search(r'@media', style_body)
    if not media_match:
        # Append before closing style tag
        new_style_body = style_body + "\n" + HAMBURGER_CSS
    else:
        insert_pos = media_match.start()
        new_style_body = style_body[:insert_pos] + HAMBURGER_CSS + "\n    " + style_body[insert_pos:]

    new_html = html[:style_match.start()] + style_open + new_style_body + style_close + html[style_match.end():]
    return new_html, True


def update_600px_media(html):
    """Add .hamburger { display: flex; } after nav.main-nav { display: none !important; }
       and .util-bar { display: none !important; } if not present."""
    changes = []

    # Pattern: inside @media (max-width: 600px) block, after nav.main-nav line
    # First add .hamburger { display: flex; } after nav.main-nav hide line
    pattern_nav = r'(nav\.main-nav\s*\{\s*display\s*:\s*none\s*!important\s*;\s*\})'
    if re.search(pattern_nav, html):
        # Check if hamburger display flex already exists nearby
        nav_match = re.search(pattern_nav, html)
        after_nav = html[nav_match.end():nav_match.end()+60]
        if '.hamburger' not in after_nav:
            replacement = r'\1\n    .hamburger { display: flex; }'
            html = re.sub(pattern_nav, replacement, html, count=1)
            changes.append("added .hamburger{display:flex} in 600px media query")

    # Add .util-bar hide if not present inside the 600px block
    media_600_match = re.search(r'@media\s*\(max-width\s*:\s*600px\s*\)\s*\{', html)
    if media_600_match:
        # Find the block content after opening brace
        block_start = media_600_match.end()
        # Check if util-bar is already there
        # Look at text from block_start until matching closing brace
        depth = 1
        pos = block_start
        while pos < len(html) and depth > 0:
            if html[pos] == '{':
                depth += 1
            elif html[pos] == '}':
                depth -= 1
            pos += 1
        block_content = html[block_start:pos-1]
        block_end = pos - 1  # position of the final }

        if '.util-bar' not in block_content:
            # Insert .util-bar rule before the closing brace of the 600px block
            insert_at = block_end
            html = html[:insert_at] + "    .util-bar { display: none !important; }\n  " + html[insert_at:]
            changes.append("added .util-bar{display:none} in 600px media query")

    return html, changes


def add_overflow_x_hidden(html):
    """Add overflow-x: hidden to html and body rules if not present."""
    changes = []

    # Handle html rule
    html_rule_match = re.search(r'(html\s*\{[^}]*)(})', html)
    if html_rule_match:
        rule_content = html_rule_match.group(1)
        if 'overflow-x' not in rule_content:
            new_rule = rule_content + "  overflow-x: hidden;\n  "
            html = html[:html_rule_match.start()] + new_rule + html_rule_match.group(2) + html[html_rule_match.end():]
            changes.append("added overflow-x:hidden to html rule")

    # Handle body rule - re-search after potential modification above
    body_rule_match = re.search(r'(body\s*\{[^}]*)(})', html)
    if body_rule_match:
        rule_content = body_rule_match.group(1)
        if 'overflow-x' not in rule_content:
            new_rule = rule_content + "  overflow-x: hidden;\n  "
            html = html[:body_rule_match.start()] + new_rule + body_rule_match.group(2) + html[body_rule_match.end():]
            changes.append("added overflow-x:hidden to body rule")

    return html, changes


def add_hamburger_button(html):
    """Add hamburger button after the closing </nav> tag inside the navbar div."""
    # We want the </nav> that closes the main nav links inside .navbar
    # Strategy: find the navbar section and locate </nav> within it
    # Look for the pattern: </nav> followed (eventually) by </div> or </header>
    # that closes the navbar container

    # Find navbar div opening
    navbar_match = re.search(r'<div[^>]+class=["\'][^"\']*navbar[^"\']*["\']', html, re.IGNORECASE)
    if not navbar_match:
        # Try header as container
        navbar_match = re.search(r'<header[^>]*>', html, re.IGNORECASE)

    if not navbar_match:
        return html, False

    search_start = navbar_match.start()

    # Find </nav> after the navbar start
    nav_close_match = re.search(r'</nav>', html[search_start:], re.IGNORECASE)
    if not nav_close_match:
        return html, False

    abs_pos = search_start + nav_close_match.end()
    html = html[:abs_pos] + "\n" + HAMBURGER_BTN_HTML + html[abs_pos:]
    return html, True


def add_mobile_nav_drawer(html, filename):
    """Add the mobile nav drawer after </header> or after the navbar's closing </div>."""
    mobile_nav_html = "\n" + build_mobile_nav_html(filename) + "\n"

    # Prefer inserting after </header>
    header_close = re.search(r'</header>', html, re.IGNORECASE)
    if header_close:
        pos = header_close.end()
        html = html[:pos] + mobile_nav_html + html[pos:]
        return html, "after </header>"

    # Fallback: after the navbar div closing tag
    # Find navbar div, then find its closing </div>
    navbar_match = re.search(r'<div[^>]+class=["\'][^"\']*navbar[^"\']*["\']', html, re.IGNORECASE)
    if navbar_match:
        # Walk forward to find the matching closing </div>
        search_start = navbar_match.start()
        tag_start = navbar_match.start()
        depth = 0
        pos = tag_start
        while pos < len(html):
            open_div = re.search(r'<div', html[pos:], re.IGNORECASE)
            close_div = re.search(r'</div>', html[pos:], re.IGNORECASE)
            if not close_div:
                break
            if open_div and open_div.start() < close_div.start():
                depth += 1
                pos += open_div.end()
            else:
                if depth == 0:
                    insert_pos = pos + close_div.end()
                    html = html[:insert_pos] + mobile_nav_html + html[insert_pos:]
                    return html, "after navbar closing </div>"
                depth -= 1
                pos += close_div.end()

    return html, None


def add_javascript(html):
    """Add hamburger JS before </body> or before first bottom <script> block."""
    # Try to find script tags near the bottom (last 25% of the file)
    bottom_start = max(0, int(len(html) * 0.5))
    bottom_html = html[bottom_start:]

    script_match = re.search(r'<script', bottom_html, re.IGNORECASE)
    if script_match:
        abs_pos = bottom_start + script_match.start()
        html = html[:abs_pos] + HAMBURGER_JS + "\n" + html[abs_pos:]
        return html, "before first bottom <script>"

    # Fall back to before </body>
    body_close = re.search(r'</body>', html, re.IGNORECASE)
    if body_close:
        pos = body_close.start()
        html = html[:pos] + HAMBURGER_JS + "\n" + html[pos:]
        return html, "before </body>"

    # Append at end
    html = html + "\n" + HAMBURGER_JS
    return html, "appended at end"


def process_file(filename):
    filepath = os.path.join(BASE_DIR, filename)
    if not os.path.exists(filepath):
        print(f"  [SKIP] {filename} — file not found")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    if already_has_hamburger(html):
        print(f"  [SKIP] {filename} — hamburger already present")
        return

    actions = []

    # 1. Insert CSS
    html, css_ok = insert_css(html)
    if css_ok:
        actions.append("inserted hamburger CSS before first @media rule")

    # 2. Update 600px media query
    html, media_changes = update_600px_media(html)
    actions.extend(media_changes)

    # 3. Add overflow-x: hidden to html/body
    html, overflow_changes = add_overflow_x_hidden(html)
    actions.extend(overflow_changes)

    # 4. Add hamburger button HTML
    html, btn_ok = add_hamburger_button(html)
    if btn_ok:
        actions.append("added hamburger button after </nav>")

    # 5. Add mobile nav drawer
    html, drawer_location = add_mobile_nav_drawer(html, filename)
    if drawer_location:
        actions.append(f"added mobile nav drawer {drawer_location}")

    # 6. Add JavaScript
    html, js_location = add_javascript(html)
    if js_location:
        actions.append(f"added hamburger JS {js_location}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  [DONE] {filename}")
    for action in actions:
        print(f"         - {action}")


def main():
    print("=" * 60)
    print("Capital ENT — Adding Hamburger Menu to Subpages")
    print("=" * 60)
    for page in PAGES:
        process_file(page)
    print("=" * 60)
    print("Done.")


if __name__ == "__main__":
    main()

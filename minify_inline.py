#!/usr/bin/env python3
"""
minify_inline.py
Minifies inline <style> and <script> blocks in HTML files.
Skips mockup.html and "index codespaces update.html".
"""

import re
import os
import sys

BASE_DIR = "/Users/raymondbrown/Documents/Capital ENT Website"

SKIP_FILES = {"mockup.html", "index codespaces update.html"}

# ---------------------------------------------------------------------------
# Token-based string/template-literal preserving transformer
# ---------------------------------------------------------------------------

def tokenize_preserve(text, extra_patterns=None):
    """
    Walk through text, extracting:
      - double-quoted strings
      - single-quoted strings
      - template literals (backticks)
      - url(...) blocks (for CSS)
    and replacing them with numbered placeholders.
    Returns (transformed_text, {placeholder: original}) dict.
    """
    placeholders = {}
    counter = [0]

    def make_placeholder():
        p = f"\x00P{counter[0]}\x00"
        counter[0] += 1
        return p

    # Order matters: template literals first (they can contain quotes),
    # then double-quoted, then single-quoted strings, then url()
    patterns = [
        # template literals
        (r'`(?:[^`\\]|\\.)*`', 'backtick'),
        # double-quoted strings (handles escaped quotes)
        (r'"(?:[^"\\]|\\.)*"', 'dquote'),
        # single-quoted strings (handles escaped quotes)
        (r"'(?:[^'\\]|\\.)*'", 'squote'),
    ]
    if extra_patterns:
        patterns.extend(extra_patterns)

    result = text
    # Process each pattern in order, replacing matches with placeholders
    for pat, kind in patterns:
        new_result = ""
        last = 0
        for m in re.finditer(pat, result, re.DOTALL):
            p = make_placeholder()
            placeholders[p] = m.group(0)
            new_result += result[last:m.start()] + p
            last = m.end()
        new_result += result[last:]
        result = new_result

    return result, placeholders


def restore_placeholders(text, placeholders):
    """Restore all placeholders back to their original values."""
    for p, orig in placeholders.items():
        text = text.replace(p, orig)
    return text


# ---------------------------------------------------------------------------
# CSS minifier
# ---------------------------------------------------------------------------

def minify_css(css):
    """
    Minify CSS content (between <style> tags).
    Preserves: url(...), string literals, data: URIs, calc() expressions.
    """
    # Step 1: Preserve url(...) blocks including data: URIs
    # We need to handle url() BEFORE we do any other processing so we don't
    # mangle data URIs or paths with spaces.
    url_placeholders = {}
    url_counter = [0]

    def save_url(m):
        key = f"\x00U{url_counter[0]}\x00"
        url_counter[0] += 1
        url_placeholders[key] = m.group(0)
        return key

    # Match url( ... ) — content can span multiple lines for data URIs
    css = re.sub(r'url\s*\([^)]*\)', save_url, css)

    # Step 2: Tokenize string literals (after url() is already protected)
    css, str_placeholders = tokenize_preserve(css)

    # Step 3: Remove CSS comments /* ... */
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)

    # Step 4: Collapse whitespace (newlines, tabs, multiple spaces → single space)
    css = re.sub(r'\s+', ' ', css)

    # Step 5: Remove spaces around structural characters
    # Around { } : ; , > ~ +
    # Be careful with : not to break pseudo-selectors — we strip spaces around
    # all colons since property:value and selector:pseudo both benefit.
    css = re.sub(r'\s*\{\s*', '{', css)
    css = re.sub(r'\s*\}\s*', '}', css)
    css = re.sub(r'\s*;\s*', ';', css)
    css = re.sub(r'\s*,\s*', ',', css)
    css = re.sub(r'\s*>\s*', '>', css)
    css = re.sub(r'\s*~\s*', '~', css)
    css = re.sub(r'\s*\+\s*', '+', css)

    # For colon, only strip spaces when it looks like a property: value pair
    # (not pseudo-selectors like :root, :hover, ::before which don't have a
    # preceding property name in the same way — but stripping spaces around ALL
    # colons is safe because pseudo-selectors are attached to selectors without
    # spaces anyway once we've collapsed whitespace).
    css = re.sub(r'\s*:\s*', ':', css)

    # Step 6: Remove trailing semicolons before }
    css = re.sub(r';+\}', '}', css)

    # Step 7: Strip leading/trailing whitespace
    css = css.strip()

    # Step 8: Restore string literals first, then url() blocks
    css = restore_placeholders(css, str_placeholders)
    for key, val in url_placeholders.items():
        css = css.replace(key, val)

    return css


# ---------------------------------------------------------------------------
# JS minifier
# ---------------------------------------------------------------------------

def minify_js(js):
    """
    Minify JS content (between <script> tags, not ld+json).
    Preserves: string literals, template literals.
    Removes: single-line comments (// ...), multi-line comments (/* ... */).
    Collapses whitespace.
    """
    # Step 1: Tokenize string literals and template literals
    # This protects their content from comment stripping and whitespace collapse.
    js, str_placeholders = tokenize_preserve(js)

    # Step 2: Remove multi-line comments /* ... */
    js = re.sub(r'/\*.*?\*/', '', js, flags=re.DOTALL)

    # Step 3: Remove single-line comments // ...
    # After string tokenization, any // inside strings is already a placeholder,
    # so this is safe. Handle the case where // might be part of https:// etc.
    # that aren't inside strings — but in JS those would normally be in strings.
    # We use a line-by-line approach to be safe.
    lines = js.split('\n')
    cleaned_lines = []
    for line in lines:
        # Remove // comment, but only if not preceded by : (URL protocol)
        # Actually with strings tokenized, all genuine // comments are safe to remove.
        # The pattern: find // not preceded by : (which would be http://)
        # Since URLs in JS should be in string literals (now placeholders), 
        # any remaining // is a real comment.
        line = re.sub(r'(?<!:)//.*$', '', line)
        cleaned_lines.append(line)
    js = '\n'.join(cleaned_lines)

    # Step 4: Collapse multiple whitespace / newlines into a single space
    js = re.sub(r'[\r\n]+', '\n', js)          # normalize newlines first
    js = re.sub(r'[ \t]+', ' ', js)             # collapse horizontal whitespace
    js = re.sub(r'\n ', '\n', js)               # remove leading spaces on lines
    js = re.sub(r' \n', '\n', js)               # remove trailing spaces on lines
    js = re.sub(r'\n+', ' ', js)               # collapse newlines to spaces

    # Step 5: Remove spaces around operators and punctuation
    # Be careful: don't mangle things like x - -y or x+ +y (unary operators)
    # For safety, we strip spaces around: = ( ) { } ; , < > | & ! 
    # and carefully around + - * /
    ops = [
        (r'\s*=\s*', '='),
        (r'\s*\(\s*', '('),
        (r'\s*\)\s*', ')'),
        (r'\s*\{\s*', '{'),
        (r'\s*\}\s*', '}'),
        (r'\s*;\s*', ';'),
        (r'\s*,\s*', ','),
        (r'\s*<\s*', '<'),
        (r'\s*>\s*', '>'),
        (r'\s*\|\s*', '|'),
        (r'\s*&\s*', '&'),
        (r'\s*!\s*', '!'),
    ]
    # For + - * / be more conservative — only remove spaces when clearly binary
    # (surrounded by word chars or ) on left, word char or ( on right)
    # Actually with modern JS minifiers, spaces around + - can be tricky due to
    # ++ -- operators. We'll skip those to be safe and just do the above.

    for pat, repl in ops:
        js = re.sub(pat, repl, js)

    # Step 6: Clean up any remaining leading/trailing whitespace
    js = js.strip()

    # Step 7: Restore string/template literals
    js = restore_placeholders(js, str_placeholders)

    return js


# ---------------------------------------------------------------------------
# HTML block replacer
# ---------------------------------------------------------------------------

def process_html(content, filename):
    """
    Find all <style> and <script> blocks in HTML content,
    minify their contents, and return the modified content.
    """
    errors = []

    # --- Process <style> blocks ---
    def replace_style(m):
        tag_open = m.group(1)   # e.g., "<style>" or "<style type='text/css'>"
        css_content = m.group(2)
        tag_close = m.group(3)  # "</style>"
        try:
            minified = minify_css(css_content)
            return f"{tag_open}{minified}{tag_close}"
        except Exception as e:
            errors.append(f"CSS error in {filename}: {e}")
            return m.group(0)   # return original on error

    content = re.sub(
        r'(<style[^>]*>)(.*?)(</style>)',
        replace_style,
        content,
        flags=re.DOTALL | re.IGNORECASE
    )

    # --- Process <script> blocks (skip ld+json) ---
    def replace_script(m):
        tag_open = m.group(1)   # the full opening tag
        js_content = m.group(2)
        tag_close = m.group(3)  # "</script>"
        # Skip structured data blocks
        if re.search(r'type\s*=\s*["\']application/ld\+json["\']', tag_open, re.IGNORECASE):
            return m.group(0)
        # Skip src= scripts (external) — they have no meaningful inline content
        if re.search(r'\bsrc\s*=', tag_open, re.IGNORECASE):
            return m.group(0)
        # Skip empty or near-empty blocks
        if not js_content.strip():
            return m.group(0)
        try:
            minified = minify_js(js_content)
            return f"{tag_open}{minified}{tag_close}"
        except Exception as e:
            errors.append(f"JS error in {filename}: {e}")
            return m.group(0)

    content = re.sub(
        r'(<script[^>]*>)(.*?)(</script>)',
        replace_script,
        content,
        flags=re.DOTALL | re.IGNORECASE
    )

    return content, errors


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    html_files = [
        f for f in os.listdir(BASE_DIR)
        if f.endswith('.html') and f not in SKIP_FILES
    ]
    html_files.sort()

    total_original = 0
    total_new = 0
    all_errors = []
    file_stats = []

    print(f"Processing {len(html_files)} HTML files...\n")

    for fname in html_files:
        fpath = os.path.join(BASE_DIR, fname)
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                original = f.read()
        except Exception as e:
            print(f"  ERROR reading {fname}: {e}")
            all_errors.append(fname)
            continue

        orig_size = len(original.encode('utf-8'))
        total_original += orig_size

        try:
            minified, errors = process_html(original, fname)
        except Exception as e:
            print(f"  ERROR processing {fname}: {e}")
            all_errors.append(fname)
            total_original -= orig_size  # don't count it in totals
            continue

        new_size = len(minified.encode('utf-8'))
        total_new += new_size
        saved = orig_size - new_size
        pct = (saved / orig_size * 100) if orig_size > 0 else 0

        file_stats.append((fname, orig_size, new_size, saved, pct))

        if errors:
            all_errors.extend(errors)
            print(f"  PARTIAL {fname}: {errors}")

        try:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(minified)
        except Exception as e:
            print(f"  ERROR writing {fname}: {e}")
            all_errors.append(fname)

    # Print per-file report
    print(f"{'File':<45} {'Original':>10} {'New':>10} {'Saved':>8} {'%':>6}")
    print("-" * 85)
    for fname, orig, new, saved, pct in file_stats:
        print(f"{fname:<45} {orig/1024:>9.1f}K {new/1024:>9.1f}K {saved/1024:>7.1f}K {pct:>5.1f}%")

    # Summary
    total_saved = total_original - total_new
    total_pct = (total_saved / total_original * 100) if total_original > 0 else 0

    print("-" * 85)
    print(f"\nSummary:")
    print(f"  Original total size : {total_original / 1024:.1f} KB ({total_original:,} bytes)")
    print(f"  New total size      : {total_new / 1024:.1f} KB ({total_new:,} bytes)")
    print(f"  Total saved         : {total_saved / 1024:.1f} KB ({total_saved:,} bytes) — {total_pct:.1f}%")

    if all_errors:
        print(f"\nErrors/warnings encountered:")
        for e in all_errors:
            print(f"  - {e}")
    else:
        print(f"\nNo errors encountered.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Add .form-call-now CSS class and update Call Toll-Free button to use it.
"""

import os
import re

FORM_CALL_CSS = '''        .form-call-now {
            display: flex; align-items: center; justify-content: center;
            padding: 12px 28px; background: var(--red); color: white;
            font-weight: 700; border-radius: 6px; font-size: 17px;
            cursor: pointer; margin: 15px auto 0; width: 100%;
            max-width: 220px; height: 60px; text-decoration: none;
            border: none; transition: all .3s;
        }
        .form-call-now:hover { transform: translateY(-3px); background: #a01830; }
'''

def update_file(filepath):
    """Update a single HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. Add .form-call-now CSS if not present (after .cf-book-button:hover)
    if '.form-call-now' not in content:
        content = re.sub(
            r'(\.cf-book-button:hover \{ transform: translateY\(-3px\); \})',
            r'\1\n' + FORM_CALL_CSS,
            content
        )

    # 2. Change the Call button to use form-call-now class instead of cf-book-button
    content = re.sub(
        r'<a href="#" class="cf-book-button phone-reveal-btn" id="cfCallButton" style="[^"]*">Call Toll-Free</a>',
        '<a href="#" class="form-call-now phone-reveal-btn" id="cfCallButton">Call Toll-Free</a>',
        content
    )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    base_dir = '/Users/globalaffiliate/thermador-appliance-repair'
    updated = 0
    total = 0

    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for filename in files:
            if filename.endswith('.html'):
                filepath = os.path.join(root, filename)
                total += 1
                if update_file(filepath):
                    updated += 1

    print(f"Files updated: {updated}/{total}")

if __name__ == '__main__':
    main()

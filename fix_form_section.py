#!/usr/bin/env python3
"""
Fix the contact form section - restore the form button functionality.
Only the nav header button should be phone reveal.
"""

import os
import re

def update_file(filepath):
    """Update a single HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. Restore the schedule text
    content = content.replace(
        'Call for Thermador Repair Service',
        'Schedule Your Thermador Repair Online'
    )

    # 2. Restore the contact form button (cfBookButton) back to a button
    content = re.sub(
        r'<a href="[^"]*" class="cf-book-button[^"]*" id="cfBookButton"[^>]*>[^<]*</a>',
        '<button class="cf-book-button" id="cfBookButton">Book Online</button>',
        content
    )

    # 3. Restore the reviews modal button back to a button (remove phone-reveal-btn)
    content = re.sub(
        r'<a href="[^"]*" id="reviewsCallBtn" class="phone-reveal-btn" style="([^"]+)">[^<]*</a>',
        r'<button id="reviewsCallBtn" style="\1">Book Online</button>',
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
                    print(f"Fixed: {filepath}")

    print(f"\n=== Summary ===")
    print(f"Total HTML files: {total}")
    print(f"Files fixed: {updated}")

if __name__ == '__main__':
    main()

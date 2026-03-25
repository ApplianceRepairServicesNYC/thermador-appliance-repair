#!/usr/bin/env python3
"""
Change Book Online button to dark blue (like Services button).
Call Toll-Free stays red.
"""

import os
import re

def update_file(filepath):
    """Update a single HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Change .cf-book-button background from red to dark blue gradient
    content = re.sub(
        r'(\.cf-book-button \{[^}]*background:) var\(--red\);',
        r'\1 linear-gradient(45deg, #1a1a2e, #2d2d4a);',
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

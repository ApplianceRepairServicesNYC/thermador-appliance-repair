#!/usr/bin/env python3
"""
Add Call Toll-Free button next to Book Online in the form section.
"""

import os
import re

def update_file(filepath):
    """Update a single HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Add Call Toll-Free button after Book Online button in the form section
    # Only if not already added
    if 'cfCallButton' not in content:
        content = re.sub(
            r'(<button class="cf-book-button" id="cfBookButton">Book Online</button>)',
            r'\1\n                <a href="#" class="cf-book-button phone-reveal-btn" id="cfCallButton" style="text-decoration:none;display:inline-block;margin-left:15px;">Call Toll-Free</a>',
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

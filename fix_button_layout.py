#!/usr/bin/env python3
"""
Fix the Call Toll-Free button layout to match other sites - centered below Book Online.
"""

import os
import re

def update_file(filepath):
    """Update a single HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Replace the current cfCallButton - remove margin-left, keep cf-book-button class for centering
    content = re.sub(
        r'<a href="#" class="cf-book-button phone-reveal-btn" id="cfCallButton" style="[^"]*">Call Toll-Free</a>',
        '<a href="#" class="cf-book-button phone-reveal-btn" id="cfCallButton" style="text-decoration:none;">Call Toll-Free</a>',
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

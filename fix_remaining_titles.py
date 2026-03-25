#!/usr/bin/env python3
"""
Fix remaining titles over 60 characters.
"""

import os
import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Shorten "Factory Certified Service" to "Factory Certified" in titles
    content = re.sub(
        r'(<title>[^<]+) - Factory Certified Service(</title>)',
        r'\1 - Factory Certified\2',
        content
    )

    # Shorten Columbia St Waterfront to Columbia St in titles
    content = re.sub(
        r'(<title>[^<]*)Columbia St Waterfront([^<]*</title>)',
        r'\1Columbia St\2',
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

    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for filename in files:
            if filename.endswith('.html'):
                filepath = os.path.join(root, filename)
                if fix_file(filepath):
                    updated += 1

    print(f"Files fixed: {updated}")

if __name__ == '__main__':
    main()

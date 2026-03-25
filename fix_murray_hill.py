#!/usr/bin/env python3
"""
Fix Murray Hill duplicate borough issue.
"""

import os
import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Fix double borough in titles
    content = content.replace('Manhattan Manhattan', 'Manhattan')
    content = content.replace('Queens Queens', 'Queens')
    content = content.replace('Brooklyn Brooklyn', 'Brooklyn')
    content = content.replace('Bronx Bronx', 'Bronx')

    # Fix double borough in H1s
    content = content.replace(', Manhattan, Manhattan', ', Manhattan')
    content = content.replace(', Queens, Queens', ', Queens')

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

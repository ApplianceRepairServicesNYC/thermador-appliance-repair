#!/usr/bin/env python3
"""
Make both buttons exactly the same size.
"""

import os
import re

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Update form-call-now CSS
    content = re.sub(
        r'\.form-call-now \{[^}]+\}',
        '''.form-call-now {
            display: flex; align-items: center; justify-content: center; padding: 12px 20px;
            background: var(--red); color: #fff; font-weight: 600;
            border-radius: 8px; border: none; cursor: pointer; margin: 10px auto;
            max-width: 220px; height: 60px; transition: all .3s; text-decoration: none;
            box-sizing: border-box;
        }''',
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
                if update_file(os.path.join(root, filename)):
                    updated += 1
    print(f"Files updated: {updated}")

if __name__ == '__main__':
    main()

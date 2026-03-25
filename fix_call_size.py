#!/usr/bin/env python3
"""
Fix Call Toll-Free button size to match Book Online exactly.
"""

import os
import re

# Match Book Online button exactly
OLD_CSS = '''        .form-call-now {
            display: flex; align-items: center; justify-content: center;
            padding: 12px 28px; background: var(--red); color: white;
            font-weight: 700; border-radius: 6px; font-size: 17px;
            cursor: pointer; margin: 15px auto 0; width: 100%;
            max-width: 220px; height: 60px; text-decoration: none;
            border: none; transition: all .3s;
        }
        .form-call-now:hover { transform: translateY(-3px); background: #a01830; }'''

NEW_CSS = '''        .form-call-now {
            display: flex; align-items: center; justify-content: center; padding: 12px 20px;
            background: var(--red); color: #fff; font-weight: 600;
            border-radius: 8px; border: none; cursor: pointer; margin: 10px auto; width: 100%;
            max-width: 220px; height: 60px; transition: all .3s; text-decoration: none;
        }
        .form-call-now:hover { transform: translateY(-3px); }'''

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    content = content.replace(OLD_CSS, NEW_CSS)

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

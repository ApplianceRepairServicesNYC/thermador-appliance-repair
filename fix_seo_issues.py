#!/usr/bin/env python3
"""
Fix SEO issues for Thermador site:
1. Shorten titles > 60 chars
2. Fix duplicate H1s for Murray Hill (add borough)
"""

import os
import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Determine borough from path
    borough = None
    if '/manhattan/' in filepath:
        borough = 'Manhattan'
    elif '/brooklyn/' in filepath:
        borough = 'Brooklyn'
    elif '/queens/' in filepath:
        borough = 'Queens'
    elif '/bronx/' in filepath:
        borough = 'Bronx'

    # === FIX 1: Shorten titles ===
    # Pattern: Remove " - Expert Service" from landing page titles
    content = re.sub(
        r'(<title>Thermador Appliance Repair [^<]+) - Expert Service(</title>)',
        r'\1\2',
        content
    )

    # Shorten "Columbia Street Waterfront District" to "Columbia St Waterfront"
    content = content.replace('Columbia Street Waterfront District', 'Columbia St Waterfront')

    # Shorten "Prospect Lefferts Gardens" to "Prospect Lefferts"
    content = content.replace('Prospect Lefferts Gardens', 'Prospect Lefferts')

    # Shorten "Douglaston-Little Neck" to "Douglaston"
    content = content.replace('Douglaston-Little Neck', 'Douglaston')

    # Shorten "South Street Seaport" to "South St Seaport"
    content = content.replace('South Street Seaport', 'South St Seaport')

    # Shorten "Morningside Heights" in titles only
    content = re.sub(r'(<title>[^<]*?)Morningside Heights', r'\1Morningside Hts', content)

    # Shorten "Washington Heights" in titles only
    content = re.sub(r'(<title>[^<]*?)Washington Heights', r'\1Washington Hts', content)

    # Shorten "Rockefeller Center" to "Rockefeller Ctr"
    content = re.sub(r'(<title>[^<]*?)Rockefeller Center', r'\1Rockefeller Ctr', content)

    # Shorten "Financial District" to "FiDi"
    content = re.sub(r'(<title>[^<]*?)Financial District', r'\1FiDi', content)

    # Shorten "Central Park South" to "Central Pk South"
    content = re.sub(r'(<title>[^<]*?)Central Park South', r'\1Central Pk South', content)

    # Shorten "Greenwich Village" to "Greenwich Vlg"
    content = re.sub(r'(<title>[^<]*?)Greenwich Village', r'\1Greenwich Vlg', content)

    # Shorten "Forest Hills Gardens" to "Forest Hills"
    content = content.replace('Forest Hills Gardens', 'Forest Hills')

    # Shorten "Flatiron District" to "Flatiron"
    content = re.sub(r'(<title>[^<]*?)Flatiron District', r'\1Flatiron', content)

    # Shorten "Bedford-Stuyvesant" to "Bed-Stuy"
    content = re.sub(r'(<title>[^<]*?)Bedford-Stuyvesant', r'\1Bed-Stuy', content)

    # Shorten "Battery Park City" to "Battery Park"
    content = re.sub(r'(<title>[^<]*?)Battery Park City', r'\1Battery Park', content)

    # Shorten "Stuyvesant Heights" to "Stuyvesant Hts"
    content = re.sub(r'(<title>[^<]*?)Stuyvesant Heights', r'\1Stuyvesant Hts', content)

    # Shorten "Prospect Park South" to "Prospect Pk South"
    content = re.sub(r'(<title>[^<]*?)Prospect Park South', r'\1Prospect Pk South', content)

    # === FIX 2: Murray Hill duplicate H1s - add borough ===
    if 'murray-hill' in filepath and borough:
        # Fix H1 tags to include borough
        content = re.sub(
            r'(<h1>Thermador [^<]+ in Murray Hill)(</h1>)',
            rf'\1, {borough}\2',
            content
        )
        # Also fix title to include borough if Murray Hill
        content = re.sub(
            r'(<title>Thermador [^<]+ Murray Hill)( [^<]*</title>)',
            rf'\1 {borough}\2',
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

    print(f"Files updated: {updated}")

if __name__ == '__main__':
    main()

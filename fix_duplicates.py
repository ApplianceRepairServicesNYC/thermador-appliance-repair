#!/usr/bin/env python3
"""
Fix duplicate H1s caused by shortening - restore unique names.
"""

import os

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Only fix files in the gardens/little-neck directories
    if 'forest-hills-gardens' in filepath:
        # Restore Forest Hills Gardens but shorter - use "FH Gardens"
        content = content.replace(
            'Thermador Appliance Repair in Forest Hills',
            'Thermador Appliance Repair in Forest Hills Gardens'
        )
        content = content.replace(
            'Thermador Refrigerator Repair in Forest Hills',
            'Thermador Refrigerator Repair in Forest Hills Gardens'
        )
        content = content.replace(
            'Thermador Oven Repair in Forest Hills',
            'Thermador Oven Repair in Forest Hills Gardens'
        )
        content = content.replace(
            'Thermador Cooktop Repair in Forest Hills',
            'Thermador Cooktop Repair in Forest Hills Gardens'
        )
        content = content.replace(
            'Thermador Dishwasher Repair in Forest Hills',
            'Thermador Dishwasher Repair in Forest Hills Gardens'
        )
        content = content.replace(
            'Thermador Microwave Repair in Forest Hills',
            'Thermador Microwave Repair in Forest Hills Gardens'
        )
        content = content.replace(
            'Thermador Wine Cooler Repair in Forest Hills',
            'Thermador Wine Cooler Repair in Forest Hills Gardens'
        )

    if 'douglaston-little-neck' in filepath:
        # Restore Douglaston-Little Neck but use "Douglaston-LN"
        content = content.replace(
            'Thermador Appliance Repair in Douglaston',
            'Thermador Appliance Repair in Douglaston-Little Neck'
        )
        content = content.replace(
            'Thermador Refrigerator Repair in Douglaston',
            'Thermador Refrigerator Repair in Douglaston-Little Neck'
        )
        content = content.replace(
            'Thermador Oven Repair in Douglaston',
            'Thermador Oven Repair in Douglaston-Little Neck'
        )
        content = content.replace(
            'Thermador Cooktop Repair in Douglaston',
            'Thermador Cooktop Repair in Douglaston-Little Neck'
        )
        content = content.replace(
            'Thermador Dishwasher Repair in Douglaston',
            'Thermador Dishwasher Repair in Douglaston-Little Neck'
        )
        content = content.replace(
            'Thermador Microwave Repair in Douglaston',
            'Thermador Microwave Repair in Douglaston-Little Neck'
        )
        content = content.replace(
            'Thermador Wine Cooler Repair in Douglaston',
            'Thermador Wine Cooler Repair in Douglaston-Little Neck'
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

#!/usr/bin/env python3
"""
Fix SEO for appliance-specific pages (3-level deep: borough/neighborhood/appliance-type).
These pages need proper location names in Schema.org, not "Refrigerator Repair" as location.
"""

import os
import re
import json
from pathlib import Path

BASE_DIR = Path('/Users/globalaffiliate/thermador-appliance-repair')
BASE_URL = "https://thermadorappliancerepairnyc.com"

# Appliance types to detect
APPLIANCE_TYPES = [
    'cooktop-repair', 'dishwasher-repair', 'microwave-repair',
    'oven-repair', 'refrigerator-repair', 'wine-cooler-repair'
]

def format_name(slug):
    """Convert slug to proper name."""
    return slug.replace("-", " ").title()

def get_page_info(file_path):
    """Extract location and appliance info from file path."""
    rel_path = file_path.relative_to(BASE_DIR)
    parts = list(rel_path.parts)

    # Remove index.html
    if parts[-1] == 'index.html':
        parts = parts[:-1]

    if len(parts) < 2:
        return None

    # Check if it's an appliance-specific page (3 levels: borough/neighborhood/appliance)
    if len(parts) >= 3 and parts[-1] in APPLIANCE_TYPES:
        borough = format_name(parts[0])
        neighborhood = format_name(parts[1])
        appliance = format_name(parts[2])
        page_url = f"{BASE_URL}/{'/'.join(parts)}/"
        return {
            'type': 'appliance',
            'borough': borough,
            'neighborhood': neighborhood,
            'appliance': appliance,
            'url': page_url,
            'location_name': f"{neighborhood}, {borough}"
        }

    # Location page (2 levels: borough/neighborhood)
    elif len(parts) == 2 and parts[-1] not in APPLIANCE_TYPES:
        borough = format_name(parts[0])
        neighborhood = format_name(parts[1])
        page_url = f"{BASE_URL}/{'/'.join(parts)}/"
        return {
            'type': 'location',
            'borough': borough,
            'neighborhood': neighborhood,
            'url': page_url,
            'location_name': f"{neighborhood}, {borough}"
        }

    return None


def fix_schema_in_file(file_path):
    """Fix the JSON-LD schema in a single HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False, None

    info = get_page_info(file_path)
    if not info:
        return False, None

    # Find the JSON-LD script block
    pattern = r'(<script type="application/ld\+json">)\s*(\{[^<]+\})\s*(</script>)'
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        return False, None

    try:
        schema = json.loads(match.group(2))
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {file_path}: {e}")
        return False, None

    # Update the schema
    schema['@id'] = info['url']
    schema['url'] = info['url']

    if info['type'] == 'appliance':
        # For appliance pages: "Thermador Refrigerator Repair Jamaica Estates, Queens"
        schema['name'] = f"Thermador {info['appliance']} {info['location_name']}"
        schema['areaServed'] = {
            "@type": "Place",
            "name": info['neighborhood'],
            "containedInPlace": {
                "@type": "City",
                "name": info['borough']
            }
        }
    else:
        # For location pages
        schema['name'] = f"Thermador Appliance Repair {info['location_name']}"
        schema['areaServed'] = {
            "@type": "Place",
            "name": info['neighborhood'],
            "containedInPlace": {
                "@type": "City",
                "name": info['borough']
            }
        }

    # Format the new JSON
    new_json = json.dumps(schema, indent=8)
    new_script = f'{match.group(1)}\n    {new_json}\n    {match.group(3)}'
    new_content = content[:match.start()] + new_script + content[match.end():]

    # Also fix og:description
    if info['type'] == 'appliance':
        new_og_desc = f"Expert Thermador {info['appliance'].lower()} in {info['location_name']}. Factory-certified technicians, same-day service available."
    else:
        new_og_desc = f"Expert Thermador appliance repair in {info['location_name']}. Same-day service for ovens, cooktops, ranges, refrigerators and more."

    og_pattern = r'<meta property="og:description" content="[^"]*">'
    new_content = re.sub(og_pattern, f'<meta property="og:description" content="{new_og_desc}">', new_content)

    # Write back
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, info['type']
    except Exception as e:
        print(f"Error writing {file_path}: {e}")
        return False, None


def main():
    # Find all index.html files in appliance-repair subdirectories
    html_files = list(BASE_DIR.rglob('index.html'))

    print(f"Found {len(html_files)} HTML files total")

    appliance_fixed = 0
    location_fixed = 0

    for html_file in html_files:
        # Skip non-page directories
        if 'assets' in str(html_file) or 'sitemap' in str(html_file):
            continue

        success, page_type = fix_schema_in_file(html_file)
        if success:
            if page_type == 'appliance':
                appliance_fixed += 1
            elif page_type == 'location':
                location_fixed += 1

    print(f"\nFixed {appliance_fixed} appliance-specific pages")
    print(f"Fixed {location_fixed} location pages")
    print(f"Total: {appliance_fixed + location_fixed} pages updated")
    print("\nDone! All pages now have correct location names in Schema.org")


if __name__ == "__main__":
    main()

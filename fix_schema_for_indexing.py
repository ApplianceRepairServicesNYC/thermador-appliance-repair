#!/usr/bin/env python3
"""
Fix Schema.org JSON-LD for unique page indexing.
Each page needs its own @id and url to be seen as unique by Google.
"""

import os
import re
import json
from pathlib import Path

def get_location_from_path(file_path, base_url="https://thermadorappliancerepairnyc.com"):
    """Extract location info from file path and build page URL."""
    rel_path = file_path.relative_to(Path('/Users/globalaffiliate/thermador-appliance-repair'))

    # Build the URL from the path
    parts = list(rel_path.parts)
    if parts[-1] == 'index.html':
        parts = parts[:-1]

    if not parts:
        return None, base_url + "/"

    page_url = base_url + "/" + "/".join(parts) + "/"

    # Extract location name for display
    if len(parts) >= 2:
        # e.g., manhattan/upper-east-side -> Upper East Side, Manhattan
        neighborhood = parts[-1].replace("-", " ").title()
        borough = parts[0].title()
        location_name = f"{neighborhood}, {borough}"
    elif len(parts) == 1:
        # e.g., manhattan -> Manhattan
        location_name = parts[0].replace("-", " ").title()
    else:
        location_name = None

    return location_name, page_url


def fix_schema_in_file(file_path):
    """Fix the JSON-LD schema in a single HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False

    location_name, page_url = get_location_from_path(file_path)

    # Find the JSON-LD script block
    pattern = r'(<script type="application/ld\+json">)\s*(\{[^<]+\})\s*(</script>)'
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        print(f"No JSON-LD found in {file_path}")
        return False

    try:
        schema = json.loads(match.group(2))
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {file_path}: {e}")
        return False

    # Update the schema with unique identifiers
    schema['@id'] = page_url
    schema['url'] = page_url

    # Update name to include location if it's a location page
    if location_name and 'name' in schema:
        schema['name'] = f"Thermador Appliance Repair {location_name}"

    # Update areaServed for location pages
    if location_name:
        parts = file_path.relative_to(Path('/Users/globalaffiliate/thermador-appliance-repair')).parts
        if len(parts) >= 2:
            neighborhood = parts[-2].replace("-", " ").title() if parts[-1] == 'index.html' else parts[-1].replace("-", " ").title()
            borough = parts[0].title()
            schema['areaServed'] = {
                "@type": "Place",
                "name": neighborhood,
                "containedInPlace": {
                    "@type": "City",
                    "name": borough
                }
            }

    # Format the new JSON with proper indentation
    new_json = json.dumps(schema, indent=8)

    # Build the new script block
    new_script = f'{match.group(1)}\n    {new_json}\n    {match.group(3)}'

    # Replace in content
    new_content = content[:match.start()] + new_script + content[match.end():]

    # Write back
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    except Exception as e:
        print(f"Error writing {file_path}: {e}")
        return False


def fix_og_description(file_path):
    """Update og:description to be location-specific."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False

    location_name, page_url = get_location_from_path(file_path)

    if not location_name:
        return False  # Skip homepage

    # Create location-specific og:description
    new_desc = f"Expert Thermador appliance repair in {location_name}. Same-day service for ovens, cooktops, ranges, refrigerators and more. Factory-certified technicians."

    # Replace og:description
    pattern = r'<meta property="og:description" content="[^"]*">'
    replacement = f'<meta property="og:description" content="{new_desc}">'

    new_content = re.sub(pattern, replacement, content)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False


def main():
    base_dir = Path('/Users/globalaffiliate/thermador-appliance-repair')

    # Find all index.html files
    html_files = list(base_dir.rglob('index.html'))

    print(f"Found {len(html_files)} HTML files")

    schema_fixed = 0
    og_fixed = 0

    for html_file in html_files:
        # Skip if it's in assets or other non-page directories
        if 'assets' in str(html_file):
            continue

        if fix_schema_in_file(html_file):
            schema_fixed += 1

        if fix_og_description(html_file):
            og_fixed += 1

    print(f"\nFixed Schema.org JSON-LD in {schema_fixed} files")
    print(f"Fixed og:description in {og_fixed} files")
    print("\nDone! Each page now has unique identifiers for Google indexing.")


if __name__ == "__main__":
    main()

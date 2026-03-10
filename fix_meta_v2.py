#!/usr/bin/env python3
"""
Script to fix meta descriptions - version 2 with better parsing.
"""

import os
import re
from pathlib import Path

BASE_DIR = "/Users/globalaffiliate/thermador-appliance-repair"

def extract_title(content):
    """Extract title from HTML content."""
    match = re.search(r'<title>([^<]+)</title>', content)
    return match.group(1) if match else None

def extract_meta_desc(content):
    """Extract current meta description."""
    match = re.search(r'<meta name="description" content="([^"]+)">', content)
    return match.group(1) if match else None

def get_info_from_path(filepath):
    """Extract service type and location from file path."""
    path_str = str(filepath)
    
    # Determine borough
    borough = None
    if '/manhattan/' in path_str:
        borough = 'Manhattan'
    elif '/brooklyn/' in path_str:
        borough = 'Brooklyn'
    elif '/queens/' in path_str:
        borough = 'Queens'
    elif '/bronx/' in path_str:
        borough = 'Bronx'
    
    # Determine service type
    service = None
    if '/refrigerator-repair/' in path_str:
        service = 'refrigerator repair'
    elif '/oven-repair/' in path_str:
        service = 'oven repair'
    elif '/cooktop-repair/' in path_str:
        service = 'cooktop repair'
    elif '/dishwasher-repair/' in path_str:
        service = 'dishwasher repair'
    elif '/microwave-repair/' in path_str:
        service = 'microwave repair'
    elif '/wine-cooler-repair/' in path_str:
        service = 'wine cooler repair'
    elif '/range-repair/' in path_str:
        service = 'range repair'
    
    # Determine neighborhood from path
    neighborhood = None
    parts = path_str.split('/')
    for i, part in enumerate(parts):
        if part in ['manhattan', 'brooklyn', 'queens', 'bronx'] and i + 1 < len(parts):
            next_part = parts[i + 1]
            if next_part not in ['index.html', 'refrigerator-repair', 'oven-repair', 'cooktop-repair', 
                                  'dishwasher-repair', 'microwave-repair', 'wine-cooler-repair', 'range-repair']:
                # Convert slug to readable name
                neighborhood = next_part.replace('-', ' ').title()
    
    return borough, neighborhood, service

def generate_description(borough, neighborhood, service):
    """Generate a unique meta description."""
    
    # Build location string
    if neighborhood and borough:
        full_location = f"{neighborhood}, {borough}"
    elif neighborhood:
        full_location = neighborhood
    elif borough:
        full_location = borough
    else:
        full_location = "New York City"
    
    # Generate description based on service type
    if service:
        desc = f"Expert Thermador {service} in {full_location}. Factory-certified technicians, same-day appointments. Call now for professional Thermador repair."
    else:
        desc = f"Professional Thermador appliance repair in {full_location}. Factory-certified technicians for ovens, cooktops, refrigerators & more. Same-day service available."
    
    return desc

def process_file(filepath):
    """Process a single HTML file and update its meta description."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        current_desc = extract_meta_desc(content)
        if not current_desc:
            return False, "No meta description found"
        
        # Get info from path
        borough, neighborhood, service = get_info_from_path(filepath)
        
        # Generate new description
        new_desc = generate_description(borough, neighborhood, service)
        
        # Replace the description
        new_content = re.sub(
            r'<meta name="description" content="[^"]+">',
            f'<meta name="description" content="{new_desc}">',
            content
        )
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, new_desc
    
    except Exception as e:
        return False, str(e)

def main():
    """Main function to process all HTML files."""
    count = 0
    errors = 0
    
    # Process all files except top-level service pages and homepage
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file == 'index.html':
                filepath = os.path.join(root, file)
                
                # Skip files we want to preserve
                rel_path = os.path.relpath(filepath, BASE_DIR)
                
                # Skip top-level files (homepage, service-level pages)
                depth = len(rel_path.split('/'))
                if depth <= 2:  # Skip homepage and /service/index.html
                    continue
                
                success, msg = process_file(filepath)
                if success:
                    count += 1
                    if count <= 5:
                        print(f"Updated: {filepath}")
                        print(f"  New description: {msg}")
                else:
                    errors += 1
                    print(f"Error: {filepath} - {msg}")
    
    print(f"\nTotal updated: {count}")
    print(f"Errors: {errors}")

if __name__ == '__main__':
    main()

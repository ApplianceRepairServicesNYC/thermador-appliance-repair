#!/usr/bin/env python3
"""
Script to generate unique meta descriptions for Thermador appliance repair pages.
"""

import os
import re
from pathlib import Path

BASE_DIR = "/Users/globalaffiliate/thermador-appliance-repair"

# Generic description to replace
GENERIC_DESC = 'Authorized Thermador appliance repair in NYC. Expert repair for ovens, cooktops, refrigerators, dishwashers, microwaves and more. Same-day service available across Manhattan, Brooklyn, Queens and Bronx.'

# Service type mappings for descriptions
SERVICE_DESCRIPTIONS = {
    'refrigerator-repair': 'refrigerator repair',
    'oven-repair': 'oven repair',
    'cooktop-repair': 'cooktop repair',
    'dishwasher-repair': 'dishwasher repair',
    'microwave-repair': 'microwave repair',
    'wine-cooler-repair': 'wine cooler repair',
    'range-repair': 'range repair',
}

def extract_title(content):
    """Extract title from HTML content."""
    match = re.search(r'<title>([^<]+)</title>', content)
    return match.group(1) if match else None

def parse_title(title):
    """Parse location and service from title like 'Thermador Refrigerator Repair Wakefield Bronx'"""
    if not title:
        return None, None
    
    # Common patterns:
    # "Thermador Refrigerator Repair Wakefield Bronx"
    # "Thermador Appliance Repair in Murray Hill"
    # "Thermador Cooktop Repair Murray Hill Manhattan"
    
    # Remove brand prefix
    title = title.replace('Thermador ', '')
    
    # Check for service types
    service = None
    location = None
    
    service_patterns = [
        ('Refrigerator Repair', 'refrigerator repair'),
        ('Oven Repair', 'oven repair'),
        ('Cooktop Repair', 'cooktop repair'),
        ('Dishwasher Repair', 'dishwasher repair'),
        ('Microwave Repair', 'microwave repair'),
        ('Wine Cooler Repair', 'wine cooler repair'),
        ('Range Repair', 'range repair'),
        ('Appliance Repair', 'appliance repair'),
    ]
    
    for pattern, svc in service_patterns:
        if pattern in title:
            service = svc
            # Extract location - everything after the service pattern
            parts = title.split(pattern)
            if len(parts) > 1:
                loc_part = parts[1].strip()
                # Clean up "in " prefix
                loc_part = loc_part.replace('in ', '').strip()
                if loc_part:
                    location = loc_part
            break
    
    return service, location

def generate_description(service, location, path):
    """Generate a unique meta description based on service and location."""
    
    # Determine borough from path
    path_str = str(path)
    borough = None
    if '/manhattan/' in path_str:
        borough = 'Manhattan'
    elif '/brooklyn/' in path_str:
        borough = 'Brooklyn'
    elif '/queens/' in path_str:
        borough = 'Queens'
    elif '/bronx/' in path_str:
        borough = 'Bronx'
    
    # Build location string
    if location and borough:
        full_location = f"{location}, {borough}"
    elif location:
        full_location = location
    elif borough:
        full_location = borough
    else:
        full_location = "NYC"
    
    # Generate description based on service type
    if service and service != 'appliance repair':
        desc = f"Expert Thermador {service} in {full_location}. Factory-certified technicians, same-day appointments. Call now for professional Thermador repair."
    else:
        desc = f"Professional Thermador appliance repair in {full_location}. Factory-certified technicians for ovens, cooktops, refrigerators & more. Same-day service available."
    
    return desc

def process_file(filepath):
    """Process a single HTML file and update its meta description."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if it has the generic description
        if GENERIC_DESC not in content:
            return False, "No generic description found"
        
        # Extract title
        title = extract_title(content)
        if not title:
            return False, "No title found"
        
        # Parse service and location
        service, location = parse_title(title)
        
        # Generate new description
        new_desc = generate_description(service, location, filepath)
        
        # Replace the generic description
        new_content = content.replace(
            f'<meta name="description" content="{GENERIC_DESC}">',
            f'<meta name="description" content="{new_desc}">'
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
    
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file == 'index.html':
                filepath = os.path.join(root, file)
                success, msg = process_file(filepath)
                if success:
                    count += 1
                    if count <= 5:
                        print(f"Updated: {filepath}")
                        print(f"  New description: {msg[:80]}...")
                elif "No generic description" not in msg:
                    errors += 1
                    print(f"Error: {filepath} - {msg}")
    
    print(f"\nTotal updated: {count}")
    print(f"Errors: {errors}")

if __name__ == '__main__':
    main()

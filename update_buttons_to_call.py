#!/usr/bin/env python3
"""
Update all 'Book Online' buttons to click-to-reveal obfuscated phone buttons.
First click reveals number, second click initiates call.
"""

import os
import re

PHONE_DISPLAY = "1 (800) 778-3572"
PHONE_TEL = "tel:+18007783572"

OBFUSCATION_SCRIPT = f'''<script>
(function() {{
    function initPhoneReveal(btn) {{
        btn.addEventListener('click', function(e) {{
            if (!this.dataset.revealed) {{
                e.preventDefault();
                this.textContent = 'Call {PHONE_DISPLAY}';
                this.href = "{PHONE_TEL}";
                this.dataset.revealed = 'true';
            }}
        }});
    }}
    document.querySelectorAll('.phone-reveal-btn').forEach(initPhoneReveal);
}})();
</script>'''

def update_file(filepath):
    """Update a single HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. Replace nav button - click to reveal (handle both original and already converted)
    content = re.sub(
        r'<button class="nav-call-btn" id="navCallNow">Book Online</button>',
        '<a href="#" class="nav-call-btn phone-reveal-btn" id="navCallNow" style="text-decoration:none;">Call Toll-Free</a>',
        content
    )
    content = re.sub(
        r'<a href="[^"]*" class="nav-call-btn[^"]*" id="navCallNow"[^>]*>[^<]*</a>',
        '<a href="#" class="nav-call-btn phone-reveal-btn" id="navCallNow" style="text-decoration:none;">Call Toll-Free</a>',
        content
    )

    # 2. Replace contact form book button - click to reveal
    content = re.sub(
        r'<button class="cf-book-button" id="cfBookButton">Book Online</button>',
        '<a href="#" class="cf-book-button phone-reveal-btn" id="cfBookButton" style="text-decoration:none;display:inline-block;">Call Toll-Free</a>',
        content
    )
    content = re.sub(
        r'<a href="[^"]*" class="cf-book-button[^"]*" id="cfBookButton"[^>]*>[^<]*</a>',
        '<a href="#" class="cf-book-button phone-reveal-btn" id="cfBookButton" style="text-decoration:none;display:inline-block;">Call Toll-Free</a>',
        content
    )

    # 3. Replace reviews modal button - click to reveal
    content = re.sub(
        r'<button id="reviewsCallBtn" style="([^"]+)">Book Online</button>',
        r'<a href="#" id="reviewsCallBtn" class="phone-reveal-btn" style="\1text-decoration:none;">Call Toll-Free</a>',
        content
    )
    content = re.sub(
        r'<a href="[^"]*" id="reviewsCallBtn" class="[^"]*" style="([^"]+)">[^<]*</a>',
        r'<a href="#" id="reviewsCallBtn" class="phone-reveal-btn" style="\1">Call Toll-Free</a>',
        content
    )

    # 4. Update the schedule text above the button
    content = content.replace(
        'Schedule Your Thermador Repair Online',
        'Call for Thermador Repair Service'
    )

    # 5. Remove old navCallNow JS handler (multiple patterns)
    content = re.sub(
        r"document\.getElementById\('navCallNow'\)\.addEventListener\('click', function\(\) \{ document\.getElementById\('cf-schedule-container'\)\.scrollIntoView\(\{behavior:'smooth'\}\); setTimeout\(toggleForm, 500\); \}\);",
        "// navCallNow handled by phone reveal",
        content
    )
    content = content.replace(
        "// Phone link - no JS handler needed",
        "// navCallNow handled by phone reveal"
    )
    content = content.replace(
        "// Phone reveal handled by initPhoneReveal",
        "// navCallNow handled by phone reveal"
    )

    # 6. Add the obfuscation JS before </body> if not already present
    if 'initPhoneReveal' not in content:
        # Insert before the closing </body> tag
        content = re.sub(
            r'(</body>)',
            OBFUSCATION_SCRIPT + r'\n\1',
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
    total = 0

    for root, dirs, files in os.walk(base_dir):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for filename in files:
            if filename.endswith('.html'):
                filepath = os.path.join(root, filename)
                total += 1
                if update_file(filepath):
                    updated += 1
                    print(f"Updated: {filepath}")

    print(f"\n=== Summary ===")
    print(f"Total HTML files: {total}")
    print(f"Files updated: {updated}")

if __name__ == '__main__':
    main()

"""
Reward Script: HTML5 slide deck export from LibreOffice Impress
Task ID: impress_gf5_049
Domain: libreoffice_impress
Scoring:
  C1: index.html exists in /home/user/html_slides/ (0.10)
  C2: Valid HTML5 structure (DOCTYPE, html, head, body) (0.10)
  C3: 10 <section> elements with id="slide-N" (0.20)
  C4: Sections contain text content from presentation slides (0.15)
  C5: 10 JPEG images (slide_01.jpg..slide_10.jpg) at 800x600 (0.20)
  C6: Dark theme CSS (dark background) (0.10)
  C7: Navigation links/buttons present (0.15)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'impress_gf5_049'
HTML_DIR = os.path.join(WORKDIR, 'html_slides')
HTML_FILE = os.path.join(HTML_DIR, 'index.html')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: index.html exists (0.10 points)
    # This is a precondition gate — if the file doesn't exist, nothing else can be checked.
    # On initial_env this file does NOT exist, so this correctly differentiates states.
    try:
        if os.path.isfile(HTML_FILE):
            html_content = open(HTML_FILE, 'r', encoding='utf-8', errors='replace').read()
            if len(html_content) > 100:
                print(f"PASS: Component 1 — index.html exists ({len(html_content)} bytes) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 1 — index.html exists but too small ({len(html_content)} bytes)")
                print("REWARD: 0.0")
                return 0.0
        else:
            print(f"FAIL: Component 1 — index.html not found at {HTML_FILE}")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: Valid HTML5 structure (0.10 points)
    try:
        has_doctype = '<!DOCTYPE html>' in html_content or '<!doctype html>' in html_content.lower()
        has_html_tag = '<html' in html_content.lower()
        has_head = '<head' in html_content.lower()
        has_body = '<body' in html_content.lower()
        has_style_or_css = '<style' in html_content.lower() or 'rel="stylesheet"' in html_content.lower()

        if has_doctype and has_html_tag and has_head and has_body and has_style_or_css:
            print(f"PASS: Component 2 — Valid HTML5 structure with CSS (0.10 pts)")
            total_score += 0.10
        else:
            missing = []
            if not has_doctype: missing.append('DOCTYPE')
            if not has_html_tag: missing.append('html tag')
            if not has_head: missing.append('head')
            if not has_body: missing.append('body')
            if not has_style_or_css: missing.append('CSS/style')
            print(f"FAIL: Component 2 — Missing HTML5 elements: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 10 <section> elements with id="slide-N" (0.20 points)
    try:
        # Find all section elements with slide IDs
        section_pattern = r'<section[^>]*id=["\']slide-(\d+)["\']'
        sections = re.findall(section_pattern, html_content, re.IGNORECASE)
        section_ids = sorted([int(s) for s in sections])

        expected_ids = list(range(1, 11))
        if section_ids == expected_ids:
            print(f"PASS: Component 3 — All 10 sections with correct slide IDs found (0.20 pts)")
            total_score += 0.20
        elif len(section_ids) >= 8:
            # Partial credit for most sections present
            partial = 0.20 * (len(section_ids) / 10)
            print(f"PARTIAL: Component 3 — {len(section_ids)}/10 sections found ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Found {len(section_ids)}/10 sections: {section_ids}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Sections contain text content from the presentation slides (0.15 points)
    try:
        # Check for key text from at least a few slides
        # These are distinctive phrases from the presentation that should appear in the HTML
        key_phrases = [
            'Strategic Planning Review',       # Slide 1 title
            'Executive Summary',               # Slide 2 title
            'Revenue Breakdown',               # Slide 3 title
            'Competitive Landscape',           # Slide 4 title
            'Product Roadmap',                 # Slide 5 title
            'Client Wins',                     # Slide 6 title
            'Talent Acquisition',              # Slide 7 title
            'Financial Outlook',               # Slide 8 title
            'Risk Assessment',                 # Slide 9 title
            'Action Items',                    # Slide 10 title
        ]
        found_count = sum(1 for phrase in key_phrases if phrase.lower() in html_content.lower())

        if found_count >= 9:
            print(f"PASS: Component 4 — {found_count}/10 slide text contents embedded (0.15 pts)")
            total_score += 0.15
        elif found_count >= 5:
            partial = 0.15 * (found_count / 10)
            print(f"PARTIAL: Component 4 — {found_count}/10 slide texts found ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — Only {found_count}/10 slide texts found in HTML")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: 10 JPEG images at 800x600 (0.20 points)
    try:
        from PIL import Image
        correct_images = 0
        for i in range(1, 11):
            img_name = f'slide_{i:02d}.jpg'
            img_path = os.path.join(HTML_DIR, img_name)
            if os.path.isfile(img_path):
                img = Image.open(img_path)
                w, h = img.size
                if w == 800 and h == 600:
                    correct_images += 1
                else:
                    print(f"  INFO: {img_name} has size {w}x{h}, expected 800x600")
            else:
                print(f"  INFO: {img_name} not found")

        if correct_images == 10:
            print(f"PASS: Component 5 — All 10 slide JPEGs at 800x600 (0.20 pts)")
            total_score += 0.20
        elif correct_images >= 1:
            partial = 0.20 * (correct_images / 10)
            print(f"PARTIAL: Component 5 — {correct_images}/10 correct JPEGs ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 — No correct slide JPEGs found")
    except ImportError:
        # Fallback: just check file existence and non-zero size
        existing = 0
        for i in range(1, 11):
            img_name = f'slide_{i:02d}.jpg'
            img_path = os.path.join(HTML_DIR, img_name)
            if os.path.isfile(img_path) and os.path.getsize(img_path) > 1000:
                existing += 1
        if existing == 10:
            print(f"PASS: Component 5 — All 10 slide JPEGs exist (PIL unavailable, size not checked) (0.20 pts)")
            total_score += 0.20
        elif existing >= 1:
            partial = 0.20 * (existing / 10)
            print(f"PARTIAL: Component 5 — {existing}/10 JPEGs exist ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 — No slide JPEGs found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Dark theme CSS (0.10 points)
    try:
        # Check for dark background color in CSS
        # Common dark theme patterns: dark background-color, background: #1a1a..., #000, #111, #222, etc.
        css_match = re.search(r'<style[^>]*>(.*?)</style>', html_content, re.DOTALL | re.IGNORECASE)
        if css_match:
            css_content = css_match.group(1)
            # Look for dark background colors
            dark_bg_patterns = [
                r'background-color\s*:\s*#([0-3][0-9a-fA-F][0-3][0-9a-fA-F][0-3][0-9a-fA-F])',  # #0x0x0x where x <= 3
                r'background-color\s*:\s*#([0-9a-fA-F]{6})',
                r'background\s*:\s*#([0-9a-fA-F]{6})',
            ]
            # Check if background color is "dark" (low RGB values)
            dark_found = False
            for pattern in dark_bg_patterns:
                matches = re.findall(pattern, css_content)
                for hex_color in matches:
                    if len(hex_color) == 6:
                        r = int(hex_color[0:2], 16)
                        g = int(hex_color[2:4], 16)
                        b = int(hex_color[4:6], 16)
                        # Dark = average RGB below 80
                        if (r + g + b) / 3 < 80:
                            dark_found = True
                            print(f"  INFO: Found dark background color: #{hex_color} (RGB: {r},{g},{b})")
                            break
                if dark_found:
                    break

            # Also check for white/light text color
            white_text = re.search(r'color\s*:\s*#(f{3,6}|fff\w*|e\w{5})', css_content, re.IGNORECASE)
            light_text = re.search(r'color\s*:\s*#?white|color\s*:\s*white', css_content, re.IGNORECASE)

            if dark_found and (white_text or light_text):
                print(f"PASS: Component 6 — Dark theme CSS with light text (0.10 pts)")
                total_score += 0.10
            elif dark_found:
                print(f"PASS: Component 6 — Dark theme CSS background found (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 6 — No dark theme background detected in CSS")
        else:
            print(f"FAIL: Component 6 — No <style> block found")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: Navigation links/buttons (0.15 points)
    try:
        # Check for navigation elements: Previous/Next links or buttons
        nav_patterns = [
            r'(Previous|Prev|&larr;|←)',
            r'(Next|&rarr;|→)',
            r'href=["\']#slide-',
        ]
        nav_found = 0
        for pattern in nav_patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                nav_found += 1

        # Also check for JavaScript keyboard navigation
        has_js_nav = ('ArrowRight' in html_content or 'ArrowLeft' in html_content or
                      'keydown' in html_content or 'keyboard' in html_content.lower())

        if nav_found >= 2 or (nav_found >= 1 and has_js_nav):
            print(f"PASS: Component 7 — Navigation present (links: {nav_found}/3, JS nav: {has_js_nav}) (0.15 pts)")
            total_score += 0.15
        elif nav_found >= 1 or has_js_nav:
            print(f"PARTIAL: Component 7 — Some navigation found ({nav_found} link patterns, JS: {has_js_nav}) (0.08 pts)")
            total_score += 0.08
        else:
            print(f"FAIL: Component 7 — No navigation elements found")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.isdir(HTML_DIR):
    print(f"Directory not found: {HTML_DIR}")
    print("REWARD: 0.0")
else:
    verify_task()

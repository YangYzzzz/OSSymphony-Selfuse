"""
Reward Script: Interactive menu slide with hyperlinks and Home buttons
Task ID: impress_gf2_003
Domain: libreoffice_impress
Scoring:
  Component 1 (0.5): Slide 2 text boxes have hyperlinks to correct slides
    - 'Introduction' -> slide 3 (0.125)
    - 'Methodology' -> slide 5 (0.125)
    - 'Results' -> slide 7 (0.125)
    - 'Conclusion' -> slide 9 (0.125)
  Component 2 (0.5): Slides 3, 5, 7, 9 have 'Home' button linking to slide 2
    - Each slide (0.125)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_gf2_003'

NS_RELS = 'http://schemas.openxmlformats.org/package/2006/relationships'
NS_A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
NS_P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
NS_R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'


def get_slide_rels(zf, slide_num):
    """Get relationship ID -> target slide number mapping for a slide."""
    rels = {}
    try:
        with zf.open(f'ppt/slides/_rels/slide{slide_num}.xml.rels') as f:
            root = ET.parse(f).getroot()
            for rel in root.findall(f'{{{NS_RELS}}}Relationship'):
                rel_type = rel.get('Type', '')
                target = rel.get('Target', '')
                rid = rel.get('Id', '')
                # Only care about slide-to-slide relationships
                if 'relationships/slide' in rel_type and target.startswith('slide') and target.endswith('.xml'):
                    target_num = int(target.replace('slide', '').replace('.xml', ''))
                    rels[rid] = target_num
    except (KeyError, Exception):
        pass
    return rels


def get_shapes_with_hyperlinks(zf, slide_num):
    """Get list of (text, target_slide_num) for shapes with hlinkClick on a slide."""
    results = []
    rels = get_slide_rels(zf, slide_num)

    try:
        with zf.open(f'ppt/slides/slide{slide_num}.xml') as f:
            root = ET.parse(f).getroot()

        # Find all shape trees (sp elements)
        for sp in root.findall(f'.//{{{NS_P}}}sp'):
            # Extract text from the shape
            texts = []
            for t_elem in sp.findall(f'.//{{{NS_A}}}t'):
                if t_elem.text:
                    texts.append(t_elem.text)
            shape_text = ''.join(texts).strip()

            # Find hlinkClick elements with action ppaction://hlinksldjump
            for hlink in sp.findall(f'.//{{{NS_A}}}hlinkClick'):
                action = hlink.get('action', '')
                rid = hlink.get(f'{{{NS_R}}}id', '')
                if action == 'ppaction://hlinksldjump' and rid in rels:
                    results.append((shape_text, rels[rid]))

    except (KeyError, Exception):
        pass

    return results


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Slide 2 hyperlinks (0.5 points total, 0.125 each)
    # Expected: Introduction->3, Methodology->5, Results->7, Conclusion->9
    expected_links = {
        'Introduction': 3,
        'Methodology': 5,
        'Results': 7,
        'Conclusion': 9,
    }

    try:
        slide2_links = get_shapes_with_hyperlinks(zf, 2)
        # Build mapping: text -> target slide
        link_map = {}
        for text, target in slide2_links:
            link_map[text] = target

        for label, expected_target in expected_links.items():
            if label in link_map and link_map[label] == expected_target:
                print(f"PASS: Slide 2 '{label}' links to slide {expected_target} (0.125 pts)")
                total_score += 0.125
            else:
                actual = link_map.get(label, 'NO LINK')
                print(f"FAIL: Slide 2 '{label}' expected link to slide {expected_target}, found: {actual}")
    except Exception as e:
        print(f"ERROR: Component 1 (Slide 2 hyperlinks) - {e}")

    # Component 2: Home buttons on slides 3, 5, 7, 9 (0.5 points total, 0.125 each)
    # Each should have a shape with text 'Home' linking to slide 2
    home_slides = [3, 5, 7, 9]

    for sn in home_slides:
        try:
            links = get_shapes_with_hyperlinks(zf, sn)
            # Look for a shape whose text contains 'Home' (case-insensitive) linking to slide 2
            home_found = any('home' in text.lower() and target == 2 for text, target in links)

            if home_found:
                print(f"PASS: Slide {sn} has 'Home' button linking to slide 2 (0.125 pts)")
                total_score += 0.125
            else:
                print(f"FAIL: Slide {sn} missing 'Home' button linking to slide 2. Found links: {links}")
        except Exception as e:
            print(f"ERROR: Component 2 (Slide {sn} Home button) - {e}")

    zf.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

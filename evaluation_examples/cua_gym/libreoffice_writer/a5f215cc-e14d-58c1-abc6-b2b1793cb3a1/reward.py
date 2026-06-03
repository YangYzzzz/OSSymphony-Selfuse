"""
Reward Script: Extract Impress slides to Writer document with headings and bullets
Task ID: osworld_multi_apps_impress_text_to_writer_004
Domain: libreoffice_writer
Scoring:
  Component 1: training_notes.odt file exists            — 0.15 pts
  Component 2: Exactly 6 Heading 2 sections present      — 0.25 pts
  Component 3: All 6 slide titles match expected format  — 0.25 pts
  Component 4: Body list items present under headings    — 0.20 pts
  Component 5: Two-level hierarchy (sub-bullets) present — 0.15 pts
  Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_impress_text_to_writer_004'
OUTPUT_FILE = os.path.join(WORKDIR, 'training_notes.odt')

# Expected slide titles (from the training_deck.odp source)
EXPECTED_SLIDE_TITLES = [
    "Slide 1: Onboarding Overview",
    "Slide 2: Company Culture and Values",
    "Slide 3: Product Portfolio",
    "Slide 4: Sales Process",
    "Slide 5: Technical Infrastructure",
    "Slide 6: Career Development",
]

NS_TEXT = 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'
NS_OFFICE = 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'


def extract_odt_structure(file_path):
    """
    Parse the ODT content.xml and return structured data.
    Returns a dict with:
      - headings: list of (level, style_name, text) tuples
      - total_list_items: total count of all list-item elements
      - top_level_list_count: count of direct <text:list> under body
      - nested_list_items: count of list-items that are nested (sub-bullets)
    """
    with zipfile.ZipFile(file_path, 'r') as z:
        with z.open('content.xml') as f:
            content = f.read().decode('utf-8')

    root = ET.fromstring(content)
    body = root.find(f'.//{{{NS_OFFICE}}}body/{{{NS_OFFICE}}}text')
    if body is None:
        raise ValueError("Could not find office:text body element")

    headings = []
    for child in body:
        tag = child.tag.split('}')[1] if '}' in child.tag else child.tag
        if tag == 'h':
            level = child.get(f'{{{NS_TEXT}}}outline-level', '?')
            style_name = child.get(f'{{{NS_TEXT}}}style-name', '')
            text = ''.join(child.itertext()).strip()
            headings.append((level, style_name, text))

    # Count total list items at all levels
    all_list_items = body.findall(f'.//{{{NS_TEXT}}}list-item')
    total_list_items = len(all_list_items)

    # Count top-level lists (direct children of body)
    top_level_lists = [c for c in body if c.tag.split('}')[1] == 'list']
    top_level_list_count = len(top_level_lists)

    # Count sub-bullet items: In ODT exported from LibreOffice Writer,
    # sub-bullets are stored in separate <text:list> elements with a different
    # list style (e.g., "WWNum2") rather than as physically nested list elements.
    # Both naming conventions are handled: nested sub-lists OR distinct style names.
    #
    # Approach 1: Check for physically nested lists (standard ODF nesting)
    nested_item_count_nested = 0
    for li in all_list_items:
        nested_lists = li.findall(f'{{{NS_TEXT}}}list')
        if nested_lists:
            for nl in nested_lists:
                sub_items = nl.findall(f'{{{NS_TEXT}}}list-item')
                nested_item_count_nested += len(sub_items)

    # Approach 2: Check for separate lists with a secondary list style (e.g. WWNum2, List_20_Bullet_20_2)
    # Top-level lists with style names that indicate sub-bullet level
    all_lists_in_body = [c for c in body if c.tag.split('}')[1] == 'list']
    sub_bullet_style_keywords = ['2', 'sub', 'Sub', 'Level2', 'Bullet_2', 'indent']
    sub_bullet_list_items = 0
    for lst in all_lists_in_body:
        style_name = lst.get(f'{{{NS_TEXT}}}style-name', '')
        # Heuristic: style name contains '2' typically = level 2
        if any(kw in style_name for kw in sub_bullet_style_keywords):
            items = lst.findall(f'{{{NS_TEXT}}}list-item')
            sub_bullet_list_items += len(items)

    # Also check paragraph styles for sub-bullet level
    # P2 style typically used for sub-bullets in auto-styles
    p2_count = 0
    for p in body.findall(f'.//{{{NS_TEXT}}}p'):
        s = p.get(f'{{{NS_TEXT}}}style-name', '')
        if s == 'P2' or s.endswith('_2') or 'Sub' in s:
            text = ''.join(p.itertext()).strip()
            if text:
                p2_count += 1

    # Use maximum of approaches to be most permissive
    nested_item_count = max(nested_item_count_nested, sub_bullet_list_items, p2_count)

    return {
        'headings': headings,
        'total_list_items': total_list_items,
        'top_level_list_count': top_level_list_count,
        'nested_list_items': nested_item_count,
    }


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists (0.15 points)
    # This FAILS on initial_env (no training_notes.odt) → PASSES on golden_env
    try:
        if os.path.exists(file_path):
            print(f"PASS: Component 1 — training_notes.odt exists (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — training_notes.odt not found at {file_path}")
            # File doesn't exist; no further checks possible
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Parse file structure
    try:
        structure = extract_odt_structure(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse ODT file: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    headings = structure['headings']
    total_list_items = structure['total_list_items']
    nested_list_items = structure['nested_list_items']

    # Component 2: Exactly 6 Heading 2 sections present (0.25 points)
    # This FAILS on initial_env → PASSES on golden_env
    try:
        heading2_list = [(lvl, style, text) for (lvl, style, text) in headings if lvl == '2']
        num_heading2 = len(heading2_list)
        if num_heading2 == 6:
            print(f"PASS: Component 2 — Exactly 6 Heading 2 sections found (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Expected 6 Heading 2 sections, found {num_heading2}")
            # Show what was found
            for h in heading2_list:
                print(f"  Found: level={h[0]} style={h[1]} text={h[2]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Slide titles match expected "Slide N: [title]" format (0.25 points)
    # Full points only if all 6 match; partial credit proportional
    try:
        heading2_texts = [text for (lvl, style, text) in headings if lvl == '2']
        matched = 0
        for expected in EXPECTED_SLIDE_TITLES:
            # Normalize whitespace for comparison
            expected_norm = ' '.join(expected.split())
            for actual in heading2_texts:
                actual_norm = ' '.join(actual.split())
                if actual_norm == expected_norm:
                    matched += 1
                    break
        if matched == 6:
            print(f"PASS: Component 3 — All 6 slide titles match expected (0.25 pts)")
            total_score += 0.25
        elif matched >= 4:
            partial = round(0.25 * matched / 6, 4)
            print(f"PARTIAL: Component 3 — {matched}/6 slide titles match expected ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Only {matched}/6 slide titles match. Found: {heading2_texts}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Body list items present (at least 18 total — 3 main bullets × 6 slides) (0.20 points)
    # The golden has 54 total list items; a passing threshold is >= 18
    try:
        if total_list_items >= 18:
            print(f"PASS: Component 4 — {total_list_items} list items present (>= 18 required) (0.20 pts)")
            total_score += 0.20
        elif total_list_items >= 6:
            partial = round(0.20 * total_list_items / 18, 4)
            print(f"PARTIAL: Component 4 — {total_list_items} list items found (>= 6, < 18) ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — Only {total_list_items} list items found (need >= 18)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Two-level hierarchy present (sub-bullets nested inside main bullets) (0.15 points)
    # The golden has 36 nested sub-bullet items; threshold >= 12 (2 sub-bullets × 6 slides)
    try:
        if nested_list_items >= 12:
            print(f"PASS: Component 5 — {nested_list_items} nested sub-bullet items (>= 12 required) (0.15 pts)")
            total_score += 0.15
        elif nested_list_items >= 1:
            partial = round(0.15 * nested_list_items / 12, 4)
            print(f"PARTIAL: Component 5 — {nested_list_items} nested items found (>= 1, < 12) ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 — No nested sub-bullet items found (need >= 12)")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical output path
if not os.path.exists(OUTPUT_FILE):
    print(f"File not found: {OUTPUT_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_FILE)

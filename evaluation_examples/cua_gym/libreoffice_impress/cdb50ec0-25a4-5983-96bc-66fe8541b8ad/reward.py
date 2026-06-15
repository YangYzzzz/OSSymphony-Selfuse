"""
Reward Script: Insert bulleted list text box on slide 3
Task ID: impress_tm_070
Domain: libreoffice_impress
Scoring:
  Component 1 (0.4): New text box on slide 3 with exactly 4 non-empty paragraphs
  Component 2 (0.3): Correct text content for all 4 items
  Component 3 (0.3): Square bullet character on all 4 items
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_tm_070'

# Expected bullet items
EXPECTED_ITEMS = ['Design Phase', 'Development Phase', 'Testing Phase', 'Launch Phase']

# Square bullet characters commonly used
SQUARE_BULLETS = {'\u25A0', '\u25AA', '\u25AB', '\u25A1', '\u25FC', '\u25FE', '\u25FB', '\u25FD'}


def find_new_textbox_paragraphs(pptx_path):
    """
    Find the new text box on slide 3 (not the title placeholder, not the
    existing 'Project Phases' textbox). Return list of (text, bullet_char) tuples
    for non-empty paragraphs.
    """
    ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
          'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}

    with zipfile.ZipFile(pptx_path, 'r') as zf:
        with zf.open('ppt/slides/slide3.xml') as f:
            root = ET.fromstring(f.read())

    # Collect all shapes
    shapes_data = []
    for sp in root.findall('.//p:sp', ns):
        cNvPr = sp.find('.//p:nvSpPr/p:cNvPr', ns)
        name = cNvPr.get('name') if cNvPr is not None else 'unknown'

        # Skip placeholders (title, subtitle, etc.)
        nvPr = sp.find('.//p:nvSpPr/p:nvPr', ns)
        ph = nvPr.find('p:ph', ns) if nvPr is not None else None
        is_placeholder = ph is not None

        txBody = sp.find('.//p:txBody', ns)
        if txBody is None:
            continue

        paras = []
        for para in txBody.findall('a:p', ns):
            text = ''.join(t.text or '' for t in para.findall('.//a:t', ns)).strip()
            pPr = para.find('a:pPr', ns)
            buChar_el = pPr.find('a:buChar', ns) if pPr is not None else None
            bullet_char = buChar_el.get('char') if buChar_el is not None else None
            if text:
                paras.append((text, bullet_char))

        shapes_data.append({
            'name': name,
            'is_placeholder': is_placeholder,
            'paras': paras,
            'full_text': ' '.join(t for t, _ in paras)
        })

    # The new textbox is the one that is NOT a placeholder AND does NOT contain
    # only 'Project Phases'. Look for a textbox with the expected items.
    for shape in shapes_data:
        if shape['is_placeholder']:
            continue
        # Skip the existing "Project Phases" title textbox
        if len(shape['paras']) == 1 and shape['paras'][0][0] == 'Project Phases':
            continue
        # This should be the new textbox with bulleted items
        if len(shape['paras']) >= 1:
            return shape['paras']

    return []


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        # Basic file validation - can we open it as a pptx?
        with zipfile.ZipFile(file_path, 'r') as zf:
            if 'ppt/slides/slide3.xml' not in zf.namelist():
                print("CRITICAL: slide3.xml not found in pptx")
                print("REWARD: 0.0")
                return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the new textbox paragraphs on slide 3
    try:
        paras = find_new_textbox_paragraphs(file_path)
    except Exception as e:
        print(f"ERROR: Failed to parse slide 3: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: New text box on slide 3 with exactly 4 non-empty paragraphs (0.4 points)
    try:
        if len(paras) == 4:
            print(f"PASS: Component 1 — New text box found with exactly 4 items (0.4 pts)")
            total_score += 0.4
        elif len(paras) > 0:
            # Partial credit: textbox exists but wrong number of items
            partial = 0.2
            print(f"PARTIAL: Component 1 — Text box found but has {len(paras)} items instead of 4 ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No new text box with bullet items found on slide 3")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Correct text content for all 4 items (0.3 points)
    try:
        if len(paras) >= 4:
            actual_texts = [t for t, _ in paras[:4]]
            matches = sum(1 for actual, expected in zip(actual_texts, EXPECTED_ITEMS)
                         if actual.strip().lower() == expected.strip().lower())
            if matches == 4:
                print(f"PASS: Component 2 — All 4 items have correct text (0.3 pts)")
                total_score += 0.3
            elif matches > 0:
                partial = round(0.3 * matches / 4, 2)
                print(f"PARTIAL: Component 2 — {matches}/4 items match ({partial} pts)")
                print(f"  Expected: {EXPECTED_ITEMS}")
                print(f"  Actual:   {actual_texts}")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — No items match expected text")
                print(f"  Expected: {EXPECTED_ITEMS}")
                print(f"  Actual:   {actual_texts}")
        else:
            print(f"FAIL: Component 2 — Not enough paragraphs to check ({len(paras)} found)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Square bullet character on all 4 items (0.3 points)
    try:
        if len(paras) >= 4:
            bullet_chars = [b for _, b in paras[:4]]
            square_count = sum(1 for b in bullet_chars if b is not None and b in SQUARE_BULLETS)
            if square_count == 4:
                print(f"PASS: Component 3 — All 4 items have square bullets (0.3 pts)")
                total_score += 0.3
            elif square_count > 0:
                partial = round(0.3 * square_count / 4, 2)
                print(f"PARTIAL: Component 3 — {square_count}/4 items have square bullets ({partial} pts)")
                print(f"  Bullet chars: {bullet_chars}")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — No square bullets found")
                print(f"  Bullet chars: {bullet_chars}")
        else:
            print(f"FAIL: Component 3 — Not enough paragraphs to check bullets")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

"""
Reward Script: Remove all bullet symbols from content textbox on slide 3 and increase indent level by 1
Task ID: osworld_impress_bullet_indent_remove_005
Domain: libreoffice_impress
Scoring:
  - Component 1: All 4 content items have bullet symbols removed (buNone=True) — 0.5 points
  - Component 2: All 4 content items have indent level increased to 1 — 0.5 points
  Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_impress_bullet_indent_remove_005'

# XML namespaces used in PPTX
NS_A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
NS_P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
NS = {
    'a': NS_A,
    'p': NS_P,
}


def get_slide3_content_paragraphs(pptx_path):
    """
    Parse slide3.xml from the PPTX and return a list of dicts describing
    each non-empty paragraph in the content placeholder (not the title).
    Each dict has:
      - 'text': stripped paragraph text
      - 'lvl': indent level as string (default '0')
      - 'buNone': True if <a:buNone/> is present (bullets removed)
      - 'buChar': bullet character string or None
    Returns None if unable to parse.
    """
    try:
        with zipfile.ZipFile(pptx_path, 'r') as zf:
            with zf.open('ppt/slides/slide3.xml') as f:
                root = ET.parse(f).getroot()

        paragraphs = []
        title_found = False

        for para in root.findall('.//a:p', NS):
            pPr = para.find('a:pPr', NS)
            text = ''.join(t.text or '' for t in para.findall('.//a:t', NS)).strip()

            if not text:
                continue

            # Skip the title paragraph (first non-empty text with pPr=None is the title)
            if not title_found and pPr is None:
                title_found = True
                continue

            if pPr is not None:
                lvl = pPr.get('lvl', '0')
                buNone = pPr.find('a:buNone', NS) is not None
                buChar_el = pPr.find('a:buChar', NS)
                buChar = buChar_el.get('char') if buChar_el is not None else None
            else:
                # No pPr means level 0 and default bullets
                lvl = '0'
                buNone = False
                buChar = None

            paragraphs.append({
                'text': text,
                'lvl': lvl,
                'buNone': buNone,
                'buChar': buChar,
            })

        return paragraphs

    except Exception as e:
        print(f"ERROR: Could not parse slide 3 paragraphs: {e}")
        return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Task: Remove all bullet symbols from the content textbox on slide 3,
          and increase the indent level of all items by one level.

    Initial state: 4 content items at level=0 with buChar='•'
    Golden state:  4 content items at level=1 with buNone=True
    """
    total_score = 0.0

    # Precondition gate: file must exist and be parseable
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    paragraphs = get_slide3_content_paragraphs(file_path)

    if paragraphs is None:
        print("CRITICAL: Could not parse slide 3 content")
        print("REWARD: 0.0")
        return 0.0

    # Gate: must have exactly 4 content items (precondition check)
    if len(paragraphs) != 4:
        print(f"CRITICAL: Expected 4 content paragraphs on slide 3, found {len(paragraphs)}")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found {len(paragraphs)} content paragraphs on slide 3")
    for p in paragraphs:
        print(f"  text={p['text'][:45]!r}: lvl={p['lvl']}, buNone={p['buNone']}, buChar={p['buChar']}")

    # Component 1: All 4 items have bullet symbols removed (buNone=True) (0.5 points)
    # Initial state: buChar='•', buNone=False → FAIL on initial
    # Golden state:  buNone=True               → PASS on golden
    try:
        items_no_bullet = sum(1 for p in paragraphs if p['buNone'])
        if items_no_bullet == 4:
            print(f"PASS: Component 1 — All 4 content items have bullet symbols removed (buNone=True) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — Expected all 4 items to have buNone=True, found {items_no_bullet}/4")
            for p in paragraphs:
                if not p['buNone']:
                    print(f"  STILL HAS BULLET: {p['text'][:50]!r}, buNone={p['buNone']}, buChar={p['buChar']}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 4 items have indent level increased to 1 (0.5 points)
    # Initial state: lvl='0' → FAIL on initial
    # Golden state:  lvl='1' → PASS on golden
    try:
        items_lvl1 = sum(1 for p in paragraphs if p['lvl'] == '1')
        if items_lvl1 == 4:
            print(f"PASS: Component 2 — All 4 content items have indent level=1 (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 — Expected all 4 items at level=1, found {items_lvl1}/4 at level=1")
            for p in paragraphs:
                if p['lvl'] != '1':
                    print(f"  WRONG LEVEL: {p['text'][:50]!r}, lvl={p['lvl']}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: run against canonical artifact path on VM
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

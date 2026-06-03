"""
Reward Script: Insert horizontal line between preamble and operative provisions
Task ID: writer_legal_056
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): A paragraph border exists separating WHEREAS section from NOW THEREFORE
  Component 2 (0.3): The border style is a solid single line
  Component 3 (0.2): The border color is black/dark
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_legal_056'
WML_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def find_border_between_whereas_and_now_therefore(doc):
    """
    Search for a horizontal line (paragraph border) between the last WHEREAS
    paragraph and the NOW, THEREFORE paragraph.

    Possible implementations:
    1. Bottom border on the last WHEREAS paragraph
    2. Top border on the NOW, THEREFORE paragraph
    3. A separate paragraph between them that has borders (top, bottom, or both)
    4. Bottom border on any paragraph between last WHEREAS and NOW THEREFORE
    """
    paragraphs = doc.paragraphs

    # Find the last WHEREAS paragraph and the NOW, THEREFORE paragraph
    last_whereas_idx = None
    now_therefore_idx = None

    for i, para in enumerate(paragraphs):
        text = para.text.strip().upper()
        if text.startswith('WHEREAS'):
            last_whereas_idx = i
        if 'NOW, THEREFORE' in text or 'NOW THEREFORE' in text:
            now_therefore_idx = i
            break  # take the first one

    print(f"DEBUG: last_whereas_idx={last_whereas_idx}, now_therefore_idx={now_therefore_idx}")

    if last_whereas_idx is None or now_therefore_idx is None:
        print("FAIL: Could not find WHEREAS or NOW, THEREFORE paragraphs")
        return None

    if now_therefore_idx <= last_whereas_idx:
        print("FAIL: NOW, THEREFORE appears before last WHEREAS")
        return None

    # Search for borders in the range [last_whereas_idx, now_therefore_idx]
    border_info = None

    # Strategy 1: Check bottom border on last WHEREAS paragraph
    border_info = _get_border(paragraphs[last_whereas_idx], 'bottom')
    if border_info:
        print(f"DEBUG: Found bottom border on last WHEREAS paragraph (idx {last_whereas_idx})")
        return border_info

    # Strategy 2: Check top border on NOW, THEREFORE paragraph
    border_info = _get_border(paragraphs[now_therefore_idx], 'top')
    if border_info:
        print(f"DEBUG: Found top border on NOW, THEREFORE paragraph (idx {now_therefore_idx})")
        return border_info

    # Strategy 3: Check any paragraph between them for any border
    for idx in range(last_whereas_idx + 1, now_therefore_idx):
        for side in ['bottom', 'top', 'between']:
            border_info = _get_border(paragraphs[idx], side)
            if border_info:
                print(f"DEBUG: Found {side} border on intermediate paragraph (idx {idx})")
                return border_info

    # Strategy 4: Check bottom border on paragraphs between WHEREAS and NOW THEREFORE
    for idx in range(last_whereas_idx, now_therefore_idx):
        for side in ['bottom', 'top']:
            border_info = _get_border(paragraphs[idx], side)
            if border_info:
                print(f"DEBUG: Found {side} border on paragraph idx {idx}")
                return border_info

    print("FAIL: No border found between WHEREAS and NOW, THEREFORE")
    return None


def _get_border(para, side):
    """Extract border info for a given side (top, bottom, between) from a paragraph."""
    pPr = para._element.find(qn('w:pPr'))
    if pPr is None:
        return None
    pBdr = pPr.find(qn('w:pBdr'))
    if pBdr is None:
        return None
    border_elem = pBdr.find(qn('w:' + side))
    if border_elem is None:
        return None
    val = border_elem.get('{%s}val' % WML_NS)
    sz = border_elem.get('{%s}sz' % WML_NS)
    color = border_elem.get('{%s}color' % WML_NS)

    # 'none' val means no border
    if val == 'none':
        return None

    return {
        'side': side,
        'val': val,
        'sz': sz,
        'color': color,
    }


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the border between WHEREAS and NOW, THEREFORE
    border_info = find_border_between_whereas_and_now_therefore(doc)

    # Component 1: A paragraph border exists separating the sections (0.5 points)
    try:
        if border_info is not None:
            print(f"PASS: Component 1 — Border found: {border_info} (0.5 pts)")
            total_score += 0.5
        else:
            print("FAIL: Component 1 — No horizontal line/border found between WHEREAS and NOW, THEREFORE")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The border style is a solid single line (0.3 points)
    try:
        if border_info is not None:
            val = border_info.get('val', '')
            # Accept 'single', 'thick', 'thin', or other solid line styles
            solid_styles = {'single', 'thick', 'thin', 'thinThickSmallGap',
                            'thickThinSmallGap', 'threeDEmboss', 'threeDEngrave'}
            if val in solid_styles:
                print(f"PASS: Component 2 — Border style is solid: '{val}' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Border style '{val}' is not a solid line type")
        else:
            print("FAIL: Component 2 — No border to check style on")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The border color is black/dark (0.2 points)
    try:
        if border_info is not None:
            color = border_info.get('color', '')
            # Accept black or very dark colors, also 'auto' which defaults to black
            dark_colors = {'000000', 'auto', '000001', '111111', '222222', '333333'}
            if color and (color.lower() in dark_colors or color.lower().startswith('0')):
                print(f"PASS: Component 3 — Border color is dark: '{color}' (0.2 pts)")
                total_score += 0.2
            elif not color:
                # No color specified typically means auto/black
                print(f"PASS: Component 3 — Border color not specified (defaults to black) (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — Border color '{color}' is not black/dark")
        else:
            print("FAIL: Component 3 — No border to check color on")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

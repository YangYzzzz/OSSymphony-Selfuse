"""
Reward Script: Create bulleted list with right-pointing arrow bullets
Task ID: writer_lec_015
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): All 7 feature paragraphs are in a numbered/bulleted list
  Component 2 (0.4): Bullet character is a right-pointing arrow (U+2192 or U+25BA)
  Component 3 (0.3): All 7 feature paragraphs are indented
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_015'

# Known feature paragraph texts (first 20 chars) to identify them
FEATURE_STARTS = [
    'Supports over 200',
    'Voice control integ',
    'Advanced energy moni',
    'Military-grade AES-2',
    'Customizable automat',
    'Built-in 7-inch touc',
    'Remote access throug',
]
NUM_FEATURES = 7

# Right-pointing arrow characters
ARROW_CHARS = {
    '\u2192',  # U+2192 RIGHTWARDS ARROW
    '\u25ba',  # U+25BA BLACK RIGHT-POINTING POINTER
    '\u25b6',  # U+25B6 BLACK RIGHT-POINTING TRIANGLE
    '\u279c',  # U+279C HEAVY ROUND-TIPPED RIGHTWARDS ARROW
    '\u27a1',  # U+27A1 BLACK RIGHTWARDS ARROW
    '\u2794',  # U+2794 HEAVY WIDE-HEADED RIGHTWARDS ARROW
}


def get_feature_paragraphs(doc):
    """Find the 7 feature paragraphs by position (indices 3-9 after heading)."""
    feature_paras = []
    for i, p in enumerate(doc.paragraphs):
        text = p.text.strip()
        for start in FEATURE_STARTS:
            if text.startswith(start):
                feature_paras.append((i, p))
                break
    return feature_paras


def get_numId(para):
    """Extract numId from paragraph XML."""
    pPr = para._element.find(qn('w:pPr'))
    if pPr is None:
        return None
    numPr = pPr.find(qn('w:numPr'))
    if numPr is None:
        return None
    numId_elem = numPr.find(qn('w:numId'))
    if numId_elem is None:
        return None
    val = numId_elem.get(qn('w:val'))
    return val


def get_bullet_char_for_numId(doc, numId_val):
    """Look up the bullet character (lvlText) for a given numId."""
    try:
        numbering = doc.part.numbering_part._element
    except Exception:
        return None

    # Find the abstractNumId for this numId
    abstractNumId_val = None
    for num in numbering.findall(qn('w:num')):
        if num.get(qn('w:numId')) == numId_val:
            absRef = num.find(qn('w:abstractNumId'))
            if absRef is not None:
                abstractNumId_val = absRef.get(qn('w:val'))
            break

    if abstractNumId_val is None:
        return None

    # Find the abstractNum and get lvlText for ilvl=0
    for absNum in numbering.findall(qn('w:abstractNum')):
        if absNum.get(qn('w:abstractNumId')) == abstractNumId_val:
            for lvl in absNum.findall(qn('w:lvl')):
                if lvl.get(qn('w:ilvl')) == '0':
                    numFmt = lvl.find(qn('w:numFmt'))
                    lvlText = lvl.find(qn('w:lvlText'))
                    fmt = numFmt.get(qn('w:val')) if numFmt is not None else None
                    txt = lvlText.get(qn('w:val')) if lvlText is not None else None
                    return (fmt, txt)
    return None


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

    feature_paras = get_feature_paragraphs(doc)
    if len(feature_paras) < NUM_FEATURES:
        print(f"WARNING: Found only {len(feature_paras)} feature paragraphs, expected {NUM_FEATURES}")

    # Component 1: All 7 feature paragraphs are in a list (have numId) (0.3 points)
    try:
        listed_count = 0
        for idx, para in feature_paras:
            nid = get_numId(para)
            if nid is not None and nid != '0':
                listed_count += 1
            else:
                print(f"  FAIL: Para {idx} not in a list (numId={nid})")

        if listed_count == NUM_FEATURES:
            print(f"PASS: Component 1 -- All {NUM_FEATURES} features are in a list (0.3 pts)")
            total_score += 0.3
        elif listed_count > 0:
            partial = round(0.3 * listed_count / NUM_FEATURES, 2)
            print(f"PARTIAL: Component 1 -- {listed_count}/{NUM_FEATURES} features in a list ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 -- No feature paragraphs are in a list")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Bullet character is a right-pointing arrow (0.4 points)
    try:
        arrow_count = 0
        for idx, para in feature_paras:
            nid = get_numId(para)
            if nid is None or nid == '0':
                continue
            bullet_info = get_bullet_char_for_numId(doc, nid)
            if bullet_info is None:
                print(f"  FAIL: Para {idx} -- could not resolve bullet definition")
                continue
            fmt, txt = bullet_info
            if fmt != 'bullet':
                print(f"  FAIL: Para {idx} -- numFmt is '{fmt}', not 'bullet'")
                continue
            if txt and any(c in ARROW_CHARS for c in txt):
                arrow_count += 1
            else:
                # Show hex codes for debugging
                hex_codes = ' '.join(f'U+{ord(c):04X}' for c in (txt or ''))
                print(f"  FAIL: Para {idx} -- bullet char is '{txt}' ({hex_codes}), not an arrow")

        if arrow_count == NUM_FEATURES:
            print(f"PASS: Component 2 -- All {NUM_FEATURES} features use arrow bullet (0.4 pts)")
            total_score += 0.4
        elif arrow_count > 0:
            partial = round(0.4 * arrow_count / NUM_FEATURES, 2)
            print(f"PARTIAL: Component 2 -- {arrow_count}/{NUM_FEATURES} features use arrow bullet ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- No feature paragraphs use arrow bullet")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: All 7 feature paragraphs are indented (0.3 points)
    try:
        indented_count = 0
        for idx, para in feature_paras:
            left_indent = para.paragraph_format.left_indent
            if left_indent is not None and left_indent > 0:
                indented_count += 1
            else:
                print(f"  FAIL: Para {idx} not indented (left_indent={left_indent})")

        if indented_count == NUM_FEATURES:
            print(f"PASS: Component 3 -- All {NUM_FEATURES} features are indented (0.3 pts)")
            total_score += 0.3
        elif indented_count > 0:
            partial = round(0.3 * indented_count / NUM_FEATURES, 2)
            print(f"PARTIAL: Component 3 -- {indented_count}/{NUM_FEATURES} features indented ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 -- No feature paragraphs are indented")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
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

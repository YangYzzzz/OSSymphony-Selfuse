"""
Reward Script: Create bulleted list with custom triangle bullet character
Task ID: writer_rd_009
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): Five feature paragraphs have bullet list numbering
  Component 2 (0.4): Bullet character is right-pointing triangle U+25B6
  Component 3 (0.2): All five items share a consistent numbering definition
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_rd_009'

# The triangle character we expect (U+25B6)
TRIANGLE_CHAR = '\u25b6'


def persist_app_state(domain):
    """Save any unsaved changes in LibreOffice Writer."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print(f"PERSIST: ctrl+s sent for {domain}")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def get_abstract_num_for_numid(numbering_xml, num_id_val):
    """Given a numId value, return the corresponding abstractNum element."""
    for num in numbering_xml.findall(qn('w:num')):
        if num.get(qn('w:numId')) == num_id_val:
            abstract_ref = num.find(qn('w:abstractNumId'))
            if abstract_ref is not None:
                abs_id = abstract_ref.get(qn('w:val'))
                # Find the abstractNum with this ID
                for abstract_num in numbering_xml.findall(qn('w:abstractNum')):
                    if abstract_num.get(qn('w:abstractNumId')) == abs_id:
                        return abstract_num
    return None


def get_bullet_char(abstract_num):
    """Extract the bullet character from level 0 of an abstractNum."""
    if abstract_num is None:
        return None
    for lvl in abstract_num.findall(qn('w:lvl')):
        if lvl.get(qn('w:ilvl')) == '0':
            lvl_text = lvl.find(qn('w:lvlText'))
            num_fmt = lvl.find(qn('w:numFmt'))
            if lvl_text is not None and num_fmt is not None:
                fmt_val = num_fmt.get(qn('w:val'))
                if fmt_val == 'bullet':
                    return lvl_text.get(qn('w:val'))
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

    # Identify the five feature paragraphs (paragraphs after "Key Features" heading)
    # The document should have: [0] heading, [1]-[5] feature items
    paragraphs = doc.paragraphs
    if len(paragraphs) < 6:
        print(f"FAIL: Expected at least 6 paragraphs, found {len(paragraphs)}")
        print("REWARD: 0.0")
        return 0.0

    feature_paras = paragraphs[1:6]

    # Component 1: All 5 feature paragraphs have bullet list numbering (0.4 points)
    try:
        bulleted_count = 0
        num_ids = []
        for i, para in enumerate(feature_paras):
            pPr = para._element.find(qn('w:pPr'))
            if pPr is not None:
                numPr = pPr.find(qn('w:numPr'))
                if numPr is not None:
                    numId_elem = numPr.find(qn('w:numId'))
                    if numId_elem is not None:
                        num_id_val = numId_elem.get(qn('w:val'))
                        if num_id_val and num_id_val != '0':
                            bulleted_count += 1
                            num_ids.append(num_id_val)
                            continue
            num_ids.append(None)

        if bulleted_count == 5:
            print(f"PASS: Component 1 — All 5 feature paragraphs have list numbering (0.4 pts)")
            total_score += 0.4
        elif bulleted_count > 0:
            partial = round(0.4 * bulleted_count / 5, 2)
            print(f"PARTIAL: Component 1 — {bulleted_count}/5 paragraphs have list numbering ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No feature paragraphs have list numbering")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Bullet character is the right-pointing triangle U+25B6 (0.4 points)
    try:
        # Get numbering part to inspect bullet definitions
        numbering_part = doc.part.numbering_part
        numbering_xml = numbering_part._element

        # Check the bullet character for each feature paragraph's numId
        triangle_count = 0
        for i, num_id_val in enumerate(num_ids):
            if num_id_val is None:
                continue
            abstract_num = get_abstract_num_for_numid(numbering_xml, num_id_val)
            bullet_char = get_bullet_char(abstract_num)
            if bullet_char == TRIANGLE_CHAR:
                triangle_count += 1
                print(f"  Para [{i+1}]: bullet char = {repr(bullet_char)} — triangle match")
            else:
                print(f"  Para [{i+1}]: bullet char = {repr(bullet_char)} — NOT triangle")

        if triangle_count == 5:
            print(f"PASS: Component 2 — All 5 items use triangle bullet U+25B6 (0.4 pts)")
            total_score += 0.4
        elif triangle_count > 0:
            partial = round(0.4 * triangle_count / 5, 2)
            print(f"PARTIAL: Component 2 — {triangle_count}/5 items use triangle bullet ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No items use the triangle bullet character")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 5 items share a consistent numbering definition (0.2 points)
    try:
        valid_ids = [nid for nid in num_ids if nid is not None]
        if len(valid_ids) == 5 and len(set(valid_ids)) == 1:
            print(f"PASS: Component 3 — All 5 items share numId={valid_ids[0]} (0.2 pts)")
            total_score += 0.2
        elif len(valid_ids) > 0:
            unique_ids = set(valid_ids)
            if len(unique_ids) == 1:
                print(f"PARTIAL: Component 3 — {len(valid_ids)}/5 items share numId={valid_ids[0]}")
                total_score += 0.1
            else:
                print(f"FAIL: Component 3 — Items use different numIds: {unique_ids}")
        else:
            print(f"FAIL: Component 3 — No items have numbering")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

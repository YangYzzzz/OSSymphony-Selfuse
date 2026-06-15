"""
Reward Script: Insert chapter numbering fields for Heading 1 paragraphs
Task ID: writer_tm_061
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): All 5 Heading 1 paragraphs have numbering properties (numPr)
  Component 2 (0.3): Numbering definition has "Chapter " prefix in lvlText
  Component 3 (0.2): Numbering format is decimal (Arabic numbers)
  Component 4 (0.2): Numbering starts at 1 and headings text content is preserved
"""

import os
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_tm_061'

WNS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': WNS}


def get_attr(elem, attr_name):
    """Get w:-namespaced attribute value from element."""
    return elem.get(f'{{{WNS}}}{attr_name}')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all Heading 1 paragraphs
    heading1_paras = [p for p in doc.paragraphs if p.style.name == 'Heading 1']
    expected_headings = ['Introduction', 'Background', 'Methodology', 'Results', 'Conclusion']

    if len(heading1_paras) != 5:
        print(f"PRECONDITION FAIL: Expected 5 Heading 1 paragraphs, found {len(heading1_paras)}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: All 5 Heading 1 paragraphs have numbering properties (0.3 points)
    try:
        headings_with_numpr = 0
        num_ids = set()
        for p in heading1_paras:
            pPr = p._element.find('w:pPr', NS)
            if pPr is not None:
                num_pr = pPr.find('w:numPr', NS)
                if num_pr is not None:
                    ilvl = num_pr.find('w:ilvl', NS)
                    num_id = num_pr.find('w:numId', NS)
                    if ilvl is not None and num_id is not None:
                        headings_with_numpr += 1
                        num_ids.add(get_attr(num_id, 'val'))

        if headings_with_numpr == 5:
            print(f"PASS: Component 1 — All 5 Heading 1 paragraphs have numPr (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Only {headings_with_numpr}/5 Heading 1 paragraphs have numPr")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Numbering definition has "Chapter " prefix in lvlText (0.3 points)
    try:
        chapter_numbering_found = False
        chapter_abstract_id = None

        # Get numbering part
        numbering_part = doc.part.numbering_part
        root = numbering_part._element

        # Resolve numId -> abstractNumId -> lvlText
        # First find which numId is used by headings
        target_num_id = num_ids.pop() if num_ids else None
        target_abstract_id = None

        if target_num_id is not None:
            for num_elem in root.findall('.//w:num', NS):
                if get_attr(num_elem, 'numId') == target_num_id:
                    abstract_ref = num_elem.find('w:abstractNumId', NS)
                    if abstract_ref is not None:
                        target_abstract_id = get_attr(abstract_ref, 'val')
                    break

        if target_abstract_id is not None:
            for abstract in root.findall('.//w:abstractNum', NS):
                if get_attr(abstract, 'abstractNumId') == target_abstract_id:
                    for lvl in abstract.findall('w:lvl', NS):
                        if get_attr(lvl, 'ilvl') == '0':
                            lvl_text_elem = lvl.find('w:lvlText', NS)
                            if lvl_text_elem is not None:
                                lvl_text_val = get_attr(lvl_text_elem, 'val') or ''
                                # Check for "Chapter" prefix with number placeholder
                                if 'Chapter' in lvl_text_val and '%1' in lvl_text_val:
                                    chapter_numbering_found = True
                                    print(f"PASS: Component 2 — lvlText='{lvl_text_val}' contains 'Chapter' prefix (0.3 pts)")
                                    total_score += 0.3
                                else:
                                    print(f"FAIL: Component 2 — lvlText='{lvl_text_val}' does not contain 'Chapter' prefix with '%1'")
                            else:
                                print(f"FAIL: Component 2 — No lvlText found in abstractNum {target_abstract_id}")
                    break

        if not chapter_numbering_found and target_abstract_id is None:
            print(f"FAIL: Component 2 — Could not resolve numbering definition (numId={target_num_id})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Numbering format is decimal / Arabic (0.2 points)
    try:
        decimal_format_found = False
        if target_abstract_id is not None:
            for abstract in root.findall('.//w:abstractNum', NS):
                if get_attr(abstract, 'abstractNumId') == target_abstract_id:
                    for lvl in abstract.findall('w:lvl', NS):
                        if get_attr(lvl, 'ilvl') == '0':
                            num_fmt = lvl.find('w:numFmt', NS)
                            if num_fmt is not None:
                                fmt_val = get_attr(num_fmt, 'val')
                                if fmt_val == 'decimal':
                                    decimal_format_found = True
                                    print(f"PASS: Component 3 — numFmt is 'decimal' (Arabic numbers) (0.2 pts)")
                                    total_score += 0.2
                                else:
                                    print(f"FAIL: Component 3 — numFmt is '{fmt_val}', expected 'decimal'")
                            else:
                                print(f"FAIL: Component 3 — No numFmt element found")
                    break

        if not decimal_format_found and target_abstract_id is None:
            print(f"FAIL: Component 3 — Could not resolve numbering definition")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Numbering starts at 1 AND heading text content is preserved (0.2 points)
    # Both sub-conditions must pass. Text preservation alone is a precondition, not scored.
    try:
        start_at_1 = False
        text_preserved = False

        # Check start value — only meaningful if numbering definition was resolved
        if target_abstract_id is not None:
            for abstract in root.findall('.//w:abstractNum', NS):
                if get_attr(abstract, 'abstractNumId') == target_abstract_id:
                    for lvl in abstract.findall('w:lvl', NS):
                        if get_attr(lvl, 'ilvl') == '0':
                            start_elem = lvl.find('w:start', NS)
                            if start_elem is not None:
                                start_val = get_attr(start_elem, 'val')
                                if start_val == '1':
                                    start_at_1 = True
                                else:
                                    print(f"FAIL: Component 4a — start val is '{start_val}', expected '1'")
                            else:
                                print(f"FAIL: Component 4a — No start element found")
                    break

        # Check that heading text content is preserved (not overwritten)
        actual_texts = [p.text.strip() for p in heading1_paras]
        preserved_count = 0
        for expected, actual in zip(expected_headings, actual_texts):
            if expected in actual:
                preserved_count += 1
        text_preserved = (preserved_count == 5)

        # Only award points if BOTH numbering start is correct AND text is preserved
        # This ensures the component scores 0 on initial_env (where numbering doesn't exist)
        if start_at_1 and text_preserved:
            print(f"PASS: Component 4 — Numbering starts at 1, all heading texts preserved (0.2 pts)")
            total_score += 0.2
        elif not start_at_1:
            print(f"FAIL: Component 4 — Numbering start value not found or not 1 (no numbering definition)")
        else:
            print(f"FAIL: Component 4 — start_at_1={start_at_1}, text_preserved={text_preserved} ({preserved_count}/5)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook: save any unsaved LibreOffice edits before verification
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    persist_app_state()
    verify_task(file_path)

"""
Reward Script: Configure outline numbering for Heading 1/2/3
Task ID: writer_bs_069
Domain: libreoffice_writer
Scoring:
  Component 1 (0.25): Heading 1 style linked to a numbering definition
  Component 2 (0.25): Heading 1 numbering uses "Chapter" prefix with Arabic number
  Component 3 (0.25): Heading 2 numbering uses multi-level format x.y
  Component 4 (0.25): Heading 3 numbering uses multi-level format x.y.z
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_bs_069'


def persist_app_state(domain: str):
    """Save any unsaved GUI edits before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify outline numbering configuration with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        from lxml import etree
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    wns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

    # Helper: find the numId and ilvl linked to a heading style
    def get_style_numPr(style_name):
        """Return (numId, ilvl) for a style, or (None, None) if not linked."""
        for style in doc.styles:
            if style.name == style_name:
                pPr = style.element.find('.//w:pPr', ns)
                if pPr is not None:
                    numPr = pPr.find('w:numPr', ns)
                    if numPr is not None:
                        numId_elem = numPr.find('w:numId', ns)
                        ilvl_elem = numPr.find('w:ilvl', ns)
                        numId = numId_elem.get(f'{{{wns}}}val') if numId_elem is not None else None
                        ilvl = ilvl_elem.get(f'{{{wns}}}val') if ilvl_elem is not None else None
                        return numId, ilvl
        return None, None

    # Helper: resolve numId -> abstractNumId -> abstractNum element
    def get_abstract_num(numId_val):
        """Return the abstractNum element for a given numId."""
        try:
            numbering_part = doc.part.numbering_part
            numbering_elem = numbering_part.element
        except Exception:
            return None

        # Find num element with matching numId
        for num_elem in numbering_elem.findall('w:num', ns):
            if num_elem.get(f'{{{wns}}}numId') == str(numId_val):
                abstract_ref = num_elem.find('w:abstractNumId', ns)
                if abstract_ref is not None:
                    abstract_id = abstract_ref.get(f'{{{wns}}}val')
                    # Find corresponding abstractNum
                    for abs_num in numbering_elem.findall('w:abstractNum', ns):
                        if abs_num.get(f'{{{wns}}}abstractNumId') == abstract_id:
                            return abs_num
        return None

    # Helper: get lvl element for a given ilvl from abstractNum
    def get_lvl(abstract_num, ilvl_val):
        """Return the lvl element for a given indent level."""
        if abstract_num is None:
            return None
        for lvl in abstract_num.findall('w:lvl', ns):
            if lvl.get(f'{{{wns}}}ilvl') == str(ilvl_val):
                return lvl
        return None

    # Helper: get lvlText value from a lvl element
    def get_lvl_text(lvl_elem):
        if lvl_elem is None:
            return None
        lt = lvl_elem.find('w:lvlText', ns)
        if lt is not None:
            return lt.get(f'{{{wns}}}val')
        return None

    # Helper: get numFmt value from a lvl element
    def get_num_fmt(lvl_elem):
        if lvl_elem is None:
            return None
        nf = lvl_elem.find('w:numFmt', ns)
        if nf is not None:
            return nf.get(f'{{{wns}}}val')
        return None

    # =========================================================================
    # Component 1: Heading 1 style is linked to a numbering definition (0.25 pts)
    # This FAILS on initial (no numPr) and PASSES on golden (numPr present)
    # =========================================================================
    try:
        h1_numId, h1_ilvl = get_style_numPr('Heading 1')
        h2_numId, h2_ilvl = get_style_numPr('Heading 2')
        h3_numId, h3_ilvl = get_style_numPr('Heading 3')

        if h1_numId is not None and h2_numId is not None and h3_numId is not None:
            # All three heading styles must reference the SAME numId (multilevel)
            if h1_numId == h2_numId == h3_numId:
                print(f"PASS: Component 1 -- Heading 1/2/3 all linked to numId={h1_numId} (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 -- Headings linked to different numIds: H1={h1_numId}, H2={h2_numId}, H3={h3_numId}")
        else:
            print(f"FAIL: Component 1 -- Not all heading styles have numPr. H1={h1_numId}, H2={h2_numId}, H3={h3_numId}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # =========================================================================
    # Component 2: Heading 1 uses "Chapter" prefix with Arabic number (0.25 pts)
    # lvlText should contain "Chapter" and "%1", numFmt should be "decimal"
    # =========================================================================
    try:
        if h1_numId is not None:
            abstract_num = get_abstract_num(h1_numId)
            lvl0 = get_lvl(abstract_num, 0)
            lvl_text = get_lvl_text(lvl0)
            num_fmt = get_num_fmt(lvl0)

            chapter_ok = (lvl_text is not None and
                          'chapter' in lvl_text.lower() and
                          '%1' in lvl_text)
            fmt_ok = (num_fmt == 'decimal')

            if chapter_ok and fmt_ok:
                print(f"PASS: Component 2 -- Heading 1 lvlText='{lvl_text}', numFmt='{num_fmt}' (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 -- Heading 1 lvlText='{lvl_text}' (need 'Chapter %1'), numFmt='{num_fmt}' (need 'decimal')")
        else:
            print(f"FAIL: Component 2 -- Heading 1 has no numbering")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # =========================================================================
    # Component 3: Heading 2 uses multi-level format x.y (0.25 pts)
    # lvlText should be "%1.%2", numFmt should be "decimal"
    # =========================================================================
    try:
        if h1_numId is not None:
            abstract_num = get_abstract_num(h1_numId)
            lvl1 = get_lvl(abstract_num, 1)
            lvl_text = get_lvl_text(lvl1)
            num_fmt = get_num_fmt(lvl1)

            # Accept patterns like "%1.%2" (with or without trailing period)
            text_ok = (lvl_text is not None and '%1' in lvl_text and '%2' in lvl_text)
            fmt_ok = (num_fmt == 'decimal')

            if text_ok and fmt_ok:
                print(f"PASS: Component 3 -- Heading 2 lvlText='{lvl_text}', numFmt='{num_fmt}' (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 -- Heading 2 lvlText='{lvl_text}' (need '%1.%2'), numFmt='{num_fmt}' (need 'decimal')")
        else:
            print(f"FAIL: Component 3 -- Heading numbering not found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # =========================================================================
    # Component 4: Heading 3 uses multi-level format x.y.z (0.25 pts)
    # lvlText should be "%1.%2.%3", numFmt should be "decimal"
    # =========================================================================
    try:
        if h1_numId is not None:
            abstract_num = get_abstract_num(h1_numId)
            lvl2 = get_lvl(abstract_num, 2)
            lvl_text = get_lvl_text(lvl2)
            num_fmt = get_num_fmt(lvl2)

            text_ok = (lvl_text is not None and '%1' in lvl_text and '%2' in lvl_text and '%3' in lvl_text)
            fmt_ok = (num_fmt == 'decimal')

            if text_ok and fmt_ok:
                print(f"PASS: Component 4 -- Heading 3 lvlText='{lvl_text}', numFmt='{num_fmt}' (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 -- Heading 3 lvlText='{lvl_text}' (need '%1.%2.%3'), numFmt='{num_fmt}' (need 'decimal')")
        else:
            print(f"FAIL: Component 4 -- Heading numbering not found")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

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

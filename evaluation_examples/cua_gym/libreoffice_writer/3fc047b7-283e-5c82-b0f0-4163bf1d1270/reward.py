"""
Reward Script: Change bullet character from default round bullet to checkmark
Task ID: writer_lec_002
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): A checkmark bullet character exists in the document numbering definitions
  Component 2 (0.3): All 8 grocery items still present as bulleted list paragraphs
  Component 3 (0.3): All 8 bullet paragraphs reference a numbering definition using checkmark
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_002'

# Known checkmark-like Unicode codepoints that an agent might use
CHECKMARK_CODEPOINTS = {
    0x2713,  # CHECK MARK
    0x2714,  # HEAVY CHECK MARK
    0x2611,  # BALLOT BOX WITH CHECK
    0x2705,  # WHITE HEAVY CHECK MARK (emoji)
    0x221A,  # SQRT (sometimes used as check)
    0x2717,  # BALLOT X (not really, but close family)
    0x2718,  # HEAVY BALLOT X
    0x10003, # old unicode check
}

# The default round bullet in Symbol font
DEFAULT_BULLET_CODEPOINT = 0xF0B7


def is_checkmark_char(char):
    """Check if a character is a checkmark or checkmark-like symbol."""
    cp = ord(char)
    return cp in CHECKMARK_CODEPOINTS


def get_bullet_char_for_numid(doc, target_numid):
    """
    Given a numId, resolve through numbering.xml to find the level-0 bullet character.
    Returns (lvlText_char, font_name) or (None, None) if not found.
    """
    try:
        from docx.oxml.ns import qn
        import lxml.etree as ET

        numbering_part = doc.part.numbering_part
        if numbering_part is None:
            return None, None

        root = ET.fromstring(numbering_part.element.xml.encode())
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

        # Find the num element with target numId
        abstract_num_id = None
        for num_el in root.findall('.//w:num', ns):
            nid = num_el.get(qn('w:numId'))
            if nid == str(target_numid):
                abs_ref = num_el.find('w:abstractNumId', ns)
                if abs_ref is not None:
                    abstract_num_id = abs_ref.get(qn('w:val'))
                # Check for lvlOverride too
                for lvl_override in num_el.findall('w:lvlOverride', ns):
                    ilvl = lvl_override.get(qn('w:ilvl'))
                    if ilvl == '0':
                        lvl = lvl_override.find('w:lvl', ns)
                        if lvl is not None:
                            lvlText_el = lvl.find('w:lvlText', ns)
                            if lvlText_el is not None:
                                return lvlText_el.get(qn('w:val')), None
                break

        if abstract_num_id is None:
            return None, None

        # Find the abstractNum
        for abs_num in root.findall('.//w:abstractNum', ns):
            aid = abs_num.get(qn('w:abstractNumId'))
            if aid == abstract_num_id:
                for lvl in abs_num.findall('w:lvl', ns):
                    ilvl = lvl.get(qn('w:ilvl'))
                    if ilvl == '0':
                        numFmt_el = lvl.find('w:numFmt', ns)
                        lvlText_el = lvl.find('w:lvlText', ns)
                        numFmt = numFmt_el.get(qn('w:val')) if numFmt_el is not None else None
                        lvlText = lvlText_el.get(qn('w:val')) if lvlText_el is not None else None
                        rPr = lvl.find('w:rPr', ns)
                        font_name = None
                        if rPr is not None:
                            rFonts = rPr.find('w:rFonts', ns)
                            if rFonts is not None:
                                font_name = rFonts.get(qn('w:ascii'))
                        return lvlText, font_name
        return None, None
    except Exception as e:
        print(f"ERROR: get_bullet_char_for_numid: {e}")
        return None, None


def get_all_bullet_definitions(doc):
    """
    Scan all abstractNum definitions and return list of (abstractNumId, lvlText, font)
    for level-0 bullet-type entries.
    """
    results = []
    try:
        from docx.oxml.ns import qn
        import lxml.etree as ET

        numbering_part = doc.part.numbering_part
        if numbering_part is None:
            return results

        root = ET.fromstring(numbering_part.element.xml.encode())
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

        for abs_num in root.findall('.//w:abstractNum', ns):
            aid = abs_num.get(qn('w:abstractNumId'))
            for lvl in abs_num.findall('w:lvl', ns):
                ilvl = lvl.get(qn('w:ilvl'))
                if ilvl != '0':
                    continue
                numFmt_el = lvl.find('w:numFmt', ns)
                lvlText_el = lvl.find('w:lvlText', ns)
                numFmt = numFmt_el.get(qn('w:val')) if numFmt_el is not None else None
                lvlText = lvlText_el.get(qn('w:val')) if lvlText_el is not None else None
                if numFmt == 'bullet' and lvlText:
                    rPr = lvl.find('w:rPr', ns)
                    font_name = None
                    if rPr is not None:
                        rFonts = rPr.find('w:rFonts', ns)
                        if rFonts is not None:
                            font_name = rFonts.get(qn('w:ascii'))
                    results.append((aid, lvlText, font_name))
    except Exception as e:
        print(f"ERROR: get_all_bullet_definitions: {e}")
    return results


def get_paragraph_numid(para):
    """Get the numId for a paragraph from its XML, or None."""
    from docx.oxml.ns import qn
    pPr = para._element.find(qn('w:pPr'))
    if pPr is not None:
        numPr = pPr.find(qn('w:numPr'))
        if numPr is not None:
            ni = numPr.find(qn('w:numId'))
            if ni is not None:
                val = ni.get(qn('w:val'))
                if val is not None:
                    return int(val)
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    from docx import Document

    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Expected grocery items (substrings to match)
    expected_items = [
        "Whole milk",
        "Organic brown eggs",
        "Sourdough bread",
        "salmon fillet",
        "Baby spinach",
        "Greek yogurt",
        "olive oil",
        "Honeycrisp apples",
    ]

    # Identify bullet paragraphs (style contains 'List Bullet' or 'List' with bullet)
    bullet_paras = []
    for para in doc.paragraphs:
        style_name = para.style.name if para.style else ""
        if "List Bullet" in style_name or "List" in style_name:
            if para.text.strip():
                bullet_paras.append(para)

    # Component 1: A checkmark bullet character exists in the document numbering (0.4 points)
    # This checks that the bullet definition has been changed to a checkmark.
    # On initial_env, all bullets are U+F0B7 (Symbol) — no checkmark exists → FAIL
    # On golden_env, abstractNumId=9 has U+2713 checkmark → PASS
    try:
        all_bullet_defs = get_all_bullet_definitions(doc)
        checkmark_found = False
        checkmark_abstract_ids = set()
        for aid, lvl_text, font in all_bullet_defs:
            for char in lvl_text:
                if is_checkmark_char(char):
                    checkmark_found = True
                    checkmark_abstract_ids.add(aid)
                    break

        if checkmark_found:
            print(f"PASS: Component 1 — Checkmark bullet definition found in abstractNumId(s): {checkmark_abstract_ids} (0.4 pts)")
            total_score += 0.4
        else:
            chars_found = [(aid, ' '.join('U+%04X' % ord(c) for c in lt), f) for aid, lt, f in all_bullet_defs]
            print(f"FAIL: Component 1 — No checkmark bullet definition found. Bullet defs: {chars_found}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 8 grocery items still present as bullet-style paragraphs (0.3 points)
    # This verifies content preservation AND that items are still in a bulleted list format.
    # On initial_env, this could pass if items exist — but we gate it with Component 1.
    # Actually we need this to fail on initial... The items ARE present on initial too.
    # So we make this a compound check: items present AND using checkmark bullet.
    # We check that at least 6 of 8 items are in bullet paras that reference a checkmark numId.
    try:
        # Build a map: numId -> whether it uses checkmark
        numid_is_checkmark = {}
        for para in bullet_paras:
            nid = get_paragraph_numid(para)
            if nid is not None and nid not in numid_is_checkmark:
                lvl_text, font = get_bullet_char_for_numid(doc, nid)
                if lvl_text:
                    has_check = any(is_checkmark_char(c) for c in lvl_text)
                    numid_is_checkmark[nid] = has_check
                else:
                    numid_is_checkmark[nid] = False

        # Also check paragraphs that inherit bullet from style (no explicit numPr)
        # These use the style's default bullet — which is the round bullet, not checkmark
        items_with_checkmark = 0
        matched_items = []
        for item_substr in expected_items:
            found_with_check = False
            for para in bullet_paras:
                if item_substr.lower() in para.text.lower():
                    nid = get_paragraph_numid(para)
                    if nid is not None and numid_is_checkmark.get(nid, False):
                        found_with_check = True
                    # If no explicit numId, the para inherits from style (default bullet) — NOT checkmark
                    break
            if found_with_check:
                items_with_checkmark += 1
                matched_items.append(item_substr)

        if items_with_checkmark >= 6:
            print(f"PASS: Component 2 — {items_with_checkmark}/8 items present with checkmark bullet ({matched_items}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Only {items_with_checkmark}/8 items have checkmark bullet. Matched: {matched_items}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: ALL 8 bullet paragraphs use checkmark (complete coverage) (0.3 points)
    # This ensures every single item was changed, not just some.
    try:
        if items_with_checkmark == 8:
            print(f"PASS: Component 3 — All 8/8 items use checkmark bullet (0.3 pts)")
            total_score += 0.3
        else:
            missing = [item for item in expected_items if item not in matched_items]
            print(f"FAIL: Component 3 — Not all items use checkmark. {items_with_checkmark}/8. Missing checkmark: {missing}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook for LibreOffice Writer
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

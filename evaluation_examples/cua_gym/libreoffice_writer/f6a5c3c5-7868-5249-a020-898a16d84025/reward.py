"""
Reward Script: Modify 'List Bullet' style to use square bullet (U+25A0)
Task ID: writer_bs_078
Domain: libreoffice_writer
Scoring:
  Component 1 (0.30): Bullet character is U+25A0 (black square)
  Component 2 (0.25): Bullet color is #CC0000 (red)
  Component 3 (0.25): Text indent (left) is 0.8cm (288000 EMU) with hanging 0.2cm (72000 EMU)
  Component 4 (0.20): Tab stop after bullet at 0.8cm (288000 EMU)
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_bs_078'


def persist_app_state(domain):
    """Best-effort save via Ctrl+S in case LibreOffice has unsaved changes."""
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print("PERSIST: ctrl+s sent for libreoffice_writer")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Strategy: Parse the numbering XML for the abstractNum linked to the
    ListBullet style (numId referenced by the 'List Bullet' paragraph style).
    Check bullet character, color, indentation, and tab stop.
    """
    total_score = 0.0

    try:
        from docx import Document
        from docx.oxml.ns import qn
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the numId used by 'List Bullet' style
    try:
        list_bullet_style = None
        for s in doc.styles:
            if s.name == 'List Bullet':
                list_bullet_style = s
                break

        if list_bullet_style is None:
            print("CRITICAL: 'List Bullet' style not found in document")
            print("REWARD: 0.0")
            return 0.0

        # Extract numId from the style's pPr/numPr
        style_el = list_bullet_style.element
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        num_pr = style_el.find('.//w:numPr', ns)
        if num_pr is None:
            print("CRITICAL: 'List Bullet' style has no numPr element")
            print("REWARD: 0.0")
            return 0.0

        num_id_el = num_pr.find('w:numId', ns)
        if num_id_el is None:
            print("CRITICAL: 'List Bullet' style has no numId")
            print("REWARD: 0.0")
            return 0.0

        num_id = num_id_el.get(qn('w:val'))
        print(f"INFO: 'List Bullet' style uses numId={num_id}")

        # Navigate numbering: numId -> abstractNumId -> abstractNum XML
        numbering_part = doc.part.numbering_part
        if numbering_part is None:
            print("CRITICAL: No numbering part in document")
            print("REWARD: 0.0")
            return 0.0

        numbering_el = numbering_part._element

        # Find abstractNumId for the given numId
        abstract_num_id = None
        for num in numbering_el.findall('.//w:num', ns):
            if num.get(qn('w:numId')) == num_id:
                abstract_ref = num.find('w:abstractNumId', ns)
                if abstract_ref is not None:
                    abstract_num_id = abstract_ref.get(qn('w:val'))
                break

        if abstract_num_id is None:
            print(f"CRITICAL: Could not find abstractNumId for numId={num_id}")
            print("REWARD: 0.0")
            return 0.0

        # Find the abstractNum element
        abstract_num = None
        for an in numbering_el.findall('.//w:abstractNum', ns):
            if an.get(qn('w:abstractNumId')) == abstract_num_id:
                abstract_num = an
                break

        if abstract_num is None:
            print(f"CRITICAL: Could not find abstractNum with id={abstract_num_id}")
            print("REWARD: 0.0")
            return 0.0

        # Also check for lvlOverride in the num element (agent might override at num level)
        lvl_override = None
        for num in numbering_el.findall('.//w:num', ns):
            if num.get(qn('w:numId')) == num_id:
                override = num.find('w:lvlOverride', ns)
                if override is not None:
                    lvl_from_override = override.find('w:lvl', ns)
                    if lvl_from_override is not None:
                        lvl_override = lvl_from_override
                break

        # Get level 0 definition (use override if present, otherwise abstractNum)
        lvl = lvl_override if lvl_override is not None else abstract_num.find('.//w:lvl', ns)
        if lvl is None:
            print("CRITICAL: No level definition found")
            print("REWARD: 0.0")
            return 0.0

        print(f"INFO: Using abstractNumId={abstract_num_id}, lvlOverride={'yes' if lvl_override else 'no'}")

    except Exception as e:
        print(f"CRITICAL: Error navigating numbering structure: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Bullet character is U+25A0 (black square) (0.30 points)
    try:
        lvl_text_el = lvl.find('.//w:lvlText', ns)
        num_fmt_el = lvl.find('.//w:numFmt', ns)

        num_fmt = num_fmt_el.get(qn('w:val')) if num_fmt_el is not None else None
        lvl_text = lvl_text_el.get(qn('w:val')) if lvl_text_el is not None else None

        if num_fmt != 'bullet':
            print(f"FAIL: Component 1 -- numFmt is '{num_fmt}', expected 'bullet'")
        elif lvl_text is None:
            print("FAIL: Component 1 -- lvlText not found")
        else:
            # U+25A0 is the black square character
            # It may appear as the character itself or as &#9632;
            char_code = ord(lvl_text) if len(lvl_text) == 1 else None
            if char_code == 0x25A0:
                print(f"PASS: Component 1 -- Bullet character is U+25A0 (black square) (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 1 -- Bullet character is U+{char_code:04X} ('{lvl_text}'), expected U+25A0")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Bullet color is #CC0000 (red) (0.25 points)
    try:
        rpr = lvl.find('.//w:rPr', ns)
        if rpr is None:
            print("FAIL: Component 2 -- No rPr (run properties) in level definition")
        else:
            color_el = rpr.find('w:color', ns)
            if color_el is None:
                print("FAIL: Component 2 -- No color element in rPr")
            else:
                color_val = color_el.get(qn('w:val'))
                if color_val is not None:
                    color_val_upper = color_val.upper()
                    if color_val_upper == 'CC0000':
                        print(f"PASS: Component 2 -- Bullet color is #CC0000 (red) (0.25 pts)")
                        total_score += 0.25
                    else:
                        print(f"FAIL: Component 2 -- Bullet color is #{color_val_upper}, expected #CC0000")
                else:
                    print("FAIL: Component 2 -- color element has no val attribute")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Text indent (left) is 0.8cm with hanging 0.2cm (0.25 points)
    # 0.8cm = 288000 EMU; 0.2cm = 72000 EMU
    # Tolerance: +/- 5% (14400 EMU for left, 3600 EMU for hanging)
    try:
        ppr = lvl.find('.//w:pPr', ns)
        if ppr is None:
            print("FAIL: Component 3 -- No pPr in level definition")
        else:
            ind_el = ppr.find('w:ind', ns)
            if ind_el is None:
                print("FAIL: Component 3 -- No ind element in pPr")
            else:
                left_val = ind_el.get(qn('w:left'))
                hanging_val = ind_el.get(qn('w:hanging'))

                left_ok = False
                hanging_ok = False

                if left_val is not None:
                    left_int = int(left_val)
                    # Accept within 5% tolerance of 288000
                    if abs(left_int - 288000) <= 14400:
                        left_ok = True
                    # Also accept twips: 0.8cm = 454 twips (check if in twips range)
                    elif abs(left_int - 454) <= 25:
                        left_ok = True

                if hanging_val is not None:
                    hanging_int = int(hanging_val)
                    # Accept within 5% tolerance of 72000
                    if abs(hanging_int - 72000) <= 3600:
                        hanging_ok = True
                    # Also accept twips: 0.2cm = 113 twips
                    elif abs(hanging_int - 113) <= 10:
                        hanging_ok = True

                if left_ok and hanging_ok:
                    print(f"PASS: Component 3 -- left={left_val}, hanging={hanging_val} (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 3 -- left={left_val} (ok={left_ok}), hanging={hanging_val} (ok={hanging_ok})")
                    print(f"  Expected: left~288000 (0.8cm), hanging~72000 (0.2cm)")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Tab stop after bullet at 0.8cm (288000 EMU) (0.20 points)
    try:
        ppr = lvl.find('.//w:pPr', ns)
        if ppr is None:
            print("FAIL: Component 4 -- No pPr in level definition")
        else:
            tabs_el = ppr.find('w:tabs', ns)
            if tabs_el is None:
                print("FAIL: Component 4 -- No tabs element in pPr")
            else:
                tab_els = tabs_el.findall('w:tab', ns)
                tab_found = False
                for tab in tab_els:
                    tab_val = tab.get(qn('w:val'))
                    tab_pos = tab.get(qn('w:pos'))
                    if tab_pos is not None and tab_val == 'num':
                        pos_int = int(tab_pos)
                        # Accept within 5% tolerance of 288000 EMU
                        if abs(pos_int - 288000) <= 14400:
                            tab_found = True
                        # Also accept twips: 0.8cm = 454 twips
                        elif abs(pos_int - 454) <= 25:
                            tab_found = True

                if tab_found:
                    print(f"PASS: Component 4 -- Tab stop at 0.8cm found (0.20 pts)")
                    total_score += 0.20
                else:
                    positions = [(t.get(qn('w:val')), t.get(qn('w:pos'))) for t in tab_els]
                    print(f"FAIL: Component 4 -- No tab stop at 0.8cm. Found tabs: {positions}")
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

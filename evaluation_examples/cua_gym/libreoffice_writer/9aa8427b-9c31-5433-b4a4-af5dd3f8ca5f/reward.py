"""
Reward Script: Add double-line page borders to a court order document
Task ID: writer_legal_072
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): pgBorders element exists on all sections
  Component 2 (0.3): All four sides have a thick-thin double line style
  Component 3 (0.2): Border spacing from text is approximately 1 cm (~28 pts)
  Component 4 (0.2): offsetFrom attribute is set to "text"
"""

import os
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_legal_072'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

# Acceptable thick-thin double line styles in OOXML
DOUBLE_LINE_STYLES = {
    'thickThinSmallGap', 'thickThinMediumGap', 'thickThinLargeGap',
    'thinThickSmallGap', 'thinThickMediumGap', 'thinThickLargeGap',
    'thinThickThinSmallGap', 'thinThickThinMediumGap', 'thinThickThinLargeGap',
    'double',
}

SIDES = ['top', 'left', 'bottom', 'right']


def persist_app_state(domain: str):
    """Try to save any unsaved LibreOffice edits."""
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
    Verify that page borders have been added to the document.
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

    sections = doc.sections
    if len(sections) == 0:
        print("FAIL: No sections found in document")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: pgBorders element exists in all sections (0.3 points)
    try:
        all_have_borders = True
        for i, section in enumerate(sections):
            sect_elem = section._sectPr
            pg_borders = sect_elem.findall('.//w:pgBorders', NS)
            if len(pg_borders) == 0:
                all_have_borders = False
                print(f"FAIL: Component 1 -- Section {i} has no pgBorders element")
                break

        if all_have_borders:
            print(f"PASS: Component 1 -- All {len(sections)} section(s) have pgBorders (0.3 pts)")
            total_score += 0.3
        else:
            print("FAIL: Component 1 -- Not all sections have page borders")
            # If no borders at all, nothing else can pass
            final_score = min(total_score, 1.0)
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {final_score}")
            return final_score
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: All four sides use a thick-thin double line style (0.3 points)
    try:
        all_double_line = True
        found_styles = {}
        for i, section in enumerate(sections):
            sect_elem = section._sectPr
            pg_borders = sect_elem.find('.//w:pgBorders', NS)
            for side in SIDES:
                side_elem = pg_borders.find(f'w:{side}', NS)
                if side_elem is None:
                    all_double_line = False
                    print(f"FAIL: Component 2 -- Section {i} missing '{side}' border element")
                    break
                border_val = side_elem.get(f'{{{NS["w"]}}}val', '')
                found_styles[f"s{i}_{side}"] = border_val
                if border_val not in DOUBLE_LINE_STYLES:
                    all_double_line = False
                    print(f"FAIL: Component 2 -- Section {i} '{side}' has style '{border_val}', not a double line style")
                    break
            if not all_double_line:
                break

        if all_double_line:
            sample_style = list(found_styles.values())[0] if found_styles else "unknown"
            print(f"PASS: Component 2 -- All sides have double line style '{sample_style}' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 -- Styles found: {found_styles}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Border spacing from text is approximately 1 cm on all sides (0.2 points)
    # 1 cm ~ 28.35 points. Accept range 24-32 to allow for rounding.
    try:
        all_spacing_ok = True
        found_spacings = {}
        for i, section in enumerate(sections):
            sect_elem = section._sectPr
            pg_borders = sect_elem.find('.//w:pgBorders', NS)
            for side in SIDES:
                side_elem = pg_borders.find(f'w:{side}', NS)
                if side_elem is None:
                    all_spacing_ok = False
                    break
                space_val = side_elem.get(f'{{{NS["w"]}}}space', '')
                found_spacings[f"s{i}_{side}"] = space_val
                try:
                    space_int = int(space_val)
                except (ValueError, TypeError):
                    all_spacing_ok = False
                    print(f"FAIL: Component 3 -- Section {i} '{side}' has non-numeric space: '{space_val}'")
                    break
                # Accept 24-32 pt range for ~1cm
                if space_int < 24 or space_int > 32:
                    all_spacing_ok = False
                    print(f"FAIL: Component 3 -- Section {i} '{side}' space={space_int}pt, expected ~28pt (1cm)")
                    break
            if not all_spacing_ok:
                break

        if all_spacing_ok:
            sample_space = list(found_spacings.values())[0] if found_spacings else "?"
            print(f"PASS: Component 3 -- Border spacing ~1cm ({sample_space}pt) on all sides (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 -- Spacings: {found_spacings}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: offsetFrom attribute is "text" (0.2 points)
    try:
        all_offset_ok = True
        for i, section in enumerate(sections):
            sect_elem = section._sectPr
            pg_borders = sect_elem.find('.//w:pgBorders', NS)
            offset_from = pg_borders.get(f'{{{NS["w"]}}}offsetFrom', '')
            if offset_from != 'text':
                all_offset_ok = False
                print(f"FAIL: Component 4 -- Section {i} offsetFrom='{offset_from}', expected 'text'")
                break

        if all_offset_ok:
            print(f"PASS: Component 4 -- offsetFrom='text' on all sections (0.2 pts)")
            total_score += 0.2
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

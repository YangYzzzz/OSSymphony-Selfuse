"""
Reward Script: Create a custom 'Code Block' paragraph style
Task ID: writer_bs_050
Domain: libreoffice_writer
Scoring:
  Component 1 (0.20): 'Code Block' style exists as paragraph style
  Component 2 (0.20): Font = Courier New, Size = 10pt
  Component 3 (0.15): Alignment = left, line spacing = single
  Component 4 (0.15): Background shading = #F0F0F0
  Component 5 (0.15): All four borders = 0.5pt solid
  Component 6 (0.15): Padding = 0.3cm on all four sides
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_bs_050'


def persist_app_state():
    """Attempt to save any open LibreOffice document via Ctrl+S."""
    try:
        os.environ["DISPLAY"] = ":0"
        import pyautogui
        import time
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.0)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify that a 'Code Block' paragraph style exists with the required properties.
    Returns: float between 0.0 and 1.0
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

    # Component 1: 'Code Block' style exists as a paragraph style (0.20 points)
    style = None
    try:
        style = doc.styles['Code Block']
        if style.type is not None and style.type.name == 'PARAGRAPH':
            print(f"PASS: Component 1 — 'Code Block' paragraph style exists (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — 'Code Block' exists but is type {style.type}, not PARAGRAPH")
    except KeyError:
        print("FAIL: Component 1 — 'Code Block' style does not exist")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if style is None:
        # No point checking further properties if style doesn't exist
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: Font = Courier New, Size = 10pt (0.20 points)
    try:
        font_name = style.font.name
        font_size_pt = style.font.size.pt if style.font.size else None

        font_ok = (font_name is not None and 'courier' in font_name.lower() and 'new' in font_name.lower())
        size_ok = (font_size_pt is not None and abs(font_size_pt - 10.0) < 0.5)

        if font_ok and size_ok:
            print(f"PASS: Component 2 — Font='{font_name}', Size={font_size_pt}pt (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — Font='{font_name}' (expect Courier New), Size={font_size_pt}pt (expect 10)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Alignment = left, line spacing = single (0.15 points)
    try:
        from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
        pf = style.paragraph_format
        alignment = pf.alignment
        line_spacing = pf.line_spacing

        # Also check XML for spacing line attribute
        pPr = style.element.find(qn('w:pPr'))
        spacing_elem = pPr.find(qn('w:spacing')) if pPr is not None else None
        line_val = spacing_elem.get(qn('w:line')) if spacing_elem is not None else None

        align_ok = (alignment is not None and alignment == WD_PARAGRAPH_ALIGNMENT.LEFT)

        # Single spacing: line_spacing == 1.0, or XML w:line="240" with lineRule="auto"
        spacing_ok = (
            (line_spacing is not None and abs(float(line_spacing) - 1.0) < 0.1)
            or (line_val is not None and line_val == "240")
        )

        if align_ok and spacing_ok:
            print(f"PASS: Component 3 — Alignment=LEFT, LineSpacing=single (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — Alignment={alignment} (expect LEFT), LineSpacing={line_spacing}/xml_line={line_val} (expect single/240)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Background shading = #F0F0F0 (0.15 points)
    try:
        pPr = style.element.find(qn('w:pPr'))
        shd = pPr.find(qn('w:shd')) if pPr is not None else None

        if shd is not None:
            fill_val = shd.get(qn('w:fill'))
            if fill_val is not None and fill_val.upper() == 'F0F0F0':
                print(f"PASS: Component 4 — Background shading fill=#{fill_val} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — Background shading fill=#{fill_val}, expected #F0F0F0")
        else:
            print("FAIL: Component 4 — No shading element found in style")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: All four borders = 0.5pt solid (0.15 points)
    try:
        pPr = style.element.find(qn('w:pPr'))
        pBdr = pPr.find(qn('w:pBdr')) if pPr is not None else None

        if pBdr is not None:
            sides = ['top', 'left', 'bottom', 'right']
            borders_ok = 0
            for side in sides:
                bdr = pBdr.find(qn(f'w:{side}'))
                if bdr is not None:
                    val = bdr.get(qn('w:val'))
                    sz = bdr.get(qn('w:sz'))
                    # sz is in 1/8th of a point; 0.5pt = 4 eighths
                    if val == 'single' and sz is not None and int(sz) == 4:
                        borders_ok += 1
                    else:
                        print(f"  Border {side}: val={val}, sz={sz} (expect single, 4)")
                else:
                    print(f"  Border {side}: element not found")

            if borders_ok == 4:
                print(f"PASS: Component 5 — All 4 borders are 0.5pt solid (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 — Only {borders_ok}/4 borders correct")
        else:
            print("FAIL: Component 5 — No paragraph borders element found in style")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Padding = 0.3cm on all four sides (0.15 points)
    # In OOXML, padding is w:space attribute on border elements, in 1/20th of a point
    # 0.3cm = approx 170 twentieths of a point (tolerance: 160-180)
    try:
        pPr = style.element.find(qn('w:pPr'))
        pBdr = pPr.find(qn('w:pBdr')) if pPr is not None else None

        if pBdr is not None:
            sides = ['top', 'left', 'bottom', 'right']
            padding_ok = 0
            for side in sides:
                bdr = pBdr.find(qn(f'w:{side}'))
                if bdr is not None:
                    space = bdr.get(qn('w:space'))
                    if space is not None:
                        space_val = int(space)
                        # 0.3cm ~ 170 twentieths of a point; allow tolerance 150-190
                        if 150 <= space_val <= 190:
                            padding_ok += 1
                        else:
                            print(f"  Padding {side}: space={space_val} (expect ~170 for 0.3cm)")
                    else:
                        print(f"  Padding {side}: no space attribute")
                else:
                    print(f"  Padding {side}: border element not found")

            if padding_ok == 4:
                print(f"PASS: Component 6 — Padding ~0.3cm on all 4 sides (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 6 — Only {padding_ok}/4 sides have correct padding")
        else:
            print("FAIL: Component 6 — No paragraph borders element (needed for padding)")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint
persist_app_state()
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

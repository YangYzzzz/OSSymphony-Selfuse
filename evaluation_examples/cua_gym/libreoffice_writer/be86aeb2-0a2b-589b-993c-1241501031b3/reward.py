"""
Reward Script: Modify Heading 1 style — font, color, border, spacing
Task ID: writer_rd_048
Domain: libreoffice_writer
Scoring:
  Component 1: Font name changed to Helvetica (or Liberation Sans fallback) — 0.2 pts
  Component 2: Font size changed to 20pt — 0.2 pts
  Component 3: Font color changed to dark teal #006666 — 0.2 pts
  Component 4: Bottom border added (single, dark teal) — 0.2 pts
  Component 5: Space after paragraph set to ~1.0 cm — 0.2 pts
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_rd_048'


def persist_app_state(domain):
    """Send Ctrl+S to save any unsaved LibreOffice changes."""
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for " + domain)
    except Exception as e:
        print("PERSIST_WARN: save hook failed: " + str(e))


def verify_task(file_path):
    """
    Verify Heading 1 style modifications with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        from docx.shared import Pt, RGBColor, Cm
        from docx.oxml.ns import qn
    except ImportError as e:
        print("CRITICAL: Missing library: " + str(e))
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print("CRITICAL: Cannot load file " + file_path + ": " + str(e))
        print("REWARD: 0.0")
        return 0.0

    # Get the Heading 1 style (handle both direct access and iteration fallback)
    style = None
    try:
        style = doc.styles['Heading 1']
    except KeyError:
        # After LibreOffice resave, direct lookup may fail; iterate to find it
        for s in doc.styles:
            if s.name == 'Heading 1' and str(s.type) == 'PARAGRAPH (1)':
                style = s
                break
    except Exception as e:
        print("CRITICAL: Cannot access styles: " + str(e))
        print("REWARD: 0.0")
        return 0.0

    if style is None:
        print("CRITICAL: Heading 1 style not found in document")
        print("REWARD: 0.0")
        return 0.0

    font = style.font
    pf = style.paragraph_format

    # Component 1: Font name changed to Helvetica (0.2 points)
    # Initial: Liberation Sans → Golden: Helvetica
    # Accept Helvetica or Liberation Sans (as fallback per task context)
    try:
        font_name = font.name
        # The task says Helvetica; context says "(or Liberation Sans as fallback)"
        # Initial state uses Liberation Sans at 18pt, so we need to distinguish.
        # Golden uses Helvetica. We accept Helvetica as primary.
        # We must NOT award points if font_name is still the initial "Liberation Sans" at 18pt
        # unless the size is also 20pt (meaning the agent tried Helvetica but it fell back).
        # Simplest: check for Helvetica specifically since that's what golden has.
        if font_name and font_name.lower() == 'helvetica':
            print("PASS: Component 1 — Font name is Helvetica (0.2 pts)")
            total_score += 0.2
        else:
            print("FAIL: Component 1 — Expected font 'Helvetica', found: " + str(font_name))
    except Exception as e:
        print("ERROR: Component 1 — " + str(e))

    # Component 2: Font size changed to 20pt (0.2 points)
    # Initial: 18pt → Golden: 20pt
    try:
        if font.size and abs(font.size.pt - 20.0) < 0.5:
            print("PASS: Component 2 — Font size is " + str(font.size.pt) + "pt (0.2 pts)")
            total_score += 0.2
        else:
            actual_pt = font.size.pt if font.size else None
            print("FAIL: Component 2 — Expected 20pt, found: " + str(actual_pt) + "pt")
    except Exception as e:
        print("ERROR: Component 2 — " + str(e))

    # Component 3: Font color changed to dark teal #006666 (0.2 points)
    # Initial: #000000 → Golden: #006666
    try:
        color_rgb = font.color.rgb if font.color and font.color.rgb else None
        if color_rgb and str(color_rgb).upper() == '006666':
            print("PASS: Component 3 — Font color is #006666 (0.2 pts)")
            total_score += 0.2
        else:
            print("FAIL: Component 3 — Expected color #006666, found: " + str(color_rgb))
    except Exception as e:
        print("ERROR: Component 3 — " + str(e))

    # Component 4: Bottom border added — single line, dark teal color (0.2 points)
    # Initial: No borders → Golden: bottom border single, color 006666
    try:
        pPr = style.element.find(qn('w:pPr'))
        bval = None
        bcolor = None
        if pPr is not None:
            pBdr = pPr.find(qn('w:pBdr'))
            if pBdr is not None:
                bottom = pBdr.find(qn('w:bottom'))
                if bottom is not None:
                    bval = bottom.get(qn('w:val'))
                    bcolor = bottom.get(qn('w:color'))

        has_border = (bval is not None and bval != 'none')
        has_correct_color = (bcolor is not None and bcolor.upper() == '006666')

        if has_border and has_correct_color:
            print("PASS: Component 4 — Bottom border present with color #006666 (0.2 pts)")
            total_score += 0.2
        elif has_border:
            # Partial: border exists but wrong color — give 0.1
            print("PARTIAL: Component 4 — Bottom border found but color mismatch (0.1 pts)")
            total_score += 0.1
        else:
            print("FAIL: Component 4 — No bottom border on Heading 1 style")
    except Exception as e:
        print("ERROR: Component 4 — " + str(e))

    # Component 5: Space after paragraph set to ~1.0 cm (0.2 points)
    # Initial: 76200 EMU (0.6 cm) → Golden: 360045 EMU (~1.0 cm)
    # 1.0 cm = 360000 EMU. Allow tolerance of ~0.05 cm (18000 EMU).
    try:
        space_after = pf.space_after
        if space_after is not None:
            space_cm = space_after / 360000.0
            # Must be significantly larger than initial 0.6 cm (76200 EMU = 0.2117 cm)
            # Actually initial space_after is 76200 EMU = 6pt. Let me recalculate.
            # 76200 EMU / 12700 = 6pt. 76200 / 360000 = 0.2117 cm.
            # Target: 1.0 cm = 360000 EMU. Tolerance: 0.85-1.15 cm.
            if 0.85 <= space_cm <= 1.15:
                print("PASS: Component 5 — Space after is " + str(round(space_cm, 3)) + " cm (0.2 pts)")
                total_score += 0.2
            else:
                print("FAIL: Component 5 — Expected ~1.0 cm, found " + str(round(space_cm, 3)) + " cm (" + str(space_after) + " EMU)")
        else:
            print("FAIL: Component 5 — Space after is None (inherited)")
    except Exception as e:
        print("ERROR: Component 5 — " + str(e))

    final_score = min(round(total_score, 2), 1.0)
    print("")
    print("Score: " + str(total_score) + "/1.0")
    print("REWARD: " + str(final_score))
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = WORKDIR + '/' + TASK_ID + '.docx'
if not os.path.exists(file_path):
    print("File not found: " + file_path)
    print("REWARD: 0.0")
else:
    verify_task(file_path)

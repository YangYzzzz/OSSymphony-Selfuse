"""
Reward Script: Configure Heading 1 style with specific font, color, spacing, and border
Task ID: writer_tech_080
Domain: libreoffice_writer
Scoring:
  Component 1 (0.25): Font name is Fira Sans
  Component 2 (0.20): Font size is 16pt
  Component 3 (0.20): Font color is dark blue #0D47A1
  Component 4 (0.15): Spacing before=12pt, after=6pt
  Component 5 (0.20): Bottom border 1pt single in dark blue #0D47A1
"""

import os
from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_tech_080'


def persist_app_state(domain):
    """Save any unsaved edits in LibreOffice Writer."""
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        import time
        time.sleep(1.0)
        print("PERSIST: ctrl+s sent for", domain)
    except Exception as e:
        print("PERSIST_WARN: save hook failed:", e)


def color_distance(hex1, hex2):
    """Compute Euclidean RGB distance between two hex color strings (without #)."""
    r1, g1, b1 = int(hex1[0:2], 16), int(hex1[2:4], 16), int(hex1[4:6], 16)
    r2, g2, b2 = int(hex2[0:2], 16), int(hex2[2:4], 16), int(hex2[4:6], 16)
    return ((r1 - r2)**2 + (g1 - g2)**2 + (b1 - b2)**2)**0.5


def verify_task(file_path):
    """
    Verify Heading 1 style configuration with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get the Heading 1 style
    try:
        style = doc.styles['Heading 1']
    except Exception as e:
        print(f"CRITICAL: Cannot find Heading 1 style: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Font name is Fira Sans (0.25 points)
    try:
        font_name = style.font.name
        # Also check the XML directly for rFonts ascii attribute
        rPr = style.element.find(qn('w:rPr'))
        xml_font = None
        if rPr is not None:
            rFonts = rPr.find(qn('w:rFonts'))
            if rFonts is not None:
                xml_font = rFonts.get(qn('w:ascii'))

        actual_name = font_name or xml_font
        if actual_name and 'fira sans' in actual_name.lower():
            print(f"PASS: Component 1 — Font name is '{actual_name}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Expected 'Fira Sans', found: font.name={font_name}, xml={xml_font}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Font size is 16pt (0.20 points)
    try:
        font_size = style.font.size
        if font_size is not None:
            size_pt = font_size.pt
            if abs(size_pt - 16.0) < 0.5:
                print(f"PASS: Component 2 — Font size is {size_pt}pt (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 — Expected 16pt, found: {size_pt}pt")
        else:
            print("FAIL: Component 2 — Font size is None (inherited)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Font color is dark blue #0D47A1 (0.20 points)
    try:
        color_rgb = style.font.color.rgb
        if color_rgb is not None:
            color_str = str(color_rgb).upper()
            dist = color_distance(color_str, '0D47A1')
            if dist < 15:
                print(f"PASS: Component 3 — Font color is #{color_str} (dist={dist:.1f}) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — Expected #0D47A1, found #{color_str} (dist={dist:.1f})")
        else:
            print("FAIL: Component 3 — Font color is None (inherited)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Spacing before=12pt, after=6pt (0.15 points)
    try:
        pf = style.paragraph_format
        space_before = pf.space_before
        space_after = pf.space_after

        before_ok = (space_before is not None and abs(space_before.pt - 12.0) < 1.0)
        after_ok = (space_after is not None and abs(space_after.pt - 6.0) < 1.0)

        if space_before is not None:
            print(f"  Space before: {space_before.pt}pt (expected 12pt) — {'OK' if before_ok else 'MISMATCH'}")
        else:
            print("  Space before: None (inherited)")

        if space_after is not None:
            print(f"  Space after: {space_after.pt}pt (expected 6pt) — {'OK' if after_ok else 'MISMATCH'}")
        else:
            print("  Space after: None (inherited)")

        if before_ok and after_ok:
            print(f"PASS: Component 4 — Spacing before=12pt, after=6pt (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — Spacing mismatch")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Bottom border 1pt single in dark blue #0D47A1 (0.20 points)
    try:
        style_elem = style.element
        pPr = style_elem.find(qn('w:pPr'))
        bottom = None

        if pPr is not None:
            pBdr = pPr.find(qn('w:pBdr'))
            if pBdr is not None:
                bottom = pBdr.find(qn('w:bottom'))

        if bottom is not None:
            bval = bottom.get(qn('w:val'))
            bsz = bottom.get(qn('w:sz'))
            bcolor = bottom.get(qn('w:color'))

            print(f"  Bottom border: val={bval}, sz={bsz}, color={bcolor}")

            # Derive all checks from comparisons
            border_style_ok = (bval == 'single')
            border_size_ok = (bsz is not None and int(bsz) == 8)  # 1pt = 8 eighths-of-a-point in OOXML
            border_color_ok = (bcolor is not None and color_distance(bcolor.upper(), '0D47A1') < 15)

            if not border_size_ok and bsz is not None:
                print(f"  Border size: {int(bsz)} (expected 8 = 1pt)")
            if not border_color_ok and bcolor is not None:
                print(f"  Border color: #{bcolor.upper()} (expected #0D47A1)")

            if border_style_ok and border_size_ok and border_color_ok:
                print(f"PASS: Component 5 — Bottom border 1pt single #0D47A1 (0.20 pts)")
                total_score += 0.20
            else:
                # Partial credit for partially correct border
                partial = 0.0
                if border_style_ok:
                    partial += 0.07
                if border_size_ok:
                    partial += 0.06
                if border_color_ok:
                    partial += 0.07
                if partial > 0:
                    print(f"PARTIAL: Component 5 — Some border properties match ({partial:.2f} pts)")
                    total_score += partial
                else:
                    print(f"FAIL: Component 5 — Border exists but properties don't match")
        else:
            print(f"FAIL: Component 5 — No bottom border found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state('libreoffice_writer')

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

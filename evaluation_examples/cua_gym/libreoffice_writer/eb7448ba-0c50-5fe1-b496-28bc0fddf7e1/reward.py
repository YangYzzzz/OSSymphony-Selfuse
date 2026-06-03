"""
Reward Script: Insert a warning triangle shape with gradient, text, and border in LibreOffice Writer
Task ID: writer_obj_073
Domain: libreoffice_writer
Scoring:
  Component 1: Triangle shape exists (0.20 pts) — shape with drawing/anchor element present
  Component 2: Triangle geometry + gradient fill red-to-orange (0.30 pts) — prstGeom triangle + gradFill colors
  Component 3: Size approximately 5cm x 5cm (0.15 pts) — cx/cy near 1800000 EMU (5cm = 1800000 EMU)
  Component 4: 'WARNING' text in white bold 14pt (0.20 pts) — text content, color, bold, font size
  Component 5: Dark red border #B71C1C with 2pt line width (0.15 pts) — a:ln element with color and width
  Total: 1.0
"""

import os
from lxml import etree

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_obj_073'
FILE_PATH = f'{WORKDIR}/safety_manual.docx'

# Namespace mappings
NS = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'wps': 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape',
}

# Tolerance for dimension checks (EMU): allow ±5% of 1800000 = 90000
EMU_5CM = 1800000  # 5cm = 1800000 EMU (360000 EMU per cm)
EMU_TOL = 90000    # 5% tolerance

# Position: X=6cm=2160000 EMU, Y=8cm=2880000 EMU
EMU_6CM = 2160000
EMU_8CM = 2880000
POS_TOL = 180000   # ~0.5cm tolerance for position checks


def color_match(actual_hex, expected_hex, tolerance=30):
    """Check if two hex colors are close (Euclidean distance in RGB space)."""
    try:
        r1, g1, b1 = int(actual_hex[0:2], 16), int(actual_hex[2:4], 16), int(actual_hex[4:6], 16)
        r2, g2, b2 = int(expected_hex[0:2], 16), int(expected_hex[2:4], 16), int(expected_hex[4:6], 16)
        dist = ((r1 - r2)**2 + (g1 - g2)**2 + (b1 - b2)**2) ** 0.5
        return dist <= tolerance
    except Exception:
        return False


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load document
    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get all drawing elements from document body
    body = doc.element.body
    drawings = body.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}drawing')

    # Component 1: Triangle shape exists as anchor drawing (0.20 pts)
    # Must fail on initial (no drawings) and pass on golden (drawing present)
    try:
        anchor_found = False
        anchor_elem = None
        for drawing in drawings:
            anchor = drawing.find(
                '{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}anchor'
            )
            if anchor is not None:
                anchor_found = True
                anchor_elem = anchor
                break
        if anchor_found:
            print(f"PASS: Component 1 — Anchor drawing shape found (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — No anchor drawing element found in document")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if anchor_elem is None:
        # No shape at all; remaining components cannot pass
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: Triangle geometry + gradient fill with correct colors (0.30 pts)
    # Checks prstGeom prst="triangle" AND gradFill with F44336 (red) and FF9800 (orange)
    try:
        # Check triangle geometry
        prstGeom = anchor_elem.find(
            './/{http://schemas.openxmlformats.org/drawingml/2006/main}prstGeom'
        )
        is_triangle = (prstGeom is not None and
                       prstGeom.get('prst', '').lower() == 'triangle')

        # Check gradient fill
        gradFill = anchor_elem.find(
            './/{http://schemas.openxmlformats.org/drawingml/2006/main}gradFill'
        )
        grad_ok = False
        if gradFill is not None:
            gs_elems = gradFill.findall(
                './/{http://schemas.openxmlformats.org/drawingml/2006/main}gs'
            )
            colors_found = []
            for gs in gs_elems:
                srgb = gs.find(
                    '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr'
                )
                if srgb is not None:
                    colors_found.append(srgb.get('val', '').upper())
            # Check for red (F44336) and orange (FF9800) — allow tolerant match
            has_red = any(color_match(c, 'F44336') for c in colors_found)
            has_orange = any(color_match(c, 'FF9800') for c in colors_found)
            grad_ok = has_red and has_orange

        if is_triangle and grad_ok:
            print(f"PASS: Component 2 — Triangle geometry + gradient fill (red→orange) (0.30 pts)")
            total_score += 0.30
        elif is_triangle and not grad_ok:
            print(f"FAIL: Component 2 — Triangle found but gradient fill missing or wrong colors. "
                  f"Colors found: {colors_found if 'colors_found' in dir() else 'none'}")
        elif not is_triangle and grad_ok:
            print(f"FAIL: Component 2 — Gradient fill OK but shape is not triangle. "
                  f"prst={prstGeom.get('prst') if prstGeom is not None else 'none'}")
        else:
            print(f"FAIL: Component 2 — Triangle geometry not found or no gradient fill")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Shape size approximately 5cm x 5cm (0.15 pts)
    # 5cm = 1800000 EMU; tolerance ±5%
    try:
        extent = anchor_elem.find(
            '{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}extent'
        )
        if extent is not None:
            cx = int(extent.get('cx', 0))
            cy = int(extent.get('cy', 0))
            size_ok = (abs(cx - EMU_5CM) <= EMU_TOL and abs(cy - EMU_5CM) <= EMU_TOL)
            if size_ok:
                print(f"PASS: Component 3 — Shape size ~5cm x 5cm (cx={cx}, cy={cy}) (0.15 pts)")
                total_score += 0.15
            else:
                # Convert to cm for readable output
                cx_cm = cx / 360000
                cy_cm = cy / 360000
                print(f"FAIL: Component 3 — Expected ~5cm x 5cm, got {cx_cm:.2f}cm x {cy_cm:.2f}cm "
                      f"(cx={cx}, cy={cy})")
        else:
            print(f"FAIL: Component 3 — extent element not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: 'WARNING' text inside shape, white bold 14pt (0.20 pts)
    # Checks: text content == 'WARNING', color FFFFFF, bold <w:b/>, size 28 half-points (14pt)
    try:
        # Look inside wps:txbx for text content
        txbx = anchor_elem.find(
            './/{http://schemas.microsoft.com/office/word/2010/wordprocessingShape}txbx'
        )
        text_ok = False
        white_ok = False
        bold_ok = False
        size_ok = False

        if txbx is not None:
            # Find all w:t elements
            t_elems = txbx.findall(
                './/{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'
            )
            full_text = ''.join(t.text or '' for t in t_elems).strip()
            text_ok = full_text.upper() == 'WARNING'

            # Check run properties
            rPr_elems = txbx.findall(
                './/{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rPr'
            )
            for rPr in rPr_elems:
                # Check bold
                b_elem = rPr.find(
                    '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}b'
                )
                if b_elem is not None:
                    bold_ok = True

                # Check white color (#FFFFFF)
                color_elem = rPr.find(
                    '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}color'
                )
                if color_elem is not None:
                    color_val = color_elem.get(
                        '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val', ''
                    ).upper()
                    if color_match(color_val, 'FFFFFF', tolerance=20):
                        white_ok = True

                # Check font size: 14pt = 28 half-points (w:sz val="28")
                sz_elem = rPr.find(
                    '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}sz'
                )
                if sz_elem is not None:
                    sz_val = int(sz_elem.get(
                        '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val', 0
                    ))
                    if sz_val == 28:  # 14pt = 28 half-points
                        size_ok = True

        all_text_ok = text_ok and white_ok and bold_ok and size_ok
        if all_text_ok:
            print(f"PASS: Component 4 — 'WARNING' text, white, bold, 14pt (0.20 pts)")
            total_score += 0.20
        else:
            details = []
            if not text_ok:
                details.append(f"text='{full_text if 'full_text' in dir() else 'not found'}' (expected 'WARNING')")
            if not white_ok:
                details.append("color not white #FFFFFF")
            if not bold_ok:
                details.append("not bold")
            if not size_ok:
                details.append("font size not 14pt (28 half-pts)")
            print(f"FAIL: Component 4 — text issues: {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Dark red border #B71C1C with 2pt solid line (0.15 pts)
    # 2pt = 25400 EMU (12700 EMU per point); tolerance ±2 points = ±25400
    try:
        ln_elem = anchor_elem.find(
            './/{http://schemas.openxmlformats.org/drawingml/2006/main}ln'
        )
        border_color_ok = False
        border_width_ok = False

        if ln_elem is not None:
            # Check line width: 2pt = 25400 EMU (12700 EMU per point)
            ln_w = int(ln_elem.get('w', 0))
            border_width_ok = abs(ln_w - 25400) <= 25400  # ±2pt tolerance

            # Check border color
            solidFill = ln_elem.find(
                './/{http://schemas.openxmlformats.org/drawingml/2006/main}solidFill'
            )
            if solidFill is not None:
                srgb = solidFill.find(
                    '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr'
                )
                if srgb is not None:
                    border_hex = srgb.get('val', '').upper()
                    border_color_ok = color_match(border_hex, 'B71C1C', tolerance=30)

        if border_color_ok and border_width_ok:
            print(f"PASS: Component 5 — Dark red border #B71C1C, 2pt width (0.15 pts)")
            total_score += 0.15
        else:
            details = []
            if not border_color_ok:
                details.append(f"border color not #B71C1C (found: {border_hex if 'border_hex' in dir() else 'not found'})")
            if not border_width_ok:
                details.append(f"border width not ~2pt (found: {ln_w if 'ln_w' in dir() else 'not found'} EMU)")
            print(f"FAIL: Component 5 — border issues: {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

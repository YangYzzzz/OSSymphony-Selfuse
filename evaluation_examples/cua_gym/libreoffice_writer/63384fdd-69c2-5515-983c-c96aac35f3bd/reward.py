"""
Reward Script: Set rectangle shape formatting and text in alert_doc.docx
Task ID: writer_obj_078
Domain: libreoffice_writer
Scoring:
  Component 1: Rectangle has no fill (transparent) — 0.30 pts
  Component 2: Rectangle border is 3pt solid dark orange (#E65100) — 0.30 pts
  Component 3: Shape contains text 'ATTENTION' — 0.20 pts
  Component 4: 'ATTENTION' is bold, 16pt, dark orange (#E65100) — 0.20 pts
  Total: 1.0
"""

import os
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_obj_078'
FILE_PATH = f'{WORKDIR}/Desktop/alert_doc.docx'

# Namespace map for DrawingML / WordprocessingShape
NS = {
    'w':   'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'wps': 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape',
    'a':   'http://schemas.openxmlformats.org/drawingml/2006/main',
    'wp':  'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
}


def color_close(hex_str, target_hex, tolerance=20):
    """Check if a hex color string is close to a target color within tolerance."""
    try:
        r1 = int(hex_str[0:2], 16)
        g1 = int(hex_str[2:4], 16)
        b1 = int(hex_str[4:6], 16)
        r2 = int(target_hex[0:2], 16)
        g2 = int(target_hex[2:4], 16)
        b2 = int(target_hex[4:6], 16)
        dist = ((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2) ** 0.5
        return dist <= tolerance
    except Exception:
        return False


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the document
    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find all drawings in the document body
    body = doc.element.body
    drawings = body.findall('.//w:drawing', NS)
    if not drawings:
        print("FAIL: No drawing/shape found in document")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Use the first (and expected only) drawing
    drawing = drawings[0]

    # Locate the wps:spPr element which holds fill and line properties
    sp_pr = drawing.find('.//wps:spPr', NS)
    if sp_pr is None:
        print("FAIL: Cannot locate shape properties (wps:spPr) in drawing")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # ------------------------------------------------------------------
    # Component 1: Rectangle has no fill (transparent) — 0.30 pts
    # Initial state has a:solidFill; golden state has a:noFill
    # ------------------------------------------------------------------
    try:
        no_fill_elem = sp_pr.find('a:noFill', NS)
        solid_fill_elem = sp_pr.find('a:solidFill', NS)
        has_no_fill = (no_fill_elem is not None) and (solid_fill_elem is None)
        if has_no_fill:
            print("PASS: Component 1 — Rectangle has no fill (transparent) (0.30 pts)")
            total_score += 0.30
        else:
            fill_detail = "solidFill present" if solid_fill_elem is not None else "noFill element missing"
            print(f"FAIL: Component 1 — Rectangle fill is not transparent ({fill_detail})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ------------------------------------------------------------------
    # Component 2: Border is 3pt solid dark orange (#E65100) — 0.30 pts
    # 3pt in EMU = 3 * 12700 = 38100; ln w="38100" with srgbClr val="E65100"
    # We allow a small tolerance on the border width (±12700 = ±1pt)
    # ------------------------------------------------------------------
    try:
        ln_elem = sp_pr.find('a:ln', NS)
        if ln_elem is None:
            print("FAIL: Component 2 — No border (a:ln) element found")
        else:
            # Check width (w attribute): 38100 EMU = 3pt
            w_attr = ln_elem.get('w')
            border_width_ok = False
            if w_attr is not None:
                w_val = int(w_attr)
                # Allow tolerance: 38100 ± 12700 (i.e., 2pt to 4pt range)
                border_width_ok = abs(w_val - 38100) <= 12700
                print(f"  Border width: {w_val} EMU ({'OK' if border_width_ok else 'FAIL, expected ~38100'})")

            # Check color
            border_color_ok = False
            ln_solid_fill = ln_elem.find('a:solidFill', NS)
            if ln_solid_fill is not None:
                srgb_clr = ln_solid_fill.find('a:srgbClr', NS)
                if srgb_clr is not None:
                    clr_val = srgb_clr.get('val', '').upper()
                    border_color_ok = color_close(clr_val, 'E65100', tolerance=20)
                    print(f"  Border color: #{clr_val} ({'OK' if border_color_ok else 'FAIL, expected ~#E65100'})")

            if border_width_ok and border_color_ok:
                print("PASS: Component 2 — Border is ~3pt solid dark orange (#E65100) (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 2 — Border check failed (width_ok={border_width_ok}, color_ok={border_color_ok})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ------------------------------------------------------------------
    # Component 3: Shape contains text 'ATTENTION' — 0.20 pts
    # Golden state has a wps:txbx with w:t containing 'ATTENTION'
    # ------------------------------------------------------------------
    try:
        txbx = drawing.find('.//wps:txbx', NS)
        attention_found = False
        if txbx is not None:
            t_elements = txbx.findall('.//w:t', NS)
            full_text = ''.join(t.text or '' for t in t_elements).strip()
            attention_found = 'ATTENTION' in full_text.upper()
            if attention_found:
                print(f"PASS: Component 3 — Text 'ATTENTION' found in shape (text='{full_text}') (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — 'ATTENTION' not found; shape text='{full_text}'")
        else:
            print("FAIL: Component 3 — No textbox (wps:txbx) found in shape")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ------------------------------------------------------------------
    # Component 4: 'ATTENTION' text is bold, 16pt, dark orange (#E65100) — 0.20 pts
    # In XML: w:b present, w:sz val="32" (half-points → 16pt), w:color val="E65100"
    # ------------------------------------------------------------------
    try:
        txbx = drawing.find('.//wps:txbx', NS)
        if txbx is None:
            print("FAIL: Component 4 — No textbox for formatting check")
        else:
            # Find run properties of the run containing 'ATTENTION'
            runs = txbx.findall('.//w:r', NS)
            formatting_ok = False
            for run in runs:
                t_elem = run.find('w:t', NS)
                if t_elem is None or 'ATTENTION' not in (t_elem.text or '').upper():
                    continue
                rpr = run.find('w:rPr', NS)
                if rpr is None:
                    print("FAIL: Component 4 — Run has no rPr (formatting properties)")
                    break

                # Check bold: w:b element present
                bold_elem = rpr.find('w:b', NS)
                is_bold = bold_elem is not None
                print(f"  Bold: {is_bold}")

                # Check font size: w:sz val="32" → 16pt (half-points)
                sz_elem = rpr.find('w:sz', NS)
                is_16pt = False
                if sz_elem is not None:
                    sz_val = sz_elem.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val') or sz_elem.get('w:val')
                    # lxml strips ns prefix; try direct attrib
                    sz_val_direct = sz_elem.attrib.get(
                        '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val'
                    )
                    if sz_val_direct is None:
                        # Try without namespace (some serializations)
                        sz_val_direct = sz_elem.attrib.get('w:val')
                    # Fallback: iterate attribs
                    if sz_val_direct is None:
                        for k, v in sz_elem.attrib.items():
                            if 'val' in k:
                                sz_val_direct = v
                                break
                    if sz_val_direct is not None:
                        is_16pt = abs(int(sz_val_direct) - 32) <= 2  # 32 half-pts = 16pt, tolerance ±1pt
                        print(f"  Font size: {sz_val_direct} half-pts ({'OK ~16pt' if is_16pt else 'FAIL'})")
                    else:
                        print("  Font size: could not read sz val")
                else:
                    print("  Font size: w:sz element not found")

                # Check color: w:color val="E65100"
                color_elem = rpr.find('w:color', NS)
                is_orange = False
                if color_elem is not None:
                    clr_val_direct = None
                    for k, v in color_elem.attrib.items():
                        if 'val' in k:
                            clr_val_direct = v
                            break
                    if clr_val_direct:
                        is_orange = color_close(clr_val_direct.upper(), 'E65100', tolerance=20)
                        print(f"  Text color: #{clr_val_direct.upper()} ({'OK' if is_orange else 'FAIL, expected ~#E65100'})")
                    else:
                        print("  Text color: w:color val not found")
                else:
                    print("  Text color: w:color element not found")

                formatting_ok = is_bold and is_16pt and is_orange
                break

            if formatting_ok:
                print("PASS: Component 4 — 'ATTENTION' is bold, 16pt, dark orange (#E65100) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 — Formatting check failed (bold={is_bold}, 16pt={is_16pt}, orange={is_orange})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

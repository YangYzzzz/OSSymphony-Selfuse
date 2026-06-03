"""
Reward Script: Create a text frame with 3 columns, border, padding, and content
Task ID: writer_obj_070
Domain: libreoffice_writer
Scoring:
  Component 1 (0.2): Text frame/drawing element exists in document
  Component 2 (0.2): Frame position (X~2cm, Y~3cm) and size (13cm x 5cm)
  Component 3 (0.2): Frame border is 2pt solid #424242 with 0.3cm internal padding
  Component 4 (0.2): 3 equal-width columns with vertical separator and ~0.4cm spacing
  Component 5 (0.2): Text content present: 'Column 1 content', 'Column 2 content', 'Column 3 content'
"""

import os
import lxml.etree as etree

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_obj_070'

# Namespace definitions for XML parsing
NS = {
    'w':   'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'wp':  'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'a':   'http://schemas.openxmlformats.org/drawingml/2006/main',
    'wps': 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape',
}

# Conversion constants
EMU_PER_CM = 360000    # 914400 EMU/inch / 2.54 cm/inch
TWIPS_PER_CM = 566.93  # 1440 twips/inch / 2.54 cm/inch
EMU_PER_PT = 12700     # 12700 EMU per point

# Tolerance for approximate comparisons
EMU_TOL = 36000        # 0.1 cm tolerance in EMU
TWIPS_TOL = 57         # ~0.1 cm tolerance in twips


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

    # -----------------------------------------------------------------------
    # Component 1: Text frame (drawing element) exists in document (0.2 points)
    # The task requires creating a new text frame on page 1.
    # Initial env has 0 drawings; golden env should have 1.
    # -----------------------------------------------------------------------
    drawing = None
    try:
        drawings = doc.element.body.findall('.//' + '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}drawing')
        if drawings and len(drawings) >= 1:
            drawing = drawings[0]
            print(f"PASS: Component 1 — Text frame drawing element found ({len(drawings)} drawing(s)) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — No drawing/text frame element found in document")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if drawing is None:
        # No frame found; remaining components all fail
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # -----------------------------------------------------------------------
    # Component 2: Frame position X~2cm, Y~3cm and size ~13cm x 5cm (0.2 points)
    # Expected: posOffset X=720000 EMU (~2cm), Y=1080000 EMU (~3cm)
    #           extent cx=4680000 EMU (~13cm), cy=1800000 EMU (~5cm)
    # -----------------------------------------------------------------------
    try:
        pos_h_elem = drawing.find('.//wp:positionH/wp:posOffset', NS)
        pos_v_elem = drawing.find('.//wp:positionV/wp:posOffset', NS)
        extent_elem = drawing.find('.//wp:extent', NS)

        pos_ok = False
        size_ok = False

        if pos_h_elem is not None and pos_v_elem is not None:
            x_emu = int(pos_h_elem.text)
            y_emu = int(pos_v_elem.text)
            x_cm = x_emu / EMU_PER_CM
            y_cm = y_emu / EMU_PER_CM
            x_ok = abs(x_emu - 720000) <= EMU_TOL
            y_ok = abs(y_emu - 1080000) <= EMU_TOL
            pos_ok = x_ok and y_ok
            print(f"  Position: X={x_cm:.2f}cm (exp 2.00cm, ok={x_ok}), Y={y_cm:.2f}cm (exp 3.00cm, ok={y_ok})")
        else:
            print(f"  Position elements not found in anchor")

        if extent_elem is not None:
            cx_emu = int(extent_elem.get('cx'))
            cy_emu = int(extent_elem.get('cy'))
            w_cm = cx_emu / EMU_PER_CM
            h_cm = cy_emu / EMU_PER_CM
            w_ok = abs(cx_emu - 4680000) <= EMU_TOL
            h_ok = abs(cy_emu - 1800000) <= EMU_TOL
            size_ok = w_ok and h_ok
            print(f"  Size: W={w_cm:.2f}cm (exp 13.00cm, ok={w_ok}), H={h_cm:.2f}cm (exp 5.00cm, ok={h_ok})")
        else:
            print(f"  Extent element not found")

        if pos_ok and size_ok:
            print(f"PASS: Component 2 — Frame position X=2cm,Y=3cm and size 13cmx5cm verified (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — Position or size mismatch (pos_ok={pos_ok}, size_ok={size_ok})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: Frame border 2pt solid #424242 with 0.3cm internal padding (0.2 points)
    # Expected: a:ln w="25400" (2pt = 25400 EMU) with srgbClr val="424242"
    #           inset="108000 108000 108000 108000" (0.3cm = 108000 EMU each side)
    # -----------------------------------------------------------------------
    try:
        border_ok = False
        padding_ok = False

        # Check border line element
        ln_elem = drawing.find('.//wps:spPr/a:ln', NS)
        if ln_elem is not None:
            ln_w = int(ln_elem.get('w', 0))
            color_elem = ln_elem.find('a:solidFill/a:srgbClr', NS)
            color_val = color_elem.get('val', '').lower() if color_elem is not None else ''
            w_pt = ln_w / EMU_PER_PT
            w_ok = abs(ln_w - 25400) <= 1270   # tolerance: ±0.1pt
            color_ok = color_val == '424242'
            border_ok = w_ok and color_ok
            print(f"  Border: width={w_pt:.2f}pt (exp 2pt, ok={w_ok}), color=#{color_val} (exp #424242, ok={color_ok})")
        else:
            print(f"  Border line element (a:ln) not found in spPr")

        # Check internal padding (inset attribute on txbx)
        txbx_elem = drawing.find('.//wps:txbx', NS)
        if txbx_elem is not None:
            inset = txbx_elem.get('inset', '')
            # inset format: "lIns tIns rIns bIns" in EMU separated by spaces
            if inset:
                parts = inset.split()
                if len(parts) >= 4:
                    inset_vals = [int(p) for p in parts]
                    # Check all sides are ~108000 EMU = 0.3cm
                    padding_ok = all(abs(v - 108000) <= EMU_TOL for v in inset_vals)
                    inset_cms = [v / EMU_PER_CM for v in inset_vals]
                    print(f"  Inset values: {[f'{c:.3f}cm' for c in inset_cms]} (exp 0.300cm each, ok={padding_ok})")
                else:
                    print(f"  Inset attribute has unexpected format: {inset!r}")
            else:
                # Check bodyPr lIns/tIns/rIns/bIns attributes as fallback
                body_pr = drawing.find('.//wps:bodyPr', NS)
                if body_pr is not None:
                    l = int(body_pr.get('lIns', 0))
                    t = int(body_pr.get('tIns', 0))
                    r = int(body_pr.get('rIns', 0))
                    b = int(body_pr.get('bIns', 0))
                    padding_ok = all(abs(v - 108000) <= EMU_TOL for v in [l, t, r, b])
                    print(f"  bodyPr inset: l={l/EMU_PER_CM:.3f}cm, t={t/EMU_PER_CM:.3f}cm, r={r/EMU_PER_CM:.3f}cm, b={b/EMU_PER_CM:.3f}cm (ok={padding_ok})")
                else:
                    print(f"  bodyPr element not found; cannot verify padding")
        else:
            print(f"  txbx element not found")

        if border_ok and padding_ok:
            print(f"PASS: Component 3 — Frame border 2pt #424242 and 0.3cm padding verified (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Border or padding mismatch (border_ok={border_ok}, padding_ok={padding_ok})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -----------------------------------------------------------------------
    # Component 4: 3 equal-width columns with vertical separator, ~0.4cm spacing (0.2 points)
    # Expected in w:sectPr inside txbxContent:
    #   w:cols w:num="3" w:equalWidth="1" w:sep="1" w:space="~227" (0.4cm)
    # -----------------------------------------------------------------------
    try:
        cols_elem = drawing.find('.//' + '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}cols')
        if cols_elem is not None:
            num_cols = int(cols_elem.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}num', 0))
            equal_width = cols_elem.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}equalWidth', '0')
            sep = cols_elem.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}sep', '0')
            space_twips = int(cols_elem.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}space', 0))
            space_cm = space_twips / TWIPS_PER_CM

            num_ok = num_cols == 3
            equal_ok = equal_width in ('1', 'true')
            sep_ok = sep in ('1', 'true')
            # 0.4cm ≈ 226-227 twips; allow ±57 twips (~0.1cm)
            space_ok = abs(space_twips - 227) <= TWIPS_TOL or abs(space_twips - 226) <= TWIPS_TOL

            print(f"  Columns: num={num_cols} (ok={num_ok}), equalWidth={equal_width} (ok={equal_ok}), sep={sep} (ok={sep_ok}), space={space_twips} twips={space_cm:.3f}cm (ok={space_ok})")

            if num_ok and equal_ok and sep_ok and space_ok:
                print(f"PASS: Component 4 — 3 equal-width columns with separator and ~0.4cm spacing (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 — Column config mismatch")
        else:
            print(f"FAIL: Component 4 — w:cols element not found in textbox sectPr")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # -----------------------------------------------------------------------
    # Component 5: Text content present in text frame (0.2 points)
    # Expected: 'Column 1 content', 'Column 2 content', 'Column 3 content' in txbxContent
    # -----------------------------------------------------------------------
    try:
        txbx_elem = drawing.find('.//wps:txbx', NS)
        if txbx_elem is not None:
            # Gather all text in txbxContent
            all_text = []
            for t_elem in txbx_elem.findall('.//' + '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'):
                if t_elem.text:
                    all_text.append(t_elem.text.strip())
            full_text = ' '.join(all_text).lower()
            print(f"  Textbox text: {all_text}")

            has_col1 = 'column 1 content' in full_text
            has_col2 = 'column 2 content' in full_text
            has_col3 = 'column 3 content' in full_text

            print(f"  'column 1 content' present: {has_col1}")
            print(f"  'column 2 content' present: {has_col2}")
            print(f"  'column 3 content' present: {has_col3}")

            if has_col1 and has_col2 and has_col3:
                print(f"PASS: Component 5 — All 3 column text strings found in frame (0.2 pts)")
                total_score += 0.2
            else:
                missing = []
                if not has_col1: missing.append("'Column 1 content'")
                if not has_col2: missing.append("'Column 2 content'")
                if not has_col3: missing.append("'Column 3 content'")
                print(f"FAIL: Component 5 — Missing text: {', '.join(missing)}")
        else:
            print(f"FAIL: Component 5 — txbx element not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/multi_column.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

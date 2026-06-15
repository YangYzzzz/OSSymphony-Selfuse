"""
Reward Script: Create an info box on page 2 using a text frame with specific formatting
Task ID: writer_obj_057
Domain: libreoffice_writer
Scoring:
  - Component 1: Text frame (drawing) exists in document (0.20 pts)
  - Component 2: Background color is #FFF3E0 (light orange) (0.15 pts)
  - Component 3: Left-only border at 4pt solid #E65100 (dark orange), no other borders (0.20 pts)
  - Component 4: Position X~2cm, Y~8cm and size ~13cm x 6cm (0.20 pts)
  - Component 5: Internal padding 0.4cm all sides (0.10 pts)
  - Component 6: Text content "Note:" bold + rest in regular weight (0.15 pts)
"""

import os
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_obj_057'

# EMU (English Metric Units) conversion helpers
# 1 cm = 360000 EMU
CM_TO_EMU = 360000
TOLERANCE = 0.15  # 15% relative tolerance for position/size checks


def emu_to_cm(emu):
    return emu / CM_TO_EMU


def approx_equal(actual_emu, expected_cm, tolerance_cm=0.5):
    """Check if EMU value is within tolerance of expected cm value."""
    actual_cm = emu_to_cm(actual_emu)
    return abs(actual_cm - expected_cm) <= tolerance_cm


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
    except ImportError:
        print("CRITICAL: python-docx not installed")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Namespaces for XML parsing
    NS = {
        'w':   'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
        'wp':  'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
        'a':   'http://schemas.openxmlformats.org/drawingml/2006/main',
        'wps': 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape',
        'mc':  'http://schemas.openxmlformats.org/markup-compatibility/2006',
    }

    body = doc.element.body

    # Locate the drawing element (text frame)
    drawing_elem = None
    for elem in body.iter():
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        if tag == 'drawing':
            # Confirm it contains a textbox (txbx attribute)
            inner_xml = etree.tostring(elem).decode()
            if 'txbx' in inner_xml or 'txbxContent' in inner_xml:
                drawing_elem = elem
                break

    # ------------------------------------------------------------
    # Component 1: Text frame (drawing/textbox) exists (0.20 pts)
    # ------------------------------------------------------------
    try:
        if drawing_elem is not None:
            print("PASS: Component 1 — Text frame (drawing+txbx) found in document (0.20 pts)")
            total_score += 0.20
        else:
            print("FAIL: Component 1 — No text frame (drawing with txbx) found in document")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if drawing_elem is None:
        # No point continuing without a text frame
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    drawing_xml = etree.tostring(drawing_elem).decode()

    # ------------------------------------------------------------
    # Component 2: Background color is #FFF3E0 (0.15 pts)
    # ------------------------------------------------------------
    try:
        # Look for solidFill with srgbClr val="FFF3E0"
        fill_elems = drawing_elem.findall(
            './/{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr'
        )
        bg_color_found = False
        for fe in fill_elems:
            val = fe.get('val', '').upper()
            if val == 'FFF3E0':
                bg_color_found = True
                break
        if bg_color_found:
            print("PASS: Component 2 — Background color #FFF3E0 (light orange) verified (0.15 pts)")
            total_score += 0.15
        else:
            found_colors = [fe.get('val', '') for fe in fill_elems]
            print(f"FAIL: Component 2 — Expected background #FFF3E0, found: {found_colors}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ------------------------------------------------------------
    # Component 3: Left-only border 4pt solid #E65100, no other borders (0.20 pts)
    # ------------------------------------------------------------
    try:
        # The left border is applied as paragraph border inside txbxContent
        # <w:pBdr><w:left w:val="single" w:sz="32" w:color="E65100"/></w:pBdr>
        # sz=32 means 32 half-points = 16pt? Actually in OOXML w:sz for borders is in 1/8pt, so 32/8=4pt
        left_borders = drawing_elem.findall(
            './/{http://schemas.openxmlformats.org/wordprocessingml/2006/main}left'
        )
        # Also check for shape-level border (a:ln with noFill = no border)
        ln_elems = drawing_elem.findall(
            './/{http://schemas.openxmlformats.org/drawingml/2006/main}ln'
        )

        # Check paragraph left border
        has_left_border = False
        left_border_correct = False
        for lb in left_borders:
            color = lb.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}color', '').upper()
            val = lb.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val', '')
            sz = lb.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}sz', '0')
            if color == 'E65100':
                has_left_border = True
                # sz=32 means 4pt (in 1/8pt units: 32/8=4)
                sz_pt = int(sz) / 8 if sz.isdigit() else 0
                if val == 'single' and abs(sz_pt - 4.0) < 0.5:
                    left_border_correct = True
                    print(f"PASS: Left border details — val={val}, sz={sz}(={sz_pt}pt), color={color}")

        # Check that shape-level border has noFill (no outer box border)
        shape_no_border = False
        for ln_elem in ln_elems:
            no_fill = ln_elem.find(
                '{http://schemas.openxmlformats.org/drawingml/2006/main}noFill'
            )
            if no_fill is not None:
                shape_no_border = True
                break

        # Check no top/right/bottom paragraph borders
        top_borders = drawing_elem.findall(
            './/{http://schemas.openxmlformats.org/wordprocessingml/2006/main}top'
        )
        right_borders = drawing_elem.findall(
            './/{http://schemas.openxmlformats.org/wordprocessingml/2006/main}right'
        )
        bottom_borders = drawing_elem.findall(
            './/{http://schemas.openxmlformats.org/wordprocessingml/2006/main}bottom'
        )
        # Filter: only count actual border elements inside pBdr context
        pBdr_ns = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pBdr'
        has_top = any(
            elem.getparent() is not None and elem.getparent().tag == pBdr_ns
            for elem in top_borders
        )
        has_right = any(
            elem.getparent() is not None and elem.getparent().tag == pBdr_ns
            for elem in right_borders
        )
        has_bottom = any(
            elem.getparent() is not None and elem.getparent().tag == pBdr_ns
            for elem in bottom_borders
        )
        no_other_borders = not has_top and not has_right and not has_bottom

        if left_border_correct and no_other_borders and shape_no_border:
            print("PASS: Component 3 — Left-only border 4pt solid #E65100 verified, no other borders (0.20 pts)")
            total_score += 0.20
        elif left_border_correct and no_other_borders:
            print("PASS: Component 3 — Left border correct, no other paragraph borders (0.20 pts)")
            total_score += 0.20
        elif has_left_border and not left_border_correct:
            print(f"FAIL: Component 3 — Left border found but incorrect specs. left_border_correct={left_border_correct}, no_other_borders={no_other_borders}")
        else:
            print(f"FAIL: Component 3 — Left border E65100 not found or other borders present. has_left={has_left_border}, no_other={no_other_borders}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ------------------------------------------------------------
    # Component 4: Position X~2cm, Y~8cm and size ~13cm x 6cm (0.20 pts)
    # ------------------------------------------------------------
    try:
        # Position from anchor
        pos_h_elem = drawing_elem.find(
            './/{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}positionH/'
            '{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}posOffset'
        )
        pos_v_elem = drawing_elem.find(
            './/{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}positionV/'
            '{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}posOffset'
        )
        extent_elem = drawing_elem.find(
            './/{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}extent'
        )

        pos_x_ok = False
        pos_y_ok = False
        size_ok = False
        details = []

        if pos_h_elem is not None:
            pos_x_emu = int(pos_h_elem.text)
            pos_x_cm = emu_to_cm(pos_x_emu)
            # Expected: 2cm = 720000 EMU
            pos_x_ok = approx_equal(pos_x_emu, 2.0, tolerance_cm=0.5)
            details.append(f"X={pos_x_cm:.2f}cm (expected ~2cm, ok={pos_x_ok})")
        else:
            details.append("X=not found")

        if pos_v_elem is not None:
            pos_y_emu = int(pos_v_elem.text)
            pos_y_cm = emu_to_cm(pos_y_emu)
            # Expected: 8cm = 2880000 EMU
            pos_y_ok = approx_equal(pos_y_emu, 8.0, tolerance_cm=0.5)
            details.append(f"Y={pos_y_cm:.2f}cm (expected ~8cm, ok={pos_y_ok})")
        else:
            details.append("Y=not found")

        if extent_elem is not None:
            cx = int(extent_elem.get('cx', '0'))
            cy = int(extent_elem.get('cy', '0'))
            w_cm = emu_to_cm(cx)
            h_cm = emu_to_cm(cy)
            # Expected: 13cm x 6cm
            w_ok = approx_equal(cx, 13.0, tolerance_cm=0.5)
            h_ok = approx_equal(cy, 6.0, tolerance_cm=0.5)
            size_ok = w_ok and h_ok
            details.append(f"width={w_cm:.2f}cm (expected ~13cm, ok={w_ok}), height={h_cm:.2f}cm (expected ~6cm, ok={h_ok})")
        else:
            details.append("extent=not found")

        detail_str = "; ".join(details)
        if pos_x_ok and pos_y_ok and size_ok:
            print(f"PASS: Component 4 — Position and size verified: {detail_str} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — Position/size mismatch: {detail_str}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ------------------------------------------------------------
    # Component 5: Internal padding 0.4cm (~144000 EMU) all sides (0.10 pts)
    # ------------------------------------------------------------
    try:
        # <wps:bodyPr lIns="144000" tIns="144000" rIns="144000" bIns="144000"/>
        body_pr = drawing_elem.find(
            './/{http://schemas.microsoft.com/office/word/2010/wordprocessingShape}bodyPr'
        )
        if body_pr is not None:
            # Expected: 0.4cm = 144000 EMU
            expected_ins = 144000
            tolerance_emu = 54000  # ~0.15cm tolerance
            l_ins = int(body_pr.get('lIns', '0'))
            t_ins = int(body_pr.get('tIns', '0'))
            r_ins = int(body_pr.get('rIns', '0'))
            b_ins = int(body_pr.get('bIns', '0'))
            l_cm = emu_to_cm(l_ins)
            t_cm = emu_to_cm(t_ins)
            r_cm = emu_to_cm(r_ins)
            b_cm = emu_to_cm(b_ins)
            padding_ok = all(
                abs(v - expected_ins) <= tolerance_emu
                for v in [l_ins, t_ins, r_ins, b_ins]
            )
            if padding_ok:
                print(f"PASS: Component 5 — Padding 0.4cm all sides: L={l_cm:.3f} T={t_cm:.3f} R={r_cm:.3f} B={b_cm:.3f} cm (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — Padding mismatch: L={l_cm:.3f} T={t_cm:.3f} R={r_cm:.3f} B={b_cm:.3f} cm (expected 0.4cm each)")
        else:
            print("FAIL: Component 5 — bodyPr element not found; cannot verify padding")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # ------------------------------------------------------------
    # Component 6: Text content with correct formatting (0.15 pts)
    # "Note:" in bold, "Please review..." in regular weight
    # ------------------------------------------------------------
    try:
        txbx_content = drawing_elem.find(
            './/{http://schemas.openxmlformats.org/wordprocessingml/2006/main}txbxContent'
        )
        if txbx_content is None:
            print("FAIL: Component 6 — txbxContent not found")
        else:
            # Collect all runs
            runs = txbx_content.findall(
                './/{http://schemas.openxmlformats.org/wordprocessingml/2006/main}r'
            )
            run_texts = []
            run_bold = []
            for r in runs:
                t_elem = r.find(
                    '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'
                )
                rpr = r.find(
                    '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rPr'
                )
                text = t_elem.text if t_elem is not None else ''
                bold = rpr is not None and rpr.find(
                    '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}b'
                ) is not None
                run_texts.append(text)
                run_bold.append(bold)

            full_text = ''.join(run_texts)
            has_note = 'Note:' in full_text
            has_body = 'Please review all attached documents before the meeting' in full_text

            # Find bold run with "Note:" and non-bold run with the body text
            note_bold = False
            body_regular = False
            for i, (text, bold) in enumerate(zip(run_texts, run_bold)):
                if 'Note:' in text and bold:
                    note_bold = True
                if 'Please review' in text and not bold:
                    body_regular = True

            details = (
                f"full_text={full_text[:80]!r}, "
                f"has_note={has_note}, has_body={has_body}, "
                f"note_bold={note_bold}, body_regular={body_regular}"
            )

            if has_note and has_body and note_bold and body_regular:
                print(f"PASS: Component 6 — Text content and formatting verified: {details} (0.15 pts)")
                total_score += 0.15
            elif has_note and has_body:
                print(f"FAIL: Component 6 — Text present but formatting incorrect: {details}")
            else:
                print(f"FAIL: Component 6 — Text content missing or incorrect: {details}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Desktop/meeting_prep.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

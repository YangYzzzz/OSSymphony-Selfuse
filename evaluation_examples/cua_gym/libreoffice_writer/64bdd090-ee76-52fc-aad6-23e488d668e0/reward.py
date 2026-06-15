"""
Reward Script: Insert three text frames on page 1 as a three-column callout section
Task ID: writer_obj_063
Domain: libreoffice_writer
Scoring:
  - Component 1: 3 text boxes (anchors) exist in document (0.20)
  - Component 2: Correct heading text ('Feature 1/2/3') with bold formatting (0.25)
  - Component 3: Correct size (4.5cm x 6cm) and position (Y=12cm, X=1.5/7/12.5cm) (0.25)
  - Component 4: Light blue background (#E3F2FD) and top-only border (#1565C0, 1pt) (0.20)
  - Component 5: Internal padding ~0.3cm on all sides (0.10)
Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_obj_063'

# EMU conversion constants
EMU_PER_CM = 914400 / 2.54  # 360000 EMU per cm

# Tolerances (±10% for position/size)
SIZE_TOL_EMU = 72000   # ~0.2cm tolerance
POS_TOL_EMU = 72000    # ~0.2cm tolerance
PAD_TOL_EMU = 36000    # ~0.1cm tolerance


def emu_to_cm(emu):
    return emu / EMU_PER_CM


def cm_to_emu(cm):
    return int(cm * EMU_PER_CM)


def verify_task(file_path):
    """
    Verify that three text boxes were correctly inserted as a callout section.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        from lxml import etree
    except ImportError as e:
        print(f"CRITICAL: Missing dependency: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    body = doc.element.body

    # Namespace shortcuts
    WP_NS = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
    A_NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'
    WPS_NS = 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape'
    W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

    # Gather all anchor elements (floating text boxes)
    anchors = body.findall(f'.//{{{WP_NS}}}anchor')

    # -------------------------------------------------------------------------
    # Component 1: Exactly 3 text box anchors exist (0.20 points)
    # This FAILS on initial_env (0 anchors) and PASSES on golden_env (3 anchors)
    # -------------------------------------------------------------------------
    try:
        # Confirm they are text boxes (contain wps:txbx)
        txbx_anchors = [
            a for a in anchors
            if a.find(f'.//{{{WPS_NS}}}txbx') is not None
        ]
        count = len(txbx_anchors)
        if count == 3:
            print(f"PASS: Component 1 — exactly 3 text box anchors found (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — expected 3 text box anchors, found {count}")
            # If 0 anchors, no further checks make sense
            if count == 0:
                print(f"\nScore: {total_score}/1.0")
                print(f"REWARD: {total_score}")
                return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        txbx_anchors = []

    # -------------------------------------------------------------------------
    # Component 2: Correct heading text ('Feature 1/2/3') in bold (0.25 points)
    # Each text box should have the correct heading and it should be bold.
    # -------------------------------------------------------------------------
    try:
        expected_texts = ['Feature 1', 'Feature 2', 'Feature 3']
        text_checks = []

        for idx, anchor in enumerate(txbx_anchors[:3]):
            # Extract text from the text box
            t_elements = anchor.findall(f'.//{{{W_NS}}}t')
            txbx_text = ''.join(t.text or '' for t in t_elements).strip()

            # Check bold formatting
            r_elements = anchor.findall(f'.//{{{W_NS}}}r')
            is_bold = False
            for r in r_elements:
                rPr = r.find(f'{{{W_NS}}}rPr')
                if rPr is not None:
                    b_elem = rPr.find(f'{{{W_NS}}}b')
                    if b_elem is not None:
                        is_bold = True
                        break

            expected = expected_texts[idx] if idx < len(expected_texts) else f'Feature {idx+1}'
            text_match = txbx_text == expected
            text_checks.append((text_match, is_bold, txbx_text, expected))

        # Sort text boxes by X position to ensure correct order matching
        # Re-extract with position for ordering
        positioned = []
        for anchor in txbx_anchors[:3]:
            posH = anchor.find(f'{{{WP_NS}}}positionH')
            x_emu = 0
            if posH is not None:
                posOff = posH.find(f'{{{WP_NS}}}posOffset')
                if posOff is not None and posOff.text:
                    x_emu = int(posOff.text)
            # Get text
            t_elements = anchor.findall(f'.//{{{W_NS}}}t')
            txbx_text = ''.join(t.text or '' for t in t_elements).strip()
            # Get bold
            r_elements = anchor.findall(f'.//{{{W_NS}}}r')
            is_bold = False
            for r in r_elements:
                rPr = r.find(f'{{{W_NS}}}rPr')
                if rPr is not None:
                    b_elem = rPr.find(f'{{{W_NS}}}b')
                    if b_elem is not None:
                        is_bold = True
                        break
            positioned.append((x_emu, txbx_text, is_bold))

        # Sort by X position
        positioned.sort(key=lambda t: t[0])

        # Verify text and bold for sorted boxes
        all_text_ok = True
        all_bold_ok = True
        for i, (x_emu, txbx_text, is_bold) in enumerate(positioned):
            expected = expected_texts[i]
            if txbx_text != expected:
                print(f"FAIL: Component 2 — box {i+1}: expected '{expected}', found '{txbx_text}'")
                all_text_ok = False
            if not is_bold:
                print(f"FAIL: Component 2 — box {i+1} '{txbx_text}': heading not bold")
                all_bold_ok = False

        if all_text_ok and all_bold_ok:
            print(f"PASS: Component 2 — all 3 headings ('Feature 1/2/3') present and bold (0.25 pts)")
            total_score += 0.25
        elif all_text_ok:
            # Partial: correct text but not all bold
            print(f"PASS (partial): Component 2 — correct headings but some not bold (0.10 pts)")
            total_score += 0.10
        elif all_bold_ok:
            # Partial: bold but wrong text
            print(f"FAIL: Component 2 — bold formatting found but heading text incorrect")
        else:
            print(f"FAIL: Component 2 — heading text and/or bold formatting incorrect")

    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Component 3: Correct size (4.5cm x 6cm) and positions (0.25 points)
    # Y=12cm for all, X=1.5cm/7cm/12.5cm left-to-right
    # -------------------------------------------------------------------------
    try:
        # Expected positions in EMU (sorted left-to-right by X)
        expected_x_cm = [1.5, 7.0, 12.5]
        expected_y_cm = 12.0
        expected_w_cm = 4.5
        expected_h_cm = 6.0

        expected_x_emu = [cm_to_emu(x) for x in expected_x_cm]
        expected_y_emu = cm_to_emu(expected_y_cm)
        expected_w_emu = cm_to_emu(expected_w_cm)
        expected_h_emu = cm_to_emu(expected_h_cm)

        # Gather position + size info for all text box anchors
        box_info = []
        for anchor in txbx_anchors:
            posH = anchor.find(f'{{{WP_NS}}}positionH')
            posV = anchor.find(f'{{{WP_NS}}}positionV')
            extent = anchor.find(f'{{{WP_NS}}}extent')

            x_emu = 0
            y_emu = 0
            w_emu = 0
            h_emu = 0

            if posH is not None:
                posOff = posH.find(f'{{{WP_NS}}}posOffset')
                if posOff is not None and posOff.text:
                    x_emu = int(posOff.text)
            if posV is not None:
                posOff = posV.find(f'{{{WP_NS}}}posOffset')
                if posOff is not None and posOff.text:
                    y_emu = int(posOff.text)
            if extent is not None:
                cx = extent.get('cx')
                cy = extent.get('cy')
                if cx:
                    w_emu = int(cx)
                if cy:
                    h_emu = int(cy)

            box_info.append((x_emu, y_emu, w_emu, h_emu))

        # Sort by X position
        box_info.sort(key=lambda t: t[0])

        size_ok = True
        pos_ok = True
        pos_passes = 0

        for i, (x_emu, y_emu, w_emu, h_emu) in enumerate(box_info):
            # Check size
            w_ok = abs(w_emu - expected_w_emu) <= SIZE_TOL_EMU
            h_ok = abs(h_emu - expected_h_emu) <= SIZE_TOL_EMU
            if not w_ok:
                print(f"FAIL: Component 3 — box {i+1} width: expected {expected_w_cm}cm ({expected_w_emu} EMU), "
                      f"found {emu_to_cm(w_emu):.3f}cm ({w_emu} EMU)")
                size_ok = False
            if not h_ok:
                print(f"FAIL: Component 3 — box {i+1} height: expected {expected_h_cm}cm ({expected_h_emu} EMU), "
                      f"found {emu_to_cm(h_emu):.3f}cm ({h_emu} EMU)")
                size_ok = False

            # Check position
            x_ok = abs(x_emu - expected_x_emu[i]) <= POS_TOL_EMU
            y_ok = abs(y_emu - expected_y_emu) <= POS_TOL_EMU
            if x_ok and y_ok:
                pos_passes += 1
            else:
                if not x_ok:
                    print(f"FAIL: Component 3 — box {i+1} X: expected {expected_x_cm[i]}cm ({expected_x_emu[i]} EMU), "
                          f"found {emu_to_cm(x_emu):.3f}cm ({x_emu} EMU)")
                    pos_ok = False
                if not y_ok:
                    print(f"FAIL: Component 3 — box {i+1} Y: expected {expected_y_cm}cm ({expected_y_emu} EMU), "
                          f"found {emu_to_cm(y_emu):.3f}cm ({y_emu} EMU)")
                    pos_ok = False

        if size_ok and pos_ok:
            print(f"PASS: Component 3 — all 3 boxes have correct size (4.5cm x 6cm) "
                  f"and positions (X=1.5/7/12.5cm, Y=12cm) (0.25 pts)")
            total_score += 0.25
        elif size_ok:
            print(f"PASS (partial): Component 3 — correct sizes but position issues ({pos_passes}/3 positions ok) (0.10 pts)")
            total_score += 0.10
        elif pos_ok:
            print(f"PASS (partial): Component 3 — correct positions but size issues (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 — size and/or position incorrect for text boxes")

    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -------------------------------------------------------------------------
    # Component 4: Light blue background (#E3F2FD) and top-only border
    #              (#1565C0, 1pt/single, no other borders) (0.20 points)
    # -------------------------------------------------------------------------
    try:
        fill_ok_count = 0
        border_ok_count = 0
        expected_fill = 'E3F2FD'
        expected_border_color = '1565C0'
        expected_border_sz = 8  # 1pt = 8 in half-points

        for idx, anchor in enumerate(txbx_anchors[:3]):
            # Check fill color (a:solidFill > a:srgbClr)
            solidFill = anchor.find(f'.//{{{A_NS}}}solidFill')
            fill_color = None
            if solidFill is not None:
                srgbClr = solidFill.find(f'{{{A_NS}}}srgbClr')
                if srgbClr is not None:
                    fill_color = srgbClr.get('val', '').upper()

            if fill_color == expected_fill.upper():
                fill_ok_count += 1
            else:
                print(f"FAIL: Component 4 — box {idx+1} fill: expected #{expected_fill}, found #{fill_color}")

            # Check top paragraph border (w:pBdr > w:top)
            pBdr = anchor.find(f'.//{{{W_NS}}}pBdr')
            top_bdr_ok = False
            no_other_borders = True
            if pBdr is not None:
                top = pBdr.find(f'{{{W_NS}}}top')
                if top is not None:
                    bdr_color = top.get(f'{{{W_NS}}}color', '').upper()
                    bdr_val = top.get(f'{{{W_NS}}}val', '')
                    bdr_sz_str = top.get(f'{{{W_NS}}}sz', '0')
                    bdr_sz = int(bdr_sz_str) if bdr_sz_str.isdigit() else 0

                    color_ok = bdr_color == expected_border_color.upper()
                    val_ok = bdr_val == 'single'
                    sz_ok = abs(bdr_sz - expected_border_sz) <= 2  # allow ±2 half-points tolerance

                    if color_ok and val_ok and sz_ok:
                        top_bdr_ok = True
                    else:
                        print(f"FAIL: Component 4 — box {idx+1} top border: "
                              f"color={bdr_color}(exp:{expected_border_color}), "
                              f"val={bdr_val}(exp:single), sz={bdr_sz}(exp:{expected_border_sz})")

                # Check that no other borders exist (bottom, left, right)
                for side in ['bottom', 'left', 'right']:
                    side_elem = pBdr.find(f'{{{W_NS}}}{side}')
                    if side_elem is not None:
                        side_val = side_elem.get(f'{{{W_NS}}}val', 'none')
                        if side_val not in ('none', 'nil'):
                            # Check if it has actual border properties
                            side_color = side_elem.get(f'{{{W_NS}}}color', '')
                            if side_color and side_color.upper() not in ('AUTO', 'FFFFFF', 'NONE'):
                                print(f"FAIL: Component 4 — box {idx+1} has unexpected {side} border")
                                no_other_borders = False

            if top_bdr_ok:
                border_ok_count += 1

        if fill_ok_count == 3 and border_ok_count == 3:
            print(f"PASS: Component 4 — all 3 boxes have light blue (#E3F2FD) background "
                  f"and 1pt #1565C0 top-only border (0.20 pts)")
            total_score += 0.20
        elif fill_ok_count == 3:
            print(f"PASS (partial): Component 4 — correct background color but top border issues "
                  f"({border_ok_count}/3 borders ok) (0.10 pts)")
            total_score += 0.10
        elif border_ok_count == 3:
            print(f"PASS (partial): Component 4 — correct borders but background color issues "
                  f"({fill_ok_count}/3 fills ok) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 — background color ({fill_ok_count}/3 ok) and/or "
                  f"top border ({border_ok_count}/3 ok) incorrect")

    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # -------------------------------------------------------------------------
    # Component 5: Internal padding ~0.3cm (108000 EMU) on all sides (0.10 points)
    # -------------------------------------------------------------------------
    try:
        expected_padding_emu = cm_to_emu(0.3)  # 108000 EMU
        padding_ok_count = 0

        for idx, anchor in enumerate(txbx_anchors[:3]):
            bodyPr = anchor.find(f'.//{{{WPS_NS}}}bodyPr')
            if bodyPr is None:
                print(f"FAIL: Component 5 — box {idx+1} has no bodyPr element")
                continue

            # Check at least insL, insR, insT, insB (or insTB shorthand)
            ins_attrs = ['insL', 'insR', 'insT', 'insB']
            ins_tb = bodyPr.get('insTB')

            all_padding_ok = True
            for attr in ins_attrs:
                val_str = bodyPr.get(attr, None)
                if val_str is None and ins_tb is not None:
                    # insTB covers insT and insB
                    val_str = ins_tb
                if val_str is None:
                    print(f"FAIL: Component 5 — box {idx+1} missing {attr} padding")
                    all_padding_ok = False
                    continue
                val_emu = int(val_str)
                if abs(val_emu - expected_padding_emu) > PAD_TOL_EMU:
                    print(f"FAIL: Component 5 — box {idx+1} {attr}: expected ~0.3cm ({expected_padding_emu} EMU), "
                          f"found {emu_to_cm(val_emu):.3f}cm ({val_emu} EMU)")
                    all_padding_ok = False

            if all_padding_ok:
                padding_ok_count += 1

        if padding_ok_count == 3:
            print(f"PASS: Component 5 — all 3 boxes have ~0.3cm internal padding (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 — padding incorrect for {3 - padding_ok_count} box(es) "
                  f"({padding_ok_count}/3 ok)")

    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {round(total_score, 4)}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path on the VM
file_path = f'{WORKDIR}/Desktop/product_page.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

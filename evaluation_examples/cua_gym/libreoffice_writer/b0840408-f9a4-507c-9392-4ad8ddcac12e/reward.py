"""
Reward Script: Insert text frame in newsletter
Task ID: writer_fs_009
Domain: libreoffice_writer
Scoring:
  Component 1: Text frame (anchor+textbox) exists           — 0.2 pts
  Component 2: Width is 6.0 cm (2160000 EMU +/- 5%)        — 0.2 pts
  Component 3: Height is 3.0 cm (1080000 EMU +/- 5%)       — 0.2 pts
  Component 4: H-position 12.0 cm from page left +/- 5%    — 0.2 pts
  Component 5: V-position 2.0 cm from page top +/- 5%      — 0.2 pts
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_fs_009'

# EMU per cm = 360000
EMU_PER_CM = 360000
TOLERANCE = 0.05  # 5% tolerance


def within_tolerance(actual_emu, expected_cm):
    """Check if actual EMU value is within tolerance of expected cm value."""
    expected_emu = expected_cm * EMU_PER_CM
    low = expected_emu * (1 - TOLERANCE)
    high = expected_emu * (1 + TOLERANCE)
    return low <= actual_emu <= high


def persist_app_state(domain):
    """Save any unsaved GUI edits before verification."""
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
    Verify task completion with progressive scoring.
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

    body = doc.element.body
    wp_ns = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
    wps_ns = 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape'

    # Find all anchored drawing objects that contain a textbox
    anchors = body.findall('.//{' + wp_ns + '}anchor')
    textbox_anchors = []
    for anchor in anchors:
        # Check if this anchor contains a wps:txbx (wordprocessing textbox)
        txbx_elements = anchor.findall('.//{' + wps_ns + '}txbx')
        if len(txbx_elements) > 0:
            textbox_anchors.append(anchor)

    # Also check for w:framePr based text frames as an alternative representation
    frame_prs = body.findall('.//' + qn('w:framePr'))

    # Component 1: Text frame/textbox exists (0.2 points)
    try:
        if len(textbox_anchors) > 0:
            print(f"PASS: Component 1 — Found {len(textbox_anchors)} textbox anchor(s) (0.2 pts)")
            total_score += 0.2
        elif len(frame_prs) > 0:
            print(f"PASS: Component 1 — Found {len(frame_prs)} text frame(s) via w:framePr (0.2 pts)")
            total_score += 0.2
        else:
            print("FAIL: Component 1 — No text frame or textbox found in document")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Use the first textbox anchor for dimension/position checks
    # Prefer anchored textbox; fallback to framePr
    if len(textbox_anchors) > 0:
        anchor = textbox_anchors[0]

        # Extract extent (width/height)
        extent = anchor.find('{' + wp_ns + '}extent')
        pos_h_elem = anchor.find('{' + wp_ns + '}positionH')
        pos_v_elem = anchor.find('{' + wp_ns + '}positionV')

        # Component 2: Width is 6.0 cm (0.2 points)
        try:
            if extent is not None:
                cx = int(extent.get('cx', '0'))
                actual_cm = cx / EMU_PER_CM
                if within_tolerance(cx, 6.0):
                    print(f"PASS: Component 2 — Width {actual_cm:.2f} cm (expected 6.0 cm, {cx} EMU) (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 2 — Width {actual_cm:.2f} cm (expected 6.0 cm, actual {cx} EMU)")
            else:
                print("FAIL: Component 2 — No extent element found on anchor")
        except Exception as e:
            print(f"ERROR: Component 2 — {e}")

        # Component 3: Height is 3.0 cm (0.2 points)
        try:
            if extent is not None:
                cy = int(extent.get('cy', '0'))
                actual_cm = cy / EMU_PER_CM
                if within_tolerance(cy, 3.0):
                    print(f"PASS: Component 3 — Height {actual_cm:.2f} cm (expected 3.0 cm, {cy} EMU) (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 3 — Height {actual_cm:.2f} cm (expected 3.0 cm, actual {cy} EMU)")
            else:
                print("FAIL: Component 3 — No extent element found on anchor")
        except Exception as e:
            print(f"ERROR: Component 3 — {e}")

        # Component 4: Horizontal position 12.0 cm from page left (0.2 points)
        try:
            if pos_h_elem is not None:
                rel_from_h = pos_h_elem.get('relativeFrom', '')
                offset_h_elem = pos_h_elem.find('{' + wp_ns + '}posOffset')
                if offset_h_elem is not None:
                    h_offset = int(offset_h_elem.text)
                    actual_cm = h_offset / EMU_PER_CM
                    # Accept both "page" and "column"/"margin" relative positioning
                    # For page-relative, 12.0 cm from left edge
                    if rel_from_h == 'page' and within_tolerance(h_offset, 12.0):
                        print(f"PASS: Component 4 — H-position {actual_cm:.2f} cm from page left (expected 12.0 cm) (0.2 pts)")
                        total_score += 0.2
                    elif rel_from_h != 'page':
                        # If relative to margin/column, adjust for typical 2.54cm margin
                        # 12.0 cm from page = ~9.46 cm from margin (with 2.54cm left margin)
                        # Be generous: check if position is roughly in the right zone
                        margin_adjusted = h_offset + (2.54 * EMU_PER_CM)  # approximate
                        if within_tolerance(margin_adjusted, 12.0):
                            print(f"PASS: Component 4 — H-position {actual_cm:.2f} cm from {rel_from_h} (~12.0 cm from page) (0.2 pts)")
                            total_score += 0.2
                        else:
                            print(f"FAIL: Component 4 — H-position {actual_cm:.2f} cm from {rel_from_h} (expected ~12.0 cm from page)")
                    else:
                        print(f"FAIL: Component 4 — H-position {actual_cm:.2f} cm from {rel_from_h} (expected 12.0 cm)")
                else:
                    print("FAIL: Component 4 — No posOffset found in positionH")
            else:
                print("FAIL: Component 4 — No positionH element found")
        except Exception as e:
            print(f"ERROR: Component 4 — {e}")

        # Component 5: Vertical position 2.0 cm from page top (0.2 points)
        try:
            if pos_v_elem is not None:
                rel_from_v = pos_v_elem.get('relativeFrom', '')
                offset_v_elem = pos_v_elem.find('{' + wp_ns + '}posOffset')
                if offset_v_elem is not None:
                    v_offset = int(offset_v_elem.text)
                    actual_cm = v_offset / EMU_PER_CM
                    if rel_from_v == 'page' and within_tolerance(v_offset, 2.0):
                        print(f"PASS: Component 5 — V-position {actual_cm:.2f} cm from page top (expected 2.0 cm) (0.2 pts)")
                        total_score += 0.2
                    elif rel_from_v != 'page':
                        margin_adjusted = v_offset + (2.54 * EMU_PER_CM)
                        if within_tolerance(margin_adjusted, 2.0):
                            print(f"PASS: Component 5 — V-position {actual_cm:.2f} cm from {rel_from_v} (~2.0 cm from page) (0.2 pts)")
                            total_score += 0.2
                        else:
                            print(f"FAIL: Component 5 — V-position {actual_cm:.2f} cm from {rel_from_v} (expected ~2.0 cm from page)")
                    else:
                        print(f"FAIL: Component 5 — V-position {actual_cm:.2f} cm from {rel_from_v} (expected 2.0 cm)")
                else:
                    print("FAIL: Component 5 — No posOffset found in positionV")
            else:
                print("FAIL: Component 5 — No positionV element found")
        except Exception as e:
            print(f"ERROR: Component 5 — {e}")

    elif len(frame_prs) > 0:
        # Fallback: w:framePr based text frame
        frame = frame_prs[0]
        # w:framePr uses attributes like w:w (width), w:h (height), w:x, w:y in twips (1 inch = 1440 twips)
        TWIPS_PER_CM = 567  # approx 566.93

        # Component 2: Width
        try:
            w_val = frame.get(qn('w:w'))
            if w_val is not None:
                width_twips = int(w_val)
                actual_cm = width_twips / TWIPS_PER_CM
                if abs(actual_cm - 6.0) <= 6.0 * TOLERANCE:
                    print(f"PASS: Component 2 — Width {actual_cm:.2f} cm (framePr) (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 2 — Width {actual_cm:.2f} cm (expected 6.0 cm)")
            else:
                print("FAIL: Component 2 — No width attribute in framePr")
        except Exception as e:
            print(f"ERROR: Component 2 — {e}")

        # Component 3: Height
        try:
            h_val = frame.get(qn('w:h'))
            if h_val is not None:
                height_twips = int(h_val)
                actual_cm = height_twips / TWIPS_PER_CM
                if abs(actual_cm - 3.0) <= 3.0 * TOLERANCE:
                    print(f"PASS: Component 3 — Height {actual_cm:.2f} cm (framePr) (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 3 — Height {actual_cm:.2f} cm (expected 3.0 cm)")
            else:
                print("FAIL: Component 3 — No height attribute in framePr")
        except Exception as e:
            print(f"ERROR: Component 3 — {e}")

        # Component 4: H-position
        try:
            x_val = frame.get(qn('w:x'))
            if x_val is not None:
                x_twips = int(x_val)
                actual_cm = x_twips / TWIPS_PER_CM
                if abs(actual_cm - 12.0) <= 12.0 * TOLERANCE:
                    print(f"PASS: Component 4 — H-position {actual_cm:.2f} cm (framePr) (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 4 — H-position {actual_cm:.2f} cm (expected 12.0 cm)")
            else:
                print("FAIL: Component 4 — No x attribute in framePr")
        except Exception as e:
            print(f"ERROR: Component 4 — {e}")

        # Component 5: V-position
        try:
            y_val = frame.get(qn('w:y'))
            if y_val is not None:
                y_twips = int(y_val)
                actual_cm = y_twips / TWIPS_PER_CM
                if abs(actual_cm - 2.0) <= 2.0 * TOLERANCE:
                    print(f"PASS: Component 5 — V-position {actual_cm:.2f} cm (framePr) (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 5 — V-position {actual_cm:.2f} cm (expected 2.0 cm)")
            else:
                print("FAIL: Component 5 — No y attribute in framePr")
        except Exception as e:
            print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 1)
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

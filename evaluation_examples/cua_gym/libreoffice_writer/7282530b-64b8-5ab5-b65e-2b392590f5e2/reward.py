"""
Reward Script: Create two linked text frames side by side
Task ID: writer_fs_011
Domain: libreoffice_writer
Scoring:
  Component 1 (0.25): Two drawing/text-frame elements exist
  Component 2 (0.25): Both frames are ~7cm wide x ~10cm tall
  Component 3 (0.25): Frames positioned side by side (left + right)
  Component 4 (0.25): Frames are linked (linkedTxbx element present)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_fs_011'


def persist_app_state(domain):
    """Save any unsaved GUI edits before verification."""
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            import time
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
        from lxml import etree
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    body = doc.element.body
    nsmap = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
        'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
        'wps': 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape',
    }

    # Gather all drawing elements
    drawings = body.findall('.//w:drawing', nsmap)

    # Component 1: Two drawing/text-frame elements exist (0.25 points)
    try:
        num_drawings = len(drawings)
        if num_drawings >= 2:
            print(f"PASS: Component 1 — Found {num_drawings} drawing elements (>= 2) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Expected >= 2 drawings, found {num_drawings}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if num_drawings < 2:
        # Cannot proceed with further checks if fewer than 2 frames
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Extract properties from the first two drawings
    frame_data = []
    for i in range(min(2, num_drawings)):
        d = drawings[i]
        info = {'index': i, 'cx': None, 'cy': None, 'h_offset': None, 'v_offset': None,
                'has_txbx': False, 'has_linkedTxbx': False, 'linked_id': None, 'linked_seq': None}

        # Size from wp:extent
        try:
            anchors = d.findall('.//wp:anchor', nsmap)
            inlines = d.findall('.//wp:inline', nsmap)
            container = anchors[0] if anchors else (inlines[0] if inlines else None)
            if container is not None:
                extent = container.find('.//wp:extent', nsmap)
                if extent is not None:
                    info['cx'] = int(extent.get('cx', 0))
                    info['cy'] = int(extent.get('cy', 0))

                # Horizontal position
                posH = container.find('wp:positionH', nsmap)
                if posH is not None:
                    offset_el = posH.find('wp:posOffset', nsmap)
                    if offset_el is not None and offset_el.text:
                        info['h_offset'] = int(offset_el.text)

                # Vertical position
                posV = container.find('wp:positionV', nsmap)
                if posV is not None:
                    offset_el = posV.find('wp:posOffset', nsmap)
                    if offset_el is not None and offset_el.text:
                        info['v_offset'] = int(offset_el.text)
        except Exception as e:
            print(f"WARN: Could not parse drawing {i} anchor/size: {e}")

        # Check for txbx (text content) or linkedTxbx (linked frame)
        try:
            txbx_list = d.findall('.//wps:txbx', nsmap)
            if txbx_list:
                info['has_txbx'] = True

            linked_list = d.findall('.//wps:linkedTxbx', nsmap)
            if linked_list:
                info['has_linkedTxbx'] = True
                info['linked_id'] = linked_list[0].get('id')
                info['linked_seq'] = linked_list[0].get('seq')
        except Exception as e:
            print(f"WARN: Could not parse drawing {i} txbx elements: {e}")

        frame_data.append(info)
        print(f"  Frame {i}: cx={info['cx']}, cy={info['cy']}, h_offset={info['h_offset']}, "
              f"has_txbx={info['has_txbx']}, has_linkedTxbx={info['has_linkedTxbx']}")

    # Component 2: Both frames are approximately 7cm wide x 10cm tall (0.25 points)
    # 7cm = 2520000 EMU, 10cm = 3600000 EMU. Allow 20% tolerance.
    try:
        target_cx = 2520000  # 7cm in EMU
        target_cy = 3600000  # 10cm in EMU
        tolerance = 0.20  # 20% tolerance

        size_ok_count = 0
        for fd in frame_data:
            if fd['cx'] is not None and fd['cy'] is not None:
                cx_ok = abs(fd['cx'] - target_cx) <= target_cx * tolerance
                cy_ok = abs(fd['cy'] - target_cy) <= target_cy * tolerance
                if cx_ok and cy_ok:
                    size_ok_count += 1
                else:
                    print(f"  Frame {fd['index']} size mismatch: "
                          f"cx={fd['cx']} (target {target_cx}), cy={fd['cy']} (target {target_cy})")

        if size_ok_count >= 2:
            print(f"PASS: Component 2 — Both frames are ~7cm x ~10cm (0.25 pts)")
            total_score += 0.25
        elif size_ok_count == 1:
            print(f"PARTIAL: Component 2 — Only 1 of 2 frames has correct size (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 2 — Neither frame has correct ~7cm x ~10cm size")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Frames positioned side by side — one on left, one on right (0.25 points)
    # The left frame should have a smaller horizontal offset than the right frame,
    # and the right frame offset should be > the left frame's width (i.e., no overlap).
    try:
        h_offsets = [fd['h_offset'] for fd in frame_data if fd['h_offset'] is not None]
        if len(h_offsets) >= 2:
            left_offset = min(h_offsets)
            right_offset = max(h_offsets)
            separation = right_offset - left_offset

            # The right frame must be clearly to the right of the left frame.
            # Minimum separation: at least 50% of a frame's width (1260000 EMU)
            if separation >= 1260000:
                print(f"PASS: Component 3 — Frames side by side (separation={separation} emu, "
                      f"{separation/360000:.1f}cm) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — Frames not side by side "
                      f"(separation={separation} emu = {separation/360000:.1f}cm, need >= 3.5cm)")
        elif len(h_offsets) == 1:
            # One frame has no explicit offset — might default to 0
            # Check if the one with offset is far enough right
            if h_offsets[0] >= 1260000:
                print(f"PASS: Component 3 — One frame at default (left), other offset right "
                      f"(offset={h_offsets[0]} emu) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — Only one frame has offset, insufficient separation")
        else:
            print(f"FAIL: Component 3 — Could not determine horizontal positions of frames")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Frames are linked — one frame has wps:linkedTxbx referencing the other (0.25 points)
    # A linked pair means: one frame has <wps:txbx> (source) and the other has <wps:linkedTxbx> (target).
    try:
        has_source = any(fd['has_txbx'] for fd in frame_data)
        has_linked = any(fd['has_linkedTxbx'] for fd in frame_data)

        if has_source and has_linked:
            print(f"PASS: Component 4 — Frames are linked (source txbx + linkedTxbx found) (0.25 pts)")
            total_score += 0.25
        elif has_linked:
            # linkedTxbx exists but source txbx not in first two drawings — still indicates linking
            print(f"PASS: Component 4 — linkedTxbx element found indicating frame linking (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — No linkedTxbx element found; frames are not linked")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

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

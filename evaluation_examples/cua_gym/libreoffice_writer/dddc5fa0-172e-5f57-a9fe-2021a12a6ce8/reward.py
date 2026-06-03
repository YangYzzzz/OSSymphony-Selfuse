"""
Reward Script: Group header rectangle and logo image, position at X:0 Y:0, anchor to page with No Wrap
Task ID: writer_obj_071
Domain: libreoffice_writer
Scoring:
  Component 1: Rectangle and logo are grouped into a single wordprocessingGroup (wpg:wgp)  — 0.50 pts
  Component 2: Group is positioned at X:0cm, Y:0cm (posH offset=0, posV offset=0)          — 0.25 pts
  Component 3: Group is anchored to page (relativeFrom=page) with wrapNone text wrapping   — 0.25 pts
  Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_obj_071'
FILE_PATH = os.path.join(WORKDIR, 'Desktop', 'branded_doc.docx')

# XML namespace constants
WP_NS = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
WPG_NS = 'http://schemas.microsoft.com/office/word/2010/wordprocessingGroup'
WPS_NS = 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape'
PIC_NS = 'http://schemas.openxmlformats.org/drawingml/2006/picture'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Task: Group header rectangle and logo into a single object, position at X:0 Y:0,
          anchor to page with No Wrap text wrapping.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load document XML
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            content = z.read('word/document.xml').decode('utf-8')
        root = ET.fromstring(content)
    except Exception as e:
        print(f"CRITICAL: Cannot load/parse file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find all wp:anchor elements in the document
    try:
        anchors = root.findall(f'.//{{{WP_NS}}}anchor')
        print(f"INFO: Found {len(anchors)} wp:anchor element(s) in document")
    except Exception as e:
        print(f"CRITICAL: Cannot find anchors: {e}")
        print("REWARD: 0.0")
        return 0.0

    # -----------------------------------------------------------------------
    # Component 1: Rectangle and logo are grouped into a single wordprocessingGroup
    # (0.5 points)
    # In initial_env: 2 separate anchors (Rectangle1 + Logo1), no group
    # In golden_env:  1 anchor containing a wpg:wgp with both child shapes
    # -----------------------------------------------------------------------
    try:
        group_anchor = None
        for anchor in anchors:
            grp = anchor.find(f'.//{{{WPG_NS}}}wgp')
            if grp is not None:
                group_anchor = anchor
                break

        if group_anchor is not None:
            # Verify the group contains both a shape (rectangle) and an image (logo)
            shapes_in_group = group_anchor.findall(f'.//{{{WPS_NS}}}wsp')
            pics_in_group = group_anchor.findall(f'.//{{{PIC_NS}}}pic')

            has_shape = len(shapes_in_group) >= 1
            has_pic = len(pics_in_group) >= 1

            if has_shape and has_pic:
                print(f"PASS: Component 1 — Group found containing {len(shapes_in_group)} shape(s) "
                      f"and {len(pics_in_group)} image(s). Objects are grouped into a single wpg:wgp. (0.5 pts)")
                total_score += 0.5
            else:
                print(f"FAIL: Component 1 — Group found but missing expected members: "
                      f"shapes={len(shapes_in_group)}, pics={len(pics_in_group)}. "
                      f"Expected at least 1 shape (rectangle) and 1 image (logo).")
        else:
            print(f"FAIL: Component 1 — No wordprocessingGroup (wpg:wgp) found. "
                  f"Found {len(anchors)} separate anchor(s). Rectangle and logo are NOT grouped.")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: Group positioned at X:0cm, Y:0cm (posH offset = 0, posV offset = 0)
    # (0.25 points)
    # In initial_env: Rectangle at posH=72000, posV=108000; Logo at posH=108000, posV=144000
    # In golden_env:  Group at posH=0, posV=0
    # -----------------------------------------------------------------------
    try:
        if group_anchor is not None:
            posH_elem = group_anchor.find(f'{{{WP_NS}}}positionH')
            posV_elem = group_anchor.find(f'{{{WP_NS}}}positionV')

            posH_ok = False
            posV_ok = False

            if posH_elem is not None:
                posH_offset_elem = posH_elem.find(f'{{{WP_NS}}}posOffset')
                if posH_offset_elem is not None:
                    posH_val = int(posH_offset_elem.text or '999')
                    # 0 EMU = 0cm
                    posH_ok = (posH_val == 0)
                    if posH_ok:
                        print(f"PASS: Component 2a — posH offset = {posH_val} EMU (0.0cm)")
                    else:
                        print(f"FAIL: Component 2a — posH offset = {posH_val} EMU "
                              f"({posH_val/914400*2.54:.3f}cm), expected 0 (0.0cm)")

            if posV_elem is not None:
                posV_offset_elem = posV_elem.find(f'{{{WP_NS}}}posOffset')
                if posV_offset_elem is not None:
                    posV_val = int(posV_offset_elem.text or '999')
                    # 0 EMU = 0cm
                    posV_ok = (posV_val == 0)
                    if posV_ok:
                        print(f"PASS: Component 2b — posV offset = {posV_val} EMU (0.0cm)")
                    else:
                        print(f"FAIL: Component 2b — posV offset = {posV_val} EMU "
                              f"({posV_val/914400*2.54:.3f}cm), expected 0 (0.0cm)")

            if posH_ok and posV_ok:
                print(f"PASS: Component 2 — Group positioned at X:0cm, Y:0cm. (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 — Group not at X:0cm Y:0cm. posH_ok={posH_ok}, posV_ok={posV_ok}")
        else:
            print("FAIL: Component 2 — Skipped (no group anchor found in Component 1)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: Group anchored to page (relativeFrom=page) with wrapNone
    # (0.25 points)
    # In initial_env: both anchors already have wrapNone and relativeFrom=page,
    #   but the group object itself doesn't exist
    # In golden_env:  the single group anchor has relativeFrom=page and wrapNone
    # Note: Only score this as part of the group anchor — ensures it's the grouped object
    # -----------------------------------------------------------------------
    try:
        if group_anchor is not None:
            posH_elem = group_anchor.find(f'{{{WP_NS}}}positionH')
            posV_elem = group_anchor.find(f'{{{WP_NS}}}positionV')

            page_anchor_H = False
            page_anchor_V = False

            if posH_elem is not None:
                page_anchor_H = (posH_elem.get('relativeFrom') == 'page')
            if posV_elem is not None:
                page_anchor_V = (posV_elem.get('relativeFrom') == 'page')

            wrap_none = group_anchor.find(f'{{{WP_NS}}}wrapNone')
            has_wrap_none = (wrap_none is not None)

            if page_anchor_H and page_anchor_V and has_wrap_none:
                print(f"PASS: Component 3 — Group anchor relativeFrom=page (H and V), "
                      f"wrapNone present. (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — page_anchor_H={page_anchor_H}, "
                      f"page_anchor_V={page_anchor_V}, wrapNone={has_wrap_none}")
        else:
            print("FAIL: Component 3 — Skipped (no group anchor found in Component 1)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

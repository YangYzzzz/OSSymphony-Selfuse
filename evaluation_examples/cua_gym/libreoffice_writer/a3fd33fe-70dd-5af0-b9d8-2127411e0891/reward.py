"""
Reward Script: Insert company logo with specific position, size, anchor, wrap, border, and alt text
Task ID: writer_obj_056
Domain: libreoffice_writer
Scoring:
  Component 1: Image/drawing anchor present in document         (0.20 pts)
  Component 2: Image size is 2.5cm x 2.5cm                     (0.20 pts)
  Component 3: Image position X: 1cm, Y: 1cm from page         (0.20 pts)
  Component 4: Alt text is 'TechCorp Logo'                     (0.10 pts)
  Component 5: Border 0.5pt solid gray (#9E9E9E)               (0.15 pts)
  Component 6: Wrap type (wrapSquare/Parallel) + spacing        (0.15 pts)
  Total: 1.0
"""

import os
import re
import zipfile

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_obj_056'

# Tolerances
EMU_TOL = 18000  # ~0.05cm tolerance for position/size checks (0.05cm = 18000 EMU)
LINE_W_TOL = 1270  # ~0.1pt tolerance for line width (0.1pt = 1270 EMU)


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Read the raw document XML for anchor/drawing analysis
    try:
        with zipfile.ZipFile(file_path) as z:
            doc_xml = z.read('word/document.xml').decode('utf-8')
    except Exception as e:
        print(f"CRITICAL: Cannot read document XML: {e}")
        print("REWARD: 0.0")
        return 0.0

    # -----------------------------------------------------------------------
    # Component 1: Image/drawing anchor present in document (0.20 pts)
    # Task requires inserting a logo image anchored to the page.
    # This FAILS on initial (no images) and PASSES on golden (image added).
    # -----------------------------------------------------------------------
    try:
        drawing_blocks = re.findall(r'<w:drawing>.*?</w:drawing>', doc_xml, re.DOTALL)
        anchor_blocks = re.findall(r'<wp:anchor[^>]*>.*?</wp:anchor>', doc_xml, re.DOTALL)

        if len(drawing_blocks) >= 1 and len(anchor_blocks) >= 1:
            print(f"PASS: Component 1 — Floating anchor image found in document (0.20 pts)")
            total_score += 0.20
        elif len(drawing_blocks) >= 1:
            print(f"FAIL: Component 1 — Drawing found but no anchor (may be inline, not page-anchored)")
        else:
            print(f"FAIL: Component 1 — No drawing/image found in document")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Extract anchor XML for subsequent checks
    anchor_xml = ""
    try:
        anchor_match = re.search(r'<wp:anchor[^>]*>.*?</wp:anchor>', doc_xml, re.DOTALL)
        if anchor_match:
            anchor_xml = anchor_match.group(0)
    except Exception as e:
        print(f"WARN: Could not extract anchor XML: {e}")

    # -----------------------------------------------------------------------
    # Component 2: Image size is 2.5cm x 2.5cm (0.20 pts)
    # Expected: cx=900000 EMU, cy=900000 EMU (2.5cm = 900000 EMU)
    # This FAILS on initial (no image) and PASSES on golden (2.5cm x 2.5cm).
    # -----------------------------------------------------------------------
    try:
        extent_match = re.search(r'<wp:extent\s+cx="(\d+)"\s+cy="(\d+)"', anchor_xml)
        if extent_match:
            cx = int(extent_match.group(1))
            cy = int(extent_match.group(2))
            expected_size = 900000  # 2.5cm in EMU
            size_ok = abs(cx - expected_size) <= EMU_TOL and abs(cy - expected_size) <= EMU_TOL
            if size_ok:
                print(f"PASS: Component 2 — Image size {cx}x{cy} EMU = ~2.5cm x 2.5cm (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 — Expected size ~900000x900000 EMU, found {cx}x{cy} EMU")
        else:
            print(f"FAIL: Component 2 — No extent element found in anchor XML")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: Image position X: 1cm, Y: 1cm from page (0.20 pts)
    # Expected: posH=360000 EMU, posV=360000 EMU (1cm = 360000 EMU)
    # Must be anchored to 'page' (relativeFrom="page")
    # This FAILS on initial (no image) and PASSES on golden (correct position).
    # -----------------------------------------------------------------------
    try:
        pos_h_match = re.search(r'<wp:positionH\s+relativeFrom="([^"]+)">\s*<wp:posOffset>(\d+)</wp:posOffset>', anchor_xml)
        pos_v_match = re.search(r'<wp:positionV\s+relativeFrom="([^"]+)">\s*<wp:posOffset>(\d+)</wp:posOffset>', anchor_xml)

        if pos_h_match and pos_v_match:
            h_anchor = pos_h_match.group(1)
            pos_h = int(pos_h_match.group(2))
            v_anchor = pos_v_match.group(1)
            pos_v = int(pos_v_match.group(2))
            expected_pos = 360000  # 1cm in EMU
            pos_ok = abs(pos_h - expected_pos) <= EMU_TOL and abs(pos_v - expected_pos) <= EMU_TOL
            anchor_ok = h_anchor == "page" and v_anchor == "page"
            if pos_ok and anchor_ok:
                print(f"PASS: Component 3 — Position {pos_h}x{pos_v} EMU = ~1cm x 1cm, anchored to page (0.20 pts)")
                total_score += 0.20
            elif pos_ok and not anchor_ok:
                print(f"FAIL: Component 3 — Position correct but anchor is '{h_anchor}/{v_anchor}' (expected 'page/page')")
            else:
                print(f"FAIL: Component 3 — Expected position ~360000x360000 EMU, found {pos_h}x{pos_v} EMU (anchor: {h_anchor}/{v_anchor})")
        else:
            print(f"FAIL: Component 3 — positionH/positionV elements not found in anchor XML")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -----------------------------------------------------------------------
    # Component 4: Alt text is 'TechCorp Logo' (0.10 pts)
    # Check both name= and descr= attributes on wp:docPr
    # This FAILS on initial (no image) and PASSES on golden (alt text set).
    # -----------------------------------------------------------------------
    try:
        docpr_match = re.search(r'<wp:docPr\s+[^>]*descr="([^"]*)"', anchor_xml)
        name_match = re.search(r'<wp:docPr\s+[^>]*name="([^"]*)"', anchor_xml)

        alt_text = docpr_match.group(1) if docpr_match else ""
        name_text = name_match.group(1) if name_match else ""

        expected_alt = "TechCorp Logo"
        if alt_text == expected_alt or name_text == expected_alt:
            print(f"PASS: Component 4 — Alt text/name is '{alt_text or name_text}' (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 — Expected alt text '{expected_alt}', found descr='{alt_text}' name='{name_text}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # -----------------------------------------------------------------------
    # Component 5: Border 0.5pt solid gray (#9E9E9E) (0.15 pts)
    # Expected: line width 6350 EMU (0.5pt), color 9E9E9E
    # This FAILS on initial (no image) and PASSES on golden (border applied).
    # -----------------------------------------------------------------------
    try:
        line_w_match = re.search(r'<a:ln\s+[^>]*w="(\d+)"', anchor_xml)
        color_match = re.search(r'<a:srgbClr\s+val="([^"]+)"', anchor_xml)
        prstdash_match = re.search(r'<a:prstDash\s+val="([^"]+)"', anchor_xml)

        line_ok = False
        color_ok = False

        if line_w_match:
            line_w = int(line_w_match.group(1))
            expected_line_w = 6350  # 0.5pt in EMU
            line_ok = abs(line_w - expected_line_w) <= LINE_W_TOL
            if not line_ok:
                print(f"FAIL: Component 5 (border width) — Expected ~6350 EMU (0.5pt), found {line_w} EMU ({line_w/12700:.2f}pt)")
        else:
            print(f"FAIL: Component 5 (border) — No border line element found")

        if color_match:
            color = color_match.group(1).upper()
            color_ok = color == "9E9E9E"
            if not color_ok:
                print(f"FAIL: Component 5 (border color) — Expected '9E9E9E', found '{color}'")
        else:
            print(f"FAIL: Component 5 (border color) — No color element found")

        if line_ok and color_ok:
            print(f"PASS: Component 5 — Border 0.5pt solid gray #9E9E9E found (0.15 pts)")
            total_score += 0.15
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # -----------------------------------------------------------------------
    # Component 6: Wrap type (wrapSquare/Parallel) + spacing (0.15 pts)
    # Task: "Parallel" wrapping (= wrapSquare in OOXML)
    # right spacing 0.5cm (distR=180000 EMU), bottom 0.3cm (distB=108000 EMU)
    # left and top spacing 0cm (distL=0, distT=0)
    # This FAILS on initial (no image) and PASSES on golden (wrap applied).
    # -----------------------------------------------------------------------
    try:
        wrap_sq_match = re.search(r'<wp:wrapSquare\s+([^>]*)/>', anchor_xml)
        if wrap_sq_match:
            wrap_attrs = wrap_sq_match.group(1)
            # Extract spacing values
            dist_r_match = re.search(r'distR="(\d+)"', wrap_attrs)
            dist_b_match = re.search(r'distB="(\d+)"', wrap_attrs)
            dist_l_match = re.search(r'distL="(\d+)"', wrap_attrs)
            dist_t_match = re.search(r'distT="(\d+)"', wrap_attrs)

            dist_r = int(dist_r_match.group(1)) if dist_r_match else 0
            dist_b = int(dist_b_match.group(1)) if dist_b_match else 0
            dist_l = int(dist_l_match.group(1)) if dist_l_match else 0
            dist_t = int(dist_t_match.group(1)) if dist_t_match else 0

            expected_r = 180000   # 0.5cm
            expected_b = 108000   # 0.3cm

            r_ok = abs(dist_r - expected_r) <= EMU_TOL
            b_ok = abs(dist_b - expected_b) <= EMU_TOL

            if r_ok and b_ok:
                print(f"PASS: Component 6 — wrapSquare (Parallel) with distR={dist_r} (~0.5cm), distB={dist_b} (~0.3cm), distL={dist_l}, distT={dist_t} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 6 — wrapSquare found but spacing wrong: distR={dist_r} (expected ~{expected_r}), distB={dist_b} (expected ~{expected_b})")
        else:
            # Also check if wrapThrough or wrapTight was used (wrong wrap type)
            other_wrap = re.search(r'<wp:wrap\w+[^>]*>', anchor_xml)
            if other_wrap:
                print(f"FAIL: Component 6 — Wrong wrap type: {other_wrap.group(0)} (expected wrapSquare/Parallel)")
            else:
                print(f"FAIL: Component 6 — No wrap element found in anchor XML")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


# Default: test against canonical artifact path on the VM
file_path = f'{WORKDIR}/letterhead.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

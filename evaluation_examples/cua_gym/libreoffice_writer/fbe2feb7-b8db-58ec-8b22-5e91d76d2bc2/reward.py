"""
Reward Script: Insert banner image into document with specific size, position, and wrapping
Task ID: writer_obj_051
Domain: libreoffice_writer
Scoring:
  Component 1: Anchored image (drawing element) is present in document (0.30 pts)
  Component 2: Image dimensions are correct — width ~17cm, height ~4cm (0.35 pts)
  Component 3: Text wrapping is set to No Wrap (wrapNone) (0.15 pts)
  Component 4: Image Y position is at or near the top margin (~0cm from top margin) (0.20 pts)
Total: 1.0
"""

import os
import re
from docx import Document

WORKDIR = '/home/user/Desktop'
TASK_ID = 'event_flyer'
FILE_PATH = f'{WORKDIR}/{TASK_ID}.docx'

# Conversion constant: EMU per centimeter
EMU_PER_CM = 914400 / 2.54  # = 360000


def cm_to_emu(cm):
    return cm * EMU_PER_CM


def emu_to_cm(emu):
    return emu / EMU_PER_CM


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Task: Insert banner.jpg into event_flyer.docx with:
      - Width: 17cm (full text area width)
      - Height: 4cm
      - Anchored to page (floating anchor)
      - Text wrapping: No Wrap (wrapNone)
      - Y position: 0cm from top margin (i.e., at top margin boundary)
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get page section for margin reference
    try:
        section = doc.sections[0]
        top_margin_emu = section.top_margin  # EMU
    except Exception as e:
        print(f"WARN: Could not read section margins: {e}")
        top_margin_emu = None

    # Parse body XML for drawing/anchor elements
    try:
        body_xml = doc.element.body.xml
    except Exception as e:
        print(f"CRITICAL: Cannot parse body XML: {e}")
        print("REWARD: 0.0")
        return 0.0

    # -------------------------------------------------------------------------
    # Component 1: Anchored image (drawing element) is present (0.30 points)
    # A task-introduced change: initial doc has no images, golden has 1 anchor.
    # We look for <wp:anchor> which indicates a floating/anchored image.
    # -------------------------------------------------------------------------
    try:
        has_anchor = '<wp:anchor' in body_xml
        has_image_rel = any('image' in rel.reltype for rel in doc.part.rels.values())

        if has_anchor and has_image_rel:
            print(f"PASS: Component 1 — Anchored image (floating drawing) found in document (0.30 pts)")
            total_score += 0.30
        elif has_image_rel and not has_anchor:
            # Inline image present but not anchored (partial — not exactly right)
            print(f"FAIL: Component 1 — Image found but not as floating anchor (inline only). "
                  f"Expected wp:anchor element for page-anchored image.")
        else:
            print(f"FAIL: Component 1 — No anchored image found in document "
                  f"(has_anchor={has_anchor}, has_image_rel={has_image_rel})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------------
    # Component 2: Image dimensions correct — width ~17cm, height ~4cm (0.35 points)
    # Extract from <wp:extent cx="..." cy="..."/>
    # Expected: cx=6120000 EMU (17cm), cy=1440000 EMU (4cm)
    # Allow 5% tolerance (~±0.85cm for width, ±0.2cm for height)
    # -------------------------------------------------------------------------
    try:
        extent_match = re.search(r'<wp:extent cx="([0-9]+)" cy="([0-9]+)"', body_xml)
        if extent_match:
            cx_emu = int(extent_match.group(1))
            cy_emu = int(extent_match.group(2))
            width_cm = emu_to_cm(cx_emu)
            height_cm = emu_to_cm(cy_emu)

            # Target: 17cm width, 4cm height
            target_width_cm = 17.0
            target_height_cm = 4.0
            tolerance_pct = 0.07  # 7% tolerance

            width_ok = abs(width_cm - target_width_cm) / target_width_cm <= tolerance_pct
            height_ok = abs(height_cm - target_height_cm) / target_height_cm <= tolerance_pct

            if width_ok and height_ok:
                print(f"PASS: Component 2 — Image dimensions correct: "
                      f"width={width_cm:.2f}cm (target 17cm), height={height_cm:.2f}cm (target 4cm) (0.35 pts)")
                total_score += 0.35
            elif width_ok:
                print(f"FAIL: Component 2 — Width correct ({width_cm:.2f}cm) but height wrong: "
                      f"{height_cm:.2f}cm (expected ~4cm)")
            elif height_ok:
                print(f"FAIL: Component 2 — Height correct ({height_cm:.2f}cm) but width wrong: "
                      f"{width_cm:.2f}cm (expected ~17cm)")
            else:
                print(f"FAIL: Component 2 — Both dimensions wrong: "
                      f"width={width_cm:.2f}cm (expected ~17cm), height={height_cm:.2f}cm (expected ~4cm)")
        else:
            print(f"FAIL: Component 2 — Could not find <wp:extent> element in drawing XML "
                  f"(no anchored image present or wrong format)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Component 3: Text wrapping is No Wrap (wrapNone) (0.15 points)
    # The task requires 'No Wrap' text wrapping.
    # In OOXML, this is <wp:wrapNone/> inside the wp:anchor element.
    # -------------------------------------------------------------------------
    try:
        has_wrap_none = '<wp:wrapNone' in body_xml or 'wrapNone' in body_xml

        if has_wrap_none:
            print(f"PASS: Component 3 — Text wrapping is 'No Wrap' (wrapNone found) (0.15 pts)")
            total_score += 0.15
        else:
            # Check what wrapping type is present
            wrap_match = re.search(r'<wp:(wrap\w+)', body_xml)
            wrap_type = wrap_match.group(1) if wrap_match else 'unknown'
            print(f"FAIL: Component 3 — Text wrapping is NOT 'No Wrap'. "
                  f"Found: {wrap_type} (expected wrapNone)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -------------------------------------------------------------------------
    # Component 4: Image Y position at/near top margin (Y=0cm from top margin) (0.20 points)
    # The anchor positionV relativeFrom="page" offset should equal the top margin EMU value,
    # meaning the image top edge coincides with the top margin boundary (Y=0 from margin).
    # Allow tolerance of ±0.5cm (180000 EMU).
    # -------------------------------------------------------------------------
    try:
        pos_v_match = re.search(
            r'<wp:positionV[^>]*relativeFrom="page"[^>]*>.*?<wp:posOffset>([0-9]+)</wp:posOffset>',
            body_xml,
            re.DOTALL
        )

        if pos_v_match and top_margin_emu is not None:
            pos_v_emu = int(pos_v_match.group(1))
            pos_v_cm = emu_to_cm(pos_v_emu)
            top_margin_cm = emu_to_cm(top_margin_emu)

            # Y relative to top margin: pos_v - top_margin
            y_from_margin_cm = pos_v_cm - top_margin_cm
            tolerance_cm = 0.5  # 0.5cm tolerance

            if abs(y_from_margin_cm) <= tolerance_cm:
                total_score += 0.20
                print(f"PASS: Component 4 — Y_from_margin={y_from_margin_cm:.2f}cm (~0cm) (0.20 pts)")
            else:
                print(f"FAIL: Component 4 — Image Y position too far from top margin: "
                      f"posV={pos_v_cm:.2f}cm from page, top_margin={top_margin_cm:.2f}cm, "
                      f"Y_from_margin={y_from_margin_cm:.2f}cm (expected ~0cm within ±{tolerance_cm}cm)")
        elif pos_v_match and top_margin_emu is None:
            # Can't compute relative position without margin, but check absolute position
            pos_v_emu = int(pos_v_match.group(1))
            pos_v_cm = emu_to_cm(pos_v_emu)
            # Typical A4 document top margin is ~2.5cm, so page-relative Y ~2.5cm means 0cm from margin
            if abs(pos_v_cm - 2.5) <= 0.6:
                print(f"PASS: Component 4 — Image Y position near top of text area: "
                      f"posV={pos_v_cm:.2f}cm from page edge (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 — Image Y position unexpected: "
                      f"posV={pos_v_cm:.2f}cm from page (expected ~2.5cm for Y=0 from top margin)")
        else:
            print(f"FAIL: Component 4 — Could not find positionV relativeFrom='page' in drawing XML")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

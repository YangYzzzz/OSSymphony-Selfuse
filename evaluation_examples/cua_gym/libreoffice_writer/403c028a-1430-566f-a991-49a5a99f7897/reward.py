"""
Reward Script: Create a C5 envelope (162 x 229 mm) with delivery address at 6cm from left, 8cm from top
Task ID: writer_lec_052
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35): Page size is C5 (162 x 229 mm)
  Component 2 (0.15): Page orientation / envelope layout
  Component 3 (0.25): Delivery address frame positioned at 6cm from left edge
  Component 4 (0.25): Delivery address frame positioned at 8cm from top edge
"""

import os
from docx import Document
from docx.shared import Emu, Cm, Mm
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_052'

# Tolerance for dimension checks (mm)
SIZE_TOLERANCE_MM = 3.0
# Tolerance for position checks (cm)
POS_TOLERANCE_CM = 0.5

WNS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': WNS}


def get_frame_positions(doc):
    """Extract text frame positions from paragraphs.

    Returns a list of dicts with frame position info and paragraph text.
    Groups consecutive paragraphs sharing the same (x, y) into frames.
    """
    frames = []
    current_frame = None

    for para in doc.paragraphs:
        pPr = para._element.find(f'{{{WNS}}}pPr')
        if pPr is not None:
            framePr = pPr.find(f'{{{WNS}}}framePr')
            if framePr is not None:
                x = framePr.get(f'{{{WNS}}}x')
                y = framePr.get(f'{{{WNS}}}y')
                if x is not None and y is not None:
                    x_emu = int(x)
                    y_emu = int(y)
                    # Group into frames by position
                    if current_frame and current_frame['x_emu'] == x_emu and current_frame['y_emu'] == y_emu:
                        current_frame['texts'].append(para.text)
                    else:
                        current_frame = {
                            'x_emu': x_emu,
                            'y_emu': y_emu,
                            'x_cm': x_emu / 360000.0,
                            'y_cm': y_emu / 360000.0,
                            'texts': [para.text]
                        }
                        frames.append(current_frame)
                    continue
        # Non-frame paragraph resets grouping
        current_frame = None

    return frames


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    section = doc.sections[0]

    # Get page dimensions in mm
    page_w_mm = section.page_width / 36000.0
    page_h_mm = section.page_height / 36000.0

    # Determine the two page dimensions regardless of orientation
    dim_long = max(page_w_mm, page_h_mm)
    dim_short = min(page_w_mm, page_h_mm)

    # Component 1: Page size is C5 envelope (162 x 229 mm) (0.35 points)
    # C5 = 162 x 229 mm. The document could be portrait (162w x 229h) or landscape (229w x 162h).
    try:
        c5_long = 229.0
        c5_short = 162.0
        long_ok = abs(dim_long - c5_long) <= SIZE_TOLERANCE_MM
        short_ok = abs(dim_short - c5_short) <= SIZE_TOLERANCE_MM

        if long_ok and short_ok:
            print(f"PASS: Component 1 - Page size is C5: {dim_long:.1f} x {dim_short:.1f} mm (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 - Expected C5 (229 x 162 mm), got {dim_long:.1f} x {dim_short:.1f} mm")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Page is NOT standard A4 (must have changed from initial blank doc) (0.15 points)
    # Initial doc is A4 (210 x 297 mm). The envelope must NOT be A4.
    try:
        a4_long = 297.0
        a4_short = 210.0
        is_a4 = abs(dim_long - a4_long) <= SIZE_TOLERANCE_MM and abs(dim_short - a4_short) <= SIZE_TOLERANCE_MM
        if not is_a4:
            print(f"PASS: Component 2 - Page is not A4 (envelope layout confirmed) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 - Page is still A4 ({dim_long:.1f} x {dim_short:.1f} mm), no envelope created")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Extract text frames for position checks
    frames = get_frame_positions(doc)
    print(f"\nFound {len(frames)} text frame(s):")
    for i, f in enumerate(frames):
        print(f"  Frame {i}: x={f['x_cm']:.2f}cm, y={f['y_cm']:.2f}cm, texts={f['texts']}")

    # Identify the delivery address frame: the one closest to (6cm, 8cm)
    # We look for a frame with x ~6cm and y ~8cm
    delivery_frame = None
    best_dist = float('inf')
    for f in frames:
        dist = ((f['x_cm'] - 6.0) ** 2 + (f['y_cm'] - 8.0) ** 2) ** 0.5
        if dist < best_dist:
            best_dist = dist
            delivery_frame = f

    # Component 3: Delivery address horizontal position at 6cm from left (0.25 points)
    try:
        if delivery_frame is not None:
            x_cm = delivery_frame['x_cm']
            if abs(x_cm - 6.0) <= POS_TOLERANCE_CM:
                print(f"PASS: Component 3 - Delivery address at x={x_cm:.2f}cm (target: 6.0cm) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 - Delivery address at x={x_cm:.2f}cm, expected ~6.0cm")
        else:
            print(f"FAIL: Component 3 - No text frames found for delivery address")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Delivery address vertical position at 8cm from top (0.25 points)
    try:
        if delivery_frame is not None:
            y_cm = delivery_frame['y_cm']
            if abs(y_cm - 8.0) <= POS_TOLERANCE_CM:
                print(f"PASS: Component 4 - Delivery address at y={y_cm:.2f}cm (target: 8.0cm) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 - Delivery address at y={y_cm:.2f}cm, expected ~8.0cm")
        else:
            print(f"FAIL: Component 4 - No text frames found for delivery address")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

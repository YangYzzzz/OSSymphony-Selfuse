"""
Reward Script: Insert a rectangle shape with gradient fill (dark blue to light blue)
Task ID: writer_obj_030
Domain: libreoffice_writer
Scoring:
  Component 1: Rectangle shape exists in document (0.30 pts)
  Component 2: Gradient fill with correct start (#0D47A1) and end (#BBDEFB) colors (0.50 pts)
  Component 3: Gradient direction is top-to-bottom (linear, angle 90 degrees) (0.20 pts)
  Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_obj_030'
FILE_PATH = '/home/user/Desktop/header_design.docx'


def persist_app_state():
    """Send Ctrl+S to save any unsaved GUI changes before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def find_rect_shapes(body, ns_a, ns_w):
    """Return list of all prstGeom elements with prst='rect' inside drawing elements."""
    drawing_elements = body.findall(f'.//{{{ns_w}}}drawing')
    rect_geoms = []
    for drw in drawing_elements:
        for geom in drw.findall(f'.//{{{ns_a}}}prstGeom'):
            if geom.get('prst') == 'rect':
                rect_geoms.append((drw, geom))
    return rect_geoms


def find_gradient_stops(drw, ns_a):
    """Return dict of {pos: color_hex} from gradient stops in a drawing element."""
    stop_map = {}
    for gradFill in drw.findall(f'.//{{{ns_a}}}gradFill'):
        for gs in gradFill.findall(f'.//{{{ns_a}}}gs'):
            pos = gs.get('pos')
            srgb = gs.find(f'{{{ns_a}}}srgbClr')
            if srgb is not None and pos is not None:
                stop_map[int(pos)] = srgb.get('val', '').upper()
    return stop_map


def find_linear_angle(drw, ns_a):
    """Return the linear gradient angle (int) from a drawing element, or None if absent."""
    for gradFill in drw.findall(f'.//{{{ns_a}}}gradFill'):
        lin = gradFill.find(f'{{{ns_a}}}lin')
        if lin is not None:
            try:
                return int(lin.get('ang', ''))
            except ValueError:
                return None
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Checks that header_design.docx contains a rectangle shape with
    a linear gradient fill from dark blue (#0D47A1) at the top to
    light blue (#BBDEFB) at the bottom.

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

    ns_w = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    ns_a = 'http://schemas.openxmlformats.org/drawingml/2006/main'

    body = doc.element.body

    # Collect rectangle shapes and their parent drawing elements
    rect_shapes = []
    try:
        rect_shapes = find_rect_shapes(body, ns_a, ns_w)
    except Exception as e:
        print(f"ERROR: Component 1 — shape search failed: {e}")

    # --- Component 1: Rectangle shape exists (0.30 points) ---
    # FAILS on initial (no drawing elements) -> PASSES on golden (has rect shape)
    try:
        num_rect_shapes = len(rect_shapes)
        if num_rect_shapes >= 1:
            print(f"PASS: Component 1 — {num_rect_shapes} rectangle shape(s) found in document (0.30 pts)")
            total_score += 0.30
        else:
            total_drawings = len(body.findall(f'.//{{{ns_w}}}drawing'))
            print(f"FAIL: Component 1 — No rectangle shape found. "
                  f"Total drawing elements: {total_drawings}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # --- Component 2: Gradient fill with correct colors (0.50 points) ---
    # Start color at pos=0 must be #0D47A1 (dark blue, top)
    # End color at pos=100000 must be #BBDEFB (light blue, bottom)
    # FAILS on initial (no drawings) -> PASSES on golden (gradient stops match)
    try:
        matching_color_count = 0
        for drw, _geom in rect_shapes:
            stop_map = find_gradient_stops(drw, ns_a)
            start_color = stop_map.get(0, '')
            end_color = stop_map.get(100000, '')
            start_ok = (start_color == '0D47A1')
            end_ok = (end_color == 'BBDEFB')
            if start_ok and end_ok:
                matching_color_count += 1
                print(f"PASS: Component 2 — Gradient colors correct: "
                      f"start={start_color} (expected 0D47A1), "
                      f"end={end_color} (expected BBDEFB) (0.50 pts)")
            else:
                print(f"FAIL: Component 2 — Gradient colors incorrect: "
                      f"start='{start_color}' (expected 0D47A1), "
                      f"end='{end_color}' (expected BBDEFB)")

        if len(rect_shapes) == 0:
            print("FAIL: Component 2 — No rectangle shapes to check gradient on.")

        if matching_color_count >= 1:
            total_score += 0.50
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # --- Component 3: Gradient direction is top-to-bottom (0.20 points) ---
    # Linear angle 5400000 = 90 degrees = top-to-bottom direction
    # FAILS on initial (no drawings) -> PASSES on golden (angle 5400000)
    try:
        matching_angle_count = 0
        for drw, _geom in rect_shapes:
            ang = find_linear_angle(drw, ns_a)
            if ang == 5400000:
                matching_angle_count += 1
                print(f"PASS: Component 3 — Gradient direction is top-to-bottom "
                      f"(a:lin ang={ang}, 90 degrees) (0.20 pts)")
            elif ang is not None:
                print(f"FAIL: Component 3 — Gradient angle is {ang} "
                      f"(expected 5400000 for 90 degrees top-to-bottom)")
            else:
                print("FAIL: Component 3 — No linear gradient angle element (a:lin) found.")

        if len(rect_shapes) == 0:
            print("FAIL: Component 3 — No rectangle shapes to check gradient direction on.")

        if matching_angle_count >= 1:
            total_score += 0.20
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.1f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


# Persist GUI state before scoring (in case LibreOffice has unsaved changes)
persist_app_state()

if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

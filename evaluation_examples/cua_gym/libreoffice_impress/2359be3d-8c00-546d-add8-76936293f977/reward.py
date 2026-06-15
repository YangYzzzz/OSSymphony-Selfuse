"""
Reward Script: Add horizontal line separator on master slide
Task ID: impress_ma_015
Domain: libreoffice_impress
Scoring:
  Component 1: Line shape exists on master slide (0.3 pts)
  Component 2: Line is horizontal and spans ~full slide width (0.2 pts)
  Component 3: Line positioned at ~y=1.8 inches (0.2 pts)
  Component 4: Stroke weight is 2pt (0.15 pts)
  Component 5: Stroke color is #E0E0E0 (0.15 pts)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_ma_015'


def persist_app_state(domain):
    """Best-effort save any open LibreOffice document."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print(f"PERSIST: ctrl+s sent for {domain}")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def find_line_shapes_on_master(pptx_path):
    """
    Parse the slide master XML to find line/connector shapes.
    Returns list of dicts with shape properties.
    We look in ppt/slideMasters/slideMaster1.xml for cxnSp or sp elements
    that have prstGeom prst='line'.
    """
    ns = {
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    }
    lines = []

    with zipfile.ZipFile(pptx_path, 'r') as zf:
        # Check all slide masters
        master_files = [f for f in zf.namelist() if f.startswith('ppt/slideMasters/slideMaster') and f.endswith('.xml')]
        for mf in master_files:
            with zf.open(mf) as f:
                root = ET.parse(f).getroot()

            # Search for connector shapes (cxnSp) and regular shapes (sp) with line geometry
            for tag_prefix in ['p:cxnSp', 'p:sp']:
                for shape_el in root.findall(f'.//{tag_prefix}', ns):
                    # Check if it's a line (prstGeom prst="line")
                    geom = shape_el.find('.//a:prstGeom', ns)
                    if geom is not None and geom.get('prst') == 'line':
                        info = {'master_file': mf}

                        # Get position and size from xfrm
                        xfrm = shape_el.find('.//a:xfrm', ns)
                        if xfrm is not None:
                            off = xfrm.find('a:off', ns)
                            ext = xfrm.find('a:ext', ns)
                            if off is not None:
                                info['x'] = int(off.get('x', '0'))
                                info['y'] = int(off.get('y', '0'))
                            if ext is not None:
                                info['cx'] = int(ext.get('cx', '0'))
                                info['cy'] = int(ext.get('cy', '0'))

                        # Get line properties
                        ln = shape_el.find('.//a:ln', ns)
                        if ln is not None:
                            info['line_width'] = int(ln.get('w', '0'))
                            # Get color
                            srgb = ln.find('.//a:srgbClr', ns)
                            if srgb is not None:
                                info['color'] = srgb.get('val', '').upper()

                        # Get name
                        cNvPr_paths = [
                            f'p:nvCxnSpPr/p:cNvPr',
                            f'p:nvSpPr/p:cNvPr',
                        ]
                        for cp in cNvPr_paths:
                            cNvPr = shape_el.find(cp, ns)
                            if cNvPr is not None:
                                info['name'] = cNvPr.get('name', '')
                                break

                        lines.append(info)

    return lines


def get_slide_width(pptx_path):
    """Get slide width in EMU from presentation.xml."""
    ns = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
          'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        with zf.open('ppt/presentation.xml') as f:
            root = ET.parse(f).getroot()
        sldSz = root.find('.//p:sldSz', ns)
        if sldSz is not None:
            return int(sldSz.get('cx', '0'))
    return 0


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Find line shapes on master slide
    try:
        line_shapes = find_line_shapes_on_master(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse pptx file: {e}")
        print("REWARD: 0.0")
        return 0.0

    slide_width = get_slide_width(file_path)
    print(f"INFO: Slide width = {slide_width} EMU ({slide_width/914400:.2f} inches)")
    print(f"INFO: Found {len(line_shapes)} line shape(s) on master slide(s)")

    # Filter to horizontal lines (cy == 0 or very small, cx is substantial)
    horizontal_lines = []
    for ls in line_shapes:
        cx = ls.get('cx', 0)
        cy = ls.get('cy', 0)
        if cx > 0 and cy <= 50000:  # horizontal: negligible height
            horizontal_lines.append(ls)

    # Component 1: A line shape exists on the master slide (0.3 points)
    try:
        if len(line_shapes) > 0:
            best_line = line_shapes[0]
            print(f"PASS: Component 1 -- Line shape found on master: name='{best_line.get('name', '')}' (0.3 pts)")
            total_score += 0.3
        else:
            print("FAIL: Component 1 -- No line shape found on master slide")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    if len(line_shapes) == 0:
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Pick the best candidate line (prefer horizontal ones)
    if horizontal_lines:
        line = horizontal_lines[0]
    else:
        line = line_shapes[0]

    print(f"INFO: Evaluating line: x={line.get('x')}, y={line.get('y')}, cx={line.get('cx')}, cy={line.get('cy')}, "
          f"width={line.get('line_width')}, color={line.get('color')}")

    # Component 2: Line is horizontal and spans approximately full slide width (0.2 points)
    try:
        cx = line.get('cx', 0)
        cy = line.get('cy', 0)
        is_horizontal = cy <= 50000  # negligible height
        # Width should be at least 80% of slide width
        width_ratio = cx / slide_width if slide_width > 0 else 0
        spans_width = width_ratio >= 0.8

        if is_horizontal and spans_width:
            print(f"PASS: Component 2 -- Line is horizontal (cy={cy}) and spans {width_ratio*100:.1f}% of slide width (0.2 pts)")
            total_score += 0.2
        else:
            reasons = []
            if not is_horizontal:
                reasons.append(f"not horizontal (cy={cy})")
            if not spans_width:
                reasons.append(f"only spans {width_ratio*100:.1f}% of slide width")
            print(f"FAIL: Component 2 -- {', '.join(reasons)}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Line positioned at approximately y=1.8 inches (0.2 points)
    # 1.8 inches = 1645920 EMU. Allow tolerance of +/- 0.3 inches (274320 EMU)
    try:
        y_pos = line.get('y', 0)
        target_y = 1645920  # 1.8 inches in EMU
        tolerance = 274320  # 0.3 inches in EMU
        y_diff = abs(y_pos - target_y)

        if y_diff <= tolerance:
            print(f"PASS: Component 3 -- Line at y={y_pos/914400:.4f} inches (target ~1.8in, diff={y_diff/914400:.4f}in) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 -- Line at y={y_pos/914400:.4f} inches, expected ~1.8in (diff={y_diff/914400:.4f}in, tolerance=0.3in)")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Stroke weight is 2pt = 25400 EMU (0.15 points)
    # Allow tolerance: 1pt-3pt range (12700-38100 EMU)
    try:
        line_width = line.get('line_width', 0)
        target_width = 25400  # 2pt
        # Accept if within 1pt tolerance
        width_ok = 12700 <= line_width <= 38100

        if width_ok:
            print(f"PASS: Component 4 -- Stroke weight {line_width/12700:.1f}pt (target 2pt) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 -- Stroke weight {line_width/12700:.1f}pt, expected ~2pt")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Stroke color is #E0E0E0 (0.15 points)
    try:
        color = line.get('color', '')
        if color == 'E0E0E0':
            print(f"PASS: Component 5 -- Line color is #{color} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 -- Line color is #{color}, expected #E0E0E0")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_impress")
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

"""
Reward Script: Insert a rectangle shape at the bottom of the flyer with dark blue fill as a footer banner.
Task ID: writer_frd_073
Domain: libreoffice_writer
Scoring:
  Component 1: Rectangle shape exists in document (0.35 points)
  Component 2: Shape filled with dark blue color ~#003366 (0.35 points)
  Component 3: Shape spans page width and positioned at bottom (0.30 points)
"""

import os
import math
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_frd_073'

# Namespace constants for OOXML
WPS_NS = 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape'
A_NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'
WP_NS = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def color_distance_rgb(hex1, hex2):
    """Euclidean distance between two hex color strings (e.g., '003366')."""
    r1, g1, b1 = int(hex1[0:2], 16), int(hex1[2:4], 16), int(hex1[4:6], 16)
    r2, g2, b2 = int(hex2[0:2], 16), int(hex2[2:4], 16), int(hex2[4:6], 16)
    return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
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

    body = doc.element.body

    # Find all wordprocessingShape elements (wps:wsp)
    shapes = body.findall(f'.//{{{WPS_NS}}}wsp')
    anchors = body.findall(f'.//{{{WP_NS}}}anchor')

    # ----------------------------------------------------------------
    # Component 1: A rectangle shape exists in the document (0.35 pts)
    # Initial doc has 0 shapes; golden has 1 rectangle shape.
    # ----------------------------------------------------------------
    rect_shape = None
    rect_anchor = None
    try:
        rect_found = False
        for wsp in shapes:
            prstGeom = wsp.find(f'.//{{{A_NS}}}prstGeom')
            if prstGeom is not None:
                prst = prstGeom.get('prst', '')
                if prst == 'rect':
                    rect_found = True
                    rect_shape = wsp
                    break

        if rect_found:
            print(f"PASS: Component 1 -- Rectangle shape found in document (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 -- No rectangle shape found. Shapes found: {len(shapes)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # If no rectangle found, remaining checks cannot pass
    if rect_shape is None:
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # ----------------------------------------------------------------
    # Component 2: Shape is filled with dark blue color (0.35 pts)
    # Expected: #003366 or perceptually close dark blue.
    # Tolerance: color distance < 60 in RGB space to account for
    # slight variations in how an agent might pick dark blue.
    # ----------------------------------------------------------------
    try:
        solidFill = rect_shape.find(f'.//{{{A_NS}}}solidFill')
        fill_color = None
        if solidFill is not None:
            srgbClr = solidFill.find(f'{{{A_NS}}}srgbClr')
            if srgbClr is not None:
                fill_color = srgbClr.get('val', '').upper()

        if fill_color:
            target_color = '003366'
            dist = color_distance_rgb(fill_color, target_color)
            # Check if it's "dark blue" - also accept navy variants
            # Parse RGB to check it's in the dark blue range
            r = int(fill_color[0:2], 16)
            g = int(fill_color[2:4], 16)
            b = int(fill_color[4:6], 16)

            is_dark_blue = (
                dist < 60  # close to #003366
                or (b > r and b > g and r < 80 and g < 80 and b > 50)  # generic dark blue
            )

            if is_dark_blue:
                print(f"PASS: Component 2 -- Fill color #{fill_color} is dark blue (distance={dist:.1f}) (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 -- Fill color #{fill_color} is not dark blue (distance from #003366={dist:.1f})")
        else:
            print(f"FAIL: Component 2 -- No solid fill color found on rectangle shape")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # ----------------------------------------------------------------
    # Component 3: Shape spans page width and is positioned at bottom (0.30 pts)
    # Expected: cx ~ 7772400 EMU (full page width 8.5"), positioned
    # in the lower portion of the page (positionV > 50% of page height).
    # ----------------------------------------------------------------
    try:
        # Find the anchor that contains our rect shape
        for anchor in anchors:
            anchor_xml = ET.tostring(anchor, encoding='unicode')
            if 'rect' in anchor_xml and 'wsp' in anchor_xml:
                rect_anchor = anchor
                break

        if rect_anchor is None:
            # Try matching by checking if anchor contains the shape
            for anchor in anchors:
                wsp_in_anchor = anchor.findall(f'.//{{{WPS_NS}}}wsp')
                for w in wsp_in_anchor:
                    pg = w.find(f'.//{{{A_NS}}}prstGeom')
                    if pg is not None and pg.get('prst') == 'rect':
                        rect_anchor = anchor
                        break
                if rect_anchor:
                    break

        width_ok = False
        position_ok = False

        # Check width from extent or xfrm
        extent = None
        if rect_anchor is not None:
            extent = rect_anchor.find(f'{{{WP_NS}}}extent')
        if extent is None:
            # Try from shape's own xfrm
            ext_el = rect_shape.find(f'.//{{{A_NS}}}xfrm/{{{A_NS}}}ext')
            if ext_el is not None:
                cx = int(ext_el.get('cx', '0'))
            else:
                cx = 0
        else:
            cx = int(extent.get('cx', '0'))

        # Page width for reference
        section = doc.sections[0]
        page_width = section.page_width  # EMU

        # Shape should span at least 80% of page width to count as "spanning the page"
        if page_width and cx >= page_width * 0.8:
            width_ok = True
            print(f"  Width check: cx={cx} EMU ({cx/914400:.2f} in), page_width={page_width} EMU -- spans page")
        else:
            print(f"  Width check: cx={cx} EMU ({cx/914400:.2f} in), page_width={page_width} EMU -- does NOT span page")

        # Check vertical position - should be in lower half of page
        if rect_anchor is not None:
            posV = rect_anchor.find(f'{{{WP_NS}}}positionV')
            if posV is not None:
                offset_el = posV.find(f'{{{WP_NS}}}posOffset')
                if offset_el is not None and offset_el.text:
                    v_offset = int(offset_el.text)
                    page_height = section.page_height
                    # Position should be in lower 40% of page (> 60% from top)
                    if page_height and v_offset > page_height * 0.6:
                        position_ok = True
                        print(f"  Position check: positionV={v_offset} EMU ({v_offset/914400:.2f} in), page_height={page_height} EMU -- at bottom")
                    else:
                        print(f"  Position check: positionV={v_offset} EMU ({v_offset/914400:.2f} in), page_height={page_height} EMU -- NOT at bottom")
                else:
                    print(f"  Position check: no posOffset found in positionV")
            else:
                # Might use simplePos or be at default position
                print(f"  Position check: no positionV element found")
        else:
            print(f"  Position check: no anchor element found for rectangle")

        if width_ok and position_ok:
            print(f"PASS: Component 3 -- Shape spans page width and is at bottom (0.30 pts)")
            total_score += 0.30
        elif width_ok or position_ok:
            partial = 0.15
            print(f"PARTIAL: Component 3 -- Only {'width' if width_ok else 'position'} check passed ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 -- Shape does not span page width or is not at bottom")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook for LibreOffice Writer
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
persist_app_state()

if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

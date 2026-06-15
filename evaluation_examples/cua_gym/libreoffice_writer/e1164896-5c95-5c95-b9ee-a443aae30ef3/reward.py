"""
Reward Script: Add CONFIDENTIAL watermark to contract document
Task ID: writer_biz_046
Domain: libreoffice_writer
Scoring:
  Component 1: Watermark shape exists in header (0.30 pts)
  Component 2: Watermark text is 'CONFIDENTIAL' (0.25 pts)
  Component 3: Watermark is rotated diagonally (0.25 pts)
  Component 4: Watermark fill is light gray / semi-transparent (0.20 pts)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_biz_046'


def persist_app_state(domain: str):
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
    Verify that a CONFIDENTIAL watermark has been added diagonally
    in light gray across the document pages.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        import lxml.etree as ET
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Namespaces used for XML inspection
    ns = {
        'v': 'urn:schemas-microsoft-com:vml',
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
        'w10': 'urn:schemas-microsoft-com:office:word',
        'o': 'urn:schemas-microsoft-com:office:office',
    }

    # Collect all v:shape elements from ALL section headers
    watermark_shapes = []
    textpath_strings = []

    for section in doc.sections:
        hdr = section.header
        hdr_xml_str = ET.tostring(hdr._element, pretty_print=True).decode()

        # Find v:shape elements in header
        shapes = hdr._element.findall('.//v:shape', ns)
        for shape in shapes:
            watermark_shapes.append(shape)
            # Extract textpath string attribute
            tp_elems = shape.findall('.//v:textpath', ns)
            for tp in tp_elems:
                s = tp.get('string', '')
                if s:
                    textpath_strings.append(s)

        # Also check for mc:AlternateContent / wps:wsp patterns (DrawingML watermarks)
        # These use a different XML structure but can also carry watermark text
        alt_ns = {'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006'}
        alt_contents = hdr._element.findall('.//mc:AlternateContent', alt_ns)
        if alt_contents and not shapes:
            # Check if CONFIDENTIAL appears in the raw header XML
            if 'CONFIDENTIAL' in hdr_xml_str:
                # Treat as a watermark shape for scoring
                watermark_shapes.append(alt_contents[0])
                textpath_strings.append('CONFIDENTIAL')

    # =========================================================================
    # Component 1: Watermark shape exists in at least one header (0.30 points)
    # This FAILS on initial (no shapes in header) and PASSES on golden.
    # =========================================================================
    try:
        if len(watermark_shapes) > 0:
            print(f"PASS: Component 1 — Watermark shape found in header ({len(watermark_shapes)} shape(s)) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — No watermark shape found in any section header")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # =========================================================================
    # Component 2: Watermark text is 'CONFIDENTIAL' (0.25 points)
    # Checks that the textpath string attribute contains CONFIDENTIAL.
    # =========================================================================
    try:
        confidential_found = any(
            'CONFIDENTIAL' in s.upper() for s in textpath_strings
        )
        if confidential_found:
            print(f"PASS: Component 2 — Watermark text is 'CONFIDENTIAL' (found: {textpath_strings}) (0.25 pts)")
            total_score += 0.25
        else:
            # Fallback: search raw header XML for CONFIDENTIAL in any shape-like context
            fallback_found = False
            for section in doc.sections:
                hdr_xml = ET.tostring(section.header._element).decode()
                if 'CONFIDENTIAL' in hdr_xml and ('v:shape' in hdr_xml or 'wps:wsp' in hdr_xml or 'mc:AlternateContent' in hdr_xml):
                    fallback_found = True
                    break
            if fallback_found:
                print(f"PASS: Component 2 — 'CONFIDENTIAL' found in header shape XML (fallback) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 — Watermark text is not 'CONFIDENTIAL'. Found textpaths: {textpath_strings}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # =========================================================================
    # Component 3: Watermark is rotated diagonally (0.25 points)
    # Diagonal watermarks typically use rotation of 315 (or -45, or 330, etc.)
    # We accept any rotation that makes the text diagonal (not 0, not 90, not 180, not 270).
    # =========================================================================
    try:
        rotation_found = False
        for shape in watermark_shapes:
            style_attr = shape.get('style', '')
            # Parse rotation from style attribute, e.g., "rotation:315"
            rot_match = re.search(r'rotation[:\s]*(-?\d+\.?\d*)', style_attr)
            if rot_match:
                rot_val = float(rot_match.group(1))
                # Diagonal means not axis-aligned: not 0, 90, 180, 270
                if rot_val % 90 != 0:
                    rotation_found = True
                    print(f"PASS: Component 3 — Watermark is rotated diagonally (rotation={rot_val}) (0.25 pts)")
                    break

        if rotation_found:
            total_score += 0.25
        else:
            # Fallback: check raw XML for rotation in style
            for section in doc.sections:
                hdr_xml = ET.tostring(section.header._element).decode()
                rot_match = re.search(r'rotation[:\s]*(-?\d+\.?\d*)', hdr_xml)
                if rot_match:
                    rot_val = float(rot_match.group(1))
                    if rot_val % 90 != 0:
                        rotation_found = True
                        print(f"PASS: Component 3 — Diagonal rotation found in header XML (rotation={rot_val}) (0.25 pts)")
                        total_score += 0.25
                        break
            if not rotation_found:
                print(f"FAIL: Component 3 — No diagonal rotation found on watermark shape")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # =========================================================================
    # Component 4: Watermark fill is light gray / semi-transparent (0.20 points)
    # Acceptable: fillcolor=silver/gray/#C0C0C0/etc., or opacity < 1.0,
    # or any light color (high luminance).
    # =========================================================================
    try:
        light_color_found = False
        light_gray_keywords = ['silver', 'gray', 'grey', 'light', '#c0c0c0', '#d3d3d3', '#a9a9a9', '#808080']

        for shape in watermark_shapes:
            fillcolor = (shape.get('fillcolor') or '').lower()
            # Check fill color
            if any(kw in fillcolor for kw in light_gray_keywords):
                light_color_found = True
                print(f"PASS: Component 4 — Watermark fill color is light gray (fillcolor={fillcolor}) (0.20 pts)")
                break
            # Check v:fill sub-element for opacity
            fill_elems = shape.findall('.//v:fill', ns)
            for fill_elem in fill_elems:
                opacity = fill_elem.get('opacity', '')
                if opacity:
                    # Opacity < 1.0 means semi-transparent (light appearance)
                    try:
                        op_val = float(opacity.strip('.'))
                        if op_val < 1.0:
                            light_color_found = True
                            print(f"PASS: Component 4 — Watermark has reduced opacity ({opacity}), appearing light (0.20 pts)")
                            break
                    except ValueError:
                        pass
            if light_color_found:
                break

        if not light_color_found:
            # Fallback: check raw header XML for color/opacity indicators
            for section in doc.sections:
                hdr_xml = ET.tostring(section.header._element).decode().lower()
                if any(kw in hdr_xml for kw in light_gray_keywords):
                    light_color_found = True
                    print(f"PASS: Component 4 — Light gray color found in header XML (fallback) (0.20 pts)")
                    break
                if 'opacity' in hdr_xml:
                    op_match = re.search(r'opacity[=:"]*([0-9.]+)', hdr_xml)
                    if op_match:
                        try:
                            op_val = float(op_match.group(1))
                            if op_val < 1.0:
                                light_color_found = True
                                print(f"PASS: Component 4 — Semi-transparent opacity found in header XML (fallback) (0.20 pts)")
                                break
                        except ValueError:
                            pass

        if light_color_found:
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — Watermark fill is not light gray or semi-transparent")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(round(total_score, 2), 1.0)
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

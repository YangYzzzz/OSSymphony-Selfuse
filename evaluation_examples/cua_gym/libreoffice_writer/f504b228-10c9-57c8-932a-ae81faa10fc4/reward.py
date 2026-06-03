"""
Reward Script: Add a watermark text 'DRAFT' diagonally across every page of thesis manuscript
Task ID: writer_acad_070
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35) - Header contains a VML shape / pict element with watermark
  Component 2 (0.30) - Watermark text is 'DRAFT'
  Component 3 (0.20) - Watermark is diagonal (rotation ~315 or ~-45 degrees)
  Component 4 (0.15) - Watermark is light/gray color and behind text (z-index < 0)
"""

import os
import re
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_acad_070'

VML_NS = 'urn:schemas-microsoft-com:vml'
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
W10_NS = 'urn:schemas-microsoft-com:office:word'
O_NS = 'urn:schemas-microsoft-com:office:office'


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

    # Collect all VML shapes and pict elements from all section headers
    all_vml_shapes = []
    all_picts = []
    watermark_shape = None
    watermark_textpath = None

    for i, section in enumerate(doc.sections):
        header = section.header
        header_xml = etree.tostring(header._element, pretty_print=True).decode()

        # Find VML shapes in header
        shapes = header._element.findall(f'.//{{{VML_NS}}}shape')
        all_vml_shapes.extend(shapes)

        # Find w:pict elements in header
        picts = header._element.findall(f'.//{{{W_NS}}}pict')
        all_picts.extend(picts)

        # Look for a shape that looks like a watermark
        for shape in shapes:
            shape_id = shape.get('id', '')
            shape_style = shape.get('style', '')
            # Check for PowerPlusWaterMarkObject or watermark-like indicators
            if 'watermark' in shape_id.lower() or 'powerpluswatermark' in shape_id.lower():
                watermark_shape = shape
            elif 'z-index:-' in shape_style.replace(' ', ''):
                # Behind-text shape is a watermark candidate
                watermark_shape = shape

            # Get textpath element
            textpaths = shape.findall(f'{{{VML_NS}}}textpath')
            for tp in textpaths:
                tp_string = tp.get('string', '')
                if tp_string:
                    watermark_textpath = tp

    # Component 1: Header contains a VML shape/pict with watermark characteristics (0.35 points)
    try:
        if watermark_shape is not None:
            print(f"PASS: Component 1 - Found watermark VML shape in header (id={watermark_shape.get('id', 'unknown')}) (0.35 pts)")
            total_score += 0.35
        elif len(all_picts) > 0 and len(all_vml_shapes) > 0:
            # Check if any VML shape has a textpath - that's a text watermark
            for shape in all_vml_shapes:
                textpaths = shape.findall(f'{{{VML_NS}}}textpath')
                if textpaths:
                    watermark_shape = shape
                    for tp in textpaths:
                        if tp.get('string', ''):
                            watermark_textpath = tp
                    break
            if watermark_shape is not None:
                print(f"PASS: Component 1 - Found VML shape with textpath in header (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 1 - No watermark-like VML shape found in headers")
        else:
            print(f"FAIL: Component 1 - No VML shapes ({len(all_vml_shapes)}) or pict elements ({len(all_picts)}) found in headers")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Watermark text is 'DRAFT' (0.30 points)
    try:
        if watermark_textpath is not None:
            draft_text = watermark_textpath.get('string', '')
            if draft_text.strip().upper() == 'DRAFT':
                print(f"PASS: Component 2 - Watermark text is 'DRAFT' (found: '{draft_text}') (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 2 - Watermark text is '{draft_text}', expected 'DRAFT'")
        elif watermark_shape is not None:
            # Try to find text in the shape XML
            shape_xml = etree.tostring(watermark_shape, pretty_print=True).decode()
            if 'DRAFT' in shape_xml:
                print(f"PASS: Component 2 - 'DRAFT' text found in watermark shape XML (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 2 - No 'DRAFT' text found in watermark shape")
        else:
            # Last resort: check all header XML for DRAFT in any shape context
            found_draft = False
            for section in doc.sections:
                header_xml = etree.tostring(section.header._element, pretty_print=True).decode()
                if 'DRAFT' in header_xml and ('shape' in header_xml.lower() or 'pict' in header_xml.lower()):
                    found_draft = True
                    break
            if found_draft:
                print(f"PASS: Component 2 - 'DRAFT' text found in header shape context (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 2 - No watermark shape with 'DRAFT' text found")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Watermark is diagonal (rotation ~315 or ~-45 degrees) (0.20 points)
    try:
        if watermark_shape is not None:
            style_attr = watermark_shape.get('style', '')
            rotation_match = re.search(r'rotation:\s*([\d.]+)', style_attr)
            if rotation_match:
                rotation_val = float(rotation_match.group(1))
                # 315 degrees or 345 degrees are both diagonal; accept range 300-350 or equivalent
                # Also accept -45 == 315
                is_diagonal = (295 <= rotation_val <= 355) or (rotation_val < 0 and -65 <= rotation_val <= -25)
                if is_diagonal:
                    print(f"PASS: Component 3 - Watermark rotation is {rotation_val} degrees (diagonal) (0.20 pts)")
                    total_score += 0.20
                else:
                    print(f"FAIL: Component 3 - Watermark rotation is {rotation_val} degrees, expected ~315 (diagonal)")
            else:
                # Check XML attribute directly
                rotation_attr = watermark_shape.get('rotation')
                if rotation_attr:
                    rot_val = float(rotation_attr)
                    is_diagonal = (295 <= rot_val <= 355) or (rot_val < 0 and -65 <= rot_val <= -25)
                    if is_diagonal:
                        print(f"PASS: Component 3 - Watermark rotation attribute is {rot_val} (diagonal) (0.20 pts)")
                        total_score += 0.20
                    else:
                        print(f"FAIL: Component 3 - Rotation attribute is {rot_val}, expected ~315")
                else:
                    print(f"FAIL: Component 3 - No rotation found in watermark shape style: {style_attr[:200]}")
        else:
            print(f"FAIL: Component 3 - No watermark shape to check rotation")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Watermark is light gray color and behind text (0.15 points)
    try:
        if watermark_shape is not None:
            style_attr = watermark_shape.get('style', '')
            fill_color = watermark_shape.get('fillcolor', '')
            stroked = watermark_shape.get('stroked', '')

            # Check z-index is negative (behind text)
            z_match = re.search(r'z-index:\s*(-?\d+)', style_attr)
            behind_text = False
            if z_match:
                z_val = int(z_match.group(1))
                behind_text = z_val < 0

            # Check fill color is light/gray/silver
            is_light_color = False
            light_colors = ['silver', 'gray', 'grey', 'lightgray', 'lightgrey', '#c0c0c0', '#d3d3d3', '#808080', '#a9a9a9']
            if fill_color.lower() in light_colors:
                is_light_color = True
            elif fill_color.startswith('#'):
                # Parse hex color and check if it's light gray
                try:
                    r = int(fill_color[1:3], 16)
                    g = int(fill_color[3:5], 16)
                    b = int(fill_color[5:7], 16)
                    # Light gray: all channels similar and > 128
                    if r > 100 and g > 100 and b > 100 and abs(r - g) < 50 and abs(g - b) < 50:
                        is_light_color = True
                except (ValueError, IndexError):
                    pass

            # Also check fill opacity
            fill_elements = watermark_shape.findall(f'{{{VML_NS}}}fill')
            has_reduced_opacity = False
            for fill_el in fill_elements:
                opacity = fill_el.get('opacity', '1')
                try:
                    if '.' in opacity:
                        op_val = float(opacity)
                    elif '%' in opacity:
                        op_val = float(opacity.replace('%', '')) / 100
                    else:
                        op_val = float(opacity)
                    if op_val < 1.0:
                        has_reduced_opacity = True
                except (ValueError, TypeError):
                    pass

            if behind_text and (is_light_color or has_reduced_opacity):
                details = f"z-index<0={behind_text}, fillcolor={fill_color}, reduced_opacity={has_reduced_opacity}"
                print(f"PASS: Component 4 - Watermark is behind text with light color ({details}) (0.15 pts)")
                total_score += 0.15
            elif behind_text:
                print(f"PARTIAL: Component 4 - Watermark is behind text but color uncertain (fillcolor={fill_color}) (0.08 pts)")
                total_score += 0.08
            elif is_light_color or has_reduced_opacity:
                print(f"PARTIAL: Component 4 - Watermark has light color but z-index unclear (0.08 pts)")
                total_score += 0.08
            else:
                print(f"FAIL: Component 4 - Watermark not behind text or not light color (z={z_match}, fillcolor={fill_color})")
        else:
            print(f"FAIL: Component 4 - No watermark shape to check color/position")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = round(min(total_score, 1.0), 2)
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

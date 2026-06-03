"""
Reward Script: Add a 'CONFIDENTIAL' watermark diagonally across every page
Task ID: writer_tech_038
Domain: libreoffice_writer
Scoring:
  Component 1: Watermark shape exists in header (0.3 pts)
  Component 2: Watermark text is 'CONFIDENTIAL' (0.35 pts)
  Component 3: Watermark is diagonal (rotation applied) (0.35 pts)
"""

import os
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_tech_038'

# Namespaces used in OOXML VML watermarks
NS = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'v': 'urn:schemas-microsoft-com:vml',
    'o': 'urn:schemas-microsoft-com:office:office',
    'w10': 'urn:schemas-microsoft-com:office:word',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}


def verify_task(file_path):
    """
    Verify that a 'CONFIDENTIAL' diagonal watermark has been added to the document.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the document as a python-docx Document to access headers
    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # We need to inspect the header XML for VML watermark shapes.
    # A standard Word watermark is placed as a VML shape (v:shape with v:textpath)
    # inside the header part (w:hdr) of each section.
    # It can also be implemented as a DrawingML shape in the header.

    import re

    watermark_shape_count = 0  # count of textpath shapes found
    watermark_text = None
    watermark_rotation = None

    # Check all sections' headers for a watermark shape
    for section in doc.sections:
        hdr = section.header
        hdr_xml = etree.tostring(hdr._element, pretty_print=True).decode()

        # Strategy 1: Look for VML textpath watermark (classic Word watermark)
        # Parse header element for v:shape elements containing v:textpath
        hdr_elem = hdr._element

        # Find w:pict elements (VML container in OOXML)
        pict_elements = hdr_elem.findall('.//w:pict', NS)
        for pict in pict_elements:
            # Look for v:shape elements
            shapes = pict.findall('.//v:shape', NS)
            for shape in shapes:
                # Check for textpath child (indicates text watermark)
                textpaths = shape.findall('.//v:textpath', NS)
                # Increment count based on actual XML elements found
                watermark_shape_count += len(textpaths)
                for tp in textpaths:
                    string_val = tp.get('string', '')
                    if string_val:
                        watermark_text = string_val

                # Check rotation from style attribute
                style = shape.get('style', '')
                rot_match = re.search(r'rotation:\s*(-?\d+\.?\d*)', style)
                if rot_match:
                    watermark_rotation = float(rot_match.group(1))

        # Strategy 2: Look for DrawingML (wps:wsp) shapes in header
        # These use a different XML structure with a:bodyPr rot attribute
        if watermark_shape_count == 0:
            # Search raw XML for shape elements with CONFIDENTIAL text
            confidential_count = hdr_xml.upper().count('CONFIDENTIAL')
            if confidential_count > 0:
                watermark_shape_count += confidential_count
                watermark_text = 'CONFIDENTIAL'
                # Try to find rotation in DrawingML
                rot_match = re.search(r'rot="(\d+)"', hdr_xml)
                if rot_match:
                    # DrawingML rotation is in 60000ths of a degree
                    rot_val = int(rot_match.group(1))
                    watermark_rotation = rot_val / 60000.0

        if watermark_shape_count > 0:
            break  # Found in at least one section header

    # Component 1: Watermark shape exists in header (0.3 points)
    # This checks that a shape/textpath object has been added to the header,
    # which is NOT present in the initial document.
    try:
        if watermark_shape_count > 0:
            print(f"PASS: Component 1 -- Watermark shape found in header ({watermark_shape_count} textpath element(s)) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 -- No watermark shape found in any section header")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Watermark text is 'CONFIDENTIAL' (0.35 points)
    # The textpath string attribute must contain 'CONFIDENTIAL'
    try:
        if watermark_text and 'CONFIDENTIAL' in watermark_text.upper():
            print(f"PASS: Component 2 -- Watermark text is '{watermark_text}' (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 -- Expected watermark text 'CONFIDENTIAL', found: {watermark_text}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Watermark is diagonal (rotation applied) (0.35 points)
    # A diagonal watermark typically has rotation of 315 degrees (or -45 degrees)
    # We accept any non-zero rotation as evidence of diagonal placement
    try:
        if watermark_rotation is not None and watermark_rotation != 0:
            print(f"PASS: Component 3 -- Watermark has rotation {watermark_rotation} degrees (0.35 pts)")
            total_score += 0.35
        else:
            # Even without explicit rotation attribute, if the style contains rotation info
            # re-check the raw header XML for any rotation indicator
            for section in doc.sections:
                hdr_xml = etree.tostring(section.header._element, pretty_print=True).decode()
                import re
                if re.search(r'rotation[:\s]', hdr_xml, re.IGNORECASE):
                    print(f"PASS: Component 3 -- Rotation attribute found in header XML (0.35 pts)")
                    total_score += 0.35
                    break
            else:
                print(f"FAIL: Component 3 -- No rotation found on watermark. Rotation value: {watermark_rotation}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

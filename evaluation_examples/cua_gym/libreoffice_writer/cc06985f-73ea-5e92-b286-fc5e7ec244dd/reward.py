"""
Reward Script: Remove the border from the text box on page 1 so it has no visible frame.
Task ID: writer_obj_022
Domain: libreoffice_writer
Scoring:
  Component 1 (0.6 pts): Text box border line element contains <a:noFill/> (border set to None)
  Component 2 (0.4 pts): Text box border line element has no solidFill with black color (original border removed)
  Total: 1.0
"""

import os
from docx import Document
from lxml import etree

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_obj_022'

# Namespace definitions for OOXML drawing elements
NS_W   = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS_A   = 'http://schemas.openxmlformats.org/drawingml/2006/main'
NS_WPS = 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Task: Remove the border from the text box on page 1 so it has no visible frame.

    Initial state: text box has <a:ln w="12700"> with <a:solidFill><a:srgbClr val="000000"/> (solid black border)
    Golden state:  text box has <a:ln><a:noFill/></a:ln> (border set to None / no fill)

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the document
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find all drawing elements in the document body
    try:
        drawings = doc.element.body.findall(f'.//{{{NS_W}}}drawing')
        if not drawings:
            print("FAIL: No drawing (text box) elements found in document")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
        print(f"INFO: Found {len(drawings)} drawing element(s)")
    except Exception as e:
        print(f"CRITICAL: Cannot search for drawing elements: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Text box border line contains <a:noFill/> (border removed / set to None) (0.6 points)
    # This is the core task requirement: border should be set to 'None' so no border line is visible.
    # In golden state: <a:ln><a:noFill/></a:ln>
    # In initial state: <a:ln w="12700"><a:solidFill>...</a:solidFill></a:ln>  -- no noFill present
    try:
        no_fill_found = False
        for draw in drawings:
            # Find line elements <a:ln> within wps:spPr
            spPr_list = draw.findall(f'.//{{{NS_WPS}}}spPr')
            for spPr in spPr_list:
                ln_elems = spPr.findall(f'{{{NS_A}}}ln')
                for ln in ln_elems:
                    no_fill_elems = ln.findall(f'{{{NS_A}}}noFill')
                    if no_fill_elems:
                        no_fill_found = True
                        print(f"PASS: Component 1 — text box border line contains <a:noFill/> (border removed)")
                        total_score += 0.6
                        break
                if no_fill_found:
                    break
            if no_fill_found:
                break

        if not no_fill_found:
            print("FAIL: Component 1 — text box border does not contain <a:noFill/>; border has not been removed")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Text box border line does NOT have solidFill with black (000000) color (0.4 points)
    # The original border was <a:solidFill><a:srgbClr val="000000"/></a:solidFill> in the <a:ln> element.
    # After task completion, this solidFill should be gone from the border line.
    try:
        original_border_absent = True
        for draw in drawings:
            spPr_list = draw.findall(f'.//{{{NS_WPS}}}spPr')
            for spPr in spPr_list:
                ln_elems = spPr.findall(f'{{{NS_A}}}ln')
                for ln in ln_elems:
                    solid_fill_elems = ln.findall(f'{{{NS_A}}}solidFill')
                    for sf in solid_fill_elems:
                        # Check for srgbClr elements (any color means a solid border)
                        srgb_elems = sf.findall(f'{{{NS_A}}}srgbClr')
                        if srgb_elems:
                            original_border_absent = False
                            val = srgb_elems[0].get('val', 'unknown')
                            print(f"FAIL: Component 2 — text box border still has solidFill color: #{val}")

        if original_border_absent:
            print("PASS: Component 2 — text box border has no solidFill color (original black border removed)")
            total_score += 0.4
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/sidebar_doc.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

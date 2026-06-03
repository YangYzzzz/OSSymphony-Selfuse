"""
Reward Script: Set text box background color to light yellow (#FFFDE7)
Task ID: writer_obj_019
Domain: libreoffice_writer
Scoring:
  Component 1: Text box has a solid fill background (not transparent/noFill)  — 0.6 points
  Component 2: The solid fill color is exactly FFFDE7 (#FFFDE7)               — 0.4 points
  Total: 1.0
"""

import os
import re

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_obj_019'
FILE_PATH = f'{WORKDIR}/callout_doc.docx'

TARGET_COLOR = 'FFFDE7'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.

    The task requires setting the text box background from transparent (noFill)
    to light yellow solid fill (#FFFDE7).

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must be loadable
    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract the wps:spPr XML from the document body to inspect shape properties
    body_xml = doc.element.body.xml

    # Locate the shape properties block (wps:spPr) for the text box
    spPr_matches = re.findall(r'<wps:spPr[^>]*>.*?</wps:spPr>', body_xml, re.DOTALL)

    if not spPr_matches:
        print("FAIL: No text box shape properties (wps:spPr) found in document.")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Use the first text box shape properties block
    spPr_xml = spPr_matches[0]

    # Component 1: Text box has a solidFill background (not noFill/transparent) — 0.6 points
    # Initial env has <a:noFill/>, golden env has <a:solidFill>...
    # We check that noFill is absent and a solidFill is present OUTSIDE of <a:ln> (border element)
    try:
        # Remove the <a:ln> section so we don't accidentally match the border solidFill
        spPr_no_border = re.sub(r'<a:ln[^>]*>.*?</a:ln>', '', spPr_xml, flags=re.DOTALL)

        has_no_fill = '<a:noFill' in spPr_no_border
        has_solid_fill = '<a:solidFill' in spPr_no_border

        if has_solid_fill and not has_no_fill:
            print(f"PASS: Component 1 — Text box has solidFill background (not transparent) (0.6 pts)")
            total_score += 0.6
        elif has_no_fill:
            print(f"FAIL: Component 1 — Text box background is still transparent (noFill found, no solidFill)")
        else:
            print(f"FAIL: Component 1 — No solidFill found in text box shape properties")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The solidFill color matches exactly FFFDE7 (#FFFDE7, light yellow) — 0.4 points
    # The golden file has: <a:solidFill><a:srgbClr val="FFFDE7"/></a:solidFill>
    # We check the background fill color (outside the border element)
    try:
        spPr_no_border = re.sub(r'<a:ln[^>]*>.*?</a:ln>', '', spPr_xml, flags=re.DOTALL)

        # Extract srgbClr values from any solidFill elements in the background area
        fill_colors = re.findall(
            r'<a:solidFill[^>]*>\s*<a:srgbClr val="([A-Fa-f0-9]{6})"',
            spPr_no_border,
            re.DOTALL
        )

        if fill_colors:
            actual_color = fill_colors[0].upper()
            if actual_color == TARGET_COLOR.upper():
                print(f"PASS: Component 2 — Text box fill color is #{actual_color} (matches target #FFFDE7) (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 — Text box fill color is #{actual_color}, expected #{TARGET_COLOR}")
        else:
            print(f"FAIL: Component 2 — No srgbClr color value found in text box solidFill")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

"""
FINAL REWARD SCRIPT - SUCCESS
Task: I'm working on sprucing up my slide deck. How can I change the fill on my Fontwork text to transition smoothly from blue (#0000FF) to cyan (#00FFFF)?
Generated: 2025-08-07 09:03:29
Status: success
Model: o4-mini
Total Steps: 1
"""

import os
import zipfile
import xml.etree.ElementTree as ET


def verify_fontwork_gradient(file_path):
    """
    Verifies that a PPTX file at file_path contains Fontwork text with a gradient fill
    transitioning smoothly from blue (#0000FF) to cyan (#00FFFF). Returns and prints
    a progressive score between 0.0 and 1.0 based on verification steps.
    """
    score = 0.0
    max_score = 1.0
    # Namespaces for XML parsing
    ns = {
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'
    }
    print(f"Checking file: {file_path}")

    # Requirement 1: File exists (0.2 points)
    if os.path.exists(file_path):
        print("✓ File exists (0.2 points)")
        score += 0.2
    else:
        print("✗ File not found (0 points)")
        print(f"Final score: {score}")
        print(f"REWARD: {score}")
        return score

    # Requirement 2: Open PPTX as ZIP (no direct points, prerequisite)
    try:
        pptx_zip = zipfile.ZipFile(file_path, 'r')
        print("✓ Opened PPTX as zip (0 points)")
    except Exception as e:
        print(f"✗ Error opening PPTX: {e} (0 points)")
        print(f"Final score: {score}")
        print(f"REWARD: {score}")
        return score

    # Find slide XML files
    slide_files = [f for f in pptx_zip.namelist()
                   if f.startswith('ppt/slides/slide') and f.endswith('.xml')]
    if not slide_files:
        print("✗ No slides found in PPTX (0 points)")
        print(f"Final score: {score}")
        print(f"REWARD: {score}")
        return score

    # Requirement 3: Find a gradient fill on a shape (0.2 points)
    found_grad = False
    for slide in slide_files:
        xml_content = pptx_zip.read(slide)
        root = ET.fromstring(xml_content)
        for sp in root.findall('.//p:sp', ns):
            spPr = sp.find('p:spPr', ns)
            if spPr is None:
                continue
            gradFill = spPr.find('a:gradFill', ns)
            if gradFill is not None:
                print(f"✓ Found gradFill in {slide} (0.2 points)")
                score += 0.2
                found_grad = True

                # Requirement 4: Check gradient stops count (0.2 points)
                gsLst = gradFill.find('a:gsLst', ns)
                if gsLst is not None:
                    stops = gsLst.findall('a:gs', ns)
                    print(f"  ✓ Found {len(stops)} gradient stops")
                    if len(stops) >= 2:
                        print("  ✓ Sufficient gradient stops (0.2 points)")
                        score += 0.2
                    else:
                        print("  ✗ Insufficient gradient stops (0 points)")

                    # Requirement 5: Verify color values at positions 0 and 100000 (0.4 points)
                    pos_color = {}
                    for stop in stops:
                        pos = stop.get('pos')
                        srgbClr = stop.find('a:srgbClr', ns)
                        if pos is not None and srgbClr is not None:
                            pos_color[pos] = srgbClr.get('val').upper()
                    if pos_color.get('0') == '0000FF' and pos_color.get('100000') == '00FFFF':
                        print("  ✓ Gradient colors match blue to cyan (0.4 points)")
                        score += 0.4
                    else:
                        print(f"  ✗ Gradient colors incorrect: {pos_color} (0 points)")
                else:
                    print("  ✗ No gradient stops list found (0 points)")
                break
        if found_grad:
            break

    if not found_grad:
        print("✗ No gradient fill shapes found (0 points)")

    # Final score, capped at max_score
    final_score = min(score, max_score)
    print(f"Final score: {final_score}")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    # Path to the PPTX file to verify
    file_path = '/home/user/im_working_on_sprucing_up_my_slide_deck_how_can_i_change_the_fill_on_my_fontwork_text_to_transition_.pptx'
    verify_fontwork_gradient(file_path)

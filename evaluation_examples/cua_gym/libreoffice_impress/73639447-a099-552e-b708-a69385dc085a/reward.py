"""
Reward Script: Enable slide numbering starting from 0 instead of 1
Task ID: impress_slides_035
Domain: libreoffice_impress
Scoring:
  Component 1: firstSlideNum attribute set to 0 in presentation.xml (0.7 pts)
  Component 2: firstSlideNum is 0 AND presentation has exactly 10 slides (0.3 pts)
  Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'impress_slides_035'

# Namespace for presentation XML
PPTX_NS = 'http://schemas.openxmlformats.org/presentationml/2006/main'


def get_first_slide_num(pptx_path):
    """Read firstSlideNum attribute from ppt/presentation.xml inside the pptx archive."""
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        with zf.open('ppt/presentation.xml') as f:
            root = ET.parse(f).getroot()
            # firstSlideNum is an attribute of the root <p:presentation> element
            first_slide_num_str = root.get('firstSlideNum')
            if first_slide_num_str is None:
                # Default is 1 when not specified
                return 1
            return int(first_slide_num_str)


def get_slide_count(pptx_path):
    """Count the number of slides in the pptx file."""
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        # ppt/slides/ directory contains slideN.xml files
        slide_files = [name for name in zf.namelist()
                       if name.startswith('ppt/slides/slide') and name.endswith('.xml')]
        return len(slide_files)


def verify_task(file_path):
    """
    Verify that slide numbering starts from 0 instead of 1.

    The task requires setting 'Number slides from' to 0 in Slide Properties,
    which sets firstSlideNum="0" in ppt/presentation.xml.

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must be loadable as a valid pptx/zip
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            namelist = zf.namelist()
            if 'ppt/presentation.xml' not in namelist:
                print(f"CRITICAL: 'ppt/presentation.xml' not found in {file_path}")
                print("REWARD: 0.0")
                return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot open file as zip archive {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: firstSlideNum attribute is set to 0 (0.7 points)
    # This FAILS on initial (firstSlideNum=1) and PASSES on golden (firstSlideNum=0)
    try:
        first_slide_num = get_first_slide_num(file_path)
        if first_slide_num == 0:
            print(f"PASS: Component 1 — firstSlideNum is 0 (0.7 pts)")
            total_score += 0.7
        else:
            print(f"FAIL: Component 1 — expected firstSlideNum=0, found firstSlideNum={first_slide_num}")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not read firstSlideNum: {e}")

    # Component 2: firstSlideNum is 0 AND slide count remains 10 (0.3 points)
    # This verifies the task was completed without corrupting the presentation structure.
    # Conditioned on firstSlideNum == 0 (fails on initial), so it does not award points
    # for preconditions.
    try:
        first_slide_num = get_first_slide_num(file_path)
        slide_count = get_slide_count(file_path)
        if first_slide_num == 0 and slide_count == 10:
            print(f"PASS: Component 2 — firstSlideNum=0 AND slide count is 10 (0.3 pts)")
            total_score += 0.3
        elif first_slide_num != 0:
            print(f"FAIL: Component 2 — firstSlideNum is not 0 (found {first_slide_num}), skipping integrity bonus")
        else:
            print(f"FAIL: Component 2 — firstSlideNum=0 but slide count is {slide_count} (expected 10)")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not check slide count: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against golden file (path on VM)
file_path = f'{WORKDIR}/{TASK_ID}_initial.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

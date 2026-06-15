"""
Reward Script: Lock the background rectangle on slide 1 so it cannot be accidentally moved or resized.
Task ID: impress_objects_049
Domain: libreoffice_impress
Scoring:
  Component 1: BackgroundRect shape has spLocks element in cNvSpPr XML (0.3 pts)
  Component 2: spLocks has noMove="1" attribute (0.3 pts)
  Component 3: spLocks has noResize="1" attribute (0.2 pts)
  Component 4: spLocks has noSelect="1" attribute (0.2 pts)
  Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'impress_objects_049'

# Namespaces used in PPTX XML
NS_P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
NS_A = 'http://schemas.openxmlformats.org/drawingml/2006/main'


def get_background_rect_cnvsppr(pptx_path, slide_idx=0, shape_name='BackgroundRect'):
    """
    Retrieve the cNvSpPr element of the named shape from the slide XML.
    Returns the element or None if not found.
    """
    ns = {'p': NS_P, 'a': NS_A}
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        slide_file = f'ppt/slides/slide{slide_idx + 1}.xml'
        if slide_file not in zf.namelist():
            return None
        with zf.open(slide_file) as f:
            root = ET.parse(f).getroot()
            for sp in root.findall('.//p:sp', ns):
                cNvPr = sp.find('p:nvSpPr/p:cNvPr', ns)
                if cNvPr is not None and cNvPr.get('name') == shape_name:
                    cNvSpPr = sp.find('p:nvSpPr/p:cNvSpPr', ns)
                    return cNvSpPr
    return None


def verify_task(file_path):
    """
    Verify that the BackgroundRect on slide 1 has been locked with spLocks attributes.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist and be a valid PPTX
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            # Check at least one slide exists
            if 'ppt/slides/slide1.xml' not in zf.namelist():
                print("CRITICAL: No slides found in PPTX")
                print("REWARD: 0.0")
                return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot open PPTX file: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Retrieve the cNvSpPr element for BackgroundRect
    try:
        cNvSpPr = get_background_rect_cnvsppr(file_path, slide_idx=0, shape_name='BackgroundRect')
        if cNvSpPr is None:
            print("FAIL: BackgroundRect shape not found on slide 1")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"CRITICAL: Error reading BackgroundRect from XML: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: BackgroundRect has spLocks element in cNvSpPr (0.3 points)
    # In the initial file cNvSpPr is empty; after locking it should contain a:spLocks
    try:
        sp_locks = cNvSpPr.find(f'{{{NS_A}}}spLocks')
        if sp_locks is not None:
            print("PASS: Component 1 — BackgroundRect.cNvSpPr contains spLocks element (0.3 pts)")
            total_score += 0.3
        else:
            print("FAIL: Component 1 — BackgroundRect.cNvSpPr does not contain spLocks element")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: spLocks has noMove="1" (0.3 points)
    # Prevents the shape from being moved
    try:
        sp_locks = cNvSpPr.find(f'{{{NS_A}}}spLocks')
        if sp_locks is not None:
            no_move = sp_locks.get('noMove')
            if no_move == '1':
                print("PASS: Component 2 — spLocks.noMove='1' (shape cannot be moved) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — spLocks.noMove expected '1', found {repr(no_move)}")
        else:
            print("FAIL: Component 2 — spLocks element missing, cannot check noMove")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: spLocks has noResize="1" (0.2 points)
    # Prevents the shape from being resized
    try:
        sp_locks = cNvSpPr.find(f'{{{NS_A}}}spLocks')
        if sp_locks is not None:
            no_resize = sp_locks.get('noResize')
            if no_resize == '1':
                print("PASS: Component 3 — spLocks.noResize='1' (shape cannot be resized) (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — spLocks.noResize expected '1', found {repr(no_resize)}")
        else:
            print("FAIL: Component 3 — spLocks element missing, cannot check noResize")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: spLocks has noSelect="1" (0.2 points)
    # Prevents the shape from being selected (fully locked)
    try:
        sp_locks = cNvSpPr.find(f'{{{NS_A}}}spLocks')
        if sp_locks is not None:
            no_select = sp_locks.get('noSelect')
            if no_select == '1':
                print("PASS: Component 4 — spLocks.noSelect='1' (shape cannot be selected) (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 — spLocks.noSelect expected '1', found {repr(no_select)}")
        else:
            print("FAIL: Component 4 — spLocks element missing, cannot check noSelect")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

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

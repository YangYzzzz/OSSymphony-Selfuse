"""
Reward Script: Hide footer text and date placeholders on master slide, keep slide number visible
Task ID: impress_ma_047
Domain: libreoffice_impress
Scoring:
  Component 1 (0.30): Date placeholder removed from slide master
  Component 2 (0.30): Footer placeholder removed from slide master
  Component 3 (0.20): Slide number placeholder still present on slide master
  Component 4 (0.20): Date and footer placeholders removed from all slide layouts
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_ma_047'

NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}


def persist_app_state(domain):
    """Save any unsaved LibreOffice changes before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print(f"PERSIST: ctrl+s sent for {domain}")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def get_master_placeholder_types(pptx_path):
    """Extract placeholder types from slide master via XML."""
    types = []
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        with zf.open('ppt/slideMasters/slideMaster1.xml') as f:
            root = ET.fromstring(f.read())
            for sp in root.findall('.//p:sp', NS):
                ph = sp.find('.//p:ph', NS)
                if ph is not None:
                    ph_type = ph.get('type', 'body')
                    types.append(ph_type)
    return types


def get_layout_footer_types(pptx_path):
    """For each slide layout, return set of footer-area placeholder types (dt, ftr, sldNum)."""
    results = {}
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        layout_files = sorted([n for n in zf.namelist() if n.startswith('ppt/slideLayouts/')])
        for lf in layout_files:
            with zf.open(lf) as f:
                root = ET.fromstring(f.read())
                footer_types = set()
                for sp in root.findall('.//p:sp', NS):
                    ph = sp.find('.//p:ph', NS)
                    if ph is not None:
                        pt = ph.get('type', 'body')
                        if pt in ('dt', 'ftr', 'sldNum'):
                            footer_types.add(pt)
                results[lf] = footer_types
    return results


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid pptx
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            if 'ppt/slideMasters/slideMaster1.xml' not in zf.namelist():
                print("CRITICAL: No slide master found in pptx")
                print("REWARD: 0.0")
                return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot open pptx file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get master placeholder types
    try:
        master_types = get_master_placeholder_types(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse slide master: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Date placeholder removed from slide master (0.30 points)
    # In the initial state, the master has a 'dt' placeholder.
    # In the golden state, the 'dt' placeholder should be absent.
    try:
        if 'dt' not in master_types:
            print(f"PASS: Component 1 -- Date placeholder NOT found on slide master (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 -- Date placeholder still present on slide master. Found types: {master_types}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Footer placeholder removed from slide master (0.30 points)
    # In the initial state, the master has a 'ftr' placeholder.
    # In the golden state, the 'ftr' placeholder should be absent.
    try:
        if 'ftr' not in master_types:
            print(f"PASS: Component 2 -- Footer placeholder NOT found on slide master (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 -- Footer placeholder still present on slide master. Found types: {master_types}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Slide number placeholder still present on slide master (0.20 points)
    # The task says to keep the slide number visible. It must still exist.
    # This component only passes if sldNum is present AND dt/ftr are absent (anchored to the change).
    try:
        if 'sldNum' in master_types and 'dt' not in master_types and 'ftr' not in master_types:
            print(f"PASS: Component 3 -- Slide number placeholder present on master with dt/ftr removed (0.20 pts)")
            total_score += 0.20
        elif 'sldNum' not in master_types:
            print(f"FAIL: Component 3 -- Slide number placeholder is MISSING from slide master")
        else:
            print(f"FAIL: Component 3 -- Slide number present but dt/ftr not yet removed. Types: {master_types}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Date and footer placeholders removed from ALL slide layouts (0.20 points)
    # In the initial state, every layout has dt and ftr placeholders.
    # In the golden state, no layout should have dt or ftr.
    try:
        layout_types = get_layout_footer_types(file_path)
        layouts_with_dt_or_ftr = []
        for layout_name, types_set in layout_types.items():
            if 'dt' in types_set or 'ftr' in types_set:
                layouts_with_dt_or_ftr.append(layout_name)

        if len(layouts_with_dt_or_ftr) == 0:
            print(f"PASS: Component 4 -- No layouts contain dt or ftr placeholders (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 -- {len(layouts_with_dt_or_ftr)} layout(s) still have dt/ftr: {layouts_with_dt_or_ftr}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
persist_app_state("libreoffice_impress")

if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

"""
Reward Script: Configure custom slide shows in LibreOffice Impress
Task ID: impress_gf3_021
Domain: libreoffice_impress
Scoring:
  Component 1: 'Executive Summary' custom show with slides 1,3,7,12 (0.40)
  Component 2: 'Technical Deep Dive' custom show with slides 1,4,5,6,8,9,10,11 (0.40)
  Component 3: Exactly 2 custom shows defined (0.20)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_gf3_021'

# Namespaces used in OOXML presentation files
NS_P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
NS_R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'


def persist_app_state(domain: str):
    """Save any unsaved LibreOffice edits before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def build_rid_to_slide_number(pres_root):
    """Build a mapping from relationship IDs (rId) to 1-based slide numbers."""
    sldIdLst = pres_root.find(f'.//{{{NS_P}}}sldIdLst')
    if sldIdLst is None:
        return {}
    rid_map = {}
    for i, sldId in enumerate(sldIdLst):
        rid = sldId.get(f'{{{NS_R}}}id')
        if rid:
            rid_map[rid] = i + 1  # 1-based slide number
    return rid_map


def parse_custom_shows(pptx_path):
    """
    Parse custom slide shows from presentation.xml.
    Returns: dict of {show_name: [slide_numbers_in_order]}
    Also returns total slide count.
    """
    custom_shows = {}
    total_slides = 0

    with zipfile.ZipFile(pptx_path, 'r') as zf:
        # Count slides
        slide_files = [f for f in zf.namelist()
                       if f.startswith('ppt/slides/slide') and f.endswith('.xml')]
        total_slides = len(slide_files)

        # Parse presentation.xml
        with zf.open('ppt/presentation.xml') as f:
            tree = ET.parse(f)
            root = tree.getroot()

        # Build rId -> slide number mapping
        rid_map = build_rid_to_slide_number(root)

        # Find custShowLst
        custShowLst = root.find(f'.//{{{NS_P}}}custShowLst')
        if custShowLst is None:
            return custom_shows, total_slides

        for custShow in custShowLst.findall(f'{{{NS_P}}}custShow'):
            name = custShow.get('name', '')
            sldLst = custShow.find(f'{{{NS_P}}}sldLst')
            slide_numbers = []
            if sldLst is not None:
                for sld in sldLst.findall(f'{{{NS_P}}}sld'):
                    rid = sld.get(f'{{{NS_R}}}id')
                    if rid and rid in rid_map:
                        slide_numbers.append(rid_map[rid])
            custom_shows[name] = slide_numbers

    return custom_shows, total_slides


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid pptx
    try:
        custom_shows, total_slides = parse_custom_shows(file_path)
        print(f"INFO: Found {total_slides} slides and {len(custom_shows)} custom show(s)")
        for name, slides in custom_shows.items():
            print(f"INFO: Custom show '{name}': slides {slides}")
    except Exception as e:
        print(f"CRITICAL: Cannot parse file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: presentation must still have 15 slides
    if total_slides != 15:
        print(f"FAIL: Presentation should have 15 slides, found {total_slides}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: 'Executive Summary' custom show with slides 1,3,7,12 in order (0.40 points)
    expected_exec_slides = [1, 3, 7, 12]
    try:
        if 'Executive Summary' in custom_shows:
            actual_slides = custom_shows['Executive Summary']
            if actual_slides == expected_exec_slides:
                print(f"PASS: Component 1 — 'Executive Summary' has correct slides {actual_slides} (0.40 pts)")
                total_score += 0.40
            else:
                print(f"FAIL: Component 1 — 'Executive Summary' has slides {actual_slides}, expected {expected_exec_slides}")
        else:
            print(f"FAIL: Component 1 — 'Executive Summary' custom show not found. Available: {list(custom_shows.keys())}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 'Technical Deep Dive' custom show with slides 1,4,5,6,8,9,10,11 in order (0.40 points)
    expected_tech_slides = [1, 4, 5, 6, 8, 9, 10, 11]
    try:
        if 'Technical Deep Dive' in custom_shows:
            actual_slides = custom_shows['Technical Deep Dive']
            if actual_slides == expected_tech_slides:
                print(f"PASS: Component 2 — 'Technical Deep Dive' has correct slides {actual_slides} (0.40 pts)")
                total_score += 0.40
            else:
                print(f"FAIL: Component 2 — 'Technical Deep Dive' has slides {actual_slides}, expected {expected_tech_slides}")
        else:
            print(f"FAIL: Component 2 — 'Technical Deep Dive' custom show not found. Available: {list(custom_shows.keys())}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Exactly 2 custom shows defined (0.20 points)
    try:
        num_shows = len(custom_shows)
        if num_shows == 2:
            print(f"PASS: Component 3 — Exactly 2 custom shows defined (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Expected 2 custom shows, found {num_shows}: {list(custom_shows.keys())}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook: save unsaved GUI edits before verification
persist_app_state("libreoffice_impress")

# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

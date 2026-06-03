"""
Reward Script: Create three sections in presentation
Task ID: impress_ndo_071
Domain: libreoffice_impress
Scoring:
  - Component 1 (0.20): Exactly 3 sections exist
  - Component 2 (0.30): Section names match in order: Introduction, Main Content, Conclusion
  - Component 3 (0.20): Introduction section contains slides 1-3
  - Component 4 (0.15): Main Content section contains slides 4-10
  - Component 5 (0.15): Conclusion section contains slides 11-15
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_ndo_071'


def persist_app_state(domain: str):
    """Attempt to save any unsaved LibreOffice edits via Ctrl+S."""
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


def extract_sections(pptx_path):
    """
    Parse ppt/presentation.xml to extract p14:section elements.
    Returns list of (name, [slide_id_ints]) tuples, or None if no sections found.
    """
    ns_p = 'http://schemas.openxmlformats.org/presentationml/2006/main'
    ns_p14 = 'http://schemas.microsoft.com/office/powerpoint/2010/main'

    with zipfile.ZipFile(pptx_path, 'r') as zf:
        with zf.open('ppt/presentation.xml') as f:
            root = ET.parse(f).getroot()

    # Also extract the ordered slide IDs from p:sldIdLst to build index mapping
    sld_id_lst = root.find(f'{{{ns_p}}}sldIdLst')
    if sld_id_lst is None:
        return None, {}

    # Build map: slide_id -> 1-based slide index
    slide_id_to_index = {}
    for idx, sld_id_elem in enumerate(sld_id_lst.findall(f'{{{ns_p}}}sldId'), start=1):
        sid = sld_id_elem.get('id')
        if sid:
            slide_id_to_index[int(sid)] = idx

    # Find sections in extLst
    sections = []
    for ext in root.iter(f'{{{ns_p}}}ext'):
        section_lst = ext.find(f'{{{ns_p14}}}sectionLst')
        if section_lst is not None:
            for section in section_lst.findall(f'{{{ns_p14}}}section'):
                name = section.get('name', '')
                slide_ids = []
                sld_id_lst_elem = section.find(f'{{{ns_p14}}}sldIdLst')
                if sld_id_lst_elem is not None:
                    for sld_id in sld_id_lst_elem.findall(f'{{{ns_p14}}}sldId'):
                        sid = sld_id.get('id')
                        if sid:
                            slide_ids.append(int(sid))
                sections.append((name, slide_ids))

    return sections, slide_id_to_index


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid zip/pptx
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        sections, slide_id_map = extract_sections(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if sections is None:
        print("FAIL: No section structure found in presentation.xml")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found {len(sections)} section(s)")
    for i, (name, sids) in enumerate(sections):
        slide_indices = sorted([slide_id_map.get(sid, -1) for sid in sids])
        print(f"  Section {i+1}: '{name}' -> slide indices {slide_indices}")

    # Component 1: Exactly 3 sections exist (0.20 points)
    try:
        if len(sections) == 3:
            print(f"PASS: Component 1 -- exactly 3 sections found (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 -- expected 3 sections, found {len(sections)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Section names in correct order (0.30 points)
    expected_names = ["Introduction", "Main Content", "Conclusion"]
    try:
        actual_names = [s[0] for s in sections]
        if actual_names == expected_names:
            print(f"PASS: Component 2 -- section names match in order: {actual_names} (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 -- expected names {expected_names}, found {actual_names}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Introduction contains slides 1-3 (0.20 points)
    try:
        if len(sections) >= 1:
            name, sids = sections[0]
            slide_indices = sorted([slide_id_map.get(sid, -1) for sid in sids])
            if slide_indices == [1, 2, 3]:
                print(f"PASS: Component 3 -- Introduction contains slides 1-3 (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 -- Introduction slides expected [1,2,3], found {slide_indices}")
        else:
            print("FAIL: Component 3 -- no sections to check")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Main Content contains slides 4-10 (0.15 points)
    try:
        if len(sections) >= 2:
            name, sids = sections[1]
            slide_indices = sorted([slide_id_map.get(sid, -1) for sid in sids])
            if slide_indices == [4, 5, 6, 7, 8, 9, 10]:
                print(f"PASS: Component 4 -- Main Content contains slides 4-10 (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 -- Main Content slides expected [4-10], found {slide_indices}")
        else:
            print("FAIL: Component 4 -- fewer than 2 sections")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Conclusion contains slides 11-15 (0.15 points)
    try:
        if len(sections) >= 3:
            name, sids = sections[2]
            slide_indices = sorted([slide_id_map.get(sid, -1) for sid in sids])
            if slide_indices == [11, 12, 13, 14, 15]:
                print(f"PASS: Component 5 -- Conclusion contains slides 11-15 (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 -- Conclusion slides expected [11-15], found {slide_indices}")
        else:
            print("FAIL: Component 5 -- fewer than 3 sections")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_impress")

file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

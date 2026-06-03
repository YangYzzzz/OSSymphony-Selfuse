"""
Reward Script: Create a new master slide named 'Section Header'
Task ID: impress_ma_005
Domain: libreoffice_impress
Scoring:
  - Component 1 (0.4): Two slide masters exist (was 1)
  - Component 2 (0.35): Second master is named 'Section Header'
  - Component 3 (0.25): Second master has at least one slide layout associated
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_ma_005'

NS_P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
NS_R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
NS_REL = 'http://schemas.openxmlformats.org/package/2006/relationships'


def persist_app_state(domain):
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


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # We use ZIP/XML parsing to inspect slide masters, since python-pptx
    # can have issues iterating over multiple masters with broken rId references.
    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open ZIP: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        # Parse presentation.xml to find master references
        with zf.open('ppt/presentation.xml') as f:
            pres_root = ET.fromstring(f.read())

        master_ids = pres_root.findall('.//{%s}sldMasterId' % NS_P)
        num_masters = len(master_ids)
        print(f"INFO: Found {num_masters} slide master reference(s) in presentation.xml")

        # Parse presentation.xml.rels to map rIds to file targets
        with zf.open('ppt/_rels/presentation.xml.rels') as f:
            rels_root = ET.fromstring(f.read())

        rid_to_target = {}
        for rel in rels_root:
            rid_to_target[rel.get('Id')] = rel.get('Target')

        # Build list of master file paths and their rIds
        master_targets = []
        for mid in master_ids:
            rid = mid.get('{%s}id' % NS_R)
            target = rid_to_target.get(rid, None)
            master_targets.append((rid, target))
            print(f"INFO: Master rId={rid} -> {target}")

    except Exception as e:
        print(f"CRITICAL: Cannot parse presentation structure: {e}")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Exactly 2 slide masters exist (0.4 points)
    # Initial has 1 master; golden should have 2.
    try:
        if num_masters >= 2:
            print(f"PASS: Component 1 -- {num_masters} slide masters found (>= 2) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 -- Expected >= 2 slide masters, found {num_masters}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: One of the masters is named 'Section Header' (0.35 points)
    # Read the cSld name attribute from each slideMaster XML
    try:
        master_names = []
        for rid, target in master_targets:
            if target is None:
                continue
            master_xml_path = 'ppt/' + target if not target.startswith('ppt/') else target
            try:
                with zf.open(master_xml_path) as f:
                    mroot = ET.fromstring(f.read())
                cSld = mroot.find('.//{%s}cSld' % NS_P)
                name = cSld.get('name', '') if cSld is not None else ''
                master_names.append(name)
                print(f"INFO: Master '{master_xml_path}' cSld name = '{name}'")
            except KeyError:
                print(f"WARN: Could not open {master_xml_path}")

        has_section_header = any(
            'section header' in n.lower() for n in master_names
        )
        if has_section_header:
            print(f"PASS: Component 2 -- Found master named 'Section Header' (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 -- No master named 'Section Header'. Names found: {master_names}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: The 'Section Header' master has at least one slide layout (0.25 points)
    # Check the .rels file for the Section Header master to find slideLayout references
    try:
        section_header_layout_count = 0
        for rid, target in master_targets:
            if target is None:
                continue
            master_xml_path = 'ppt/' + target if not target.startswith('ppt/') else target
            # Check if this is the Section Header master
            try:
                with zf.open(master_xml_path) as f:
                    mroot = ET.fromstring(f.read())
                cSld = mroot.find('.//{%s}cSld' % NS_P)
                name = cSld.get('name', '') if cSld is not None else ''
            except KeyError:
                continue

            if 'section header' not in name.lower():
                continue

            # Found the Section Header master; now check its rels for layouts
            rels_path = master_xml_path.replace('slideMasters/', 'slideMasters/_rels/') + '.rels'
            try:
                with zf.open(rels_path) as f:
                    rels_root2 = ET.fromstring(f.read())
                for rel in rels_root2:
                    rel_type = rel.get('Type', '')
                    if 'slideLayout' in rel_type:
                        section_header_layout_count += 1
                if section_header_layout_count > 0:
                    print(f"INFO: Section Header master has {section_header_layout_count} layout(s)")
            except KeyError:
                print(f"WARN: No rels file at {rels_path}")

        if section_header_layout_count > 0:
            print(f"PASS: Component 3 -- Section Header master has associated layout(s) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 -- Section Header master has no associated layouts")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    zf.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist unsaved GUI state before scoring
persist_app_state("libreoffice_impress")

# Run verification
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

"""
Reward Script: Apply 'Grow & Shrink' emphasis animation to E=mc2 text box on slide 5
Task ID: impress_teach_047
Domain: libreoffice_impress
Scoring:
  Component 1 (0.35): Slide 5 has animation timing elements
  Component 2 (0.25): Animation targets the 'E = mc²' text box
  Component 3 (0.20): Animation is 'Grow & Shrink' emphasis type (presetID=6, presetClass=emph)
  Component 4 (0.20): Duration is 1 second (1000ms) and trigger is on click
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_teach_047'

NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
}


def find_emc2_shape_id(zip_path):
    """Find the shape ID of the text box containing 'E = mc' on slide 5."""
    with zipfile.ZipFile(zip_path, 'r') as zf:
        with zf.open('ppt/slides/slide5.xml') as f:
            tree = ET.parse(f)
            root = tree.getroot()

    # Namespace for shape tree
    p_ns = NS['p']
    a_ns = NS['a']

    # Walk the shape tree to find shape containing E = mc
    spTree = root.find(f'.//{{{p_ns}}}cSld/{{{p_ns}}}spTree')
    if spTree is None:
        spTree = root.find(f'.//{{{p_ns}}}spTree')
    if spTree is None:
        return None

    for sp in spTree:
        # Look for text containing 'E = mc' in this shape element
        texts = []
        for t_elem in sp.iter(f'{{{a_ns}}}t'):
            if t_elem.text:
                texts.append(t_elem.text)
        full_text = ''.join(texts).strip()

        if 'E = mc' in full_text or 'E=mc' in full_text:
            # Get the shape ID from cNvPr
            for cnvpr in sp.iter(f'{{{p_ns}}}cNvPr'):
                return cnvpr.get('id')
            # Also try without namespace prefix (sp namespace)
            for child in sp:
                if child.tag.endswith('}nvSpPr') or child.tag.endswith('}nvGrpSpPr'):
                    for sub in child:
                        if sub.tag.endswith('}cNvPr'):
                            return sub.get('id')
    return None


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

    # Find the shape ID of the E=mc2 text box
    try:
        emc2_spid = find_emc2_shape_id(file_path)
        print(f"INFO: E=mc2 text box shape ID: {emc2_spid}")
    except Exception as e:
        print(f"ERROR: Could not find E=mc2 shape ID: {e}")
        emc2_spid = None

    # Parse slide 5 XML for animation timing
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            with zf.open('ppt/slides/slide5.xml') as f:
                tree = ET.parse(f)
                root = tree.getroot()
    except Exception as e:
        print(f"CRITICAL: Cannot parse slide5.xml: {e}")
        print("REWARD: 0.0")
        return 0.0

    p_ns = NS['p']
    timing = root.find(f'.//{{{p_ns}}}timing')

    # Component 1: Slide 5 has animation timing elements (0.35 points)
    try:
        if timing is not None:
            # Check for actual animation nodes (not just empty timing)
            ctn_nodes = list(timing.iter(f'{{{p_ns}}}cTn'))
            if len(ctn_nodes) >= 2:
                print(f"PASS: Component 1 — Slide 5 has animation timing with {len(ctn_nodes)} cTn nodes (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 1 — Timing element exists but has insufficient cTn nodes: {len(ctn_nodes)}")
        else:
            print("FAIL: Component 1 — No p:timing element found on slide 5")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Animation targets the E=mc2 text box (0.25 points)
    try:
        if timing is not None and emc2_spid is not None:
            # Look for spTgt with matching spid
            target_found = False
            for spTgt in timing.iter(f'{{{p_ns}}}spTgt'):
                if spTgt.get('spid') == emc2_spid:
                    target_found = True
                    break
            if target_found:
                print(f"PASS: Component 2 — Animation targets E=mc2 text box (spid={emc2_spid}) (0.25 pts)")
                total_score += 0.25
            else:
                # List all targeted shape IDs
                all_targets = [s.get('spid') for s in timing.iter(f'{{{p_ns}}}spTgt')]
                print(f"FAIL: Component 2 — Animation does not target E=mc2 (spid={emc2_spid}). Targets found: {all_targets}")
        else:
            if timing is None:
                print("FAIL: Component 2 — No timing element to check")
            else:
                print(f"FAIL: Component 2 — Could not identify E=mc2 shape (spid={emc2_spid})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Animation is 'Grow & Shrink' emphasis (presetID=6, presetClass=emph) (0.20 points)
    try:
        if timing is not None:
            emph_grow_found = False
            for ctn in timing.iter(f'{{{p_ns}}}cTn'):
                preset_id = ctn.get('presetID')
                preset_class = ctn.get('presetClass')
                if preset_id == '6' and preset_class == 'emph':
                    emph_grow_found = True
                    break
            if emph_grow_found:
                print("PASS: Component 3 — Animation is Grow & Shrink emphasis (presetID=6, presetClass=emph) (0.20 pts)")
                total_score += 0.20
            else:
                # List what presets we found
                presets = [(c.get('presetID'), c.get('presetClass'))
                           for c in timing.iter(f'{{{p_ns}}}cTn')
                           if c.get('presetID') is not None]
                print(f"FAIL: Component 3 — No Grow & Shrink emphasis found. Presets: {presets}")
        else:
            print("FAIL: Component 3 — No timing element to check")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Duration 1s (1000ms) and on-click trigger (0.20 points)
    try:
        if timing is not None:
            # Check duration: look for dur="1000" in the animation behavior node
            # The animScale's cBhvr/cTn should have dur="1000"
            duration_ok = False
            for anim_scale in timing.iter(f'{{{p_ns}}}animScale'):
                for ctn in anim_scale.iter(f'{{{p_ns}}}cTn'):
                    dur = ctn.get('dur')
                    if dur == '1000':
                        duration_ok = True
                        break
                if duration_ok:
                    break

            # If not found via animScale, check the preset cTn's child animation nodes
            if not duration_ok:
                for ctn in timing.iter(f'{{{p_ns}}}cTn'):
                    if ctn.get('presetID') == '6' and ctn.get('presetClass') == 'emph':
                        for child_ctn in ctn.iter(f'{{{p_ns}}}cTn'):
                            dur = child_ctn.get('dur')
                            if dur == '1000':
                                duration_ok = True
                                break

            # Check on-click trigger: the sequence parent cTn should have stCondLst with delay="indefinite"
            onclick_ok = False
            # In OOXML, on-click is indicated by delay="indefinite" on the click sequence parent
            main_seq = timing.find(f'.//{{{p_ns}}}seq')
            if main_seq is not None:
                # The first par child of mainSeq should have stCondLst with delay="indefinite"
                for par in main_seq.iter(f'{{{p_ns}}}par'):
                    ctn = par.find(f'{{{p_ns}}}cTn')
                    if ctn is not None:
                        st_cond = ctn.find(f'{{{p_ns}}}stCondLst')
                        if st_cond is not None:
                            for cond in st_cond.findall(f'{{{p_ns}}}cond'):
                                if cond.get('delay') == 'indefinite':
                                    onclick_ok = True
                                    break
                    if onclick_ok:
                        break

            sub_score = 0.0
            if duration_ok and onclick_ok:
                sub_score = 0.20
                print(f"PASS: Component 4 — Duration=1000ms and on-click trigger (0.20 pts)")
            elif duration_ok:
                sub_score = 0.10
                print(f"PARTIAL: Component 4 — Duration=1000ms correct, but on-click trigger not confirmed (0.10 pts)")
            elif onclick_ok:
                sub_score = 0.10
                print(f"PARTIAL: Component 4 — On-click trigger correct, but duration not 1000ms (0.10 pts)")
            else:
                print(f"FAIL: Component 4 — Duration not 1000ms and on-click not found")
            total_score += sub_score
        else:
            print("FAIL: Component 4 — No timing element to check")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

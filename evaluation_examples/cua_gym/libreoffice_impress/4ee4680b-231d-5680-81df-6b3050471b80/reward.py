"""
Reward Script: Animate bullet list on slide 4 with Fly In From Left, By Word, After Previous
Task ID: impress_anim_079
Domain: libreoffice_impress
Scoring:
  Component 1 (0.35): Timing/animation element exists on slide 4, targeting shape 3 (bullet text box)
  Component 2 (0.35): Fly In From Left entrance — presetID=2, presetClass=entr, presetSubtype=4, filter=fly(dir=left)
  Component 3 (0.15): Animate by word — bldLst contains bldP with build='byWord' for shape 3
  Component 4 (0.15): After Previous trigger — nodeType='afterEffect' on animation cTn elements
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_anim_079'

NS_P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
NS_A = 'http://schemas.openxmlformats.org/drawingml/2006/main'


def verify_task(file_path):
    """
    Verify that slide 4's bullet text box has been animated with:
    - Fly In entrance from the Left
    - Each bullet item animated By Word
    - Each item triggered After Previous
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Read slide4 XML from the pptx archive
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            slide4_name = 'ppt/slides/slide4.xml'
            if slide4_name not in zf.namelist():
                print(f"CRITICAL: {slide4_name} not found in archive")
                print("REWARD: 0.0")
                return 0.0
            with zf.open(slide4_name) as f:
                slide4_xml = f.read().decode('utf-8')
    except Exception as e:
        print(f"CRITICAL: Cannot open pptx archive {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        root = ET.fromstring(slide4_xml)
    except Exception as e:
        print(f"CRITICAL: Cannot parse slide4 XML: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse timing element
    timing = root.find(f'{{{NS_P}}}timing')

    # Component 1: Timing element exists and contains animation targeting shape 3 (bullet text box)
    # (0.35 points) — FAILS on initial (no timing), PASSES on golden
    try:
        if timing is None:
            print("FAIL: Component 1 — No timing/animation element found on slide 4 (no animations at all)")
        else:
            # Check that there are animEffect or par elements targeting spid="3"
            all_spTgt = timing.findall(f'.//{{{NS_P}}}spTgt')
            shape3_targets = [sp for sp in all_spTgt if sp.get('spid') == '3']
            if len(shape3_targets) > 0:
                print(f"PASS: Component 1 — Timing element found with {len(shape3_targets)} animation target(s) on shape 3 (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 1 — Timing element found but no animations target shape 3 (bullet text box). Found spTgts: {[sp.get('spid') for sp in all_spTgt]}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Fly In From Left entrance animation
    # Verified by: presetID="2", presetClass="entr", presetSubtype="4" on cTn elements
    # AND animEffect filter="fly(dir=left)"
    # (0.35 points) — FAILS on initial, PASSES on golden
    try:
        if timing is None:
            print("FAIL: Component 2 — No timing element (cannot check animation type)")
        else:
            # Find all cTn elements with presetClass="entr" (entrance animations)
            all_cTn = timing.findall(f'.//{{{NS_P}}}cTn')
            fly_left_anims = []
            for cTn in all_cTn:
                preset_class = cTn.get('presetClass')
                preset_id = cTn.get('presetID')
                preset_subtype = cTn.get('presetSubtype')
                # presetID=2 = Fly In, presetClass=entr = Entrance, presetSubtype=4 = From Left
                if preset_class == 'entr' and preset_id == '2' and preset_subtype == '4':
                    fly_left_anims.append(cTn)

            # Also verify animEffect filter="fly(dir=left)"
            all_animEffect = timing.findall(f'.//{{{NS_P}}}animEffect')
            fly_dir_left_effects = [ae for ae in all_animEffect if ae.get('filter') == 'fly(dir=left)']

            if len(fly_left_anims) >= 3 and len(fly_dir_left_effects) >= 3:
                print(f"PASS: Component 2 — Found {len(fly_left_anims)} Fly In From Left entrance animations "
                      f"(presetID=2, presetClass=entr, presetSubtype=4) and "
                      f"{len(fly_dir_left_effects)} fly(dir=left) effects (0.35 pts)")
                total_score += 0.35
            elif len(fly_left_anims) >= 1 or len(fly_dir_left_effects) >= 1:
                print(f"PARTIAL: Component 2 — Found some Fly In From Left animations but fewer than 3: "
                      f"cTn matches={len(fly_left_anims)}, animEffect matches={len(fly_dir_left_effects)} "
                      f"(expected 3 for 3 bullet items)")
                # No partial credit here — need all 3 bullets animated correctly
            else:
                # Check what presets exist
                entr_anims = [(cTn.get('presetID'), cTn.get('presetClass'), cTn.get('presetSubtype'))
                              for cTn in all_cTn if cTn.get('presetClass') is not None]
                print(f"FAIL: Component 2 — No Fly In From Left (presetID=2, presetSubtype=4) found. "
                      f"Existing entrance animations: {entr_anims[:5]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Animate by word (bldLst contains bldP with build='byWord' for shape 3)
    # (0.15 points) — FAILS on initial (no bldLst), PASSES on golden
    try:
        if timing is None:
            print("FAIL: Component 3 — No timing element (cannot check build list)")
        else:
            bld_lst = timing.find(f'{{{NS_P}}}bldLst')
            if bld_lst is None:
                print("FAIL: Component 3 — No bldLst (build list) element found in timing")
            else:
                bld_p_elements = bld_lst.findall(f'{{{NS_P}}}bldP')
                byword_shape3 = [bp for bp in bld_p_elements
                                 if bp.get('spid') == '3' and bp.get('build') == 'byWord']
                if len(byword_shape3) > 0:
                    print(f"PASS: Component 3 — bldLst contains bldP with spid=3 and build='byWord' "
                          f"(animate text by word) (0.15 pts)")
                    total_score += 0.15
                else:
                    # Report what's actually there
                    found_builds = [(bp.get('spid'), bp.get('build')) for bp in bld_p_elements]
                    print(f"FAIL: Component 3 — No bldP with spid=3 and build='byWord' found. "
                          f"Found bldP entries: {found_builds}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: After Previous trigger — nodeType='afterEffect' on animation cTn elements
    # In OOXML, 'afterEffect' nodeType on the inner cTn means the animation triggers after previous
    # (0.15 points) — FAILS on initial, PASSES on golden
    try:
        if timing is None:
            print("FAIL: Component 4 — No timing element (cannot check trigger type)")
        else:
            all_cTn = timing.findall(f'.//{{{NS_P}}}cTn')
            after_prev_nodes = [cTn for cTn in all_cTn
                                if cTn.get('nodeType') == 'afterEffect'
                                and cTn.get('presetClass') == 'entr']
            if len(after_prev_nodes) >= 3:
                print(f"PASS: Component 4 — Found {len(after_prev_nodes)} animations with "
                      f"nodeType='afterEffect' (After Previous trigger) (0.15 pts)")
                total_score += 0.15
            elif len(after_prev_nodes) >= 1:
                print(f"PARTIAL: Component 4 — Only {len(after_prev_nodes)}/3 animations have "
                      f"nodeType='afterEffect' (After Previous trigger)")
                # No partial credit for incomplete After Previous setup
            else:
                # Check if any other trigger mechanism is present
                node_types = set(cTn.get('nodeType') for cTn in all_cTn if cTn.get('nodeType'))
                print(f"FAIL: Component 4 — No animations with nodeType='afterEffect' found. "
                      f"Existing nodeTypes in timing: {node_types}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


# Default: test against golden file (path on VM)
file_path = f'{WORKDIR}/{TASK_ID}_initial.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

"""
Reward Script: Verify entrance animations on slide 2 shapes
Task ID: impress_ma_075
Domain: libreoffice_impress
Scoring:
  - Component 1 (0.1): Animation timing/sequence element exists on slide 2
  - Component 2 (0.225): Circle - Appear entrance, On Click
  - Component 3 (0.225): Square - Fade entrance, On Click
  - Component 4 (0.225): Triangle - Fly In From Left entrance, On Click
  - Component 5 (0.225): Star - Bounce entrance, On Click
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_ma_075'

NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
}

def get_shape_name_to_id(pptx_path, slide_idx=1):
    """Get mapping of shape name -> spid for a given slide (0-indexed)."""
    mapping = {}
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        with zf.open(f'ppt/slides/slide{slide_idx + 1}.xml') as f:
            root = ET.fromstring(f.read())
            for sp in root.findall('.//p:cSld/p:spTree/p:sp', NS):
                nvSpPr = sp.find('p:nvSpPr/p:cNvPr', NS)
                if nvSpPr is not None:
                    mapping[nvSpPr.get('name')] = nvSpPr.get('id')
    return mapping


def parse_animations(pptx_path, slide_idx=1):
    """
    Parse entrance animations from slide XML.
    Returns list of dicts in sequence order:
      [{spid, presetID, presetClass, presetSubtype, nodeType}, ...]
    """
    animations = []
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        with zf.open(f'ppt/slides/slide{slide_idx + 1}.xml') as f:
            root = ET.fromstring(f.read())

    timing = root.find('.//p:timing', NS)
    if timing is None:
        return animations

    # The mainSeq contains the ordered animation pars
    main_seq = timing.find('.//p:seq/p:cTn[@nodeType="mainSeq"]', NS)
    if main_seq is None:
        return animations

    child_list = main_seq.find('p:childTnLst', NS)
    if child_list is None:
        return animations

    # Each top-level <p:par> in mainSeq's childTnLst is one click-triggered group
    for par in child_list.findall('p:par', NS):
        # Inside each par, find the actual animation cTn with presetID
        for ctn in par.iter(f'{{{NS["p"]}}}cTn'):
            preset_id = ctn.get('presetID')
            preset_class = ctn.get('presetClass')
            if preset_id and preset_class:
                node_type = ctn.get('nodeType', '')
                preset_subtype = ctn.get('presetSubtype', '0')
                # Find target shape spid
                spid = None
                for spTgt in ctn.iter(f'{{{NS["p"]}}}spTgt'):
                    spid = spTgt.get('spid')
                    break
                animations.append({
                    'spid': spid,
                    'presetID': preset_id,
                    'presetClass': preset_class,
                    'presetSubtype': preset_subtype,
                    'nodeType': node_type,
                })
                break  # only first cTn with presetID per par

    return animations


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

    # Get shape name -> spid mapping
    try:
        name_to_id = get_shape_name_to_id(file_path, slide_idx=1)
        print(f"Shape mapping: {name_to_id}")
    except Exception as e:
        print(f"CRITICAL: Cannot read shapes: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse animations
    try:
        animations = parse_animations(file_path, slide_idx=1)
        print(f"Found {len(animations)} animations")
        for i, anim in enumerate(animations):
            print(f"  Anim {i}: spid={anim['spid']}, presetID={anim['presetID']}, "
                  f"presetClass={anim['presetClass']}, presetSubtype={anim['presetSubtype']}, "
                  f"nodeType={anim['nodeType']}")
    except Exception as e:
        print(f"CRITICAL: Cannot parse animations: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Animation sequence exists on slide 2 with exactly 4 entrance animations (0.1 points)
    try:
        entrance_anims = [a for a in animations if a['presetClass'] == 'entr']
        if len(entrance_anims) == 4:
            print(f"PASS: Component 1 — 4 entrance animations found on slide 2 (0.1 pts)")
            total_score += 0.1
        elif len(entrance_anims) > 0:
            print(f"FAIL: Component 1 — Expected 4 entrance animations, found {len(entrance_anims)}")
        else:
            print(f"FAIL: Component 1 — No entrance animations found on slide 2")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Build spid lookup for expected shapes
    circle_spid = name_to_id.get('Circle')
    square_spid = name_to_id.get('Square')
    triangle_spid = name_to_id.get('Triangle')
    star_spid = name_to_id.get('Star')

    # Expected animation specs: (shape_name, spid, presetID, presetClass, presetSubtype_check, order_idx)
    expected = [
        ('Circle',   circle_spid,   '1',  'entr', None, 0),   # Appear
        ('Square',   square_spid,   '10', 'entr', None, 1),   # Fade
        ('Triangle', triangle_spid, '2',  'entr', '4',  2),   # Fly In From Left (subtype 4)
        ('Star',     star_spid,     '26', 'entr', None, 3),   # Bounce
    ]

    component_names = [
        'Circle - Appear entrance On Click',
        'Square - Fade entrance On Click',
        'Triangle - Fly In From Left entrance On Click',
        'Star - Bounce entrance On Click',
    ]

    for idx, (shape_name, spid, expected_preset_id, expected_preset_class, expected_subtype, order_idx) in enumerate(expected):
        comp_num = idx + 2
        pts = 0.225
        try:
            if spid is None:
                print(f"FAIL: Component {comp_num} — Shape '{shape_name}' not found on slide 2")
                continue

            # Check if this shape has the right animation at the right position
            if order_idx >= len(entrance_anims):
                print(f"FAIL: Component {comp_num} — Not enough animations; expected {shape_name} at position {order_idx}")
                continue

            anim = entrance_anims[order_idx]

            details = []

            # Check target shape
            if anim['spid'] != spid:
                details.append(f"wrong target shape (expected spid={spid}, got spid={anim['spid']})")

            # Check preset ID (animation type)
            if anim['presetID'] != expected_preset_id:
                details.append(f"wrong animation type (expected presetID={expected_preset_id}, got {anim['presetID']})")

            # Check preset class (must be entrance)
            if anim['presetClass'] != expected_preset_class:
                details.append(f"wrong preset class (expected {expected_preset_class}, got {anim['presetClass']})")

            # Check subtype if specified (e.g., Fly In direction)
            if expected_subtype is not None and anim['presetSubtype'] != expected_subtype:
                details.append(f"wrong subtype/direction (expected {expected_subtype}, got {anim['presetSubtype']})")

            # Check On Click trigger (nodeType should be clickEffect)
            if anim['nodeType'] != 'clickEffect':
                details.append(f"wrong trigger (expected clickEffect, got {anim['nodeType']})")

            if len(details) == 0:
                print(f"PASS: Component {comp_num} — {component_names[idx]} ({pts} pts)")
                total_score += pts
            else:
                print(f"FAIL: Component {comp_num} — {component_names[idx]}: {'; '.join(details)}")

        except Exception as e:
            print(f"ERROR: Component {comp_num} — {e}")

    final_score = min(total_score, 1.0)
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

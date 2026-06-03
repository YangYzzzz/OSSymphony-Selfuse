"""
Reward Script: Apply 'Appear' animation to each bullet point on slide 3
Task ID: impress_teach_023
Domain: libreoffice_impress
Scoring:
  Component 1 (0.3): Slide 3 has animation timing elements
  Component 2 (0.3): All 5 bullet points have individual Appear entrance animations
  Component 3 (0.2): Animations target the correct content shape with per-paragraph ranges
  Component 4 (0.2): All animations are On Click (clickEffect)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_teach_023'

# Save any unsaved LibreOffice state before verification
def persist_app_state():
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        import time
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.0)
        print("PERSIST: ctrl+s sent for libreoffice_impress")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify that slide 3 has Appear animations on each of the 5 bullet points,
    triggered on click. Uses ZIP/XML parsing since python-pptx does not expose
    animation/timing data.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    pns = 'http://schemas.openxmlformats.org/presentationml/2006/main'

    # Load slide 3 XML
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            with zf.open('ppt/slides/slide3.xml') as f:
                root = ET.parse(f).getroot()
    except Exception as e:
        print(f"CRITICAL: Cannot load slide 3 XML from {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all animation nodes (cTn elements with presetID)
    anim_nodes = []
    for ctn in root.iter('{%s}cTn' % pns):
        preset_id = ctn.get('presetID')
        if preset_id is not None:
            preset_class = ctn.get('presetClass', '')
            node_type = ctn.get('nodeType', '')
            # Find target shape and paragraph range
            tgt = ctn.find('.//{%s}spTgt' % pns)
            spid = tgt.get('spid') if tgt is not None else None
            prg = None
            if tgt is not None:
                prg = tgt.find('{%s}txEl/{%s}pRg' % (pns, pns))
            para_st = prg.get('st') if prg is not None else None
            para_end = prg.get('end') if prg is not None else None
            anim_nodes.append({
                'presetID': preset_id,
                'presetClass': preset_class,
                'nodeType': node_type,
                'spid': spid,
                'para_st': para_st,
                'para_end': para_end,
            })

    print(f"Found {len(anim_nodes)} animation nodes on slide 3")
    for i, node in enumerate(anim_nodes):
        print(f"  Anim {i}: presetID={node['presetID']}, class={node['presetClass']}, "
              f"nodeType={node['nodeType']}, spid={node['spid']}, "
              f"para={node['para_st']}-{node['para_end']}")

    # Component 1: Slide 3 has animation timing elements (0.3 points)
    # This checks that ANY entrance animations exist on slide 3
    try:
        entrance_anims = [a for a in anim_nodes if a['presetClass'] == 'entr']
        if len(entrance_anims) >= 1:
            print(f"PASS: Component 1 - Slide 3 has {len(entrance_anims)} entrance animations (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 - No entrance animations found on slide 3")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: All 5 bullet points have individual Appear (presetID=1) entrance animations (0.3 points)
    # Appear animation = presetID="1", presetClass="entr"
    try:
        appear_anims = [a for a in anim_nodes
                        if a['presetID'] == '1' and a['presetClass'] == 'entr']
        if len(appear_anims) >= 5:
            print(f"PASS: Component 2 - Found {len(appear_anims)} Appear entrance animations for 5 bullets (0.3 pts)")
            total_score += 0.3
        elif len(appear_anims) >= 3:
            partial = round(0.3 * len(appear_anims) / 5, 2)
            print(f"PARTIAL: Component 2 - Found {len(appear_anims)}/5 Appear animations ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 - Found only {len(appear_anims)} Appear entrance animations, expected 5")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Animations target the content shape with per-paragraph ranges (0.2 points)
    # Each bullet should have its own paragraph range (0,0), (1,1), (2,2), (3,3), (4,4)
    try:
        appear_anims = [a for a in anim_nodes
                        if a['presetID'] == '1' and a['presetClass'] == 'entr']
        expected_paras = {'0', '1', '2', '3', '4'}
        found_paras = set()
        for a in appear_anims:
            if a['para_st'] is not None and a['para_st'] == a['para_end']:
                found_paras.add(a['para_st'])

        if found_paras >= expected_paras:
            print(f"PASS: Component 3 - All 5 paragraphs (0-4) have individual animations (0.2 pts)")
            total_score += 0.2
        elif len(found_paras) >= 3:
            partial = round(0.2 * len(found_paras & expected_paras) / 5, 2)
            print(f"PARTIAL: Component 3 - Found individual animations for paragraphs {sorted(found_paras)}, expected {sorted(expected_paras)} ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 - Individual paragraph animations found for {sorted(found_paras)}, expected {sorted(expected_paras)}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: All animations are On Click (nodeType=clickEffect) (0.2 points)
    try:
        appear_anims = [a for a in anim_nodes
                        if a['presetID'] == '1' and a['presetClass'] == 'entr']
        if len(appear_anims) == 0:
            print(f"FAIL: Component 4 - No Appear animations to check trigger type")
        else:
            click_anims = [a for a in appear_anims if a['nodeType'] == 'clickEffect']
            if len(click_anims) == len(appear_anims):
                print(f"PASS: Component 4 - All {len(click_anims)} animations trigger On Click (0.2 pts)")
                total_score += 0.2
            else:
                non_click = len(appear_anims) - len(click_anims)
                print(f"FAIL: Component 4 - {non_click}/{len(appear_anims)} animations are NOT On Click")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state()

file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

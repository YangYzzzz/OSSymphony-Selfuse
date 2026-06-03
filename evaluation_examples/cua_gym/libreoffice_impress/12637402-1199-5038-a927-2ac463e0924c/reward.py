"""
Reward Script: Apply 'Spiral In' exit animation to title of slide 9 (3s duration)
               and simultaneously trigger a 'Box' entrance animation for the image.
Task ID: impress_gf1_047
Domain: libreoffice_impress
Scoring:
  Component 1 (0.25): Timing/animation element exists on slide 9
  Component 2 (0.30): Exit animation on title with Spiral type, 3s duration
  Component 3 (0.25): Entrance animation on image with Box type
  Component 4 (0.20): Animations are synchronized (withEffect / same click group)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_gf1_047'

# PowerPoint animation XML namespaces
NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}


def find_shape_id_by_type(root, shape_type):
    """Find shape ID for a given type ('pic' for picture, 'sp' for text shapes)."""
    results = []
    for elem in root.iter():
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        if tag == shape_type:
            # Find cNvPr inside this element
            for child in elem.iter():
                ctag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                if ctag == 'cNvPr':
                    results.append({
                        'id': child.get('id'),
                        'name': child.get('name', ''),
                    })
                    break
    return results


def find_title_shape_id(root):
    """Find the shape ID for the title text box containing 'Transition Point'."""
    for elem in root.iter():
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        if tag == 'sp':
            # Check if this shape has text "Transition Point"
            texts = []
            for t_elem in elem.iter():
                t_tag = t_elem.tag.split('}')[-1] if '}' in t_elem.tag else t_elem.tag
                if t_tag == 't' and t_elem.text:
                    texts.append(t_elem.text)
            full_text = ''.join(texts).strip()
            if 'Transition Point' in full_text:
                for child in elem.iter():
                    ctag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                    if ctag == 'cNvPr':
                        return child.get('id')
    return None


def find_picture_shape_id(root):
    """Find the shape ID for the picture element."""
    for elem in root.iter():
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        if tag == 'pic':
            for child in elem.iter():
                ctag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                if ctag == 'cNvPr':
                    return child.get('id')
    return None


def get_animation_nodes(timing_elem):
    """Extract all cTn nodes that have presetClass (actual animation definitions)."""
    animations = []
    for elem in timing_elem.iter():
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        if tag == 'cTn' and elem.get('presetClass'):
            # Find target shape ID
            target_spid = None
            for child in elem.iter():
                ctag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                if ctag == 'spTgt':
                    target_spid = child.get('spid')
                    break

            # Find animEffect filter if present
            anim_filter = None
            for child in elem.iter():
                ctag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                if ctag == 'animEffect':
                    anim_filter = child.get('filter', '')
                    break

            animations.append({
                'presetID': elem.get('presetID'),
                'presetClass': elem.get('presetClass'),
                'presetSubtype': elem.get('presetSubtype'),
                'dur': elem.get('dur'),
                'nodeType': elem.get('nodeType'),
                'target_spid': target_spid,
                'filter': anim_filter,
            })
    return animations


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse slide 9 XML
    try:
        with zf.open('ppt/slides/slide9.xml') as f:
            content = f.read().decode()
        root = ET.fromstring(content)
    except Exception as e:
        print(f"CRITICAL: Cannot parse slide 9 XML: {e}")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    # Identify shapes
    title_spid = find_title_shape_id(root)
    picture_spid = find_picture_shape_id(root)
    print(f"INFO: Title shape ('Transition Point') spid={title_spid}")
    print(f"INFO: Picture shape spid={picture_spid}")

    if not title_spid or not picture_spid:
        print(f"CRITICAL: Could not identify required shapes on slide 9")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    # Find timing element
    timing_elem = None
    for elem in root.iter():
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        if tag == 'timing':
            timing_elem = elem
            break

    # Component 1: Timing/animation element exists on slide 9 (0.25 points)
    # This FAILS on initial (no animations) and PASSES on golden (animations added)
    try:
        if timing_elem is not None:
            animations = get_animation_nodes(timing_elem)
            if len(animations) >= 2:
                print(f"PASS: Component 1 — Timing element found with {len(animations)} animation(s) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 — Timing element found but only {len(animations)} animation(s), expected >= 2")
        else:
            print(f"FAIL: Component 1 — No timing element found on slide 9")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if timing_elem is None:
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        zf.close()
        return final_score

    animations = get_animation_nodes(timing_elem)

    # Component 2: Exit animation on title with Spiral type and 3s duration (0.30 points)
    # presetID=49 is "Spiral Out" (exit spiral), presetClass="exit", dur=3000
    try:
        exit_anims = [a for a in animations if a['presetClass'] == 'exit' and a['target_spid'] == title_spid]
        if exit_anims:
            exit_anim = exit_anims[0]
            is_spiral = exit_anim['presetID'] == '49'
            dur_val = exit_anim.get('dur', '')
            is_3s = dur_val == '3000'

            if is_spiral and is_3s:
                print(f"PASS: Component 2 — Spiral exit animation on title, duration=3000ms (0.30 pts)")
                total_score += 0.30
            elif is_spiral and not is_3s:
                print(f"PARTIAL: Component 2 — Spiral exit found but duration={dur_val}, expected 3000 (0.15 pts)")
                total_score += 0.15
            elif not is_spiral and is_3s:
                print(f"PARTIAL: Component 2 — Exit animation presetID={exit_anim['presetID']} (not Spiral/49) but duration correct (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 2 — Exit animation presetID={exit_anim['presetID']}, dur={dur_val} (expected 49/3000)")
        else:
            print(f"FAIL: Component 2 — No exit animation found targeting title shape (spid={title_spid})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Entrance animation on image with Box type (0.25 points)
    # presetID=42 is "Box", presetClass="entr", filter contains "box"
    try:
        entr_anims = [a for a in animations if a['presetClass'] == 'entr' and a['target_spid'] == picture_spid]
        if entr_anims:
            entr_anim = entr_anims[0]
            is_box_by_id = entr_anim['presetID'] == '42'
            is_box_by_filter = entr_anim.get('filter', '') and 'box' in entr_anim.get('filter', '').lower()
            is_box = is_box_by_id or is_box_by_filter

            if is_box:
                print(f"PASS: Component 3 — Box entrance animation on image (presetID={entr_anim['presetID']}, filter={entr_anim.get('filter')}) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — Entrance animation on image but not Box type (presetID={entr_anim['presetID']}, filter={entr_anim.get('filter')})")
        else:
            print(f"FAIL: Component 3 — No entrance animation found targeting image shape (spid={picture_spid})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Synchronization — entrance is "withEffect" (simultaneous) (0.20 points)
    # The Box entrance should have nodeType="withEffect" to play simultaneously with the exit
    try:
        entr_anims = [a for a in animations if a['presetClass'] == 'entr' and a['target_spid'] == picture_spid]
        if entr_anims:
            entr_anim = entr_anims[0]
            node_type = entr_anim.get('nodeType', '')
            if node_type == 'withEffect':
                print(f"PASS: Component 4 — Entrance animation nodeType='withEffect' (simultaneous) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 — Entrance animation nodeType='{node_type}', expected 'withEffect' for simultaneous trigger")
        else:
            print(f"FAIL: Component 4 — No entrance animation to check synchronization")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    zf.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point — persist app state then verify
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


persist_app_state("libreoffice_impress")

file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

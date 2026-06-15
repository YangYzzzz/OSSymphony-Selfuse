"""
Reward Script: Remove emphasis animations from slide 7, keep entrance animations
Task ID: impress_fix_062
Domain: libreoffice_impress
Scoring:
  Component 1 (0.4): All emphasis animations removed from slide 7
  Component 2 (0.4): All 5 entrance (Fly In) animations preserved on slide 7
  Component 3 (0.2): Entrance animations target correct paragraphs 0-4
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_fix_062'
NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}


def persist_app_state(domain):
    """Save any unsaved GUI state before verification."""
    os.environ["DISPLAY"] = ":0"
    if domain in ("libreoffice_calc", "libreoffice_writer", "libreoffice_impress"):
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            import time
            time.sleep(0.8)
            print("PERSIST: ctrl+s sent for %s" % domain)
        except Exception as e:
            print("PERSIST_WARN: save hook failed: %s" % e)


def get_animations_on_slide(pptx_path, slide_num):
    """
    Parse slide XML to extract animation preset info.
    Returns list of dicts with presetClass, presetID, paragraph index.
    slide_num is 1-based.
    """
    animations = []
    try:
        with zipfile.ZipFile(pptx_path, 'r') as zf:
            slide_xml = 'ppt/slides/slide%d.xml' % slide_num
            if slide_xml not in zf.namelist():
                print("ERROR: %s not found in archive" % slide_xml)
                return animations
            with zf.open(slide_xml) as f:
                tree = ET.parse(f)
                root = tree.getroot()

            timing = root.find('.//p:timing', NS)
            if timing is None:
                return animations

            for elem in timing.iter():
                preset_class = elem.get('presetClass')
                preset_id = elem.get('presetID')
                if preset_class:
                    # Find target paragraph range
                    para_idx = None
                    for child in elem.iter():
                        if child.tag.endswith('pRg'):
                            para_idx = child.get('st')
                            break
                    animations.append({
                        'presetClass': preset_class,
                        'presetID': preset_id,
                        'paragraph': para_idx,
                    })
    except Exception as e:
        print("ERROR: Failed to parse animations: %s" % e)
    return animations


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid zip/pptx
    if not os.path.exists(file_path):
        print("CRITICAL: File not found: %s" % file_path)
        print("REWARD: 0.0")
        return 0.0

    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            if 'ppt/slides/slide7.xml' not in zf.namelist():
                print("CRITICAL: slide7.xml not found in presentation")
                print("REWARD: 0.0")
                return 0.0
    except Exception as e:
        print("CRITICAL: Cannot open pptx file: %s" % e)
        print("REWARD: 0.0")
        return 0.0

    animations = get_animations_on_slide(file_path, 7)
    entrance_anims = [a for a in animations if a['presetClass'] == 'entr']
    emphasis_anims = [a for a in animations if a['presetClass'] == 'emph']
    exit_anims = [a for a in animations if a['presetClass'] == 'exit']

    print("Slide 7 animations found:")
    print("  Entrance: %d" % len(entrance_anims))
    print("  Emphasis: %d" % len(emphasis_anims))
    print("  Exit: %d" % len(exit_anims))

    # Component 1: All emphasis animations removed from slide 7 (0.5 points)
    # Initial has 5 emphasis animations; golden should have 0.
    # This is the core task change -- FAILS on initial, PASSES on golden.
    try:
        if len(emphasis_anims) == 0:
            print("PASS: Component 1 -- No emphasis animations on slide 7 (0.5 pts)")
            total_score += 0.5
        else:
            print("FAIL: Component 1 -- Found %d emphasis animation(s), expected 0" % len(emphasis_anims))
    except Exception as e:
        print("ERROR: Component 1 -- %s" % e)

    # Component 2: Emphasis removed AND all 5 Fly In entrance animations preserved (0.3 points)
    # Compound check: only scores if emphasis is gone AND entrance is intact.
    # FAILS on initial (emphasis present), PASSES on golden.
    try:
        fly_in_anims = [a for a in entrance_anims if a['presetID'] == '2']
        if len(emphasis_anims) == 0 and len(fly_in_anims) == 5:
            print("PASS: Component 2 -- Emphasis removed AND all 5 Fly In entrance animations preserved (0.3 pts)")
            total_score += 0.3
        elif len(emphasis_anims) == 0 and len(fly_in_anims) > 0:
            # Partial: emphasis removed but some entrance lost
            partial = 0.3 * (len(fly_in_anims) / 5.0)
            print("PARTIAL: Component 2 -- Emphasis removed, but only %d/5 Fly In animations remain (%.2f pts)" % (len(fly_in_anims), partial))
            total_score += partial
        else:
            if len(emphasis_anims) > 0:
                print("FAIL: Component 2 -- Emphasis animations still present (%d found)" % len(emphasis_anims))
            else:
                print("FAIL: Component 2 -- No Fly In entrance animations found")
    except Exception as e:
        print("ERROR: Component 2 -- %s" % e)

    # Component 3: Emphasis removed AND entrance animations target correct paragraphs 0-4 (0.2 points)
    # Compound check anchored to the task change.
    # FAILS on initial (emphasis present), PASSES on golden.
    try:
        entrance_paras = sorted([a['paragraph'] for a in entrance_anims if a['paragraph'] is not None])
        expected_paras = ['0', '1', '2', '3', '4']
        if len(emphasis_anims) == 0 and entrance_paras == expected_paras:
            print("PASS: Component 3 -- Emphasis removed AND entrance targets paragraphs 0-4 (0.2 pts)")
            total_score += 0.2
        else:
            if len(emphasis_anims) > 0:
                print("FAIL: Component 3 -- Emphasis animations still present")
            else:
                print("FAIL: Component 3 -- Entrance paragraphs: %s, expected %s" % (entrance_paras, expected_paras))
    except Exception as e:
        print("ERROR: Component 3 -- %s" % e)

    final_score = min(total_score, 1.0)
    print("\nScore: %.1f/1.0" % total_score)
    print("REWARD: %.1f" % final_score)
    return final_score


# Entry point
persist_app_state("libreoffice_impress")

file_path = os.path.join(WORKDIR, '%s.pptx' % TASK_ID)
if not os.path.exists(file_path):
    print("File not found: %s" % file_path)
    print("REWARD: 0.0")
else:
    verify_task(file_path)

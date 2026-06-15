"""
Reward Script: Animate bulleted text on slide 5 with word-by-word Fade entrance animation
Task ID: impress_ma_073
Domain: libreoffice_impress
Scoring:
  Component 1: Timing/animation element exists on slide 5 (0.15 pts)
  Component 2: Fade entrance animation (presetID=10, presetClass=entr) (0.30 pts)
  Component 3: Word-by-word iteration (iterate type=wd) (0.30 pts)
  Component 4: Animation targets the text box shape on slide 5 (0.15 pts)
  Component 5: Fade filter in animEffect (0.10 pts)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_ma_073'

# Namespaces used in OOXML
P_NS = 'http://schemas.openxmlformats.org/presentationml/2006/main'
A_NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'


def find_textbox_spid(root):
    """Find the shape ID of the text box containing the target sentence on slide 5."""
    for elem in root.iter():
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        if tag == 'cNvPr':
            name = elem.get('name', '')
            # The text box is named 'TextBox 2' (not a placeholder/title)
            if 'TextBox' in name:
                return elem.get('id')
    return None


def verify_task(file_path):
    """
    Verify that slide 5 has a Fade entrance animation with word-by-word text reveal.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid pptx
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open ZIP: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: slide5.xml must exist
    try:
        with zf.open('ppt/slides/slide5.xml') as f:
            slide5_content = f.read()
        root = ET.fromstring(slide5_content)
    except Exception as e:
        print(f"CRITICAL: Cannot parse slide5.xml: {e}")
        print("REWARD: 0.0")
        zf.close()
        return 0.0

    # Find the text box shape ID for later target verification
    textbox_spid = find_textbox_spid(root)
    print(f"INFO: Text box shape ID on slide 5: {textbox_spid}")

    # Component 1: Timing/animation element exists on slide 5 (0.15 pts)
    # This MUST fail on initial (no animations) and pass on golden (has animations)
    try:
        timing_elem = root.find(f'.//{{{P_NS}}}timing')
        if timing_elem is not None:
            # Check there is actual animation content (not just empty timing)
            ctn_nodes = timing_elem.findall(f'.//{{{P_NS}}}cTn')
            if len(ctn_nodes) > 1:  # root cTn + at least one animation cTn
                print(f"PASS: Component 1 — Timing element with animation data found on slide 5 ({len(ctn_nodes)} cTn nodes) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — Timing element found but no animation content")
        else:
            print(f"FAIL: Component 1 — No timing element on slide 5")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Fade entrance animation (presetID=10, presetClass=entr) (0.30 pts)
    # presetID 10 = Fade in OOXML animation presets
    try:
        fade_entrance_found = False
        for ctn in root.findall(f'.//{{{P_NS}}}cTn'):
            preset_id = ctn.get('presetID')
            preset_class = ctn.get('presetClass')
            if preset_id == '10' and preset_class == 'entr':
                fade_entrance_found = True
                break
        if fade_entrance_found:
            print(f"PASS: Component 2 — Fade entrance animation found (presetID=10, presetClass=entr) (0.30 pts)")
            total_score += 0.30
        else:
            # Check what animations exist for diagnostic
            found_anims = []
            for ctn in root.findall(f'.//{{{P_NS}}}cTn'):
                pid = ctn.get('presetID')
                pcl = ctn.get('presetClass')
                if pid is not None:
                    found_anims.append(f"presetID={pid}, presetClass={pcl}")
            print(f"FAIL: Component 2 — No Fade entrance (presetID=10, presetClass=entr). Found: {found_anims}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Word-by-word iteration (iterate type=wd) (0.30 pts)
    # The <p:iterate type="wd"> element indicates word-level animation
    try:
        word_iterate_found = False
        for iterate in root.findall(f'.//{{{P_NS}}}iterate'):
            iter_type = iterate.get('type')
            if iter_type == 'wd':
                word_iterate_found = True
                # Also check tmPct exists (timing percentage for word delay)
                tmPct = iterate.find(f'{{{P_NS}}}tmPct')
                if tmPct is not None:
                    print(f"  INFO: Word iteration timing percentage: {tmPct.get('val')}")
                break
        if word_iterate_found:
            print(f"PASS: Component 3 — Word-by-word iteration found (iterate type=wd) (0.30 pts)")
            total_score += 0.30
        else:
            found_iterates = []
            for iterate in root.findall(f'.//{{{P_NS}}}iterate'):
                found_iterates.append(f"type={iterate.get('type')}")
            print(f"FAIL: Component 3 — No word-by-word iteration. Found iterates: {found_iterates}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Animation targets the text box shape on slide 5 (0.15 pts)
    try:
        targets_textbox = False
        for spTgt in root.findall(f'.//{{{P_NS}}}spTgt'):
            target_spid = spTgt.get('spid')
            if textbox_spid is not None and target_spid == textbox_spid:
                targets_textbox = True
                break
            # Also accept if the target has a txEl child (animating text of some shape)
            tx_el = spTgt.find(f'{{{P_NS}}}txEl')
            if tx_el is not None and target_spid == textbox_spid:
                targets_textbox = True
                break

        if targets_textbox:
            print(f"PASS: Component 4 — Animation targets text box (spid={textbox_spid}) (0.15 pts)")
            total_score += 0.15
        else:
            # Check what shapes are targeted
            targeted = set()
            for spTgt in root.findall(f'.//{{{P_NS}}}spTgt'):
                targeted.add(spTgt.get('spid'))
            print(f"FAIL: Component 4 — Animation does not target text box (spid={textbox_spid}). Targeted spids: {targeted}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Fade filter in animEffect (0.10 pts)
    try:
        fade_filter_found = False
        for anim_effect in root.findall(f'.//{{{P_NS}}}animEffect'):
            filt = anim_effect.get('filter')
            transition = anim_effect.get('transition')
            if filt == 'fade' and transition == 'in':
                fade_filter_found = True
                break
        if fade_filter_found:
            print(f"PASS: Component 5 — Fade filter found in animEffect (transition=in, filter=fade) (0.10 pts)")
            total_score += 0.10
        else:
            found_effects = []
            for ae in root.findall(f'.//{{{P_NS}}}animEffect'):
                found_effects.append(f"filter={ae.get('filter')}, transition={ae.get('transition')}")
            print(f"FAIL: Component 5 — No fade filter in animEffect. Found: {found_effects}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    zf.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

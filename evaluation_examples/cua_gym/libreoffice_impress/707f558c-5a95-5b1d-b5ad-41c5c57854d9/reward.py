"""
Reward Script: Add Appear entrance animations to bullet items and motion path to summary box on slide 3
Task ID: impress_gf3_013
Domain: libreoffice_impress
Scoring:
  Component 1 (0.35): 5 Appear entrance animations exist on slide 3 targeting bullet paragraphs
  Component 2 (0.20): Bullet animations triggered on click (nodeType=clickEffect)
  Component 3 (0.25): Motion path animation exists targeting the summary box shape
  Component 4 (0.20): Motion path triggered after previous (afterEffect) and total 6 animation entries
"""

import os
import zipfile
import xml.etree.ElementTree as ET


WORKDIR = '/home/user'
TASK_ID = 'impress_gf3_013'

NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
}


def persist_app_state(domain):
    """Try to save any unsaved LibreOffice state."""
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


def get_shape_info(root):
    """Extract shape id -> (name, paragraph_count, text_preview) mapping from slide XML."""
    shape_map = {}
    for sp in root.iter():
        if not sp.tag.endswith('}sp'):
            continue
        sp_id = None
        sp_name = None
        for e in sp.iter():
            if e.tag.endswith('cNvPr'):
                sp_id = e.get('id')
                sp_name = e.get('name')
                break
        if sp_id is None:
            continue

        paragraphs = []
        for e in sp.iter():
            if e.tag.endswith('}p') and not e.tag.endswith('}sp'):
                texts = []
                for t in e.iter():
                    if t.tag.endswith('}t') and t.text:
                        texts.append(t.text)
                paragraphs.append(''.join(texts))

        full_text = ' '.join(p for p in paragraphs if p.strip())
        shape_map[sp_id] = {
            'name': sp_name,
            'para_count': len(paragraphs),
            'text': full_text[:200],
            'paragraphs': paragraphs,
        }
    return shape_map


def parse_animations(root):
    """Parse animation entries from the timing element on a slide.
    Returns a list of dicts with keys: preset_id, preset_class, node_type, spid, para_range, path.
    """
    timing = root.find('.//p:timing', NS)
    if timing is None:
        return []

    animations = []
    # Find the mainSeq node — contains all animation entries as child <p:par> elements
    main_seq = None
    for ctn in timing.iter():
        if ctn.tag.endswith('}cTn') and ctn.get('nodeType') == 'mainSeq':
            main_seq = ctn
            break

    if main_seq is None:
        return []

    # Each top-level <p:par> child of mainSeq's childTnLst is one animation entry
    child_list = main_seq.find('{http://schemas.openxmlformats.org/presentationml/2006/main}childTnLst')
    if child_list is None:
        return []

    for top_par in child_list:
        if not top_par.tag.endswith('}par'):
            continue
        # Find the innermost cTn with presetID
        anim_info = {}
        for ctn in top_par.iter():
            if ctn.tag.endswith('}cTn') and ctn.get('presetID') is not None:
                anim_info['preset_id'] = ctn.get('presetID')
                anim_info['preset_class'] = ctn.get('presetClass')
                anim_info['node_type'] = ctn.get('nodeType', '')
                anim_info['preset_subtype'] = ctn.get('presetSubtype', '')
                break

        # Find target shape and optional paragraph range
        for spTgt in top_par.iter():
            if spTgt.tag.endswith('}spTgt'):
                anim_info['spid'] = spTgt.get('spid')
                pRg = spTgt.find('{http://schemas.openxmlformats.org/presentationml/2006/main}txEl/{http://schemas.openxmlformats.org/presentationml/2006/main}pRg')
                if pRg is not None:
                    anim_info['para_st'] = pRg.get('st')
                    anim_info['para_end'] = pRg.get('end')
                break

        # Check for motion path
        for mot in top_par.iter():
            if mot.tag.endswith('}animMotion'):
                anim_info['path'] = mot.get('path', '')
                anim_info['origin'] = mot.get('origin', '')
                break

        if anim_info:
            animations.append(anim_info)

    return animations


def find_bullet_shape_id(shape_map):
    """Find the shape ID that contains the bullet items (5 paragraphs of content)."""
    for sid, info in shape_map.items():
        if info['para_count'] >= 5 and 'communication' in info['text'].lower():
            return sid
    # Fallback: shape with most paragraphs >= 5
    for sid, info in shape_map.items():
        if info['para_count'] >= 5:
            return sid
    return None


def find_summary_shape_id(shape_map):
    """Find the shape ID that contains the summary box ('Apply these daily')."""
    for sid, info in shape_map.items():
        if 'apply these daily' in info['text'].lower():
            return sid
    # Fallback: look for rectangle
    for sid, info in shape_map.items():
        if 'rectangle' in (info['name'] or '').lower():
            return sid
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            with zf.open('ppt/slides/slide3.xml') as f:
                content = f.read().decode()
        root = ET.fromstring(content)
    except Exception as e:
        print(f"CRITICAL: Cannot load slide 3 from {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get shape information
    shape_map = get_shape_info(root)
    print(f"INFO: Shapes on slide 3: {[(sid, info['name'], info['para_count']) for sid, info in shape_map.items()]}")

    bullet_sid = find_bullet_shape_id(shape_map)
    summary_sid = find_summary_shape_id(shape_map)
    print(f"INFO: Bullet shape ID: {bullet_sid}, Summary shape ID: {summary_sid}")

    # Parse all animations
    animations = parse_animations(root)
    print(f"INFO: Found {len(animations)} animation entries")
    for i, anim in enumerate(animations):
        print(f"  Anim {i}: {anim}")

    # Component 1: 5 Appear entrance animations targeting bullet paragraphs (0.35 pts)
    # presetID="1" is "Appear", presetClass="entr" is entrance
    try:
        appear_anims = [a for a in animations
                        if a.get('preset_id') == '1' and a.get('preset_class') == 'entr']
        # Count those targeting paragraph ranges (individual bullet items)
        bullet_appear = [a for a in appear_anims if 'para_st' in a]

        if len(bullet_appear) >= 5:
            # Verify they cover paragraphs 0-4
            para_indices = sorted(set(int(a['para_st']) for a in bullet_appear))
            if len(para_indices) >= 5:
                print(f"PASS: Component 1 — Found {len(bullet_appear)} Appear entrance animations on paragraphs {para_indices} (0.35 pts)")
                total_score += 0.35
            else:
                print(f"PARTIAL: Component 1 — Found {len(bullet_appear)} Appear anims but only {len(para_indices)} unique paragraphs: {para_indices}")
                partial = min(len(para_indices) / 5.0, 1.0) * 0.35
                total_score += partial
                print(f"  Awarding {partial:.2f} pts")
        elif len(bullet_appear) > 0:
            partial = (len(bullet_appear) / 5.0) * 0.35
            total_score += partial
            print(f"PARTIAL: Component 1 — Found {len(bullet_appear)} Appear entrance anims (expected 5), awarding {partial:.2f} pts")
        else:
            print(f"FAIL: Component 1 — No Appear entrance animations found targeting paragraphs. Found {len(appear_anims)} Appear anims total.")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Bullet animations triggered on click (0.20 pts)
    # nodeType="clickEffect" means triggered on click
    try:
        click_appear = [a for a in animations
                        if a.get('preset_id') == '1'
                        and a.get('preset_class') == 'entr'
                        and a.get('node_type') == 'clickEffect'
                        and 'para_st' in a]

        if len(click_appear) >= 5:
            print(f"PASS: Component 2 — All 5 bullet Appear animations are triggered on click (0.20 pts)")
            total_score += 0.20
        elif len(click_appear) > 0:
            partial = (len(click_appear) / 5.0) * 0.20
            total_score += partial
            print(f"PARTIAL: Component 2 — {len(click_appear)}/5 bullet anims triggered on click, awarding {partial:.2f} pts")
        else:
            # Check if there are appear anims with any trigger
            any_appear = [a for a in animations if a.get('preset_id') == '1' and a.get('preset_class') == 'entr']
            print(f"FAIL: Component 2 — No bullet Appear animations with clickEffect trigger. Found {len(any_appear)} Appear anims with triggers: {[a.get('node_type') for a in any_appear]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Motion path animation exists on the summary box (0.25 pts)
    # presetClass="path" indicates a motion path animation
    try:
        motion_anims = [a for a in animations if a.get('preset_class') == 'path']

        if len(motion_anims) >= 1:
            ma = motion_anims[0]
            path_str = ma.get('path', '')
            # Check if it's a horizontal path (moving from right to current position)
            # Typical: "M 0.5 0.0 L 0.0 0.0" means start at 0.5 right offset, end at origin
            has_horizontal_motion = ('path' in ma and ma['path'])
            print(f"PASS: Component 3 — Motion path animation found (path='{path_str}', target spid={ma.get('spid')}) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — No motion path animation found on slide 3")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Motion path triggered after previous + 6 total animation entries (0.20 pts)
    try:
        motion_anims = [a for a in animations if a.get('preset_class') == 'path']
        sub_score = 0.0

        # Check motion path trigger: afterEffect = "After Previous"
        if len(motion_anims) >= 1:
            ma = motion_anims[0]
            if ma.get('node_type') == 'afterEffect':
                print(f"  PASS: Motion path has 'afterEffect' trigger (After Previous)")
                sub_score += 0.10
            else:
                print(f"  FAIL: Motion path trigger is '{ma.get('node_type')}', expected 'afterEffect'")
        else:
            print(f"  FAIL: No motion path animation to check trigger on")

        # Check total count = 6 (5 bullet appears + 1 motion path)
        if len(animations) == 6:
            print(f"  PASS: Total animation entries = 6 (correct)")
            sub_score += 0.10
        elif len(animations) >= 6:
            print(f"  PARTIAL: Total animation entries = {len(animations)} (expected 6, but at least 6 present)")
            sub_score += 0.05
        else:
            print(f"  FAIL: Total animation entries = {len(animations)}, expected 6")

        if sub_score > 0:
            print(f"PASS: Component 4 — Motion path trigger + count check ({sub_score:.2f} pts)")
            total_score += sub_score
        else:
            print(f"FAIL: Component 4 — Both sub-checks failed")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
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

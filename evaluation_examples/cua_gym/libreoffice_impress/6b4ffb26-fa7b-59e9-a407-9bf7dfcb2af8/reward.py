"""
Reward Script: Build slide 2 with layered entrance animations in investor_roadshow.pptx
Task ID: impress_anim_078
Domain: libreoffice_impress
Scoring:
  Component 1: 3 animation entries exist on slide 2           — 0.20 pts
  Component 2: BackgroundRect Fades In (On Click, 1.0s)       — 0.30 pts
  Component 3: TitleBox Flies In from Top (After Prev, 0.3s delay, 0.8s) — 0.30 pts
  Component 4: SubtitleBox Appears (After Prev, 0.2s delay)   — 0.20 pts
  Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user/Desktop'
TASK_ID = 'impress_anim_078'

# XML namespaces for OOXML
NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
}


def get_slide2_timing(pptx_path):
    """Returns the parsed timing XML element for slide 2, or None if not present."""
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        try:
            with zf.open('ppt/slides/slide2.xml') as f:
                root = ET.fromstring(f.read())
                return root.find('.//p:timing', NS)
        except KeyError:
            return None


def collect_animations(timing_elem):
    """
    Collect top-level animation entries (par elements) from the main sequence.
    Returns list of par elements, each representing one animation entry.
    """
    if timing_elem is None:
        return []

    # Navigate: tnLst > par > cTn[tmRoot] > childTnLst > seq[mainSeq] > cTn > childTnLst
    tn_lst = timing_elem.find('p:tnLst', NS)
    if tn_lst is None:
        return []

    root_par = tn_lst.find('p:par', NS)
    if root_par is None:
        return []

    root_ctn = root_par.find('p:cTn', NS)
    if root_ctn is None:
        return []

    child_tn_lst = root_ctn.find('p:childTnLst', NS)
    if child_tn_lst is None:
        return []

    for seq in child_tn_lst.findall('p:seq', NS):
        seq_ctn = seq.find('p:cTn', NS)
        if seq_ctn is not None and seq_ctn.get('nodeType') == 'mainSeq':
            main_child_lst = seq_ctn.find('p:childTnLst', NS)
            if main_child_lst is not None:
                return main_child_lst.findall('p:par', NS)
    return []


def extract_effect_ctn(entry_par):
    """
    From a top-level entry par, extract the innermost effect cTn element.
    Path: par > cTn > childTnLst > par > cTn > childTnLst > par > cTn[effect]
    """
    ctn1 = entry_par.find('p:cTn', NS)
    if ctn1 is None:
        return None
    child1 = ctn1.find('p:childTnLst', NS)
    if child1 is None:
        return None
    par2 = child1.find('p:par', NS)
    if par2 is None:
        return None
    ctn2 = par2.find('p:cTn', NS)
    if ctn2 is None:
        return None
    child2 = ctn2.find('p:childTnLst', NS)
    if child2 is None:
        return None
    par3 = child2.find('p:par', NS)
    if par3 is None:
        return None
    return par3.find('p:cTn', NS)


def get_effect_start_delay(effect_ctn):
    """Return the start condition delay (ms string) for an effect cTn."""
    if effect_ctn is None:
        return None
    st_cond_lst = effect_ctn.find('p:stCondLst', NS)
    if st_cond_lst is None:
        return None
    cond = st_cond_lst.find('p:cond', NS)
    if cond is None:
        return None
    return cond.get('delay')


def get_effect_duration(effect_ctn):
    """
    Return animation effect duration in ms (string).
    For Fade In: animEffect > cBhvr > cTn.dur
    For Fly In: animMotion > cBhvr > cTn.dur
    """
    if effect_ctn is None:
        return None
    child_list = effect_ctn.find('p:childTnLst', NS)
    if child_list is None:
        return None

    for tag in ['p:animEffect', 'p:animMotion']:
        anim = child_list.find(tag, NS)
        if anim is not None:
            cbhvr = anim.find('p:cBhvr', NS)
            if cbhvr is not None:
                ctn = cbhvr.find('p:cTn', NS)
                if ctn is not None:
                    return ctn.get('dur')
    return None


def get_target_spid(effect_ctn):
    """Return the shape ID (string) targeted by this effect."""
    if effect_ctn is None:
        return None
    sp_tgt = effect_ctn.find('.//p:spTgt', NS)
    if sp_tgt is not None:
        return sp_tgt.get('spid')
    return None


def has_anim_effect_filter(effect_ctn, filter_type):
    """Check if effect has an animEffect with a specific filter (e.g. 'fade')."""
    if effect_ctn is None:
        return False
    child_list = effect_ctn.find('p:childTnLst', NS)
    if child_list is None:
        return False
    anim_eff = child_list.find('p:animEffect', NS)
    if anim_eff is not None:
        return anim_eff.get('filter', '').lower() == filter_type.lower()
    return False


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist and be parseable
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        timing = get_slide2_timing(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot read PPTX file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if timing is None:
        print("FAIL: No timing/animation data found on slide 2")
        print("\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    # Collect animation entries from main sequence
    try:
        entries = collect_animations(timing)
    except Exception as e:
        print(f"ERROR: Could not collect animations: {e}")
        entries = []

    # -----------------------------------------------------------------------
    # Component 1: Exactly 3 animation entries exist on slide 2 (0.20 pts)
    # -----------------------------------------------------------------------
    try:
        num_entries = len(entries)
        if num_entries == 3:
            print(f"PASS: Component 1 — 3 animation entries found on slide 2 (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — expected 3 animation entries, found {num_entries}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if len(entries) < 1:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Extract effect cTn elements for each entry
    effects = []
    for i, entry in enumerate(entries):
        try:
            eff = extract_effect_ctn(entry)
            effects.append(eff)
        except Exception as e:
            print(f"  WARNING: Could not extract effect {i+1}: {e}")
            effects.append(None)

    # -----------------------------------------------------------------------
    # Component 2: BackgroundRect (spid=3) Fades In — On Click, 1.0s (0.30 pts)
    # Checks:
    #   - Effect targets spid=3
    #   - nodeType = 'clickEffect' (On Click trigger)
    #   - presetID = 10 (Fade), presetClass = 'entr'
    #   - animEffect filter = 'fade'
    #   - duration = 1000ms (1.0s)
    # -----------------------------------------------------------------------
    try:
        # Find the entry that targets BackgroundRect (spid=3)
        bg_effect = None
        for eff in effects:
            if get_target_spid(eff) == '3':
                bg_effect = eff
                break

        if bg_effect is None:
            print("FAIL: Component 2 — No animation found targeting BackgroundRect (spid=3)")
        else:
            node_type = bg_effect.get('nodeType', '')
            is_click = (node_type == 'clickEffect')
            preset_id = bg_effect.get('presetID', '')
            preset_class = bg_effect.get('presetClass', '')
            is_fade_preset = (preset_id == '10' and preset_class == 'entr')
            has_fade_filter = has_anim_effect_filter(bg_effect, 'fade')
            dur = get_effect_duration(bg_effect)
            is_1s = (dur == '1000')

            # Award points only when the effect is fully correct
            if is_click and is_fade_preset and has_fade_filter and is_1s:
                print("PASS: Component 2 — BackgroundRect Fade In On Click 1.0s: all checks pass (0.30 pts)")
                total_score += 0.30
            elif is_fade_preset and has_fade_filter:
                print(f"PARTIAL: Component 2 — Fade In confirmed; missing: "
                      f"click={is_click}, dur1s={is_1s} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 — BackgroundRect: nodeType={node_type}, "
                      f"presetID={preset_id}, class={preset_class}, "
                      f"fade_filter={has_fade_filter}, dur={dur}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: TitleBox (spid=4) Flies In from Top — After Previous,
    #              0.3s delay, 0.8s duration (0.30 pts)
    # Checks:
    #   - Effect targets spid=4
    #   - nodeType = 'afterEffect' (After Previous)
    #   - presetID = 2 (Fly In), presetSubtype = 8 (from Top)
    #   - delay = 300ms
    #   - duration = 800ms
    # -----------------------------------------------------------------------
    try:
        title_effect = None
        for eff in effects:
            if get_target_spid(eff) == '4':
                title_effect = eff
                break

        if title_effect is None:
            print("FAIL: Component 3 — No animation found targeting TitleBox (spid=4)")
        else:
            node_type = title_effect.get('nodeType', '')
            is_after = (node_type == 'afterEffect')
            preset_id = title_effect.get('presetID', '')
            preset_subtype = title_effect.get('presetSubtype', '')
            is_fly_from_top = (preset_id == '2' and preset_subtype == '8')
            delay = get_effect_start_delay(title_effect)
            is_300ms = (delay == '300')
            dur = get_effect_duration(title_effect)
            is_800ms = (dur == '800')

            # Award full points when all checks pass
            if is_after and is_fly_from_top and is_300ms and is_800ms:
                print("PASS: Component 3 — TitleBox Fly In From Top AfterPrev 300ms/800ms: all checks pass (0.30 pts)")
                total_score += 0.30
            elif is_fly_from_top and is_after:
                print(f"PARTIAL: Component 3 — Fly In From Top After Previous confirmed; "
                      f"missing: delay300={is_300ms}, dur800={is_800ms} (0.15 pts)")
                total_score += 0.15
            elif is_after and preset_id == '2':
                print(f"PARTIAL: Component 3 — Fly In After Previous confirmed; "
                      f"subtype={preset_subtype}, delay={delay}, dur={dur} (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 — TitleBox: nodeType={node_type}, "
                      f"presetID={preset_id}, sub={preset_subtype}, delay={delay}, dur={dur}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -----------------------------------------------------------------------
    # Component 4: SubtitleBox (spid=5) Appears — After Previous, 0.2s delay (0.20 pts)
    # Checks:
    #   - Effect targets spid=5
    #   - nodeType = 'afterEffect' (After Previous)
    #   - presetID = 1 (Appear)
    #   - delay = 200ms
    # -----------------------------------------------------------------------
    try:
        subtitle_effect = None
        for eff in effects:
            if get_target_spid(eff) == '5':
                subtitle_effect = eff
                break

        if subtitle_effect is None:
            print("FAIL: Component 4 — No animation found targeting SubtitleBox (spid=5)")
        else:
            node_type = subtitle_effect.get('nodeType', '')
            is_after = (node_type == 'afterEffect')
            preset_id = subtitle_effect.get('presetID', '')
            is_appear = (preset_id == '1')
            delay = get_effect_start_delay(subtitle_effect)
            is_200ms = (delay == '200')

            # Award full points when all checks pass
            if is_after and is_appear and is_200ms:
                print("PASS: Component 4 — SubtitleBox Appear AfterPrev 200ms: all checks pass (0.20 pts)")
                total_score += 0.20
            elif is_appear and is_after:
                print(f"PARTIAL: Component 4 — Appear After Previous confirmed; "
                      f"missing: delay200={is_200ms}, actual delay={delay} (0.10 pts)")
                total_score += 0.10
            elif is_appear:
                print(f"PARTIAL: Component 4 — Appear confirmed; trigger={node_type}, delay={delay} (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 4 — SubtitleBox: nodeType={node_type}, presetID={preset_id}, delay={delay}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against golden file (path on VM)
file_path = f'{WORKDIR}/{TASK_ID}_initial.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

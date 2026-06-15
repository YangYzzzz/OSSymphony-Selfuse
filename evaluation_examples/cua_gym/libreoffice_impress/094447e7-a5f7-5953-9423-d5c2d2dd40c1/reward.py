"""
Reward Script: Choreographed entrance animation sequence on slide 3
Task ID: impress_gf2_001
Domain: libreoffice_impress
Scoring:
  C1 (0.10) - Timing/animation section exists on slide 3
  C2 (0.15) - Exactly 7 animation entries in sequence
  C3 (0.20) - BackgroundRect: Fade entrance, ~1s duration, On Click trigger
  C4 (0.20) - TitleBox: Fly In From Top entrance, ~0.5s duration, After Previous, ~0.5s delay
  C5 (0.35) - 5 bullet points: Appear entrance, After Previous, ~0.3s delay each
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_gf2_001'

# OOXML namespaces
NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}


def parse_slide3_animations(pptx_path):
    """Parse slide 3 XML and extract animation entries from the timing tree."""
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        try:
            with zf.open('ppt/slides/slide3.xml') as f:
                root = ET.parse(f).getroot()
        except KeyError:
            return None, []

    timing = root.find('.//p:timing', NS)
    if timing is None:
        return None, []

    # Navigate: timing > tnLst > par > cTn(tmRoot) > childTnLst > seq > cTn(mainSeq) > childTnLst
    # The mainSeq childTnLst contains click groups; inside each click group, the innermost
    # childTnLst holds the individual animation <p:par> entries with presetID.
    main_seq = timing.find('.//p:seq/p:cTn[@nodeType="mainSeq"]', NS)
    if main_seq is None:
        return timing, []

    # Collect all animation cTn nodes that have a presetID (these are actual animation entries)
    anim_nodes = []
    for ctn in main_seq.iter('{http://schemas.openxmlformats.org/presentationml/2006/main}cTn'):
        if ctn.get('presetID') is not None:
            anim_nodes.append(ctn)

    return timing, anim_nodes


def get_anim_info(ctn):
    """Extract key properties from an animation cTn node."""
    info = {
        'presetID': ctn.get('presetID'),
        'presetClass': ctn.get('presetClass'),
        'presetSubtype': ctn.get('presetSubtype', '0'),
        'nodeType': ctn.get('nodeType'),
        'delay': 0,
        'duration': 0,
        'target_spid': None,
        'target_para_st': None,
    }

    # Get delay from stCondLst
    st_cond = ctn.find('p:stCondLst/p:cond', NS)
    if st_cond is not None:
        try:
            info['delay'] = int(st_cond.get('delay', '0'))
        except (ValueError, TypeError):
            pass

    # Get target shape ID and optional paragraph range
    sp_tgt = ctn.find('.//p:spTgt', NS)
    if sp_tgt is not None:
        info['target_spid'] = sp_tgt.get('spid')
        p_rg = sp_tgt.find('p:txEl/p:pRg', NS)
        if p_rg is not None:
            info['target_para_st'] = p_rg.get('st')

    # Get duration from animEffect or anim child elements
    anim_effect = ctn.find('.//p:animEffect/p:cBhvr/p:cTn', NS)
    if anim_effect is not None:
        try:
            info['duration'] = int(anim_effect.get('dur', '0'))
        except (ValueError, TypeError):
            pass

    # Also check p:anim elements for duration (fly-in uses these)
    for anim_el in ctn.findall('.//p:anim/p:cBhvr/p:cTn', NS):
        try:
            dur = int(anim_el.get('dur', '0'))
            if dur > info['duration']:
                info['duration'] = dur
        except (ValueError, TypeError):
            pass

    # Get filter type from animEffect
    anim_eff = ctn.find('.//p:animEffect', NS)
    if anim_eff is not None:
        info['filter'] = anim_eff.get('filter', '')
    else:
        info['filter'] = ''

    return info


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

    timing, anim_nodes = parse_slide3_animations(file_path)

    # Component 1: Timing/animation section exists on slide 3 (0.10 points)
    try:
        if timing is not None and len(anim_nodes) > 0:
            print(f"PASS: Component 1 -- Animation timing exists on slide 3 with {len(anim_nodes)} entries (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 -- No animation timing found on slide 3 (timing={'exists' if timing else 'missing'}, entries={len(anim_nodes)})")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Exactly 7 animation entries (0.15 points)
    try:
        num_anims = len(anim_nodes)
        if num_anims == 7:
            print(f"PASS: Component 2 -- Exactly 7 animation entries found (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 -- Expected 7 animation entries, found {num_anims}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: BackgroundRect Fade entrance, ~1s, On Click (0.20 points)
    try:
        if len(anim_nodes) >= 1:
            a1 = get_anim_info(anim_nodes[0])
            checks = []
            # presetID=10 is Fade
            if a1['presetID'] == '10':
                checks.append('fade_preset')
            else:
                print(f"  DEBUG C3: presetID={a1['presetID']} (expected 10)")
            # presetClass=entr (entrance)
            if a1['presetClass'] == 'entr':
                checks.append('entrance_class')
            else:
                print(f"  DEBUG C3: presetClass={a1['presetClass']} (expected entr)")
            # nodeType=clickEffect (On Click trigger)
            if a1['nodeType'] == 'clickEffect':
                checks.append('click_trigger')
            else:
                print(f"  DEBUG C3: nodeType={a1['nodeType']} (expected clickEffect)")
            # Duration ~1000ms (allow 800-1200ms tolerance)
            if a1['filter'] == 'fade':
                checks.append('fade_filter')
            else:
                print(f"  DEBUG C3: filter={a1['filter']} (expected fade)")
            # Duration check with tolerance
            if 800 <= a1['duration'] <= 1200:
                checks.append('duration_1s')
            else:
                print(f"  DEBUG C3: duration={a1['duration']} (expected ~1000)")

            passed = len(checks)
            if passed >= 4:
                print(f"PASS: Component 3 -- BackgroundRect fade entrance, On Click, ~1s ({passed}/5 sub-checks) (0.20 pts)")
                total_score += 0.20
            elif passed >= 2:
                partial = round(0.20 * passed / 5, 2)
                print(f"PARTIAL: Component 3 -- BackgroundRect animation partially correct ({passed}/5 sub-checks) ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 -- BackgroundRect animation incorrect ({passed}/5 sub-checks, info={a1})")
        else:
            print(f"FAIL: Component 3 -- No animation entries found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: TitleBox Fly In From Top, ~0.5s, After Previous, ~0.5s delay (0.20 points)
    try:
        if len(anim_nodes) >= 2:
            a2 = get_anim_info(anim_nodes[1])
            checks = []
            # presetID=2 is Fly In
            if a2['presetID'] == '2':
                checks.append('fly_in_preset')
            else:
                print(f"  DEBUG C4: presetID={a2['presetID']} (expected 2)")
            # presetClass=entr (entrance)
            if a2['presetClass'] == 'entr':
                checks.append('entrance_class')
            else:
                print(f"  DEBUG C4: presetClass={a2['presetClass']} (expected entr)")
            # presetSubtype=4 means from top
            if a2['presetSubtype'] == '4':
                checks.append('from_top')
            else:
                print(f"  DEBUG C4: presetSubtype={a2['presetSubtype']} (expected 4)")
            # nodeType=afterEffect (After Previous)
            if a2['nodeType'] == 'afterEffect':
                checks.append('after_previous')
            else:
                print(f"  DEBUG C4: nodeType={a2['nodeType']} (expected afterEffect)")
            # Delay ~500ms (allow 300-700ms)
            if 300 <= a2['delay'] <= 700:
                checks.append('delay_05s')
            else:
                print(f"  DEBUG C4: delay={a2['delay']} (expected ~500)")
            # Duration ~500ms (allow 300-700ms)
            if 300 <= a2['duration'] <= 700:
                checks.append('duration_05s')
            else:
                print(f"  DEBUG C4: duration={a2['duration']} (expected ~500)")

            passed = len(checks)
            if passed >= 5:
                print(f"PASS: Component 4 -- TitleBox fly-in from top, After Previous, ~0.5s delay/duration ({passed}/6 sub-checks) (0.20 pts)")
                total_score += 0.20
            elif passed >= 3:
                partial = round(0.20 * passed / 6, 2)
                print(f"PARTIAL: Component 4 -- TitleBox animation partially correct ({passed}/6 sub-checks) ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 -- TitleBox animation incorrect ({passed}/6 sub-checks, info={a2})")
        else:
            print(f"FAIL: Component 4 -- Fewer than 2 animation entries")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: 5 bullet Appear animations, After Previous, ~0.3s delay each (0.35 points)
    try:
        if len(anim_nodes) >= 7:
            bullet_anims = anim_nodes[2:7]
            bullet_pass_count = 0
            for idx, ba in enumerate(bullet_anims):
                bi = get_anim_info(ba)
                sub_ok = 0
                # presetID=1 is Appear
                if bi['presetID'] == '1':
                    sub_ok += 1
                # presetClass=entr
                if bi['presetClass'] == 'entr':
                    sub_ok += 1
                # nodeType=afterEffect
                if bi['nodeType'] == 'afterEffect':
                    sub_ok += 1
                # delay ~300ms (allow 200-500ms)
                if 200 <= bi['delay'] <= 500:
                    sub_ok += 1
                # targets a paragraph of BulletList (spid=4 with pRg)
                if bi['target_para_st'] == str(idx):
                    sub_ok += 1

                if sub_ok >= 4:
                    bullet_pass_count += 1
                else:
                    print(f"  DEBUG C5: Bullet {idx+1} only {sub_ok}/5 sub-checks (info={bi})")

            if bullet_pass_count == 5:
                print(f"PASS: Component 5 -- All 5 bullet Appear animations correct (0.35 pts)")
                total_score += 0.35
            elif bullet_pass_count >= 3:
                partial = round(0.35 * bullet_pass_count / 5, 2)
                print(f"PARTIAL: Component 5 -- {bullet_pass_count}/5 bullet animations correct ({partial} pts)")
                total_score += partial
            elif bullet_pass_count >= 1:
                partial = round(0.35 * bullet_pass_count / 5, 2)
                print(f"PARTIAL: Component 5 -- {bullet_pass_count}/5 bullet animations correct ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 5 -- No bullet animations correct")
        else:
            print(f"FAIL: Component 5 -- Fewer than 7 animation entries (need 2 + 5 bullets)")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

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

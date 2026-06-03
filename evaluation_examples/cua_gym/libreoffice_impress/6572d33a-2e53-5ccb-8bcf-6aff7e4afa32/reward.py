"""
Reward Script: Motion path animation on arrow shape in slide 4
Task ID: impress_rp_015
Domain: libreoffice_impress
Scoring:
  Component 1: Slide 4 has animation timing data with animMotion (0.15)
  Component 2: animMotion targets the arrow shape (spid with rightArrow geometry) (0.25)
  Component 3: Motion path is horizontal (Y values near 0) (0.20)
  Component 4: Animation duration is 2 seconds (2000ms) (0.20)
  Component 5: Animation trigger is On Click (sequence-based) (0.20)
"""

import os
import re
import zipfile
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'impress_rp_015'

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

    # Read slide4.xml
    try:
        slide4_xml = zf.read('ppt/slides/slide4.xml').decode('utf-8')
    except Exception as e:
        print(f"CRITICAL: Cannot read slide4.xml: {e}")
        print("REWARD: 0.0")
        return 0.0

    ns = {
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    }
    root = etree.fromstring(slide4_xml.encode('utf-8'))

    # First, identify the arrow shape's spid for later checks
    arrow_spid = None
    for sp in root.findall('.//p:cSld/p:spTree/p:sp', ns):
        geom = sp.find('.//a:prstGeom', ns)
        if geom is not None and 'arrow' in (geom.get('prst') or '').lower():
            nvSpPr = sp.find('.//p:nvSpPr/p:cNvPr', ns)
            if nvSpPr is not None:
                arrow_spid = nvSpPr.get('id')
                print(f"INFO: Found arrow shape with spid={arrow_spid}, name={nvSpPr.get('name')}")
                break

    if arrow_spid is None:
        print("CRITICAL: No arrow shape found on slide 4")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Slide 4 has animation timing data with animMotion (0.15 points)
    try:
        timing_el = root.find('.//p:timing', ns)
        anim_motions = root.findall('.//p:animMotion', ns)
        if timing_el is not None and len(anim_motions) > 0:
            print(f"PASS: Component 1 -- Slide 4 has timing with {len(anim_motions)} animMotion element(s) (0.15 pts)")
            total_score += 0.15
        else:
            has_timing = timing_el is not None
            print(f"FAIL: Component 1 -- timing={has_timing}, animMotion count={len(anim_motions)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: animMotion targets the arrow shape (0.25 points)
    try:
        target_matches_arrow = False
        for am in anim_motions:
            sp_tgt = am.find('.//p:spTgt', ns)
            if sp_tgt is not None:
                targeted_spid = sp_tgt.get('spid')
                if targeted_spid == arrow_spid:
                    target_matches_arrow = True
                    print(f"PASS: Component 2 -- animMotion targets arrow shape spid={arrow_spid} (0.25 pts)")
                    total_score += 0.25
                    break
                else:
                    print(f"FAIL: Component 2 -- animMotion targets spid={targeted_spid}, expected arrow spid={arrow_spid}")
            else:
                print(f"FAIL: Component 2 -- animMotion has no spTgt element")

        if not target_matches_arrow and len(anim_motions) > 0:
            # Already printed FAIL above
            pass
        elif len(anim_motions) == 0:
            print(f"FAIL: Component 2 -- No animMotion elements found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Motion path is horizontal (Y values near 0) (0.20 points)
    try:
        path_is_horizontal = False
        for am in anim_motions:
            path_str = am.get('path')
            if path_str:
                print(f"INFO: Motion path = {path_str}")
                # Parse path coordinates: M x1 y1 L x2 y2 E
                coords = re.findall(r'[-\d.]+', path_str)
                if len(coords) >= 4:
                    # coords = [x1, y1, x2, y2, ...]
                    y_values = [float(coords[i]) for i in range(1, len(coords), 2)]
                    max_y_deviation = max(abs(y) for y in y_values)
                    if max_y_deviation < 0.05:  # Y values near 0 = horizontal path
                        path_is_horizontal = True
                        print(f"PASS: Component 3 -- Path is horizontal, Y deviation={max_y_deviation:.4f} (0.20 pts)")
                        total_score += 0.20
                    else:
                        print(f"FAIL: Component 3 -- Path Y deviation={max_y_deviation:.4f}, not horizontal")
                else:
                    print(f"FAIL: Component 3 -- Could not parse enough coordinates from path")
            else:
                print(f"FAIL: Component 3 -- animMotion has no path attribute")

        if not path_is_horizontal and len(anim_motions) == 0:
            print(f"FAIL: Component 3 -- No animMotion elements found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Animation duration is 2 seconds (2000ms) (0.20 points)
    try:
        duration_correct = False
        for am in anim_motions:
            # Duration is on the cBhvr/cTn child of animMotion
            ctn = am.find('.//p:cTn', ns)
            if ctn is not None:
                dur = ctn.get('dur')
                if dur is not None:
                    dur_int = int(dur)
                    if dur_int == 2000:
                        duration_correct = True
                        print(f"PASS: Component 4 -- Duration is 2000ms (2 seconds) (0.20 pts)")
                        total_score += 0.20
                    else:
                        print(f"FAIL: Component 4 -- Duration is {dur_int}ms, expected 2000ms")
                else:
                    print(f"FAIL: Component 4 -- cTn has no dur attribute")
            else:
                print(f"FAIL: Component 4 -- No cTn found in animMotion")

        if not duration_correct and len(anim_motions) == 0:
            print(f"FAIL: Component 4 -- No animMotion elements found")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Animation trigger is On Click (sequence-based mainSeq) (0.20 points)
    try:
        is_on_click = False
        # On Click animations are within a <p:seq> with <p:cTn nodeType="mainSeq">
        main_seq = root.find('.//p:timing//p:seq/p:cTn[@nodeType="mainSeq"]', ns)
        if main_seq is not None:
            # Verify that our animMotion is nested inside this mainSeq
            # Check if any animMotion under mainSeq targets the arrow
            parent_seq = main_seq.getparent()  # <p:seq>
            anim_in_seq = parent_seq.findall('.//p:animMotion', ns)
            for am in anim_in_seq:
                sp_tgt = am.find('.//p:spTgt', ns)
                if sp_tgt is not None and sp_tgt.get('spid') == arrow_spid:
                    is_on_click = True
                    print(f"PASS: Component 5 -- Animation is On Click (inside mainSeq) (0.20 pts)")
                    total_score += 0.20
                    break
            if not is_on_click:
                print(f"FAIL: Component 5 -- animMotion for arrow not found inside mainSeq")
        else:
            print(f"FAIL: Component 5 -- No mainSeq found in timing (not On Click trigger)")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

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

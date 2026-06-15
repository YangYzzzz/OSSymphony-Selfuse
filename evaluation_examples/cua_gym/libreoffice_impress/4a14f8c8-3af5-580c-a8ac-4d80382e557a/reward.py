"""
Reward Script: Add motion path animations to 4 arrow shapes on slide 8
Task ID: impress_fix_085
Domain: libreoffice_impress
Scoring:
  Component 1 (0.3): Timing/animation structure exists on slide 8
  Component 2 (0.4): All 4 arrow shapes have motion path animations with horizontal paths
  Component 3 (0.15): Animation duration is ~1 second for each
  Component 4 (0.15): Animations use "After Previous" sequencing (afterEffect nodeType)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_fix_085'

# The 4 arrow shape IDs on slide 8
ARROW_SPIDS = {'4', '6', '8', '10'}
ARROW_NAMES = {
    '4': 'Right Arrow 3 (Procurement)',
    '6': 'Right Arrow 5 (Assembly)',
    '8': 'Right Arrow 7 (Quality Control)',
    '10': 'Right Arrow 9 (Distribution)',
}

NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
}


def _is_horizontal_path(path):
    """Check if a motion path string represents horizontal movement to the right."""
    if not path:
        return False
    parts = path.strip().split()
    if len(parts) >= 6 and parts[0] == 'M' and parts[3] == 'L' and parts[-1] == 'E':
        try:
            y_start = float(parts[2])
            x_end = float(parts[4])
            y_end = float(parts[5])
            return abs(y_start - y_end) < 0.01 and x_end > 0
        except ValueError:
            return False
    return False


def parse_animations(pptx_path, slide_number=8):
    """Parse slide XML to extract animation info for the target slide."""
    results = {
        'has_timing': False,
        'motion_paths': {},  # spid -> {path, dur, preset_class, node_type}
    }

    try:
        with zipfile.ZipFile(pptx_path, 'r') as zf:
            slide_xml_path = f'ppt/slides/slide{slide_number}.xml'
            if slide_xml_path not in zf.namelist():
                print(f"FAIL: {slide_xml_path} not found in archive")
                return results

            with zf.open(slide_xml_path) as f:
                content = f.read().decode('utf-8')
                root = ET.fromstring(content)

            # Check for timing element
            timing = root.find('.//p:timing', NS)
            if timing is None:
                return results

            results['has_timing'] = True

            # Find all animMotion elements
            for anim_motion in root.iter():
                tag = anim_motion.tag.split('}')[-1] if '}' in anim_motion.tag else anim_motion.tag
                if tag != 'animMotion':
                    continue

                path_val = anim_motion.get('path', '')
                origin = anim_motion.get('origin', '')

                # Find the target shape ID from cBhvr/tgtEl/spTgt
                spid = None
                dur = None
                for child in anim_motion:
                    child_tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                    if child_tag == 'cBhvr':
                        for sub in child:
                            sub_tag = sub.tag.split('}')[-1] if '}' in sub.tag else sub.tag
                            if sub_tag == 'cTn':
                                dur = sub.get('dur', '')
                            if sub_tag == 'tgtEl':
                                for tgt in sub:
                                    tgt_tag = tgt.tag.split('}')[-1] if '}' in tgt.tag else tgt.tag
                                    if tgt_tag == 'spTgt':
                                        spid = tgt.get('spid', '')

                if spid:
                    results['motion_paths'][spid] = {
                        'path': path_val,
                        'dur': dur,
                        'origin': origin,
                    }

            # Also extract nodeType from the parent cTn of each animMotion
            # Walk the tree to find cTn elements with presetClass="path"
            for elem in root.iter():
                tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
                if tag == 'cTn' and elem.get('presetClass') == 'path':
                    node_type = elem.get('nodeType', '')
                    # Find the animMotion child's target spid
                    for desc in elem.iter():
                        desc_tag = desc.tag.split('}')[-1] if '}' in desc.tag else desc.tag
                        if desc_tag == 'spTgt':
                            spid = desc.get('spid', '')
                            if spid in results['motion_paths']:
                                results['motion_paths'][spid]['node_type'] = node_type
                                results['motion_paths'][spid]['preset_class'] = 'path'

    except Exception as e:
        print(f"ERROR: Failed to parse animations: {e}")

    return results


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

    anim_data = parse_animations(file_path, slide_number=8)

    # Component 1: Timing/animation structure exists on slide 8 (0.3 points)
    # This is the primary change: initial has NO timing element, golden has one
    try:
        if anim_data['has_timing']:
            motion_count = len(anim_data['motion_paths'])
            if motion_count > 0:
                print(f"PASS: Component 1 — Timing element found with {motion_count} motion path animation(s) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 — Timing element exists but no motion path animations found")
        else:
            print(f"FAIL: Component 1 — No timing/animation structure on slide 8")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 4 arrow shapes have motion path animations with horizontal paths (0.4 points)
    # Award partial credit: 0.1 per arrow shape with a valid horizontal motion path
    try:
        arrows_with_motion = 0
        for spid in ARROW_SPIDS:
            if spid in anim_data['motion_paths']:
                mp = anim_data['motion_paths'][spid]
                path = mp.get('path', '')
                # Check the path is horizontal: starts at origin, moves right (positive X, zero Y change)
                # Expected pattern: "M 0 0 L <positive_x> 0 E" (horizontal line)
                # The path should have the same Y at start and end (horizontal movement)
                if _is_horizontal_path(path):
                    arrows_with_motion += 1
                    print(f"  PASS: Arrow spid={spid} ({ARROW_NAMES.get(spid, '?')}) has horizontal motion path: {mp.get('path', '')}")
                else:
                    print(f"  FAIL: Arrow spid={spid} ({ARROW_NAMES.get(spid, '?')}) has motion path but not horizontal: {mp.get('path', '')}")
            else:
                print(f"  FAIL: Arrow spid={spid} ({ARROW_NAMES.get(spid, '?')}) has no motion path animation")

        if arrows_with_motion == 4:
            comp2_score = 0.4
            print(f"PASS: Component 2 — All 4 arrows have horizontal motion paths ({comp2_score} pts)")
            total_score += comp2_score
        elif arrows_with_motion > 0:
            comp2_score = arrows_with_motion * 0.1
            print(f"PARTIAL: Component 2 — {arrows_with_motion}/4 arrows have horizontal motion paths ({comp2_score} pts)")
            total_score += comp2_score
        else:
            print(f"FAIL: Component 2 — No arrows have horizontal motion paths")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Animation duration is ~1 second (1000ms) for each arrow (0.15 points)
    try:
        correct_duration_count = 0
        for spid in ARROW_SPIDS:
            if spid in anim_data['motion_paths']:
                dur = anim_data['motion_paths'][spid].get('dur', '')
                try:
                    dur_val = int(dur)
                    # Allow some tolerance: 500-2000ms is acceptable, but 1000 is ideal
                    if 500 <= dur_val <= 2000:
                        correct_duration_count += 1
                        print(f"  PASS: Arrow spid={spid} duration={dur_val}ms")
                    else:
                        print(f"  FAIL: Arrow spid={spid} duration={dur_val}ms (expected ~1000ms)")
                except (ValueError, TypeError):
                    print(f"  FAIL: Arrow spid={spid} invalid duration: {dur}")

        if correct_duration_count == 4:
            print(f"PASS: Component 3 — All 4 arrows have ~1s duration (0.15 pts)")
            total_score += 0.15
        elif correct_duration_count > 0:
            partial = 0.15 * (correct_duration_count / 4)
            print(f"PARTIAL: Component 3 — {correct_duration_count}/4 arrows have correct duration ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No arrows have correct duration")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Animations use "After Previous" sequencing (0.15 points)
    # In OOXML, "After Previous" = nodeType="afterEffect"
    try:
        after_prev_count = 0
        for spid in ARROW_SPIDS:
            if spid in anim_data['motion_paths']:
                node_type = anim_data['motion_paths'][spid].get('node_type', '')
                # "afterEffect" = After Previous, "clickEffect" = On Click, "withEffect" = With Previous
                if node_type == 'afterEffect':
                    after_prev_count += 1
                    print(f"  PASS: Arrow spid={spid} nodeType=afterEffect (After Previous)")
                else:
                    print(f"  PARTIAL: Arrow spid={spid} nodeType={node_type!r} (expected afterEffect)")

        if after_prev_count == 4:
            print(f"PASS: Component 4 — All 4 arrows use 'After Previous' sequencing (0.15 pts)")
            total_score += 0.15
        elif after_prev_count > 0:
            partial = 0.15 * (after_prev_count / 4)
            print(f"PARTIAL: Component 4 — {after_prev_count}/4 arrows use 'After Previous' ({partial:.3f} pts)")
            total_score += partial
        else:
            # Still give partial credit if animations exist but with different trigger
            animated_count = sum(1 for spid in ARROW_SPIDS if spid in anim_data['motion_paths'])
            if animated_count > 0:
                print(f"FAIL: Component 4 — Animations exist but none use 'After Previous' trigger")
            else:
                print(f"FAIL: Component 4 — No animations found to check trigger type")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

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

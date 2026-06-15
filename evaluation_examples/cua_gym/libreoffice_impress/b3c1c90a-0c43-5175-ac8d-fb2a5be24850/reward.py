"""
Reward Script: Add Fly In from Bottom entrance animation to chart on slide 5
Task ID: impress_sales_032
Domain: libreoffice_impress
Scoring:
  Component 1 (0.4): Chart shape on slide 5 has an entrance animation
  Component 2 (0.3): Animation is Fly In from Bottom (ppt_y from bottom)
  Component 3 (0.3): Triggered after previous with 0.5s delay
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_sales_032'

# Namespaces used in PPTX XML
NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}


def find_chart_shape_id(root):
    """Find the shape ID of the chart (graphicFrame) on the slide."""
    for gf in root.findall('.//p:graphicFrame', NS):
        nvPr = gf.find('.//p:cNvPr', NS)
        if nvPr is not None:
            return nvPr.get('id')
    return None


def get_animation_pars_for_shape(root, spid):
    """
    Get all <p:par> timing nodes that contain animations targeting the given shape ID.
    Returns a list of (par_cTn_element, anim_children) tuples.
    """
    results = []
    # Navigate to mainSeq childTnLst
    timing = root.find('.//p:timing', NS)
    if timing is None:
        return results

    # Find all p:par elements inside the main sequence
    main_seq_ctn = timing.find('.//p:seq/p:cTn', NS)
    if main_seq_ctn is None:
        return results

    child_list = main_seq_ctn.find('p:childTnLst', NS)
    if child_list is None:
        return results

    # Each top-level par in mainSeq represents a click group
    for top_par in child_list.findall('p:par', NS):
        top_ctn = top_par.find('p:cTn', NS)
        if top_ctn is None:
            continue
        inner_child_list = top_ctn.find('p:childTnLst', NS)
        if inner_child_list is None:
            continue

        # Each inner par represents an individual animation
        for inner_par in inner_child_list.findall('p:par', NS):
            inner_ctn = inner_par.find('p:cTn', NS)
            if inner_ctn is None:
                continue
            anim_child_list = inner_ctn.find('p:childTnLst', NS)
            if anim_child_list is None:
                continue

            # Check if any child animation targets our shape
            matching_tgts = [
                child for child in list(anim_child_list)
                if child.find('.//p:spTgt', NS) is not None
                and child.find('.//p:spTgt', NS).get('spid') == spid
            ]

            if len(matching_tgts) > 0:
                results.append((inner_ctn, list(anim_child_list)))

    return results


def check_fly_in_from_bottom(anim_children):
    """
    Check if animation children represent a Fly In from Bottom effect.
    Fly In from Bottom animates ppt_y from "1+#ppt_h/2" to "#ppt_y".
    """
    for child in anim_children:
        tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
        if tag == 'anim':
            attr_name_el = child.find('.//p:attrName', NS)
            if attr_name_el is not None and attr_name_el.text == 'ppt_y':
                # Check the from/to values
                tavs = child.findall('.//p:tav', NS)
                if len(tavs) >= 2:
                    from_val = tavs[0].find('.//p:strVal', NS)
                    to_val = tavs[-1].find('.//p:strVal', NS)
                    if from_val is not None and to_val is not None:
                        from_str = from_val.get('val', '')
                        to_str = to_val.get('val', '')
                        # Fly In from Bottom: starts below (1+#ppt_h/2) and ends at original position (#ppt_y)
                        if '1' in from_str and 'ppt_h' in from_str and 'ppt_y' in to_str:
                            return True
    return False


def check_after_previous_with_delay(ctn_element, expected_delay_ms=500):
    """
    Check if the animation is triggered 'After Previous' with the specified delay.
    In PPTX XML, 'After Previous' means the par's stCondLst has a delay > 0
    (it follows the previous animation within the same click group).
    """
    st_cond_list = ctn_element.find('p:stCondLst', NS)
    if st_cond_list is None:
        return False, None

    for cond in st_cond_list.findall('p:cond', NS):
        delay = cond.get('delay')
        if delay is not None:
            try:
                delay_val = int(delay)
                return delay_val == expected_delay_ms, delay_val
            except ValueError:
                pass
    return False, None


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

    # Parse slide 5 XML
    try:
        with zf.open('ppt/slides/slide5.xml') as f:
            root = ET.parse(f).getroot()
    except Exception as e:
        print(f"CRITICAL: Cannot parse slide 5: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the chart shape ID
    chart_spid = find_chart_shape_id(root)
    if chart_spid is None:
        print("CRITICAL: No chart found on slide 5")
        print("REWARD: 0.0")
        return 0.0
    print(f"INFO: Chart shape ID on slide 5: {chart_spid}")

    # Get all animations targeting the chart
    anim_pars = get_animation_pars_for_shape(root, chart_spid)

    # Component 1: Chart has an entrance animation (0.4 points)
    try:
        if len(anim_pars) > 0:
            print(f"PASS: Component 1 — Chart (spid={chart_spid}) has {len(anim_pars)} animation(s) on slide 5 (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Chart (spid={chart_spid}) has no animations on slide 5")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Animation is Fly In from Bottom (0.3 points)
    try:
        if len(anim_pars) > 0:
            ctn, anim_children = anim_pars[0]
            is_fly_in = check_fly_in_from_bottom(anim_children)
            if is_fly_in:
                print(f"PASS: Component 2 — Animation is Fly In from Bottom (ppt_y) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Animation is not Fly In from Bottom")
        else:
            print(f"FAIL: Component 2 — No animation to check (depends on Component 1)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Triggered After Previous with 0.5s delay (0.3 points)
    try:
        if len(anim_pars) > 0:
            ctn, anim_children = anim_pars[0]
            delay_ok, actual_delay = check_after_previous_with_delay(ctn, expected_delay_ms=500)
            if delay_ok:
                print(f"PASS: Component 3 — After Previous with 500ms delay (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — Expected 500ms delay, found: {actual_delay}ms")
        else:
            print(f"FAIL: Component 3 — No animation to check (depends on Component 1)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    zf.close()

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

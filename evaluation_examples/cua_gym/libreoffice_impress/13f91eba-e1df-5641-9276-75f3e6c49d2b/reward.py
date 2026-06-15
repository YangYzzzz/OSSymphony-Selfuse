"""
Reward Script: Animated countdown sequence on slide 1
Task ID: impress_gf2_015
Domain: libreoffice_impress
Scoring:
  Component 1: Timing/animation element exists on slide 1 (0.15 pts)
  Component 2: '3' textbox has appear+disappear with 1s delay (0.25 pts)
  Component 3: '2' textbox has appear+disappear with 1s delay (0.25 pts)
  Component 4: '1' textbox has appear+disappear with 1s delay (0.20 pts)
  Component 5: Title textbox has entrance animation after countdown (0.15 pts)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_gf2_015'

NS_P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
NS_A = 'http://schemas.openxmlformats.org/drawingml/2006/main'


def get_shape_text_map(root):
    """Map shape id -> text content for shapes on the slide."""
    shape_map = {}
    for sp in root.iter('{%s}sp' % NS_P):
        cNvPr = None
        for elem in sp.iter():
            if elem.tag.endswith('}cNvPr'):
                cNvPr = elem
                break
        if cNvPr is None:
            continue
        spid = cNvPr.get('id', '')
        texts = []
        for t in sp.iter('{%s}t' % NS_A):
            if t.text:
                texts.append(t.text)
        shape_map[spid] = ' '.join(texts).strip()
    return shape_map


def get_text_to_spid(shape_map):
    """Reverse map: text -> spid."""
    return {v: k for k, v in shape_map.items()}


def parse_animation_actions(timing_elem):
    """
    Parse the timing XML and extract a list of animation actions.
    Each action: {'spid': str, 'value': 'visible'|'hidden', 'delay_ms': int}
    Actions are extracted in document order from the sequential animation tree.
    """
    actions = []
    if timing_elem is None:
        return actions

    # Find all <set> elements which represent appear/disappear animations
    # We need to walk the tree in order and track delays
    def walk_pars(elem, accumulated_delay=0):
        """Recursively walk <par> elements to extract animation actions with delays."""
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag

        if tag == 'set':
            # This is an animation action
            spTgt = elem.find('.//{%s}spTgt' % NS_P)
            strVal = elem.find('.//{%s}strVal' % NS_P)
            if spTgt is not None and strVal is not None:
                actions.append({
                    'spid': spTgt.get('spid', ''),
                    'value': strVal.get('val', ''),
                    'delay_ms': accumulated_delay
                })
            return

        if tag == 'cTn':
            # Check for delay in stCondLst
            stCondLst = elem.find('{%s}stCondLst' % NS_P)
            delay = 0
            if stCondLst is not None:
                cond = stCondLst.find('{%s}cond' % NS_P)
                if cond is not None:
                    delay_str = cond.get('delay', '0')
                    try:
                        delay = int(delay_str)
                    except ValueError:
                        delay = 0
            new_delay = accumulated_delay + delay

            childTnLst = elem.find('{%s}childTnLst' % NS_P)
            if childTnLst is not None:
                for child in childTnLst:
                    walk_pars(child, new_delay)
            return

        if tag == 'par':
            cTn = elem.find('{%s}cTn' % NS_P)
            if cTn is not None:
                walk_pars(cTn, accumulated_delay)
            return

        if tag == 'seq':
            cTn = elem.find('{%s}cTn' % NS_P)
            if cTn is not None:
                walk_pars(cTn, accumulated_delay)
            return

        # For other elements, recurse into children
        for child in elem:
            walk_pars(child, accumulated_delay)

    walk_pars(timing_elem)
    return actions


def extract_animation_pairs(actions, target_spid):
    """
    Given a list of actions, find appear(visible) and disappear(hidden) pairs
    for a specific spid.
    Returns list of tuples: (appear_action, disappear_action) or partial.
    """
    spid_actions = [a for a in actions if a['spid'] == target_spid]
    appears = [a for a in spid_actions if a['value'] == 'visible']
    disappears = [a for a in spid_actions if a['value'] == 'hidden']
    return appears, disappears


def has_delayed_disappear(disappears, min_ms=800, max_ms=2000):
    """Check if any disappear action has a delay within the expected range."""
    return any(d['delay_ms'] >= min_ms and d['delay_ms'] <= max_ms for d in disappears)


def check_countdown_shape(actions, spid, label, points):
    """
    Check a countdown shape has appear + disappear with ~1s delay.
    Returns (score, message).
    """
    if not spid:
        return 0.0, "FAIL: Component %s - Could not find shape '%s'" % (label, label)

    appears, disappears = extract_animation_pairs(actions, spid)

    if len(appears) >= 1 and len(disappears) >= 1:
        if has_delayed_disappear(disappears):
            return points, "PASS: Component %s - '%s' has appear+disappear with delay (%s pts)" % (label, label, points)
        else:
            partial = round(points * 0.6, 2)
            return partial, "PARTIAL: Component %s - '%s' has appear+disappear but delay=%s (expected ~1000ms) (%s pts)" % (label, label, [d['delay_ms'] for d in disappears], partial)
    elif len(appears) >= 1:
        partial = round(points * 0.4, 2)
        return partial, "PARTIAL: Component %s - '%s' has appear but no disappear (%s pts)" % (label, label, partial)
    else:
        return 0.0, "FAIL: Component %s - '%s' has no appear animation" % (label, label)


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            with zf.open('ppt/slides/slide1.xml') as f:
                root = ET.fromstring(f.read())
    except Exception as e:
        print("CRITICAL: Cannot load file %s: %s" % (file_path, e))
        print("REWARD: 0.0")
        return 0.0

    # Get shape text mapping
    shape_map = get_shape_text_map(root)
    text_to_spid = get_text_to_spid(shape_map)
    print("Shape map: %s" % shape_map)

    # Find spids for our target shapes
    spid_3 = text_to_spid.get('3', '')
    spid_2 = text_to_spid.get('2', '')
    spid_1 = text_to_spid.get('1', '')
    # Title might contain "Annual Gala 2024" or similar
    spid_title = ''
    for spid, text in shape_map.items():
        if 'Annual Gala' in text or 'Gala 2024' in text or 'annual gala' in text.lower():
            spid_title = spid
            break

    if not all([spid_3, spid_2, spid_1, spid_title]):
        print("WARNING: Could not identify all target shapes. Found: 3=%s, 2=%s, 1=%s, title=%s" % (spid_3, spid_2, spid_1, spid_title))

    # Component 1: Timing/animation element exists on slide 1 (0.15 pts)
    try:
        timing = root.find('.//{%s}timing' % NS_P)
        if timing is not None:
            # Check it has actual animation content (set elements)
            set_elems = list(timing.iter('{%s}set' % NS_P))
            if len(set_elems) >= 4:
                print("PASS: Component 1 - Timing element exists with %d animation actions (0.15 pts)" % len(set_elems))
                total_score += 0.15
            else:
                print("FAIL: Component 1 - Timing element exists but only %d set actions (need >= 4)" % len(set_elems))
        else:
            print("FAIL: Component 1 - No timing/animation element on slide 1")
    except Exception as e:
        print("ERROR: Component 1 - %s" % e)

    if timing is None:
        final_score = min(total_score, 1.0)
        print("\nScore: %s/1.0" % total_score)
        print("REWARD: %s" % final_score)
        return final_score

    # Parse all animation actions
    actions = parse_animation_actions(timing)
    print("Parsed %d animation actions" % len(actions))
    for i, a in enumerate(actions):
        shape_text = shape_map.get(a['spid'], '?')
        print("  Action %d: spid=%s (%s) -> %s (delay=%dms)" % (i, a['spid'], shape_text, a['value'], a['delay_ms']))

    # Component 2: '3' textbox has appear + disappear with ~1s delay (0.25 pts)
    try:
        score_2, msg_2 = check_countdown_shape(actions, spid_3, '3', 0.25)
        print(msg_2)
        if score_2 > 0:
            total_score += score_2
    except Exception as e:
        print("ERROR: Component 2 - %s" % e)

    # Component 3: '2' textbox has appear + disappear with ~1s delay (0.25 pts)
    try:
        score_3, msg_3 = check_countdown_shape(actions, spid_2, '2', 0.25)
        print(msg_3)
        if score_3 > 0:
            total_score += score_3
    except Exception as e:
        print("ERROR: Component 3 - %s" % e)

    # Component 4: '1' textbox has appear + disappear with ~1s delay (0.20 pts)
    try:
        score_4, msg_4 = check_countdown_shape(actions, spid_1, '1', 0.20)
        print(msg_4)
        if score_4 > 0:
            total_score += score_4
    except Exception as e:
        print("ERROR: Component 4 - %s" % e)

    # Component 5: Title textbox has entrance animation after countdown (0.15 pts)
    try:
        if spid_title:
            appears, disappears = extract_animation_pairs(actions, spid_title)
            has_appear = len(appears) >= 1

            if has_appear:
                # Check it comes after the countdown shapes in action order
                title_appear_idx = None
                last_countdown_idx = None
                for i, a in enumerate(actions):
                    if a['spid'] == spid_title and a['value'] == 'visible':
                        title_appear_idx = i
                    if a['spid'] in [spid_3, spid_2, spid_1]:
                        last_countdown_idx = i

                if title_appear_idx is not None and last_countdown_idx is not None and title_appear_idx > last_countdown_idx:
                    print("PASS: Component 5 - Title has entrance after countdown (action index %d > %d) (0.15 pts)" % (title_appear_idx, last_countdown_idx))
                    total_score += 0.15
                elif title_appear_idx is not None:
                    print("PARTIAL: Component 5 - Title has entrance but ordering unclear (0.10 pts)")
                    total_score += 0.10
                else:
                    print("FAIL: Component 5 - Title appear not found in actions")
            else:
                print("FAIL: Component 5 - Title has no entrance animation")
        else:
            print("FAIL: Component 5 - Could not find title shape")
    except Exception as e:
        print("ERROR: Component 5 - %s" % e)

    final_score = min(total_score, 1.0)
    print("\nScore: %s/1.0" % total_score)
    print("REWARD: %s" % final_score)
    return final_score


# Default: test against canonical artifact path
file_path = '%s/%s.pptx' % (WORKDIR, TASK_ID)
if not os.path.exists(file_path):
    print("File not found: %s" % file_path)
    print("REWARD: 0.0")
else:
    verify_task(file_path)

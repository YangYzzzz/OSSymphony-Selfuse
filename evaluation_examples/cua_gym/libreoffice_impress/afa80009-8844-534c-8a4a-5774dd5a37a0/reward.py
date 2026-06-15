import sys
import zipfile
import re
import xml.etree.ElementTree as ET

def verify_task(file_path):
    """
    Verify that action buttons (Next/Previous) have been added to all slides.

    Scoring breakdown (total 1.0):
      - Prerequisite: File loads and has 20 slides (gate, 0 points)
      - Component 1 (0.15): Slide 1 has exactly 1 action button (Next), no Previous
      - Component 2 (0.15): Slide 20 has exactly 1 action button (Previous), no Next
      - Component 3 (0.30): Slides 2-19 each have both Next and Previous action buttons
      - Component 4 (0.20): All buttons have correct ppaction hyperlink actions
      - Component 5 (0.20): All buttons are in correct positions (Next=bottom-right, Previous=bottom-left)
    """
    total_score = 0.0

    # ---- Helper: parse slide XML to extract action button info ----
    def get_action_buttons_from_xml(pptx_path):
        """Parse XML to get action button details per slide."""
        buttons_per_slide = {}
        with zipfile.ZipFile(pptx_path, 'r') as zf:
            slide_files = [f for f in zf.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', f)]
            for sf in slide_files:
                slide_num = int(re.search(r'slide(\d+)\.xml', sf).group(1))
                with zf.open(sf) as f:
                    content = f.read().decode('utf-8')

                # Extract all shape (p:sp) elements
                shapes = re.findall(r'<p:sp\b.*?</p:sp>', content, re.DOTALL)
                buttons = []
                for s in shapes:
                    # Check for action button preset geometry
                    prst_match = re.search(r'prst="(actionButton[^"]*)"', s)
                    if not prst_match:
                        continue

                    prst = prst_match.group(1)

                    # Extract action from hlinkClick
                    action_match = re.search(r'action="([^"]*)"', s)
                    action = action_match.group(1) if action_match else None

                    # Extract position
                    off_match = re.search(r'<a:off x="(\d+)" y="(\d+)"', s)
                    ext_match = re.search(r'<a:ext cx="(\d+)" cy="(\d+)"', s)
                    x = int(off_match.group(1)) if off_match else 0
                    y = int(off_match.group(2)) if off_match else 0
                    cx = int(ext_match.group(1)) if ext_match else 0
                    cy = int(ext_match.group(2)) if ext_match else 0

                    btn_type = None
                    if 'ForwardNext' in prst or 'forwardNext' in prst:
                        btn_type = 'next'
                    elif 'BackPrevious' in prst or 'backPrevious' in prst:
                        btn_type = 'previous'

                    buttons.append({
                        'type': btn_type,
                        'prst': prst,
                        'action': action,
                        'x': x, 'y': y, 'cx': cx, 'cy': cy
                    })

                buttons_per_slide[slide_num] = buttons
        return buttons_per_slide

    # ---- Prerequisite: File loads and has 20 slides (gate, 0 points) ----
    try:
        from pptx import Presentation
        prs = Presentation(file_path)
        num_slides = len(prs.slides)
        slide_width = prs.slide_width
        slide_height = prs.slide_height

        if num_slides == 20:
            print(f"[PASS] Prerequisite: Presentation has {num_slides} slides")
        else:
            print(f"[FAIL] Prerequisite: Expected 20 slides, found {num_slides}")
            print(f"\nREWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"[FAIL] Prerequisite: Could not load file - {e}")
        print(f"\nREWARD: 0.0")
        return 0.0

    # Parse XML for detailed button analysis
    try:
        buttons_per_slide = get_action_buttons_from_xml(file_path)
    except Exception as e:
        print(f"[FAIL] XML parsing error: {e}")
        print(f"REWARD: {round(total_score, 2)}")
        return round(total_score, 2)

    # ---- Component 1: Slide 1 has exactly 1 Next button, no Previous (0.15) ----
    try:
        s1_buttons = buttons_per_slide.get(1, [])
        s1_next = [b for b in s1_buttons if b['type'] == 'next']
        s1_prev = [b for b in s1_buttons if b['type'] == 'previous']

        if len(s1_next) == 1 and len(s1_prev) == 0:
            total_score += 0.15
            print(f"[PASS] Component 1: Slide 1 has 1 Next button, 0 Previous buttons (0.15)")
        else:
            print(f"[FAIL] Component 1: Slide 1 has {len(s1_next)} Next, {len(s1_prev)} Previous (expected 1 Next, 0 Previous) (0.00)")
    except Exception as e:
        print(f"[FAIL] Component 1: Error checking slide 1 - {e} (0.00)")

    # ---- Component 2: Slide 20 has exactly 1 Previous button, no Next (0.15) ----
    try:
        s20_buttons = buttons_per_slide.get(20, [])
        s20_next = [b for b in s20_buttons if b['type'] == 'next']
        s20_prev = [b for b in s20_buttons if b['type'] == 'previous']

        if len(s20_prev) == 1 and len(s20_next) == 0:
            total_score += 0.15
            print(f"[PASS] Component 2: Slide 20 has 1 Previous button, 0 Next buttons (0.15)")
        else:
            print(f"[FAIL] Component 2: Slide 20 has {len(s20_next)} Next, {len(s20_prev)} Previous (expected 0 Next, 1 Previous) (0.00)")
    except Exception as e:
        print(f"[FAIL] Component 2: Error checking slide 20 - {e} (0.00)")

    # ---- Component 3: Slides 2-19 each have both Next and Previous (0.30) ----
    try:
        slides_ok = 0
        slides_total = 18  # slides 2 through 19
        for sn in range(2, 20):
            sn_buttons = buttons_per_slide.get(sn, [])
            sn_next = [b for b in sn_buttons if b['type'] == 'next']
            sn_prev = [b for b in sn_buttons if b['type'] == 'previous']
            if len(sn_next) >= 1 and len(sn_prev) >= 1:
                slides_ok += 1
            else:
                print(f"  Slide {sn}: {len(sn_next)} Next, {len(sn_prev)} Previous (expected 1 each)")

        comp3_score = round(0.30 * (slides_ok / slides_total), 4)
        total_score += comp3_score
        if slides_ok == slides_total:
            print(f"[PASS] Component 3: All 18 middle slides have both buttons ({comp3_score})")
        else:
            print(f"[FAIL] Component 3: {slides_ok}/{slides_total} middle slides have both buttons ({comp3_score})")
    except Exception as e:
        print(f"[FAIL] Component 3: Error checking middle slides - {e} (0.00)")

    # ---- Component 4: All buttons have correct ppaction hyperlink actions (0.20) ----
    try:
        correct_actions = 0
        total_buttons = 0

        for sn in range(1, 21):
            sn_buttons = buttons_per_slide.get(sn, [])
            for b in sn_buttons:
                if b['type'] in ('next', 'previous'):
                    total_buttons += 1
                    expected_action = 'ppaction://nextslide' if b['type'] == 'next' else 'ppaction://previousslide'
                    if b['action'] == expected_action:
                        correct_actions += 1
                    else:
                        print(f"  Slide {sn} {b['type']} button: action='{b['action']}' (expected '{expected_action}')")

        if total_buttons > 0:
            comp4_score = round(0.20 * (correct_actions / total_buttons), 4)
        else:
            comp4_score = 0.0
        total_score += comp4_score
        if correct_actions == total_buttons and total_buttons > 0:
            print(f"[PASS] Component 4: All {total_buttons} buttons have correct actions ({comp4_score})")
        else:
            print(f"[FAIL] Component 4: {correct_actions}/{total_buttons} buttons have correct actions ({comp4_score})")
    except Exception as e:
        print(f"[FAIL] Component 4: Error checking actions - {e} (0.00)")

    # ---- Component 5: Buttons in correct positions (0.20) ----
    # Next = bottom-right: x > slide_width * 0.5, y > slide_height * 0.7
    # Previous = bottom-left: x < slide_width * 0.3, y > slide_height * 0.7
    try:
        correct_pos = 0
        total_pos_buttons = 0

        # slide_width and slide_height are in EMU
        sw = slide_width
        sh = slide_height

        for sn in range(1, 21):
            sn_buttons = buttons_per_slide.get(sn, [])
            for b in sn_buttons:
                if b['type'] in ('next', 'previous'):
                    total_pos_buttons += 1
                    x, y = b['x'], b['y']
                    cx, cy = b['cx'], b['cy']

                    if b['type'] == 'next':
                        # Bottom-right: right edge near right side, button in bottom region
                        right_edge = x + cx
                        is_right = x > sw * 0.5
                        is_bottom = y > sh * 0.7
                        if is_right and is_bottom:
                            correct_pos += 1
                        else:
                            print(f"  Slide {sn} Next: x={x}({x/sw:.2f}), y={y}({y/sh:.2f}) - right={is_right}, bottom={is_bottom}")
                    elif b['type'] == 'previous':
                        # Bottom-left: left side, bottom region
                        is_left = x < sw * 0.3
                        is_bottom = y > sh * 0.7
                        if is_left and is_bottom:
                            correct_pos += 1
                        else:
                            print(f"  Slide {sn} Previous: x={x}({x/sw:.2f}), y={y}({y/sh:.2f}) - left={is_left}, bottom={is_bottom}")

        if total_pos_buttons > 0:
            comp5_score = round(0.20 * (correct_pos / total_pos_buttons), 4)
        else:
            comp5_score = 0.0
        total_score += comp5_score
        if correct_pos == total_pos_buttons and total_pos_buttons > 0:
            print(f"[PASS] Component 5: All {total_pos_buttons} buttons in correct positions ({comp5_score})")
        else:
            print(f"[FAIL] Component 5: {correct_pos}/{total_pos_buttons} buttons in correct positions ({comp5_score})")
    except Exception as e:
        print(f"[FAIL] Component 5: Error checking positions - {e} (0.00)")

    total_score = round(total_score, 2)
    print(f"\nREWARD: {total_score}")
    return total_score


if __name__ == "__main__":
    file_path = sys.argv[1] if len(sys.argv) > 1 else "/home/user/impress_fix_049.pptx"
    verify_task(file_path)

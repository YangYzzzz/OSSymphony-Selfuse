"""
Reward Script: Kiosk display slide show configuration
Task ID: impress_gf4_026
Domain: libreoffice_impress
Scoring:
  C1 (0.25) - Dissolve transition on all 12 slides
  C2 (0.30) - Correct automatic advance timings per slide
  C3 (0.15) - Mouse click advancement disabled (advClick=0) on all slides
  C4 (0.15) - Kiosk/loop mode enabled in presentation settings
  C5 (0.15) - Exit Kiosk shape on slide 1 with end-show action
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_gf4_026'

# Expected advance times in ms per slide (1-indexed key)
EXPECTED_TIMINGS = {
    1: 10000,
    2: 8000, 3: 8000, 4: 8000, 5: 8000,
    6: 12000, 7: 12000, 8: 12000,
    9: 6000, 10: 6000, 11: 6000,
    12: 15000,
}

NS_P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
NS_A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
NS_R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'


def verify_task(file_path):
    """
    Verify kiosk slideshow configuration with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

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

    # ---- Component 1: Dissolve transition on all 12 slides (0.25 pts) ----
    try:
        dissolve_count = 0
        for i in range(1, 13):
            fname = f'ppt/slides/slide{i}.xml'
            with zf.open(fname) as f:
                root = ET.parse(f).getroot()
            tr = root.find(f'.//{{{NS_P}}}transition')
            if tr is not None:
                dissolve = tr.find(f'{{{NS_P}}}dissolve')
                if dissolve is not None:
                    dissolve_count += 1
                else:
                    children = [c.tag.split('}')[-1] for c in tr]
                    print(f"  Slide {i}: transition found but not dissolve: {children}")
            else:
                print(f"  Slide {i}: no transition element")

        if dissolve_count == 12:
            print(f"PASS: Component 1 — All 12 slides have dissolve transition (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Only {dissolve_count}/12 slides have dissolve transition")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ---- Component 2: Correct advance timings (0.30 pts) ----
    try:
        correct_timings = 0
        for i in range(1, 13):
            fname = f'ppt/slides/slide{i}.xml'
            with zf.open(fname) as f:
                root = ET.parse(f).getroot()
            tr = root.find(f'.//{{{NS_P}}}transition')
            expected_ms = EXPECTED_TIMINGS[i]
            if tr is not None:
                adv_tm = tr.get('advTm')
                if adv_tm is not None and int(adv_tm) == expected_ms:
                    correct_timings += 1
                else:
                    print(f"  Slide {i}: advTm={adv_tm}, expected={expected_ms}")
            else:
                print(f"  Slide {i}: no transition (no timing)")

        if correct_timings == 12:
            print(f"PASS: Component 2 — All 12 slides have correct advance timings (0.30 pts)")
            total_score += 0.30
        elif correct_timings >= 8:
            partial = round(0.30 * correct_timings / 12, 2)
            print(f"PARTIAL: Component 2 — {correct_timings}/12 timings correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Only {correct_timings}/12 timings correct")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ---- Component 3: advClick disabled on all slides (0.15 pts) ----
    try:
        click_disabled_count = 0
        for i in range(1, 13):
            fname = f'ppt/slides/slide{i}.xml'
            with zf.open(fname) as f:
                root = ET.parse(f).getroot()
            tr = root.find(f'.//{{{NS_P}}}transition')
            if tr is not None:
                adv_click = tr.get('advClick', '1')  # default is '1' (enabled)
                if adv_click == '0':
                    click_disabled_count += 1
                else:
                    print(f"  Slide {i}: advClick={adv_click} (should be 0)")
            else:
                print(f"  Slide {i}: no transition element")

        if click_disabled_count == 12:
            print(f"PASS: Component 3 — Mouse click disabled on all 12 slides (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — Only {click_disabled_count}/12 slides have advClick=0")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ---- Component 4: Kiosk/loop mode in presentation settings (0.15 pts) ----
    try:
        with zf.open('ppt/presentation.xml') as f:
            pres_root = ET.parse(f).getroot()

        show_pr = pres_root.find(f'{{{NS_P}}}showPr')
        if show_pr is None:
            # Try with namespace wildcard
            show_pr = pres_root.find(f'.//{{{NS_P}}}showPr')

        if show_pr is not None:
            loop_val = show_pr.get('loop', '0')
            kiosk_el = show_pr.find(f'{{{NS_P}}}kiosk')

            has_loop = loop_val == '1'
            has_kiosk = kiosk_el is not None

            if has_loop and has_kiosk:
                print(f"PASS: Component 4 — Kiosk mode with loop enabled (0.15 pts)")
                total_score += 0.15
            elif has_loop or has_kiosk:
                print(f"PARTIAL: Component 4 — loop={has_loop}, kiosk={has_kiosk} (0.07 pts)")
                total_score += 0.07
            else:
                print(f"FAIL: Component 4 — showPr exists but no loop or kiosk")
        else:
            print(f"FAIL: Component 4 — No showPr element in presentation.xml")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ---- Component 5: Exit Kiosk shape on slide 1 with end-show action (0.15 pts) ----
    try:
        with zf.open('ppt/slides/slide1.xml') as f:
            slide1_content = f.read().decode()

        # Parse and look for a shape with hlinkEndShow action
        root = ET.fromstring(slide1_content)
        # Register namespaces for searching
        found_exit_shape = False
        found_end_show = False
        shape_in_top_left = False

        # Search for hlinkClick with action=ppaction://hlinkEndShow
        # This can be in cNvPr or in a:hlinkClick
        if 'ppaction://hlinkEndShow' in slide1_content:
            found_end_show = True

        # Also verify there's a shape in the top-left corner area
        # Look for shapes at position (0,0) or very close to it
        all_ns = {
            'p': NS_P,
            'a': NS_A,
            'r': NS_R,
        }

        # Find all sp (shape) elements
        for sp in root.iter(f'{{{NS_P}}}sp'):
            # Check if this shape has the endShow action
            cNvPr = sp.find(f'.//{{{NS_P}}}nvSpPr/{{{NS_P}}}cNvPr')
            if cNvPr is None:
                cNvPr = sp.find(f'.//{{{NS_P}}}cNvPr')
            if cNvPr is not None:
                hlinkClick = cNvPr.find(f'{{{NS_A}}}hlinkClick')
                if hlinkClick is not None:
                    action = hlinkClick.get('action', '')
                    if 'hlinkEndShow' in action:
                        found_exit_shape = True
                        # Check position
                        xfrm = sp.find(f'.//{{{NS_A}}}xfrm')
                        if xfrm is not None:
                            off = xfrm.find(f'{{{NS_A}}}off')
                            if off is not None:
                                x = int(off.get('x', '999999'))
                                y = int(off.get('y', '999999'))
                                # Top-left: x and y should be small (within ~1 inch = 914400 EMU)
                                if x <= 914400 and y <= 914400:
                                    shape_in_top_left = True

        if found_exit_shape and found_end_show and shape_in_top_left:
            print(f"PASS: Component 5 — Exit Kiosk shape with end-show action in top-left (0.15 pts)")
            total_score += 0.15
        elif found_end_show:
            print(f"PARTIAL: Component 5 — end-show action found but position issue (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 — No exit shape with end-show action on slide 1")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    zf.close()

    final_score = round(min(total_score, 1.0), 2)
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

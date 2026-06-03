"""
Reward Script: Interactive menu system with navigation and progress bars
Task ID: impress_gf4_023
Domain: libreoffice_impress
Scoring:
  Component 1 (0.25): Slide 1 section buttons have correct hyperlinks to slides 3,7,11,15,19
  Component 2 (0.25): 'Back to Menu' buttons on slides 6,10,14,18,22 link to slide 1
  Component 3 (0.30): Previous/Next navigation arrows on slides 2-22 with correct hyperlinks
  Component 4 (0.20): Progress bar shapes on slides 2-22 with proportional widths
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_gf4_023'

NS_A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
NS_P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
NS_R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'


def get_shapes_per_slide(pptx_path):
    """
    Parse PPTX ZIP to extract all shapes with text, hyperlink targets, and dimensions.
    Returns dict: {slide_num: [shape_dict, ...]}
    """
    result = {}
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        slide_files = sorted(
            [f for f in zf.namelist() if f.startswith('ppt/slides/slide') and f.endswith('.xml')],
            key=lambda x: int(x.replace('ppt/slides/slide', '').replace('.xml', ''))
        )

        for slide_file in slide_files:
            slide_num = int(slide_file.replace('ppt/slides/slide', '').replace('.xml', ''))

            # Load rels for this slide
            rels_file = slide_file.replace('slides/', 'slides/_rels/') + '.rels'
            rels_map = {}
            try:
                with zf.open(rels_file) as rf:
                    rels_root = ET.parse(rf).getroot()
                    for rel in rels_root:
                        rid = rel.get('Id', '')
                        target = rel.get('Target', '')
                        if rid and target:
                            rels_map[rid] = target
            except KeyError:
                pass

            with zf.open(slide_file) as sf:
                root = ET.parse(sf).getroot()

            sp_tree = root.find(f'{{{NS_P}}}cSld/{{{NS_P}}}spTree')
            if sp_tree is None:
                result[slide_num] = []
                continue

            shapes = []
            for sp in sp_tree:
                tag = sp.tag.split('}')[-1] if '}' in sp.tag else sp.tag
                if tag != 'sp':
                    continue

                # Extract text from txBody - search in BOTH namespaces
                text = ''
                # txBody can be in p: namespace (p:txBody) for shape elements
                txBody = sp.find(f'{{{NS_P}}}txBody')
                if txBody is None:
                    txBody = sp.find(f'{{{NS_A}}}txBody')
                if txBody is not None:
                    for t_elem in txBody.findall(f'.//{{{NS_A}}}t'):
                        if t_elem.text:
                            text += t_elem.text

                # Extract dimensions from xfrm
                xfrm = sp.find(f'.//{{{NS_A}}}xfrm')
                width = height = left = top = 0
                if xfrm is not None:
                    ext = xfrm.find(f'{{{NS_A}}}ext')
                    off = xfrm.find(f'{{{NS_A}}}off')
                    if ext is not None:
                        width = int(ext.get('cx', '0'))
                        height = int(ext.get('cy', '0'))
                    if off is not None:
                        left = int(off.get('x', '0'))
                        top = int(off.get('y', '0'))

                # Extract hyperlink target from cNvPr hlinkClick
                target = None
                nvSpPr = sp.find(f'{{{NS_P}}}nvSpPr')
                if nvSpPr is not None:
                    # cNvPr is in p: namespace
                    cNvPr = nvSpPr.find(f'{{{NS_P}}}cNvPr')
                    if cNvPr is not None:
                        hlinkClick = cNvPr.find(f'{{{NS_A}}}hlinkClick')
                        if hlinkClick is not None:
                            rid = hlinkClick.get(f'{{{NS_R}}}id', '')
                            if rid and rid in rels_map:
                                target = rels_map[rid]

                # Fallback: check run-level hyperlinks
                if target is None and txBody is not None:
                    for r_elem in txBody.findall(f'.//{{{NS_A}}}r'):
                        rPr = r_elem.find(f'{{{NS_A}}}rPr')
                        if rPr is not None:
                            hlinkClick = rPr.find(f'{{{NS_A}}}hlinkClick')
                            if hlinkClick is not None:
                                rid = hlinkClick.get(f'{{{NS_R}}}id', '')
                                if rid and rid in rels_map:
                                    target = rels_map[rid]
                                    break

                shapes.append({
                    'text': text.strip(),
                    'target': target,
                    'width': width,
                    'height': height,
                    'left': left,
                    'top': top,
                })

            result[slide_num] = shapes

    return result


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        all_shapes = get_shapes_per_slide(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if len(all_shapes) < 22:
        print(f"CRITICAL: Expected 22 slides, found {len(all_shapes)}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Slide 1 section buttons have hyperlinks to correct slides (0.25 pts)
    # Expected: Strategy->slide3, Operations->slide7, Finance->slide11, People->slide15, Outlook->slide19
    try:
        section_map = {
            'Strategy': 'slide3.xml',
            'Operations': 'slide7.xml',
            'Finance': 'slide11.xml',
            'People': 'slide15.xml',
            'Outlook': 'slide19.xml',
        }
        slide1_shapes = all_shapes.get(1, [])
        matched = 0
        for section_name, expected_target in section_map.items():
            found_link = False
            for shape in slide1_shapes:
                if section_name.lower() in shape['text'].lower() and shape['target'] is not None:
                    if expected_target in shape['target']:
                        found_link = True
                        break
            if found_link:
                matched += 1
                print(f"  PASS: '{section_name}' button links to {expected_target}")
            else:
                print(f"  FAIL: '{section_name}' button missing or wrong link")

        if matched == 5:
            print(f"PASS: Component 1 - All 5 section buttons have correct hyperlinks (0.25 pts)")
            total_score += 0.25
        elif matched >= 3:
            partial = round(0.25 * matched / 5, 3)
            print(f"PARTIAL: Component 1 - {matched}/5 section buttons correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 - Only {matched}/5 section buttons correct")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: 'Back to Menu' buttons on slides 6,10,14,18,22 link to slide 1 (0.25 pts)
    try:
        back_to_menu_slides = [6, 10, 14, 18, 22]
        btm_matched = 0
        for snum in back_to_menu_slides:
            shapes = all_shapes.get(snum, [])
            found_btm = False
            for shape in shapes:
                text_lower = shape['text'].lower()
                if 'back' in text_lower and 'menu' in text_lower and shape['target'] is not None:
                    if 'slide1.xml' in shape['target']:
                        found_btm = True
                        break
            if found_btm:
                btm_matched += 1
                print(f"  PASS: Slide {snum} has 'Back to Menu' -> slide1")
            else:
                print(f"  FAIL: Slide {snum} missing 'Back to Menu' -> slide1")

        if btm_matched == 5:
            print(f"PASS: Component 2 - All 5 'Back to Menu' buttons correct (0.25 pts)")
            total_score += 0.25
        elif btm_matched >= 1:
            partial = round(0.25 * btm_matched / 5, 3)
            print(f"PARTIAL: Component 2 - {btm_matched}/5 'Back to Menu' buttons correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 - No 'Back to Menu' buttons found")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Previous/Next navigation arrows on slides 2-22 (0.30 pts)
    try:
        nav_correct = 0
        nav_total = 0
        for snum in range(2, 23):
            shapes = all_shapes.get(snum, [])
            prev_target = f'slide{snum - 1}.xml'
            next_target = f'slide{snum + 1}.xml' if snum < 22 else f'slide{snum}.xml'

            has_prev = False
            has_next = False
            for shape in shapes:
                if shape['target'] is None:
                    continue
                # Identify arrow shapes by text content or position
                is_left_arrow = (
                    '\u25c0' in shape['text'] or
                    'prev' in shape['text'].lower() or
                    '\u2190' in shape['text'] or
                    '\u25c4' in shape['text'] or
                    (shape['left'] < 1000000 and shape['top'] > 5500000 and shape['width'] < 700000)
                )
                is_right_arrow = (
                    '\u25b6' in shape['text'] or
                    'next' in shape['text'].lower() or
                    '\u2192' in shape['text'] or
                    '\u25ba' in shape['text'] or
                    (shape['left'] > 10000000 and shape['top'] > 5500000 and shape['width'] < 700000)
                )

                if is_left_arrow and prev_target in shape['target']:
                    has_prev = True
                if is_right_arrow and next_target in shape['target']:
                    has_next = True

            if has_prev:
                nav_correct += 1
            if has_next:
                nav_correct += 1
            nav_total += 2

        nav_ratio = nav_correct / nav_total if nav_total > 0 else 0
        nav_score = round(0.30 * nav_ratio, 3)
        if nav_ratio >= 0.95:
            print(f"PASS: Component 3 - Navigation arrows: {nav_correct}/{nav_total} correct (0.30 pts)")
            total_score += 0.30
        elif nav_correct > 0:
            print(f"PARTIAL: Component 3 - Navigation arrows: {nav_correct}/{nav_total} correct ({nav_score} pts)")
            total_score += nav_score
        else:
            print(f"FAIL: Component 3 - No navigation arrows found")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Progress bar shapes on slides 2-22 (0.20 pts)
    # Each slide should have thin rectangles at the bottom representing progress.
    # Sections: Strategy(3-6), Operations(7-10), Finance(11-14), People(15-18), Outlook(19-22)
    # Slide 2 is standalone.
    try:
        sections = {}
        sections[2] = (1, 1)
        for start in [3, 7, 11, 15, 19]:
            for s in range(start, start + 4):
                pos = s - start + 1
                sections[s] = (pos, 4)

        progress_bar_found = 0
        progress_bar_proportional = 0

        for snum in range(2, 23):
            shapes = all_shapes.get(snum, [])
            # Find thin rectangles near bottom with no hyperlink
            bottom_bars = []
            for shape in shapes:
                if (shape['top'] > 6000000 and
                    shape['height'] < 300000 and
                    shape['height'] > 0 and
                    shape['width'] > 0 and
                    shape['target'] is None):
                    bottom_bars.append(shape)

            if len(bottom_bars) >= 2:
                progress_bar_found += 1

                # Check proportionality
                bottom_bars.sort(key=lambda s: s['width'])
                pos, length = sections.get(snum, (1, 1))
                expected_ratio = pos / length

                if bottom_bars[1]['width'] > 0:
                    actual_ratio = bottom_bars[0]['width'] / bottom_bars[1]['width']
                else:
                    actual_ratio = 0

                # For full progress (last slide in section), both bars should be same width
                if expected_ratio >= 0.99:
                    if abs(bottom_bars[0]['width'] - bottom_bars[1]['width']) < 500000:
                        progress_bar_proportional += 1
                else:
                    tolerance = 0.25
                    if abs(actual_ratio - expected_ratio) <= tolerance:
                        progress_bar_proportional += 1
            elif len(bottom_bars) >= 1:
                progress_bar_found += 0.5

        total_slides_checked = 21
        bar_found_ratio = progress_bar_found / total_slides_checked
        bar_prop_ratio = progress_bar_proportional / total_slides_checked

        bar_score = round(0.20 * (0.6 * bar_found_ratio + 0.4 * bar_prop_ratio), 3)

        if bar_found_ratio >= 0.9 and bar_prop_ratio >= 0.7:
            print(f"PASS: Component 4 - Progress bars found on {progress_bar_found}/{total_slides_checked} slides, "
                  f"{progress_bar_proportional}/{total_slides_checked} proportional (0.20 pts)")
            total_score += 0.20
        elif progress_bar_found > 0:
            print(f"PARTIAL: Component 4 - Progress bars found on {progress_bar_found}/{total_slides_checked} slides, "
                  f"{progress_bar_proportional}/{total_slides_checked} proportional ({bar_score} pts)")
            total_score += bar_score
        else:
            print(f"FAIL: Component 4 - No progress bars found")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

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

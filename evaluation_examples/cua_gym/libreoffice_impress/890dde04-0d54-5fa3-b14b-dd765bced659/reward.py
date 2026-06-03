"""
Reward Script: Change bullet color to red (#CC0000) on all slides
Task ID: impstruct_029
Domain: libreoffice_impress
Scoring:
  Component 1 (0.30): Bullet color CC0000 on slides 2-3
  Component 2 (0.30): Bullet color CC0000 on slides 4-5
  Component 3 (0.15): Bullet color CC0000 on slide 6
  Component 4 (0.15): No custom bullet character (default round preserved)
  Component 5 (0.10): Slide 1 title paragraphs have no bullet color
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impstruct_029'

NS = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
}


def get_bullet_info_for_slide(zf, slide_num):
    """
    Extract bullet color and character info for all non-empty paragraphs on a slide.
    Returns list of dicts with keys: text, buClr, buChar, is_title_like
    """
    results = []
    try:
        with zf.open(f'ppt/slides/slide{slide_num}.xml') as f:
            root = ET.parse(f).getroot()
            for sp in root.findall('.//p:sp', NS):
                # Detect if this shape is a title/centered title placeholder
                nvSpPr = sp.find('.//p:nvSpPr', NS)
                is_title = False
                if nvSpPr is not None:
                    ph = nvSpPr.find('.//p:ph', NS)
                    if ph is not None:
                        ph_type = ph.get('type', '')
                        if ph_type in ('title', 'ctrTitle', 'subTitle'):
                            is_title = True

                for para in sp.findall('.//a:p', NS):
                    text = ''.join(t.text or '' for t in para.findall('.//a:t', NS))
                    if not text.strip():
                        continue

                    pPr = para.find('a:pPr', NS)
                    buClr = None
                    buChar = None

                    if pPr is not None:
                        buClr_elem = pPr.find('a:buClr', NS)
                        if buClr_elem is not None:
                            srgb = buClr_elem.find('a:srgbClr', NS)
                            if srgb is not None:
                                buClr = srgb.get('val', '').upper()

                        buChar_elem = pPr.find('a:buChar', NS)
                        if buChar_elem is not None:
                            buChar = buChar_elem.get('char')

                    results.append({
                        'text': text[:60],
                        'buClr': buClr,
                        'buChar': buChar,
                        'is_title': is_title,
                    })
    except Exception as e:
        print(f"ERROR reading slide {slide_num}: {e}")
    return results


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

    # Gather bullet info for all slides
    all_slides = {}
    for si in range(1, 7):
        all_slides[si] = get_bullet_info_for_slide(zf, si)

    # Component 1: Bullet color CC0000 on slides 2-3 (0.30 points)
    # Only check non-title paragraphs (bullet items)
    try:
        slides_23_bullets = []
        for si in [2, 3]:
            for info in all_slides[si]:
                if not info['is_title']:
                    slides_23_bullets.append(info)

        if len(slides_23_bullets) == 0:
            print("FAIL: Component 1 - No bullet items found on slides 2-3")
        else:
            cc_count = sum(1 for b in slides_23_bullets if b['buClr'] == 'CC0000')
            total_bullets = len(slides_23_bullets)
            if cc_count == total_bullets:
                print(f"PASS: Component 1 - All {total_bullets} bullets on slides 2-3 have color CC0000 (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 1 - {cc_count}/{total_bullets} bullets on slides 2-3 have CC0000")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Bullet color CC0000 on slides 4-5 (0.30 points)
    try:
        slides_45_bullets = []
        for si in [4, 5]:
            for info in all_slides[si]:
                if not info['is_title']:
                    slides_45_bullets.append(info)

        if len(slides_45_bullets) == 0:
            print("FAIL: Component 2 - No bullet items found on slides 4-5")
        else:
            cc_count = sum(1 for b in slides_45_bullets if b['buClr'] == 'CC0000')
            total_bullets = len(slides_45_bullets)
            if cc_count == total_bullets:
                print(f"PASS: Component 2 - All {total_bullets} bullets on slides 4-5 have color CC0000 (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 2 - {cc_count}/{total_bullets} bullets on slides 4-5 have CC0000")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Bullet color CC0000 on slide 6 (0.15 points)
    try:
        slide_6_bullets = [info for info in all_slides[6] if not info['is_title']]

        if len(slide_6_bullets) == 0:
            print("FAIL: Component 3 - No bullet items found on slide 6")
        else:
            cc_count = sum(1 for b in slide_6_bullets if b['buClr'] == 'CC0000')
            total_bullets = len(slide_6_bullets)
            if cc_count == total_bullets:
                print(f"PASS: Component 3 - All {total_bullets} bullets on slide 6 have color CC0000 (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 - {cc_count}/{total_bullets} bullets on slide 6 have CC0000")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Bullets have CC0000 color AND default round shape preserved (0.15 points)
    # Anchored to the task change: only passes if red bullets exist AND no custom buChar is set
    try:
        red_bullet_count = 0
        custom_char_found = []
        for si in range(2, 7):
            for info in all_slides[si]:
                if not info['is_title']:
                    if info['buClr'] == 'CC0000':
                        red_bullet_count += 1
                    if info['buChar'] is not None:
                        custom_char_found.append(f"slide{si}: char='{info['buChar']}' text={info['text'][:30]}")

        if red_bullet_count > 0 and len(custom_char_found) == 0:
            print(f"PASS: Component 4 - {red_bullet_count} red bullets found with default round shape preserved (0.15 pts)")
            total_score += 0.15
        elif red_bullet_count == 0:
            print(f"FAIL: Component 4 - No red bullets found; cannot verify bullet shape preservation")
        else:
            print(f"FAIL: Component 4 - Custom bullet characters found: {custom_char_found[:3]}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Slide 1 title paragraphs have no bullet color set (0.10 points)
    # This ensures the title slide was not modified
    try:
        slide1_has_buclr = False
        for info in all_slides[1]:
            if info['buClr'] is not None:
                slide1_has_buclr = True
                break

        # Also check: at least one bullet on slides 2-6 HAS buClr CC0000
        # This ensures we are verifying a real change happened
        any_red_bullet = False
        for si in range(2, 7):
            for info in all_slides[si]:
                if not info['is_title'] and info['buClr'] == 'CC0000':
                    any_red_bullet = True
                    break
            if any_red_bullet:
                break

        if not slide1_has_buclr and any_red_bullet:
            print(f"PASS: Component 5 - Slide 1 has no bullet color AND red bullets exist on content slides (0.10 pts)")
            total_score += 0.10
        elif slide1_has_buclr:
            print(f"FAIL: Component 5 - Slide 1 unexpectedly has bullet color set")
        else:
            print(f"FAIL: Component 5 - No red bullets found on any content slide")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

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

"""
Reward Script: Increase bullet size on slide 4 to 150% of text size
Task ID: impstruct_036
Domain: libreoffice_impress
Scoring:
  Component 1 (0.6): Bullet paragraphs on slide 4 have buSzPct=150000 (150%)
  Component 2 (0.4): No other slides have buSzPct set (only slide 4 affected)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impstruct_036'

NS = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}


def get_buSzPct_values(pptx_path, slide_num):
    """Extract buSzPct values from bullet paragraphs on a given slide.
    Returns list of (para_text, buSzPct_value_or_None) for paragraphs with text.
    """
    results = []
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        with zf.open(f'ppt/slides/slide{slide_num}.xml') as f:
            root = ET.parse(f).getroot()
            for p_elem in root.findall('.//a:p', NS):
                text = ''.join(t.text or '' for t in p_elem.findall('.//a:t', NS)).strip()
                if not text:
                    continue
                pPr = p_elem.find('a:pPr', NS)
                buSzPct = None
                if pPr is not None:
                    bsp = pPr.find('a:buSzPct', NS)
                    if bsp is not None:
                        buSzPct = bsp.get('val')
                results.append((text[:60], buSzPct))
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

    # Verify it's a valid pptx
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            zf.open('ppt/slides/slide4.xml')
    except Exception as e:
        print(f"CRITICAL: Cannot open pptx or slide4 missing: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Bullet paragraphs on slide 4 have buSzPct=150000 (0.6 points)
    # The title paragraph ("Key Points") should NOT have buSzPct.
    # The 4 bullet paragraphs should each have buSzPct=150000.
    try:
        slide4_paras = get_buSzPct_values(file_path, 4)
        print(f"Slide 4 paragraphs found: {len(slide4_paras)}")

        # Identify bullet paragraphs (skip the title "Key Points")
        bullet_paras = []
        for text, val in slide4_paras:
            if text.lower().startswith('key points'):
                continue  # title paragraph, skip
            bullet_paras.append((text, val))

        if len(bullet_paras) == 0:
            print("FAIL: Component 1 -- No bullet paragraphs found on slide 4")
        else:
            correct_count = 0
            for text, val in bullet_paras:
                if val == '150000':
                    correct_count += 1
                    print(f"  PASS: '{text[:40]}...' buSzPct={val}")
                else:
                    print(f"  FAIL: '{text[:40]}...' buSzPct={val} (expected 150000)")

            # Award proportional credit: 0.6 * (correct / total)
            ratio = correct_count / len(bullet_paras)
            component1_score = 0.6 * ratio
            if ratio == 1.0:
                print(f"PASS: Component 1 -- All {correct_count}/{len(bullet_paras)} bullet paragraphs have buSzPct=150000 ({component1_score} pts)")
                total_score += component1_score
            elif correct_count > 0:
                print(f"PARTIAL: Component 1 -- {correct_count}/{len(bullet_paras)} bullet paragraphs correct ({component1_score} pts)")
                total_score += component1_score
            else:
                print(f"FAIL: Component 1 -- 0/{len(bullet_paras)} bullet paragraphs have buSzPct=150000")

    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: No other slides have buSzPct set (0.4 points)
    # Only slide 4 should be affected per the task instruction.
    try:
        contaminated_slides = []
        for slide_num in [1, 2, 3, 5]:
            try:
                other_paras = get_buSzPct_values(file_path, slide_num)
                for text, val in other_paras:
                    if val is not None:
                        print(f"  FAIL: Slide {slide_num} paragraph '{text[:40]}' has buSzPct={val}")
                        contaminated_slides.append(slide_num)
            except KeyError:
                # Slide doesn't exist, that's fine
                pass

        if len(contaminated_slides) == 0:
            # But only award points if Component 1 also found changes on slide 4
            # (to avoid awarding points when nothing changed at all)
            slide4_has_any_buSzPct = any(
                val is not None for _, val in get_buSzPct_values(file_path, 4)
                if not _.lower().startswith('key points')
            )
            if slide4_has_any_buSzPct:
                print(f"PASS: Component 2 -- No other slides have buSzPct (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 -- Slide 4 has no buSzPct changes either, so no isolation credit")
        elif len(contaminated_slides) > 0:
            print(f"FAIL: Component 2 -- Other slides have unexpected buSzPct values")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

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

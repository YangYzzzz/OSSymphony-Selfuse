"""
Reward Script: Remove bullet symbols and create staircase indentation on slide 5
Task ID: osworld_impress_bullet_indent_remove_009
Domain: libreoffice_impress
Scoring:
  Component 1: Bullet symbols removed from all 4 items (0.4 pts)
  Component 2: Staircase indentation applied (+1cm per item starting from 0) (0.6 pts)
  Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_impress_bullet_indent_remove_009'

# 1 cm = 360000 EMU
CM_IN_EMU = 360000

NS = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.

    Task: On slide 5, remove bullet symbols and create a staircase indentation
          where each item is indented 1cm more than the previous.

    Initial state: 4 paragraphs with bullet character '•' and uniform marL=457200
    Golden state: 4 paragraphs with buNone (no bullets), marL increasing by 360000 per item
                  Item 1: marL=0, Item 2: marL=360000, Item 3: marL=720000, Item 4: marL=1080000

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the presentation file via ZIP/XML for precise bullet/indent verification
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            with zf.open('ppt/slides/slide5.xml') as f:
                root = ET.parse(f).getroot()
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect paragraphs with non-empty text from slide 5 content placeholder
    # (excluding title paragraph "Creative Highlights")
    content_paras = []
    try:
        for p_elem in root.findall('.//a:p', NS):
            pPr = p_elem.find('a:pPr', NS)
            texts = [t.text or '' for t in p_elem.findall('.//a:t', NS)]
            text = ''.join(texts).strip()
            # Skip empty paragraphs and title paragraph
            if text and text != 'Creative Highlights':
                content_paras.append((p_elem, pPr, text))
    except Exception as e:
        print(f"ERROR: Could not parse paragraphs: {e}")
        print("REWARD: 0.0")
        return 0.0

    if len(content_paras) < 4:
        print(f"FAIL: Expected 4 content paragraphs on slide 5, found {len(content_paras)}")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found {len(content_paras)} content paragraphs on slide 5")

    # Component 1: Bullet symbols removed from all 4 items (0.4 points)
    # In initial state: buChar with '•' is present. After task: buNone should be present.
    try:
        bullets_removed_count = 0
        bullets_still_present = []

        for idx, (p_elem, pPr, text) in enumerate(content_paras[:4]):
            buNone = pPr.find('a:buNone', NS) if pPr is not None else None
            buChar = pPr.find('a:buChar', NS) if pPr is not None else None

            if buNone is not None:
                bullets_removed_count += 1
                print(f"  Para {idx}: buNone present (bullet removed) for text: {repr(text[:30])}")
            elif buChar is not None:
                char = buChar.get('char', '')
                bullets_still_present.append((idx, char, text[:30]))
                print(f"  Para {idx}: buChar='{char}' still present for text: {repr(text[:30])}")
            else:
                # No explicit bullet setting — check if inherited; still counts as not removed
                bullets_still_present.append((idx, None, text[:30]))
                print(f"  Para {idx}: No explicit bullet setting for text: {repr(text[:30])}")

        if bullets_removed_count == 4:
            print(f"PASS: Component 1 — All 4 bullet symbols removed (buNone present on all items) (0.4 pts)")
            total_score += 0.4
        elif bullets_removed_count > 0:
            partial = round(0.4 * bullets_removed_count / 4, 4)
            print(f"PARTIAL: Component 1 — {bullets_removed_count}/4 bullets removed, partial score {partial}")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No bullets removed. Still present: {bullets_still_present}")

    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Staircase indentation (0.6 points)
    # Expected marL values: 0, 360000, 720000, 1080000 (each +1cm = +360000 EMU)
    # Tolerance: 5% of 360000 = 18000 EMU (about 0.5mm)
    TOLERANCE = 18000
    expected_marL = [0, CM_IN_EMU, 2 * CM_IN_EMU, 3 * CM_IN_EMU]
    expected_str = ', '.join(str(v) for v in expected_marL)

    try:
        staircase_ok_count = 0
        marL_values = []

        for idx, (p_elem, pPr, text) in enumerate(content_paras[:4]):
            marL_str = pPr.get('marL') if pPr is not None else None
            try:
                marL_val = int(marL_str) if marL_str is not None else None
            except (ValueError, TypeError):
                marL_val = None
            marL_values.append(marL_val)

            exp = expected_marL[idx]
            if marL_val is not None and abs(marL_val - exp) <= TOLERANCE:
                staircase_ok_count += 1
                print(f"  Para {idx}: marL={marL_val} (expected ~{exp}) OK")
            else:
                print(f"  Para {idx}: marL={marL_val} (expected ~{exp}) FAIL")

        # Also verify staircase property: each step increases by ~1cm
        steps_ok = 0
        if len(marL_values) == 4 and all(v is not None for v in marL_values):
            for i in range(1, 4):
                step = marL_values[i] - marL_values[i - 1]
                if abs(step - CM_IN_EMU) <= TOLERANCE:
                    steps_ok += 1

        if staircase_ok_count == 4:
            print(f"PASS: Component 2 — Staircase indentation applied correctly. "
                  f"marL values: {marL_values} (expected: {expected_str}) (0.6 pts)")
            total_score += 0.6
        elif steps_ok == 3 and staircase_ok_count >= 2:
            # Staircase shape is correct but starting offset is wrong — partial credit
            print(f"PARTIAL: Component 2 — Staircase pattern correct but wrong start. "
                  f"marL values: {marL_values}, steps_ok={steps_ok}. Awarding 0.3 pts")
            total_score += 0.3
        elif staircase_ok_count > 0 or steps_ok > 0:
            partial = round(0.6 * (staircase_ok_count + steps_ok) / 7, 4)
            print(f"PARTIAL: Component 2 — Partial staircase. "
                  f"staircase_ok={staircase_ok_count}, steps_ok={steps_ok}. Partial score {partial}")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Staircase indentation not applied. "
                  f"Actual marL: {marL_values}, expected: {expected_str}")

    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(round(total_score, 4), 1.0)
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

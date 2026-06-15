"""
Reward Script: Three-level numbered list on slide 2
Task ID: impstruct_035
Domain: libreoffice_impress
Scoring:
  Component 1 (0.4): Paragraph levels follow 0,1,2 repeating pattern
  Component 2 (0.2): Level-0 paragraphs use arabicPeriod numbering
  Component 3 (0.2): Level-1 paragraphs use alphaLcPeriod numbering
  Component 4 (0.2): Level-2 paragraphs use romanLcPeriod numbering
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impstruct_035'

# Expected level pattern for the 9 content paragraphs on slide 2
EXPECTED_LEVELS = ['0', '1', '2', '0', '1', '2', '0', '1', '2']

# Expected numbering type per level
EXPECTED_NUM_TYPE = {
    '0': 'arabicPeriod',
    '1': 'alphaLcPeriod',
    '2': 'romanLcPeriod',
}

NS = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
}


def persist_app_state(domain):
    """Attempt to save any unsaved LibreOffice state."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print(f"PERSIST: ctrl+s sent for {domain}")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def get_slide2_content_paragraphs(pptx_path):
    """
    Parse slide2.xml and return a list of (level, buAutoNum_type, text)
    for content paragraphs (non-empty text, excluding the title).
    """
    paragraphs = []
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        with zf.open('ppt/slides/slide2.xml') as f:
            root = ET.parse(f).getroot()
            # Find all shape trees
            sp_tree = root.find('.//p:cSld/p:spTree', NS)
            if sp_tree is None:
                return paragraphs

            shapes = sp_tree.findall('p:sp', NS)
            for shape in shapes:
                # Identify the content placeholder (not the title)
                nvSpPr = shape.find('p:nvSpPr', NS)
                if nvSpPr is not None:
                    nvPr = nvSpPr.find('p:nvPr', NS)
                    if nvPr is not None:
                        ph = nvPr.find('p:ph', NS)
                        if ph is not None:
                            ph_type = ph.get('type', '')
                            # Skip title placeholders
                            if ph_type in ('title', 'ctrTitle'):
                                continue

                txBody = shape.find('p:txBody', NS)
                if txBody is None:
                    continue

                for para in txBody.findall('a:p', NS):
                    text = ''.join(
                        t.text or '' for t in para.findall('.//a:t', NS)
                    )
                    if not text.strip():
                        continue

                    pPr = para.find('a:pPr', NS)
                    lvl = pPr.get('lvl', '0') if pPr is not None else '0'
                    buAutoNum = (
                        pPr.find('a:buAutoNum', NS) if pPr is not None else None
                    )
                    num_type = (
                        buAutoNum.get('type', '') if buAutoNum is not None else None
                    )
                    paragraphs.append((lvl, num_type, text))

    return paragraphs


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

    # Parse slide 2 content paragraphs
    try:
        paragraphs = get_slide2_content_paragraphs(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if len(paragraphs) < 9:
        print(f"FAIL: Expected 9 content paragraphs on slide 2, found {len(paragraphs)}")
        print("REWARD: 0.0")
        return 0.0

    # Use the first 9 content paragraphs (skip title which was already filtered)
    content_paras = paragraphs[:9]
    actual_levels = [p[0] for p in content_paras]

    # Component 1: Level hierarchy (0.4 points)
    # Paragraphs must follow the 0,1,2,0,1,2,0,1,2 pattern
    try:
        level_matches = sum(
            1 for a, e in zip(actual_levels, EXPECTED_LEVELS) if a == e
        )
        if level_matches == 9:
            print(f"PASS: Component 1 — All 9 paragraphs have correct levels (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — {level_matches}/9 paragraphs have correct levels. "
                  f"Actual: {actual_levels}, Expected: {EXPECTED_LEVELS}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Level-0 uses arabicPeriod (0.2 points)
    # Check paragraphs at indices 0, 3, 6 (level-0 items)
    try:
        level0_indices = [0, 3, 6]
        level0_correct = 0
        for idx in level0_indices:
            lvl, num_type, text = content_paras[idx]
            if num_type == 'arabicPeriod':
                level0_correct += 1
            else:
                print(f"  INFO: Para {idx} ('{text[:40]}...') num_type={num_type}, expected arabicPeriod")

        if level0_correct == 3:
            print(f"PASS: Component 2 — All 3 level-0 paragraphs use arabicPeriod (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — {level0_correct}/3 level-0 paragraphs use arabicPeriod")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Level-1 uses alphaLcPeriod (0.2 points)
    # Check paragraphs at indices 1, 4, 7 (level-1 items)
    try:
        level1_indices = [1, 4, 7]
        level1_correct = 0
        for idx in level1_indices:
            lvl, num_type, text = content_paras[idx]
            if num_type == 'alphaLcPeriod':
                level1_correct += 1
            else:
                print(f"  INFO: Para {idx} ('{text[:40]}...') num_type={num_type}, expected alphaLcPeriod")

        if level1_correct == 3:
            print(f"PASS: Component 3 — All 3 level-1 paragraphs use alphaLcPeriod (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — {level1_correct}/3 level-1 paragraphs use alphaLcPeriod")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Level-2 uses romanLcPeriod (0.2 points)
    # Check paragraphs at indices 2, 5, 8 (level-2 items)
    try:
        level2_indices = [2, 5, 8]
        level2_correct = 0
        for idx in level2_indices:
            lvl, num_type, text = content_paras[idx]
            if num_type == 'romanLcPeriod':
                level2_correct += 1
            else:
                print(f"  INFO: Para {idx} ('{text[:40]}...') num_type={num_type}, expected romanLcPeriod")

        if level2_correct == 3:
            print(f"PASS: Component 4 — All 3 level-2 paragraphs use romanLcPeriod (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — {level2_correct}/3 level-2 paragraphs use romanLcPeriod")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist any unsaved GUI state before verification
persist_app_state('libreoffice_impress')

# Run verification
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

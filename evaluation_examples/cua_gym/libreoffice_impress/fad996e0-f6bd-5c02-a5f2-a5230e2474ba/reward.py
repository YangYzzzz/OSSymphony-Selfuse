"""
Reward Script: Convert bullet points to numbered list on slide 3
Task ID: impress_stu_081
Domain: libreoffice_impress
Scoring:
  Precondition gate: Text content of the 6 paragraphs is preserved (no points, early exit if corrupted)
  Component 1 (0.6): All 6 content paragraphs have buAutoNum numbering
  Component 2 (0.4): Numbering type is arabicPeriod (1. 2. 3.) format
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_stu_081'

# Expected text content for the 6 scientific method steps on slide 3
EXPECTED_TEXTS = [
    'Make an observation about a natural phenomenon',
    'Formulate a testable hypothesis',
    'Design and conduct an experiment',
    'Collect and analyze the data',
    'Draw conclusions from the results',
    'Communicate findings and repeat if necessary',
]

def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
          'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}

    # Load the pptx as ZIP to inspect XML for bullet/number formatting
    try:
        zf = zipfile.ZipFile(file_path, 'r')
        with zf.open('ppt/slides/slide3.xml') as f:
            root = ET.parse(f).getroot()
        zf.close()
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract content paragraphs from slide 3 (skip title paragraph)
    # We identify content paragraphs as those whose text matches our expected steps
    content_paras = []
    for para in root.findall('.//a:p', ns):
        text = ''.join(t.text or '' for t in para.findall('.//a:t', ns)).strip()
        if text and text != 'Steps of the Scientific Method':
            content_paras.append((para, text))

    if len(content_paras) < 6:
        print(f"FAIL: Expected 6 content paragraphs on slide 3, found {len(content_paras)}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: Text content must be preserved (no points awarded)
    # The task says "Keep the same text content" - if text is corrupted, return 0.0
    try:
        actual_texts = [text for _, text in content_paras[:6]]
        text_matching = 0
        for i, expected in enumerate(EXPECTED_TEXTS):
            if i < len(actual_texts) and actual_texts[i].strip() == expected.strip():
                text_matching += 1
        if text_matching < 6:
            print(f"GATE FAIL: Text content was modified ({text_matching}/6 match). No credit awarded.")
            print("REWARD: 0.0")
            return 0.0
        else:
            print(f"GATE PASS: All 6 step texts preserved unchanged")
    except Exception as e:
        print(f"GATE ERROR: Could not verify text content: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: All 6 content paragraphs have buAutoNum numbering (0.6 points)
    # This is the key task-introduced change: bullets -> numbers
    try:
        numbered_count = 0
        for para, text in content_paras[:6]:
            pPr = para.find('a:pPr', ns)
            if pPr is not None:
                buAutoNum = pPr.find('a:buAutoNum', ns)
                if buAutoNum is not None:
                    numbered_count += 1

        if numbered_count == 6:
            print(f"PASS: Component 1 — All 6 paragraphs have buAutoNum numbering (0.6 pts)")
            total_score += 0.6
        elif numbered_count > 0:
            # Partial credit: proportional to how many paragraphs are numbered
            partial = round(0.6 * (numbered_count / 6), 2)
            print(f"PARTIAL: Component 1 — {numbered_count}/6 paragraphs have numbering ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No paragraphs have buAutoNum numbering (0/6)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Numbering type is arabicPeriod format (0.4 points)
    # The task says "1. through 6." which corresponds to arabicPeriod
    try:
        arabic_period_count = 0
        for para, text in content_paras[:6]:
            pPr = para.find('a:pPr', ns)
            if pPr is not None:
                buAutoNum = pPr.find('a:buAutoNum', ns)
                if buAutoNum is not None:
                    num_type = buAutoNum.get('type', '')
                    # Accept arabicPeriod or arabicParenR as valid "1." style numbering
                    if num_type in ('arabicPeriod', 'arabicParenR', 'arabicParenBoth'):
                        arabic_period_count += 1

        if arabic_period_count == 6:
            print(f"PASS: Component 2 — All 6 paragraphs use arabic numbering style (0.4 pts)")
            total_score += 0.4
        elif arabic_period_count > 0:
            partial = round(0.4 * (arabic_period_count / 6), 2)
            print(f"PARTIAL: Component 2 — {arabic_period_count}/6 paragraphs use arabic style ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No paragraphs use arabic numbering style")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
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

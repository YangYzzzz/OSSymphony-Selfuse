"""
Reward Script: Convert bulleted items to plain paragraphs and add horizontal rule separators
Task ID: wrpara_039
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): All 8 items converted from List Bullet to plain paragraph style
  Component 2 (0.3): Exactly 7 horizontal rule separators present (empty paras with bottom border)
  Component 3 (0.2): Separators correctly positioned between each pair of content paragraphs
  Component 4 (0.1): Original text content preserved across all 8 items
"""

import os
from docx import Document
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'wrpara_039'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

# The 8 original bullet item text prefixes (first 40 chars) for content verification
EXPECTED_STARTS = [
    "Cloud migration projects require",
    "Cross-functional teams consistently",
    "Data governance policies must be",
    "Remote onboarding effectiveness",
    "API versioning should follow",
    "Sustainability reporting is shifting",
    "Automated regression testing catches",
    "Customer feedback loops should be",
]


def has_bottom_border(para):
    """Check if a paragraph has a bottom border (horizontal rule indicator)."""
    pBdr = para._element.find('.//w:pBdr', NS)
    if pBdr is None:
        return False
    bottom = pBdr.find('w:bottom', NS)
    return bottom is not None


def is_bullet_style(para):
    """Check if a paragraph uses a bullet list style."""
    style_name = para.style.name if para.style else ''
    # Check style name for bullet indicators
    if 'bullet' in style_name.lower() or 'list bullet' in style_name.lower():
        return True
    # Also check for numPr XML element (numbering properties)
    numPr = para._element.find('.//w:numPr', NS)
    if numPr is not None:
        numId_el = numPr.find('w:numId', NS)
        if numId_el is not None:
            val = numId_el.get(f'{{{NS["w"]}}}val')
            # numId=0 means no numbering
            if val is not None and val != '0':
                return True
    return False


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paras = doc.paragraphs

    # Precondition: heading still present
    if len(paras) < 2:
        print("FAIL: Document has fewer than 2 paragraphs")
        print("REWARD: 0.0")
        return 0.0

    # Separate content paragraphs from separator paragraphs (skip heading at index 0)
    content_paras = []
    separator_paras = []
    for p in paras[1:]:  # skip heading
        if p.text.strip() == '' and has_bottom_border(p):
            separator_paras.append(p)
        elif p.text.strip():
            content_paras.append(p)
        # empty paras without borders are ignored

    print(f"INFO: Found {len(content_paras)} content paragraphs, {len(separator_paras)} separator paragraphs")

    # Component 1: All 8 items are plain paragraphs (bullets removed) (0.4 points)
    # This checks that NONE of the content paragraphs use bullet styling.
    # In initial_env, all 8 are "List Bullet" -> this component FAILS on initial.
    # In golden_env, all 8 are "Normal" -> this component PASSES on golden.
    try:
        if len(content_paras) >= 8:
            bullet_count = sum(1 for p in content_paras[:8] if is_bullet_style(p))
            non_bullet_count = 8 - bullet_count
            if bullet_count == 0:
                print(f"PASS: Component 1 -- All 8 items are plain paragraphs (no bullets) (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 1 -- {bullet_count}/8 items still have bullet formatting")
        else:
            print(f"FAIL: Component 1 -- Expected 8 content paragraphs, found {len(content_paras)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Exactly 7 horizontal rule separators present (0.3 points)
    # In initial_env, there are 0 separators -> FAILS.
    # In golden_env, there are 7 separators -> PASSES.
    try:
        sep_count = len(separator_paras)
        if sep_count == 7:
            print(f"PASS: Component 2 -- Exactly 7 horizontal rule separators found (0.3 pts)")
            total_score += 0.3
        elif sep_count > 0:
            # Partial credit: proportional to how many separators are present
            partial = 0.3 * (min(sep_count, 7) / 7.0)
            if sep_count <= 7:
                print(f"PARTIAL: Component 2 -- Found {sep_count}/7 separators ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 -- Found {sep_count} separators, expected exactly 7")
        else:
            print(f"FAIL: Component 2 -- No horizontal rule separators found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Separators correctly positioned between content paragraphs (0.2 points)
    # Check that the ordering is: content, separator, content, separator, ..., content
    # In initial_env, no separators exist -> FAILS.
    # In golden_env, they alternate correctly -> PASSES.
    try:
        # Rebuild the sequence from paras[1:] (skip heading)
        sequence = []
        for p in paras[1:]:
            if p.text.strip() == '' and has_bottom_border(p):
                sequence.append('SEP')
            elif p.text.strip():
                sequence.append('CONTENT')
            # skip other empty paras

        # Expected pattern: CONTENT, SEP, CONTENT, SEP, ..., CONTENT (8 content + 7 sep = 15 items)
        expected = []
        for i in range(8):
            expected.append('CONTENT')
            if i < 7:
                expected.append('SEP')

        if sequence == expected:
            print(f"PASS: Component 3 -- Separators correctly positioned between content paragraphs (0.2 pts)")
            total_score += 0.2
        elif 'SEP' not in sequence:
            # No separators at all -- no partial credit (avoids initial_env scoring)
            print(f"FAIL: Component 3 -- No separators in sequence, cannot evaluate positioning")
        else:
            # Some separators exist but ordering is wrong -- partial credit
            matches = sum(1 for a, b in zip(sequence, expected) if a == b)
            ratio = matches / len(expected)
            partial = round(0.2 * ratio, 4)
            if partial > 0:
                total_score += partial
                print(f"PARTIAL: Component 3 -- Sequence match {matches}/{len(expected)} ({partial:.2f} pts)")
                print(f"  Actual:   {sequence}")
                print(f"  Expected: {expected}")
            else:
                print(f"FAIL: Component 3 -- No positions match expected sequence")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Original text content preserved (0.1 points)
    # Both initial and golden should have the same text, but we only award this
    # if bullets were actually removed (Component 1 check prevents initial from scoring).
    # We tie this to Component 1: only award if NO bullets remain AND text matches.
    try:
        if len(content_paras) >= 8:
            preserved_count = 0
            bullet_remains = any(is_bullet_style(p) for p in content_paras[:8])
            if bullet_remains:
                print(f"FAIL: Component 4 -- Cannot verify text preservation while bullets remain")
            else:
                for i, prefix in enumerate(EXPECTED_STARTS):
                    if content_paras[i].text.startswith(prefix):
                        preserved_count += 1
                    else:
                        print(f"  MISMATCH para {i}: expected start '{prefix}', got '{content_paras[i].text[:40]}'")
                if preserved_count == 8:
                    print(f"PASS: Component 4 -- All 8 items text content preserved (0.1 pts)")
                    total_score += 0.1
                else:
                    print(f"FAIL: Component 4 -- Only {preserved_count}/8 items have preserved text")
        else:
            print(f"FAIL: Component 4 -- Not enough content paragraphs to verify text")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook for LibreOffice Writer
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'

persist_app_state()

if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

"""
Reward Script: Remove all list formatting from the entire document
Task ID: writer_lec_032
Domain: libreoffice_writer
Scoring:
  Component 1: No List Bullet styles remain (0.35)
  Component 2: No List Number styles remain (0.35)
  Component 3: No numPr XML elements in any paragraph (0.15)
  Component 4: All text content preserved (0.15)
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_032'

# Known paragraph texts from initial document (used for text preservation check)
EXPECTED_PARA_COUNT = 50

# Indices of paragraphs that were List Bullet in initial (14 total)
LIST_BULLET_INDICES = [5, 6, 7, 8, 9, 25, 26, 27, 28, 41, 42, 43, 44, 45]

# Indices of paragraphs that were List Number in initial (11 total)
LIST_NUMBER_INDICES = [14, 15, 16, 17, 18, 19, 32, 33, 34, 35, 36]


def persist_app_state(domain):
    """Save any unsaved edits in LibreOffice before verification."""
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.0)
        print("PERSIST: ctrl+s sent for LibreOffice Writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify that all list formatting has been removed from the document.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
    except ImportError:
        print("CRITICAL: python-docx not available")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paragraphs = doc.paragraphs

    # Component 1: No List Bullet styles remain (0.35 points)
    # In the initial doc, paragraphs at LIST_BULLET_INDICES had style "List Bullet".
    # After task completion, NONE should have any List-related style.
    try:
        list_bullet_found = []
        for para in paragraphs:
            style_name = para.style.name if para.style else ''
            if 'List Bullet' in style_name:
                list_bullet_found.append(style_name)

        if len(list_bullet_found) == 0:
            print(f"PASS: Component 1 - No List Bullet styles found (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 - Found {len(list_bullet_found)} paragraphs with List Bullet style")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: No List Number styles remain (0.35 points)
    # In the initial doc, paragraphs at LIST_NUMBER_INDICES had style "List Number".
    # After task completion, NONE should have any List Number style.
    try:
        list_number_found = []
        for para in paragraphs:
            style_name = para.style.name if para.style else ''
            if 'List Number' in style_name:
                list_number_found.append(style_name)

        if len(list_number_found) == 0:
            print(f"PASS: Component 2 - No List Number styles found (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 - Found {len(list_number_found)} paragraphs with List Number style")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: No numPr XML elements in any paragraph (0.15 points)
    # numPr is the XML element that defines list numbering. It must be completely absent.
    try:
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        numPr_count = 0
        for para in paragraphs:
            pPr = para._element.find('.//w:pPr', ns)
            if pPr is not None:
                numPr = pPr.find('w:numPr', ns)
                if numPr is not None:
                    numPr_count += 1

        if numPr_count == 0:
            print(f"PASS: Component 3 - No numPr XML elements found (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 - Found {numPr_count} paragraphs with numPr XML elements")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: List formatting removed AND text content preserved (0.15 points)
    # This is a compound check: lists must be removed (no List styles) AND all text preserved.
    # The text preservation alone is a precondition; combined with list removal it confirms
    # the task was done without destroying content.
    try:
        para_count = len(paragraphs)
        count_ok = para_count == EXPECTED_PARA_COUNT

        # Check key texts from known list paragraphs are still present
        all_text = '\n'.join(p.text for p in paragraphs)
        key_phrases = [
            "Enterprise software licensing grew 18%",
            "Cloud services subscription revenue increased",
            "Launched the Aurora 3.0 platform",
            "Achieved SOC 2 Type II certification",
            "Expand the Aurora platform's AI capabilities",
            "Increased competition in the enterprise analytics",
            "Launched a mentorship program pairing 120",
            "Rolled out an enhanced parental leave policy",
        ]
        phrases_found = sum(1 for phrase in key_phrases if phrase in all_text)
        text_ok = count_ok and phrases_found == len(key_phrases)

        # Must also have no list styles (anchoring this to the task change)
        any_list_styles = any(
            'List' in (p.style.name if p.style else '')
            for p in paragraphs
        )
        lists_removed = not any_list_styles

        if lists_removed and text_ok:
            print(f"PASS: Component 4 - Lists removed AND text preserved: {para_count} paragraphs, {phrases_found}/{len(key_phrases)} key phrases (0.15 pts)")
            total_score += 0.15
        elif not lists_removed:
            print(f"FAIL: Component 4 - List styles still present, cannot award text preservation points")
        else:
            print(f"FAIL: Component 4 - Text not fully preserved: para count={para_count} (expected {EXPECTED_PARA_COUNT}), key phrases={phrases_found}/{len(key_phrases)}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'

# Persist any unsaved GUI state
persist_app_state('libreoffice_writer')

if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

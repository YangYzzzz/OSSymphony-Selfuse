"""
Reward Script: Reorganize document by moving Conclusion section after Introduction
Task ID: wrpara_034
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35): Section headings appear in correct new order
  Component 2 (0.35): Conclusion section content is in the correct position (paragraphs 3-5)
  Component 3 (0.30): All original content is preserved (no paragraphs lost or duplicated)
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'wrpara_034'

# Expected section order after the move
EXPECTED_HEADING_ORDER = ['Introduction', 'Conclusion', 'Background', 'Analysis', 'Counter-arguments']


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

    paragraphs = doc.paragraphs

    # Extract heading paragraphs in order
    headings = []
    for i, para in enumerate(paragraphs):
        if para.style and para.style.name.startswith('Heading'):
            headings.append((i, para.text.strip()))

    heading_names = [h[1] for h in headings]
    print(f"Found headings: {heading_names}")

    # Component 1: Section headings appear in the correct new order (0.35 points)
    # In the initial doc, order is [Intro, Background, Analysis, Counter-arguments, Conclusion]
    # In the golden doc, order is [Intro, Conclusion, Background, Analysis, Counter-arguments]
    try:
        if heading_names == EXPECTED_HEADING_ORDER:
            print(f"PASS: Component 1 -- Headings in correct order: {heading_names} (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 -- Expected headings {EXPECTED_HEADING_ORDER}, found {heading_names}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Conclusion section content is at the right position (0.35 points)
    # After Introduction (heading idx 0 + 2 body paras), Conclusion heading should be at para index 3,
    # followed by its 2 body paragraphs at indices 4 and 5.
    try:
        # Check paragraph at index 3 is the Conclusion heading
        if len(paragraphs) > 5:
            para3 = paragraphs[3]
            para3_is_conclusion_heading = (
                para3.style and para3.style.name.startswith('Heading')
                and para3.text.strip() == 'Conclusion'
            )
            # Check paragraphs 4 and 5 are Normal style (Conclusion body)
            para4_is_normal = paragraphs[4].style and paragraphs[4].style.name == 'Normal'
            para5_is_normal = paragraphs[5].style and paragraphs[5].style.name == 'Normal'
            # Check paragraph 4 starts with expected Conclusion content
            para4_starts_correct = paragraphs[4].text.startswith('The evidence presented')
            para5_starts_correct = paragraphs[5].text.startswith('Looking ahead')

            if para3_is_conclusion_heading and para4_is_normal and para5_is_normal:
                if para4_starts_correct and para5_starts_correct:
                    print(f"PASS: Component 2 -- Conclusion content at correct position (paras 3-5) (0.35 pts)")
                    total_score += 0.35
                else:
                    print(f"FAIL: Component 2 -- Conclusion body text doesn't match expected content")
                    print(f"  Para 4 starts with: {paragraphs[4].text[:50]!r}")
                    print(f"  Para 5 starts with: {paragraphs[5].text[:50]!r}")
            else:
                print(f"FAIL: Component 2 -- Para 3 is not Conclusion heading or paras 4-5 not Normal")
                print(f"  Para 3 style={para3.style.name!r} text={para3.text[:50]!r}")
        else:
            print(f"FAIL: Component 2 -- Document has fewer than 6 paragraphs ({len(paragraphs)})")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: All original content preserved - total paragraph count and no duplication (0.30 points)
    # The original document has 18 paragraphs (5 headings + 13 body paragraphs).
    # After reorganization, the count should remain the same.
    try:
        expected_para_count = 18
        actual_count = len(paragraphs)

        # Check no duplicate headings
        heading_counts = {}
        for h in heading_names:
            heading_counts[h] = heading_counts.get(h, 0) + 1
        duplicates = {k: v for k, v in heading_counts.items() if v > 1}

        # Also verify Background follows Conclusion (para index 6 should be Background heading)
        background_after_conclusion = False
        if len(paragraphs) > 6:
            background_after_conclusion = (
                paragraphs[6].style and paragraphs[6].style.name.startswith('Heading')
                and paragraphs[6].text.strip() == 'Background'
            )

        if actual_count == expected_para_count and not duplicates and background_after_conclusion:
            print(f"PASS: Component 3 -- Document has {actual_count} paragraphs, no duplicates, Background follows Conclusion (0.30 pts)")
            total_score += 0.30
        else:
            if actual_count != expected_para_count:
                print(f"FAIL: Component 3 -- Expected {expected_para_count} paragraphs, found {actual_count}")
            if duplicates:
                print(f"FAIL: Component 3 -- Duplicate headings found: {duplicates}")
            if not background_after_conclusion:
                print(f"FAIL: Component 3 -- Background does not follow Conclusion at expected position")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
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

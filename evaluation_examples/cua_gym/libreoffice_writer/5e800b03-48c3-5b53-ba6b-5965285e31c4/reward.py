"""
Reward Script: Apply heading styles to create a four-level document hierarchy
Task ID: writer_bs_074
Domain: libreoffice_writer
Scoring:
  - Component 1: Heading 1 on chapter titles (0.30)
  - Component 2: Heading 2 on section titles (0.30)
  - Component 3: Heading 3 on subsections (0.25)
  - Component 4: Heading 4 on sub-subsections (0.15)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_bs_074'

# Expected heading assignments based on task requirements:
# "Chapter X: ..." -> Heading 1
# "N.N ..." (section-level, e.g. 1.1, 2.2) -> Heading 2
# "N.N.N ..." (subsection, e.g. 1.1.1, 2.1.1) -> Heading 3
# "N.N.N.N ..." (sub-subsection, e.g. 1.1.1.1) -> Heading 4


def persist_app_state(domain):
    """Try to save any unsaved changes in LibreOffice."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def classify_paragraph(text):
    """
    Classify a paragraph by its expected heading level based on text pattern.
    Returns the expected style name or None if it's body text.
    """
    text = text.strip()
    if not text:
        return None

    # Chapter titles: "Chapter N: ..."
    if re.match(r'^Chapter\s+\d+:', text):
        return 'Heading 1'

    # Sub-subsection: "N.N.N.N ..." (four-part numbering)
    if re.match(r'^\d+\.\d+\.\d+\.\d+\s', text):
        return 'Heading 4'

    # Subsection: "N.N.N ..." (three-part numbering)
    if re.match(r'^\d+\.\d+\.\d+\s', text):
        return 'Heading 3'

    # Section: "N.N ..." (two-part numbering)
    if re.match(r'^\d+\.\d+\s', text):
        return 'Heading 2'

    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect expected headings and actual styles
    heading1_expected = []  # paragraphs expected to be Heading 1
    heading2_expected = []  # paragraphs expected to be Heading 2
    heading3_expected = []  # paragraphs expected to be Heading 3
    heading4_expected = []  # paragraphs expected to be Heading 4

    for i, para in enumerate(doc.paragraphs):
        expected = classify_paragraph(para.text)
        actual_style = para.style.name if para.style else 'None'
        if expected == 'Heading 1':
            heading1_expected.append((i, para.text[:60], actual_style))
        elif expected == 'Heading 2':
            heading2_expected.append((i, para.text[:60], actual_style))
        elif expected == 'Heading 3':
            heading3_expected.append((i, para.text[:60], actual_style))
        elif expected == 'Heading 4':
            heading4_expected.append((i, para.text[:60], actual_style))

    # Component 1: Heading 1 on chapter titles (0.30 points)
    try:
        if len(heading1_expected) == 0:
            print("FAIL: Component 1 -- No chapter titles found in document")
        else:
            correct = sum(1 for _, _, style in heading1_expected if style == 'Heading 1')
            total_h1 = len(heading1_expected)
            if correct == total_h1:
                print(f"PASS: Component 1 -- All {total_h1} chapter titles have Heading 1 (0.30 pts)")
                total_score += 0.30
            elif correct > 0:
                # Partial: proportional credit
                partial = 0.30 * (correct / total_h1)
                total_score += partial
                print(f"PARTIAL: Component 1 -- {correct}/{total_h1} chapter titles have Heading 1 ({partial:.2f} pts)")
                for idx, text, style in heading1_expected:
                    if style != 'Heading 1':
                        print(f"  MISS: para[{idx}] '{text}' has style '{style}' instead of 'Heading 1'")
            else:
                print(f"FAIL: Component 1 -- 0/{total_h1} chapter titles have Heading 1 (0.00 pts)")
                for idx, text, style in heading1_expected:
                    print(f"  MISS: para[{idx}] '{text}' has style '{style}' instead of 'Heading 1'")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Heading 2 on section titles (0.30 points)
    try:
        if len(heading2_expected) == 0:
            print("FAIL: Component 2 -- No section titles found in document")
        else:
            correct = sum(1 for _, _, style in heading2_expected if style == 'Heading 2')
            total_h2 = len(heading2_expected)
            if correct == total_h2:
                print(f"PASS: Component 2 -- All {total_h2} section titles have Heading 2 (0.30 pts)")
                total_score += 0.30
            elif correct > 0:
                partial = 0.30 * (correct / total_h2)
                total_score += partial
                print(f"PARTIAL: Component 2 -- {correct}/{total_h2} section titles have Heading 2 ({partial:.2f} pts)")
                for idx, text, style in heading2_expected:
                    if style != 'Heading 2':
                        print(f"  MISS: para[{idx}] '{text}' has style '{style}' instead of 'Heading 2'")
            else:
                print(f"FAIL: Component 2 -- 0/{total_h2} section titles have Heading 2 (0.00 pts)")
                for idx, text, style in heading2_expected:
                    print(f"  MISS: para[{idx}] '{text}' has style '{style}' instead of 'Heading 2'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Heading 3 on subsections (0.25 points)
    try:
        if len(heading3_expected) == 0:
            print("FAIL: Component 3 -- No subsections found in document")
        else:
            correct = sum(1 for _, _, style in heading3_expected if style == 'Heading 3')
            total_h3 = len(heading3_expected)
            if correct == total_h3:
                print(f"PASS: Component 3 -- All {total_h3} subsections have Heading 3 (0.25 pts)")
                total_score += 0.25
            elif correct > 0:
                partial = 0.25 * (correct / total_h3)
                total_score += partial
                print(f"PARTIAL: Component 3 -- {correct}/{total_h3} subsections have Heading 3 ({partial:.2f} pts)")
                for idx, text, style in heading3_expected:
                    if style != 'Heading 3':
                        print(f"  MISS: para[{idx}] '{text}' has style '{style}' instead of 'Heading 3'")
            else:
                print(f"FAIL: Component 3 -- 0/{total_h3} subsections have Heading 3 (0.00 pts)")
                for idx, text, style in heading3_expected:
                    print(f"  MISS: para[{idx}] '{text}' has style '{style}' instead of 'Heading 3'")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Heading 4 on sub-subsections (0.15 points)
    try:
        if len(heading4_expected) == 0:
            print("FAIL: Component 4 -- No sub-subsections found in document")
        else:
            correct = sum(1 for _, _, style in heading4_expected if style == 'Heading 4')
            total_h4 = len(heading4_expected)
            if correct == total_h4:
                print(f"PASS: Component 4 -- All {total_h4} sub-subsections have Heading 4 (0.15 pts)")
                total_score += 0.15
            elif correct > 0:
                partial = 0.15 * (correct / total_h4)
                total_score += partial
                print(f"PARTIAL: Component 4 -- {correct}/{total_h4} sub-subsections have Heading 4 ({partial:.2f} pts)")
                for idx, text, style in heading4_expected:
                    if style != 'Heading 4':
                        print(f"  MISS: para[{idx}] '{text}' has style '{style}' instead of 'Heading 4'")
            else:
                print(f"FAIL: Component 4 -- 0/{total_h4} sub-subsections have Heading 4 (0.00 pts)")
                for idx, text, style in heading4_expected:
                    print(f"  MISS: para[{idx}] '{text}' has style '{style}' instead of 'Heading 4'")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

"""
Reward Script: Compare document versions, accept changes in sections 1-2, reject changes in sections 3-4
Task ID: writer_lec_083
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.25): Section 3 has been reverted to old text
  - Component 2 (0.25): Section 4 has been reverted to old text
  - Component 3 (0.25): Section 3 reverted AND Sections 1-2 preserved with current text
  - Component 4 (0.25): Section 4 reverted AND no tracked changes remain
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_083'


def persist_app_state():
    """Send Ctrl+S to save any unsaved edits in LibreOffice Writer."""
    try:
        os.environ["DISPLAY"] = ":0"
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        import time
        time.sleep(1.0)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.

    The task asks the agent to compare the current document with an older version,
    accept changes in sections 1 and 2 (keep current text), and reject changes
    in sections 3 and 4 (revert to old text).

    In the initial state, ALL sections have current (new) text.
    In the golden state, sections 1-2 keep current text, sections 3-4 revert to old text.
    Therefore, the CHANGES are in sections 3-4 reverting to old content.

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

    paragraphs = doc.paragraphs
    if len(paragraphs) < 18:
        print(f"FAIL: Expected at least 18 paragraphs, found {len(paragraphs)}")
        print("REWARD: 0.0")
        return 0.0

    # Identify section boundaries by heading text
    section_map = {}
    for i, para in enumerate(paragraphs):
        text = para.text.strip()
        if text.startswith("Section 1:"):
            section_map[1] = i
        elif text.startswith("Section 2:"):
            section_map[2] = i
        elif text.startswith("Section 3:"):
            section_map[3] = i
        elif text.startswith("Section 4:"):
            section_map[4] = i

    if len(section_map) < 4:
        print(f"FAIL: Could not find all 4 section headings, found: {list(section_map.keys())}")
        print("REWARD: 0.0")
        return 0.0

    # Helper: get concatenated text of a section
    def get_section_text(section_num):
        start = section_map[section_num] + 1
        next_sections = [section_map[s] for s in section_map if s > section_num]
        end = min(next_sections) if next_sections else len(paragraphs)
        return " ".join(paragraphs[i].text for i in range(start, end))

    # Distinguishing markers
    # Section 1: current="completed the Neptune platform redesign", old="been focused on the Neptune platform redesign"
    # Section 2: current="expanded the Horizon campaign in January 2025", old="launched the Horizon campaign in November 2024"
    # Section 3: current="completed a follow-up pulse survey in February 2025", old="conducted the annual employee engagement survey in December 2024"
    # Section 4: current="Q1 2025 reached $5.6 million", old="Q4 2024 reached $4.8 million"

    s1_text = get_section_text(1)
    s2_text = get_section_text(2)
    s3_text = get_section_text(3)
    s4_text = get_section_text(4)

    s3_has_old = "conducted the annual employee engagement survey in December 2024" in s3_text
    s3_has_current = "completed a follow-up pulse survey in February 2025" in s3_text
    s4_has_old = "Q4 2024 reached $4.8 million" in s4_text
    s4_has_current = "Q1 2025 reached $5.6 million" in s4_text
    s1_has_current = "completed the Neptune platform redesign" in s1_text
    s2_has_current = "expanded the Horizon campaign in January 2025" in s2_text

    # Component 1: Section 3 has been reverted to old text (0.25 points)
    # FAILS on initial (section 3 has current text), PASSES on golden (section 3 has old text)
    try:
        if s3_has_old and not s3_has_current:
            print(f"PASS: Component 1 — Section 3 has old text (reverted) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Section 3: has_old={s3_has_old}, has_current={s3_has_current}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Section 4 has been reverted to old text (0.25 points)
    # FAILS on initial (section 4 has current text), PASSES on golden (section 4 has old text)
    try:
        if s4_has_old and not s4_has_current:
            print(f"PASS: Component 2 — Section 4 has old text (reverted) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Section 4: has_old={s4_has_old}, has_current={s4_has_current}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Section 3 reverted AND Sections 1-2 preserved (0.25 points)
    # This compound check ensures that rejecting changes in 3-4 didn't break sections 1-2.
    # FAILS on initial (section 3 is not reverted), PASSES on golden.
    try:
        if s3_has_old and s1_has_current and s2_has_current:
            print(f"PASS: Component 3 — Sections 1-2 preserved + Section 3 reverted (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — s3_old={s3_has_old}, s1_current={s1_has_current}, s2_current={s2_has_current}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Section 4 reverted AND no tracked changes remain (0.25 points)
    # This compound check anchors the "no tracked changes" check to a task-introduced change.
    # FAILS on initial (section 4 is not reverted), PASSES on golden.
    try:
        from lxml import etree
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        body = doc.element.body
        ins_count = len(body.findall('.//w:ins', ns))
        del_count = len(body.findall('.//w:del', ns))
        no_tracked = (ins_count == 0 and del_count == 0)

        if s4_has_old and no_tracked:
            print(f"PASS: Component 4 — Section 4 reverted + no tracked changes (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — s4_old={s4_has_old}, tracked_ins={ins_count}, tracked_del={del_count}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state()

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

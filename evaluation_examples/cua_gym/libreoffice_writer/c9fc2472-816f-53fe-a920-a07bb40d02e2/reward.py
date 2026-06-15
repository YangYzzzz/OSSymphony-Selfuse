"""
Reward Script: Duplicate each section heading as an italic 'End of' closing label at the end of each section.
Task ID: writer_edit_014
Domain: libreoffice_writer
Scoring:
  Component 1: 'End of Company Overview' italic paragraph at end of Section 1 (0.35 pts)
  Component 2: 'End of Our Mission' italic paragraph at end of Section 2 (0.35 pts)
  Component 3: 'End of Global Reach' italic paragraph at end of Section 3 (0.30 pts)
  Total: 1.0
"""

import os

from docx import Document

WORKDIR = '/home/user/Desktop'
TASK_ID = 'company_intro'
FILE_PATH = f'{WORKDIR}/{TASK_ID}.docx'


def is_italic_run(run):
    """Return True if the run is italic (run.italic or run.font.italic is True)."""
    return run.italic is True or run.font.italic is True


def verify_closing_label(paragraphs, expected_text, section_name):
    """
    Verify that a paragraph with the given expected_text exists,
    has italic formatting, and is placed correctly (after body paragraphs,
    before the next Heading 1 or at end of document).

    Returns (found_text, has_correct_italic, has_correct_position).
    """
    found_idx = None
    for i, para in enumerate(paragraphs):
        if para.text.strip() == expected_text:
            found_idx = i
            break

    if found_idx is None:
        return False, False, False

    para = paragraphs[found_idx]

    # Check italic: all non-empty runs must be italic
    runs_with_text = [r for r in para.runs if r.text.strip()]
    if not runs_with_text:
        # Fallback: check full text via XML is not ideal but check text at least exists
        is_italic = False
    else:
        is_italic = all(is_italic_run(r) for r in runs_with_text)

    # Check position: the paragraph immediately before it should be a Normal paragraph
    # (body text, not a Heading), and the paragraph after it (if any) should be
    # either a Heading 1 or it is the last paragraph.
    correct_position = True

    # Before: must not be another 'End of' or a heading
    if found_idx > 0:
        prev_para = paragraphs[found_idx - 1]
        prev_style = prev_para.style.name
        if 'Heading' in prev_style:
            # Would mean no body paragraphs in section — unusual
            correct_position = False
        if prev_para.text.strip().startswith('End of '):
            correct_position = False

    # After: must be Heading 1 or end of document
    if found_idx < len(paragraphs) - 1:
        next_para = paragraphs[found_idx + 1]
        next_style = next_para.style.name
        if 'Heading 1' not in next_style:
            correct_position = False

    return True, is_italic, correct_position


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
    print(f"Document has {len(paragraphs)} paragraphs.")

    # Precondition: original headings and body text must still be present
    heading_texts = [p.text.strip() for p in paragraphs if 'Heading 1' in p.style.name]
    required_headings = {'Company Overview', 'Our Mission', 'Global Reach'}
    if not required_headings.issubset(set(heading_texts)):
        print(f"PRECONDITION FAIL: Original headings missing. Found: {heading_texts}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: 'End of Company Overview' italic paragraph at end of Section 1 (0.35 pts)
    try:
        found, is_italic, correct_pos = verify_closing_label(
            paragraphs, 'End of Company Overview', 'Company Overview'
        )
        if found and is_italic and correct_pos:
            print("PASS: Component 1 — 'End of Company Overview' found, italic, correct position (0.35 pts)")
            total_score += 0.35
        elif found and is_italic:
            print("PARTIAL: Component 1 — 'End of Company Overview' found and italic but wrong position (0.20 pts)")
            total_score += 0.20
        elif found:
            print(f"PARTIAL: Component 1 — 'End of Company Overview' found but NOT italic (0.10 pts)")
            total_score += 0.10
        else:
            print("FAIL: Component 1 — 'End of Company Overview' paragraph not found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 'End of Our Mission' italic paragraph at end of Section 2 (0.35 pts)
    try:
        found, is_italic, correct_pos = verify_closing_label(
            paragraphs, 'End of Our Mission', 'Our Mission'
        )
        if found and is_italic and correct_pos:
            print("PASS: Component 2 — 'End of Our Mission' found, italic, correct position (0.35 pts)")
            total_score += 0.35
        elif found and is_italic:
            print("PARTIAL: Component 2 — 'End of Our Mission' found and italic but wrong position (0.20 pts)")
            total_score += 0.20
        elif found:
            print(f"PARTIAL: Component 2 — 'End of Our Mission' found but NOT italic (0.10 pts)")
            total_score += 0.10
        else:
            print("FAIL: Component 2 — 'End of Our Mission' paragraph not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 'End of Global Reach' italic paragraph at end of Section 3 (0.30 pts)
    try:
        found, is_italic, correct_pos = verify_closing_label(
            paragraphs, 'End of Global Reach', 'Global Reach'
        )
        if found and is_italic and correct_pos:
            print("PASS: Component 3 — 'End of Global Reach' found, italic, correct position (0.30 pts)")
            total_score += 0.30
        elif found and is_italic:
            print("PARTIAL: Component 3 — 'End of Global Reach' found and italic but wrong position (0.20 pts)")
            total_score += 0.20
        elif found:
            print(f"PARTIAL: Component 3 — 'End of Global Reach' found but NOT italic (0.10 pts)")
            total_score += 0.10
        else:
            print("FAIL: Component 3 — 'End of Global Reach' paragraph not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

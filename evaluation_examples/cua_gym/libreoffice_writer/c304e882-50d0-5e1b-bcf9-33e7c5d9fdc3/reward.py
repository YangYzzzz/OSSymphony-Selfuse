"""
Reward Script: Interview questionnaire template with numbered behavioral questions
Task ID: writer_hr_029
Domain: libreoffice_writer
Scoring:
  Component 1 (0.10): "Interview Questions" heading section exists
  Component 2 (0.30): 10 numbered behavioral questions present
  Component 3 (0.30): Each question followed by "Notes:" line with underlined blank
  Component 4 (0.30): Scoring Guide section with 1-5 rating scale
"""

import os
import re

from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_hr_029'


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

    # Component 1: "Interview Questions" heading section exists (0.10 points)
    # The golden file has a Heading 2 paragraph with "Interview Questions"
    # This does NOT exist in the initial file.
    try:
        heading_found = False
        for p in paragraphs:
            if p.style and 'Heading' in p.style.name and 'interview' in p.text.lower() and 'question' in p.text.lower():
                heading_found = True
                break
        if heading_found:
            print(f"PASS: Component 1 — 'Interview Questions' heading found (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — No 'Interview Questions' heading found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 10 numbered behavioral questions present (0.30 points)
    # Questions are numbered 1-10 and start with a digit followed by '.'
    # Initial file has 0 such paragraphs.
    try:
        numbered_questions = []
        for p in paragraphs:
            text = p.text.strip()
            if re.match(r'^\d+\.\s+', text) and len(text) > 20:
                # Must be a question (reasonably long text, not just a number)
                numbered_questions.append(text)

        num_q = len(numbered_questions)
        if num_q >= 10:
            print(f"PASS: Component 2 — Found {num_q} numbered questions (0.30 pts)")
            total_score += 0.30
        elif num_q >= 5:
            partial = round(0.30 * num_q / 10, 2)
            print(f"PARTIAL: Component 2 — Found {num_q}/10 numbered questions ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Found only {num_q} numbered questions, need 10")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Each question followed by "Notes:" line with underlined blank (0.30 points)
    # Each numbered question should be immediately followed (within 1-2 paras) by a "Notes:" paragraph.
    # The blank space after "Notes:" should have underline formatting.
    # Initial file has NO "Notes:" paragraphs.
    try:
        notes_count = 0
        underlined_notes_count = 0

        for i, p in enumerate(paragraphs):
            text = p.text.strip()
            if text.lower().startswith('notes:'):
                notes_count += 1
                # Check if the blank/underline part has underline formatting
                has_underline = False
                for run in p.runs:
                    if run.text.strip() and run.text.strip() != 'Notes:' and '_' in run.text:
                        if run.font.underline:
                            has_underline = True
                            break
                    # Also check for underline on any run after "Notes:"
                    if run.font.underline and len(run.text.strip()) > 0:
                        has_underline = True
                        break
                if has_underline:
                    underlined_notes_count += 1

        if notes_count >= 10 and underlined_notes_count >= 8:
            print(f"PASS: Component 3 — Found {notes_count} Notes lines, {underlined_notes_count} with underline (0.30 pts)")
            total_score += 0.30
        elif notes_count >= 5:
            # Partial credit: give credit proportional to notes found
            ratio = min(notes_count, 10) / 10
            partial = round(0.30 * ratio, 2)
            print(f"PARTIAL: Component 3 — Found {notes_count}/10 Notes lines ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Found only {notes_count} Notes lines, need 10")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Scoring Guide section with 1-5 rating scale (0.30 points)
    # Must have a scoring section heading AND 5 rating descriptions (1-5).
    # Initial file has NONE of this.
    try:
        # Check for scoring section heading
        scoring_heading_found = False
        for p in paragraphs:
            if p.style and 'Heading' in p.style.name and 'scor' in p.text.lower():
                scoring_heading_found = True
                break

        # Check for 1-5 scale lines
        scale_labels = {1: False, 2: False, 3: False, 4: False, 5: False}
        expected_keywords = {
            1: 'poor',
            2: 'below average',
            3: 'average',
            4: 'above average',
            5: 'excellent'
        }

        for p in paragraphs:
            text = p.text.strip().lower()
            for num in range(1, 6):
                # Match patterns like "1 - Poor" or "1 — Poor" or "1. Poor"
                if re.match(rf'^{num}\s*[-—.)\s]', text):
                    if expected_keywords[num] in text:
                        scale_labels[num] = True

        scales_found = sum(1 for v in scale_labels.values() if v)

        if scoring_heading_found and scales_found >= 5:
            print(f"PASS: Component 4 — Scoring Guide heading + all 5 scale levels found (0.30 pts)")
            total_score += 0.30
        elif scoring_heading_found and scales_found >= 3:
            partial = round(0.15 + 0.15 * scales_found / 5, 2)
            print(f"PARTIAL: Component 4 — Scoring heading found, {scales_found}/5 scale levels ({partial} pts)")
            total_score += partial
        elif scales_found >= 3:
            partial = round(0.15 * scales_found / 5, 2)
            print(f"PARTIAL: Component 4 — No scoring heading, but {scales_found}/5 scale levels ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — Scoring heading: {scoring_heading_found}, scale levels found: {scales_found}/5")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

"""
Reward Script: Insert a blank line after every sentence throughout the entire document.
Task ID: osworld_writer_blank_line_insertion_009
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): Document has ~31 paragraphs (15 sentences + 15 blank lines + 1 title)
  Component 2 (0.4): Non-title paragraphs follow alternating sentence/blank pattern
  Component 3 (0.3): All original sentence content is preserved in the document
"""

import os
import re

try:
    from docx import Document
except ImportError:
    print("CRITICAL: python-docx not available")
    print("REWARD: 0.0")
    raise SystemExit(1)

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_blank_line_insertion_009'

# The 15 sentences expected (split from the 3 body paragraphs in the initial document)
EXPECTED_SENTENCES = [
    "All employees are expected to report to work on time and maintain consistent attendance throughout the year.",
    "Tardiness of more than fifteen minutes without prior notice will be recorded as an unexcused absence.",
    "Employees who anticipate being late must notify their direct supervisor at least thirty minutes before their scheduled start time.",
    "Repeated unexcused absences may result in disciplinary action, up to and including termination of employment.",
    "Any employee with an attendance concern should contact Human Resources to discuss available accommodations or leave options.",
    "All staff members are required to maintain a professional and respectful demeanor when interacting with colleagues, clients, and vendors.",
    "Harassment, discrimination, or any form of hostile behavior in the workplace is strictly prohibited and will not be tolerated.",
    "Employees who witness or experience inappropriate conduct should report it immediately to their manager or the Human Resources department.",
    "Confidential investigations will be conducted for all reported incidents to ensure a fair and impartial review process.",
    "Violations of the workplace conduct policy may result in immediate suspension or termination depending on the severity of the offense.",
    "Employees approved for remote work arrangements must maintain a secure and productive home office environment during all scheduled work hours.",
    "Company-issued equipment, including laptops, monitors, and peripherals, must be used exclusively for business-related activities.",
    "Any loss, damage, or theft of company equipment must be reported to the IT department within twenty-four hours of the incident.",
    "Remote employees are expected to participate in all scheduled virtual meetings and respond to communications within two business hours.",
    "The company reserves the right to revoke remote work privileges if performance standards or security requirements are not consistently met.",
]

# In initial state, 3 body paragraphs contain multiple sentences each (concatenated)
# After task: 15 sentence paragraphs + 15 blank paragraphs + 1 title = 31 paragraphs
EXPECTED_TOTAL_PARAGRAPHS = 31
# Tolerance: allow +/- 2 paragraphs in case of trailing blank or minor variation
PARA_COUNT_MIN = 29
PARA_COUNT_MAX = 33


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
    num_paras = len(paragraphs)

    print(f"INFO: Document has {num_paras} paragraphs")
    for i, p in enumerate(paragraphs):
        print(f"  [{i}] empty={len(p.text.strip())==0} | {repr(p.text[:60])}")

    # -------------------------------------------------------
    # Component 1: Document paragraph count is ~31 (0.3 pts)
    # The initial document has 4 paragraphs (1 title + 3 long body paragraphs).
    # After inserting a blank line after every sentence, the golden state has 31 paragraphs.
    # We allow a small tolerance in case of trailing blank paragraphs.
    # -------------------------------------------------------
    try:
        if PARA_COUNT_MIN <= num_paras <= PARA_COUNT_MAX:
            print(f"PASS: Component 1 — paragraph count {num_paras} is in expected range "
                  f"[{PARA_COUNT_MIN}, {PARA_COUNT_MAX}] (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — paragraph count {num_paras} is outside expected range "
                  f"[{PARA_COUNT_MIN}, {PARA_COUNT_MAX}]. Initial doc has only 4 paragraphs.")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------
    # Component 2: Non-title paragraphs follow alternating sentence/blank pattern (0.4 pts)
    # Starting from paragraph index 1 (first body paragraph), the pattern should be:
    #   [sentence], [blank], [sentence], [blank], ...
    # We verify that every even-indexed body paragraph (0-indexed from body start) is non-empty
    # and every odd-indexed body paragraph is empty.
    # -------------------------------------------------------
    try:
        # Skip the title paragraph (index 0)
        body_paras = paragraphs[1:]
        if len(body_paras) == 0:
            print("FAIL: Component 2 — no body paragraphs found")
        else:
            # Count pairs that match the alternating pattern
            sentence_positions = list(range(0, len(body_paras), 2))  # should be non-empty
            blank_positions = list(range(1, len(body_paras), 2))     # should be empty

            sentence_ok = sum(1 for i in sentence_positions if body_paras[i].text.strip() != "")
            blank_ok = sum(1 for i in blank_positions if body_paras[i].text.strip() == "")

            total_sentence_positions = len(sentence_positions)
            total_blank_positions = len(blank_positions)

            # Expect at least 14 out of 15 sentence positions to be non-empty
            # and at least 14 out of 15 blank positions to be empty
            sentence_ratio = sentence_ok / max(total_sentence_positions, 1)
            blank_ratio = blank_ok / max(total_blank_positions, 1)

            print(f"INFO: Component 2 — sentence positions: {sentence_ok}/{total_sentence_positions} correct, "
                  f"blank positions: {blank_ok}/{total_blank_positions} correct")

            if sentence_ratio >= 0.9 and blank_ratio >= 0.9:
                print(f"PASS: Component 2 — alternating sentence/blank pattern verified "
                      f"(sentence_ratio={sentence_ratio:.2f}, blank_ratio={blank_ratio:.2f}) (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 — alternating pattern not satisfied "
                      f"(sentence_ratio={sentence_ratio:.2f}, blank_ratio={blank_ratio:.2f})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------
    # Component 3: All original sentence content is preserved in the document (0.3 pts)
    # Collect all non-empty paragraph text and check that each of the 15 expected sentences
    # appears as an independent paragraph (exact or near-exact match).
    # -------------------------------------------------------
    try:
        non_empty_texts = [p.text.strip() for p in paragraphs if p.text.strip() != ""]
        # Remove the title from consideration
        body_texts = [t for t in non_empty_texts if t != "Employee Policy Notice"]

        matched = 0
        for expected_sent in EXPECTED_SENTENCES:
            # Check if the sentence appears as a standalone paragraph (exact match)
            sentence_found = (expected_sent in body_texts)
            if sentence_found:
                matched += 1
            else:
                print(f"FAIL: Component 3 — sentence not found as standalone paragraph: "
                      f"{repr(expected_sent[:60])}")

        match_ratio = matched / len(EXPECTED_SENTENCES)
        print(f"INFO: Component 3 — {matched}/{len(EXPECTED_SENTENCES)} sentences found as standalone paragraphs")

        if match_ratio >= 0.9:
            print(f"PASS: Component 3 — content preservation verified "
                  f"({matched}/{len(EXPECTED_SENTENCES)} sentences) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — only {matched}/{len(EXPECTED_SENTENCES)} sentences matched "
                  f"(need >= 90%)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in a given env
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

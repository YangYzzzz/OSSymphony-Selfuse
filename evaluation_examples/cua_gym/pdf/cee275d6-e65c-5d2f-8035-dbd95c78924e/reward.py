"""
Reward Script: Create a conference agenda PDF on the Desktop
Task ID: pdf_cr_036
Domain: pdf
Scoring:
  Component 1 (0.20): File exists and is a valid PDF with >= 1 page
  Component 2 (0.20): Contains event title 'TechSummit 2024'
  Component 3 (0.20): Contains venue 'Grand Convention Center'
  Component 4 (0.20): Contains key content: 'Dr. Sarah Lin' and 'Cybersecurity Trends'
  Component 5 (0.20): Schedule table has at least 6 session rows (identified by time slots)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_036'
FILE_PATH = os.path.join(WORKDIR, 'Desktop', 'agenda.pdf')

# Expected time slots from the schedule
EXPECTED_TIME_SLOTS = [
    '09:00',
    '09:45',
    '10:45',
    '11:45',
    '14:00',
    '15:00',
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: must be a loadable PDF
    try:
        import pymupdf
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract all text from the PDF
    full_text = ""
    try:
        for i in range(doc.page_count):
            page = doc[i]
            full_text += page.get_text()
    except Exception as e:
        print(f"ERROR: Could not extract text: {e}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Valid PDF with at least 1 page (0.20 points)
    # This component verifies the file was created (it didn't exist on initial_env)
    try:
        page_count = doc.page_count
        if page_count >= 1:
            print(f"PASS: Component 1 - Valid PDF with {page_count} page(s) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 - PDF has 0 pages")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Contains event title 'TechSummit 2024' (0.20 points)
    try:
        if 'TechSummit 2024' in full_text:
            print(f"PASS: Component 2 - Found 'TechSummit 2024' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 - 'TechSummit 2024' not found in text")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Contains venue 'Grand Convention Center' (0.20 points)
    try:
        if 'Grand Convention Center' in full_text:
            print(f"PASS: Component 3 - Found 'Grand Convention Center' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 - 'Grand Convention Center' not found in text")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Contains key content markers (0.20 points)
    # Both 'Dr. Sarah Lin' and 'Cybersecurity Trends' must be present
    try:
        has_speaker = 'Dr. Sarah Lin' in full_text
        has_session = 'Cybersecurity Trends' in full_text
        if has_speaker and has_session:
            print(f"PASS: Component 4 - Found 'Dr. Sarah Lin' and 'Cybersecurity Trends' (0.20 pts)")
            total_score += 0.20
        else:
            missing = []
            if not has_speaker:
                missing.append("'Dr. Sarah Lin'")
            if not has_session:
                missing.append("'Cybersecurity Trends'")
            print(f"FAIL: Component 4 - Missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Schedule table with at least 6 session rows (0.20 points)
    # Identify session rows by matching time slot patterns (HH:MM)
    try:
        # Count how many of the expected time slots appear in the text
        found_slots = 0
        for slot in EXPECTED_TIME_SLOTS:
            if slot in full_text:
                found_slots += 1

        if found_slots >= 6:
            print(f"PASS: Component 5 - Found {found_slots}/6 expected time slots (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 5 - Found only {found_slots}/6 expected time slots")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

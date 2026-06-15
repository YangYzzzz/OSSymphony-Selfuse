"""
Reward Script: Book Reading Rate / Exhibition Attendance Research
Task ID: osworld_multi_apps_book_reading_rate_012
Domain: multi_apps (LibreOffice Writer + Web Research)

Task: Research museum websites to find visitor counts for 5 exhibitions,
then write the exhibition with the fewest visitors into lowest_attendance.docx on the Desktop.

Expected answer: 'Picasso Celebration' (280,000 visitors — fewest among all exhibitions)

Scoring:
  Component 1: lowest_attendance.docx contains non-empty text  (0.4 pts)
  Component 2: The text identifies 'Picasso Celebration'        (0.6 pts)
  Total: 1.0
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_book_reading_rate_012'

# Target file: lowest_attendance.docx on the Desktop
DOCX_PATH = f'{WORKDIR}/Desktop/lowest_attendance.docx'

# The expected answer — exhibition with fewest visitors based on museum websites
EXPECTED_EXHIBITION = 'Picasso Celebration'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    The task requires:
    1. Researching museum websites for visitor counts of 5 exhibitions
    2. Identifying the exhibition with the lowest attendance
    3. Writing that exhibition name ('Picasso Celebration', 280,000 visitors) into lowest_attendance.docx

    Initial state: lowest_attendance.docx is empty (0 paragraphs, no content)
    Golden state: lowest_attendance.docx contains 'Picasso Celebration'
    """
    total_score = 0.0

    # Load the document
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract all text from the document
    all_text = ""
    try:
        paragraphs = doc.paragraphs
        all_text = " ".join(para.text for para in paragraphs).strip()
    except Exception as e:
        print(f"ERROR: Could not extract text from document: {e}")

    # Component 1: Document contains non-empty text (0.4 points)
    # Initial state: empty document (no paragraphs with text)
    # Golden state: document contains the exhibition name
    try:
        if all_text:
            print(f"PASS: Component 1 — Document contains text: [{all_text[:100]}] (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Document is empty (no text found)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Document identifies 'Picasso Celebration' as the lowest attendance exhibition (0.6 points)
    # Based on museum website data: Picasso Celebration had 280,000 visitors (fewest of 5 exhibitions)
    # Vermeer: 650,000 | Picasso Celebration: 280,000 | Art and Climate Change: 320,000 |
    # After Impressionism: 385,000 | Manet/Degas: 425,000
    # Initial state: empty document — cannot contain this answer
    # Golden state: document contains 'Picasso Celebration'
    try:
        if EXPECTED_EXHIBITION.lower() in all_text.lower():
            print(f"PASS: Component 2 — Document contains '{EXPECTED_EXHIBITION}' as the lowest attendance exhibition (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 2 — Expected '{EXPECTED_EXHIBITION}' in document, found: [{all_text[:200]}]")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against the target file path on the VM
if not os.path.exists(DOCX_PATH):
    print(f"File not found: {DOCX_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(DOCX_PATH)

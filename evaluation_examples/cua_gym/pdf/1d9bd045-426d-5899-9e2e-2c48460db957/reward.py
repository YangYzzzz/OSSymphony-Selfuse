"""
Reward Script: Create a student report card PDF
Task ID: pdf_cr_035
Domain: pdf
Scoring:
  Component 1 (0.15): PDF exists at correct path with exactly 1 page
  Component 2 (0.25): Student info — Emma Wilson, STU-2024-0789, Fall 2024
  Component 3 (0.25): All 6 subjects present in text
  Component 4 (0.20): Grade data correct (grades, credits, points per subject)
  Component 5 (0.15): GPA summary — 3.57, total credits 19, total points 67.9
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_035'
FILE_PATH = os.path.join(WORKDIR, 'Desktop', 'report_card.pdf')


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

    try:
        import fitz  # PyMuPDF
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract full text from all pages
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    page_count = len(doc)
    doc.close()

    # Normalize text for searching
    text_lower = full_text.lower()

    # Component 1: PDF has exactly 1 page (0.15 points)
    # This checks a task-introduced change: the golden PDF must be a single-page document.
    # On initial_env, the file doesn't exist so we never reach here.
    try:
        if page_count == 1:
            print(f"PASS: Component 1 — PDF has exactly 1 page (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Expected 1 page, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Student info present (0.25 points)
    # Check for Emma Wilson, STU-2024-0789, Fall 2024
    try:
        info_checks = {
            'Emma Wilson': 'emma wilson' in text_lower,
            'STU-2024-0789': 'stu-2024-0789' in text_lower,
            'Fall 2024': 'fall 2024' in text_lower,
        }
        info_pass_count = sum(1 for v in info_checks.values() if v)
        info_score = (info_pass_count / 3) * 0.25

        if info_pass_count == 3:
            print(f"PASS: Component 2 — All student info found: Emma Wilson, STU-2024-0789, Fall 2024 (0.25 pts)")
        else:
            failed = [k for k, v in info_checks.items() if not v]
            print(f"PARTIAL: Component 2 — {info_pass_count}/3 info items. Missing: {failed} ({info_score:.3f} pts)")
        total_score += info_score
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 6 subjects present (0.25 points)
    # Subjects: Mathematics, Physics, Computer Science, English Literature, Chemistry, History
    try:
        subjects = ['mathematics', 'physics', 'computer science', 'english literature', 'chemistry', 'history']
        found_subjects = [s for s in subjects if s in text_lower]
        subj_count = len(found_subjects)
        subj_score = (subj_count / 6) * 0.25

        if subj_count == 6:
            print(f"PASS: Component 3 — All 6 subjects found (0.25 pts)")
        else:
            missing = [s for s in subjects if s not in text_lower]
            print(f"PARTIAL: Component 3 — {subj_count}/6 subjects. Missing: {missing} ({subj_score:.3f} pts)")
        total_score += subj_score
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Grade data correct (0.20 points)
    # Check that grade values, credits, and points are present for each subject
    try:
        grade_data = {
            'Mathematics': ('A', '4', '16.0'),
            'Physics': ('B+', '4', '13.2'),
            'Computer Science': ('A-', '3', '11.1'),
            'English Literature': ('B', '3', '9.0'),
            'Chemistry': ('A', '3', '12.0'),
            'History': ('B+', '2', '6.6'),
        }
        grade_checks_passed = 0
        total_grade_checks = len(grade_data)

        for subject, (grade, credits, points) in grade_data.items():
            # Check if grade, credits, and points values appear in the text
            # We verify that each specific points value is present (these are unique per subject)
            if points in full_text:
                grade_checks_passed += 1
            else:
                print(f"  DETAIL: Missing points value {points} for {subject}")

        grade_score = (grade_checks_passed / total_grade_checks) * 0.20

        if grade_checks_passed == total_grade_checks:
            print(f"PASS: Component 4 — All grade data points values found (0.20 pts)")
        else:
            print(f"PARTIAL: Component 4 — {grade_checks_passed}/{total_grade_checks} grade entries ({grade_score:.3f} pts)")
        total_score += grade_score
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: GPA summary (0.15 points)
    # Check for GPA 3.57, total credits 19, total points 67.9
    try:
        gpa_checks = {
            'GPA 3.57': '3.57' in full_text,
            'Total Credits 19': '19' in full_text,
            'Total Points 67.9': '67.9' in full_text,
        }
        gpa_pass_count = sum(1 for v in gpa_checks.values() if v)
        gpa_score = (gpa_pass_count / 3) * 0.15

        if gpa_pass_count == 3:
            print(f"PASS: Component 5 — GPA summary correct: 3.57, credits 19, points 67.9 (0.15 pts)")
        else:
            failed = [k for k, v in gpa_checks.items() if not v]
            print(f"PARTIAL: Component 5 — {gpa_pass_count}/3 GPA items. Missing: {failed} ({gpa_score:.3f} pts)")
        total_score += gpa_score
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

"""
Reward Script: Desktop File Organizer — Sort course files into subject folders
Task ID: osworld_multi_apps_desktop_organizer_015
Domain: os (file system)
Scoring:
  Component 1: Computer_Science folder has exactly the 4 correct files  — 0.4 pts
  Component 2: Mathematics folder has exactly the 3 correct files       — 0.3 pts
  Component 3: Biology folder has exactly the 3 correct files           — 0.3 pts
  Total: 1.0
"""

import os

DESKTOP = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_desktop_organizer_015'

# Expected contents of each subject folder after the task is completed
EXPECTED_CS = {
    'algorithms_lecture.pdf',
    'computational_biology_intro.pdf',
    'data_structures.pptx',
    'statistics_for_cs.pdf',
}

EXPECTED_MATH = {
    'linear_algebra_notes.pdf',
    'statistics_for_cs.pdf',
    'calculus_problems.xlsx',
}

EXPECTED_BIO = {
    'cell_biology_chapter3.pdf',
    'computational_biology_intro.pdf',
    'genetics_homework.docx',
}


def verify_task():
    """
    Verify desktop organizer task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: Desktop must exist
    if not os.path.isdir(DESKTOP):
        print(f"CRITICAL: Desktop directory not found at {DESKTOP}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Computer_Science folder has correct files (0.4 points)
    try:
        cs_path = os.path.join(DESKTOP, 'Computer_Science')
        if not os.path.isdir(cs_path):
            print("FAIL: Component 1 — Computer_Science directory does not exist")
        else:
            actual_cs = set(os.listdir(cs_path))
            if actual_cs == EXPECTED_CS:
                print(f"PASS: Component 1 — Computer_Science folder has correct 4 files: {sorted(actual_cs)} (0.4 pts)")
                total_score += 0.4
            else:
                missing = EXPECTED_CS - actual_cs
                extra = actual_cs - EXPECTED_CS
                print(f"FAIL: Component 1 — Computer_Science folder mismatch.")
                if missing:
                    print(f"  Missing: {sorted(missing)}")
                if extra:
                    print(f"  Unexpected: {sorted(extra)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Mathematics folder has correct files (0.3 points)
    try:
        math_path = os.path.join(DESKTOP, 'Mathematics')
        if not os.path.isdir(math_path):
            print("FAIL: Component 2 — Mathematics directory does not exist")
        else:
            actual_math = set(os.listdir(math_path))
            if actual_math == EXPECTED_MATH:
                print(f"PASS: Component 2 — Mathematics folder has correct 3 files: {sorted(actual_math)} (0.3 pts)")
                total_score += 0.3
            else:
                missing = EXPECTED_MATH - actual_math
                extra = actual_math - EXPECTED_MATH
                print(f"FAIL: Component 2 — Mathematics folder mismatch.")
                if missing:
                    print(f"  Missing: {sorted(missing)}")
                if extra:
                    print(f"  Unexpected: {sorted(extra)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Biology folder has correct files (0.3 points)
    try:
        bio_path = os.path.join(DESKTOP, 'Biology')
        if not os.path.isdir(bio_path):
            print("FAIL: Component 3 — Biology directory does not exist")
        else:
            actual_bio = set(os.listdir(bio_path))
            if actual_bio == EXPECTED_BIO:
                print(f"PASS: Component 3 — Biology folder has correct 3 files: {sorted(actual_bio)} (0.3 pts)")
                total_score += 0.3
            else:
                missing = EXPECTED_BIO - actual_bio
                extra = actual_bio - EXPECTED_BIO
                print(f"FAIL: Component 3 — Biology folder mismatch.")
                if missing:
                    print(f"  Missing: {sorted(missing)}")
                if extra:
                    print(f"  Unexpected: {sorted(extra)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

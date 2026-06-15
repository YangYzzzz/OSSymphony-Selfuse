"""
Reward Script: Desktop Organizer - Smart Cleanup
Task ID: osworld_multi_apps_desktop_organizer_013
Domain: os (filesystem)

Scoring Rubric:
  Component 1: Old_Files/ directory exists and contains budget_2024.xlsx and old_notes.txt (0.4 pts)
  Component 2: Duplicates/ directory exists and contains report_final_v2.docx and presentation_backup.pptx (0.4 pts)
  Component 3: Desktop root contains only report_final.docx and presentation_latest.pptx (0.2 pts)
  Total: 1.0

Task Description:
  Move all files older than 30 days to 'Old_Files/' folder.
  Move duplicate files (same content, different names) to 'Duplicates/' folder.
  Leave unique recent files in place.
"""

import os

DESKTOP = '/home/user/Desktop'


def check_old_files():
    """Component 1: Old_Files/ directory contains budget_2024.xlsx and old_notes.txt."""
    old_files_dir = os.path.join(DESKTOP, 'Old_Files')
    if not os.path.isdir(old_files_dir):
        print(f"FAIL: Component 1 — Old_Files/ directory does not exist at {old_files_dir}")
        return 0.0
    contents = set(os.listdir(old_files_dir))
    expected = {'budget_2024.xlsx', 'old_notes.txt'}
    missing = expected - contents
    if missing:
        print(f"FAIL: Component 1 — Old_Files/ is missing required files: {missing}")
        return 0.0
    extra = contents - expected
    if extra:
        print(f"PASS: Component 1 — Old_Files/ has required files (extra: {extra}) (0.4 pts)")
    else:
        print(f"PASS: Component 1 — Old_Files/ contains exactly budget_2024.xlsx and old_notes.txt (0.4 pts)")
    return 0.4


def check_duplicates():
    """Component 2: Duplicates/ directory contains report_final_v2.docx and presentation_backup.pptx."""
    duplicates_dir = os.path.join(DESKTOP, 'Duplicates')
    if not os.path.isdir(duplicates_dir):
        print(f"FAIL: Component 2 — Duplicates/ directory does not exist at {duplicates_dir}")
        return 0.0
    contents = set(os.listdir(duplicates_dir))
    expected = {'report_final_v2.docx', 'presentation_backup.pptx'}
    missing = expected - contents
    if missing:
        print(f"FAIL: Component 2 — Duplicates/ is missing required files: {missing}")
        return 0.0
    extra = contents - expected
    if extra:
        print(f"PASS: Component 2 — Duplicates/ has required files (extra: {extra}) (0.4 pts)")
    else:
        print(f"PASS: Component 2 — Duplicates/ contains exactly report_final_v2.docx and presentation_backup.pptx (0.4 pts)")
    return 0.4


def check_desktop_root():
    """Component 3: Desktop root contains only report_final.docx and presentation_latest.pptx."""
    all_entries = set(os.listdir(DESKTOP))
    allowed_dirs = {'Old_Files', 'Duplicates'}
    root_files = {e for e in all_entries if os.path.isfile(os.path.join(DESKTOP, e))}
    root_dirs = {e for e in all_entries if os.path.isdir(os.path.join(DESKTOP, e))}
    expected_root_files = {'report_final.docx', 'presentation_latest.pptx'}
    unexpected_files = root_files - expected_root_files
    missing_files = expected_root_files - root_files
    unexpected_dirs = root_dirs - allowed_dirs
    if missing_files:
        print(f"FAIL: Component 3 — Desktop root is missing required files: {missing_files}")
        return 0.0
    if unexpected_files:
        print(f"FAIL: Component 3 — Desktop root has files that should have been moved: {unexpected_files}")
        return 0.0
    if unexpected_dirs:
        print(f"FAIL: Component 3 — Desktop root has unexpected directories: {unexpected_dirs}")
        return 0.0
    print(f"PASS: Component 3 — Desktop root contains exactly report_final.docx and presentation_latest.pptx (0.2 pts)")
    return 0.2


def verify_task():
    """
    Verify desktop cleanup task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    # Precondition: Desktop directory must exist
    if not os.path.isdir(DESKTOP):
        print(f"CRITICAL: Desktop directory not found at {DESKTOP}")
        print("REWARD: 0.0")
        return 0.0

    total_score = 0.0

    # Component 1: Old files (>30 days) moved to Old_Files/ (0.4 pts)
    try:
        score1 = check_old_files()
        if score1 > 0:
            total_score += score1
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Duplicate files moved to Duplicates/ (0.4 pts)
    try:
        score2 = check_duplicates()
        if score2 > 0:
            total_score += score2
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Correct files remain at Desktop root (0.2 pts)
    try:
        score3 = check_desktop_root()
        if score3 > 0:
            total_score += score3
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: run directly on the VM
verify_task()

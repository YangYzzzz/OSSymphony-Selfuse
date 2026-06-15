"""
Reward Script: Download chapter PDFs from tutorial website into ~/ml_course
Task ID: osworld_multi_apps_web_download_002
Domain: os (file system verification)
Scoring:
  - Component 1: chapter2.pdf present in ~/ml_course with correct size (0.1 pts)
  - Component 2: chapter3.pdf present in ~/ml_course with correct size (0.1 pts)
  - Component 3: chapter4.pdf present in ~/ml_course with correct size (0.1 pts)
  - Component 4: chapter5.pdf present in ~/ml_course with correct size (0.1 pts)
  - Component 5: chapter6.pdf present in ~/ml_course with correct size (0.1 pts)
  - Component 6: chapter7.pdf present in ~/ml_course with correct size (0.1 pts)
  - Component 7: chapter8.pdf present in ~/ml_course with correct size (0.1 pts)
  - Component 8: chapter1.pdf is unchanged (still present, same size) (0.15 pts)
  - Component 9: No extra unexpected files added to ~/ml_course (0.15 pts)

  Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_download_002'
ML_COURSE_DIR = '/home/user/ml_course'

# Expected sizes of PDFs as downloaded from the tutorial site
# (these match the files in ml_tutorial_site on the initial_env)
EXPECTED_CHAPTERS = {
    'chapter2.pdf': 1202,
    'chapter3.pdf': 1202,
    'chapter4.pdf': 1165,
    'chapter5.pdf': 1179,
    'chapter6.pdf': 1165,
    'chapter7.pdf': 1134,
    'chapter8.pdf': 1169,
}

# chapter1.pdf was already present and should remain unchanged
CHAPTER1_EXPECTED_SIZE = 1245

# The complete expected set of files in ml_course after task completion
EXPECTED_ALL_FILES = set(EXPECTED_CHAPTERS.keys()) | {'chapter1.pdf'}


def verify_task():
    """
    Verify that chapters 2-8 have been downloaded into ~/ml_course
    with original filenames and correct sizes, and that chapter1.pdf
    remains unchanged.

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: ml_course directory must exist
    if not os.path.isdir(ML_COURSE_DIR):
        print(f"CRITICAL: Directory not found: {ML_COURSE_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Components 1-7: Each new chapter PDF (2-8) must be present with correct size
    # Each is worth 0.1 points — they FAIL on initial_env (files not present) and
    # PASS on golden_env (files downloaded correctly).
    for chapter_file, expected_size in EXPECTED_CHAPTERS.items():
        file_path = os.path.join(ML_COURSE_DIR, chapter_file)
        try:
            if os.path.isfile(file_path):
                actual_size = os.path.getsize(file_path)
                if actual_size == expected_size:
                    print(f"PASS: {chapter_file} present with correct size {actual_size} bytes (0.1 pts)")
                    total_score += 0.1
                elif actual_size > 0:
                    # File present but wrong size - partial credit not awarded (size mismatch)
                    print(f"FAIL: {chapter_file} present but wrong size: expected {expected_size}, got {actual_size}")
                else:
                    print(f"FAIL: {chapter_file} present but empty (0 bytes)")
            else:
                print(f"FAIL: {chapter_file} NOT found in {ML_COURSE_DIR}")
        except Exception as e:
            print(f"ERROR: Checking {chapter_file}: {e}")

    # Check chapter1.pdf integrity as a sub-condition for Component 8
    # (chapter1.pdf exists in both initial and golden, so this is NOT a standalone scored component)
    chapter1_path = os.path.join(ML_COURSE_DIR, 'chapter1.pdf')
    chapter1_actual_size = -1
    try:
        if os.path.isfile(chapter1_path):
            chapter1_actual_size = os.path.getsize(chapter1_path)
            if chapter1_actual_size == CHAPTER1_EXPECTED_SIZE:
                print(f"INFO: chapter1.pdf intact ({chapter1_actual_size} bytes) — unchanged as required")
            else:
                print(f"WARN: chapter1.pdf size changed: expected {CHAPTER1_EXPECTED_SIZE}, got {chapter1_actual_size}")
        else:
            print(f"WARN: chapter1.pdf is missing from {ML_COURSE_DIR}")
    except Exception as e:
        print(f"ERROR: Checking chapter1.pdf: {e}")
        chapter1_actual_size = -1

    # Component 8: All 7 new files downloaded AND chapter1.pdf still intact (0.1 pts)
    # This component only passes if all 7 new files scored AND chapter1 is intact.
    # On initial_env: 0 new files present → this will fail → earns 0 pts. CORRECT.
    # On golden_env: 7 new files present AND chapter1 intact → earns 0.1 pts. CORRECT.
    try:
        actual_files = set(os.listdir(ML_COURSE_DIR))
        # Only PDF files
        actual_pdfs = {f for f in actual_files if f.endswith('.pdf')}
        new_chapters_present = set(EXPECTED_CHAPTERS.keys()).issubset(actual_pdfs)

        if new_chapters_present and (chapter1_actual_size == CHAPTER1_EXPECTED_SIZE):
            print(f"PASS: Component 8 — All 7 new chapters downloaded AND chapter1.pdf intact (0.1 pts)")
            total_score += 0.1
        elif new_chapters_present and (chapter1_actual_size != CHAPTER1_EXPECTED_SIZE):
            print(f"FAIL: Component 8 — New chapters present but chapter1.pdf was modified/removed")
        else:
            print(f"FAIL: Component 8 — Not all new chapters downloaded yet")
    except Exception as e:
        print(f"ERROR: Component 8 — {e}")

    # Component 9: No extra unexpected files in ml_course (0.2 pts)
    # Checks that only the expected PDF files are present — no duplicate chapters,
    # no renamed files, no junk files.
    # On initial_env: only chapter1.pdf → unexpected_files = {} → this PASSES on initial too.
    # So we must anchor this to the new files: "new chapters present AND no extras".
    # We check: actual PDFs == EXPECTED_ALL_FILES (all 8 chapters, no extras).
    # On initial_env: actual_pdfs = {chapter1.pdf} != EXPECTED_ALL_FILES → FAILS. CORRECT.
    # On golden_env: actual_pdfs = EXPECTED_ALL_FILES → PASSES. CORRECT.
    try:
        actual_files = set(os.listdir(ML_COURSE_DIR))
        actual_pdfs = {f for f in actual_files if f.endswith('.pdf')}
        non_pdf_files = {f for f in actual_files if not f.endswith('.pdf')}

        if actual_pdfs == EXPECTED_ALL_FILES:
            print(f"PASS: Component 9 — Exactly the expected files present in ml_course: {sorted(actual_pdfs)} (0.2 pts)")
            total_score += 0.2
        elif EXPECTED_ALL_FILES.issubset(actual_pdfs):
            extra_files = actual_pdfs - EXPECTED_ALL_FILES
            print(f"FAIL: Component 9 — Expected files all present but extra PDF files found: {sorted(extra_files)}")
        else:
            missing = EXPECTED_ALL_FILES - actual_pdfs
            print(f"FAIL: Component 9 — Missing expected PDFs: {sorted(missing)}")

        if non_pdf_files:
            print(f"INFO: Non-PDF files in ml_course (informational): {sorted(non_pdf_files)}")
    except Exception as e:
        print(f"ERROR: Component 9 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


# Entry point — run verification
if __name__ == "__main__" or True:
    verify_task()

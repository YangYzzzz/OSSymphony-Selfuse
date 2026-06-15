"""
Reward Script: Move all three .txt files from docs/drafts/ into docs/final/
Task ID: vscode_file_013
Domain: vs_code
Scoring:
  Component 1: All 3 .txt files exist in docs/final/       — 0.5 pts
  Component 2: File contents are preserved (content check) — 0.3 pts
  Component 3: docs/drafts/ contains no .txt files         — 0.2 pts
  Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'vscode_file_013'

PROJECT_ROOT = os.path.join(WORKDIR, 'project')
DRAFTS_DIR = os.path.join(PROJECT_ROOT, 'docs', 'drafts')
FINAL_DIR = os.path.join(PROJECT_ROOT, 'docs', 'final')

EXPECTED_FILES = ['report.txt', 'summary.txt', 'notes.txt']

# Expected content signatures (first line of each file) to verify content preservation
EXPECTED_FIRST_LINES = {
    'report.txt': 'Quarterly Performance Report - Q1 2025',
    'summary.txt': 'Project Alpha \u2014 Executive Summary',
    'notes.txt': 'Meeting Notes \u2014 Product Roadmap Review',
}


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: project structure must exist
    if not os.path.isdir(PROJECT_ROOT):
        print(f"CRITICAL: Project directory not found: {PROJECT_ROOT}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: All 3 .txt files exist in docs/final/ (0.5 points)
    # This FAILS on initial (final/ is empty) and PASSES on golden (files moved there)
    try:
        files_in_final = []
        missing_files = []
        for fname in EXPECTED_FILES:
            fpath = os.path.join(FINAL_DIR, fname)
            if os.path.isfile(fpath):
                files_in_final.append(fname)
            else:
                missing_files.append(fname)

        if len(files_in_final) == 3:
            print(f"PASS: Component 1 — All 3 files found in docs/final/: {files_in_final} (0.5 pts)")
            total_score += 0.5
        elif len(files_in_final) > 0:
            partial = round(0.5 * len(files_in_final) / 3, 4)
            print(f"PARTIAL: Component 1 — {len(files_in_final)}/3 files in docs/final/ ({partial} pts)")
            print(f"  Found: {files_in_final}  Missing: {missing_files}")
            if partial > 0:
                total_score += partial
        else:
            print(f"FAIL: Component 1 — No expected .txt files found in docs/final/")
            print(f"  Missing: {missing_files}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: File contents are preserved in docs/final/ (0.3 points)
    # Checks that moving did not corrupt or truncate the files.
    # This FAILS on initial (files don't exist in final/) and PASSES on golden (content intact).
    try:
        content_ok_count = 0
        for fname, expected_first_line in EXPECTED_FIRST_LINES.items():
            fpath = os.path.join(FINAL_DIR, fname)
            if not os.path.isfile(fpath):
                print(f"FAIL: Component 2 — {fname} not found in docs/final/ (cannot check content)")
                continue
            with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
                first_line = f.readline().rstrip('\n')
            if first_line == expected_first_line:
                print(f"PASS: Component 2 — {fname} first line correct: '{first_line}'")
                content_ok_count += 1
            else:
                print(f"FAIL: Component 2 — {fname} first line mismatch: expected '{expected_first_line}', found '{first_line}'")

        if content_ok_count == 3:
            print(f"PASS: Component 2 — All 3 file contents preserved (0.3 pts)")
            total_score += 0.3
        elif content_ok_count > 0:
            partial = round(0.3 * content_ok_count / 3, 4)
            print(f"PARTIAL: Component 2 — {content_ok_count}/3 files have correct content ({partial} pts)")
            if partial > 0:
                total_score += partial
        else:
            print(f"FAIL: Component 2 — No files with correct content found in docs/final/")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: docs/drafts/ contains no .txt files (0.2 points)
    # This FAILS on initial (3 .txt files in drafts/) and PASSES on golden (drafts/ is empty of .txt).
    try:
        if not os.path.isdir(DRAFTS_DIR):
            # If drafts/ was deleted entirely, that also satisfies "no files in drafts/"
            print(f"PASS: Component 3 — docs/drafts/ directory does not exist (fully removed) (0.2 pts)")
            total_score += 0.2
        else:
            txt_files_in_drafts = [
                f for f in os.listdir(DRAFTS_DIR)
                if f.endswith('.txt') and os.path.isfile(os.path.join(DRAFTS_DIR, f))
            ]
            if len(txt_files_in_drafts) == 0:
                print(f"PASS: Component 3 — docs/drafts/ contains no .txt files (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — docs/drafts/ still contains .txt files: {txt_files_in_drafts}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

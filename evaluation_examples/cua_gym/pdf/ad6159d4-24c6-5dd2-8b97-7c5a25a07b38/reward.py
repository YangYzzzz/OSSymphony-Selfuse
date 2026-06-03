"""
Reward Script: Extract all figures from PDF and save as JPEG files
Task ID: pdf_res_037
Domain: pdf
Scoring:
  Component 1: figures/ directory exists with files inside (0.1 pts)
  Component 2: Exactly 10 files in figures/ directory (0.2 pts)
  Component 3: Files named img_001.jpg through img_010.jpg (0.3 pts)
  Component 4: All 10 files are valid JPEG images with non-zero size (0.4 pts)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_037'
FIGURES_DIR = os.path.join(WORKDIR, 'papers', 'figures')
EXPECTED_COUNT = 10
EXPECTED_NAMES = [f'img_{i:03d}.jpg' for i in range(1, EXPECTED_COUNT + 1)]


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: figures/ directory exists and contains at least one file (0.1 points)
    try:
        if os.path.isdir(FIGURES_DIR):
            contents = os.listdir(FIGURES_DIR)
            if len(contents) > 0:
                print(f"PASS: Component 1 — figures/ directory exists with {len(contents)} file(s) (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 1 — figures/ directory exists but is empty")
        else:
            print(f"FAIL: Component 1 — figures/ directory does not exist at {FIGURES_DIR}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Exactly 10 files in figures/ directory (0.2 points)
    try:
        if os.path.isdir(FIGURES_DIR):
            files = [f for f in os.listdir(FIGURES_DIR) if os.path.isfile(os.path.join(FIGURES_DIR, f))]
            if len(files) == EXPECTED_COUNT:
                print(f"PASS: Component 2 — Exactly {EXPECTED_COUNT} files found (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2 — Expected {EXPECTED_COUNT} files, found {len(files)}")
        else:
            print(f"FAIL: Component 2 — figures/ directory does not exist")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Files named img_001.jpg through img_010.jpg (0.3 points)
    try:
        if os.path.isdir(FIGURES_DIR):
            files = sorted(os.listdir(FIGURES_DIR))
            matching = [f for f in EXPECTED_NAMES if f in files]
            if len(matching) == EXPECTED_COUNT:
                print(f"PASS: Component 3 — All {EXPECTED_COUNT} expected filenames present (0.3 pts)")
                total_score += 0.3
            else:
                missing = [f for f in EXPECTED_NAMES if f not in files]
                print(f"FAIL: Component 3 — {len(matching)}/{EXPECTED_COUNT} expected filenames found. Missing: {missing}")
        else:
            print(f"FAIL: Component 3 — figures/ directory does not exist")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: All 10 files are valid JPEG images with non-zero size (0.4 points)
    try:
        valid_count = 0
        if os.path.isdir(FIGURES_DIR):
            for fname in EXPECTED_NAMES:
                fpath = os.path.join(FIGURES_DIR, fname)
                if not os.path.isfile(fpath):
                    print(f"  SKIP: {fname} does not exist")
                    continue
                fsize = os.path.getsize(fpath)
                if fsize == 0:
                    print(f"  SKIP: {fname} is empty (0 bytes)")
                    continue
                # Check JPEG magic bytes (FFD8FF)
                with open(fpath, 'rb') as f:
                    header = f.read(3)
                if header[:2] == b'\xff\xd8':
                    valid_count += 1
                else:
                    print(f"  SKIP: {fname} is not a valid JPEG (header: {header.hex()})")

            if valid_count == EXPECTED_COUNT:
                print(f"PASS: Component 4 — All {EXPECTED_COUNT} files are valid JPEG images (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 4 — {valid_count}/{EXPECTED_COUNT} files are valid JPEGs")
        else:
            print(f"FAIL: Component 4 — figures/ directory does not exist")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

"""
Reward Script: Download all ZIP archives from programming workshop page into ~/workshop_materials
Task ID: osworld_multi_apps_web_download_003
Domain: os (file download verification)
Scoring:
  Component 1: All 4 expected ZIP files exist in ~/workshop_materials (0.5 pts)
  Component 2: All ZIP files are valid archives with correct internal filenames (0.3 pts)
  Component 3: All ZIP files have correct byte sizes matching source (0.2 pts)
"""

import os
import zipfile

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_download_003'

# Expected files based on task context: exercise1.zip, exercise2.zip, exercise3.zip, solutions.zip
EXPECTED_FILES = {
    'exercise1.zip': {
        'size': 445,
        'contents': ['exercise1_python_basics.py'],
    },
    'exercise2.zip': {
        'size': 552,
        'contents': ['exercise2_data_structures.py'],
    },
    'exercise3.zip': {
        'size': 642,
        'contents': ['exercise3_file_io.py'],
    },
    'solutions.zip': {
        'size': 910,
        'contents': ['all_solutions.py'],
    },
}

TARGET_DIR = os.path.join(WORKDIR, 'workshop_materials')


def verify_task():
    """
    Verify that all ZIP archives from the programming workshop page have been downloaded
    into ~/workshop_materials with the correct filenames and valid contents.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: workshop_materials directory must exist
    if not os.path.isdir(TARGET_DIR):
        print(f"CRITICAL: Target directory not found: {TARGET_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: All 4 expected ZIP files are present in ~/workshop_materials (0.5 points)
    # This FAILS on initial (empty dir) and PASSES on golden (all files present)
    try:
        present_files = set(os.listdir(TARGET_DIR))
        expected_names = set(EXPECTED_FILES.keys())
        found_names = present_files & expected_names
        missing_names = expected_names - present_files

        if len(found_names) == len(expected_names):
            print(f"PASS: Component 1 — All 4 ZIP files present in workshop_materials ({found_names}) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — Missing ZIP files: {missing_names}, Found: {found_names}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All ZIP files are valid archives with correct internal contents (0.3 points)
    # This FAILS on initial (files don't exist) and PASSES on golden (valid zips with correct contents)
    try:
        valid_count = 0
        for fname, expected in EXPECTED_FILES.items():
            fpath = os.path.join(TARGET_DIR, fname)
            if not os.path.isfile(fpath):
                print(f"FAIL: Component 2 — {fname} not found at {fpath}")
                continue
            try:
                with zipfile.ZipFile(fpath, 'r') as zf:
                    actual_contents = zf.namelist()
                    expected_contents = expected['contents']
                    if set(actual_contents) == set(expected_contents):
                        print(f"PASS: Component 2 — {fname} contains expected: {actual_contents}")
                        valid_count += 1
                    else:
                        print(f"FAIL: Component 2 — {fname} has contents {actual_contents}, expected {expected_contents}")
            except zipfile.BadZipFile:
                print(f"FAIL: Component 2 — {fname} is not a valid ZIP archive")
            except Exception as inner_e:
                print(f"ERROR: Component 2 — {fname}: {inner_e}")

        if valid_count == len(EXPECTED_FILES):
            print(f"PASS: Component 2 — All {valid_count} ZIP files are valid with correct contents (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Only {valid_count}/{len(EXPECTED_FILES)} ZIP files are valid with correct contents")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All ZIP files have correct byte sizes (0.2 points)
    # This FAILS on initial (files don't exist) and PASSES on golden (correct sizes)
    try:
        size_ok_count = 0
        for fname, expected in EXPECTED_FILES.items():
            fpath = os.path.join(TARGET_DIR, fname)
            if not os.path.isfile(fpath):
                print(f"FAIL: Component 3 — {fname} not found")
                continue
            actual_size = os.path.getsize(fpath)
            expected_size = expected['size']
            if actual_size == expected_size:
                print(f"PASS: Component 3 — {fname} size={actual_size} bytes (matches expected)")
                size_ok_count += 1
            else:
                print(f"FAIL: Component 3 — {fname} size={actual_size}, expected={expected_size}")

        if size_ok_count == len(EXPECTED_FILES):
            print(f"PASS: Component 3 — All {size_ok_count} ZIP files have correct sizes (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Only {size_ok_count}/{len(EXPECTED_FILES)} ZIP files have correct sizes")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()

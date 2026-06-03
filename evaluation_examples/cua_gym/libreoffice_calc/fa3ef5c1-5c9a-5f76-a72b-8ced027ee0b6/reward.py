"""
Reward Script: Download all PDF spec sheets from Chrome API docs page into ~/api_docs/
Task ID: osworld_multi_apps_web_download_005
Domain: multi_apps / web_download + os
Scoring:
  Component 1 (0.5 pts): ~/api_docs/ contains exactly the 3 expected PDF files with correct names
  Component 2 (0.5 pts): All 3 files have valid PDF content (correct size: 2781, 2872, 2921 bytes)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_download_005'

# Expected PDF filenames as listed on the API documentation page
EXPECTED_FILES = ['api_v1_spec.pdf', 'api_v2_spec.pdf', 'api_v3_spec.pdf']

# Expected file sizes in bytes (from the source files served by the local web server)
# The task asks to download from the page without renaming, so content should be valid PDFs
EXPECTED_SIZES = {
    'api_v1_spec.pdf': 2781,
    'api_v2_spec.pdf': 2872,
    'api_v3_spec.pdf': 2921,
}


def verify_task(api_docs_dir):
    """
    Verify that all PDF spec files have been downloaded to ~/api_docs/
    with the correct filenames (no renaming).
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: ~/api_docs directory must exist
    if not os.path.isdir(api_docs_dir):
        print(f"CRITICAL: Directory {api_docs_dir} does not exist")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Check that api_docs contains exactly the 3 expected PDF files (0.5 pts)
    # This FAILS on initial_env (api_docs is empty) and PASSES on golden_env
    try:
        actual_files = set(os.listdir(api_docs_dir))
        expected_set = set(EXPECTED_FILES)

        # Check for exact match: all 3 expected files must be present
        missing = expected_set - actual_files
        extra = actual_files - expected_set

        # Award points if all required PDFs are present (extra files do not disqualify)
        all_required_present = len(missing) == 0
        if all_required_present and not extra:
            print(f"PASS: Component 1 — api_docs contains exactly the 3 expected PDF files: {sorted(actual_files)} (0.5 pts)")
            total_score += 0.5
        elif all_required_present and extra:
            # All required files present but extra files exist — still pass
            # since the task says "download all spec PDFs from the current page"
            print(f"PASS: Component 1 — api_docs contains all 3 required PDFs (plus extra files: {sorted(extra)}) (0.5 pts)")
            if all_required_present:
                total_score += 0.5
        else:
            print(f"FAIL: Component 1 — Missing files in api_docs: {sorted(missing)}, found: {sorted(actual_files)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Verify each expected PDF file has valid content (correct size + PDF header) (0.5 pts)
    # This FAILS on initial_env (files don't exist in api_docs) and PASSES on golden_env
    try:
        valid_count = 0
        for fname in EXPECTED_FILES:
            fpath = os.path.join(api_docs_dir, fname)
            if not os.path.isfile(fpath):
                print(f"FAIL: Component 2 — File not found: {fpath}")
                continue

            # Check file size matches expected
            actual_size = os.path.getsize(fpath)
            expected_size = EXPECTED_SIZES[fname]
            if actual_size != expected_size:
                print(f"FAIL: Component 2 — {fname}: size mismatch (expected {expected_size}, got {actual_size})")
                continue

            # Check valid PDF magic bytes (%PDF header)
            with open(fpath, 'rb') as f:
                header = f.read(4)
            if header != b'%PDF':
                print(f"FAIL: Component 2 — {fname}: not a valid PDF (header: {header!r})")
                continue

            print(f"PASS: Component 2 — {fname}: valid PDF, size {actual_size} bytes")
            valid_count += 1

        if valid_count == len(EXPECTED_FILES):
            print(f"PASS: Component 2 — All {len(EXPECTED_FILES)} PDFs are valid with correct sizes (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 — Only {valid_count}/{len(EXPECTED_FILES)} PDFs are valid")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: verify the api_docs directory
api_docs_dir = os.path.join(WORKDIR, 'api_docs')
verify_task(api_docs_dir)

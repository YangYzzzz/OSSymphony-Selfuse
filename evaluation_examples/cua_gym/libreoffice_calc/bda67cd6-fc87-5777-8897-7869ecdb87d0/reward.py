"""
Reward Script: Search for Janet Brooks photos, move to 'janet_brooks' folder, compress as 'janet_brooks.zip'
Task ID: osworld_multi_apps_photo_zip_054
Domain: os (file operations)
Scoring:
  Component 1: 'janet_brooks' folder exists on Desktop with the 4 correct Janet Brooks photos (0.5 pts)
  Component 2: 'janet_brooks.zip' exists on Desktop and contains exactly those same 4 photos (0.5 pts)
  Total: 1.0
"""

import os
import zipfile

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_photo_zip_054'

# Ground truth: the 4 Janet Brooks photos identified in the golden_env artifact
JANET_BROOKS_PHOTOS = {'picnic_02.jpg', 'picnic_05.jpg', 'picnic_08.jpg', 'picnic_11.jpg'}

DESKTOP = os.path.join(WORKDIR, 'Desktop')
JANET_FOLDER = os.path.join(DESKTOP, 'janet_brooks')
JANET_ZIP = os.path.join(DESKTOP, 'janet_brooks.zip')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: Desktop must exist
    if not os.path.isdir(DESKTOP):
        print(f"CRITICAL: Desktop directory not found at {DESKTOP}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: 'janet_brooks' folder exists and contains exactly the correct photos (0.5 pts)
    # This checks that the correct 4 photos are in the janet_brooks folder.
    # FAILS on initial_env (no janet_brooks folder), PASSES on golden_env.
    try:
        if not os.path.isdir(JANET_FOLDER):
            print(f"FAIL: Component 1 — 'janet_brooks' folder not found at {JANET_FOLDER}")
        else:
            actual_files = set(
                f for f in os.listdir(JANET_FOLDER)
                if os.path.isfile(os.path.join(JANET_FOLDER, f))
            )
            if actual_files == JANET_BROOKS_PHOTOS:
                print(f"PASS: Component 1 — 'janet_brooks' folder contains exactly the correct 4 photos: {sorted(actual_files)} (0.5 pts)")
                total_score += 0.5
            else:
                missing = JANET_BROOKS_PHOTOS - actual_files
                extra = actual_files - JANET_BROOKS_PHOTOS
                print(f"FAIL: Component 1 — 'janet_brooks' folder contents mismatch.")
                if missing:
                    print(f"  Missing photos: {sorted(missing)}")
                if extra:
                    print(f"  Unexpected photos: {sorted(extra)}")
                print(f"  Expected: {sorted(JANET_BROOKS_PHOTOS)}, Found: {sorted(actual_files)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 'janet_brooks.zip' exists on Desktop and contains exactly the correct 4 photos (0.5 pts)
    # FAILS on initial_env (no zip file), PASSES on golden_env.
    try:
        if not os.path.isfile(JANET_ZIP):
            print(f"FAIL: Component 2 — 'janet_brooks.zip' not found at {JANET_ZIP}")
        else:
            try:
                with zipfile.ZipFile(JANET_ZIP, 'r') as zf:
                    # Get only file entries (exclude directories)
                    zip_contents = set(
                        name for name in zf.namelist()
                        if not name.endswith('/')
                    )
                    # Normalize: strip any leading directory paths
                    zip_basenames = set(os.path.basename(name) for name in zip_contents)

                    if zip_basenames == JANET_BROOKS_PHOTOS:
                        print(f"PASS: Component 2 — 'janet_brooks.zip' contains exactly the correct 4 photos: {sorted(zip_basenames)} (0.5 pts)")
                        total_score += 0.5
                    else:
                        missing = JANET_BROOKS_PHOTOS - zip_basenames
                        extra = zip_basenames - JANET_BROOKS_PHOTOS
                        print(f"FAIL: Component 2 — 'janet_brooks.zip' contents mismatch.")
                        if missing:
                            print(f"  Missing from zip: {sorted(missing)}")
                        if extra:
                            print(f"  Unexpected in zip: {sorted(extra)}")
                        print(f"  Expected: {sorted(JANET_BROOKS_PHOTOS)}, Found: {sorted(zip_basenames)}")
            except zipfile.BadZipFile as e:
                print(f"FAIL: Component 2 — 'janet_brooks.zip' is not a valid zip file: {e}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

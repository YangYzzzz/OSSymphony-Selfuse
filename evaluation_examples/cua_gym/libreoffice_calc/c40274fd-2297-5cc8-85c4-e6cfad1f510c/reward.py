"""
Reward Script: Download missing wallpapers from GitHub elementary/wallpapers repo
Task ID: osworld_multi_apps_collect_missing_002
Domain: os (file management / web download)

Task: Find wallpapers present in https://github.com/elementary/wallpapers (backgrounds/ folder)
      that are NOT in ~/Pictures/Wallpapers, and download them.

Scoring Rubric:
  - Component 1: Each of the 6 known missing wallpapers is present in ~/Pictures/Wallpapers
                 Partial credit: each file counts as 1/6 of the total score
                 Total: 1.0 (all 6 downloaded) with partial credit per file

The 6 wallpapers that are present in the GitHub repo but MISSING from the initial local state:
  1. Ashim DSilva.jpg
  2. Morskie Oko.jpg
  3. odin-dark.jpg
  4. Photo by SpaceX.jpg
  5. Snow-Capped Mountain.jpg
  6. Sunset by the Pier.jpg
"""

import os

WALLPAPERS_DIR = '/home/user/Pictures/Wallpapers'
TASK_ID = 'osworld_multi_apps_collect_missing_002'

# These are the wallpapers that were in the GitHub repo but MISSING from the initial local state.
# The task is to download these missing files.
MISSING_WALLPAPERS = [
    'Ashim DSilva.jpg',
    'Morskie Oko.jpg',
    'odin-dark.jpg',
    'Photo by SpaceX.jpg',
    'Snow-Capped Mountain.jpg',
    'Sunset by the Pier.jpg',
]

# Per-file score weight
PER_FILE_SCORE = 1.0 / len(MISSING_WALLPAPERS)  # ~0.1667 each


def verify_task():
    """
    Verify that the missing wallpapers have been downloaded to ~/Pictures/Wallpapers.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: Wallpapers directory must exist
    if not os.path.isdir(WALLPAPERS_DIR):
        print(f"CRITICAL: Wallpapers directory does not exist: {WALLPAPERS_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # List the files currently in the wallpapers directory
    try:
        existing_files = set(os.listdir(WALLPAPERS_DIR))
        print(f"INFO: Found {len(existing_files)} files in {WALLPAPERS_DIR}")
    except Exception as e:
        print(f"CRITICAL: Cannot list directory {WALLPAPERS_DIR}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Each missing wallpaper must now be present AND have non-zero file size
    # These files were NOT in the initial env and must have been downloaded by the agent.
    # Each file earns 1/6 of total score (progressive partial credit).
    downloaded_count = 0
    for wallpaper_name in MISSING_WALLPAPERS:
        file_path = os.path.join(WALLPAPERS_DIR, wallpaper_name)
        try:
            if wallpaper_name in existing_files:
                # Verify the file is non-empty (actually downloaded, not a stub)
                size = os.path.getsize(file_path)
                if size > 0:
                    print(f"PASS: '{wallpaper_name}' present with size={size} bytes (+{PER_FILE_SCORE:.4f} pts)")
                    total_score += PER_FILE_SCORE
                    downloaded_count += 1
                else:
                    print(f"FAIL: '{wallpaper_name}' exists but is empty (0 bytes)")
            else:
                print(f"FAIL: '{wallpaper_name}' is missing from {WALLPAPERS_DIR}")
        except Exception as e:
            print(f"ERROR: Could not check '{wallpaper_name}': {e}")

    # Summary
    print(f"\nDownloaded {downloaded_count}/{len(MISSING_WALLPAPERS)} missing wallpapers.")

    final_score = round(min(total_score, 1.0), 4)
    # Normalize: if all 6 are present, ensure exactly 1.0
    if downloaded_count == len(MISSING_WALLPAPERS):
        final_score = 1.0

    print(f"Score: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: run the verification
if not os.path.isdir(WALLPAPERS_DIR):
    print(f"Directory not found: {WALLPAPERS_DIR}")
    print("REWARD: 0.0")
else:
    verify_task()

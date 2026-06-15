"""
Reward Script: Remove VLC Media Library scan path ~/Music/Old_Library/
Task ID: vlc_playlist_073
Domain: vlc
Scoring:
  Component 1 (0.6): Old_Library path removed from media library DB
  Component 2 (0.4): Old_Library removed AND Current path preserved (compound check)
"""

import os
import sqlite3

WORKDIR = '/home/user'
TASK_ID = 'vlc_playlist_073'
ML_DB_PATH = os.path.join(WORKDIR, '.local/share/vlc/medialibrary/ml.db')

def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: ML database must exist
    if not os.path.exists(ML_DB_PATH):
        print(f"CRITICAL: Media library database not found: {ML_DB_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        conn = sqlite3.connect(ML_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT path FROM Folder")
        rows = cursor.fetchall()
        folder_paths = [row[0] for row in rows]
        conn.close()
        print(f"INFO: Found {len(folder_paths)} folder(s) in media library: {folder_paths}")
    except Exception as e:
        print(f"CRITICAL: Cannot read media library database: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Normalize paths for comparison (ensure trailing slash consistency)
    old_library_path = '/home/user/Music/Old_Library/'
    current_path = '/home/user/Music/Current/'

    # Check if Old_Library is present (normalize with and without trailing slash)
    old_library_present = any(
        p.rstrip('/') == old_library_path.rstrip('/')
        for p in folder_paths
    )
    current_present = any(
        p.rstrip('/') == current_path.rstrip('/')
        for p in folder_paths
    )

    # Component 1: Old_Library path is removed from media library (0.6 points)
    # FAILS on initial_env (Old_Library exists) -> PASSES on golden_env (Old_Library removed)
    try:
        if not old_library_present:
            print(f"PASS: Component 1 — Old_Library path not found in media library (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 1 — Old_Library path still present in media library")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Old_Library removed AND Current path preserved (0.4 points)
    # Compound check anchored to the task change
    # FAILS on initial_env (Old_Library present) -> PASSES on golden_env (Old_Library gone, Current kept)
    try:
        if not old_library_present and current_present:
            print(f"PASS: Component 2 — Old_Library removed and Current path preserved (0.4 pts)")
            total_score += 0.4
        else:
            if old_library_present:
                print(f"FAIL: Component 2 — Old_Library still present")
            if not current_present:
                print(f"FAIL: Component 2 — Current path is missing (should be preserved)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()

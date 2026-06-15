"""
Reward Script: Fix tile merge logic in 2048 game
Task ID: osworld_multi_apps_vscode_debug_game_011
Domain: vscode (multi_apps)
Scoring:
  - Component 1 (0.4 pts): board.py _slide_row contains the merge fix
    (calls merge_with and removes merged tile via pop/del)
  - Component 2 (0.3 pts): Unit tests for merge logic all pass
    (test_merge.py run_all() returns 1.0)
  - Component 3 (0.3 pts): Score accumulation in _slide_row
    (self.score += current.value or equivalent)
"""

import os
import sys
import re

WORKDIR = '/home/user/Desktop/game2048'
TASK_ID = 'osworld_multi_apps_vscode_debug_game_011'

BOARD_PY = os.path.join(WORKDIR, 'board.py')
TEST_PY   = os.path.join(WORKDIR, 'test_merge.py')


def verify_task():
    """
    Verify that the tile merge logic bug in board.py has been fixed.
    Returns a float between 0.0 and 1.0.
    """
    total_score = 0.0

    # --- Precondition: board.py must exist ---------------------------------
    if not os.path.exists(BOARD_PY):
        print(f"CRITICAL: board.py not found at {BOARD_PY}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(BOARD_PY, 'r') as f:
            board_src = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read board.py: {e}")
        print("REWARD: 0.0")
        return 0.0

    # -----------------------------------------------------------------------
    # Component 1: _slide_row performs actual merge (0.4 points)
    #
    # The bug was that can_merge_with() was called but merge_with() was never
    # invoked and the merged-away tile was never removed.
    # The fix requires:
    #   (a) a call to merge_with inside the merge branch, AND
    #   (b) removal of the consumed tile (pop or del on tiles list)
    # -----------------------------------------------------------------------
    try:
        has_merge_with_call = bool(re.search(r'\.merge_with\(', board_src))
        # Check for tile removal: tiles.pop(...) or del tiles[...]
        has_tile_removal = bool(
            re.search(r'tiles\.pop\(', board_src) or
            re.search(r'del\s+tiles\[', board_src)
        )

        if has_merge_with_call and has_tile_removal:
            print("PASS: Component 1 — merge_with() is called and merged tile is removed (0.4 pts)")
            total_score += 0.4
        else:
            if not has_merge_with_call:
                print("FAIL: Component 1 — merge_with() is NOT called in board.py")
            if not has_tile_removal:
                print("FAIL: Component 1 — merged tile is NOT removed from the tiles list")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: All unit tests pass (0.3 points)
    #
    # test_merge.py provides run_all() which returns fraction of passed tests.
    # Full score (1.0) is required, meaning all 4 merge tests must pass.
    # -----------------------------------------------------------------------
    try:
        if not os.path.exists(TEST_PY):
            print("FAIL: Component 2 — test_merge.py not found")
        else:
            import importlib.util
            import uuid

            original_cwd = os.getcwd()
            original_path = sys.path.copy()
            module_name = f"test_{uuid.uuid4().hex[:8]}"
            try:
                os.chdir(WORKDIR)
                if WORKDIR not in sys.path:
                    sys.path.insert(0, WORKDIR)
                spec = importlib.util.spec_from_file_location(module_name, TEST_PY)
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                fraction = module.run_all()
                if fraction == 1.0:
                    print(f"PASS: Component 2 — all merge unit tests pass (0.3 pts)")
                    total_score += 0.3
                elif fraction > 0.0:
                    partial = round(0.3 * fraction, 4)
                    print(f"PARTIAL: Component 2 — {fraction:.0%} tests pass; "
                          f"partial credit {partial} pts")
                    # No partial credit awarded — require all tests to pass
                    print("FAIL: Component 2 — not all tests pass; 0 pts awarded")
                else:
                    print(f"FAIL: Component 2 — no merge tests pass ({fraction})")
            except Exception as e:
                print(f"FAIL: Component 2 — test execution error: {e}")
            finally:
                if module_name in sys.modules:
                    del sys.modules[module_name]
                os.chdir(original_cwd)
                sys.path[:] = original_path
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: Score is accumulated during merge (0.3 points)
    #
    # The golden fix adds `self.score += current.value` (or equivalent)
    # inside the merge branch of _slide_row. We check that board.py contains
    # a score increment tied to the merge action.
    # -----------------------------------------------------------------------
    try:
        # Look for score accumulation: self.score += or self.score = self.score +
        has_score_update = bool(
            re.search(r'self\.score\s*\+=', board_src) or
            re.search(r'self\.score\s*=\s*self\.score\s*\+', board_src)
        )

        if has_score_update:
            print("PASS: Component 3 — self.score is updated during merge (0.3 pts)")
            total_score += 0.3
        else:
            print("FAIL: Component 3 — self.score is NOT updated in _slide_row")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -----------------------------------------------------------------------
    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

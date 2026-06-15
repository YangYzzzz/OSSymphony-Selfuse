"""
Reward Script: Fix Python Sudoku Solver RecursionError
Task ID: osworld_multi_apps_vscode_debug_game_010
Domain: vs-code (Python debugging)
Scoring:
  Component 1 (0.4 pts): solver.py _backtrack method correctly propagates recursive return value
  Component 2 (0.3 pts): Solver successfully solves the easy puzzle with a valid solution
  Component 3 (0.3 pts): Solver successfully solves the medium puzzle with a valid solution
Total: 1.0
"""

import os
import sys
import re

WORKDIR = '/home/user/Desktop/sudoku'
TASK_ID = 'osworld_multi_apps_vscode_debug_game_010'
SOLVER_PATH = os.path.join(WORKDIR, 'solver.py')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: solver.py must exist
    if not os.path.exists(SOLVER_PATH):
        print(f"CRITICAL: solver.py not found at {SOLVER_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: _backtrack method correctly propagates recursive return value (0.4 points)
    # The fix requires changing `self._backtrack(board)` to `if self._backtrack(board): return True`
    # so that a successful recursive call terminates further backtracking immediately.
    try:
        with open(SOLVER_PATH, 'r') as f:
            solver_code = f.read()

        # Check that the fixed pattern is present:
        # The return value of _backtrack must be checked (if self._backtrack(board): return True)
        fixed_pattern = re.search(
            r'if\s+self\._backtrack\s*\(\s*board\s*\)\s*:\s*\n\s*return\s+True',
            solver_code
        )

        # Also check that the buggy pattern is absent:
        # The standalone call `self._backtrack(board)` without checking return value
        # We look for lines that call _backtrack without an 'if' guard
        lines = solver_code.split('\n')
        buggy_lines = [
            line.strip() for line in lines
            if re.match(r'^self\._backtrack\s*\(\s*board\s*\)\s*$', line.strip())
        ]
        buggy_pattern_absent = len(buggy_lines) == 0

        if fixed_pattern and buggy_pattern_absent:
            print("PASS: Component 1 — _backtrack return value correctly propagated with 'if self._backtrack(board): return True' (0.4 pts)")
            total_score += 0.4
        else:
            if not fixed_pattern:
                print("FAIL: Component 1 — Missing 'if self._backtrack(board): return True' pattern in solver.py")
            if not buggy_pattern_absent:
                print("FAIL: Component 1 — Buggy pattern 'self._backtrack(board)' (without return propagation) still present")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not read/analyze solver.py: {e}")

    # Component 2: Solver solves easy puzzle and produces a valid solution (0.3 points)
    try:
        # Add the sudoku project to path
        if WORKDIR not in sys.path:
            sys.path.insert(0, WORKDIR)

        # Clear any cached modules to ensure fresh import
        for mod in ['board', 'solver', 'validator']:
            if mod in sys.modules:
                del sys.modules[mod]

        from board import Board
        from solver import Solver
        from validator import Validator

        easy_grid = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9],
        ]

        board_easy = Board(easy_grid)
        solver_easy = Solver()
        v = Validator()

        result_easy = solver_easy.solve(board_easy)
        valid_easy = v.is_valid_solution(board_easy)

        if result_easy and valid_easy:
            print(f"PASS: Component 2 — Easy puzzle solved correctly in {solver_easy.steps} steps (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Easy puzzle: result={result_easy}, valid_solution={valid_easy}")
    except RecursionError as e:
        print(f"FAIL: Component 2 — RecursionError solving easy puzzle: {e}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Solver solves medium puzzle and produces a valid solution (0.3 points)
    try:
        # Clear cached modules again for fresh import
        for mod in ['board', 'solver', 'validator']:
            if mod in sys.modules:
                del sys.modules[mod]

        from board import Board
        from solver import Solver
        from validator import Validator

        medium_grid = [
            [0, 0, 0, 2, 6, 0, 7, 0, 1],
            [6, 8, 0, 0, 7, 0, 0, 9, 0],
            [1, 9, 0, 0, 0, 4, 5, 0, 0],
            [8, 2, 0, 1, 0, 0, 0, 4, 0],
            [0, 0, 4, 6, 0, 2, 9, 0, 0],
            [0, 5, 0, 0, 0, 3, 0, 2, 8],
            [0, 0, 9, 3, 0, 0, 0, 7, 4],
            [0, 4, 0, 0, 5, 0, 0, 3, 6],
            [7, 0, 3, 0, 1, 8, 0, 0, 0],
        ]

        board_med = Board(medium_grid)
        solver_med = Solver()
        v2 = Validator()

        result_med = solver_med.solve(board_med)
        valid_med = v2.is_valid_solution(board_med)

        if result_med and valid_med:
            print(f"PASS: Component 3 — Medium puzzle solved correctly in {solver_med.steps} steps (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — Medium puzzle: result={result_med}, valid_solution={valid_med}")
    except RecursionError as e:
        print(f"FAIL: Component 3 — RecursionError solving medium puzzle: {e}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    # Change to the sudoku project directory so imports work correctly
    os.chdir(WORKDIR)
    verify_task()

"""
Initial Setup: Python Sudoku Solver with buggy backtracking (recursion error)
Task ID: osworld_multi_apps_vscode_debug_game_010
Domain: vs-code (Python debugging)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vscode_debug_game_010'
PROJECT_DIR = f'{WORKDIR}/Desktop/sudoku'


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_initial():
    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # ---- board.py ----
    board_py = '''\
"""
board.py - Sudoku board representation
"""


class Board:
    """Represents a 9x9 Sudoku board."""

    def __init__(self, grid=None):
        if grid is None:
            self.grid = [[0] * 9 for _ in range(9)]
        else:
            # Deep copy the grid
            self.grid = [row[:] for row in grid]

    def get(self, row, col):
        return self.grid[row][col]

    def set(self, row, col, value):
        self.grid[row][col] = value

    def find_empty(self):
        """Return (row, col) of first empty cell (0 means empty), or None if full."""
        for r in range(9):
            for c in range(9):
                if self.grid[r][c] == 0:
                    return (r, c)
        return None

    def __str__(self):
        lines = []
        for i, row in enumerate(self.grid):
            if i % 3 == 0 and i != 0:
                lines.append('------+-------+------')
            line_parts = []
            for j, val in enumerate(row):
                if j % 3 == 0 and j != 0:
                    line_parts.append('|')
                line_parts.append(str(val) if val != 0 else '.')
            lines.append(' '.join(line_parts))
        return '\\n'.join(lines)

    def copy(self):
        return Board(self.grid)
'''

    # ---- validator.py ----
    validator_py = '''\
"""
validator.py - Sudoku move validation
"""


class Validator:
    """Validates Sudoku moves according to game rules."""

    @staticmethod
    def is_valid(board, row, col, num):
        """
        Check if placing `num` at (row, col) is valid.
        Returns True if the move doesn't violate any Sudoku rules.
        """
        # Check row
        if num in board.grid[row]:
            return False

        # Check column
        for r in range(9):
            if board.grid[r][col] == num:
                return False

        # Check 3x3 box
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if board.grid[r][c] == num:
                    return False

        return True

    @staticmethod
    def is_complete(board):
        """Check if the board is completely and correctly filled."""
        for r in range(9):
            for c in range(9):
                if board.grid[r][c] == 0:
                    return False
        return True

    @staticmethod
    def is_valid_solution(board):
        """Verify that the filled board is a valid Sudoku solution."""
        # Check all rows
        for row in board.grid:
            if sorted(row) != list(range(1, 10)):
                return False

        # Check all columns
        for col in range(9):
            column = [board.grid[row][col] for row in range(9)]
            if sorted(column) != list(range(1, 10)):
                return False

        # Check all 3x3 boxes
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box = []
                for r in range(box_row, box_row + 3):
                    for c in range(box_col, box_col + 3):
                        box.append(board.grid[r][c])
                if sorted(box) != list(range(1, 10)):
                    return False

        return True
'''

    # ---- solver.py (BUGGY - missing return in backtracking, causes infinite recursion on hard puzzles) ----
    solver_py = '''\
"""
solver.py - Sudoku solver using backtracking algorithm
BUG: The backtracking function does not return True when a recursive call succeeds,
causing the solver to continue trying after a solution is found, leading to
RecursionError on complex puzzle inputs.
"""

from board import Board
from validator import Validator


class Solver:
    """Solves Sudoku puzzles using recursive backtracking."""

    def __init__(self):
        self.validator = Validator()
        self.steps = 0

    def solve(self, board):
        """
        Solve the puzzle in-place using backtracking.
        Returns True if solved, False if no solution exists.
        """
        self.steps = 0
        return self._backtrack(board)

    def _backtrack(self, board):
        """
        Recursive backtracking solver.
        BUG: Missing `return True` when recursive call succeeds —
        the solver keeps backtracking even after finding a valid solution,
        which causes excessive recursion and RecursionError on hard puzzles.
        """
        empty = board.find_empty()
        if empty is None:
            return True  # Board is complete

        row, col = empty
        self.steps += 1

        for num in range(1, 10):
            if self.validator.is_valid(board, row, col, num):
                board.set(row, col, num)

                # BUG: The return value of the recursive call is not propagated.
                # This causes the solver to undo a correct solution and try more
                # combinations, leading to unbounded recursion on hard puzzles.
                self._backtrack(board)  # BUG: should be: if self._backtrack(board): return True

                board.set(row, col, 0)  # backtrack

        return False
'''

    # ---- main.py ----
    main_py = '''\
"""
main.py - Entry point for the Sudoku solver
Runs solver against multiple test puzzles and reports results.
"""

import sys
from board import Board
from solver import Solver
from validator import Validator


# Test puzzles (0 = empty cell)
PUZZLES = {
    "easy": [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ],
    "medium": [
        [0, 0, 0, 2, 6, 0, 7, 0, 1],
        [6, 8, 0, 0, 7, 0, 0, 9, 0],
        [1, 9, 0, 0, 0, 4, 5, 0, 0],
        [8, 2, 0, 1, 0, 0, 0, 4, 0],
        [0, 0, 4, 6, 0, 2, 9, 0, 0],
        [0, 5, 0, 0, 0, 3, 0, 2, 8],
        [0, 0, 9, 3, 0, 0, 0, 7, 4],
        [0, 4, 0, 0, 5, 0, 0, 3, 6],
        [7, 0, 3, 0, 1, 8, 0, 0, 0],
    ],
    "hard": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 0, 8, 5],
        [0, 0, 1, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 5, 0, 7, 0, 0, 0],
        [0, 0, 4, 0, 0, 0, 1, 0, 0],
        [0, 9, 0, 0, 0, 0, 0, 0, 0],
        [5, 0, 0, 0, 0, 0, 0, 7, 3],
        [0, 0, 2, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 9],
    ],
}


def run_solver(name, grid):
    print(f"\\n{'='*40}")
    print(f"Puzzle: {name}")
    print(f"{'='*40}")
    board = Board(grid)
    print("Initial board:")
    print(board)
    print()

    solver = Solver()
    result = solver.solve(board)

    if result:
        print(f"Solved in {solver.steps} steps:")
        print(board)
        validator = Validator()
        if validator.is_valid_solution(board):
            print(f"[PASS] Valid solution for {name} puzzle!")
        else:
            print(f"[FAIL] Solution is invalid for {name} puzzle!")
    else:
        print(f"[FAIL] Could not solve {name} puzzle.")
    return result


def main():
    print("Sudoku Solver - Backtracking Algorithm")
    print("=" * 40)

    all_passed = True
    for name, grid in PUZZLES.items():
        try:
            result = run_solver(name, grid)
            if not result:
                all_passed = False
        except RecursionError as e:
            print(f"\\n[ERROR] RecursionError on {name} puzzle: {e}")
            print("The backtracking algorithm has a bug causing infinite recursion.")
            all_passed = False
        except Exception as e:
            print(f"\\n[ERROR] Unexpected error on {name} puzzle: {e}")
            all_passed = False

    print("\\n" + "=" * 40)
    if all_passed:
        print("All puzzles solved successfully!")
    else:
        print("Some puzzles failed. Please check the solver implementation.")
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
'''

    # Write all files
    files = {
        'board.py': board_py,
        'validator.py': validator_py,
        'solver.py': solver_py,
        'main.py': main_py,
    }

    for filename, content in files.items():
        filepath = os.path.join(PROJECT_DIR, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f'Created: {filepath}')

    print(f'\nSudoku project created at: {PROJECT_DIR}')
    print('Files: board.py, validator.py, solver.py (buggy), main.py')

    # GUI-ready startup: open VSCode with the sudoku project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    # Also open solver.py in the editor (the file to be fixed)
    launch_gui(f'code "{PROJECT_DIR}/solver.py"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

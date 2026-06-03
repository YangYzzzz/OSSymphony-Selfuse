"""
Initial Setup: Maze generator project with a connectivity bug for VSCode debugging
Task ID: osworld_multi_apps_vscode_debug_game_013
Domain: multi_apps (VSCode + Python)

Creates a Python maze generator project at /home/user/Desktop/maze_gen/ with:
- cell.py: Cell class
- generator.py: Maze generator with a BUG (early termination via max_visits guard
                 that stops after visiting only half the grid, leaving remaining
                 cells disconnected)
- renderer.py: ASCII maze renderer
- main.py: Entry point
- test_connectivity.py: Unit tests that verify all cells are reachable (FAIL initially)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT_DIR = '/home/user/Desktop/maze_gen'


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

    # --- cell.py ---
    cell_py = '''\
"""
cell.py - Represents a single cell in the maze grid.
"""


class Cell:
    """A single cell in the maze grid.

    Attributes:
        row (int): Row index of the cell (0-based).
        col (int): Column index of the cell (0-based).
        walls (dict): Which walls are present. Keys: 'N', 'S', 'E', 'W'.
        visited (bool): Whether this cell has been visited during generation.
    """

    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}
        self.visited = False

    def remove_wall(self, direction: str):
        """Remove the wall in the given direction."""
        self.walls[direction] = False

    def has_wall(self, direction: str) -> bool:
        """Return True if the wall in the given direction is present."""
        return self.walls[direction]

    def __repr__(self):
        return f"Cell({self.row}, {self.col}, visited={self.visited})"
'''

    # --- generator.py with a BUG ---
    # Bug: A "safety guard" max_visits counter limits the DFS to visiting
    # only rows*cols//2 cells, leaving the other half disconnected.
    # This looks like a well-intentioned anti-infinite-loop guard but
    # terminates the generation too early.
    generator_py = '''\
"""
generator.py - Recursive backtracking maze generator.

Uses depth-first search (DFS) with a stack to carve passages
through a grid of cells. Each cell starts fully walled; the
algorithm removes walls between adjacent cells to create a
connected maze.
"""

import random
from cell import Cell


# Mapping: direction -> (row_delta, col_delta)
DIRECTIONS = {
    'N': (-1, 0),
    'S': (1, 0),
    'E': (0, 1),
    'W': (0, -1),
}

# Mapping: direction -> opposite direction (used when removing walls)
OPPOSITE = {
    'N': 'S',
    'S': 'N',
    'E': 'W',
    'W': 'E',
}


def generate_maze(rows: int, cols: int, seed: int = None) -> list:
    """Generate a maze using iterative DFS (recursive backtracking).

    Args:
        rows: Number of rows in the maze grid.
        cols: Number of columns in the maze grid.
        seed: Optional random seed for reproducibility.

    Returns:
        2D list of Cell objects representing the completed maze.
    """
    if seed is not None:
        random.seed(seed)

    # Create grid of cells
    grid = [[Cell(r, c) for c in range(cols)] for r in range(rows)]

    # Start from top-left cell
    start = grid[0][0]
    start.visited = True

    stack = [start]

    # Safety guard: prevent infinite loops in degenerate grids.
    # BUG: This guard limits total visits to rows*cols//2, so the DFS
    # terminates after visiting only half the cells, leaving the remaining
    # cells unreachable (no passages carved into them).
    max_visits = (rows * cols) // 2
    visits = 1

    while stack and visits < max_visits:
        current = stack[-1]
        row, col = current.row, current.col

        # Find unvisited neighbours
        neighbours = []
        for direction, (dr, dc) in DIRECTIONS.items():
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbour = grid[nr][nc]
                if not neighbour.visited:
                    neighbours.append((direction, neighbour))

        if neighbours:
            direction, chosen = random.choice(neighbours)
            # Remove wall between current and chosen
            current.remove_wall(direction)
            opp = OPPOSITE[direction]
            chosen.remove_wall(opp)

            # Mark chosen as visited and push to stack
            chosen.visited = True
            visits += 1
            stack.append(chosen)
        else:
            stack.pop()

    return grid
'''

    # --- renderer.py ---
    renderer_py = '''\
"""
renderer.py - ASCII renderer for the maze grid.

Converts a 2D grid of Cell objects into a printable
ASCII string representation.
"""

from cell import Cell


def render_maze(grid: list) -> str:
    """Render a maze grid as an ASCII string.

    Uses '+', '-', '|', and ' ' characters to represent walls and passages.

    Args:
        grid: 2D list of Cell objects (rows x cols).

    Returns:
        Multi-line string representation of the maze.
    """
    rows = len(grid)
    cols = len(grid[0])
    lines = []

    # Top border
    top = '+'
    for c in range(cols):
        top += '---+'
    lines.append(top)

    for r in range(rows):
        # Row with E/W walls
        row_line = '|'
        for c in range(cols):
            cell = grid[r][c]
            row_line += '   '
            row_line += '|' if cell.has_wall('E') else ' '
        lines.append(row_line)

        # Row with N/S walls (bottom of this row)
        bottom_line = '+'
        for c in range(cols):
            cell = grid[r][c]
            bottom_line += '---+' if cell.has_wall('S') else '   +'
        lines.append(bottom_line)

    return '\\n'.join(lines)


def print_maze(grid: list):
    """Print the maze to stdout."""
    print(render_maze(grid))
'''

    # --- main.py ---
    main_py = '''\
"""
main.py - Entry point for the maze generator.

Generates a maze and renders it to the terminal.
"""

from generator import generate_maze
from renderer import print_maze


def main():
    rows, cols = 10, 15
    seed = 42

    print(f"Generating {rows}x{cols} maze (seed={seed})...")
    grid = generate_maze(rows, cols, seed=seed)
    print_maze(grid)
    print("Done.")


if __name__ == "__main__":
    main()
'''

    # --- test_connectivity.py ---
    test_connectivity_py = '''\
"""
test_connectivity.py - Unit tests for maze connectivity.

Tests that every cell in the generated maze is reachable
from the starting cell (top-left corner).
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generator import generate_maze
from collections import deque


def get_reachable_cells(grid: list) -> set:
    """BFS from top-left to find all reachable cells.

    Args:
        grid: 2D list of Cell objects.

    Returns:
        Set of (row, col) tuples for all reachable cells.
    """
    rows = len(grid)
    cols = len(grid[0])
    visited = set()
    queue = deque()

    # Start BFS from (0, 0)
    start = (0, 0)
    queue.append(start)
    visited.add(start)

    directions = {
        'N': (-1, 0),
        'S': (1, 0),
        'E': (0, 1),
        'W': (0, -1),
    }

    while queue:
        r, c = queue.popleft()
        cell = grid[r][c]

        for direction, (dr, dc) in directions.items():
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                # Can move to neighbour only if no wall in that direction
                if not cell.has_wall(direction) and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc))

    return visited


def test_connectivity_small():
    """Test that a small 5x5 maze is fully connected."""
    grid = generate_maze(5, 5, seed=1)
    rows, cols = len(grid), len(grid[0])
    total_cells = rows * cols
    reachable = get_reachable_cells(grid)
    assert len(reachable) == total_cells, (
        f"5x5 maze: only {len(reachable)}/{total_cells} cells reachable!"
    )


def test_connectivity_medium():
    """Test that a medium 10x15 maze is fully connected."""
    grid = generate_maze(10, 15, seed=42)
    rows, cols = len(grid), len(grid[0])
    total_cells = rows * cols
    reachable = get_reachable_cells(grid)
    assert len(reachable) == total_cells, (
        f"10x15 maze: only {len(reachable)}/{total_cells} cells reachable!"
    )


def test_connectivity_multiple_seeds():
    """Test connectivity across multiple random seeds."""
    for seed in [0, 7, 13, 99, 256]:
        grid = generate_maze(8, 8, seed=seed)
        rows, cols = len(grid), len(grid[0])
        total_cells = rows * cols
        reachable = get_reachable_cells(grid)
        assert len(reachable) == total_cells, (
            f"8x8 maze (seed={seed}): only {len(reachable)}/{total_cells} cells reachable!"
        )


if __name__ == "__main__":
    import traceback
    tests = [
        test_connectivity_small,
        test_connectivity_medium,
        test_connectivity_multiple_seeds,
    ]
    passed = 0
    failed = 0
    for test_fn in tests:
        try:
            test_fn()
            print(f"PASS: {test_fn.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"FAIL: {test_fn.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"ERROR: {test_fn.__name__}: {e}")
            traceback.print_exc()
            failed += 1
    print(f"\\nResults: {passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)
'''

    # Write all files
    files = {
        'cell.py': cell_py,
        'generator.py': generator_py,
        'renderer.py': renderer_py,
        'main.py': main_py,
        'test_connectivity.py': test_connectivity_py,
    }

    for filename, content in files.items():
        filepath = os.path.join(PROJECT_DIR, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f'Created: {filepath}')

    print(f'Maze project created at: {PROJECT_DIR}')
    print('Bug: generator.py has max_visits = rows*cols//2 causing early termination')
    print('     Tests will FAIL because ~50% of cells are unreachable from start')

    # GUI-ready startup: open VSCode with the maze_gen folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with maze_gen folder, DISPLAY=:0')


create_initial()

"""
Reward Script: Fix maze generator so every cell is reachable
Task ID: osworld_multi_apps_vscode_debug_game_013
Domain: vs-code / python debugging

Scoring rubric (total = 1.0):
  Component 1: generator.py no longer contains the broken max_visits guard (0.4 pts)
  Component 2: Small 5x5 maze is fully connected — all 25 cells reachable (0.3 pts)
  Component 3: Multiple maze sizes/seeds are all fully connected (0.3 pts)
"""

import os
import sys

WORKDIR = '/home/user/Desktop/maze_gen'
TASK_ID = 'osworld_multi_apps_vscode_debug_game_013'

# Add the maze project directory to the path so we can import its modules
sys.path.insert(0, WORKDIR)


def get_reachable_cells(grid: list) -> set:
    """BFS from top-left (0,0) to find all reachable cells.

    Traverses via cell walls (Cell.has_wall) to determine valid moves.
    Returns a set of (row, col) tuples.
    """
    from collections import deque

    rows = len(grid)
    cols = len(grid[0])
    visited = set()
    queue = deque()

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
                if not cell.has_wall(direction) and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc))

    return visited


def verify_task():
    """
    Verify that the maze generator bug has been fixed.
    Returns a float between 0.0 and 1.0.
    """
    total_score = 0.0

    # --- Precondition gate: generator.py must exist ---
    generator_path = os.path.join(WORKDIR, 'generator.py')
    if not os.path.isfile(generator_path):
        print(f"CRITICAL: generator.py not found at {generator_path}")
        print("REWARD: 0.0")
        return 0.0

    # --- Component 1: Broken max_visits guard removed (0.4 points) ---
    # The original bug used `max_visits = (rows * cols) // 2` and
    # `while stack and visits < max_visits:` to artificially cap DFS traversal,
    # causing only ~50% of cells to be carved. The fix removes this guard so
    # the DFS runs until the stack is empty (standard recursive backtracking).
    try:
        with open(generator_path, 'r') as f:
            generator_code = f.read()

        has_max_visits_var = 'max_visits' in generator_code
        has_visits_counter = ('visits < max_visits' in generator_code or
                              'visits <= max_visits' in generator_code)

        if not has_max_visits_var and not has_visits_counter:
            print(f"PASS: Component 1 — broken max_visits guard is absent from generator.py (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — generator.py still contains 'max_visits' or visit-count guard")
            print(f"  Hint: Remove the max_visits variable and the 'visits < max_visits' condition.")
    except Exception as e:
        print(f"ERROR: Component 1 — could not read generator.py: {e}")

    # --- Precondition gate: import generate_maze ---
    try:
        # Force fresh import (avoid cached broken version)
        if 'generator' in sys.modules:
            del sys.modules['generator']
        if 'cell' in sys.modules:
            del sys.modules['cell']

        from generator import generate_maze
    except Exception as e:
        print(f"CRITICAL: Cannot import generate_maze from generator.py: {e}")
        print(f"Score so far: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # --- Component 2: Small 5x5 maze is fully connected (0.3 points) ---
    # With the original bug, a 5x5 maze has max_visits = 25//2 = 12,
    # so only 12/25 cells would be reachable. The fix must allow all 25.
    try:
        grid = generate_maze(5, 5, seed=1)
        rows, cols = len(grid), len(grid[0])
        total_cells = rows * cols
        reachable = get_reachable_cells(grid)
        reachable_count = len(reachable)

        if reachable_count == total_cells:
            print(f"PASS: Component 2 — 5x5 maze fully connected: {reachable_count}/{total_cells} cells reachable (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — 5x5 maze not fully connected: {reachable_count}/{total_cells} cells reachable")
    except Exception as e:
        print(f"ERROR: Component 2 — 5x5 maze test failed: {e}")

    # --- Component 3: Multiple maze sizes and seeds are all fully connected (0.3 points) ---
    # Verifies the fix generalises across sizes (10x15) and different random seeds.
    # The original bug affects all mazes equally since max_visits = rows*cols//2.
    try:
        failures = []

        test_cases = [
            (10, 15, 42),   # medium maze
            (8,  8,  0),    # different seed
            (8,  8,  7),
            (8,  8,  13),
            (8,  8,  99),
            (8,  8,  256),
        ]

        for r, c, seed in test_cases:
            # Re-import to avoid any module-level state bleeding between runs
            if 'generator' in sys.modules:
                del sys.modules['generator']
            if 'cell' in sys.modules:
                del sys.modules['cell']
            from generator import generate_maze as gm
            grid = gm(r, c, seed=seed)
            total_cells = r * c
            reachable = get_reachable_cells(grid)
            if len(reachable) != total_cells:
                failures.append(f"{r}x{c} seed={seed}: {len(reachable)}/{total_cells}")

        if len(failures) == 0:
            print(f"PASS: Component 3 — all {len(test_cases)} multi-seed/size mazes fully connected (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — some mazes not fully connected: {failures}")
    except Exception as e:
        print(f"ERROR: Component 3 — multi-seed connectivity test failed: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.1f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

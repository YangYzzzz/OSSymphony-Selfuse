"""
Reward Script: Fix maze game bugs and add get_position() method
Task ID: osworld_multi_apps_code_python_game_009
Domain: multi_apps / python code
Scoring:
  Component 1 (0.35): player.py move() accepts direction string (not dx,dy integers)
  Component 2 (0.25): player.py has get_position() method returning (x, y) tuple
  Component 3 (0.20): maze.py is_wall() off-by-one bug removed (no extra boundary shrink)
  Component 4 (0.20): main.py uses player.get_position() to display current position
  Total: 1.0
"""

import os
import ast

WORKDIR = '/home/user/projects/maze_game'
TASK_ID = 'osworld_multi_apps_code_python_game_009'


def read_file(path):
    """Read and return file content; return None if not found."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"ERROR: Cannot read {path}: {e}")
        return None


def check_move_accepts_direction_string(player_code):
    """
    Component 1: Verify player.py move() accepts a direction string.
    Initial state: move(self, dx: int, dy: int) — two integer parameters.
    Fixed state: move(self, direction: str) — single string parameter.
    Returns True only if the signature has one non-self param that is NOT dx or dy.
    """
    try:
        tree = ast.parse(player_code)
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == 'Player':
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name == 'move':
                        params = [arg.arg for arg in item.args.args if arg.arg != 'self']
                        # Fixed: single param not named dx/dy
                        if len(params) == 1 and params[0] not in ('dx', 'dy'):
                            return True, f"move() has 1 param: '{params[0]}' (not dx/dy)"
                        # Buggy: two params dx, dy
                        return False, f"move() has params {params} — still uses dx/dy signature"
    except SyntaxError as se:
        return False, f"SyntaxError: {se}"
    except Exception as e:
        return False, f"Error: {e}"
    return False, "Player.move() not found in player.py"


def check_get_position_method(player_code):
    """
    Component 2: Verify player.py has get_position() returning (x, y).
    Initial state: no get_position() method at all.
    Fixed state: get_position() method present and returns self.x, self.y.
    """
    try:
        tree = ast.parse(player_code)
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == 'Player':
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name == 'get_position':
                        # Method exists — check it returns something involving self.x or self.y
                        for stmt in ast.walk(item):
                            if isinstance(stmt, ast.Return) and stmt.value is not None:
                                ret_dump = ast.dump(stmt.value)
                                if 'self' in ret_dump:
                                    return True, "get_position() method found, returns self.x/y"
                        return True, "get_position() method found"
                return False, "Player class found but no get_position() method"
    except SyntaxError as se:
        return False, f"SyntaxError: {se}"
    except Exception as e:
        return False, f"Error: {e}"
    return False, "Player class not found in player.py"


def check_maze_offbyone_fixed(maze_code):
    """
    Component 3: Verify maze.py is_wall() no longer has the off-by-one shrink.
    Initial state: extra check 'if x >= self.cols - 1 or y >= self.rows - 1: return True'
    Fixed state: that extra check removed — only the standard bounds + grid lookup remain.
    """
    try:
        tree = ast.parse(maze_code)
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == 'Maze':
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name == 'is_wall':
                        # Check for BinOp with Sub and Constant(1) referencing cols/rows
                        for subnode in ast.walk(item):
                            if isinstance(subnode, ast.BinOp) and isinstance(subnode.op, ast.Sub):
                                if isinstance(subnode.right, ast.Constant) and subnode.right.value == 1:
                                    left_dump = ast.dump(subnode.left)
                                    if 'cols' in left_dump or 'rows' in left_dump:
                                        return False, "is_wall() still contains (cols-1)/(rows-1) off-by-one shrink"
                        return True, "is_wall() has no off-by-one boundary shrink"
        return False, "Maze.is_wall() not found"
    except SyntaxError as se:
        return False, f"SyntaxError: {se}"
    except Exception as e:
        return False, f"Error: {e}"


def check_main_uses_get_position(main_code):
    """
    Component 4: Verify main.py calls player.get_position() and displays it.
    Initial state: main.py never calls get_position().
    Fixed state: main.py calls player.get_position() and prints position.
    """
    try:
        tree = ast.parse(main_code)
        get_pos_calls = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr == 'get_position':
                        get_pos_calls += 1

        if get_pos_calls == 0:
            return False, "main.py does not call player.get_position()"

        # Also verify 'position' or 'pos' appears in a print context
        if 'get_position' in main_code and ('position' in main_code.lower() or 'pos' in main_code.lower()):
            return True, f"main.py calls get_position() {get_pos_calls} time(s) and references position display"
        return True, f"main.py calls get_position() {get_pos_calls} time(s)"

    except SyntaxError as se:
        return False, f"SyntaxError: {se}"
    except Exception as e:
        return False, f"Error: {e}"


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    player_path = os.path.join(WORKDIR, 'player.py')
    maze_path = os.path.join(WORKDIR, 'maze.py')
    main_path = os.path.join(WORKDIR, 'main.py')

    # Precondition: all three files must exist
    for fpath in [player_path, maze_path, main_path]:
        if not os.path.isfile(fpath):
            print(f"CRITICAL: Required file not found: {fpath}")
            print("REWARD: 0.0")
            return 0.0

    player_code = read_file(player_path)
    maze_code = read_file(maze_path)
    main_code = read_file(main_path)

    if player_code is None or maze_code is None or main_code is None:
        print("CRITICAL: Could not read one or more source files")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: player.py move() accepts direction string (0.35 points)
    # FAILS on initial (move has dx,dy params), PASSES on golden (direction string param)
    try:
        passed, detail = check_move_accepts_direction_string(player_code)
        if passed:
            print(f"PASS: Component 1 — {detail} (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — {detail}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: player.py has get_position() method (0.25 points)
    # FAILS on initial (no get_position), PASSES on golden
    try:
        passed, detail = check_get_position_method(player_code)
        if passed:
            print(f"PASS: Component 2 — {detail} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — {detail}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: maze.py is_wall() off-by-one bug removed (0.20 points)
    # FAILS on initial (extra boundary shrink present), PASSES on golden
    try:
        passed, detail = check_maze_offbyone_fixed(maze_code)
        if passed:
            print(f"PASS: Component 3 — {detail} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — {detail}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: main.py calls player.get_position() and displays position (0.20 points)
    # FAILS on initial (no get_position call), PASSES on golden
    try:
        passed, detail = check_main_uses_get_position(main_code)
        if passed:
            print(f"PASS: Component 4 — {detail} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — {detail}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint: verify game files at canonical path
if not os.path.isdir(WORKDIR):
    print(f"CRITICAL: Project directory not found: {WORKDIR}")
    print("REWARD: 0.0")
else:
    verify_task()

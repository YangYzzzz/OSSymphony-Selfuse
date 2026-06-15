"""
Initial Setup: Maze game Python project with bugs to fix
Task ID: osworld_multi_apps_code_python_game_009
Domain: multi_apps / code / python

Creates the initial buggy state of the maze game project:
  - main.py calls player.move(direction_string) [wrong signature]
  - maze.py has off-by-one wall check bug (>= instead of >)
  - player.py has move(dx, dy) but no get_position() method
"""

import os
import shlex
import subprocess
import time
from pathlib import Path

WORKDIR = '/home/user'
PROJECT_DIR = f'{WORKDIR}/projects/maze_game'

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
    # Create the project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # -----------------------------------------------------------------------
    # player.py — defines Player class with move(dx, dy) but NO get_position()
    # main.py calls move(direction_string), so this causes AttributeError
    # -----------------------------------------------------------------------
    player_py = '''\
"""
player.py — Player class for the maze game.
"""


class Player:
    def __init__(self, start_x: int, start_y: int):
        self.x = start_x
        self.y = start_y

    def move(self, dx: int, dy: int):
        """Move the player by (dx, dy) offset."""
        self.x += dx
        self.y += dy

    def __repr__(self):
        return f"Player(x={self.x}, y={self.y})"
'''
    Path(f'{PROJECT_DIR}/player.py').write_text(player_py)

    # -----------------------------------------------------------------------
    # maze.py — Maze class with off-by-one wall check bug.
    # is_wall() uses >= for upper-bound check instead of >
    # causing valid moves to be blocked at the last interior cell.
    # -----------------------------------------------------------------------
    maze_py = '''\
"""
maze.py — Maze class for the maze game.
"""


class Maze:
    def __init__(self):
        # 0 = open path, 1 = wall
        self.grid = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 1, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

    def is_wall(self, x: int, y: int) -> bool:
        """Return True if (x, y) is a wall or out of bounds."""
        # BUG: upper bound uses >= instead of > causing off-by-one error
        if x < 0 or y < 0 or x >= self.cols or y >= self.rows:
            return True
        # BUG: boundary check is one cell too restrictive
        if x >= self.cols - 1 or y >= self.rows - 1:
            return True
        return self.grid[y][x] == 1

    def display(self, player_x: int, player_y: int):
        """Print the maze with the player position shown as P."""
        for row_idx, row in enumerate(self.grid):
            row_str = ''
            for col_idx, cell in enumerate(row):
                if col_idx == player_x and row_idx == player_y:
                    row_str += 'P '
                elif cell == 1:
                    row_str += '# '
                else:
                    row_str += '. '
            print(row_str)
'''
    Path(f'{PROJECT_DIR}/maze.py').write_text(maze_py)

    # -----------------------------------------------------------------------
    # main.py — Game loop that calls player.move(direction_string)
    # This does NOT match player.py's move(dx, dy) signature → AttributeError
    # Also does NOT call get_position() since that method doesn't exist yet.
    # -----------------------------------------------------------------------
    main_py = '''\
"""
main.py — Entry point for the maze game.
"""

from maze import Maze
from player import Player


def main():
    maze = Maze()
    player = Player(start_x=1, start_y=1)

    print("Maze Game — use w/a/s/d to move, q to quit")
    print()
    maze.display(player.x, player.y)

    move_count = 0
    while True:
        direction = input("Move (w=up, s=down, a=left, d=right, q=quit): ").strip().lower()

        if direction == 'q':
            print("Thanks for playing!")
            break

        # BUG: Player.move() expects (dx, dy) integers, but we pass a string.
        # This causes: TypeError: move() takes 3 positional arguments but 2 were given
        player.move(direction)
        move_count += 1

        maze.display(player.x, player.y)
        print(f"Moves made: {move_count}")

        if move_count >= 5:
            print("You have completed 5 moves!")
            break


if __name__ == "__main__":
    main()
'''
    Path(f'{PROJECT_DIR}/main.py').write_text(main_py)

    print(f'Project created at: {PROJECT_DIR}')
    print(f'  main.py   - calls player.move(direction_string) [BUG: wrong arg type]')
    print(f'  maze.py   - off-by-one wall check bug (>= instead of >)')
    print(f'  player.py - has move(dx,dy) but no get_position() method')

    # GUI-ready startup: open a terminal showing the project files
    # The agent should use a text editor or terminal to fix the code
    launch_gui(f'nautilus "{PROJECT_DIR}"', delay_sec=1.5)
    # Also open main.py in a text editor so the agent can immediately start editing
    launch_gui(f'gedit "{PROJECT_DIR}/main.py" "{PROJECT_DIR}/player.py" "{PROJECT_DIR}/maze.py"', delay_sec=2.0)
    print('GUI_READY: launched nautilus and gedit with project files (DISPLAY=:0)')


create_initial()

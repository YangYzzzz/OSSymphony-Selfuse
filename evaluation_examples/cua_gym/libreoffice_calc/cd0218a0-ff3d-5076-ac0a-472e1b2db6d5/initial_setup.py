"""
Initial Setup: 2048 game with broken tile merge logic
Task ID: osworld_multi_apps_vscode_debug_game_011
Domain: multi_apps / vscode
Description: Create a 2048 game project with a bug in the tile merge logic
  so that tiles do NOT merge when they collide. The agent must fix this.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
GAME_DIR = '/home/user/Desktop/game2048'


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
    # Create game directory
    os.makedirs(GAME_DIR, exist_ok=True)

    # ── tile.py ──────────────────────────────────────────────────────────────
    tile_py = '''\
"""Represents a single tile on the 2048 board."""


class Tile:
    def __init__(self, value: int):
        self.value = value
        self.merged = False  # Prevents a tile from merging more than once per move

    def __repr__(self):
        return f"Tile({self.value})"

    def can_merge_with(self, other: "Tile") -> bool:
        """Return True if this tile can merge with another tile."""
        return (
            other is not None
            and not self.merged
            and not other.merged
            and self.value == other.value
        )

    def merge_with(self, other: "Tile") -> None:
        """Merge another tile into this one, doubling this tile\'s value."""
        self.value *= 2
        self.merged = True
'''

    # ── board.py (BROKEN merge logic) ────────────────────────────────────────
    # BUG: In _slide_row, the merge step is missing the actual merge call.
    # The code checks whether two adjacent tiles could merge, but instead of
    # calling tile.merge_with(next_tile), it simply skips to the next position
    # without merging.  As a result tiles accumulate without ever combining.
    board_py = '''\
"""Manages the 4×4 game board and slide/merge operations."""

import random
from tile import Tile


BOARD_SIZE = 4


class Board:
    def __init__(self):
        self.grid: list[list[Tile | None]] = [
            [None] * BOARD_SIZE for _ in range(BOARD_SIZE)
        ]
        self.score = 0
        self._spawn_tile()
        self._spawn_tile()

    # ------------------------------------------------------------------ #
    #  Tile spawning                                                       #
    # ------------------------------------------------------------------ #

    def _empty_cells(self) -> list[tuple[int, int]]:
        return [
            (r, c)
            for r in range(BOARD_SIZE)
            for c in range(BOARD_SIZE)
            if self.grid[r][c] is None
        ]

    def _spawn_tile(self) -> None:
        empty = self._empty_cells()
        if not empty:
            return
        r, c = random.choice(empty)
        self.grid[r][c] = Tile(4 if random.random() < 0.1 else 2)

    # ------------------------------------------------------------------ #
    #  Core slide logic                                                    #
    # ------------------------------------------------------------------ #

    def _slide_row(self, row: list[Tile | None]) -> list[Tile | None]:
        """Slide a single row to the left, merging equal adjacent tiles.

        Steps
        -----
        1. Compact non-None tiles to the front.
        2. Merge adjacent pairs with equal values.
        3. Compact again to fill gaps left by merges.
        """
        # Step 1 – compact
        tiles = [t for t in row if t is not None]

        # Step 2 – merge
        i = 0
        while i < len(tiles) - 1:
            current = tiles[i]
            nxt = tiles[i + 1]
            # BUG: merge condition is checked but merge is never performed.
            # The `if` block below is supposed to call current.merge_with(nxt)
            # and remove nxt from the list, but instead it just increments i,
            # leaving both tiles unchanged.
            if current.can_merge_with(nxt):
                i += 2   # <-- BUG: skips merge; should merge and remove nxt
            else:
                i += 1

        # Step 3 – compact again
        tiles = [t for t in tiles if t is not None]
        # Pad with None to restore original length
        return tiles + [None] * (BOARD_SIZE - len(tiles))

    def _reset_merged_flags(self) -> None:
        for row in self.grid:
            for tile in row:
                if tile is not None:
                    tile.merged = False

    # ------------------------------------------------------------------ #
    #  Directional moves                                                   #
    # ------------------------------------------------------------------ #

    def _transpose(self) -> None:
        self.grid = [list(row) for row in zip(*self.grid)]

    def _reverse_rows(self) -> None:
        for row in self.grid:
            row.reverse()

    def _apply_slide(self) -> bool:
        """Apply _slide_row to every row; return True if board changed."""
        changed = False
        for r in range(BOARD_SIZE):
            original = self.grid[r][:]
            self.grid[r] = self._slide_row(self.grid[r])
            if self.grid[r] != original:
                changed = True
        return changed

    def move_left(self) -> bool:
        self._reset_merged_flags()
        changed = self._apply_slide()
        if changed:
            self._spawn_tile()
        return changed

    def move_right(self) -> bool:
        self._reset_merged_flags()
        self._reverse_rows()
        changed = self._apply_slide()
        self._reverse_rows()
        if changed:
            self._spawn_tile()
        return changed

    def move_up(self) -> bool:
        self._reset_merged_flags()
        self._transpose()
        changed = self._apply_slide()
        self._transpose()
        if changed:
            self._spawn_tile()
        return changed

    def move_down(self) -> bool:
        self._reset_merged_flags()
        self._transpose()
        self._reverse_rows()
        changed = self._apply_slide()
        self._reverse_rows()
        self._transpose()
        if changed:
            self._spawn_tile()
        return changed

    # ------------------------------------------------------------------ #
    #  Win / lose detection                                                #
    # ------------------------------------------------------------------ #

    def has_won(self) -> bool:
        return any(
            self.grid[r][c] is not None and self.grid[r][c].value == 2048
            for r in range(BOARD_SIZE)
            for c in range(BOARD_SIZE)
        )

    def has_moves(self) -> bool:
        if self._empty_cells():
            return True
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE - 1):
                if self.grid[r][c].value == self.grid[r][c + 1].value:
                    return True
        for c in range(BOARD_SIZE):
            for r in range(BOARD_SIZE - 1):
                if self.grid[r][c].value == self.grid[r + 1][c].value:
                    return True
        return False

    # ------------------------------------------------------------------ #
    #  Display                                                             #
    # ------------------------------------------------------------------ #

    def __str__(self) -> str:
        lines = []
        for row in self.grid:
            lines.append(
                " | ".join(
                    f"{t.value:4d}" if t is not None else "   ." for t in row
                )
            )
        return "\\n".join(lines)
'''

    # ── game.py ──────────────────────────────────────────────────────────────
    game_py = '''\
"""High-level game controller tying Board to user input."""

from board import Board


KEY_MAP = {
    "a": "left",
    "d": "right",
    "w": "up",
    "s": "down",
    "left":  "left",
    "right": "right",
    "up":    "up",
    "down":  "down",
}


class Game:
    def __init__(self):
        self.board = Board()
        self.over = False
        self.won = False

    def process_key(self, key: str) -> bool:
        """Handle one keypress.  Returns True if the move changed the board."""
        direction = KEY_MAP.get(key.lower())
        if direction is None:
            return False
        move_fn = getattr(self.board, f"move_{direction}")
        changed = move_fn()
        if self.board.has_won():
            self.won = True
            self.over = True
        elif not self.board.has_moves():
            self.over = True
        return changed

    def get_board(self) -> Board:
        return self.board

    def get_score(self) -> int:
        return self.board.score

    def is_over(self) -> bool:
        return self.over

    def is_won(self) -> bool:
        return self.won
'''

    # ── main.py ──────────────────────────────────────────────────────────────
    main_py = '''\
"""Entry point for the terminal-based 2048 game."""

import sys
import tty
import termios

from game import Game


def get_key() -> str:
    """Read a single keypress (including arrow keys) from stdin."""
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == "\\x1b":
            ch2 = sys.stdin.read(1)
            if ch2 == "[":
                ch3 = sys.stdin.read(1)
                return {"A": "up", "B": "down", "C": "right", "D": "left"}.get(ch3, "")
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def main():
    game = Game()
    print("2048 – use arrow keys or w/a/s/d to play, q to quit\\n")
    while not game.is_over():
        print(game.get_board())
        print(f"Score: {game.get_score()}\\n")
        key = get_key()
        if key in ("q", "\\x03"):
            print("Quit.")
            break
        game.process_key(key)
    if game.is_won():
        print("You reached 2048!  Well done.")
    elif game.is_over():
        print("No more moves.  Game over.")


if __name__ == "__main__":
    main()
'''

    # ── test_merge.py ─────────────────────────────────────────────────────────
    test_merge_py = '''\
"""Unit tests for the tile merge logic in Board._slide_row."""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from tile import Tile
from board import Board


def _row(*values):
    """Build a list of Tile objects (or None) from a sequence of ints (0 = None)."""
    return [Tile(v) if v else None for v in values]


def _vals(row):
    """Extract integer values from a row (None → 0)."""
    return [t.value if t is not None else 0 for t in row]


def test_merge_two_equal_tiles():
    """Two equal tiles at the left edge must merge into one."""
    board = Board.__new__(Board)          # skip __init__ / random tile spawn
    board.score = 0
    row = _row(2, 2, 0, 0)
    result = board._slide_row(row)
    vals = _vals(result)
    assert vals[0] == 4,  f"Expected 4 at index 0, got {vals}"
    assert vals[1] == 0,  f"Expected 0 at index 1, got {vals}"
    assert vals[2] == 0,  f"Expected 0 at index 2, got {vals}"
    assert vals[3] == 0,  f"Expected 0 at index 3, got {vals}"
    print("PASS test_merge_two_equal_tiles")
    return True


def test_no_double_merge():
    """Three equal tiles: only the first pair merges; the third stays."""
    board = Board.__new__(Board)
    board.score = 0
    row = _row(2, 2, 2, 0)
    result = board._slide_row(row)
    vals = _vals(result)
    # Expected: [4, 2, 0, 0]  – first pair merges, third slides left
    assert vals[0] == 4, f"Expected 4 at index 0, got {vals}"
    assert vals[1] == 2, f"Expected 2 at index 1, got {vals}"
    assert vals[2] == 0, f"Expected 0 at index 2, got {vals}"
    print("PASS test_no_double_merge")
    return True


def test_four_equal_tiles():
    """Four equal tiles produce two merged tiles."""
    board = Board.__new__(Board)
    board.score = 0
    row = _row(4, 4, 4, 4)
    result = board._slide_row(row)
    vals = _vals(result)
    assert vals[0] == 8, f"Expected 8 at index 0, got {vals}"
    assert vals[1] == 8, f"Expected 8 at index 1, got {vals}"
    assert vals[2] == 0, f"Expected 0 at index 2, got {vals}"
    assert vals[3] == 0, f"Expected 0 at index 3, got {vals}"
    print("PASS test_four_equal_tiles")
    return True


def test_no_merge_different_values():
    """Tiles with different values must NOT merge."""
    board = Board.__new__(Board)
    board.score = 0
    row = _row(2, 4, 0, 0)
    result = board._slide_row(row)
    vals = _vals(result)
    assert vals[0] == 2, f"Expected 2 at index 0, got {vals}"
    assert vals[1] == 4, f"Expected 4 at index 1, got {vals}"
    print("PASS test_no_merge_different_values")
    return True


def run_all() -> float:
    """Run all tests and return fraction passed."""
    tests = [
        test_merge_two_equal_tiles,
        test_no_double_merge,
        test_four_equal_tiles,
        test_no_merge_different_values,
    ]
    passed = 0
    for t in tests:
        try:
            if t():
                passed += 1
        except AssertionError as e:
            print(f"FAIL {t.__name__}: {e}")
        except Exception as e:
            print(f"ERROR {t.__name__}: {e}")
    print(f"\\nResult: {passed}/{len(tests)} tests passed")
    return passed / len(tests)


if __name__ == "__main__":
    score = run_all()
    sys.exit(0 if score == 1.0 else 1)
'''

    # ── Write files ──────────────────────────────────────────────────────────
    files = {
        'tile.py': tile_py,
        'board.py': board_py,
        'game.py': game_py,
        'main.py': main_py,
        'test_merge.py': test_merge_py,
    }

    for filename, content in files.items():
        path = os.path.join(GAME_DIR, filename)
        with open(path, 'w') as f:
            f.write(content)
        print(f'Created: {path}')

    print(f'\nGame project created at: {GAME_DIR}')
    print('Files: tile.py, board.py (BUG: merge skipped), game.py, main.py, test_merge.py')

    # GUI-ready startup: open VSCode with the game folder
    launch_gui(f'code "{GAME_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

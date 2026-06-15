"""
Initial Setup: Pac-Man project with broken ghost AI
Task ID: osworld_multi_apps_vscode_debug_game_008
Domain: vscode + python (multi-app)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT_DIR = '/home/user/Desktop/pacman'

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
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # --- maze.py ---
    maze_content = '''"""
Pac-Man Maze module.
Provides the maze grid and utility functions.
"""

# 0 = empty path, 1 = wall, 2 = dot, 3 = power pellet
MAZE = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,1],
    [1,3,1,1,2,1,1,1,2,1,1,2,1,1,1,2,1,1,3,1],
    [1,2,1,1,2,1,1,1,2,1,1,2,1,1,1,2,1,1,2,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,2,1,2,1,1,1,1,1,1,2,1,2,1,1,2,1],
    [1,2,2,2,2,1,2,2,2,1,1,2,2,2,1,2,2,2,2,1],
    [1,1,1,1,2,1,1,0,0,0,0,0,1,1,1,2,1,1,1,1],
    [1,1,1,1,2,1,0,0,0,0,0,0,0,1,1,2,1,1,1,1],
    [1,1,1,1,2,0,0,1,0,0,0,1,0,0,1,2,1,1,1,1],
    [0,0,0,0,2,0,0,1,0,0,0,1,0,0,0,2,0,0,0,0],
    [1,1,1,1,2,0,0,1,1,1,1,1,0,0,1,2,1,1,1,1],
    [1,1,1,1,2,1,0,0,0,0,0,0,0,1,1,2,1,1,1,1],
    [1,1,1,1,2,1,0,1,1,1,1,1,1,1,1,2,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,2,1,1,1,2,1,1,2,1,1,1,2,1,1,2,1],
    [1,3,2,1,2,2,2,2,2,2,2,2,2,2,2,2,1,2,3,1],
    [1,1,2,1,2,1,2,1,1,1,1,1,1,2,1,2,1,2,1,1],
    [1,2,2,2,2,1,2,2,2,1,1,2,2,2,1,2,2,2,2,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

TILE_SIZE = 32
COLS = len(MAZE[0])
ROWS = len(MAZE)


def is_wall(row, col):
    """Return True if the tile at (row, col) is a wall."""
    if row < 0 or row >= ROWS or col < 0 or col >= COLS:
        return True
    return MAZE[row][col] == 1


def get_tile(row, col):
    if row < 0 or row >= ROWS or col < 0 or col >= COLS:
        return -1
    return MAZE[row][col]


def pixel_to_tile(x, y):
    """Convert pixel coordinates to tile (row, col)."""
    return int(y // TILE_SIZE), int(x // TILE_SIZE)


def tile_to_pixel(row, col):
    """Convert tile (row, col) to pixel center coordinates."""
    x = col * TILE_SIZE + TILE_SIZE // 2
    y = row * TILE_SIZE + TILE_SIZE // 2
    return x, y
'''
    with open(os.path.join(PROJECT_DIR, 'maze.py'), 'w') as f:
        f.write(maze_content)

    # --- player.py ---
    player_content = '''"""
Pac-Man Player module.
Handles player movement and input.
"""

import pygame
from maze import is_wall, pixel_to_tile, TILE_SIZE


class Player:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.speed = 3.0
        self.direction = (0, 0)   # (dx, dy) in pixels per frame
        self.next_direction = (0, 0)
        self.score = 0
        self.lives = 3
        self.radius = TILE_SIZE // 2 - 2
        self.color = (255, 255, 0)  # Yellow

    @property
    def row(self):
        return int(self.y // TILE_SIZE)

    @property
    def col(self):
        return int(self.x // TILE_SIZE)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.next_direction = (-self.speed, 0)
        elif keys[pygame.K_RIGHT]:
            self.next_direction = (self.speed, 0)
        elif keys[pygame.K_UP]:
            self.next_direction = (0, -self.speed)
        elif keys[pygame.K_DOWN]:
            self.next_direction = (0, self.speed)

    def update(self):
        nx = self.x + self.next_direction[0]
        ny = self.y + self.next_direction[1]
        nr, nc = pixel_to_tile(nx, ny)
        if not is_wall(nr, nc):
            self.direction = self.next_direction

        nx = self.x + self.direction[0]
        ny = self.y + self.direction[1]
        nr, nc = pixel_to_tile(nx, ny)
        if not is_wall(nr, nc):
            self.x = nx
            self.y = ny

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        # Draw mouth (simple wedge approximation)
        import math
        mouth_angle = 30
        start_angle = math.radians(mouth_angle)
        end_angle = math.radians(-mouth_angle)
        pygame.draw.polygon(screen, (0, 0, 0), [
            (int(self.x), int(self.y)),
            (int(self.x + self.radius * math.cos(start_angle)),
             int(self.y - self.radius * math.sin(start_angle))),
            (int(self.x + self.radius * math.cos(end_angle)),
             int(self.y - self.radius * math.sin(end_angle))),
        ])

    def get_position(self):
        """Return current pixel position as (x, y) tuple."""
        return (self.x, self.y)
'''
    with open(os.path.join(PROJECT_DIR, 'player.py'), 'w') as f:
        f.write(player_content)

    # --- ghost.py — BROKEN version: ghosts do NOT chase the player ---
    ghost_content = '''"""
Pac-Man Ghost module.
BUG: Ghost AI does not navigate toward the player — ghosts stay near center.
"""

import pygame
import random
from maze import is_wall, pixel_to_tile, TILE_SIZE, ROWS, COLS


GHOST_COLORS = [
    (255, 0,   0  ),  # Blinky - red
    (255, 184, 255),  # Pinky  - pink
    (0,   255, 255),  # Inky   - cyan
    (255, 184, 82 ),  # Clyde  - orange
]


class Ghost:
    def __init__(self, x, y, color_index=0):
        self.x = float(x)
        self.y = float(y)
        self.start_x = float(x)
        self.start_y = float(y)
        self.speed = 2.0
        self.color = GHOST_COLORS[color_index % len(GHOST_COLORS)]
        self.direction = (0, 0)
        self.mode = "scatter"   # "scatter" | "chase" | "frightened"
        self.radius = TILE_SIZE // 2 - 2

    @property
    def row(self):
        return int(self.y // TILE_SIZE)

    @property
    def col(self):
        return int(self.x // TILE_SIZE)

    def _get_valid_directions(self):
        """Return list of (dx, dy) directions that are not walls."""
        candidates = [
            ( self.speed,  0),
            (-self.speed,  0),
            ( 0,  self.speed),
            ( 0, -self.speed),
        ]
        valid = []
        for dx, dy in candidates:
            nx = self.x + dx
            ny = self.y + dy
            nr, nc = pixel_to_tile(nx, ny)
            if not is_wall(nr, nc):
                valid.append((dx, dy))
        return valid

    def _choose_direction_toward(self, target_x, target_y):
        """
        Choose the direction that minimizes distance to (target_x, target_y).
        BUG: This method is never called — update() uses random movement instead.
        """
        valid = self._get_valid_directions()
        if not valid:
            return (0, 0)

        best_dir = valid[0]
        best_dist = float('inf')
        for dx, dy in valid:
            nx = self.x + dx
            ny = self.y + dy
            dist = (nx - target_x) ** 2 + (ny - target_y) ** 2
            if dist < best_dist:
                best_dist = dist
                best_dir = (dx, dy)
        return best_dir

    def update(self, player_x, player_y):
        """
        Update ghost position.
        BUG: Ghost always moves randomly, ignoring player position entirely.
        The call to _choose_direction_toward is missing — ghosts never chase.
        """
        # Decide whether to pick a new direction at tile boundaries
        cx = self.x % TILE_SIZE
        cy = self.y % TILE_SIZE
        at_tile_center = (abs(cx - TILE_SIZE // 2) < self.speed and
                          abs(cy - TILE_SIZE // 2) < self.speed)

        if at_tile_center or self.direction == (0, 0):
            # BUG: Always picks a random direction — never uses player position
            valid = self._get_valid_directions()
            if valid:
                self.direction = random.choice(valid)

        nx = self.x + self.direction[0]
        ny = self.y + self.direction[1]
        nr, nc = pixel_to_tile(nx, ny)
        if not is_wall(nr, nc):
            self.x = nx
            self.y = ny
        else:
            self.direction = (0, 0)

    def draw(self, screen):
        cx, cy = int(self.x), int(self.y)
        r = self.radius
        # Draw ghost body (circle top + rectangle bottom)
        pygame.draw.circle(screen, self.color, (cx, cy - r // 4), r)
        pygame.draw.rect(screen, self.color, (cx - r, cy - r // 4, r * 2, r + r // 4))
        # Eyes
        pygame.draw.circle(screen, (255, 255, 255), (cx - r // 3, cy - r // 4), r // 4)
        pygame.draw.circle(screen, (255, 255, 255), (cx + r // 3, cy - r // 4), r // 4)
        pygame.draw.circle(screen, (0, 0, 200),     (cx - r // 3, cy - r // 4), r // 8)
        pygame.draw.circle(screen, (0, 0, 200),     (cx + r // 3, cy - r // 4), r // 8)

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.direction = (0, 0)
'''
    with open(os.path.join(PROJECT_DIR, 'ghost.py'), 'w') as f:
        f.write(ghost_content)

    # --- main.py ---
    main_content = '''"""
Pac-Man main entry point.
Initializes pygame, creates maze, player and ghosts, runs game loop.
"""

import sys
import pygame
from maze import MAZE, TILE_SIZE, ROWS, COLS, is_wall
from player import Player
from ghost import Ghost

FPS = 60
SCREEN_W = COLS * TILE_SIZE
SCREEN_H = ROWS * TILE_SIZE

# Colors
BLACK  = (0,   0,   0  )
BLUE   = (0,   0,   180)
WHITE  = (255, 255, 255)
YELLOW = (255, 255, 0  )


def draw_maze(screen):
    for row in range(ROWS):
        for col in range(COLS):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            tile = MAZE[row][col]
            if tile == 1:
                pygame.draw.rect(screen, BLUE, (x, y, TILE_SIZE, TILE_SIZE))
            elif tile == 2:
                cx = x + TILE_SIZE // 2
                cy = y + TILE_SIZE // 2
                pygame.draw.circle(screen, WHITE, (cx, cy), 3)
            elif tile == 3:
                cx = x + TILE_SIZE // 2
                cy = y + TILE_SIZE // 2
                pygame.draw.circle(screen, WHITE, (cx, cy), 7)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Pac-Man")
    clock = pygame.time.Clock()

    player = Player(x=10 * TILE_SIZE + TILE_SIZE // 2,
                    y=15 * TILE_SIZE + TILE_SIZE // 2)

    ghost_starts = [
        (9 * TILE_SIZE + TILE_SIZE // 2, 9 * TILE_SIZE + TILE_SIZE // 2),
        (10 * TILE_SIZE + TILE_SIZE // 2, 9 * TILE_SIZE + TILE_SIZE // 2),
        (11 * TILE_SIZE + TILE_SIZE // 2, 9 * TILE_SIZE + TILE_SIZE // 2),
        (10 * TILE_SIZE + TILE_SIZE // 2, 10 * TILE_SIZE + TILE_SIZE // 2),
    ]
    ghosts = [Ghost(gx, gy, i) for i, (gx, gy) in enumerate(ghost_starts)]

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        player.handle_input()
        player.update()

        px, py = player.get_position()
        for ghost in ghosts:
            ghost.update(px, py)

        screen.fill(BLACK)
        draw_maze(screen)
        player.draw(screen)
        for ghost in ghosts:
            ghost.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
'''
    with open(os.path.join(PROJECT_DIR, 'main.py'), 'w') as f:
        f.write(main_content)

    # --- test_ghost_ai.py ---
    # This test checks that ghost AI chases the player.
    # In the initial (broken) state, this test should FAIL because ghosts use random movement.
    test_content = '''"""
Test for ghost pathfinding / chase AI.
Tests that Ghost.update() causes the ghost to move toward the player.
"""

import sys
import os

# Allow importing from the pacman project directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Stub out pygame before importing ghost module
import types

# Create minimal pygame stub
pygame_stub = types.ModuleType("pygame")
pygame_stub.TILE_SIZE = 32   # not used but needed for import

class _FakeDisplay:
    def set_mode(self, *a, **kw): return None
    def set_caption(self, *a, **kw): return None

class _FakeClock:
    def tick(self, *a): pass

pygame_stub.display = _FakeDisplay()
pygame_stub.Clock = _FakeClock
pygame_stub.draw = types.SimpleNamespace(
    circle=lambda *a, **kw: None,
    rect=lambda *a, **kw: None,
    polygon=lambda *a, **kw: None,
)
pygame_stub.init = lambda: None
pygame_stub.quit = lambda: None
pygame_stub.QUIT = 256
pygame_stub.KEYDOWN = 768
pygame_stub.K_ESCAPE = 27
pygame_stub.K_LEFT = 276
pygame_stub.K_RIGHT = 275
pygame_stub.K_UP = 273
pygame_stub.K_DOWN = 274
pygame_stub.key = types.SimpleNamespace(get_pressed=lambda: {})
pygame_stub.event = types.SimpleNamespace(get=lambda: [])
sys.modules["pygame"] = pygame_stub

from ghost import Ghost
from maze import TILE_SIZE


def test_ghost_chases_player():
    """
    Deterministic test: ghost and player placed on the same open maze row.
    A chasing ghost MUST move consistently rightward toward the player.

    Row 4 of the maze is fully open (all path tiles, cols 1-18).
    Ghost starts at tile (row=4, col=4) pixel (144, 144).
    Player is at tile (row=4, col=18) pixel (592, 144) — SAME ROW.

    After 200 update steps at speed=2:
      - A chasing ghost picks 'right' at every tile boundary => moves ~400px right => x ~ 544
      - A random ghost wanders in all directions and cannot reliably advance 300px right.
    """
    # Ghost at tile (4,4) center => pixel (144, 144)
    ghost_start_x = 4 * TILE_SIZE + TILE_SIZE // 2   # 144
    ghost_start_y = 4 * TILE_SIZE + TILE_SIZE // 2   # 144

    # Player on same row, far right: tile (4,18) => pixel (592, 144)
    player_x = 18 * TILE_SIZE + TILE_SIZE // 2       # 592
    player_y = 4  * TILE_SIZE + TILE_SIZE // 2       # 144  -- SAME ROW

    ghost = Ghost(ghost_start_x, ghost_start_y, color_index=0)

    # Run 200 update steps (200 * speed=2 = up to 400px of rightward movement)
    for _ in range(200):
        ghost.update(player_x, player_y)

    # A chasing ghost must advance at least 300 pixels right from its start position.
    # Expected: ghost.x ~ 144 + 400 = 544 (only 48px from player at x=592).
    assert ghost.x > ghost_start_x + 300, (
        f"Ghost x={ghost.x:.1f} did not advance far enough toward player at x={player_x}. "
        f"Expected x > {ghost_start_x + 300} after 200 steps. "
        f"Ghost is using random movement instead of greedy chase toward the player."
    )
    return True


if __name__ == "__main__":
    try:
        result = test_ghost_chases_player()
        print(f"TEST PASSED: ghost_chases_player = {result}")
        sys.exit(0)
    except AssertionError as e:
        print(f"TEST FAILED: {e}")
        sys.exit(1)
'''
    with open(os.path.join(PROJECT_DIR, 'test_ghost_ai.py'), 'w') as f:
        f.write(test_content)

    print(f"Project created at: {PROJECT_DIR}")
    print("Files: ghost.py (BROKEN AI), player.py, maze.py, main.py, test_ghost_ai.py")

    # GUI-ready startup: open VSCode with the pacman project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    # Also open ghost.py directly so the agent sees the bug immediately
    launch_gui(f'code "{PROJECT_DIR}/ghost.py"', delay_sec=1.5)
    print('GUI_READY: VSCode launched with pacman project (DISPLAY=:0)')


create_initial()

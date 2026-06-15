"""
Initial Setup: Tetris game without score display
Task ID: osworld_multi_apps_code_python_game_004
Domain: code/python/game (VSCode + pygame)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_code_python_game_004'
PROJECT_DIR = f'{WORKDIR}/projects/tetris'
OUTPUT = f'{PROJECT_DIR}/main.py'


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

    # Tetris game source code WITHOUT score display
    # The score variable is tracked but NOT rendered on screen
    tetris_code = '''\
import pygame
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE   # 10
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE  # 20
FPS = 30

# Colors
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
CYAN   = (0, 255, 255)
BLUE   = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN  = (0, 255, 0)
RED    = (255, 0, 0)
PURPLE = (128, 0, 128)

# Tetromino shapes
SHAPES = [
    # I
    [[1, 1, 1, 1]],
    # O
    [[1, 1],
     [1, 1]],
    # T
    [[0, 1, 0],
     [1, 1, 1]],
    # S
    [[0, 1, 1],
     [1, 1, 0]],
    # Z
    [[1, 1, 0],
     [0, 1, 1]],
    # J
    [[1, 0, 0],
     [1, 1, 1]],
    # L
    [[0, 0, 1],
     [1, 1, 1]],
]

COLORS = [CYAN, YELLOW, PURPLE, GREEN, RED, BLUE, ORANGE]

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Font initialization
pygame.font.init()
font = pygame.font.SysFont("monospace", 24, bold=True)

clock = pygame.time.Clock()

# Global score variable (tracked but not displayed)
score = 0


def create_grid():
    """Create an empty 20x10 grid."""
    return [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]


def draw_grid(surface, grid):
    """Draw the grid cells."""
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            color = grid[row][col]
            pygame.draw.rect(
                surface,
                color,
                (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
            )
            pygame.draw.rect(
                surface,
                WHITE,
                (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                1,
            )


class Tetromino:
    def __init__(self):
        idx = random.randint(0, len(SHAPES) - 1)
        self.shape = SHAPES[idx]
        self.color = COLORS[idx]
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        """Rotate the tetromino 90 degrees clockwise."""
        self.shape = [
            [self.shape[GRID_HEIGHT_IDX][col]
             for GRID_HEIGHT_IDX in range(len(self.shape) - 1, -1, -1)]
            for col in range(len(self.shape[0]))
        ]

    def draw(self, surface):
        for row_idx, row in enumerate(self.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        surface,
                        self.color,
                        (
                            (self.x + col_idx) * BLOCK_SIZE,
                            (self.y + row_idx) * BLOCK_SIZE,
                            BLOCK_SIZE,
                            BLOCK_SIZE,
                        ),
                    )
                    pygame.draw.rect(
                        surface,
                        WHITE,
                        (
                            (self.x + col_idx) * BLOCK_SIZE,
                            (self.y + row_idx) * BLOCK_SIZE,
                            BLOCK_SIZE,
                            BLOCK_SIZE,
                        ),
                        1,
                    )


def check_collision(grid, piece, offset_x=0, offset_y=0):
    """Check if piece collides with grid walls or other pieces."""
    for row_idx, row in enumerate(piece.shape):
        for col_idx, cell in enumerate(row):
            if cell:
                new_x = piece.x + col_idx + offset_x
                new_y = piece.y + row_idx + offset_y
                if new_x < 0 or new_x >= GRID_WIDTH:
                    return True
                if new_y >= GRID_HEIGHT:
                    return True
                if new_y >= 0 and grid[new_y][new_x] != BLACK:
                    return True
    return False


def lock_piece(grid, piece):
    """Lock a piece into the grid."""
    for row_idx, row in enumerate(piece.shape):
        for col_idx, cell in enumerate(row):
            if cell:
                grid[piece.y + row_idx][piece.x + col_idx] = piece.color


def clear_lines(grid):
    """Remove completed lines and return number of lines cleared."""
    global score
    lines_cleared = 0
    new_grid = []
    for row in grid:
        if BLACK not in row:
            lines_cleared += 1
        else:
            new_grid.append(row)
    # Add empty rows at top
    for _ in range(lines_cleared):
        new_grid.insert(0, [BLACK for _ in range(GRID_WIDTH)])
    # Update score based on lines cleared
    if lines_cleared == 1:
        score += 100
    elif lines_cleared == 2:
        score += 300
    elif lines_cleared == 3:
        score += 500
    elif lines_cleared >= 4:
        score += 800
    return new_grid


def draw_screen(surface, grid, piece):
    """Render the current game frame."""
    surface.fill(BLACK)
    draw_grid(surface, grid)
    piece.draw(surface)
    # NOTE: Score is tracked in the global `score` variable but is NOT drawn here.
    # The score display rendering is missing from this draw loop.
    pygame.display.flip()


def main():
    global score
    score = 0
    grid = create_grid()
    current_piece = Tetromino()
    fall_timer = 0
    fall_speed = 500  # milliseconds per drop

    running = True
    while running:
        clock.tick(FPS)
        fall_timer += clock.get_time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not check_collision(grid, current_piece, offset_x=-1):
                        current_piece.x -= 1
                elif event.key == pygame.K_RIGHT:
                    if not check_collision(grid, current_piece, offset_x=1):
                        current_piece.x += 1
                elif event.key == pygame.K_DOWN:
                    if not check_collision(grid, current_piece, offset_y=1):
                        current_piece.y += 1
                elif event.key == pygame.K_UP:
                    current_piece.rotate()
                    if check_collision(grid, current_piece):
                        # Undo rotation if collision
                        for _ in range(3):
                            current_piece.rotate()
                elif event.key == pygame.K_ESCAPE:
                    running = False

        # Automatic downward movement
        if fall_timer >= fall_speed:
            fall_timer = 0
            if not check_collision(grid, current_piece, offset_y=1):
                current_piece.y += 1
            else:
                lock_piece(grid, current_piece)
                grid = clear_lines(grid)
                current_piece = Tetromino()
                if check_collision(grid, current_piece):
                    # Game over
                    running = False

        draw_screen(screen, grid, current_piece)

    pygame.quit()


if __name__ == "__main__":
    main()
'''

    with open(OUTPUT, 'w') as f:
        f.write(tetris_code)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

"""
Initial Setup: Snake game without pause functionality
Task ID: osworld_multi_apps_code_python_game_005
Domain: multi_apps / code / python / vscode

Creates /home/user/projects/snake/game.py with a functional Snake game
that has NO pause feature. The agent must add pause (P key) functionality.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'  # VM path — all scripts run on the VM
TASK_ID = 'osworld_multi_apps_code_python_game_005'
PROJECT_DIR = f'{WORKDIR}/projects/snake'
GAME_FILE = f'{PROJECT_DIR}/game.py'

# Snake game source WITHOUT any pause functionality
GAME_SOURCE = '''\
import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
CELL_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 140, 0)
RED = (200, 0, 0)
GRAY = (50, 50, 50)
YELLOW = (255, 220, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def draw_grid(surface):
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(surface, GRAY, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, GRAY, (0, y), (WINDOW_WIDTH, y))


def draw_snake(surface, snake_body):
    for i, segment in enumerate(snake_body):
        x = segment[0] * CELL_SIZE
        y = segment[1] * CELL_SIZE
        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        color = DARK_GREEN if i == 0 else GREEN
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)


def draw_food(surface, food_pos):
    x = food_pos[0] * CELL_SIZE
    y = food_pos[1] * CELL_SIZE
    rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, RED, rect)
    pygame.draw.rect(surface, YELLOW, rect, 2)


def draw_score(surface, score, font):
    score_text = font.render(f"Score: {score}", True, WHITE)
    surface.blit(score_text, (10, 10))


def spawn_food(snake_body):
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in snake_body:
            return pos


def show_game_over(surface, score, font, big_font):
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    surface.blit(overlay, (0, 0))
    over_text = big_font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = font.render("Press R to restart or Q to quit", True, WHITE)
    surface.blit(over_text, (WINDOW_WIDTH // 2 - over_text.get_width() // 2, WINDOW_HEIGHT // 2 - 80))
    surface.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, WINDOW_HEIGHT // 2 - 10))
    surface.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, WINDOW_HEIGHT // 2 + 40))
    pygame.display.flip()


def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 20)
    big_font = pygame.font.SysFont("monospace", 48, bold=True)

    # Game state
    snake_body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = RIGHT
    next_direction = RIGHT
    food_pos = spawn_food(snake_body)
    score = 0
    game_over = False

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != DOWN:
                    next_direction = UP
                elif event.key == pygame.K_DOWN and direction != UP:
                    next_direction = DOWN
                elif event.key == pygame.K_LEFT and direction != RIGHT:
                    next_direction = LEFT
                elif event.key == pygame.K_RIGHT and direction != LEFT:
                    next_direction = RIGHT
                elif event.key == pygame.K_r and game_over:
                    # Restart game
                    snake_body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
                    direction = RIGHT
                    next_direction = RIGHT
                    food_pos = spawn_food(snake_body)
                    score = 0
                    game_over = False
                elif event.key == pygame.K_q and game_over:
                    pygame.quit()
                    sys.exit()

        if not game_over:
            # Update direction
            direction = next_direction

            # Move snake
            head_x, head_y = snake_body[0]
            new_head = (head_x + direction[0], head_y + direction[1])

            # Check wall collision
            if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                    new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
                game_over = True
            # Check self collision
            elif new_head in snake_body:
                game_over = True
            else:
                snake_body.insert(0, new_head)
                # Check food collision
                if new_head == food_pos:
                    score += 10
                    food_pos = spawn_food(snake_body)
                else:
                    snake_body.pop()

        # Draw
        screen.fill(BLACK)
        draw_grid(screen)
        draw_snake(screen, snake_body)
        draw_food(screen, food_pos)
        draw_score(screen, score, font)

        if game_over:
            show_game_over(screen, score, font, big_font)
        else:
            pygame.display.flip()

        clock.tick(FPS)


if __name__ == "__main__":
    main()
'''


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

    # Write the game file (without pause functionality)
    with open(GAME_FILE, 'w') as f:
        f.write(GAME_SOURCE)
    print(f'Game file created: {GAME_FILE}')

    # Verify file exists and has expected content
    with open(GAME_FILE, 'r') as f:
        content = f.read()
    assert 'paused' not in content, 'ERROR: initial file should NOT contain paused variable'
    assert 'K_p' not in content.lower() and 'pygame.K_p' not in content, \
        'ERROR: initial file should NOT contain P key handler'
    print('Verification passed: no pause functionality in initial file')

    # GUI-ready startup: open the project folder in VSCode
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.5)
    print('GUI_READY: launched VSCode with snake project folder (DISPLAY=:0)')


create_initial()

"""
Initial Setup: Pong game with score variables incorrectly inside the game loop
Task ID: osworld_multi_apps_code_python_game_007
Domain: os (Python file editing)
"""

import os
import shlex
import subprocess
import time
from pathlib import Path

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_code_python_game_007'
PROJECT_DIR = f'{WORKDIR}/projects/pong'
OUTPUT = f'{PROJECT_DIR}/game.py'


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

    # Buggy game.py: score_left and score_right are INSIDE the while loop
    # This causes them to reset to 0 every frame
    game_code = '''\
"""
Pong Game
A simple two-player Pong game using pygame.
Player 1: W/S keys  |  Player 2: Up/Down arrow keys
"""

import pygame
import sys

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Paddle settings
PADDLE_WIDTH = 12
PADDLE_HEIGHT = 80
PADDLE_SPEED = 6

# Ball settings
BALL_SIZE = 12
BALL_SPEED_X = 5
BALL_SPEED_Y = 4


def draw_dashed_line(surface, color, start, end, dash_length=10):
    """Draw a dashed vertical line in the center of the screen."""
    x = start[0]
    y = start[1]
    while y < end[1]:
        pygame.draw.line(surface, color, (x, y), (x, min(y + dash_length, end[1])))
        y += dash_length * 2


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 48, bold=True)
    small_font = pygame.font.SysFont("monospace", 24)

    # Paddles
    left_paddle = pygame.Rect(20, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2,
                              PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = pygame.Rect(SCREEN_WIDTH - 20 - PADDLE_WIDTH,
                               SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2,
                               PADDLE_WIDTH, PADDLE_HEIGHT)

    # Ball
    ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_SIZE // 2,
                       SCREEN_HEIGHT // 2 - BALL_SIZE // 2,
                       BALL_SIZE, BALL_SIZE)
    ball_dx = BALL_SPEED_X
    ball_dy = BALL_SPEED_Y

    running = True
    while running:
        # BUG: score variables are re-initialized here inside the loop,
        # causing them to reset to 0 every frame instead of persisting.
        score_left = 0
        score_right = 0

        clock.tick(FPS)

        # --- Event handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # --- Paddle movement ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_s] and left_paddle.bottom < SCREEN_HEIGHT:
            left_paddle.y += PADDLE_SPEED
        if keys[pygame.K_UP] and right_paddle.top > 0:
            right_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and right_paddle.bottom < SCREEN_HEIGHT:
            right_paddle.y += PADDLE_SPEED

        # --- Ball movement ---
        ball.x += ball_dx
        ball.y += ball_dy

        # Top / bottom wall bounce
        if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
            ball_dy = -ball_dy

        # Paddle collision
        if ball.colliderect(left_paddle) and ball_dx < 0:
            ball_dx = -ball_dx
            # Slight angle variation based on hit position
            offset = (ball.centery - left_paddle.centery) / (PADDLE_HEIGHT / 2)
            ball_dy = int(offset * BALL_SPEED_Y * 1.5)

        if ball.colliderect(right_paddle) and ball_dx > 0:
            ball_dx = -ball_dx
            offset = (ball.centery - right_paddle.centery) / (PADDLE_HEIGHT / 2)
            ball_dy = int(offset * BALL_SPEED_Y * 1.5)

        # --- Scoring ---
        if ball.left <= 0:
            score_right += 1
            # Reset ball to center
            ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            ball_dx = BALL_SPEED_X
            ball_dy = BALL_SPEED_Y

        if ball.right >= SCREEN_WIDTH:
            score_left += 1
            # Reset ball to center
            ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            ball_dx = -BALL_SPEED_X
            ball_dy = BALL_SPEED_Y

        # --- Drawing ---
        screen.fill(BLACK)

        # Center dashed line
        draw_dashed_line(screen, GRAY,
                         (SCREEN_WIDTH // 2, 0),
                         (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

        # Paddles
        pygame.draw.rect(screen, WHITE, left_paddle)
        pygame.draw.rect(screen, WHITE, right_paddle)

        # Ball
        pygame.draw.rect(screen, WHITE, ball)

        # Scores
        left_score_surf = font.render(str(score_left), True, WHITE)
        right_score_surf = font.render(str(score_right), True, WHITE)
        screen.blit(left_score_surf, (SCREEN_WIDTH // 4 - left_score_surf.get_width() // 2, 20))
        screen.blit(right_score_surf, (3 * SCREEN_WIDTH // 4 - right_score_surf.get_width() // 2, 20))

        # Instructions
        hint = small_font.render("W/S  vs  UP/DOWN   |   ESC to quit", True, GRAY)
        screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 30))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
'''

    Path(OUTPUT).write_text(game_code)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open the game.py file in gedit for editing
    launch_gui(f'gedit "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched gedit with game.py using DISPLAY=:0')


create_initial()

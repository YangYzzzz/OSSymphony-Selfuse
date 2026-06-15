"""
Initial Setup: Space Invaders clone with broken bullet-alien hit detection
Task ID: osworld_multi_apps_vscode_debug_game_004
Domain: vscode / python
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT_DIR = f'{WORKDIR}/Desktop/invaders'


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

    # ---- alien.py ----
    alien_py = '''\
"""
alien.py — Alien enemy sprite for Space Invaders clone.
"""

import pygame


class Alien(pygame.sprite.Sprite):
    """Represents an alien enemy in the Space Invaders game."""

    WIDTH = 40
    HEIGHT = 32
    POINTS = 10

    def __init__(self, x: int, y: int, color=(0, 200, 50)):
        super().__init__()
        self.image = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        self._draw_alien(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.alive = True
        self.points = self.POINTS

    def _draw_alien(self, color):
        """Draw a simple pixelated alien shape."""
        pygame.draw.rect(self.image, color, (8, 8, 24, 16))
        pygame.draw.rect(self.image, color, (4, 12, 32, 8))
        pygame.draw.rect(self.image, color, (0, 16, 8, 8))
        pygame.draw.rect(self.image, color, (32, 16, 8, 8))
        pygame.draw.rect(self.image, color, (12, 4, 6, 8))
        pygame.draw.rect(self.image, color, (22, 4, 6, 8))

    def update(self, dx: int = 0, dy: int = 0):
        """Move the alien by dx, dy pixels."""
        self.rect.x += dx
        self.rect.y += dy

    def kill(self):
        """Mark alien as dead and remove from sprite groups."""
        self.alive = False
        super().kill()
'''

    # ---- bullet.py — INTENTIONALLY BROKEN hit detection ----
    # The bug: check_hit compares rect positions using wrong coordinates
    # (uses rect.x > other.rect.x instead of rect.colliderect)
    bullet_py = '''\
"""
bullet.py — Player bullet sprite for Space Invaders clone.

BUG: The check_hit method has broken collision detection logic.
     It compares raw x/y coordinates incorrectly, so bullets
     never register hits against aliens.
"""

import pygame


class Bullet(pygame.sprite.Sprite):
    """A laser shot fired upward by the player."""

    WIDTH = 4
    HEIGHT = 12
    SPEED = 10
    COLOR = (255, 255, 100)

    def __init__(self, x: int, y: int):
        super().__init__()
        self.image = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(self.image, self.COLOR, (0, 0, self.WIDTH, self.HEIGHT))
        self.rect = self.image.get_rect(centerx=x, bottom=y)
        self.active = True

    def update(self):
        """Move bullet upward each frame."""
        self.rect.y -= self.SPEED
        # Remove bullet when it leaves the top of the screen
        if self.rect.bottom < 0:
            self.active = False
            self.kill()

    def check_hit(self, alien) -> bool:
        """
        Check whether this bullet has hit the given alien sprite.

        Returns True if a collision is detected, False otherwise.

        BUG: Uses wrong coordinate comparison — should use rect.colliderect().
        Current logic checks if bullet.rect.x > alien.rect.x which is always
        False when bullet is centered on the player and aliens are to the right,
        so hits are never registered.
        """
        # BUGGY IMPLEMENTATION: incorrect positional comparison
        if self.rect.x > alien.rect.x and self.rect.y < alien.rect.y:
            return True
        return False
'''

    # ---- player.py ----
    player_py = '''\
"""
player.py — Player sprite for Space Invaders clone.
"""

import pygame
from bullet import Bullet


class Player(pygame.sprite.Sprite):
    """The player\'s ship at the bottom of the screen."""

    WIDTH = 48
    HEIGHT = 24
    SPEED = 5
    COLOR = (100, 180, 255)
    SHOOT_COOLDOWN = 400  # milliseconds between shots

    def __init__(self, screen_width: int, screen_height: int):
        super().__init__()
        self.image = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        self._draw_ship()
        self.rect = self.image.get_rect(
            centerx=screen_width // 2,
            bottom=screen_height - 10
        )
        self.screen_width = screen_width
        self._last_shot = 0
        self.score = 0

    def _draw_ship(self):
        pygame.draw.polygon(
            self.image, self.COLOR,
            [(self.WIDTH // 2, 0), (0, self.HEIGHT), (self.WIDTH, self.HEIGHT)]
        )
        pygame.draw.rect(self.image, (200, 220, 255), (self.WIDTH // 2 - 4, 4, 8, 12))

    def update(self, keys_pressed):
        """Move left/right and enforce screen boundaries."""
        if keys_pressed[pygame.K_LEFT]:
            self.rect.x -= self.SPEED
        if keys_pressed[pygame.K_RIGHT]:
            self.rect.x += self.SPEED
        # Clamp to screen edges
        self.rect.clamp_ip(pygame.Rect(0, 0, self.screen_width, self.rect.height + self.rect.top + 10))

    def shoot(self, bullet_group, all_sprites) -> bool:
        """Fire a bullet if cooldown has elapsed. Returns True if shot fired."""
        now = pygame.time.get_ticks()
        if now - self._last_shot >= self.SHOOT_COOLDOWN:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            all_sprites.add(bullet)
            self._last_shot = now
            return True
        return False

    def add_score(self, points: int):
        self.score += points
'''

    # ---- main.py ----
    main_py = '''\
"""
main.py — Entry point for the Space Invaders clone.

Run:
    python main.py

Controls:
    Arrow Left / Right  — move ship
    Space               — fire laser
    ESC                 — quit
"""

import sys
import pygame
from player import Player
from alien import Alien
from bullet import Bullet

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
BG_COLOR = (10, 10, 30)

ALIEN_ROWS = 4
ALIEN_COLS = 10
ALIEN_X_SPACING = 60
ALIEN_Y_SPACING = 50
ALIEN_START_X = 80
ALIEN_START_Y = 60
ALIEN_MOVE_INTERVAL = 600  # ms between alien moves
ALIEN_MOVE_STEP = 12


def build_alien_grid():
    aliens = pygame.sprite.Group()
    colors = [
        (220, 50, 50),
        (220, 130, 50),
        (200, 200, 50),
        (50, 200, 50),
    ]
    for row in range(ALIEN_ROWS):
        color = colors[row % len(colors)]
        for col in range(ALIEN_COLS):
            x = ALIEN_START_X + col * ALIEN_X_SPACING
            y = ALIEN_START_Y + row * ALIEN_Y_SPACING
            alien = Alien(x, y, color)
            aliens.add(alien)
    return aliens


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Invaders")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 20)

    all_sprites = pygame.sprite.Group()
    player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)
    all_sprites.add(player)

    aliens = build_alien_grid()
    all_sprites.add(aliens)

    bullets = pygame.sprite.Group()

    alien_direction = 1  # 1 = right, -1 = left
    last_alien_move = pygame.time.get_ticks()

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    player.shoot(bullets, all_sprites)

        keys = pygame.key.get_pressed()
        player.update(keys)
        bullets.update()

        # Alien movement
        now = pygame.time.get_ticks()
        if now - last_alien_move >= ALIEN_MOVE_INTERVAL:
            # Check if any alien touches the edge
            hit_edge = False
            for alien in aliens:
                if (alien_direction == 1 and alien.rect.right >= SCREEN_WIDTH - 20) or \
                   (alien_direction == -1 and alien.rect.left <= 20):
                    hit_edge = True
                    break
            if hit_edge:
                alien_direction *= -1
                for alien in aliens:
                    alien.update(dy=ALIEN_Y_SPACING // 2)
            else:
                for alien in aliens:
                    alien.update(dx=alien_direction * ALIEN_MOVE_STEP)
            last_alien_move = now

        # ---- COLLISION DETECTION (uses broken Bullet.check_hit) ----
        for bullet in list(bullets):
            if not bullet.active:
                continue
            for alien in list(aliens):
                if bullet.check_hit(alien):
                    player.add_score(alien.points)
                    alien.kill()
                    bullet.active = False
                    bullet.kill()
                    break

        # Check win / lose conditions
        if not aliens:
            print(f"You Win! Score: {player.score}")
            running = False
        for alien in aliens:
            if alien.rect.bottom >= SCREEN_HEIGHT - 60:
                print("Game Over! The aliens reached your base.")
                running = False
                break

        # Draw
        screen.fill(BG_COLOR)
        all_sprites.draw(screen)
        score_surf = font.render(f"Score: {player.score}", True, (255, 255, 255))
        screen.blit(score_surf, (10, 10))
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
'''

    # ---- test_hit_detection.py — test suite that FAILS with broken code ----
    test_py = '''\
"""
test_hit_detection.py — Unit tests for bullet-alien collision detection.

Run:
    python test_hit_detection.py

Expected: All tests pass after fixing Bullet.check_hit() in bullet.py.
"""

import sys
import os
import types

# ---------------------------------------------------------------------------
# Minimal pygame stub so tests run without a display
# ---------------------------------------------------------------------------
pygame_stub = types.ModuleType("pygame")
pygame_stub.sprite = types.ModuleType("pygame.sprite")


class _StubSprite:
    def __init__(self):
        self._groups = []

    def kill(self):
        pass


class _StubGroup:
    def __init__(self):
        self._sprites = []

    def add(self, *sprites):
        for s in sprites:
            self._sprites.append(s)

    def __iter__(self):
        return iter(self._sprites)

    def __len__(self):
        return len(self._sprites)


pygame_stub.sprite.Sprite = _StubSprite
pygame_stub.sprite.Group = _StubGroup


class _Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.left = x
        self.right = x + w
        self.top = y
        self.bottom = y + h
        self.centerx = x + w // 2
        self.centery = y + h // 2

    def colliderect(self, other):
        return (
            self.left < other.right and
            self.right > other.left and
            self.top < other.bottom and
            self.bottom > other.top
        )

    def get_rect(self, **kwargs):
        r = _Rect(0, 0, self.width, self.height)
        if "centerx" in kwargs:
            r.x = kwargs["centerx"] - self.width // 2
            r.centerx = kwargs["centerx"]
        if "bottom" in kwargs:
            r.y = kwargs["bottom"] - self.height
            r.bottom = kwargs["bottom"]
            r.top = r.y
        if "topleft" in kwargs:
            r.x, r.y = kwargs["topleft"]
            r.left = r.x
            r.top = r.y
            r.right = r.x + r.width
            r.bottom = r.y + r.height
            r.centerx = r.x + r.width // 2
        return r


class _Surface:
    def __init__(self, size, flags=0):
        self.width, self.height = size

    def get_rect(self, **kwargs):
        r = _Rect(0, 0, self.width, self.height)
        if "centerx" in kwargs:
            r.x = kwargs["centerx"] - self.width // 2
            r.centerx = kwargs["centerx"]
        if "bottom" in kwargs:
            r.y = kwargs["bottom"] - self.height
            r.bottom = kwargs["bottom"]
            r.top = r.y
            r.left = r.x
            r.right = r.x + self.width
        if "topleft" in kwargs:
            r.x, r.y = kwargs["topleft"]
            r.left = r.x
            r.top = r.y
            r.right = r.x + self.width
            r.bottom = r.y + self.height
            r.centerx = r.x + self.width // 2
        return r


pygame_stub.Surface = _Surface
pygame_stub.SRCALPHA = 65536


def _draw_rect(surface, color, rect, **kwargs):
    pass


def _draw_polygon(surface, color, points, **kwargs):
    pass


pygame_stub.draw = types.ModuleType("pygame.draw")
pygame_stub.draw.rect = _draw_rect
pygame_stub.draw.polygon = _draw_polygon
sys.modules["pygame"] = pygame_stub
sys.modules["pygame.sprite"] = pygame_stub.sprite
sys.modules["pygame.draw"] = pygame_stub.draw

# ---------------------------------------------------------------------------
# Import Bullet and Alien from the project
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from bullet import Bullet  # noqa: E402
from alien import Alien    # noqa: E402


# ---------------------------------------------------------------------------
# Helpers to create test objects with explicit rects
# ---------------------------------------------------------------------------

def _make_bullet(cx, bottom):
    """Create a Bullet and forcefully set its rect."""
    b = Bullet.__new__(Bullet)
    b.active = True
    b.rect = _Rect(cx - Bullet.WIDTH // 2, bottom - Bullet.HEIGHT,
                   Bullet.WIDTH, Bullet.HEIGHT)
    b.rect.bottom = bottom
    b.rect.top = bottom - Bullet.HEIGHT
    b.rect.left = cx - Bullet.WIDTH // 2
    b.rect.right = cx + Bullet.WIDTH // 2
    b.rect.centerx = cx
    return b


def _make_alien(x, y):
    """Create an Alien and forcefully set its rect."""
    a = Alien.__new__(Alien)
    a.alive = True
    a.points = 10
    a.rect = _Rect(x, y, Alien.WIDTH, Alien.HEIGHT)
    a.rect.left = x
    a.rect.top = y
    a.rect.right = x + Alien.WIDTH
    a.rect.bottom = y + Alien.HEIGHT
    a.rect.centerx = x + Alien.WIDTH // 2
    return a


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_direct_hit():
    """Bullet overlapping alien center should be a hit."""
    alien = _make_alien(100, 80)         # alien at (100,80) size 40x32
    bullet = _make_bullet(120, 100)      # bullet center at x=120, bottom=100 -> overlaps
    result = bullet.check_hit(alien)
    assert result is True, (
        f"Expected True for direct hit, got {result!r}. "
        "check_hit() must use rect.colliderect() for correct detection."
    )


def test_miss_left():
    """Bullet entirely to the left of alien should NOT be a hit."""
    alien = _make_alien(200, 80)
    bullet = _make_bullet(50, 100)       # far left, no overlap
    result = bullet.check_hit(alien)
    assert result is False, (
        f"Expected False for miss (left), got {result!r}."
    )


def test_miss_right():
    """Bullet entirely to the right of alien should NOT be a hit."""
    alien = _make_alien(50, 80)
    bullet = _make_bullet(300, 100)      # far right, no overlap
    result = bullet.check_hit(alien)
    assert result is False, (
        f"Expected False for miss (right), got {result!r}."
    )


def test_miss_above():
    """Bullet above and not overlapping alien should NOT be a hit."""
    alien = _make_alien(100, 300)
    bullet = _make_bullet(120, 100)      # bullet bottom=100 < alien top=300
    result = bullet.check_hit(alien)
    assert result is False, (
        f"Expected False for miss (above), got {result!r}."
    )


def test_edge_overlap():
    """Bullet overlapping the right edge of alien should be a hit."""
    alien = _make_alien(100, 80)         # alien right edge = 140
    bullet = _make_bullet(138, 96)       # bullet left overlaps alien right
    result = bullet.check_hit(alien)
    assert result is True, (
        f"Expected True for edge overlap, got {result!r}."
    )


def test_multiple_aliens_only_hit_overlapping():
    """Only the alien spatially overlapping the bullet should register a hit."""
    aliens = [
        _make_alien(50, 80),    # alien A — not overlapping
        _make_alien(200, 80),   # alien B — bullet will overlap this one
        _make_alien(400, 80),   # alien C — not overlapping
    ]
    bullet = _make_bullet(220, 100)      # overlaps alien B
    hits = [bullet.check_hit(a) for a in aliens]
    assert hits == [False, True, False], (
        f"Expected [False, True, False], got {hits}. "
        "Only the overlapping alien should be hit."
    )


if __name__ == "__main__":
    tests = [
        test_direct_hit,
        test_miss_left,
        test_miss_right,
        test_miss_above,
        test_edge_overlap,
        test_multiple_aliens_only_hit_overlapping,
    ]
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  FAIL  {t.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"  ERROR {t.__name__}: {e}")
            failed += 1

    print(f"\\nResults: {passed} passed, {failed} failed out of {len(tests)} tests.")
    sys.exit(0 if failed == 0 else 1)
'''

    # Write all files to project directory
    files = {
        'alien.py': alien_py,
        'bullet.py': bullet_py,
        'player.py': player_py,
        'main.py': main_py,
        'test_hit_detection.py': test_py,
    }
    for filename, content in files.items():
        filepath = os.path.join(PROJECT_DIR, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f'Created: {filepath}')

    print(f'Space Invaders project created at: {PROJECT_DIR}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

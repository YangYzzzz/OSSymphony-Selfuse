"""
Reward Script: Fix bullet-alien collision detection in Space Invaders VSCode project
Task ID: osworld_multi_apps_vscode_debug_game_004
Domain: vscode (multi_apps)
Scoring:
  Component 1 (0.6): bullet.py check_hit() uses rect.colliderect() for proper AABB detection
  Component 2 (0.4): Test suite (test_hit_detection.py) passes all 6 tests
"""

import os
import re
import sys
import types

WORKDIR = '/home/user/Desktop/invaders'
TASK_ID = 'osworld_multi_apps_vscode_debug_game_004'

BULLET_PATH = os.path.join(WORKDIR, 'bullet.py')
TEST_PATH = os.path.join(WORKDIR, 'test_hit_detection.py')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: required files must exist
    if not os.path.exists(BULLET_PATH):
        print(f"CRITICAL: bullet.py not found at {BULLET_PATH}")
        print("REWARD: 0.0")
        return 0.0

    if not os.path.exists(TEST_PATH):
        print(f"CRITICAL: test_hit_detection.py not found at {TEST_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: check_hit() uses rect.colliderect() — the actual fix (0.6 points)
    # The buggy version used 'self.rect.x > alien.rect.x' positional comparison.
    # The fixed version uses 'self.rect.colliderect(alien.rect)'.
    # FAILS on initial (buggy code), PASSES on golden (fixed code).
    try:
        with open(BULLET_PATH, 'r') as f:
            bullet_content = f.read()

        # Check that colliderect is used in check_hit
        uses_colliderect = 'colliderect' in bullet_content

        # Check that the buggy pattern is gone (x-coordinate comparison as the hit detection logic)
        has_buggy_pattern = bool(re.search(
            r'self\.rect\.x\s*[><=!]+\s*alien\.rect\.x',
            bullet_content
        ))

        if uses_colliderect and not has_buggy_pattern:
            print(f"PASS: Component 1 — check_hit() uses rect.colliderect() for AABB collision detection (0.6 pts)")
            total_score += 0.6
        elif not uses_colliderect:
            print(f"FAIL: Component 1 — check_hit() does not use rect.colliderect(). Found in bullet.py: {bullet_content[bullet_content.find('def check_hit'):bullet_content.find('def check_hit')+300] if 'def check_hit' in bullet_content else 'check_hit not found'}")
        elif has_buggy_pattern:
            print(f"FAIL: Component 1 — Buggy 'self.rect.x > alien.rect.x' pattern still present in check_hit()")
        else:
            print(f"FAIL: Component 1 — check_hit() implementation unclear")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not read bullet.py: {e}")

    # Component 2: Test suite passes all 6 tests (0.4 points)
    # test_hit_detection.py exercises all collision scenarios.
    # FAILS on initial (4 of 6 tests fail), PASSES on golden (all 6 pass).
    try:
        # Build a minimal pygame stub to run tests headlessly (no display needed)
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

        # Force re-import of bullet module with fresh pygame stub
        for mod_name in list(sys.modules.keys()):
            if mod_name in ('bullet', 'alien'):
                del sys.modules[mod_name]

        if WORKDIR not in sys.path:
            sys.path.insert(0, WORKDIR)

        from bullet import Bullet
        from alien import Alien

        # Define test helper functions
        def _make_bullet(cx, bottom):
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

        # Run all 6 tests inline
        tests_passed = 0
        tests_total = 6

        # Test 1: direct_hit
        try:
            alien = _make_alien(100, 80)
            bullet = _make_bullet(120, 100)
            result = bullet.check_hit(alien)
            if result is True:
                tests_passed += 1
                print("  PASS: test_direct_hit")
            else:
                print(f"  FAIL: test_direct_hit — expected True, got {result!r}")
        except Exception as e:
            print(f"  ERROR: test_direct_hit — {e}")

        # Test 2: miss_left
        try:
            alien = _make_alien(200, 80)
            bullet = _make_bullet(50, 100)
            result = bullet.check_hit(alien)
            if result is False:
                tests_passed += 1
                print("  PASS: test_miss_left")
            else:
                print(f"  FAIL: test_miss_left — expected False, got {result!r}")
        except Exception as e:
            print(f"  ERROR: test_miss_left — {e}")

        # Test 3: miss_right
        try:
            alien = _make_alien(50, 80)
            bullet = _make_bullet(300, 100)
            result = bullet.check_hit(alien)
            if result is False:
                tests_passed += 1
                print("  PASS: test_miss_right")
            else:
                print(f"  FAIL: test_miss_right — expected False, got {result!r}")
        except Exception as e:
            print(f"  ERROR: test_miss_right — {e}")

        # Test 4: miss_above
        try:
            alien = _make_alien(100, 300)
            bullet = _make_bullet(120, 100)
            result = bullet.check_hit(alien)
            if result is False:
                tests_passed += 1
                print("  PASS: test_miss_above")
            else:
                print(f"  FAIL: test_miss_above — expected False, got {result!r}")
        except Exception as e:
            print(f"  ERROR: test_miss_above — {e}")

        # Test 5: edge_overlap
        try:
            alien = _make_alien(100, 80)
            bullet = _make_bullet(138, 96)
            result = bullet.check_hit(alien)
            if result is True:
                tests_passed += 1
                print("  PASS: test_edge_overlap")
            else:
                print(f"  FAIL: test_edge_overlap — expected True, got {result!r}")
        except Exception as e:
            print(f"  ERROR: test_edge_overlap — {e}")

        # Test 6: multiple_aliens_only_hit_overlapping
        try:
            aliens = [
                _make_alien(50, 80),
                _make_alien(200, 80),
                _make_alien(400, 80),
            ]
            bullet = _make_bullet(220, 100)
            hits = [bullet.check_hit(a) for a in aliens]
            if hits == [False, True, False]:
                tests_passed += 1
                print("  PASS: test_multiple_aliens_only_hit_overlapping")
            else:
                print(f"  FAIL: test_multiple_aliens_only_hit_overlapping — expected [False, True, False], got {hits}")
        except Exception as e:
            print(f"  ERROR: test_multiple_aliens_only_hit_overlapping — {e}")

        if tests_passed == tests_total:
            print(f"PASS: Component 2 — All {tests_total} hit-detection tests passed (0.4 pts)")
            total_score += 0.4
        elif tests_passed > 0:
            # No partial credit for partial test pass — collision detection is either correct or not
            print(f"FAIL: Component 2 — Only {tests_passed}/{tests_total} tests passed; all must pass for full credit")
        else:
            print(f"FAIL: Component 2 — All {tests_total} tests failed")

    except Exception as e:
        print(f"ERROR: Component 2 — Could not run test suite: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

"""
Reward Script: Fix Pac-Man ghost AI to chase the player instead of moving randomly.
Task ID: osworld_multi_apps_vscode_debug_game_008
Domain: vs-code (Python file editing task)

Scoring Rubric:
  Component 1 (0.5): ghost.py update() calls _choose_direction_toward() instead of random.choice()
  Component 2 (0.5): test_ghost_ai.py test_ghost_chases_player() passes
  Total: 1.0

The bug: In the initial state, Ghost.update() uses random.choice(valid) to pick a direction,
ignoring the player position. The fix: replace random.choice with _choose_direction_toward(player_x, player_y).
"""

import os
import re
import sys
import importlib.util
import types

WORKDIR = '/home/user/Desktop/pacman'
TASK_ID = 'osworld_multi_apps_vscode_debug_game_008'

GHOST_PY = os.path.join(WORKDIR, 'ghost.py')
TEST_PY  = os.path.join(WORKDIR, 'test_ghost_ai.py')


def verify_task():
    """
    Verify ghost AI fix with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # --- Precondition: ghost.py must exist ---
    if not os.path.exists(GHOST_PY):
        print(f"CRITICAL: ghost.py not found at {GHOST_PY}")
        print("REWARD: 0.0")
        return 0.0

    # -----------------------------------------------------------------------
    # Component 1: update() calls _choose_direction_toward() instead of random.choice
    # This is the core code fix. (0.5 points)
    # -----------------------------------------------------------------------
    try:
        with open(GHOST_PY, 'r') as f:
            ghost_source = f.read()

        # Parse the update() method body
        # Find the update method and check if it calls _choose_direction_toward
        # and does NOT call random.choice for direction selection.
        update_match = re.search(
            r'def update\s*\(self.*?\).*?(?=\ndef |\Z)',
            ghost_source,
            re.DOTALL
        )

        if update_match:
            update_body = update_match.group(0)

            # Strip comments and docstrings from update_body before checking
            # to avoid matching mentions of the method name in comments/docstrings.
            # Strip triple-quoted docstrings
            code_only = re.sub(r'""".*?"""', '', update_body, flags=re.DOTALL)
            code_only = re.sub(r"'''.*?'''", '', code_only, flags=re.DOTALL)
            # Strip single-line comments
            code_only = re.sub(r'#[^\n]*', '', code_only)

            # The fix requires an actual call to self._choose_direction_toward(...)
            # in the executable code (not in comments/docstrings).
            calls_choose_toward = bool(re.search(
                r'self\._choose_direction_toward\s*\(',
                code_only
            ))
            # The bug uses random.choice to set self.direction
            uses_random_choice_for_direction = bool(re.search(
                r'random\.choice\s*\(',
                code_only
            ))

            if calls_choose_toward and not uses_random_choice_for_direction:
                print(f"PASS: Component 1 — update() calls self._choose_direction_toward() "
                      f"and does not use random.choice for direction selection (0.5 pts)")
                total_score += 0.5
            elif calls_choose_toward and uses_random_choice_for_direction:
                print(f"FAIL: Component 1 — update() calls _choose_direction_toward() "
                      f"BUT still uses random.choice for direction (partially fixed but incorrect)")
            else:
                print(f"FAIL: Component 1 — update() does not call self._choose_direction_toward(). "
                      f"Ghost AI is still using random movement instead of chasing the player.")
        else:
            print(f"FAIL: Component 1 — Could not locate update() method in ghost.py")

    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: test_ghost_chases_player() passes (0.5 points)
    # This is the behavioral verification — ghost must actually move toward player.
    # -----------------------------------------------------------------------
    try:
        if not os.path.exists(TEST_PY):
            print(f"FAIL: Component 2 — test_ghost_ai.py not found at {TEST_PY}")
        else:
            # We need to load the test module in the WORKDIR context to allow
            # ghost.py and maze.py to be imported correctly.

            # First, install a pygame stub (no display available in reward context)
            pygame_stub = types.ModuleType("pygame")
            pygame_stub.TILE_SIZE = 32

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

            # Change to WORKDIR so relative imports in ghost/maze work
            original_cwd = os.getcwd()
            original_sys_path = sys.path.copy()
            try:
                os.chdir(WORKDIR)
                if WORKDIR not in sys.path:
                    sys.path.insert(0, WORKDIR)

                # Remove cached ghost/maze modules to force re-import from WORKDIR
                for mod_name in list(sys.modules.keys()):
                    if mod_name in ('ghost', 'maze', 'player', 'main'):
                        del sys.modules[mod_name]

                # Load and run the test module
                module_name = "test_ghost_ai_reward"
                spec = importlib.util.spec_from_file_location(module_name, TEST_PY)
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)

                # Call the test function
                result = module.test_ghost_chases_player()
                if result is True or result == 1.0:
                    print(f"PASS: Component 2 — test_ghost_chases_player() passed: "
                          f"ghost moved toward player position (0.5 pts)")
                    total_score += 0.5
                else:
                    print(f"FAIL: Component 2 — test_ghost_chases_player() returned {result}: "
                          f"ghost did not sufficiently advance toward player")

            except AssertionError as ae:
                print(f"FAIL: Component 2 — test_ghost_chases_player() assertion failed: {ae}")
            except Exception as te:
                print(f"ERROR: Component 2 — Failed to run test: {te}")
            finally:
                os.chdir(original_cwd)
                sys.path[:] = original_sys_path
                if module_name in sys.modules:
                    del sys.modules[module_name]

    except Exception as e:
        print(f"ERROR: Component 2 — Outer exception: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

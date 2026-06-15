"""
Reward Script: Fix shuffle bug in Python card game (War)
Task ID: osworld_multi_apps_vscode_debug_game_009
Domain: multi_apps / vscode_debug
Scoring:
  Component 1: shuffle() uses random.shuffle (not sorted) in deck.py — 0.5 pts
  Component 2: Two independent shuffles produce different orders (randomness test) — 0.3 pts
  Component 3: Full test suite (all 7 tests including shuffle + draw + battle) pass — 0.2 pts
  Total: 1.0

Note: All three components FAIL on initial_env (buggy shuffle) and PASS on golden_env (fixed shuffle).
  - Component 1 checks source code directly: sorted() still present → FAIL on initial
  - Component 2 checks runtime behavior: deterministic order → FAIL on initial
  - Component 3 runs ALL 7 unit tests including TestShuffleIsRandom.test_two_shuffles_differ → FAIL on initial
"""

import os
import sys
import re
import importlib.util
import unittest

WORKDIR = '/home/user/Desktop/war_game'
TASK_ID = 'osworld_multi_apps_vscode_debug_game_009'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: Check that the project directory and deck.py exist
    if not os.path.isdir(WORKDIR):
        print(f"CRITICAL: Project directory not found at {WORKDIR}")
        print("REWARD: 0.0")
        return 0.0

    deck_path = os.path.join(WORKDIR, 'deck.py')
    if not os.path.isfile(deck_path):
        print(f"CRITICAL: deck.py not found at {deck_path}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: shuffle() uses random.shuffle (not sorted) in deck.py (0.5 points)
    # The bug was: self.cards = sorted(self.cards) instead of random.shuffle(self.cards)
    # Initial env: uses sorted() → FAIL
    # Golden env: uses random.shuffle() → PASS
    try:
        with open(deck_path, 'r') as f:
            deck_content = f.read()

        uses_random_shuffle = bool(re.search(r'random\.shuffle\s*\(', deck_content))
        uses_sorted_bug = bool(re.search(r'sorted\s*\(\s*self\.cards\s*\)', deck_content))
        uses_deterministic_sort = bool(re.search(r'self\.cards\s*=\s*sorted\s*\(', deck_content))

        if uses_random_shuffle and not uses_sorted_bug and not uses_deterministic_sort:
            print(f"PASS: Component 1 — deck.py shuffle() uses random.shuffle(self.cards), bug is fixed (0.5 pts)")
            total_score += 0.5
        elif uses_sorted_bug or uses_deterministic_sort:
            print(f"FAIL: Component 1 — deck.py shuffle() still uses sorted() (bug not fixed)")
        else:
            print(f"FAIL: Component 1 — deck.py shuffle() does not use random.shuffle. Content snippet: {deck_content[:200]}")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not read deck.py: {e}")

    # Component 2: Two independent shuffles produce different card orders (0.3 points)
    # Directly verifies runtime randomness.
    # Initial env: sorted() makes both shuffles identical → FAIL
    # Golden env: random.shuffle() produces different orders → PASS (with ~1/52! chance of false failure)
    try:
        original_cwd = os.getcwd()
        original_path = sys.path.copy()

        os.chdir(WORKDIR)
        if WORKDIR not in sys.path:
            sys.path.insert(0, WORKDIR)

        # Force reload to pick up any code changes
        for m in list(sys.modules.keys()):
            if m in ('deck', 'card', 'player'):
                del sys.modules[m]

        from deck import Deck

        d1 = Deck()
        d1.shuffle()
        order1 = [str(c) for c in d1.cards]

        d2 = Deck()
        d2.shuffle()
        order2 = [str(c) for c in d2.cards]

        # Clean up imported modules
        for m in ('deck', 'card', 'player'):
            if m in sys.modules:
                del sys.modules[m]

        os.chdir(original_cwd)
        sys.path[:] = original_path

        if order1 != order2:
            print(f"PASS: Component 2 — Two shuffled decks have different orders (shuffle is truly random) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Two shuffled decks have identical orders (shuffle is deterministic/not random)")
            print(f"  First 5 cards of both: {order1[:5]}")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not run shuffle randomness check: {e}")
        try:
            os.chdir(original_cwd)
            sys.path[:] = original_path
        except Exception:
            pass

    # Component 3: Full test suite (all 7 tests) passes — including TestShuffleIsRandom (0.2 points)
    # Runs ALL unit tests from test_war.py (TestShuffleIsRandom + TestDrawLogic + TestBattleLogic).
    # Initial env: TestShuffleIsRandom.test_two_shuffles_differ FAILS → total FAIL → 0 pts
    # Golden env: All 7 tests pass → PASS → 0.2 pts
    # This also verifies that the shuffle fix did NOT break draw/battle logic.
    try:
        original_cwd = os.getcwd()
        original_path = sys.path.copy()

        os.chdir(WORKDIR)
        if WORKDIR not in sys.path:
            sys.path.insert(0, WORKDIR)

        # Force reload
        for m in list(sys.modules.keys()):
            if m in ('deck', 'card', 'player') or m.startswith('test_war'):
                del sys.modules[m]

        test_path = os.path.join(WORKDIR, 'test_war.py')
        spec = importlib.util.spec_from_file_location("test_war_module", test_path)
        test_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(test_module)

        # Run ALL test classes (including shuffle randomness test)
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        suite.addTests(loader.loadTestsFromTestCase(test_module.TestShuffleIsRandom))
        suite.addTests(loader.loadTestsFromTestCase(test_module.TestDrawLogic))
        suite.addTests(loader.loadTestsFromTestCase(test_module.TestBattleLogic))

        import io
        stream = io.StringIO()
        runner = unittest.TextTestRunner(verbosity=0, stream=stream)
        result = runner.run(suite)

        # Clean up
        for m in list(sys.modules.keys()):
            if m.startswith('test_war'):
                del sys.modules[m]
        for m in ('deck', 'card', 'player'):
            if m in sys.modules:
                del sys.modules[m]

        os.chdir(original_cwd)
        sys.path[:] = original_path

        total_tests = result.testsRun
        failures = len(result.failures) + len(result.errors)

        if result.wasSuccessful():
            print(f"PASS: Component 3 — All {total_tests} unit tests pass (shuffle + draw + battle logic) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — {failures} of {total_tests} unit test(s) failed")
            for failure in result.failures:
                print(f"  FAIL: {failure[0]}")
            for error in result.errors:
                print(f"  ERROR: {error[0]}")
    except Exception as e:
        print(f"ERROR: Component 3 — Could not run full unit test suite: {e}")
        try:
            os.chdir(original_cwd)
            sys.path[:] = original_path
        except Exception:
            pass

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

"""
Reward Script: RPG Combat System Bug Fixes and Logging
Task ID: osworld_multi_apps_code_python_game_010
Domain: os / python code
Scoring:
  - Component 1: character.py heal() capped at max_hp          (0.15 pts)
  - Component 2: enemy.py attack() uses self.damage             (0.15 pts)
  - Component 3: combat.py uses enemy.hp not enemy.health       (0.15 pts)
  - Component 4: log_combat() function exists in combat.py      (0.20 pts)
  - Component 5: combat_log.txt exists with >= 3 log entries    (0.20 pts)
  - Component 6: test_combat.py exists and runs printing PASS   (0.15 pts)
  Total: 1.0
"""

import os
import re
import sys

WORKDIR = '/home/user/projects/rpg'
TASK_ID = 'osworld_multi_apps_code_python_game_010'

CHARACTER_PY = os.path.join(WORKDIR, 'character.py')
ENEMY_PY     = os.path.join(WORKDIR, 'enemy.py')
COMBAT_PY    = os.path.join(WORKDIR, 'combat.py')
COMBAT_LOG   = os.path.join(WORKDIR, 'combat_log.txt')
TEST_SCRIPT  = os.path.join(WORKDIR, 'test_combat.py')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: all original Python files must exist
    required_files = [CHARACTER_PY, ENEMY_PY, COMBAT_PY]
    for f in required_files:
        if not os.path.isfile(f):
            print(f"CRITICAL: Required file missing: {f}")
            print("REWARD: 0.0")
            return 0.0

    # -----------------------------------------------------------------
    # Component 1: character.py heal() is capped at max_hp (0.15 pts)
    # The buggy code was: self.hp += amount
    # The fix should use min(..., self.max_hp) to cap hp.
    # -----------------------------------------------------------------
    try:
        with open(CHARACTER_PY, 'r') as fh:
            char_content = fh.read()

        # Extract the heal() method body
        heal_body_lines = []
        parsing_heal = False
        for line in char_content.split('\n'):
            if 'def heal(' in line:
                parsing_heal = True
                heal_body_lines = []
                continue
            if parsing_heal:
                stripped = line.strip()
                # End of method: new def at class level
                if stripped.startswith('def ') and 'heal(' not in stripped:
                    parsing_heal = False
                else:
                    heal_body_lines.append(line)
        heal_body = '\n'.join(heal_body_lines)

        # The fix must use min() with max_hp cap, or an equivalent conditional
        uses_min_cap = bool(re.search(r'min\s*\(', heal_body)) and 'max_hp' in heal_body
        uses_conditional_cap = bool(re.search(r'if\s+self\.hp\s*>', heal_body)) and 'max_hp' in heal_body
        # Reject if still has the plain bug pattern (no capping at all)
        still_buggy = bool(re.search(r'self\.hp\s*\+=\s*amount', heal_body))

        if (uses_min_cap or uses_conditional_cap) and not still_buggy:
            print("PASS: Component 1 — character.py heal() caps hp at max_hp (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — heal() bug not fixed "
                  f"(uses_min_cap={uses_min_cap}, uses_conditional_cap={uses_conditional_cap}, "
                  f"still_buggy={still_buggy})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------
    # Component 2: enemy.py attack() uses self.damage (0.15 pts)
    # The buggy code was: damage_dealt = 10  (hardcoded, ignoring self.damage)
    # The fix must be: damage_dealt = self.damage
    # We inspect the attack() method body specifically.
    # -----------------------------------------------------------------
    try:
        with open(ENEMY_PY, 'r') as fh:
            enemy_content = fh.read()

        # Extract the attack() method body
        attack_body_lines = []
        parsing_attack = False
        for line in enemy_content.split('\n'):
            if 'def attack(' in line:
                parsing_attack = True
                attack_body_lines = []
                continue
            if parsing_attack:
                stripped = line.strip()
                # End of method: new def at class level
                if stripped.startswith('def ') and 'attack(' not in stripped:
                    parsing_attack = False
                else:
                    attack_body_lines.append(line)
        attack_body = '\n'.join(attack_body_lines)

        # The fix: attack() body must assign damage_dealt using self.damage
        fix_applied = bool(re.search(r'damage_dealt\s*=\s*self\.damage', attack_body))
        # Also accept directly returning self.damage
        returns_self_damage = bool(re.search(r'return\s+self\.damage', attack_body))
        # Detect the bug: hardcoded 10 used in damage_dealt assignment
        buggy_assignment = bool(re.search(r'damage_dealt\s*=\s*10\b', attack_body))

        if (fix_applied or returns_self_damage) and not buggy_assignment:
            print("PASS: Component 2 — enemy.py attack() uses self.damage (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — attack() bug not fixed "
                  f"(fix_applied={fix_applied}, returns_self_damage={returns_self_damage}, "
                  f"buggy_assignment={buggy_assignment})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------
    # Component 3: combat.py uses enemy.hp instead of enemy.health (0.15 pts)
    # The buggy code used: enemy.health
    # The fix should use: enemy.hp
    # -----------------------------------------------------------------
    try:
        with open(COMBAT_PY, 'r') as fh:
            combat_content = fh.read()

        still_uses_enemy_health = 'enemy.health' in combat_content
        uses_enemy_hp = 'enemy.hp' in combat_content

        if uses_enemy_hp and not still_uses_enemy_health:
            print("PASS: Component 3 — combat.py uses enemy.hp not enemy.health (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — attribute name bug not fixed "
                  f"(uses_enemy_hp={uses_enemy_hp}, "
                  f"still_uses_enemy_health={still_uses_enemy_health})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -----------------------------------------------------------------
    # Component 4: log_combat() function exists in combat.py (0.20 pts)
    # The task requires adding a log_combat() function that writes to
    # /home/user/projects/rpg/combat_log.txt.
    # -----------------------------------------------------------------
    try:
        with open(COMBAT_PY, 'r') as fh:
            combat_content = fh.read()

        has_log_combat_def = 'def log_combat(' in combat_content
        references_log_file = ('combat_log.txt' in combat_content or
                                'LOG_FILE' in combat_content)

        if has_log_combat_def and references_log_file:
            print("PASS: Component 4 — log_combat() defined in combat.py "
                  "referencing the log file (0.20 pts)")
            total_score += 0.20
        elif has_log_combat_def:
            print("PASS (partial): Component 4 — log_combat() exists but log file "
                  "reference not found (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 — log_combat() not found in combat.py "
                  f"(has_def={has_log_combat_def}, "
                  f"references_log_file={references_log_file})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # -----------------------------------------------------------------
    # Component 5: combat_log.txt exists and has >= 3 log entries (0.20 pts)
    # The task requires the log file to be created with round entries.
    # -----------------------------------------------------------------
    try:
        log_exists = os.path.isfile(COMBAT_LOG)
        if not log_exists:
            print(f"FAIL: Component 5 — combat_log.txt not found at {COMBAT_LOG}")
        else:
            with open(COMBAT_LOG, 'r') as fh:
                log_lines = [line.strip() for line in fh.readlines() if line.strip()]
            num_lines = len(log_lines)
            if num_lines >= 3:
                print(f"PASS: Component 5 — combat_log.txt has {num_lines} entries "
                      f"(>= 3 required) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 5 — combat_log.txt has only {num_lines} lines, "
                      f"need >= 3")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # -----------------------------------------------------------------
    # Component 6: test_combat.py exists and verifiable behavior is correct (0.15 pts)
    # We verify by:
    #   (a) test_combat.py file exists
    #   (b) it imports from the rpg modules (character, enemy, combat)
    #   (c) the imported Character/Enemy/combat behave correctly (bug-free)
    #       - Character.heal() does not exceed max_hp
    #       - Enemy.attack() uses self.damage
    #       - log_combat() creates the log file
    # -----------------------------------------------------------------
    try:
        if not os.path.isfile(TEST_SCRIPT):
            print(f"FAIL: Component 6 — test_combat.py not found at {TEST_SCRIPT}")
        else:
            with open(TEST_SCRIPT, 'r') as fh:
                test_content = fh.read()

            # Check that test_combat.py imports from the required modules
            imports_character = 'from character import' in test_content or 'import character' in test_content
            imports_enemy = 'from enemy import' in test_content or 'import enemy' in test_content
            imports_combat = ('from combat import' in test_content or 'import combat' in test_content)
            has_structure = imports_character and imports_enemy and imports_combat

            # Try to actually run the module logic via importlib (no subprocess)
            # We load the modules dynamically and perform a minimal functional test
            run_passed = False
            run_error = None
            try:
                # Ensure WORKDIR is on sys.path for module resolution
                if WORKDIR not in sys.path:
                    sys.path.insert(0, WORKDIR)

                # Reload fresh module objects to avoid stale state
                import importlib
                for mod_name in ['character', 'enemy', 'combat']:
                    if mod_name in sys.modules:
                        del sys.modules[mod_name]

                char_mod   = importlib.import_module('character')
                enemy_mod  = importlib.import_module('enemy')
                combat_mod = importlib.import_module('combat')

                Character = char_mod.Character
                Enemy     = enemy_mod.Enemy

                # Functional test 1: heal() capped
                hero = Character(name='T', hp=100, max_hp=100, attack=20, defense=0)
                hero.heal(50)  # should not exceed max_hp=100
                heal_capped = (hero.hp <= 100)

                # Functional test 2: enemy.attack() uses self.damage
                goblin = Enemy(name='G', hp=50, damage=15)
                hero2 = Character(name='T2', hp=200, max_hp=200, attack=5, defense=0)
                hp_before = hero2.hp
                goblin.attack(hero2)
                damage_dealt = hp_before - hero2.hp
                enemy_damage_correct = (damage_dealt == 15)  # should be self.damage=15

                # Functional test 3: log_combat() writes to log file
                # Remove log if it exists to test creation
                test_log = os.path.join(WORKDIR, 'combat_log_test_tmp.txt')
                orig_log_file = getattr(combat_mod, 'LOG_FILE', None)

                log_func = getattr(combat_mod, 'log_combat', None)
                log_func_works = False
                if log_func is not None:
                    # Temporarily patch LOG_FILE to write to a temp location
                    if orig_log_file is not None:
                        combat_mod.LOG_FILE = test_log
                    log_func('Round 1: Test action')
                    log_func('Round 2: Test action')
                    log_func('Round 3: Test action')
                    if os.path.isfile(test_log):
                        with open(test_log, 'r') as fh:
                            written_lines = [l.strip() for l in fh.readlines() if l.strip()]
                        log_func_works = (len(written_lines) >= 3)
                        os.remove(test_log)
                    # Restore LOG_FILE
                    if orig_log_file is not None:
                        combat_mod.LOG_FILE = orig_log_file

                if heal_capped and enemy_damage_correct and log_func_works:
                    run_passed = True
                else:
                    run_error = (f"heal_capped={heal_capped}, "
                                 f"enemy_damage_correct={enemy_damage_correct}, "
                                 f"log_func_works={log_func_works}")
            except Exception as exc:
                run_error = str(exc)

            if has_structure and run_passed:
                print("PASS: Component 6 — test_combat.py present with correct imports; "
                      "functional tests passed (0.15 pts)")
                total_score += 0.15
            elif has_structure and not run_passed:
                print(f"FAIL: Component 6 — test_combat.py has structure but functional "
                      f"tests failed: {run_error}")
            else:
                print(f"FAIL: Component 6 — test_combat.py missing expected imports "
                      f"(char={imports_character}, enemy={imports_enemy}, "
                      f"combat={imports_combat})")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

"""
Reward Script: Snake game pause functionality
Task ID: osworld_multi_apps_code_python_game_005
Domain: os / code editing (Python)
Scoring:
  Component 1 (0.35): 'paused' boolean variable initialized in game state
  Component 2 (0.35): P key handler toggles the 'paused' boolean
  Component 3 (0.30): Game loop movement update guarded by 'not paused' condition
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_code_python_game_005'
GAME_FILE = '/home/user/projects/snake/game.py'


def verify_task(file_path):
    """
    Verify that the Snake game now has pause functionality:
    1. A 'paused' boolean variable is initialized in game state
    2. Pressing 'P' toggles the paused boolean
    3. The game loop skips movement updates when paused
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the file
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: 'paused' boolean variable initialized in game state (0.35 points)
    # Must be initialized as False (not True) in the game state setup (before main loop)
    # We look for 'paused = False' as a variable assignment in the main() function body
    try:
        # Check that 'paused = False' appears as an initialization in main()
        # It should appear in the game state section (before the while loop or at least once)
        paused_init_pattern = re.compile(r'\bpaused\s*=\s*False\b')
        paused_init_matches = paused_init_pattern.findall(content)

        if len(paused_init_matches) >= 1:
            print(f"PASS: Component 1 — 'paused = False' initialization found ({len(paused_init_matches)} occurrence(s)) (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — 'paused = False' initialization not found in game.py")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: P key handler that toggles paused boolean (0.35 points)
    # Must have an event handler for pygame.K_p that toggles paused
    # Pattern: event.key == pygame.K_p (followed eventually by paused = not paused)
    try:
        # Check for K_p key detection
        k_p_pattern = re.compile(r'pygame\.K_p\b')
        k_p_found = bool(k_p_pattern.search(content))

        # Check for toggle: paused = not paused
        toggle_pattern = re.compile(r'\bpaused\s*=\s*not\s+paused\b')
        toggle_found = bool(toggle_pattern.search(content))

        if k_p_found and toggle_found:
            print(f"PASS: Component 2 — P key handler found (pygame.K_p) and toggle logic (paused = not paused) present (0.35 pts)")
            total_score += 0.35
        elif k_p_found and not toggle_found:
            print(f"FAIL: Component 2 — pygame.K_p found but no 'paused = not paused' toggle logic")
        elif not k_p_found and toggle_found:
            print(f"FAIL: Component 2 — 'paused = not paused' toggle found but no pygame.K_p handler")
        else:
            print(f"FAIL: Component 2 — Neither pygame.K_p handler nor toggle logic found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Game loop movement skipped when paused (0.30 points)
    # The movement update block must be guarded by 'not paused'
    # Pattern: 'not game_over and not paused' OR 'not paused and not game_over'
    # or nested: 'if not paused:' inside 'if not game_over:'
    try:
        # Check for compound condition: not game_over and not paused (or reversed)
        compound_pattern = re.compile(
            r'not\s+game_over\s+and\s+not\s+paused|not\s+paused\s+and\s+not\s+game_over',
            re.IGNORECASE
        )
        compound_found = bool(compound_pattern.search(content))

        # Also check for nested pattern: if not paused: inside if not game_over:
        # This is a more permissive check for nested conditionals
        nested_pattern = re.compile(
            r'if\s+not\s+game_over.*?if\s+not\s+paused',
            re.DOTALL
        )
        nested_found = bool(nested_pattern.search(content))

        # Also check for: if not paused: (standalone, inside the game_over block)
        standalone_paused_pattern = re.compile(r'if\s+not\s+paused\s*:')
        standalone_found = bool(standalone_paused_pattern.search(content))

        if compound_found:
            print(f"PASS: Component 3 — Movement guarded by compound 'not game_over and not paused' condition (0.30 pts)")
            total_score += 0.30
        elif nested_found:
            print(f"PASS: Component 3 — Movement guarded by nested 'not paused' inside 'not game_over' block (0.30 pts)")
            total_score += 0.30
        elif standalone_found:
            # Verify there's actual movement code after the paused check
            # (not just the restart logic)
            # Check it appears outside the restart block by looking for direction/snake update nearby
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if re.search(r'if\s+not\s+paused\s*:', line):
                    # Check surrounding lines for movement-related code
                    context = '\n'.join(lines[max(0, i):min(len(lines), i+10)])
                    if re.search(r'direction\s*=|new_head|snake_body\.insert', context):
                        print(f"PASS: Component 3 — Movement guarded by standalone 'if not paused:' with movement code (0.30 pts)")
                        total_score += 0.30
                        break
            else:
                print(f"FAIL: Component 3 — 'if not paused' found but not guarding movement update code")
        else:
            print(f"FAIL: Component 3 — No 'not paused' condition found guarding movement updates")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


if not os.path.exists(GAME_FILE):
    print(f"File not found: {GAME_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(GAME_FILE)

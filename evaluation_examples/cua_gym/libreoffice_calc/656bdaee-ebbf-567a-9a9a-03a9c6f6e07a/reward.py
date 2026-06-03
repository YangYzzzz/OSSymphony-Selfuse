"""
Reward Script: Add score display to Tetris game using pygame font rendering
Task ID: osworld_multi_apps_code_python_game_004
Domain: python/pygame (code editing)
Scoring:
  Component 1: draw_screen function calls font.render with score variable (0.4 pts)
  Component 2: surface.blit called to display the rendered score text (0.3 pts)
  Component 3: File is valid Python and imports pygame (no syntax errors) (0.3 pts)
Total: 1.0
"""

import os
import ast
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_code_python_game_004'

FILE_PATH = f'{WORKDIR}/projects/tetris/main.py'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    The task is to add a score display to a Tetris game's draw_screen function
    using pygame's font rendering (font.render + surface.blit).
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: File must exist
    if not os.path.isfile(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Read the file content
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: font.render called with score variable in draw_screen (0.4 pts)
    # The task requires adding pygame font rendering of the score.
    # We check that font.render is called and references the 'score' variable.
    # In initial_env: the draw_screen function only has a comment, no font.render call.
    # In golden_env: font.render(f"Score: {score}", True, WHITE) is added.
    try:
        # Find the draw_screen function body
        draw_screen_match = re.search(
            r'def draw_screen\s*\([^)]*\).*?(?=\ndef |\Z)',
            content,
            re.DOTALL
        )
        if draw_screen_match:
            draw_screen_body = draw_screen_match.group(0)
        else:
            draw_screen_body = content  # fallback: search entire file

        # Check for font.render call that references score
        has_font_render = bool(re.search(r'font\.render\s*\(', draw_screen_body))
        has_score_in_render = bool(re.search(r'font\.render\s*\([^)]*score[^)]*\)', draw_screen_body))

        if has_font_render and has_score_in_render:
            print(f"PASS: Component 1 — font.render called with 'score' variable in draw_screen (0.4 pts)")
            total_score += 0.4
        elif has_font_render:
            # font.render present but might not reference score correctly
            print(f"FAIL: Component 1 — font.render found but 'score' variable not referenced in render call")
        else:
            print(f"FAIL: Component 1 — font.render not found in draw_screen function")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: surface.blit called to display the rendered score text (0.3 pts)
    # In initial_env: draw_screen never calls surface.blit.
    # In golden_env: surface.blit(score_surface, (5, 5)) is present.
    # We verify blit is called in draw_screen with a variable that holds the rendered text.
    try:
        if draw_screen_match:
            ds_body = draw_screen_body
        else:
            ds_body = content

        # Check that surface.blit is called (the surface parameter name varies)
        # In the code the parameter is 'surface' and it calls surface.blit(score_surface, ...)
        has_blit = bool(re.search(r'\.blit\s*\(', ds_body))

        # Additionally verify the blit call uses a variable that was the result of font.render
        # Pattern: score_surface = font.render(...) followed by surface.blit(score_surface, ...)
        has_render_var_blit = bool(re.search(
            r'(\w+)\s*=\s*font\.render\s*\([^)]*\).*?\.blit\s*\(\s*\1\s*,',
            ds_body,
            re.DOTALL
        ))

        if has_blit and has_render_var_blit:
            print(f"PASS: Component 2 — surface.blit called with rendered score surface (0.3 pts)")
            total_score += 0.3
        elif has_blit:
            # blit present but might not reference the render result
            print(f"FAIL: Component 2 — blit called but not with the font.render result variable")
        else:
            print(f"FAIL: Component 2 — surface.blit not found in draw_screen function")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: File is valid Python syntax AND score display was added without the
    # "not displayed" placeholder comment (0.3 pts).
    # In initial_env: the file has a comment saying score "is NOT drawn here" (no render code).
    # In golden_env: that placeholder comment is removed and font.render + blit are present.
    # This component fails on initial_env because the "NOT drawn" comment exists there,
    # and fails if syntax is broken. It passes only when the task is properly completed.
    try:
        # Check syntax by parsing; parse raises SyntaxError if invalid
        parse_error = None
        try:
            ast.parse(content)
        except SyntaxError as se:
            parse_error = se

        if parse_error is not None:
            print(f"FAIL: Component 3 — Syntax error in modified file: {parse_error}")
        else:
            # Check that the "NOT drawn" placeholder comment is gone (indicates task was done)
            # Initial file has: "# NOTE: Score is tracked ... but is NOT drawn here."
            # Golden file removes this comment and adds real rendering code.
            had_no_display_comment = ('NOT drawn' in content or
                                      'is not drawn' in content.lower() or
                                      'is NOT rendered' in content or
                                      'not render' in content.lower())

            # Score display code must also be present (font.render with score + blit)
            score_display_present = (
                bool(re.search(r'font\.render\s*\([^)]*score', content)) and
                bool(re.search(r'\.blit\s*\(', content))
            )

            if score_display_present and not had_no_display_comment:
                print(f"PASS: Component 3 — Valid Python, score display added, placeholder comment removed (0.3 pts)")
                total_score += 0.3
            elif score_display_present:
                print(f"FAIL: Component 3 — Score display added but placeholder comment 'NOT drawn' still present")
            else:
                print(f"FAIL: Component 3 — Valid Python but score display rendering not present or comment not removed")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

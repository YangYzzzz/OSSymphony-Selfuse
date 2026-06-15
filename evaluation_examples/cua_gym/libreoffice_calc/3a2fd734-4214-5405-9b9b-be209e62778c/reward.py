"""
Reward Script: Extract UI button states from strip image and write automation script
Task ID: osworld_multi_apps_gimp_vscode_010
Domain: gimp + vscode (multi-app)
Scoring:
  Component 1: 6 button_N.png files exist, correct size (80x30) — 0.35 pts
  Component 2: 6 button_N_code.png files exist, correct size (80x30) — 0.35 pts
  Component 3: extract_ui.py exists, valid Python, saves _code suffix, handles 6 buttons — 0.15 pts
  Component 4: button_N.png and button_N_code.png are visually similar (MSE similarity >= 0.85) — 0.15 pts
  Total: 1.0
"""

import os
import ast
import math

WORKDIR = '/home/user'
DESKTOP = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_gimp_vscode_010'
STRIP_PATH = os.path.join(DESKTOP, 'ui_elements.png')
SCRIPT_PATH = os.path.join(WORKDIR, 'extract_ui.py')

BUTTON_W = 80
BUTTON_H = 30
NUM_BUTTONS = 6
SIMILARITY_THRESHOLD = 0.85  # task context specifies SSIM >= 0.85


def compute_mse_similarity(arr1, arr2):
    """Compute similarity from MSE: 1.0=identical, lower with more difference.
    Uses exponential decay: sim = exp(-10 * mse).
    MSE=0 -> 1.0; MSE=0.016 -> ~0.85 (threshold).
    """
    a1 = arr1.astype(float) / 255.0
    a2 = arr2.astype(float) / 255.0
    mse = float(((a1 - a2) ** 2).mean())
    return math.exp(-10.0 * mse)


def check_script_properties(script_path):
    """Return count of key implementation properties found in script.
    Returns (syntax_ok, checks_passed, details_dict)."""
    with open(script_path, 'r') as f:
        content = f.read()
    try:
        ast.parse(content)
    except SyntaxError as se:
        return False, 0, {'syntax_error': str(se)}
    has_code_suffix = '_code' in content
    handles_6 = ('6' in content or 'NUM_BUTTONS' in content)
    uses_image = ('Image' in content or 'PIL' in content or 'cv2' in content)
    saves_out = ('.save(' in content or 'imsave' in content or 'imwrite' in content)
    n_pass = sum([has_code_suffix, handles_6, uses_image, saves_out])
    return True, n_pass, {
        '_code_suffix': has_code_suffix,
        'handles_6': handles_6,
        'image_lib': uses_image,
        'saves': saves_out
    }


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from PIL import Image
        import numpy as np
    except ImportError as e:
        print(f"CRITICAL: Cannot import required libraries: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: source image must exist on Desktop
    if not os.path.exists(STRIP_PATH):
        print(f"PRECONDITION FAIL: Source image not found at {STRIP_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: 6 button_N.png files exist and have correct size (0.35 pts)
    # These files should NOT exist in initial_env — they are task-introduced changes
    try:
        button_valid_count = 0
        for i in range(1, NUM_BUTTONS + 1):
            btn_path = os.path.join(DESKTOP, f'button_{i}.png')
            if not os.path.exists(btn_path):
                print(f"FAIL: Component 1 — button_{i}.png not found at {btn_path}")
                continue
            try:
                img = Image.open(btn_path)
                w, h = img.size
                if w == BUTTON_W and h == BUTTON_H:
                    button_valid_count += 1
                    print(f"PASS: button_{i}.png exists, size={w}x{h}")
                else:
                    print(f"FAIL: button_{i}.png wrong size: got {w}x{h}, "
                          f"expected {BUTTON_W}x{BUTTON_H}")
            except Exception as e:
                print(f"ERROR: Cannot open button_{i}.png: {e}")

        comp1_score = round(0.35 * button_valid_count / NUM_BUTTONS, 4)
        if button_valid_count == NUM_BUTTONS:
            print(f"PASS: Component 1 — All 6 button_N.png files present "
                  f"with correct size (0.35 pts)")
        elif button_valid_count > 0:
            print(f"PARTIAL: Component 1 — {button_valid_count}/6 button_N.png valid "
                  f"(+{comp1_score} pts)")
        else:
            print(f"FAIL: Component 1 — No valid button_N.png files found")
        if comp1_score > 0:
            total_score += comp1_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 6 button_N_code.png files exist and have correct size (0.35 pts)
    # These files should NOT exist in initial_env — task-introduced by running extract_ui.py
    try:
        code_valid_count = 0
        for i in range(1, NUM_BUTTONS + 1):
            code_path = os.path.join(DESKTOP, f'button_{i}_code.png')
            if not os.path.exists(code_path):
                print(f"FAIL: Component 2 — button_{i}_code.png not found at {code_path}")
                continue
            try:
                img = Image.open(code_path)
                w, h = img.size
                if w == BUTTON_W and h == BUTTON_H:
                    code_valid_count += 1
                    print(f"PASS: button_{i}_code.png exists, size={w}x{h}")
                else:
                    print(f"FAIL: button_{i}_code.png wrong size: got {w}x{h}, "
                          f"expected {BUTTON_W}x{BUTTON_H}")
            except Exception as e:
                print(f"ERROR: Cannot open button_{i}_code.png: {e}")

        comp2_score = round(0.35 * code_valid_count / NUM_BUTTONS, 4)
        if code_valid_count == NUM_BUTTONS:
            print(f"PASS: Component 2 — All 6 button_N_code.png files present "
                  f"with correct size (0.35 pts)")
        elif code_valid_count > 0:
            print(f"PARTIAL: Component 2 — {code_valid_count}/6 button_N_code.png valid "
                  f"(+{comp2_score} pts)")
        else:
            print(f"FAIL: Component 2 — No valid button_N_code.png files found")
        if comp2_score > 0:
            total_score += comp2_score
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: extract_ui.py exists and is valid Python with correct implementation (0.15 pts)
    # extract_ui.py should NOT exist in initial_env — it is task-introduced
    try:
        if not os.path.exists(SCRIPT_PATH):
            print(f"FAIL: Component 3 — extract_ui.py not found at {SCRIPT_PATH}")
        else:
            syntax_ok, checks_passed, details = check_script_properties(SCRIPT_PATH)
            print(f"INFO: extract_ui.py: syntax_ok={syntax_ok}, checks={details}")
            if not syntax_ok:
                print(f"FAIL: Component 3 — extract_ui.py syntax error: "
                      f"{details.get('syntax_error')}")
            elif checks_passed == 4:
                print(f"PASS: Component 3 — extract_ui.py valid with all required "
                      f"properties (0.15 pts)")
                total_score += 0.15
            elif checks_passed >= 3:
                print(f"PARTIAL: Component 3 — extract_ui.py valid, "
                      f"{checks_passed}/4 property checks passed (+0.075 pts)")
                total_score += 0.075
            else:
                print(f"FAIL: Component 3 — extract_ui.py missing key requirements "
                      f"({checks_passed}/4 checks passed)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: button_N.png and button_N_code.png are visually similar (0.15 pts)
    # Task context requires SSIM >= 0.85; we use MSE-based exponential similarity as proxy.
    # This verifies the _code images are correct counterparts to the manually extracted buttons.
    try:
        if button_valid_count == 0 or code_valid_count == 0:
            print(f"SKIP: Component 4 — Cannot compare, no valid button files found")
        else:
            similar_count = 0
            checked_count = 0
            for i in range(1, NUM_BUTTONS + 1):
                btn_path = os.path.join(DESKTOP, f'button_{i}.png')
                code_path = os.path.join(DESKTOP, f'button_{i}_code.png')
                if not os.path.exists(btn_path) or not os.path.exists(code_path):
                    continue
                try:
                    b = Image.open(btn_path)
                    bc = Image.open(code_path)
                    checked_count += 1
                    if b.size != bc.size:
                        bc = bc.resize(b.size, Image.LANCZOS)
                    arr1 = np.array(b.convert('RGB'))
                    arr2 = np.array(bc.convert('RGB'))
                    sim = compute_mse_similarity(arr1, arr2)
                    if sim >= SIMILARITY_THRESHOLD:
                        similar_count += 1
                        print(f"PASS: button_{i} similarity={sim:.4f} >= {SIMILARITY_THRESHOLD}")
                    else:
                        print(f"FAIL: button_{i} similarity={sim:.4f} < {SIMILARITY_THRESHOLD}")
                except Exception as e:
                    print(f"ERROR: Comparing button_{i}: {e}")

            comp4_score = round(0.15 * similar_count / NUM_BUTTONS, 4) if checked_count > 0 else 0.0
            if checked_count > 0 and similar_count == checked_count:
                print(f"PASS: Component 4 — All {similar_count}/{checked_count} "
                      f"button pairs are visually similar (0.15 pts)")
            elif checked_count > 0 and similar_count > 0:
                print(f"PARTIAL: Component 4 — {similar_count}/{checked_count} "
                      f"pairs similar (+{comp4_score} pts)")
            else:
                print(f"FAIL: Component 4 — No visually similar pairs found")
            if comp4_score > 0:
                total_score += comp4_score
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.4f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


# Entrypoint
verify_task()

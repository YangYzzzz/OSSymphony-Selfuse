"""
Reward Script: GIMP + terminal image processing task
Task ID: osworld_multi_apps_gimp_os_025
Domain: gimp / os
Scoring:
  Component 1 (0.2): cityscape_warm.png exists on Desktop
  Component 2 (0.3): Warm color tone overall (mean Red channel > mean Blue channel)
  Component 3 (0.3): All three vertical sections are individually warm-toned (R > B)
  Component 4 (0.2): Progressive warmth gradient left < right across sections
  Total: 1.0
"""

import os

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_gimp_os_025'

OUTPUT_PATH = os.path.join(WORKDIR, 'cityscape_warm.png')


def verify_task(file_path):
    """
    Verify that cityscape_warm.png is a warm-toned version of cityscape.png
    with progressively stronger warm tones left-to-right across three vertical sections.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: cityscape_warm.png exists on Desktop (0.2 points)
    # This FAILS on initial_env (file not present) and PASSES on golden_env
    try:
        if os.path.isfile(file_path):
            print(f"PASS: Component 1 — cityscape_warm.png exists at {file_path} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — cityscape_warm.png not found at {file_path}")
            # No file means no further checks possible
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Load image for remaining components
    try:
        from PIL import Image
        import numpy as np
        img = Image.open(file_path).convert('RGB')
        arr = np.array(img)
        h, w = arr.shape[:2]
    except Exception as e:
        print(f"CRITICAL: Cannot load image {file_path}: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Overall warm tone — mean Red > mean Blue (0.3 points)
    # Initial cityscape.png is cool (R < B). Golden cityscape_warm.png must be warm (R > B).
    try:
        mean_r = float(arr[:, :, 0].mean())
        mean_g = float(arr[:, :, 1].mean())
        mean_b = float(arr[:, :, 2].mean())
        warmth_score = mean_r - mean_b

        if mean_r > mean_b:
            print(f"PASS: Component 2 — Overall warm tone: mean_R={mean_r:.2f} > mean_B={mean_b:.2f}, "
                  f"warmth(R-B)={warmth_score:.2f} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Expected warm tone (R > B), "
                  f"found mean_R={mean_r:.2f}, mean_B={mean_b:.2f}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All three vertical sections have positive warmth (R > B) (0.3 points)
    # Verifies that the split-and-process step created warm sections throughout.
    # Initial image has cool sections (R < B in all three).
    try:
        section_w = w // 3
        sections = {
            'left':  arr[:, :section_w, :],
            'mid':   arr[:, section_w:2 * section_w, :],
            'right': arr[:, 2 * section_w:, :],
        }
        cool_section_count = 0
        for name, sec in sections.items():
            sec_r = float(sec[:, :, 0].mean())
            sec_b = float(sec[:, :, 2].mean())
            w_sec = sec_r - sec_b
            if sec_r <= sec_b:
                print(f"FAIL: Component 3 — Section '{name}' is not warm: "
                      f"R={sec_r:.2f}, B={sec_b:.2f}, warmth={w_sec:.2f}")
                cool_section_count += 1
            else:
                print(f"  INFO: Section '{name}' is warm: R={sec_r:.2f}, B={sec_b:.2f}, warmth={w_sec:.2f}")

        if cool_section_count == 0:
            print(f"PASS: Component 3 — All three sections are warm-toned (R > B) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — {cool_section_count} section(s) are not warm-toned")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Progressive warmth gradient — left section warmth < right section warmth (0.2 points)
    # The task asks for progressively stronger warm-tone curves left-to-right.
    # Initial image has no such gradient (all sections are cool with similar warmth values).
    try:
        section_w = w // 3
        left_sec  = arr[:, :section_w, :]
        right_sec = arr[:, 2 * section_w:, :]

        left_warmth  = float(left_sec[:, :, 0].mean())  - float(left_sec[:, :, 2].mean())
        right_warmth = float(right_sec[:, :, 0].mean()) - float(right_sec[:, :, 2].mean())

        if left_warmth < right_warmth:
            print(f"PASS: Component 4 — Progressive gradient: left warmth={left_warmth:.2f} < "
                  f"right warmth={right_warmth:.2f} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — Expected left_warmth < right_warmth, "
                  f"found left={left_warmth:.2f}, right={right_warmth:.2f}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: verify the output file on the VM
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_PATH)

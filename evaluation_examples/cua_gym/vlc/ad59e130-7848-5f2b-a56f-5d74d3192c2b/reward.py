"""
FINAL REWARD SCRIPT - SUCCESS
Task: Set subtitle font size to 18pt with Arial font family.
Generated: 2025-09-13 11:39:47
Status: success
Model: azure-o3
Total Steps: 4
"""

import os
import traceback

"""
Reward Verification Script for VLC Subtitle Font Settings
Task: Ensure VLC subtitle font size is set to 18 pt and the font family contains "Arial".
Scoring (progressive):
    • 0.5 points – correct subtitle font size (freetype-fontsize=18)
    • 0.5 points – subtitle font family contains the substring "arial" (case-insensitive)
Returns exactly 1.0 only if BOTH checks pass.
"""

def load_vlcrc(path: str):
    """Parse vlcrc into a dictionary of key → value."""
    config = {}
    if not os.path.isfile(path):
        print(f"✗ VLC config not found at: {path}")
        return config  # Empty dict – verification will fail gracefully

    with open(path, "r", encoding="utf-8", errors="ignore") as fh:
        for raw_line in fh:
            line = raw_line.lstrip()
            if not line or line.startswith("#"):
                continue  # skip comments / blanks
            if "=" not in line:
                continue  # malformed – ignore
            key, value = line.split("=", 1)
            config[key.strip()] = value.strip().strip('"').strip("'")
    return config


def verify_subtitle_settings(cfg: dict, expected_size: str = "18", expected_font_sub: str = "arial") -> float:
    """Return progressive score (0.0–1.0) after performing real checks."""
    score = 0.0

    # 1. Font size check
    size_val = cfg.get("freetype-fontsize", "")
    if size_val:
        if size_val == expected_size:
            print(f"✓ Subtitle font size correctly set to {size_val} pt")
            score += 0.5
        else:
            print(f"✗ Subtitle font size is {size_val} pt (expected {expected_size} pt)")
    else:
        print("✗ 'freetype-fontsize' key missing or empty in vlcrc")

    # 2. Font family check
    font_val = cfg.get("freetype-font", "")
    if font_val:
        if expected_font_sub.lower() in font_val.lower():
            print(f"✓ Subtitle font family contains '{expected_font_sub}': {font_val}")
            score += 0.5
        else:
            print(f"✗ Subtitle font family is '{font_val}' (does not contain '{expected_font_sub}')")
    else:
        print("✗ 'freetype-font' key missing or empty in vlcrc")

    return score


def main():
    vlcrc_path = os.path.expanduser("~/.config/vlc/vlcrc")
    print(f"Loading VLC configuration from: {vlcrc_path}\n")

    cfg = load_vlcrc(vlcrc_path)
    total_score = verify_subtitle_settings(cfg)

    final_score = round(min(total_score, 1.0), 2)

    print(f"\nFinal score: {final_score} / 1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        print("REWARD: 0.0")

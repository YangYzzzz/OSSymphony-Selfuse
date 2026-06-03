"""
FINAL REWARD SCRIPT - SUCCESS
Task: Remove the VLC watermark overlay from the video display area.
Generated: 2025-09-13 09:23:08
Status: success
Model: azure-o3
Total Steps: 16
"""

import os

"""
Reward Script: Verify removal of VLC watermark overlay
-----------------------------------------------------
This script inspects the user-level VLC configuration file (vlcrc) and
checks that every setting related to VLC’s on-screen watermark / logo /
marquee overlay has been disabled.  Three independent conditions are
verified and scored progressively:

1. logo-file (image watermark)            – 0.4 pts
2. marq-marquee (text marquee watermark)  – 0.3 pts
3. video-filter / sub-filter do NOT load  – 0.3 pts
   the “logo” or “marq” filters

A score of 1.0 is returned only when **all** three conditions are met.
Every verification step prints explicit diagnostic information so that
failures are clearly visible in the tool output.
"""

# ---------------------------  helpers  ---------------------------------

def load_vlcrc(path: str) -> dict:
    """Parse vlcrc file into a dict of key -> value (strings)."""
    config = {}
    try:
        with open(path, "r", errors="ignore") as f:
            for raw in f:
                line = raw.rstrip("\n")
                if not line or line.lstrip().startswith("#"):
                    continue  # Skip comments / empty lines
                if "=" not in line:
                    continue  # Not a key=value pair
                key, val = line.split("=", 1)
                config[key.strip()] = val.strip()
    except FileNotFoundError:
        print(f"✗ vlcrc not found at {path}")
    return config


def check_no_logo_file(cfg: dict) -> bool:
    """True when no image watermark is configured."""
    value = cfg.get("logo-file", "")
    if value == "":
        print("✓ watermark image (logo-file) not set")
        return True
    print(f"✗ logo-file is set to '{value}' (watermark still active)")
    return False


def check_no_marquee(cfg: dict) -> bool:
    """True when no text marquee watermark is configured."""
    value = cfg.get("marq-marquee", "")
    if value == "":
        print("✓ marquee text (marq-marquee) not set")
        return True
    print(f"✗ marq-marquee is set to '{value}' (text overlay still active)")
    return False


def check_filters_clean(cfg: dict) -> bool:
    """Ensure filter chains do NOT include 'logo' or 'marq'."""
    offenders = []
    for key in ("video-filter", "sub-filter"):
        value = cfg.get(key, "")
        if value and any(tok in value.lower() for tok in ("logo", "marq")):
            offenders.append((key, value))
    if not offenders:
        print("✓ Neither video-filter nor sub-filter enable watermark filters")
        return True
    for k, v in offenders:
        print(f"✗ {k} contains watermark filters: '{v}'")
    return False


def compute_score(results: list[bool]) -> float:
    """Progressive scoring based on the three boolean results."""
    weights = [0.4, 0.3, 0.3]  # logo-file, marq-marquee, filters
    score = sum(w for passed, w in zip(results, weights) if passed)
    return round(min(score, 1.0), 2)


# ---------------------------  main  ------------------------------------

def verify_task() -> float:
    print("--- VLC Watermark Removal Verification ---")
    vlcrc_path = os.path.expanduser("~/.config/vlc/vlcrc")
    cfg = load_vlcrc(vlcrc_path)

    r_logo   = check_no_logo_file(cfg)
    r_marq   = check_no_marquee(cfg)
    r_filter = check_filters_clean(cfg)

    final_score = compute_score([r_logo, r_marq, r_filter])
    print(f"Computed score: {final_score}")
    return final_score


if __name__ == "__main__":
    reward = verify_task()
    print(f"REWARD: {reward}")

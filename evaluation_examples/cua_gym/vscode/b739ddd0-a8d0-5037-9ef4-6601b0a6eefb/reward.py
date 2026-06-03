"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m tidying up /home/user/scripts/data_processor.py and noticed that lines 10 through 20 are indented four spaces too far—can you help me pull them back to the correct level?
Generated: 2025-09-11 19:42:53
Status: success
Model: azure-o3
Total Steps: 18
"""

import os

# -----------------  CONFIGURATION  -----------------
FILE_PATH = "/home/user/scripts/data_processor.py"
RANGE_START = 10   # first line to check (1-based)
RANGE_END   = 20   # last  line to check (inclusive)
TAB_SIZE    = 4    # how many spaces a tab is worth when counting indents
# ---------------------------------------------------

def _spaces(line: str) -> int:
    """Return the visual indentation (tabs = TAB_SIZE spaces)."""
    count = 0
    for ch in line:
        if ch == " ":
            count += 1
        elif ch == "\t":
            count += TAB_SIZE
        else:
            break
    return count


def _baseline_indent(lines):
    """Indentation of the first non-blank / non-comment line."""
    for txt in lines:
        if txt.strip() and not txt.lstrip().startswith("#"):
            return _spaces(txt)
    return 0


def verify_task(path: str = FILE_PATH,
                start: int = RANGE_START,
                end: int = RANGE_END) -> float:
    """Return progressive score (0-1) verifying indentation fix."""

    print(f"Verifying: {path}")
    score = 0.0

    # ---------- File checks ----------
    if not os.path.isfile(path):
        print("✗ File not found")
        print("REWARD: 0.0")
        return 0.0
    score += 0.2  # minimal progress – file exists

    try:
        with open(path, "r", encoding="utf-8") as fh:
            lines = fh.readlines()
    except Exception as exc:
        print("✗ Cannot read file:", exc)
        print("REWARD: 0.0")
        return 0.0

    if len(lines) < end:
        print(f"✗ File has < {end} lines ({len(lines)})")
        print(f"REWARD: {score:.2f}")
        return score
    score += 0.1      # basic length requirement satisfied

    # ---------- Baseline indent ----------
    baseline = _baseline_indent(lines[:start-1])
    print(f"Baseline indent: {baseline} spaces")

    # ---------- Analyse target range ----------
    significant = [
        (lnum, _spaces(txt))
        for lnum, txt in zip(range(start, end + 1), lines[start-1:end])
        if txt.strip() and not txt.lstrip().startswith("#")
    ]

    if not significant:
        print("✗ No code lines between", start, "and", end)
        print(f"REWARD: {score:.2f}")
        return score

    over_indented = [(ln, ind) for ln, ind in significant if ind - baseline >= 4]
    correctly_indented = [(ln, ind) for ln, ind in significant if ind == baseline]

    if not over_indented:
        print("✓ No lines remain over-indented by ≥4 spaces")
        score += 0.3
    else:
        print("✗ Still over-indented:", over_indented[:5], "…" if len(over_indented) > 5 else "")

    proportion_correct = len(correctly_indented) / len(significant)
    incremental = 0.4 * proportion_correct        # up to 0.4 extra
    score += incremental
    print(f"✓ Correct indent on {len(correctly_indented)}/{len(significant)} lines (+{incremental:.2f})")

    final = round(min(score, 1.0), 2)
    print(f"REWARD: {final}")
    return final


if __name__ == "__main__":
    verify_task()


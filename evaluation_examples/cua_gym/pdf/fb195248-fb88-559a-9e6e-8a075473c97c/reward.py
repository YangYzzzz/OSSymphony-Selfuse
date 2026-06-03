"""
FINAL REWARD SCRIPT - SUCCESS
Task: Please perform OCR on the low-resolution scanned PDF 'old_manuscript.pdf' (100 DPI) in /home/user/Archives using enhanced OCR settings. Save to 'manuscript_text.txt'.
Generated: 2025-11-29 10:11:49
Status: success
Model: o3
Total Steps: 9
"""

# Reward script for verifying OCR extraction of old_manuscript.pdf
# --------------------------------------------------------------
# This script awards up to 1.0 points when:
#   1) The OCR output file `manuscript_text.txt` exists in /home/user/Archives
#   2) The extracted text is long enough to be credible (≥100 chars)         (0.20)
#   3) Four key phrases that should appear after correct OCR are present     (4×0.20)
#      • aged manuscript
#      • ocr demonstration
#      • scanned copy
#      • 100 dpi
# No points are given for mere file existence. All checks are falsifiable.  
# --------------------------------------------------------------

import re
from pathlib import Path

# Paths
TXT_PATH = Path('/home/user/Archives/manuscript_text.txt')

# Keywords we expect to find if OCR succeeded
KEYWORDS = [
    'aged manuscript',
    'ocr demonstration',
    'scanned copy',
    '100 dpi'
]


def _normalize(txt: str) -> str:
    """Lower-case text with condensed whitespace for robust searching."""
    return re.sub(r"\s+", " ", txt).strip().lower()


def verify_task() -> float:
    """Return a progressive score in [0.0, 1.0] based on OCR quality."""
    max_score = 1.0
    score = 0.0

    # ----------------------------------------------------------
    # 1. Fundamental prerequisite: TXT must exist (0 points)
    # ----------------------------------------------------------
    if not TXT_PATH.exists():
        print(f"✗ Missing OCR output file: {TXT_PATH}")
        print("REWARD: 0.0")
        return 0.0
    print(f"✓ Found OCR text file: {TXT_PATH}")

    # ----------------------------------------------------------
    # 2. Load the text content safely
    # ----------------------------------------------------------
    try:
        content = TXT_PATH.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        print(f"✗ Error reading text file: {e}")
        print("REWARD: 0.0")
        return 0.0

    norm = _normalize(content)
    print(f"Normalized text length: {len(norm)} characters")

    # ----------------------------------------------------------
    # 3. Length check (0.20 if ≥100 characters)
    # ----------------------------------------------------------
    if len(norm) >= 100:
        score += 0.20
        print("✓ Text length ≥ 100 chars (+0.20)")
    else:
        print("✗ Text too short (<100 chars)")

    # ----------------------------------------------------------
    # 4. Keyword verification (0.20 each, total 0.80)
    # ----------------------------------------------------------
    per_kw = 0.80 / len(KEYWORDS)
    for kw in KEYWORDS:
        if kw in norm:
            score += per_kw
            print(f"✓ Found keyword '{kw}' (+{per_kw:.2f})")
        else:
            print(f"✗ Missing keyword '{kw}'")

    # ----------------------------------------------------------
    # 5. Final score capping & output
    # ----------------------------------------------------------
    final_score = min(score, max_score)
    print(f"Total score: {score} → Capped: {final_score}")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_task()

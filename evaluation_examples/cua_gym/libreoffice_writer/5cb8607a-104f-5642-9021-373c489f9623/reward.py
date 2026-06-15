"""
Reward Script: Interleave English/Spanish paragraphs with spacing
Task ID: wrpara_045
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.50): Paragraph ordering — interleaved E1, S1, E2, S2, E3, S3, E4, S4
    Only counts a pair (En, Sn) as correct if BOTH are in the right position.
  - Component 2 (0.25): 18pt spacing before each English paragraph at correct position
  - Component 3 (0.25): Explicit 0pt spacing before each Spanish paragraph at correct position
"""

import os

from docx import Document
from docx.shared import Pt

WORKDIR = '/home/user'
TASK_ID = 'wrpara_045'

# Known paragraph start texts for ordering verification
ENGLISH_STARTS = [
    "The Amazon rainforest",
    "Renewable energy sources",
    "The human brain contains",
    "Urban agriculture is transforming",
]

SPANISH_STARTS = [
    "La selva amazonica",
    "Las fuentes de energia",
    "El cerebro humano contiene",
    "La agricultura urbana",
]

# Expected interleaved order (after title at index 0):
# content[0]=E1, content[1]=S1, content[2]=E2, content[3]=S2, ...
EXPECTED_ORDER = []
for eng, spa in zip(ENGLISH_STARTS, SPANISH_STARTS):
    EXPECTED_ORDER.append(("english", eng))
    EXPECTED_ORDER.append(("spanish", spa))


def persist_app_state(domain):
    """Best-effort save of any open LibreOffice document."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print(f"PERSIST: ctrl+s sent for {domain}")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paras = doc.paragraphs
    if len(paras) < 9:
        print(f"FAIL: Expected at least 9 paragraphs, found {len(paras)}")
        print("REWARD: 0.0")
        return 0.0

    content_paras = paras[1:9]

    # Component 1: Paragraph ordering — interleaved pairs (0.50 points)
    # Score per PAIR (En + Sn both correct) = 0.50 / 4 = 0.125
    # This ensures coincidental single-position matches don't score.
    try:
        ordering_score = 0.0
        per_pair = 0.50 / 4.0
        for pair_idx in range(4):
            eng_ci = pair_idx * 2      # content index for English
            spa_ci = pair_idx * 2 + 1  # content index for Spanish
            eng_text = content_paras[eng_ci].text.strip()
            spa_text = content_paras[spa_ci].text.strip()
            eng_ok = eng_text.startswith(ENGLISH_STARTS[pair_idx])
            spa_ok = spa_text.startswith(SPANISH_STARTS[pair_idx])
            if eng_ok and spa_ok:
                ordering_score += per_pair
                print(f"PASS: Pair {pair_idx+1} — E{pair_idx+1} at P{eng_ci+1}, S{pair_idx+1} at P{spa_ci+1} ({per_pair:.4f} pts)")
            else:
                print(f"FAIL: Pair {pair_idx+1} — E{pair_idx+1} ok={eng_ok}, S{pair_idx+1} ok={spa_ok}")
        total_score += ordering_score
        print(f"Component 1 subtotal: {ordering_score:.4f}/0.50")
    except Exception as e:
        print(f"ERROR: Component 1 (ordering) — {e}")

    # Component 2: 18pt spacing before each English paragraph (0.25 points)
    # Only score if the paragraph at that position is actually the correct English paragraph
    # AND has 18pt spacing. This combined check ensures initial state scores 0.
    try:
        eng_spacing_score = 0.0
        per_eng = 0.25 / 4.0
        for pair_idx in range(4):
            eng_ci = pair_idx * 2
            para = content_paras[eng_ci]
            para_text = para.text.strip()
            is_correct_eng = para_text.startswith(ENGLISH_STARTS[pair_idx])
            sb = para.paragraph_format.space_before
            has_18pt = sb is not None and abs(sb.pt - 18.0) < 0.5
            if is_correct_eng and has_18pt:
                eng_spacing_score += per_eng
                print(f"PASS: E{pair_idx+1} at P{eng_ci+1} space_before={sb.pt}pt ({per_eng:.4f} pts)")
            else:
                sb_val = sb.pt if (sb is not None) else "None"
                print(f"FAIL: E{pair_idx+1} at P{eng_ci+1} — correct_eng={is_correct_eng}, space_before={sb_val}")
        total_score += eng_spacing_score
        print(f"Component 2 subtotal: {eng_spacing_score:.4f}/0.25")
    except Exception as e:
        print(f"ERROR: Component 2 (English spacing) — {e}")

    # Component 3: Explicit 0pt spacing before each Spanish paragraph (0.25 points)
    # Only score if: (a) Spanish paragraph is at correct position, (b) has explicit 0pt spacing,
    # AND (c) the preceding English paragraph is also correctly positioned.
    # The (c) condition ensures that coincidental matches in the initial state don't score.
    try:
        spa_spacing_score = 0.0
        per_spa = 0.25 / 4.0
        for pair_idx in range(4):
            eng_ci = pair_idx * 2
            spa_ci = pair_idx * 2 + 1
            para = content_paras[spa_ci]
            para_text = para.text.strip()
            eng_text = content_paras[eng_ci].text.strip()
            is_correct_spa = para_text.startswith(SPANISH_STARTS[pair_idx])
            is_correct_eng = eng_text.startswith(ENGLISH_STARTS[pair_idx])
            sb = para.paragraph_format.space_before
            # Must be explicitly set to 0 (not None/inherited)
            has_explicit_zero = sb is not None and abs(sb.pt) < 0.5
            if is_correct_spa and is_correct_eng and has_explicit_zero:
                spa_spacing_score += per_spa
                print(f"PASS: S{pair_idx+1} at P{spa_ci+1} space_before={sb.pt}pt (explicit 0) ({per_spa:.4f} pts)")
            else:
                sb_val = sb.pt if (sb is not None) else "None (inherited)"
                print(f"FAIL: S{pair_idx+1} at P{spa_ci+1} — correct_spa={is_correct_spa}, correct_eng={is_correct_eng}, space_before={sb_val}")
        total_score += spa_spacing_score
        print(f"Component 3 subtotal: {spa_spacing_score:.4f}/0.25")
    except Exception as e:
        print(f"ERROR: Component 3 (Spanish spacing) — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

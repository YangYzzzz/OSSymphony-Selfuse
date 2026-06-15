"""
Reward Script: Split first paragraph into individual sentences with 6pt spacing
Task ID: wrpara_015
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): First paragraph split into 5 separate single-sentence paragraphs
  Component 2 (0.3): Each of the 5 new paragraphs has space_after ~6pt (76200 EMU)
  Component 3 (0.3): Original paragraphs 2 and 3 remain unchanged
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'wrpara_015'

# The 5 expected sentence starts from the original first paragraph
EXPECTED_SENTENCE_STARTS = [
    "Renewable energy sources have become",
    "Solar power installations have grown",
    "Wind energy now accounts for",
    "Governments around the world have implemented",
    "The transition to renewable energy is expected",
]

# The original paragraphs 2 and 3 that should remain unchanged
ORIGINAL_PARA2_START = "Energy storage remains one of the most significant challenges"
ORIGINAL_PARA3_START = "The economic impact of the renewable energy transition"


def persist_app_state(domain):
    """Save any unsaved changes in LibreOffice before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
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
    from docx import Document
    from docx.shared import Pt

    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paras = doc.paragraphs
    num_paras = len(paras)
    print(f"INFO: Document has {num_paras} paragraphs")

    # Component 1: First paragraph split into 5 separate single-sentence paragraphs (0.4 points)
    # The initial doc has 3 paragraphs; the golden should have 7 (5 from split + 2 original).
    # We check that paragraphs 0-4 each start with the expected sentence text.
    try:
        if num_paras < 7:
            print(f"FAIL: Component 1 — Expected at least 7 paragraphs, found {num_paras}")
        else:
            matched = 0
            for idx, expected_start in enumerate(EXPECTED_SENTENCE_STARTS):
                para_text = paras[idx].text.strip()
                if para_text.startswith(expected_start):
                    # Verify it's a single sentence (contains roughly one period at the end)
                    # A single sentence paragraph should only have one sentence
                    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', para_text) if s.strip()]
                    if len(sentences) == 1:
                        matched += 1
                    else:
                        print(f"FAIL: Component 1 — Para {idx} has {len(sentences)} sentences, expected 1")
                else:
                    print(f"FAIL: Component 1 — Para {idx} expected to start with '{expected_start[:50]}...', found '{para_text[:50]}...'")

            if matched == 5:
                print(f"PASS: Component 1 — All 5 sentences correctly split into separate paragraphs (0.4 pts)")
                total_score += 0.4
            elif matched >= 3:
                partial = round(0.4 * matched / 5, 2)
                print(f"PARTIAL: Component 1 — {matched}/5 sentences correctly split ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 1 — Only {matched}/5 sentences correctly split")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Each of the 5 new paragraphs has space_after ~6pt / 76200 EMU (0.3 points)
    # 6pt = 76200 EMU. We allow a small tolerance (within 5% or ~3800 EMU).
    try:
        if num_paras < 7:
            print(f"FAIL: Component 2 — Not enough paragraphs to check spacing")
        else:
            spacing_ok = 0
            target_emu = 76200  # 6pt in EMU
            tolerance = 5000  # small tolerance for rounding

            for idx in range(5):
                sa = paras[idx].paragraph_format.space_after
                if sa is not None and abs(sa - target_emu) <= tolerance:
                    spacing_ok += 1
                else:
                    print(f"FAIL: Component 2 — Para {idx} space_after={sa}, expected ~{target_emu} (6pt)")

            if spacing_ok == 5:
                print(f"PASS: Component 2 — All 5 new paragraphs have 6pt spacing after (0.3 pts)")
                total_score += 0.3
            elif spacing_ok >= 3:
                partial = round(0.3 * spacing_ok / 5, 2)
                print(f"PARTIAL: Component 2 — {spacing_ok}/5 paragraphs have correct spacing ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — Only {spacing_ok}/5 paragraphs have correct spacing")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Original paragraphs 2 and 3 remain unchanged (0.3 points)
    # In the golden doc, these should be at index 5 and 6.
    # We check text starts and that space_after is NOT set (None or 0).
    try:
        if num_paras < 7:
            print(f"FAIL: Component 3 — Not enough paragraphs to verify unchanged paras")
        else:
            unchanged_count = 0

            # Check paragraph at index 5 (originally para 2)
            p5_text = paras[5].text.strip()
            if p5_text.startswith(ORIGINAL_PARA2_START):
                # Verify it still has multiple sentences (was not split)
                sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', p5_text) if s.strip()]
                if len(sentences) >= 3:
                    unchanged_count += 1
                else:
                    print(f"FAIL: Component 3 — Para 5 has only {len(sentences)} sentences, expected >=3 (original para 2)")
            else:
                print(f"FAIL: Component 3 — Para 5 expected to start with '{ORIGINAL_PARA2_START[:50]}...', found '{p5_text[:50]}...'")

            # Check paragraph at index 6 (originally para 3)
            p6_text = paras[6].text.strip()
            if p6_text.startswith(ORIGINAL_PARA3_START):
                sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', p6_text) if s.strip()]
                if len(sentences) >= 3:
                    unchanged_count += 1
                else:
                    print(f"FAIL: Component 3 — Para 6 has only {len(sentences)} sentences, expected >=3 (original para 3)")
            else:
                print(f"FAIL: Component 3 — Para 6 expected to start with '{ORIGINAL_PARA3_START[:50]}...', found '{p6_text[:50]}...'")

            if unchanged_count == 2:
                print(f"PASS: Component 3 — Original paragraphs 2 and 3 remain unchanged (0.3 pts)")
                total_score += 0.3
            elif unchanged_count == 1:
                print(f"PARTIAL: Component 3 — Only 1/2 original paragraphs verified (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — Neither original paragraph found at expected positions")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

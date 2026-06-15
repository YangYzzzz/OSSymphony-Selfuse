"""
Reward Script: Heading 2 paragraph formatting — keep with next + 0.5 cm space above
Task ID: writer_fs_042
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): All Heading 2 paragraphs have space_before ~0.5 cm
  Component 2 (0.5): All Heading 2 paragraphs have keep_with_next explicitly True
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_fs_042'


def persist_app_state(domain: str):
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
    total_score = 0.0

    try:
        from docx import Document
    except ImportError:
        print("CRITICAL: python-docx not available")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find all Heading 2 paragraphs
    h2_paras = [p for p in doc.paragraphs if p.style and p.style.name == 'Heading 2']
    if not h2_paras:
        print("FAIL: No Heading 2 paragraphs found in document")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found {len(h2_paras)} Heading 2 paragraphs")

    # Component 1: All Heading 2 paragraphs have space_before ~0.5 cm (0.5 points)
    # 0.5 cm = 180000 EMU (1 cm = 360000 EMU). Accept tolerance of ~10%.
    # Initial state: space_before = 0 (explicitly set to 0) -> FAIL
    # Golden state: space_before ~179705 (~0.499 cm) -> PASS
    TARGET_SPACE_BEFORE_EMU = 180000  # 0.5 cm
    TOLERANCE_EMU = 18000  # ~0.05 cm tolerance (10%)
    try:
        h2_space_pass = 0
        for para in h2_paras:
            sb = para.paragraph_format.space_before
            if sb is not None and abs(sb - TARGET_SPACE_BEFORE_EMU) <= TOLERANCE_EMU:
                h2_space_pass += 1
            else:
                sb_cm = round(sb / 360000, 3) if sb is not None else None
                print(f"  DETAIL: Heading 2 '{para.text[:40]}' space_before={sb} ({sb_cm} cm)")

        if h2_space_pass == len(h2_paras):
            print(f"PASS: Component 1 — All {len(h2_paras)} Heading 2 paragraphs have ~0.5 cm space above (0.5 pts)")
            total_score += 0.5
        elif h2_space_pass > 0:
            partial = round(0.5 * h2_space_pass / len(h2_paras), 2)
            print(f"PARTIAL: Component 1 — {h2_space_pass}/{len(h2_paras)} Heading 2 paragraphs have ~0.5 cm space above ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No Heading 2 paragraphs have ~0.5 cm space above")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All Heading 2 paragraphs have keep_with_next == True (0.5 points)
    # Initial state: keep_with_next = None (inherits from style, but not explicitly set) -> FAIL
    # Golden state: keep_with_next = True (explicitly set) -> PASS
    try:
        h2_keep_pass = 0
        for para in h2_paras:
            kwn = para.paragraph_format.keep_with_next
            if kwn is True:
                h2_keep_pass += 1
            else:
                print(f"  DETAIL: Heading 2 '{para.text[:40]}' keep_with_next={kwn}")

        if h2_keep_pass == len(h2_paras):
            print(f"PASS: Component 2 — All {len(h2_paras)} Heading 2 paragraphs have keep_with_next=True (0.5 pts)")
            total_score += 0.5
        elif h2_keep_pass > 0:
            partial = round(0.5 * h2_keep_pass / len(h2_paras), 2)
            print(f"PARTIAL: Component 2 — {h2_keep_pass}/{len(h2_paras)} Heading 2 paragraphs have keep_with_next=True ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No Heading 2 paragraphs have keep_with_next=True")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
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

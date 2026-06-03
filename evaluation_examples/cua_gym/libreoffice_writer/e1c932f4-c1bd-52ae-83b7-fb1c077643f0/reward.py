"""
Reward Script: Change TOC tab leader from dots to dashes for all levels
Task ID: writer_mt_063
Domain: libreoffice_writer
Scoring:
  Component 1: TOC 1 entries use DASHES leader (0.35 pts)
  Component 2: TOC 2 entries use DASHES leader (0.35 pts)
  Component 3: TOC 3 entries use DASHES leader (0.30 pts)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_mt_063'

# WD_TAB_LEADER enum values:
# DOTS = 1, DASHES = 2, LINES = 3, HEAVY = 4, SPACES = 0
LEADER_DASHES = 2


def persist_app_state():
    """Save any unsaved LibreOffice changes before verification."""
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        import time
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
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
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Gather TOC paragraphs grouped by level
    toc_levels = {'TOC 1': [], 'TOC 2': [], 'TOC 3': []}
    for para in doc.paragraphs:
        style_name = para.style.name if para.style else ''
        if style_name in toc_levels:
            toc_levels[style_name].append(para)

    # Precondition: TOC paragraphs exist
    total_toc = sum(len(v) for v in toc_levels.values())
    if total_toc == 0:
        print("FAIL: No TOC paragraphs found in document")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: TOC 1 entries have DASHES leader (0.35 points)
    try:
        toc1_paras = toc_levels['TOC 1']
        if len(toc1_paras) == 0:
            print("FAIL: Component 1 — No TOC 1 paragraphs found")
        else:
            all_dashes = True
            for para in toc1_paras:
                has_right_tab_with_dashes = False
                for ts in para.paragraph_format.tab_stops:
                    if ts.alignment is not None and int(ts.alignment) == 2:  # RIGHT
                        if ts.leader is not None and int(ts.leader) == LEADER_DASHES:
                            has_right_tab_with_dashes = True
                if not has_right_tab_with_dashes:
                    all_dashes = False
                    break
            if all_dashes:
                print(f"PASS: Component 1 — All {len(toc1_paras)} TOC 1 entries use DASHES leader (0.35 pts)")
                total_score += 0.35
            else:
                # Check what leader they have for diagnostic
                leaders = set()
                for para in toc1_paras:
                    for ts in para.paragraph_format.tab_stops:
                        if ts.alignment is not None and int(ts.alignment) == 2:
                            leaders.add(int(ts.leader) if ts.leader is not None else None)
                print(f"FAIL: Component 1 — TOC 1 entries do not all use DASHES. Found leaders: {leaders}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: TOC 2 entries have DASHES leader (0.35 points)
    try:
        toc2_paras = toc_levels['TOC 2']
        if len(toc2_paras) == 0:
            print("FAIL: Component 2 — No TOC 2 paragraphs found")
        else:
            all_dashes = True
            for para in toc2_paras:
                has_right_tab_with_dashes = False
                for ts in para.paragraph_format.tab_stops:
                    if ts.alignment is not None and int(ts.alignment) == 2:
                        if ts.leader is not None and int(ts.leader) == LEADER_DASHES:
                            has_right_tab_with_dashes = True
                if not has_right_tab_with_dashes:
                    all_dashes = False
                    break
            if all_dashes:
                print(f"PASS: Component 2 — All {len(toc2_paras)} TOC 2 entries use DASHES leader (0.35 pts)")
                total_score += 0.35
            else:
                leaders = set()
                for para in toc2_paras:
                    for ts in para.paragraph_format.tab_stops:
                        if ts.alignment is not None and int(ts.alignment) == 2:
                            leaders.add(int(ts.leader) if ts.leader is not None else None)
                print(f"FAIL: Component 2 — TOC 2 entries do not all use DASHES. Found leaders: {leaders}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: TOC 3 entries have DASHES leader (0.30 points)
    try:
        toc3_paras = toc_levels['TOC 3']
        if len(toc3_paras) == 0:
            print("FAIL: Component 3 — No TOC 3 paragraphs found")
        else:
            all_dashes = True
            for para in toc3_paras:
                has_right_tab_with_dashes = False
                for ts in para.paragraph_format.tab_stops:
                    if ts.alignment is not None and int(ts.alignment) == 2:
                        if ts.leader is not None and int(ts.leader) == LEADER_DASHES:
                            has_right_tab_with_dashes = True
                if not has_right_tab_with_dashes:
                    all_dashes = False
                    break
            if all_dashes:
                print(f"PASS: Component 3 — All {len(toc3_paras)} TOC 3 entries use DASHES leader (0.30 pts)")
                total_score += 0.30
            else:
                leaders = set()
                for para in toc3_paras:
                    for ts in para.paragraph_format.tab_stops:
                        if ts.alignment is not None and int(ts.alignment) == 2:
                            leaders.add(int(ts.leader) if ts.leader is not None else None)
                print(f"FAIL: Component 3 — TOC 3 entries do not all use DASHES. Found leaders: {leaders}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state()

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

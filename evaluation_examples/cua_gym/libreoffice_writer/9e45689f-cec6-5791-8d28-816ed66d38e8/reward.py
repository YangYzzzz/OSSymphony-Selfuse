"""
Reward Script: Change TOC leader characters to none (blank space)
Task ID: writer_mt_080
Domain: libreoffice_writer
Scoring:
  Component 1 (0.6): All TOC entries have right-aligned tab stops with NO dot leader
  Component 2 (0.4): Tab stops still right-aligned and at correct position (structure preserved)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_mt_080'


def persist_app_state(domain: str):
    """Save any unsaved GUI edits before verification."""
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

    Scoring rubric:
      Component 1 (0.6 pts): TOC entry tab stops have NO dot/dash/other leader
        - Check all TOC paragraphs (those with tab + page number pattern)
        - Each must have leader that is NOT 'dot', 'hyphen', 'underscore', 'middleDot'
        - Partial credit: proportional to fraction of entries fixed
      Component 2 (0.4 pts): Tab stops are right-aligned at correct position (preserved structure)
        - Ensures the right-alignment and position were not destroyed
        - Partial credit: proportional to fraction of entries correct
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

    # Identify TOC entries: paragraphs after "Table of Contents" heading
    # that contain a tab character followed by a page number
    import re
    toc_start = None
    toc_entries = []

    for i, para in enumerate(doc.paragraphs):
        if toc_start is None:
            # Look for the TOC heading
            if para.style and 'Heading' in para.style.name and 'table of contents' in para.text.lower():
                toc_start = i
                continue
        else:
            # After TOC heading, collect entries with tab + number pattern
            text = para.text.strip()
            if not text:
                continue
            # TOC entry pattern: text followed by tab and page number
            if '\t' in text and re.search(r'\t\d+$', text):
                toc_entries.append((i, para))
            else:
                # End of TOC section (non-TOC paragraph encountered)
                break

    if not toc_entries:
        print("CRITICAL: No TOC entries found in document")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found {len(toc_entries)} TOC entries")

    # Define forbidden leader values (the ones that should NOT be present)
    ns_w = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    FORBIDDEN_LEADERS = {'dot', 'hyphen', 'underscore', 'middleDot', 'heavy'}

    # Component 1: TOC entries have NO dot/dash leader (0.6 points)
    # This is the core task change: initial has dot leaders, golden has none
    try:
        no_leader_count = 0
        for idx, para in toc_entries:
            pPr = para._element.find(f'{{{ns_w}}}pPr')
            if pPr is None:
                continue
            tabs_el = pPr.find(f'{{{ns_w}}}tabs')
            if tabs_el is None:
                # No tabs element means no explicit leader - counts as no leader
                no_leader_count += 1
                continue

            found_forbidden = any(
                tab.get(f'{{{ns_w}}}leader', '') in FORBIDDEN_LEADERS
                for tab in tabs_el.findall(f'{{{ns_w}}}tab')
            )
            if found_forbidden:
                print(f"  FAIL: Para {idx} has forbidden leader: {para.text[:40]}")
            else:
                no_leader_count += 1

        fraction_clean = no_leader_count / len(toc_entries)
        comp1_score = 0.6 * fraction_clean
        if fraction_clean == 1.0:
            print(f"PASS: Component 1 -- All {len(toc_entries)} TOC entries have no dot/dash leader ({comp1_score:.2f} pts)")
        else:
            print(f"PARTIAL: Component 1 -- {no_leader_count}/{len(toc_entries)} entries have no leader ({comp1_score:.2f} pts)")
        if comp1_score > 0:
            total_score += comp1_score
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Tab stops are right-aligned and at correct position (0.4 points)
    # Verifies structure is preserved: right-aligned tab AND no leader (combined check)
    # This FAILS on initial because initial has dot leaders
    try:
        from docx.enum.text import WD_TAB_ALIGNMENT
        correct_count = 0
        for idx, para in toc_entries:
            matching_tabs = [
                ts for ts in para.paragraph_format.tab_stops
                if (ts.alignment == WD_TAB_ALIGNMENT.RIGHT
                    and ts.leader is not None
                    and int(ts.leader) == 0)
            ]
            if len(matching_tabs) > 0:
                correct_count += 1

        fraction_correct = correct_count / len(toc_entries)
        comp2_score = 0.4 * fraction_correct
        if fraction_correct == 1.0:
            print(f"PASS: Component 2 -- All {len(toc_entries)} entries have right-aligned tab with no leader ({comp2_score:.2f} pts)")
        else:
            print(f"PARTIAL: Component 2 -- {correct_count}/{len(toc_entries)} entries correct ({comp2_score:.2f} pts)")
        if comp2_score > 0:
            total_score += comp2_score
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
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

"""
Reward Script: Generate Table of Contents in Writer document
Task ID: writer_rd_029
Domain: libreoffice_writer
Scoring:
  Component 1: TOC title "Table of Contents" as Heading 1 (0.20 pts)
  Component 2: TOC entries exist with dotted tab leaders (0.25 pts)
  Component 3: Right-aligned tab stops on TOC entries (0.25 pts)
  Component 4: Progressive indentation across 3 levels (0.15 pts)
  Component 5: Document grew (TOC paragraphs added) (0.15 pts)
"""

import os
import time


WORKDIR = '/home/user'
TASK_ID = 'writer_rd_029'


def persist_app_state(domain: str):
    """Best-effort save of any open LibreOffice document."""
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print("PERSIST: ctrl+s sent for libreoffice_writer")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify that a Table of Contents was inserted at the beginning of the document.
    Checks: TOC title, TOC entries with dotted leaders, right-aligned tabs,
    progressive indentation, and document growth.
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

    paragraphs = doc.paragraphs

    # ---------------------------------------------------------------
    # Component 1: TOC title "Table of Contents" as Heading 1 (0.20 pts)
    # In the initial doc, there is NO paragraph with "Table of Contents" text.
    # In the golden doc, P7 has style=Heading 1 and text="Table of Contents".
    # ---------------------------------------------------------------
    try:
        toc_title_score = 0.0
        for para in paragraphs[:20]:  # TOC title should be near the top
            if 'table of contents' in para.text.lower().strip():
                style_name = para.style.name if para.style else ''
                print(f"PASS: Component 1 — TOC title found: '{para.text}' style={style_name} (0.20 pts)")
                toc_title_score = 0.20
                break
        if toc_title_score > 0:
            total_score += toc_title_score
        else:
            print("FAIL: Component 1 — No 'Table of Contents' title found in first 20 paragraphs")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ---------------------------------------------------------------
    # Component 2: TOC entries with dotted tab leaders (0.25 pts)
    # Initial doc has 0 paragraphs with dotted tab leaders.
    # Golden doc has 33 TOC entries with DOTS leaders.
    # We require at least 15 entries with dotted leaders to pass.
    # ---------------------------------------------------------------
    try:
        dotted_entries = []
        for i, para in enumerate(paragraphs):
            for ts in para.paragraph_format.tab_stops:
                if ts.leader is not None and str(ts.leader) == 'DOTS (1)':
                    dotted_entries.append(i)
                    break

        num_dotted = len(dotted_entries)
        if num_dotted >= 15:
            print(f"PASS: Component 2 — {num_dotted} TOC entries with dotted leaders found (0.25 pts)")
            total_score += 0.25
        elif num_dotted >= 5:
            partial = 0.25 * (num_dotted / 25.0)
            print(f"PARTIAL: Component 2 — {num_dotted} dotted entries (partial: {partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Only {num_dotted} entries with dotted leaders, expected >=15")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ---------------------------------------------------------------
    # Component 3: Right-aligned tab stops on TOC entries (0.25 pts)
    # Initial doc has no right-aligned dotted tab stops.
    # Golden doc has RIGHT (2) alignment on all TOC entry tab stops.
    # ---------------------------------------------------------------
    try:
        right_aligned_count = 0
        for i in dotted_entries:
            para = paragraphs[i]
            for ts in para.paragraph_format.tab_stops:
                if str(ts.leader) == 'DOTS (1)' and str(ts.alignment) == 'RIGHT (2)':
                    right_aligned_count += 1
                    break

        if num_dotted > 0 and right_aligned_count >= num_dotted * 0.8:
            print(f"PASS: Component 3 — {right_aligned_count}/{num_dotted} entries have right-aligned tabs (0.25 pts)")
            total_score += 0.25
        elif right_aligned_count > 0:
            partial = 0.25 * (right_aligned_count / max(num_dotted, 1))
            print(f"PARTIAL: Component 3 — {right_aligned_count}/{num_dotted} right-aligned (partial: {partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No right-aligned tab stops found on TOC entries")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ---------------------------------------------------------------
    # Component 4: Progressive indentation across 3 levels (0.15 pts)
    # Initial doc has no TOC entries, so no indentation levels.
    # Golden doc uses: L1=0, L2=274320, L3=548640 EMU.
    # We check that there are at least 2 distinct non-zero indent levels.
    # ---------------------------------------------------------------
    try:
        indent_levels = set()
        for i in dotted_entries:
            para = paragraphs[i]
            indent = para.paragraph_format.left_indent
            if indent is None:
                indent = 0
            indent_levels.add(indent)

        # We expect at least 3 distinct levels (0, some, more)
        distinct_levels = len(indent_levels)
        if distinct_levels >= 3:
            print(f"PASS: Component 4 — {distinct_levels} indent levels found: {sorted(indent_levels)} (0.15 pts)")
            total_score += 0.15
        elif distinct_levels == 2:
            print(f"PARTIAL: Component 4 — Only 2 indent levels: {sorted(indent_levels)} (0.08 pts)")
            total_score += 0.08
        else:
            print(f"FAIL: Component 4 — Only {distinct_levels} indent level(s): {sorted(indent_levels)}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ---------------------------------------------------------------
    # Component 5: Document grew — TOC paragraphs added (0.15 pts)
    # Initial doc has 126 paragraphs. Golden has 163.
    # The TOC adds ~37 paragraphs. We check for at least 20 more paragraphs
    # than the baseline of ~126 (no-TOC state).
    # ---------------------------------------------------------------
    try:
        num_paragraphs = len(paragraphs)
        # The initial doc has approximately 126 paragraphs.
        # TOC should add at least 20+ paragraphs.
        baseline = 126
        growth = num_paragraphs - baseline
        if growth >= 20:
            print(f"PASS: Component 5 — Document has {num_paragraphs} paragraphs (+{growth} from baseline ~{baseline}) (0.15 pts)")
            total_score += 0.15
        elif growth >= 10:
            partial = 0.15 * (growth / 20.0)
            print(f"PARTIAL: Component 5 — {num_paragraphs} paragraphs (+{growth}), expected +20 (partial: {partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 — Document has {num_paragraphs} paragraphs (+{growth} from baseline ~{baseline}), expected +20")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
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

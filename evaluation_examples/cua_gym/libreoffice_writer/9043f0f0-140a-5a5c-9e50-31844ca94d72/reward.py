"""
Reward Script: Create Table of Contents with 4 heading levels, bold H1 entries, 10pt font, 'Contents' title
Task ID: osworld_writer_toc_generation_004
Domain: libreoffice_writer
Scoring:
  Component 1: TOC is present at document start (0.3 pts)
  Component 2: TOC covers all 4 heading levels (0.2 pts)
  Component 3: Heading 1 TOC entries are bold (0.2 pts)
  Component 4: All TOC entries have 10pt font size (0.2 pts)
  Component 5: 'Contents' title paragraph exists before TOC (0.1 pts)
"""

import os
from docx import Document
from docx.shared import Pt

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_toc_generation_004'


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

    # Identify TOC section: paragraphs that look like TOC entries (contain a tab
    # followed by a page number, appearing before the document body headings).
    # The document body starts where Heading 1/2/3/4 styled paragraphs appear.
    # In the golden file:
    #   - para[0] = 'Contents' title
    #   - para[1..60] = TOC entries (Normal style, text contains \t + page number)
    #   - para[61] = empty separator
    #   - para[62+] = document body

    all_paras = doc.paragraphs

    # --- Component 5: 'Contents' title paragraph (0.1 pts) ---
    # The first paragraph should be the 'Contents' title
    try:
        first_para_text = all_paras[0].text.strip() if all_paras else ''
        if first_para_text == 'Contents':
            print(f"PASS: Component 5 — 'Contents' title found at paragraph 0 (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 5 — Expected 'Contents' at paragraph 0, found: {first_para_text!r}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # --- Component 1: TOC is present at document start (0.3 pts) ---
    # A TOC entry is a Normal-style paragraph containing a tab character followed
    # by a digit (page number). We expect at least 40 such entries near the start.
    try:
        # Collect TOC-like paragraphs from the beginning of the document
        # (before we hit the document body, identified by Heading styles)
        toc_entries = []

        for i, p in enumerate(all_paras):
            # Stop collecting TOC once we see the real document headings
            # The first Heading-styled paragraph that matches H1/H2/H3/H4 marks body start
            # TOC entries use Normal style, document headings use Heading styles
            if p.style.name in ('Heading 1', 'Heading 2', 'Heading 3', 'Heading 4'):
                break
            # A TOC entry: Normal style with tab and trailing digit(s)
            if (p.style.name == 'Normal' and
                    '\t' in p.text and
                    p.text.strip() and
                    p.text.split('\t')[-1].strip().isdigit()):
                toc_entries.append((i, p))

        toc_count = len(toc_entries)
        if toc_count >= 40:
            print(f"PASS: Component 1 — TOC present with {toc_count} entries at document start (0.3 pts)")
            total_score += 0.3
        elif toc_count >= 10:
            # Partial: some TOC entries present
            print(f"PARTIAL: Component 1 — TOC has only {toc_count} entries (expected >= 40), awarding 0.15 pts")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — No TOC detected or fewer than 10 entries (found {toc_count})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # --- Component 2: TOC covers all 4 heading levels (0.2 pts) ---
    # Heading levels are identified by left_indent:
    #   H1 -> indent = 0 (or None treated as 0)
    #   H2 -> indent ~= 228600 EMU
    #   H3 -> indent ~= 457200 EMU
    #   H4 -> indent ~= 685800 EMU
    try:
        indent_levels_found = set()
        for idx, p in toc_entries:
            indent = p.paragraph_format.left_indent
            if indent is None or indent == 0:
                indent_levels_found.add('H1')
            elif 150000 < indent < 310000:  # ~228600
                indent_levels_found.add('H2')
            elif 390000 < indent < 530000:  # ~457200
                indent_levels_found.add('H3')
            elif 610000 < indent < 760000:  # ~685800
                indent_levels_found.add('H4')

        if len(indent_levels_found) == 4:
            print(f"PASS: Component 2 — TOC covers all 4 heading levels: {sorted(indent_levels_found)} (0.2 pts)")
            total_score += 0.2
        elif len(indent_levels_found) >= 2:
            comp2_partial = round(0.2 * len(indent_levels_found) / 4, 2)
            print(f"PARTIAL: Component 2 — TOC covers {len(indent_levels_found)} levels ({indent_levels_found}), awarding {comp2_partial} pts")
            total_score += comp2_partial
        else:
            print(f"FAIL: Component 2 — TOC does not cover 4 heading levels; found: {indent_levels_found}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # --- Component 3: Heading 1 TOC entries are bold (0.2 pts) ---
    # H1 entries have left_indent == 0 (or None).
    # All text runs (non-whitespace) must be bold=True.
    try:
        h1_toc_entries = [(idx, p) for idx, p in toc_entries
                          if p.paragraph_format.left_indent is None or
                          p.paragraph_format.left_indent == 0]

        if not h1_toc_entries:
            print("FAIL: Component 3 — No H1 TOC entries found to check for bold")
        else:
            bold_count = 0
            non_bold_count = 0
            for idx, p in h1_toc_entries:
                # Check if text runs (non-tab/non-whitespace) are bold
                text_runs = [r for r in p.runs if r.text.strip() and r.text.strip() != '\t']
                entry_bold = all(r.font.bold is True for r in text_runs if r.text.strip())
                if entry_bold:
                    bold_count += 1
                else:
                    non_bold_count += 1
                    # Show details for debugging
                    for r in text_runs:
                        if r.text.strip():
                            print(f"  DEBUG: H1 TOC entry [{idx}] run bold={r.font.bold}, text={r.text[:40]!r}")

            if non_bold_count == 0 and bold_count > 0:
                print(f"PASS: Component 3 — All {bold_count} H1 TOC entries are bold (0.2 pts)")
                total_score += 0.2
            elif bold_count > 0:
                comp3_partial = round(0.2 * bold_count / (bold_count + non_bold_count), 2)
                print(f"PARTIAL: Component 3 — {bold_count}/{bold_count + non_bold_count} H1 entries bold, awarding {comp3_partial} pts")
                total_score += comp3_partial
            else:
                print(f"FAIL: Component 3 — No H1 TOC entries are bold (found {len(h1_toc_entries)} H1 entries)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # --- Component 4: All TOC entries have 10pt font size (0.2 pts) ---
    # Every text run in every TOC entry (excluding pure whitespace/tab runs) should
    # have font size == Pt(10) == 127000 EMU.
    try:
        total_runs = 0
        correct_size_runs = 0

        for idx, p in toc_entries:
            for r in p.runs:
                if r.text.strip():  # skip pure whitespace runs
                    total_runs += 1
                    size = r.font.size
                    if size is not None and abs(size - Pt(10)) < 100:  # 127000 EMU for 10pt
                        correct_size_runs += 1
                    else:
                        size_pt = size.pt if size else None
                        # Log only first few mismatches
                        if total_runs - correct_size_runs <= 3:
                            print(f"  DEBUG: Para [{idx}] run size={size_pt}pt, expected 10pt, text={r.text[:30]!r}")

        if total_runs == 0:
            print("FAIL: Component 4 — No text runs found in TOC entries")
        elif correct_size_runs == total_runs:
            print(f"PASS: Component 4 — All {total_runs} TOC text runs have 10pt font size (0.2 pts)")
            total_score += 0.2
        elif correct_size_runs >= total_runs * 0.9:
            print(f"PARTIAL: Component 4 — {correct_size_runs}/{total_runs} TOC runs at 10pt (>= 90%), awarding 0.15 pts")
            total_score += 0.15
        elif correct_size_runs >= total_runs * 0.5:
            print(f"PARTIAL: Component 4 — {correct_size_runs}/{total_runs} TOC runs at 10pt (>= 50%), awarding 0.1 pts")
            total_score += 0.1
        else:
            print(f"FAIL: Component 4 — Only {correct_size_runs}/{total_runs} TOC runs have 10pt font size")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in the environment
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

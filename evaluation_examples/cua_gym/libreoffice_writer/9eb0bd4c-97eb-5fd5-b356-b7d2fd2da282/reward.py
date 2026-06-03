"""
Reward Script: Find all text formatted in bold and change it to italic instead.
Task ID: writer_edit_013
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.6): All 8 target terms are now italic (font.italic == True)
  - Component 2 (0.4): All 8 target terms have bold removed (font.bold is not True)
  Total: 1.0

The task requires converting 8 specific bold terms to italic:
  'machine learning', 'neural networks', 'deep learning', 'reinforcement learning',
  'supervised learning', 'unsupervised learning', 'transfer learning', 'natural language processing'
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_edit_013'

# The 8 target terms that should be converted from bold to italic
TARGET_TERMS = [
    'machine learning',
    'neural networks',
    'deep learning',
    'reinforcement learning',
    'supervised learning',
    'unsupervised learning',
    'transfer learning',
    'natural language processing',
]


def find_target_runs(doc):
    """Find all runs whose text exactly matches any target term."""
    found = {}
    for i, para in enumerate(doc.paragraphs):
        for run in para.runs:
            text = run.text.strip()
            if text in TARGET_TERMS:
                if text not in found:
                    found[text] = []
                found[text].append((i, run))
    return found


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must be loadable
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find all runs matching the 8 target terms
    found_runs = find_target_runs(doc)

    if not found_runs:
        print("CRITICAL: No target terms found in document — file may be corrupted or wrong document")
        print("REWARD: 0.0")
        return 0.0

    # Report discovery
    print(f"Found {len(found_runs)}/{len(TARGET_TERMS)} target terms in document")

    # Component 1: All 8 target terms are italic (0.6 points)
    # Each term that is italic contributes 0.6 / 8 = 0.075 pts
    try:
        italic_count = 0
        not_italic_terms = []
        for term in TARGET_TERMS:
            if term in found_runs:
                # Check via font.italic property (explicit), then fallback to .italic (inherited)
                term_italic = any(run.font.italic == True for (_, run) in found_runs[term])
                if not term_italic:
                    term_italic = any(run.italic == True for (_, run) in found_runs[term])
                if term_italic:
                    italic_count += 1
                else:
                    not_italic_terms.append(term)
            else:
                not_italic_terms.append(f"[missing] {term}")

        if italic_count == len(TARGET_TERMS):
            print(f"PASS: Component 1 — All {italic_count}/{len(TARGET_TERMS)} target terms are italic (0.60 pts)")
            total_score += 0.6
        elif italic_count > 0:
            partial = round((italic_count / len(TARGET_TERMS)) * 0.6, 4)
            print(f"PARTIAL: Component 1 — {italic_count}/{len(TARGET_TERMS)} target terms are italic ({partial} pts)")
            print(f"  Not italic: {not_italic_terms}")
            if partial > 0:
                total_score += partial
        else:
            print(f"FAIL: Component 1 — 0/{len(TARGET_TERMS)} target terms are italic (0.00 pts)")
            print(f"  Not italic: {not_italic_terms}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 8 target terms have bold removed (0.4 points)
    # Each term that has bold removed contributes 0.4 / 8 = 0.05 pts
    try:
        not_bold_count = 0
        still_bold_terms = []
        for term in TARGET_TERMS:
            if term in found_runs:
                # term_still_bold = True if any run has bold=True for this term
                term_still_bold = any(
                    run.font.bold == True or run.bold == True
                    for (_, run) in found_runs[term]
                )
                if not term_still_bold:
                    not_bold_count += 1
                else:
                    still_bold_terms.append(term)
            else:
                still_bold_terms.append(f"[missing] {term}")

        if not_bold_count == len(TARGET_TERMS):
            print(f"PASS: Component 2 — All {not_bold_count}/{len(TARGET_TERMS)} target terms have bold removed (0.40 pts)")
            total_score += 0.4
        elif not_bold_count > 0:
            partial = round((not_bold_count / len(TARGET_TERMS)) * 0.4, 4)
            print(f"PARTIAL: Component 2 — {not_bold_count}/{len(TARGET_TERMS)} target terms have bold removed ({partial} pts)")
            print(f"  Still bold: {still_bold_terms}")
            if partial > 0:
                total_score += partial
        else:
            print(f"FAIL: Component 2 — 0/{len(TARGET_TERMS)} target terms have bold removed (0.00 pts)")
            print(f"  Still bold: {still_bold_terms}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {total_score:.4f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in given env
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

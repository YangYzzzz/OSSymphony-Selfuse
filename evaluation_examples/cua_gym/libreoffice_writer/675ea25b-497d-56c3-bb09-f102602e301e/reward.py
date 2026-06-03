"""
Reward Script: Continuous caption numbering across subdocument chapters
Task ID: writer_rm_095
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35): Figure captions use continuous numbering (1-19)
  Component 2 (0.35): Equation captions use continuous numbering (1-27)
  Component 3 (0.30): Table captions use continuous numbering (1-9)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_095'


def extract_caption_numbers(doc):
    """Extract ordered lists of figure, table, and equation numbers from the document."""
    figures = []
    tables = []
    equations = []

    for p in doc.paragraphs:
        text = p.text.strip()

        # Match "Figure N:" pattern
        m = re.match(r'^Figure\s+(\d+)\s*:', text)
        if m:
            figures.append(int(m.group(1)))

        # Match "Table N:" pattern
        m = re.match(r'^Table\s+(\d+)\s*:', text)
        if m:
            tables.append(int(m.group(1)))

        # Match "(Equation N)" pattern
        m = re.search(r'\(Equation\s+(\d+)\)', text)
        if m:
            equations.append(int(m.group(1)))

    return figures, tables, equations


def is_continuous(numbers):
    """Check if a list of numbers forms a continuous sequence starting from 1."""
    if not numbers:
        return False
    expected = list(range(1, len(numbers) + 1))
    return numbers == expected


def has_restarts(numbers):
    """Check if numbers restart (go back to a lower number) at any point."""
    for i in range(1, len(numbers)):
        if numbers[i] <= numbers[i - 1]:
            return True
    return False


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

    figures, tables, equations = extract_caption_numbers(doc)

    print(f"Found {len(figures)} figures, {len(tables)} tables, {len(equations)} equations")
    print(f"Figure numbers: {figures}")
    print(f"Table numbers:  {tables}")
    print(f"Equation numbers: {equations}")

    # Component 1: Figure captions use continuous numbering (0.35 points)
    # Expected: 19 figures numbered 1 through 19 with no restarts
    try:
        if is_continuous(figures) and len(figures) >= 19:
            print(f"PASS: Component 1 -- Figures are continuously numbered 1-{len(figures)} (0.35 pts)")
            total_score += 0.35
        elif not has_restarts(figures) and len(figures) >= 19:
            # Continuous but maybe not starting at 1 -- partial credit
            print(f"PARTIAL: Component 1 -- Figures don't restart but sequence is non-standard: {figures[:5]}... (0.15 pts)")
            total_score += 0.15
        else:
            restart_indices = [i for i in range(1, len(figures)) if figures[i] <= figures[i - 1]]
            print(f"FAIL: Component 1 -- Figures have {len(restart_indices)} restart(s). Numbers: {figures}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Equation captions use continuous numbering (0.35 points)
    # Expected: 27 equations numbered 1 through 27 with no restarts
    try:
        if is_continuous(equations) and len(equations) >= 27:
            print(f"PASS: Component 2 -- Equations are continuously numbered 1-{len(equations)} (0.35 pts)")
            total_score += 0.35
        elif not has_restarts(equations) and len(equations) >= 27:
            print(f"PARTIAL: Component 2 -- Equations don't restart but sequence is non-standard: {equations[:5]}... (0.15 pts)")
            total_score += 0.15
        else:
            restart_indices = [i for i in range(1, len(equations)) if equations[i] <= equations[i - 1]]
            print(f"FAIL: Component 2 -- Equations have {len(restart_indices)} restart(s). Numbers: {equations}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Table captions use continuous numbering (0.30 points)
    # Expected: 9 tables numbered 1 through 9 with no restarts
    try:
        if is_continuous(tables) and len(tables) >= 9:
            print(f"PASS: Component 3 -- Tables are continuously numbered 1-{len(tables)} (0.30 pts)")
            total_score += 0.30
        elif not has_restarts(tables) and len(tables) >= 9:
            print(f"PARTIAL: Component 3 -- Tables don't restart but sequence is non-standard: {tables[:5]}... (0.15 pts)")
            total_score += 0.15
        else:
            restart_indices = [i for i in range(1, len(tables)) if tables[i] <= tables[i - 1]]
            print(f"FAIL: Component 3 -- Tables have {len(restart_indices)} restart(s). Numbers: {tables}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

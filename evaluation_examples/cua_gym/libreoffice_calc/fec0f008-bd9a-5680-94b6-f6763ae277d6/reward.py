"""
Reward Script: Classical Music - Identify Shortest Piece
Task ID: osworld_multi_apps_book_reading_rate_009
Domain: multi_apps (LibreOffice Calc + LibreOffice Writer)

Task Description:
  A spreadsheet of classical music pieces (classical_2023.xlsx) on Desktop has 5 compositions
  with empty Duration column. User must look up average durations (via allmusic.com or similar)
  and identify the shortest piece, then record its name in shortest_piece.docx on the Desktop.

Scoring Rubric:
  Component 1: shortest_piece.docx contains a valid piece name indicating Bolero (0.7 pts)
               - The expected answer is "Bolero" (~16 min), which is the shortest
               - Accept "Eine kleine Nachtmusik" as a valid alternate answer (also acceptably short)
  Component 2: classical_2023.xlsx Duration column has numeric values filled in (0.3 pts)
               - At least 3 out of 5 Duration cells must have numeric values
               - Confirms research was done to fill the spreadsheet
"""

import os

from docx import Document
import openpyxl

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_book_reading_rate_009'

# Accepted valid answers for shortest piece
# Bolero (~16 min) is the true shortest; Eine kleine Nachtmusik (~20 min) is an alternate
VALID_SHORTEST_PIECES = [
    'bolero',
    'eine kleine nachtmusik',
    'eine kleine',
]


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    docx_path = os.path.join(WORKDIR, 'shortest_piece.docx')
    xlsx_path = os.path.join(WORKDIR, 'classical_2023.xlsx')

    # Precondition gates: if files don't exist, return 0.0 immediately
    if not os.path.exists(docx_path):
        print(f"CRITICAL: shortest_piece.docx not found at {docx_path}")
        print("REWARD: 0.0")
        return 0.0

    if not os.path.exists(xlsx_path):
        print(f"CRITICAL: classical_2023.xlsx not found at {xlsx_path}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: shortest_piece.docx contains the name of the shortest piece (0.7 pts)
    # This is the primary deliverable: the file should name "Bolero" (or "Eine kleine Nachtmusik")
    # Initial state: file is empty (0 paragraphs / no text) → this FAILS on initial, PASSES on golden
    try:
        doc = Document(docx_path)

        # Gather all text from the document
        doc_text = ' '.join(p.text.strip() for p in doc.paragraphs if p.text.strip())
        doc_text_lower = doc_text.lower()

        print(f"INFO: shortest_piece.docx text = {doc_text!r}")

        # Check if document contains any text at all (not empty)
        if not doc_text_lower:
            print("FAIL: Component 1 — shortest_piece.docx is empty, no piece name recorded")
        else:
            # Check if the named piece is one of the valid shortest answers
            matched_piece = None
            for candidate in VALID_SHORTEST_PIECES:
                if candidate in doc_text_lower:
                    matched_piece = candidate
                    break

            if matched_piece == 'bolero':
                # Exact correct answer: Bolero is the shortest
                print(f"PASS: Component 1 — Correct answer 'Bolero' found in shortest_piece.docx (0.7 pts)")
                total_score += 0.7
            elif matched_piece:
                # Acceptable alternate answer
                print(f"PASS: Component 1 — Acceptable alternate answer '{matched_piece}' found (0.7 pts)")
                total_score += 0.7
            else:
                # Document has text but incorrect answer
                print(f"FAIL: Component 1 — Document contains text '{doc_text}' but not 'Bolero' or 'Eine kleine Nachtmusik'")

    except Exception as e:
        print(f"ERROR: Component 1 — Could not read shortest_piece.docx: {e}")

    # Component 2: classical_2023.xlsx Duration column has numeric values filled (0.3 pts)
    # Initial state: all Duration cells are None/empty → this FAILS on initial, PASSES on golden
    # This shows the agent did the research to look up durations
    try:
        wb = openpyxl.load_workbook(xlsx_path)
        ws = wb.active

        # Duration is column C (index 3). Data rows are 2-6 (5 pieces).
        # Check how many Duration cells have numeric values
        duration_filled = 0
        total_pieces = 5
        for row_idx in range(2, 7):  # rows 2 through 6
            cell_val = ws.cell(row=row_idx, column=3).value
            if cell_val is not None and isinstance(cell_val, (int, float)) and cell_val > 0:
                duration_filled += 1

        print(f"INFO: Duration cells filled: {duration_filled}/{total_pieces}")

        if duration_filled >= 3:
            print(f"PASS: Component 2 — Duration column has {duration_filled}/{total_pieces} values filled (0.3 pts)")
            total_score += 0.3
        elif duration_filled > 0:
            # Partial: some but fewer than 3 filled
            partial = round(0.3 * (duration_filled / total_pieces), 2)
            print(f"PARTIAL: Component 2 — Duration column has only {duration_filled}/{total_pieces} values filled ({partial} pts)")
            if partial > 0:
                total_score += partial
        else:
            print(f"FAIL: Component 2 — Duration column is empty (no values filled)")

    except Exception as e:
        print(f"ERROR: Component 2 — Could not read classical_2023.xlsx: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

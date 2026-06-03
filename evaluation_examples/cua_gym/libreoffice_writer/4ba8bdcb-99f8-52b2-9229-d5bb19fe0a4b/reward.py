"""
Reward Script: Insert a 3x3 identity matrix equation using the equation editor
Task ID: writer_acad_082
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): oMath equation element exists in the document
  Component 2 (0.2): Matrix structure is 3x3 (3 rows, 3 entries per row)
  Component 3 (0.3): Matrix values match the 3x3 identity matrix
  Component 4 (0.2): Placeholder text removed from document
"""

import os
import time


WORKDIR = '/home/user'
TASK_ID = 'writer_acad_082'
FILE_NAME = f'{TASK_ID}.docx'

PLACEHOLDER_TEXT = '[Insert 3x3 Identity Matrix Equation Here]'

IDENTITY_MATRIX = [
    ['1', '0', '0'],
    ['0', '1', '0'],
    ['0', '0', '1'],
]


def persist_app_state(domain: str):
    """Attempt to save any unsaved changes in LibreOffice."""
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

    # Load the document
    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    body = doc.element.body
    m_ns = 'http://schemas.openxmlformats.org/officeDocument/2006/math'

    # Component 1: oMath equation element exists in the document (0.3 points)
    # This checks that an equation was inserted. The initial doc has zero oMath elements.
    try:
        omath_elements = body.findall('.//{' + m_ns + '}oMath')
        omath_count = len(omath_elements)
        if omath_count > 0:
            print(f"PASS: Component 1 - oMath element found ({omath_count} element(s)) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 - No oMath elements found in document")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Matrix structure is 3x3 (0.2 points)
    # Check that there is an m:m (matrix) element with exactly 3 rows and 3 columns each.
    try:
        matrix_ok = False
        matrix_elements = body.findall('.//{' + m_ns + '}m')
        for mat in matrix_elements:
            rows = mat.findall('{' + m_ns + '}mr')
            if len(rows) == 3:
                cols_per_row = [len(r.findall('{' + m_ns + '}e')) for r in rows]
                if all(c == 3 for c in cols_per_row):
                    matrix_ok = True
                    break
        if matrix_ok:
            print(f"PASS: Component 2 - Found 3x3 matrix structure (0.2 pts)")
            total_score += 0.2
        else:
            if len(matrix_elements) == 0:
                print(f"FAIL: Component 2 - No matrix (m:m) elements found")
            else:
                print(f"FAIL: Component 2 - Matrix found but not 3x3 dimensions")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Matrix values match 3x3 identity matrix (0.3 points)
    # Extract text values from each matrix entry and compare to expected identity matrix.
    try:
        values_ok = False
        matrix_elements = body.findall('.//{' + m_ns + '}m')
        for mat in matrix_elements:
            rows = mat.findall('{' + m_ns + '}mr')
            if len(rows) != 3:
                continue
            extracted = []
            for row in rows:
                entries = row.findall('{' + m_ns + '}e')
                if len(entries) != 3:
                    break
                row_vals = []
                for entry in entries:
                    t_elems = entry.findall('.//{' + m_ns + '}t')
                    val = ''.join(t.text.strip() for t in t_elems if t.text)
                    row_vals.append(val)
                extracted.append(row_vals)
            if len(extracted) == 3 and extracted == IDENTITY_MATRIX:
                values_ok = True
                break
        if values_ok:
            print(f"PASS: Component 3 - Matrix values match identity matrix {{1,0,0}},{{0,1,0}},{{0,0,1}} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 - Matrix values do not match identity matrix. Extracted: {extracted if 'extracted' in dir() and extracted else 'N/A'}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Placeholder text removed (0.2 points)
    # The initial doc has "[Insert 3x3 Identity Matrix Equation Here]" in paragraph 9.
    # After inserting the equation, this placeholder must be gone.
    try:
        all_text = ' '.join(p.text for p in doc.paragraphs)
        if PLACEHOLDER_TEXT not in all_text:
            print(f"PASS: Component 4 - Placeholder text removed (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 - Placeholder text '{PLACEHOLDER_TEXT}' still present in document")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{FILE_NAME}'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

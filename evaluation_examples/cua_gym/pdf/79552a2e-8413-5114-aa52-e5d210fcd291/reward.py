"""
Reward Script: Create a 5-page A4 PDF with centered headings for seminar notes
Task ID: pdf_res_042
Domain: pdf
Scoring:
  Component 1 (0.3): File exists at correct path with exactly 5 pages
  Component 2 (0.3): All 5 pages have A4 dimensions (595x842 pts)
  Component 3 (0.4): Each page contains correct heading 'Notes - Paper N'
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_042'
FILE_PATH = os.path.join(WORKDIR, 'papers', 'seminar_notes.pdf')

# A4 dimensions in points (tolerance of 1 pt for rounding)
A4_WIDTH = 595.0
A4_HEIGHT = 842.0
DIM_TOLERANCE = 2.0


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be loadable
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import fitz
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: File has exactly 5 pages (0.3 points)
    # This FAILS on initial_env (file does not exist) and PASSES on golden_env
    try:
        page_count = len(doc)
        if page_count == 5:
            print(f"PASS: Component 1 — PDF has exactly 5 pages (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Expected 5 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All pages have A4 dimensions (0.3 points)
    # Each page worth 0.06 pts (0.3 / 5)
    try:
        a4_count = 0
        for i in range(min(len(doc), 5)):
            page = doc[i]
            r = page.rect
            w_ok = abs(r.width - A4_WIDTH) <= DIM_TOLERANCE
            h_ok = abs(r.height - A4_HEIGHT) <= DIM_TOLERANCE
            if w_ok and h_ok:
                a4_count += 1
            else:
                print(f"FAIL: Component 2 — Page {i+1} dimensions {r.width:.1f}x{r.height:.1f}, expected ~{A4_WIDTH}x{A4_HEIGHT}")

        if a4_count == 5:
            print(f"PASS: Component 2 — All 5 pages have A4 dimensions (0.3 pts)")
            total_score += 0.3
        elif a4_count > 0:
            partial = round(0.3 * a4_count / 5, 2)
            print(f"PARTIAL: Component 2 — {a4_count}/5 pages have A4 dimensions ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No pages have A4 dimensions")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Each page contains the correct heading text (0.4 points)
    # Each correct heading worth 0.08 pts (0.4 / 5)
    try:
        heading_count = 0
        for i in range(min(len(doc), 5)):
            page = doc[i]
            text = page.get_text().strip()
            expected = f"Notes - Paper {i+1}"
            if expected in text:
                heading_count += 1
            else:
                print(f"FAIL: Component 3 — Page {i+1} text is {repr(text)}, expected to contain {repr(expected)}")

        if heading_count == 5:
            print(f"PASS: Component 3 — All 5 pages have correct headings (0.4 pts)")
            total_score += 0.4
        elif heading_count > 0:
            partial = round(0.4 * heading_count / 5, 2)
            print(f"PARTIAL: Component 3 — {heading_count}/5 pages have correct headings ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No pages have correct headings")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

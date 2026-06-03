"""
Reward Script: Set PDF initial view settings
Task ID: pdf_res_044
Domain: pdf
Scoring:
  Component 1: PageMode = /UseOutlines (bookmarks panel visible) — 0.35 pts
  Component 2: OpenAction targets page 0 with /FitH (fit width) — 0.40 pts
  Component 3: PageLayout = /SinglePage — 0.25 pts
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_044'
OUTPUT_FILE = os.path.join(WORKDIR, 'thesis', 'thesis_presentation_view.pdf')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid PDF openable by pikepdf
    try:
        import pikepdf
        pdf = pikepdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: PageMode = /UseOutlines (bookmarks panel visible) — 0.35 pts
    try:
        if '/PageMode' in pdf.Root:
            page_mode = str(pdf.Root['/PageMode'])
            if page_mode == '/UseOutlines':
                print(f"PASS: Component 1 — PageMode is /UseOutlines (bookmarks panel visible) (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 1 — Expected PageMode /UseOutlines, found: {page_mode}")
        else:
            print("FAIL: Component 1 — /PageMode not set in PDF catalog")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: OpenAction targets page 0 (page 1) with /FitH (fit width) — 0.40 pts
    try:
        if '/OpenAction' in pdf.Root:
            oa = pdf.Root['/OpenAction']
            if isinstance(oa, pikepdf.Array) and len(oa) >= 2:
                # Check fit type is /FitH (fit width)
                fit_type = str(oa[1])
                fit_ok = (fit_type == '/FitH')

                # Check page reference is page 0 (first page)
                page_ref = oa[0]
                page_idx = None
                for i, p in enumerate(pdf.pages):
                    if p.obj == page_ref:
                        page_idx = i
                        break

                page_ok = (page_idx == 0)

                if fit_ok and page_ok:
                    print(f"PASS: Component 2 — OpenAction targets page 0 with /FitH (0.40 pts)")
                    total_score += 0.40
                elif fit_ok and not page_ok:
                    # Partial: fit type correct but wrong page
                    print(f"PARTIAL: Component 2 — /FitH correct but page index is {page_idx}, expected 0 (0.20 pts)")
                    total_score += 0.20
                elif page_ok and not fit_ok:
                    # Partial: page correct but wrong fit type
                    print(f"PARTIAL: Component 2 — Page 0 correct but fit type is {fit_type}, expected /FitH (0.20 pts)")
                    total_score += 0.20
                else:
                    print(f"FAIL: Component 2 — OpenAction page index={page_idx} (expected 0), fit type={fit_type} (expected /FitH)")
            else:
                print(f"FAIL: Component 2 — /OpenAction is not a valid array or too short: {oa}")
        else:
            print("FAIL: Component 2 — /OpenAction not set in PDF catalog")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: PageLayout = /SinglePage — 0.25 pts
    try:
        if '/PageLayout' in pdf.Root:
            page_layout = str(pdf.Root['/PageLayout'])
            if page_layout == '/SinglePage':
                print(f"PASS: Component 3 — PageLayout is /SinglePage (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — Expected PageLayout /SinglePage, found: {page_layout}")
        else:
            print("FAIL: Component 3 — /PageLayout not set in PDF catalog")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    pdf.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path
if not os.path.exists(OUTPUT_FILE):
    print(f"File not found: {OUTPUT_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_FILE)

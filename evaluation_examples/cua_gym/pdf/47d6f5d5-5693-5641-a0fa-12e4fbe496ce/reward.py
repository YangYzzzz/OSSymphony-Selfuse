"""
Reward Script: Audit cover letter PDF creation
Task ID: pdf_fin_040
Domain: pdf
Scoring:
  Component 1: PDF exists at correct path and is single page (0.15)
  Component 2: Letterhead contains firm name (0.15)
  Component 3: Address line present (0.10)
  Component 4: Date line present (0.10)
  Component 5: Addressee (Board of Directors, TechVentures Inc.) (0.10)
  Component 6: Body paragraphs with audit keywords (FY2023, unqualified, GAAP) (0.20)
  Component 7: Signature block (Robert Sterling, CPA, Managing Partner) (0.20)
"""

import os

try:
    import pymupdf
except ImportError:
    try:
        import fitz as pymupdf
    except ImportError:
        pymupdf = None

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_040'
FILE_PATH = os.path.join(WORKDIR, 'finance', 'audit_cover.pdf')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    if pymupdf is None:
        print("CRITICAL: pymupdf/fitz not available")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract full text for content checks
    try:
        full_text = ""
        for page in doc:
            full_text += page.get_text("text")
        full_text_lower = full_text.lower()
    except Exception as e:
        print(f"CRITICAL: Cannot extract text: {e}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    # Component 1: PDF is single page (0.15 points)
    # Initial env has no PDF, so this only passes when the PDF is created correctly
    try:
        page_count = doc.page_count
        if page_count == 1:
            print(f"PASS: Component 1 — Single page PDF (page_count={page_count}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Expected 1 page, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Letterhead contains firm name (0.15 points)
    try:
        if "sterling & associates cpas" in full_text_lower:
            print(f"PASS: Component 2 — Firm name 'Sterling & Associates CPAs' found (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Firm name 'Sterling & Associates CPAs' not found in text")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Address line present (0.10 points)
    try:
        if "500 financial plaza" in full_text_lower and "new york" in full_text_lower and "10004" in full_text_lower:
            print(f"PASS: Component 3 — Address '500 Financial Plaza...NY 10004' found (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 — Address not found. Checked for '500 Financial Plaza', 'New York', '10004'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Date line present (0.10 points)
    try:
        if "march 28, 2024" in full_text_lower or "march 28 2024" in full_text_lower:
            print(f"PASS: Component 4 — Date 'March 28, 2024' found (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 — Date 'March 28, 2024' not found in text")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Addressee - Board of Directors, TechVentures Inc. (0.10 points)
    try:
        has_board = "board of directors" in full_text_lower
        has_techventures = "techventures inc" in full_text_lower
        if has_board and has_techventures:
            print(f"PASS: Component 5 — Addressee 'Board of Directors, TechVentures Inc.' found (0.10 pts)")
            total_score += 0.10
        else:
            missing = []
            if not has_board:
                missing.append("'Board of Directors'")
            if not has_techventures:
                missing.append("'TechVentures Inc.'")
            print(f"FAIL: Component 5 — Missing addressee elements: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Body contains 3 audit-relevant paragraphs with key terms (0.20 points)
    # Must reference FY2023, unqualified opinion, and GAAP compliance
    try:
        has_fy2023 = "fy2023" in full_text_lower or "fiscal year" in full_text_lower and "2023" in full_text_lower
        has_unqualified = "unqualified" in full_text_lower
        has_gaap = "gaap" in full_text_lower or "generally accepted in the united states" in full_text_lower

        matches = sum([has_fy2023, has_unqualified, has_gaap])
        if matches == 3:
            print(f"PASS: Component 6 — All 3 audit keywords found (FY2023, unqualified, GAAP) (0.20 pts)")
            total_score += 0.20
        elif matches >= 2:
            partial = round(0.20 * (matches / 3), 2)
            print(f"PARTIAL: Component 6 — {matches}/3 audit keywords found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 6 — Only {matches}/3 audit keywords found. "
                  f"FY2023={has_fy2023}, unqualified={has_unqualified}, GAAP={has_gaap}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: Signature block - Robert Sterling, CPA, Managing Partner (0.20 points)
    try:
        has_name = "robert sterling" in full_text_lower
        has_cpa = "cpa" in full_text_lower
        has_managing_partner = "managing partner" in full_text_lower

        sig_matches = sum([has_name, has_cpa, has_managing_partner])
        if sig_matches == 3:
            print(f"PASS: Component 7 — Full signature block found (Robert Sterling, CPA, Managing Partner) (0.20 pts)")
            total_score += 0.20
        elif sig_matches >= 1:
            partial = round(0.20 * (sig_matches / 3), 2)
            print(f"PARTIAL: Component 7 — {sig_matches}/3 signature elements found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 7 — Signature block not found. "
                  f"Robert Sterling={has_name}, CPA={has_cpa}, Managing Partner={has_managing_partner}")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

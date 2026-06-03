"""
Reward Script: Certificate of Service appended to motion_compel.pdf
Task ID: pdf_legal_074
Domain: pdf
Scoring:
  Component 1 (0.25): Output PDF has 11 pages (original 10 + appended CoS page)
  Component 2 (0.20): Last page contains "CERTIFICATE OF SERVICE" heading
  Component 3 (0.25): Last page contains the required certification text
  Component 4 (0.15): Last page contains "Sarah Chen, Esq." signature
  Component 5 (0.15): Last page contains "Bar No. 123456"
"""

import os
import sys

# Use pymupdf (fitz) for PDF verification
try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_074'
OUTPUT_FILE = os.path.join(WORKDIR, 'legal', 'motion_compel_with_cos.pdf')
ORIGINAL_FILE = os.path.join(WORKDIR, 'legal', 'motion_compel.pdf')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be loadable
    if not os.path.exists(file_path):
        print(f"CRITICAL: Output file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    page_count = doc.page_count

    # Component 1: Output PDF has 11 pages (0.25 points)
    # Initial has 10 pages; golden should have 11 (original + certificate of service)
    try:
        if page_count == 11:
            print(f"PASS: Component 1 — Page count is 11 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Expected 11 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Get last page text for remaining checks
    try:
        last_page = doc[-1]
        last_text = last_page.get_text("text")
    except Exception as e:
        print(f"CRITICAL: Cannot read last page text: {e}")
        doc.close()
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: Last page contains "CERTIFICATE OF SERVICE" heading (0.20 points)
    try:
        if "CERTIFICATE OF SERVICE" in last_text.upper():
            print(f"PASS: Component 2 — 'CERTIFICATE OF SERVICE' found on last page (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — 'CERTIFICATE OF SERVICE' not found on last page")
            print(f"  Last page text preview: {last_text[:200]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Last page contains the required certification text (0.25 points)
    # Key phrases from the task instruction
    try:
        text_upper = last_text.upper()
        # Check for key phrases from the required certification text
        has_certify = "I HEREBY CERTIFY" in text_upper
        has_date = "MARCH 25, 2024" in text_upper
        has_motion = "MOTION TO COMPEL" in text_upper
        has_cmecf = "CM/ECF" in text_upper
        has_electronic = "ELECTRONIC FILING" in text_upper

        matches = sum([has_certify, has_date, has_motion, has_cmecf, has_electronic])
        if matches >= 4:
            print(f"PASS: Component 3 — Certification text verified ({matches}/5 key phrases) (0.25 pts)")
            total_score += 0.25
        elif matches >= 2:
            partial = round(0.25 * matches / 5, 2)
            print(f"PARTIAL: Component 3 — {matches}/5 key phrases found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Only {matches}/5 key phrases found")
            print(f"  certify={has_certify}, date={has_date}, motion={has_motion}, cmecf={has_cmecf}, electronic={has_electronic}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Last page contains "Sarah Chen, Esq." (0.15 points)
    try:
        if "Sarah Chen" in last_text and "Esq" in last_text:
            print(f"PASS: Component 4 — 'Sarah Chen, Esq.' found on last page (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — 'Sarah Chen, Esq.' not found on last page")
            print(f"  Last page text preview: {last_text[:300]}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Last page contains "Bar No. 123456" (0.15 points)
    try:
        if "Bar No" in last_text and "123456" in last_text:
            print(f"PASS: Component 5 — 'Bar No. 123456' found on last page (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — 'Bar No. 123456' not found on last page")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_FILE):
    print(f"File not found: {OUTPUT_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_FILE)

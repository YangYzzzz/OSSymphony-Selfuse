"""
Reward Script: Add cross-reference hyperlinks in thesis PDF
Task ID: pdf_res_067
Domain: pdf
Scoring:
  - Component 1 (0.10): Output file exists and has 90 pages
  - Component 2 (0.30): 'see Chapter 2' link on page 5 targets page 20
  - Component 3 (0.30): 'see Chapter 3' link on page 15 targets page 45
  - Component 4 (0.30): 'see Appendix A' link on page 60 targets page 80
"""

import os
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    import pymupdf as fitz

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_067'
OUTPUT_PATH = os.path.join(WORKDIR, 'thesis', 'thesis_links_active.pdf')

# Expected links: (source_page_0indexed, target_page_0indexed, description)
EXPECTED_LINKS = [
    (4, 19, "'see Chapter 2' on page 5 -> page 20"),
    (14, 44, "'see Chapter 3' on page 15 -> page 45"),
    (59, 79, "'see Appendix A' on page 60 -> page 80"),
]


def check_internal_link(doc, source_page_idx, target_page_idx):
    """
    Check if any link on source_page points to target_page (0-indexed).
    Returns True if such a link exists with kind LINK_GOTO.
    """
    try:
        page = doc[source_page_idx]
        links = page.get_links()
        for link in links:
            # kind 1 = LINK_GOTO (internal link)
            if link.get("kind") == 1 and link.get("page") == target_page_idx:
                return True
        return False
    except Exception:
        return False


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: output file must exist
    if not os.path.exists(OUTPUT_PATH):
        print(f"CRITICAL: Output file not found: {OUTPUT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = fitz.open(OUTPUT_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {OUTPUT_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output file has all 90 pages preserved (0.10 points)
    try:
        page_count = len(doc)
        if page_count == 90:
            print(f"PASS: Component 1 — Output has {page_count} pages (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — Expected 90 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Link on page 5 (idx 4) targets page 20 (idx 19) (0.30 points)
    try:
        src, tgt, desc = EXPECTED_LINKS[0]
        if check_internal_link(doc, src, tgt):
            print(f"PASS: Component 2 — {desc} (0.30 pts)")
            total_score += 0.30
        else:
            links = doc[src].get_links()
            print(f"FAIL: Component 2 — No internal link from page {src+1} to page {tgt+1}. "
                  f"Found {len(links)} links: {links}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Link on page 15 (idx 14) targets page 45 (idx 44) (0.30 points)
    try:
        src, tgt, desc = EXPECTED_LINKS[1]
        if check_internal_link(doc, src, tgt):
            print(f"PASS: Component 3 — {desc} (0.30 pts)")
            total_score += 0.30
        else:
            links = doc[src].get_links()
            print(f"FAIL: Component 3 — No internal link from page {src+1} to page {tgt+1}. "
                  f"Found {len(links)} links: {links}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Link on page 60 (idx 59) targets page 80 (idx 79) (0.30 points)
    try:
        src, tgt, desc = EXPECTED_LINKS[2]
        if check_internal_link(doc, src, tgt):
            print(f"PASS: Component 4 — {desc} (0.30 pts)")
            total_score += 0.30
        else:
            links = doc[src].get_links()
            print(f"FAIL: Component 4 — No internal link from page {src+1} to page {tgt+1}. "
                  f"Found {len(links)} links: {links}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

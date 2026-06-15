"""
Reward Script: Add underline annotations to defined terms in partnership agreement
Task ID: pdf_legal_037
Domain: pdf
Scoring:
  C1 (0.10): Output file exists at correct path
  C2 (0.10): Valid PDF with 14 pages (same as source)
  C3 (0.10): All annotations are Underline type (no other types)
  C4 (0.30): Exactly 12 underline annotations (one per defined term)
  C5 (0.20): Annotations are on the expected pages
  C6 (0.20): Annotations cover actual defined term text patterns
"""

import os
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    import pymupdf as fitz

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_037'
OUTPUT_PATH = f'{WORKDIR}/legal/partnership_agreement_annotated.pdf'
SOURCE_PATH = f'{WORKDIR}/legal/partnership_agreement.pdf'

# Expected defined terms and the pages they appear on (0-indexed)
# Based on task context: 12 defined terms found via "hereinafter referred to as"
EXPECTED_TERM_COUNT = 12

# Pages where underline annotations are expected (0-indexed)
# From golden exploration: pages 1,2,3,4,5,6 have annotations
EXPECTED_PAGES_WITH_ANNOTS = {1, 2, 3, 4, 5, 6}

# Defined term keywords to verify annotations cover actual terms
DEFINED_TERM_KEYWORDS = [
    "Agreement",
    "Managing Partner",
    "Limited Partner",
    "Advisory Partner",
    "Partners",
    "Partnership",
    "Principal",
    "Business Activities",
    "Initial Capital",
    "Capital Records",
    "Reserved",
    "Transfer Restrictions",
]


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists at correct path (0.1 points)
    try:
        if os.path.exists(OUTPUT_PATH) and os.path.getsize(OUTPUT_PATH) > 0:
            print(f"PASS: Component 1 — Output file exists at {OUTPUT_PATH} (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 — Output file not found or empty at {OUTPUT_PATH}")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print("REWARD: 0.0")
        return 0.0

    # Load the PDF
    try:
        doc = fitz.open(OUTPUT_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {OUTPUT_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: Valid PDF with 14 pages (0.1 points)
    try:
        page_count = len(doc)
        if page_count == 14:
            print(f"PASS: Component 2 — PDF has {page_count} pages as expected (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 2 — Expected 14 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Collect all annotations across all pages
    all_annotations = []
    pages_with_underline = set()
    non_underline_types = set()

    try:
        for page_idx in range(len(doc)):
            page = doc[page_idx]
            annot_iter = page.annots()
            if annot_iter:
                for annot in annot_iter:
                    atype = annot.type[1]
                    rect = annot.rect
                    text_under = page.get_textbox(rect).strip()
                    all_annotations.append({
                        "page": page_idx,
                        "type": atype,
                        "rect": tuple(rect),
                        "text": text_under,
                    })
                    if atype == "Underline":
                        pages_with_underline.add(page_idx)
                    else:
                        non_underline_types.add(atype)
    except Exception as e:
        print(f"ERROR: Failed to collect annotations — {e}")

    underline_annots = [a for a in all_annotations if a["type"] == "Underline"]
    other_annots = [a for a in all_annotations if a["type"] != "Underline"]

    # Component 3: All annotations are Underline type (0.1 points)
    try:
        if len(other_annots) == 0 and len(underline_annots) > 0:
            print(f"PASS: Component 3 — All {len(underline_annots)} annotations are Underline type (0.1 pts)")
            total_score += 0.1
        elif len(underline_annots) == 0:
            print(f"FAIL: Component 3 — No underline annotations found at all")
        else:
            print(f"FAIL: Component 3 — Found non-Underline annotation types: {non_underline_types}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Exactly 12 underline annotations (0.3 points)
    # Award partial credit: 0.3 * (count / expected) capped at 0.3
    try:
        count = len(underline_annots)
        if count == EXPECTED_TERM_COUNT:
            print(f"PASS: Component 4 — Found exactly {count} underline annotations (0.3 pts)")
            total_score += 0.3
        elif count > 0:
            # Partial credit proportional to how many we found, but penalize extras
            ratio = min(count, EXPECTED_TERM_COUNT) / EXPECTED_TERM_COUNT
            if count > EXPECTED_TERM_COUNT:
                # Penalize for extra annotations
                penalty = (count - EXPECTED_TERM_COUNT) * 0.02
                partial = max(0.0, 0.3 * ratio - penalty)
            else:
                partial = 0.3 * ratio
            partial = round(min(partial, 0.25), 2)  # cap partial below full score
            print(f"FAIL: Component 4 — Found {count} underline annotations, expected {EXPECTED_TERM_COUNT} (partial: {partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No underline annotations found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Annotations are on expected pages (0.2 points)
    try:
        if pages_with_underline == EXPECTED_PAGES_WITH_ANNOTS:
            print(f"PASS: Component 5 — Annotations on correct pages: {sorted(pages_with_underline)} (0.2 pts)")
            total_score += 0.2
        elif len(pages_with_underline) > 0:
            overlap = pages_with_underline & EXPECTED_PAGES_WITH_ANNOTS
            partial = 0.2 * len(overlap) / len(EXPECTED_PAGES_WITH_ANNOTS)
            partial = round(min(partial, 0.15), 2)  # cap partial
            print(f"FAIL: Component 5 — Annotations on pages {sorted(pages_with_underline)}, expected {sorted(EXPECTED_PAGES_WITH_ANNOTS)} (partial: {partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 — No pages with underline annotations")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Annotations cover actual defined term text (0.2 points)
    # Check that the text under each annotation contains one of the expected keywords
    # Some defined terms span multiple lines, so also check expanded rect below annotation
    try:
        matched_keywords = set()
        doc2 = fitz.open(OUTPUT_PATH)
        for annot_info in underline_annots:
            text = annot_info["text"]
            page_idx = annot_info["page"]
            rect = annot_info["rect"]
            # Also get text from expanded rect (captures multi-line terms)
            # Some defined terms wrap to the next line, so expand down significantly
            page = doc2[page_idx]
            expanded_rect = fitz.Rect(
                max(0, rect[0] - 10), rect[1],
                min(page.rect.width, rect[2] + 200), rect[3] + 25
            )
            expanded_text = page.get_textbox(expanded_rect).strip()
            # Also check the line immediately below the annotation
            next_line_rect = fitz.Rect(50, rect[3], 550, rect[3] + 20)
            next_line_text = page.get_textbox(next_line_rect).strip()
            combined = text + " " + expanded_text + " " + next_line_text
            for kw in DEFINED_TERM_KEYWORDS:
                if kw.lower() in combined.lower():
                    matched_keywords.add(kw)
        doc2.close()

        match_count = len(matched_keywords)
        expected_kw_count = len(DEFINED_TERM_KEYWORDS)

        if match_count >= expected_kw_count * 0.9:  # allow slight tolerance
            print(f"PASS: Component 6 — {match_count}/{expected_kw_count} defined term keywords found in annotation text (0.2 pts)")
            total_score += 0.2
        elif match_count > 0:
            partial = round(0.2 * match_count / expected_kw_count, 2)
            partial = min(partial, 0.15)  # cap partial
            print(f"FAIL: Component 6 — Only {match_count}/{expected_kw_count} keywords matched: {sorted(matched_keywords)} (partial: {partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 6 — No defined term keywords found in annotation text")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()

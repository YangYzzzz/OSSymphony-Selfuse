"""
Reward Script: Export presentation as accessible PDF with tagged PDF and bookmarks
Task ID: impstruct_049
Domain: libreoffice_impress
Scoring:
  Component 1: PDF file exists at /home/user/Desktop/accessible.pdf (0.2 pts)
               — only awards if file is a valid PDF, not just existence
  Component 2: PDF has correct page count matching source pptx (0.2 pts)
  Component 3: Tagged PDF enabled (MarkInfo/Marked true + StructTreeRoot) (0.3 pts)
  Component 4: Bookmarks/outlines exported (TOC entries present) (0.3 pts)
"""

import os
import sys

# pymupdf must be installed on the VM (pip3 install pymupdf)
try:
    import fitz
except ImportError:
    print("CRITICAL: pymupdf not installed. Run: pip3 install pymupdf")
    print("REWARD: 0.0")
    sys.exit(0)

WORKDIR = '/home/user'
TASK_ID = 'impstruct_049'
PDF_PATH = '/home/user/Desktop/accessible.pdf'
PPTX_PATH = '/home/user/accessible_deck.pptx'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ---------------------------------------------------------------
    # Component 1: PDF file exists and is a valid PDF (0.2 points)
    # This is task-introduced: initial_env has no PDF at all.
    # ---------------------------------------------------------------
    try:
        if not os.path.isfile(PDF_PATH):
            print(f"FAIL: Component 1 — PDF not found at {PDF_PATH}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        doc = fitz.open(PDF_PATH)
        if len(doc) == 0:
            print(f"FAIL: Component 1 — PDF has 0 pages, invalid")
            doc.close()
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        print(f"PASS: Component 1 — Valid PDF found at {PDF_PATH} with {len(doc)} pages (0.2 pts)")
        total_score += 0.2
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # ---------------------------------------------------------------
    # Component 2: PDF page count matches source presentation (0.2 points)
    # The source pptx has 10 slides; the PDF should have 10 pages.
    # ---------------------------------------------------------------
    try:
        pdf_pages = len(doc)
        expected_pages = 10  # from task context: 10 slides

        if pdf_pages == expected_pages:
            print(f"PASS: Component 2 — PDF has {pdf_pages} pages matching {expected_pages} slides (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — PDF has {pdf_pages} pages, expected {expected_pages}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ---------------------------------------------------------------
    # Component 3: Tagged PDF enabled (0.3 points)
    # Check that the PDF catalog contains MarkInfo with Marked=true
    # and a StructTreeRoot reference (document structure tags).
    # ---------------------------------------------------------------
    try:
        cat_xref = doc.pdf_catalog()
        cat_str = doc.xref_object(cat_xref)

        has_markinfo = '/MarkInfo' in cat_str
        has_marked_true = '/Marked true' in cat_str
        has_struct_tree = '/StructTreeRoot' in cat_str

        if has_markinfo and has_marked_true and has_struct_tree:
            print(f"PASS: Component 3 — Tagged PDF enabled: MarkInfo/Marked=true, StructTreeRoot present (0.3 pts)")
            total_score += 0.3
        else:
            details = []
            if not has_markinfo:
                details.append("missing /MarkInfo")
            if not has_marked_true:
                details.append("Marked not set to true")
            if not has_struct_tree:
                details.append("missing /StructTreeRoot")
            print(f"FAIL: Component 3 — Tagged PDF issues: {', '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ---------------------------------------------------------------
    # Component 4: Bookmarks/outlines exported (0.3 points)
    # Check that the PDF has a table of contents (outlines/bookmarks).
    # The exported PDF should have bookmark entries for the slides.
    # ---------------------------------------------------------------
    try:
        toc = doc.get_toc()
        # Also check catalog for /Outlines reference
        has_outlines_ref = '/Outlines' in cat_str

        if len(toc) > 0 and has_outlines_ref:
            print(f"PASS: Component 4 — Bookmarks exported: {len(toc)} TOC entries, /Outlines in catalog (0.3 pts)")
            total_score += 0.3
        elif len(toc) > 0:
            # TOC exists but no explicit Outlines ref — still valid
            print(f"PASS: Component 4 — Bookmarks exported: {len(toc)} TOC entries (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 4 — No bookmarks/outlines found in PDF (TOC empty)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

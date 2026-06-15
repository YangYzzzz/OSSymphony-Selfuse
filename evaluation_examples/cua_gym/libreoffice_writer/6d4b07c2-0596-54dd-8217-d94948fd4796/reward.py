"""
Reward Script: Export technical manual to PDF with bookmarks, hyperlinks, and tagged structure
Task ID: writer_tech_056
Domain: libreoffice_writer
Scoring:
  Component 1: PDF file exists at expected path (0.15 pts)
  Component 2: Bookmarks/TOC generated from headings (0.35 pts)
  Component 3: Tagged PDF structure for accessibility (0.25 pts)
  Component 4: Hyperlink URLs preserved in PDF text (0.25 pts)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_tech_056'


def verify_task(pdf_path):
    """
    Verify PDF export with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: PDF file exists (0.15 points)
    # This is the core task change — initial_env has no PDF, golden_env does
    try:
        if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 1000:
            print(f"PASS: Component 1 — PDF exists at {pdf_path}, size={os.path.getsize(pdf_path)} bytes (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — PDF not found or too small at {pdf_path}")
            # If no PDF, nothing else to check
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Load PDF with PyMuPDF
    try:
        import fitz
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {pdf_path}: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Bookmarks/TOC from headings (0.35 points)
    # The docx has Heading 1/2/3 styles; the PDF should have a bookmark tree
    try:
        toc = doc.get_toc()
        num_bookmarks = len(toc)
        if num_bookmarks >= 20:
            # Full bookmark tree with multi-level headings
            # Check that there are multiple levels (at least 2 distinct levels)
            levels = set(entry[0] for entry in toc)
            if len(levels) >= 2:
                print(f"PASS: Component 2 — {num_bookmarks} bookmarks with {len(levels)} heading levels (0.35 pts)")
                total_score += 0.35
            else:
                # Single level only — partial credit
                print(f"PARTIAL: Component 2 — {num_bookmarks} bookmarks but only {len(levels)} level(s) (0.20 pts)")
                total_score += 0.20
        elif num_bookmarks >= 5:
            # Some bookmarks but incomplete
            print(f"PARTIAL: Component 2 — Only {num_bookmarks} bookmarks found (expected 20+) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Only {num_bookmarks} bookmarks found (expected 20+)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Tagged PDF structure for accessibility (0.25 points)
    # Check for MarkInfo with Marked=true and StructTreeRoot in the PDF catalog
    try:
        has_mark_info = False
        has_struct_tree = False
        xref_count = doc.xref_length()
        for i in range(1, xref_count):
            obj_str = doc.xref_object(i)
            if 'MarkInfo' in obj_str and 'Marked true' in obj_str:
                has_mark_info = True
            if 'StructTreeRoot' in obj_str:
                has_struct_tree = True
            if has_mark_info and has_struct_tree:
                break

        if has_mark_info and has_struct_tree:
            print(f"PASS: Component 3 — Tagged PDF: MarkInfo/Marked=true and StructTreeRoot present (0.25 pts)")
            total_score += 0.25
        elif has_struct_tree:
            print(f"PARTIAL: Component 3 — StructTreeRoot found but MarkInfo missing (0.15 pts)")
            total_score += 0.15
        elif has_mark_info:
            print(f"PARTIAL: Component 3 — MarkInfo found but StructTreeRoot missing (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 — No tagged PDF structure found (no MarkInfo or StructTreeRoot)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Hyperlink URLs preserved in PDF (0.25 points)
    # The source docx has 8 hyperlinks; check that URL text appears in the PDF
    try:
        expected_urls = [
            "developer.cloudsync.example.com",
            "api.cloudsync.example.com/docs",
            "community.cloudsync.example.com",
            "github.com/cloudsync/deploy",
            "docs.cloudsync.example.com/security/tls",
            "api.cloudsync.example.com/docs/webhooks",
            "docs.cloudsync.example.com/troubleshooting",
            "support.cloudsync.example.com",
        ]

        # Extract all text from PDF
        full_text = ""
        for page_num in range(doc.page_count):
            full_text += doc[page_num].get_text()

        found_count = 0
        for url_fragment in expected_urls:
            if url_fragment in full_text:
                found_count += 1

        if found_count >= 6:
            print(f"PASS: Component 4 — {found_count}/{len(expected_urls)} hyperlink URLs found in PDF text (0.25 pts)")
            total_score += 0.25
        elif found_count >= 3:
            ratio = found_count / len(expected_urls)
            partial = round(0.25 * ratio, 2)
            print(f"PARTIAL: Component 4 — {found_count}/{len(expected_urls)} hyperlink URLs found (0.{int(partial*100):02d} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — Only {found_count}/{len(expected_urls)} hyperlink URLs found in PDF text")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path
pdf_path = f'{WORKDIR}/{TASK_ID}.pdf'
if not os.path.exists(pdf_path):
    print(f"File not found: {pdf_path}")
    print("REWARD: 0.0")
else:
    verify_task(pdf_path)

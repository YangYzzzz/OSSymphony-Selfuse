"""
Reward Script: Add redaction annotations to confidential terms in settlement PDF
Task ID: pdf_legal_060
Domain: pdf
Scoring:
  - Component 1 (0.15): Output file exists and is a valid 8-page PDF
  - Component 2 (0.15): Content NOT actually redacted (text still visible)
  - Component 3 (0.25): Dollar amounts on page 2 (index 1) marked with Redact annotations
  - Component 4 (0.20): Large redaction rect on page 3 (index 2) near (72,300)-(540,400)
  - Component 5 (0.25): 'Plaintiff Name' instances marked with Redact annotations across pages
"""

import os
import re
import fitz  # PyMuPDF

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_060'
TARGET_FILE = os.path.join(WORKDIR, 'legal', 'proposed_settlement_marked.pdf')
ORIGINAL_FILE = os.path.join(WORKDIR, 'legal', 'proposed_settlement.pdf')

REDACT_TYPE = 12  # PyMuPDF annotation type code for Redact


def get_redact_annots(page):
    """Get all Redact-type annotations on a page."""
    annots = list(page.annots()) if page.annots() else []
    return [a for a in annots if a.type[0] == REDACT_TYPE]


def rects_overlap(r1, r2, threshold=0.5):
    """Check if two rects overlap significantly. r1, r2 are fitz.Rect or tuples (x0,y0,x1,y1)."""
    if not isinstance(r1, fitz.Rect):
        r1 = fitz.Rect(r1)
    if not isinstance(r2, fitz.Rect):
        r2 = fitz.Rect(r2)
    intersection = r1 & r2
    if intersection.is_empty:
        return False
    inter_area = intersection.width * intersection.height
    r2_area = r2.width * r2.height
    if r2_area == 0:
        return False
    return (inter_area / r2_area) >= threshold


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists and is a valid 8-page PDF (0.15 points)
    try:
        if not os.path.exists(file_path):
            print("FAIL: Component 1 -- output file does not exist: %s" % file_path)
            print("REWARD: 0.0")
            return 0.0

        doc = fitz.open(file_path)
        page_count = doc.page_count

        if page_count == 8:
            print("PASS: Component 1 -- valid PDF with %d pages (0.15 pts)" % page_count)
            total_score += 0.15
        else:
            print("FAIL: Component 1 -- expected 8 pages, found %d" % page_count)
    except Exception as e:
        print("CRITICAL: Cannot load file %s: %s" % (file_path, e))
        print("REWARD: 0.0")
        return 0.0

    # Component 2: Content NOT actually redacted -- text still visible (0.15 points)
    # The task says "without applying them", so dollar amounts and Plaintiff Name should still be readable
    try:
        page1_text = doc[1].get_text()  # page 2 in doc (0-indexed)
        dollar_amounts = re.findall(r'\$[\d,]+\.?\d*', page1_text)
        has_dollars = len(dollar_amounts) >= 3  # should have many dollar amounts still visible

        plaintiff_visible = any("Plaintiff Name" in doc[i].get_text() for i in range(doc.page_count))

        if has_dollars and plaintiff_visible:
            print("PASS: Component 2 -- content still visible (not applied): %d dollar amounts on page 2, 'Plaintiff Name' present (0.15 pts)" % len(dollar_amounts))
            total_score += 0.15
        else:
            print("FAIL: Component 2 -- content appears redacted (dollars visible: %s, plaintiff visible: %s)" % (has_dollars, plaintiff_visible))
    except Exception as e:
        print("ERROR: Component 2 -- %s" % e)

    # Component 3: Dollar amounts on page 2 (index 1) marked with Redact annotations (0.25 points)
    # The task says "all dollar amounts on page 2" -- page 2 in the doc is index 1 (0-based)
    try:
        page1 = doc[1]
        page1_text = page1.get_text()
        dollar_matches = re.findall(r'\$[\d,]+\.?\d*', page1_text)
        redact_annots_p1 = get_redact_annots(page1)

        if len(redact_annots_p1) == 0:
            print("FAIL: Component 3 -- no Redact annotations found on page 2 (index 1)")
        else:
            # Check how many dollar amount locations are covered by redact annotations
            # Search for dollar amount text positions on the page
            covered_count = 0
            for dollar in dollar_matches:
                text_instances = page1.search_for(dollar)
                for inst in text_instances:
                    # Check if any redact annotation covers this text location
                    for annot in redact_annots_p1:
                        annot_rect = fitz.Rect(annot.rect)
                        if annot_rect.intersects(fitz.Rect(inst)):
                            covered_count += 1
                            break
                    break  # only check first instance of each amount

            total_dollars = len(dollar_matches)
            if total_dollars > 0:
                coverage_ratio = covered_count / total_dollars
                if coverage_ratio >= 0.7:
                    print("PASS: Component 3 -- %d/%d dollar amounts covered by Redact annotations on page 2 (0.25 pts)" % (covered_count, total_dollars))
                    total_score += 0.25
                elif coverage_ratio >= 0.4:
                    partial = 0.15
                    print("PARTIAL: Component 3 -- %d/%d dollar amounts covered (%.2f pts)" % (covered_count, total_dollars, partial))
                    total_score += partial
                else:
                    print("FAIL: Component 3 -- only %d/%d dollar amounts covered by Redact" % (covered_count, total_dollars))
            else:
                print("FAIL: Component 3 -- no dollar amounts found in page text")
    except Exception as e:
        print("ERROR: Component 3 -- %s" % e)

    # Component 4: Large redaction rect on page 3 (index 2) near (72,300)-(540,400) (0.20 points)
    try:
        page2 = doc[2]
        redact_annots_p2 = get_redact_annots(page2)

        # Look for a large redaction annotation that covers approximately (72,300)-(540,400)
        expected_rect = fitz.Rect(72, 300, 540, 400)
        # Search for a large annotation covering the settlement terms area
        large_matches = [a for a in redact_annots_p2
                         if fitz.Rect(a.rect).width > 200
                         and fitz.Rect(a.rect).height > 40
                         and rects_overlap(fitz.Rect(a.rect), expected_rect, threshold=0.3)]

        if len(large_matches) > 0:
            matched_rect = tuple(fitz.Rect(large_matches[0].rect))
            print("PASS: Component 4 -- large Redact annotation found on page 3 at %s covering settlement terms (0.20 pts)" % str(matched_rect))
            total_score += 0.20
        else:
            # Check if multiple smaller annotations collectively cover the area
            annots_in_area = [a for a in redact_annots_p2 if fitz.Rect(a.rect).intersects(expected_rect)]
            if len(annots_in_area) >= 1:
                print("PARTIAL: Component 4 -- found %d Redact annotation(s) intersecting with settlement terms area but no single large rect (0.10 pts)" % len(annots_in_area))
                total_score += 0.10
            else:
                print("FAIL: Component 4 -- no Redact annotation found near (72,300)-(540,400) on page 3")
    except Exception as e:
        print("ERROR: Component 4 -- %s" % e)

    # Component 5: 'Plaintiff Name' instances marked with Redact annotations (0.25 points)
    # The task says "all instances of 'Plaintiff Name' throughout"
    try:
        pages_with_plaintiff_redacts = 0
        total_plaintiff_instances = 0
        covered_plaintiff_instances = 0

        for i in range(doc.page_count):
            page = doc[i]
            text = page.get_text()
            pn_count = text.count("Plaintiff Name")
            if pn_count == 0:
                continue

            total_plaintiff_instances += pn_count
            redact_annots = get_redact_annots(page)
            if len(redact_annots) == 0:
                continue

            # Search for 'Plaintiff Name' text positions
            text_instances = page.search_for("Plaintiff Name")
            page_covered = 0
            for inst in text_instances:
                for annot in redact_annots:
                    annot_rect = fitz.Rect(annot.rect)
                    if annot_rect.intersects(fitz.Rect(inst)):
                        page_covered += 1
                        break

            if page_covered > 0:
                pages_with_plaintiff_redacts += 1
            covered_plaintiff_instances += page_covered

        if total_plaintiff_instances > 0:
            coverage = covered_plaintiff_instances / total_plaintiff_instances
            # We need coverage across multiple pages
            if coverage >= 0.7 and pages_with_plaintiff_redacts >= 3:
                print("PASS: Component 5 -- %d/%d 'Plaintiff Name' instances covered across %d pages (0.25 pts)" % (covered_plaintiff_instances, total_plaintiff_instances, pages_with_plaintiff_redacts))
                total_score += 0.25
            elif coverage >= 0.4 and pages_with_plaintiff_redacts >= 2:
                partial = 0.15
                print("PARTIAL: Component 5 -- %d/%d instances covered across %d pages (%.2f pts)" % (covered_plaintiff_instances, total_plaintiff_instances, pages_with_plaintiff_redacts, partial))
                total_score += partial
            else:
                print("FAIL: Component 5 -- only %d/%d instances covered across %d pages" % (covered_plaintiff_instances, total_plaintiff_instances, pages_with_plaintiff_redacts))
        else:
            print("FAIL: Component 5 -- no 'Plaintiff Name' text found in document")
    except Exception as e:
        print("ERROR: Component 5 -- %s" % e)

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print("\nScore: %.2f/1.0" % total_score)
    print("REWARD: %.1f" % final_score)
    return final_score


# Default: test against canonical artifact path
if not os.path.exists(TARGET_FILE):
    print("File not found: %s" % TARGET_FILE)
    print("REWARD: 0.0")
else:
    verify_task(TARGET_FILE)

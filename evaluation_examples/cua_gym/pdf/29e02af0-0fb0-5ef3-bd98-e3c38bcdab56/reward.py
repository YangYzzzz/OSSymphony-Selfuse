"""
Reward Script: Annotate audit findings on financial statement PDF
Task ID: pdf_fin_017
Domain: pdf
Scoring:
  Component 1 (0.15): Output file exists at expected path
  Component 2 (0.30): Highlight annotation on page 2 (index 1) covering revenue area
  Component 3 (0.30): Text (sticky note) annotation on page 2 with correct comment
  Component 4 (0.25): Circle annotation on page 3 (index 2) in red color
"""

import os
import fitz  # PyMuPDF

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_017'
OUTPUT_PATH = os.path.join(WORKDIR, 'finance', 'income_statement_2023_annotated.pdf')


def get_annotations(doc, page_num):
    """Get all annotations on a page with their properties."""
    page = doc[page_num]
    annots = []
    if page.annots():
        for annot in page.annots():
            annots.append({
                "type_name": annot.type[1],       # "Highlight", "Text", "Circle", etc.
                "type_code": annot.type[0],
                "content": annot.info.get("content", ""),
                "rect": tuple(annot.rect),         # (x0, y0, x1, y1)
                "colors": {
                    "stroke": annot.colors.get("stroke"),
                    "fill": annot.colors.get("fill"),
                },
            })
    return annots


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: output file must exist
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

    # Component 1: Output file exists and is a valid annotated PDF (0.15 points)
    # This checks that the file exists AND has annotations — the initial env has no
    # annotated file at all, so this differentiates initial from golden.
    try:
        total_annots = 0
        for i in range(len(doc)):
            page_annots = get_annotations(doc, i)
            total_annots += len(page_annots)

        if total_annots >= 3:
            print(f"PASS: Component 1 — Annotated PDF has {total_annots} annotations (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Expected >= 3 annotations, found {total_annots}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Highlight annotation on page 2 (index 1) in revenue area (0.30 points)
    # Task specifies: highlight on page 2, rect approx (100,300,500,320)
    try:
        page1_annots = get_annotations(doc, 1)  # page 2 = index 1
        highlight_annots = [a for a in page1_annots if a["type_name"] == "Highlight"]

        if len(highlight_annots) >= 1:
            # Check that at least one highlight overlaps the expected revenue area
            expected_rect = fitz.Rect(100, 300, 500, 320)
            found_overlap = False
            for h in highlight_annots:
                annot_rect = fitz.Rect(h["rect"])
                # Check intersection — annotation should overlap the target area
                if annot_rect.intersects(expected_rect):
                    found_overlap = True
                    print(f"PASS: Component 2 — Highlight on page 2 at {h['rect']} overlaps revenue area (0.30 pts)")
                    total_score += 0.30
                    break
            if not found_overlap:
                print(f"FAIL: Component 2 — Highlight(s) on page 2 do not overlap revenue area (100,300,500,320). Found: {[h['rect'] for h in highlight_annots]}")
        else:
            print(f"FAIL: Component 2 — No Highlight annotation on page 2. Annotations found: {[a['type_name'] for a in page1_annots]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Text annotation (sticky note) on page 2 with correct comment (0.30 points)
    # Task specifies: text comment at (520,310) saying "Revenue recognition timing needs review - see AS 606"
    try:
        page1_annots = get_annotations(doc, 1)  # page 2 = index 1
        text_annots = [a for a in page1_annots if a["type_name"] == "Text"]

        if len(text_annots) >= 1:
            expected_content = "Revenue recognition timing needs review - see AS 606"
            found_match = False
            for t in text_annots:
                content = t["content"].strip()
                if expected_content.lower() in content.lower():
                    # Also check approximate position — should be near (520, 310)
                    rx0, ry0 = t["rect"][0], t["rect"][1]
                    pos_ok = abs(rx0 - 520) < 30 and abs(ry0 - 310) < 30
                    if pos_ok:
                        print(f"PASS: Component 3 — Text annotation on page 2 with correct content at {t['rect']} (0.30 pts)")
                        total_score += 0.30
                    else:
                        # Content matches but position is off — give partial credit
                        print(f"PARTIAL: Component 3 — Text annotation content correct but position {t['rect']} far from expected (520,310) (0.20 pts)")
                        total_score += 0.20
                    found_match = True
                    break
            if not found_match:
                print(f"FAIL: Component 3 — No Text annotation with expected content. Found: {[(t['content'][:50], t['rect']) for t in text_annots]}")
        else:
            print(f"FAIL: Component 3 — No Text annotation on page 2. Annotations found: {[a['type_name'] for a in page1_annots]}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Circle annotation on page 3 (index 2) in red (0.25 points)
    # Task specifies: circle on page 3, rect (200,450,400,470), red color
    try:
        page2_annots = get_annotations(doc, 2)  # page 3 = index 2
        circle_annots = [a for a in page2_annots if a["type_name"] == "Circle"]

        if len(circle_annots) >= 1:
            expected_rect = fitz.Rect(200, 450, 400, 470)
            found_match = False
            for c in circle_annots:
                annot_rect = fitz.Rect(c["rect"])
                if annot_rect.intersects(expected_rect):
                    # Check red color (stroke should be (1, 0, 0))
                    stroke = c["colors"].get("stroke")
                    if stroke and len(stroke) >= 3:
                        is_red = (abs(stroke[0] - 1.0) < 0.1 and
                                  abs(stroke[1] - 0.0) < 0.1 and
                                  abs(stroke[2] - 0.0) < 0.1)
                        if is_red:
                            print(f"PASS: Component 4 — Red circle on page 3 at {c['rect']} (0.25 pts)")
                            total_score += 0.25
                            found_match = True
                            break
                        else:
                            print(f"FAIL: Component 4 — Circle on page 3 not red, stroke={stroke}")
                    else:
                        print(f"FAIL: Component 4 — Circle on page 3 has no stroke color: {c['colors']}")
                else:
                    print(f"INFO: Component 4 — Circle at {c['rect']} does not overlap expected area")
            if not found_match and not any(fitz.Rect(c["rect"]).intersects(expected_rect) for c in circle_annots):
                print(f"FAIL: Component 4 — No Circle annotation overlapping expected area on page 3. Found: {[c['rect'] for c in circle_annots]}")
        else:
            print(f"FAIL: Component 4 — No Circle annotation on page 3. Annotations found: {[a['type_name'] for a in page2_annots]}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

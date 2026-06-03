"""
Reward Script: Add numbered exhibit stickers to deposition exhibit package
Task ID: pdf_legal_088
Domain: pdf
Scoring:
  Component 1 (0.10): Output file exists at correct path
  Component 2 (0.50): All 5 exhibit labels present with correct text on correct pages (0.10 each)
  Component 3 (0.20): Labels have correct style (bold, ~14pt, red color)
  Component 4 (0.10): Labels positioned in top-right region of pages
  Component 5 (0.10): Non-exhibit pages have no spurious labels
"""

import os
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    import pymupdf as fitz

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_088'
OUTPUT_PATH = f'{WORKDIR}/legal/depo/exhibits_package_labeled.pdf'

# Exhibit definitions: (1-indexed page number, expected label text)
EXHIBITS = [
    (1,  "Deposition Exhibit 1"),
    (8,  "Deposition Exhibit 2"),
    (15, "Deposition Exhibit 3"),
    (20, "Deposition Exhibit 4"),
    (28, "Deposition Exhibit 5"),
]


def find_exhibit_spans(page):
    """Find all text spans containing 'Deposition Exhibit' on a page.
    Returns list of dicts with text, font, size, color_rgb, is_bold, bbox."""
    results = []
    data = page.get_text("dict")
    for block in data["blocks"]:
        if block.get("type", 0) != 0:
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                if "Deposition Exhibit" in span["text"]:
                    color_int = span["color"]
                    r = (color_int >> 16) & 0xFF
                    g = (color_int >> 8) & 0xFF
                    b = color_int & 0xFF
                    results.append({
                        "text": span["text"].strip(),
                        "font": span["font"],
                        "size": span["size"],
                        "color_rgb": (r, g, b),
                        "is_bold": bool(span["flags"] & 16),
                        "bbox": span["bbox"],  # (x0, y0, x1, y1)
                    })
    return results


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists (0.10 points)
    # This is task-introduced: the labeled file does not exist in initial_env.
    try:
        if not os.path.exists(file_path):
            print(f"FAIL: Component 1 — Output file not found at {file_path}")
            print("REWARD: 0.0")
            return 0.0

        doc = fitz.open(file_path)
        if len(doc) != 35:
            print(f"FAIL: Component 1 — Expected 35 pages, found {len(doc)}")
            print("REWARD: 0.0")
            return 0.0

        print(f"PASS: Component 1 — Output file exists with 35 pages (0.10 pts)")
        total_score += 0.10
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: All 5 exhibit labels present with correct text (0.50 points, 0.10 each)
    try:
        labels_found = 0
        for page_num_1indexed, expected_label in EXHIBITS:
            page_idx = page_num_1indexed - 1
            page = doc[page_idx]
            spans = find_exhibit_spans(page)

            matched = False
            for sp in spans:
                if sp["text"] == expected_label:
                    matched = True
                    break

            if matched:
                print(f"PASS: Component 2.{labels_found+1} — '{expected_label}' found on page {page_num_1indexed} (0.10 pts)")
                total_score += 0.10
                labels_found += 1
            else:
                found_texts = [sp["text"] for sp in spans]
                print(f"FAIL: Component 2 — '{expected_label}' NOT found on page {page_num_1indexed}. Found: {found_texts}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Labels have correct style — bold, ~14pt, red (0.20 points)
    # Check all found labels for style compliance
    try:
        style_checks_passed = 0
        style_checks_total = 0
        for page_num_1indexed, expected_label in EXHIBITS:
            page_idx = page_num_1indexed - 1
            page = doc[page_idx]
            spans = find_exhibit_spans(page)

            for sp in spans:
                if sp["text"] == expected_label:
                    style_checks_total += 1
                    # Check: bold
                    is_bold = sp["is_bold"] or "Bold" in sp["font"] or "bold" in sp["font"].lower()
                    # Check: ~14pt (allow tolerance)
                    is_14pt = abs(sp["size"] - 14.0) <= 1.0
                    # Check: red color (R high, G and B low)
                    r, g, b = sp["color_rgb"]
                    is_red = r >= 200 and g <= 50 and b <= 50

                    if is_bold and is_14pt and is_red:
                        style_checks_passed += 1
                    else:
                        reasons = []
                        if not is_bold:
                            reasons.append(f"not bold (font={sp['font']}, flags bold={sp['is_bold']})")
                        if not is_14pt:
                            reasons.append(f"size={sp['size']} (expected ~14)")
                        if not is_red:
                            reasons.append(f"color=({r},{g},{b}) (expected red)")
                        print(f"FAIL: Component 3 — Style issue on page {page_num_1indexed}: {', '.join(reasons)}")
                    break

        if style_checks_total > 0 and style_checks_passed == style_checks_total:
            print(f"PASS: Component 3 — All {style_checks_passed} labels have correct style (bold, 14pt, red) (0.20 pts)")
            total_score += 0.20
        elif style_checks_total > 0:
            partial = 0.20 * (style_checks_passed / style_checks_total)
            print(f"PARTIAL: Component 3 — {style_checks_passed}/{style_checks_total} labels with correct style ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No labels found to check style")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Labels positioned in top-right region (0.10 points)
    # Top-right means: x > page_width/2 and y < page_height * 0.15
    try:
        position_ok = 0
        position_total = 0
        for page_num_1indexed, expected_label in EXHIBITS:
            page_idx = page_num_1indexed - 1
            page = doc[page_idx]
            pw, ph = page.rect.width, page.rect.height
            spans = find_exhibit_spans(page)

            for sp in spans:
                if sp["text"] == expected_label:
                    position_total += 1
                    x0, y0, x1, y1 = sp["bbox"]
                    # Check top-right: right half of page, top portion
                    in_right = x1 > pw / 2
                    in_top = y0 < ph * 0.15
                    if in_right and in_top:
                        position_ok += 1
                    else:
                        print(f"FAIL: Component 4 — Label on page {page_num_1indexed} at bbox={sp['bbox']}, page size=({pw},{ph}), right={in_right}, top={in_top}")
                    break

        if position_total > 0 and position_ok == position_total:
            print(f"PASS: Component 4 — All {position_ok} labels in top-right region (0.10 pts)")
            total_score += 0.10
        elif position_total > 0:
            partial = 0.10 * (position_ok / position_total)
            print(f"PARTIAL: Component 4 — {position_ok}/{position_total} labels in top-right ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No labels found to check position")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Non-exhibit pages have no spurious labels (0.10 points)
    try:
        exhibit_page_indices = set(p - 1 for p, _ in EXHIBITS)
        spurious_count = 0
        for pg_idx in range(len(doc)):
            if pg_idx in exhibit_page_indices:
                continue
            page = doc[pg_idx]
            spans = find_exhibit_spans(page)
            if spans:
                spurious_count += 1
                print(f"FAIL: Component 5 — Spurious exhibit label on page {pg_idx+1}: {[s['text'] for s in spans]}")

        if spurious_count == 0:
            print(f"PASS: Component 5 — No spurious labels on non-exhibit pages (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 — Found spurious labels on {spurious_count} non-exhibit pages")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_PATH)

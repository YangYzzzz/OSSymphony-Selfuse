"""
Reward Script: Strikethrough old prices and add new prices in PDF
Task ID: pdf_ro_027
Domain: pdf
Scoring:
  Component 1 (0.15): All 4 pages preserved in output file
  Component 2 (0.35): 8 red StrikeOut annotations over '$49.99' instances
  Component 3 (0.30): 8 instances of '$39.99' text inserted
  Component 4 (0.20): '$39.99' text properties — green color, bold, ~12pt
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_027'

def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("CRITICAL: PyMuPDF (fitz) not available")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: file must exist (gate, not scored)
    if not os.path.exists(file_path):
        print(f"PRECONDITION FAIL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: All 4 pages preserved (0.15 points)
    # The output file must have exactly 4 pages matching the original
    try:
        page_count = doc.page_count
        if page_count == 4:
            print(f"PASS: Component 1 — PDF has 4 pages as expected (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Expected 4 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 8 red StrikeOut annotations over '$49.99' (0.35 points)
    # Each valid strikeout earns 0.35/8 points
    try:
        strikeout_count = 0
        red_strikeout_count = 0
        overlapping_strikeout_count = 0

        for page_num in range(doc.page_count):
            page = doc[page_num]
            old_price_rects = page.search_for("$49.99")

            for annot in page.annots():
                if annot.type[1] == "StrikeOut":
                    strikeout_count += 1
                    # Check red color
                    stroke_color = annot.colors.get("stroke")
                    is_red = (stroke_color is not None and
                              len(stroke_color) >= 3 and
                              stroke_color[0] > 0.8 and
                              stroke_color[1] < 0.2 and
                              stroke_color[2] < 0.2)
                    if is_red:
                        red_strikeout_count += 1

                    # Check overlap with '$49.99' text
                    for rect in old_price_rects:
                        if annot.rect.intersects(rect):
                            if is_red:
                                overlapping_strikeout_count += 1
                            break

        points_per_annot = 0.35 / 8
        comp2_score = min(overlapping_strikeout_count * points_per_annot, 0.35)

        if overlapping_strikeout_count == 8:
            print(f"PASS: Component 2 — Found 8 red StrikeOut annotations over '$49.99' (0.35 pts)")
            total_score += 0.35
        elif overlapping_strikeout_count > 0:
            total_score += comp2_score
            print(f"PARTIAL: Component 2 — Found {overlapping_strikeout_count}/8 red strikeouts "
                  f"(total strikeouts={strikeout_count}, red={red_strikeout_count}) "
                  f"({comp2_score:.3f} pts)")
        else:
            print(f"FAIL: Component 2 — No red strikeout annotations found over '$49.99'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 8 instances of '$39.99' text inserted (0.30 points)
    # Each instance earns 0.30/8 points
    try:
        new_price_count = 0
        for page_num in range(doc.page_count):
            page = doc[page_num]
            instances = page.search_for("$39.99")
            new_price_count += len(instances)

        points_per_text = 0.30 / 8
        comp3_score = min(new_price_count * points_per_text, 0.30)

        if new_price_count >= 8:
            print(f"PASS: Component 3 — Found {new_price_count} instances of '$39.99' (0.30 pts)")
            total_score += 0.30
        elif new_price_count > 0:
            print(f"PARTIAL: Component 3 — Found {new_price_count}/8 instances of '$39.99' ({comp3_score:.3f} pts)")
            total_score += comp3_score
        else:
            print(f"FAIL: Component 3 — No instances of '$39.99' found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: '$39.99' text properties — green, bold, ~12pt (0.20 points)
    # Check text spans for color=#008000 (32768), bold flag, fontsize ~12
    try:
        matching_spans = 0
        total_spans = 0

        for page_num in range(doc.page_count):
            page = doc[page_num]
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" not in block:
                    continue
                for line in block["lines"]:
                    for span in line["spans"]:
                        if "$39.99" in span["text"]:
                            total_spans += 1
                            # Check color: 32768 = 0x008000 = green
                            color_ok = span["color"] == 32768
                            # Check bold: flags bit 4 (value 16) indicates bold
                            bold_ok = (span["flags"] & 16) != 0
                            # Check font size ~ 12pt (allow small tolerance)
                            size_ok = abs(span["size"] - 12.0) < 1.0

                            if color_ok and bold_ok and size_ok:
                                matching_spans += 1
                            else:
                                details = []
                                if not color_ok:
                                    details.append(f"color={span['color']} (expected 32768)")
                                if not bold_ok:
                                    details.append(f"flags={span['flags']} (no bold)")
                                if not size_ok:
                                    details.append(f"size={span['size']} (expected ~12)")
                                print(f"  INFO: Page {page_num} span mismatch: {', '.join(details)}")

        if total_spans >= 8 and matching_spans >= 8:
            print(f"PASS: Component 4 — All {matching_spans} '$39.99' spans are green/bold/12pt (0.20 pts)")
            total_score += 0.20
        elif matching_spans > 0:
            comp4_score = 0.20 * (matching_spans / max(total_spans, 8))
            print(f"PARTIAL: Component 4 — {matching_spans}/{total_spans} spans have correct properties ({comp4_score:.3f} pts)")
            total_score += comp4_score
        else:
            print(f"FAIL: Component 4 — No '$39.99' spans with correct green/bold/12pt properties "
                  f"(found {total_spans} spans total)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {total_score:.4f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/marketing/price_list_updated.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

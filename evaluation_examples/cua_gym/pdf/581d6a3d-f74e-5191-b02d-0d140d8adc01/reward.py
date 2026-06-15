"""
Reward Script: Copy annotations from source_review.pdf page 5 to target_review.pdf page 5
Task ID: pdf_fm_048
Domain: pdf
Scoring:
  Component 1 (0.25): Correct annotation count (4 annotations on page 5)
  Component 2 (0.25): Correct annotation types (2 Highlight + 2 Text)
  Component 3 (0.25): Annotation positions match source within tolerance
  Component 4 (0.25): Annotation content and colors match source
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_048'

TARGET_PATH = os.path.join(WORKDIR, 'Documents', 'target_review.pdf')
SOURCE_PATH = os.path.join(WORKDIR, 'Documents', 'source_review.pdf')
PAGE_IDX = 4  # 0-indexed page 5

# Position tolerance in points
POS_TOLERANCE = 5.0


def get_annotations(pdf_path, page_num):
    """Get all annotations on a page with properties."""
    doc = pymupdf.open(pdf_path)
    page = doc[page_num]
    annots = []
    for annot in page.annots():
        annots.append({
            "type_code": annot.type[0],
            "type_name": annot.type[1],
            "content": annot.info.get("content", ""),
            "rect": tuple(annot.rect),  # (x0, y0, x1, y1)
            "stroke": tuple(annot.colors.get("stroke", [])) if annot.colors.get("stroke") else None,
        })
    doc.close()
    return annots


def rects_match(r1, r2, tol=POS_TOLERANCE):
    """Check if two rects are approximately equal."""
    return all(abs(a - b) < tol for a, b in zip(r1, r2))


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: target file must exist
    if not os.path.exists(TARGET_PATH):
        print(f"CRITICAL: Target file not found: {TARGET_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: source file must exist (for comparison)
    if not os.path.exists(SOURCE_PATH):
        print(f"CRITICAL: Source file not found: {SOURCE_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Get annotations from both files
    try:
        target_annots = get_annotations(TARGET_PATH, PAGE_IDX)
    except Exception as e:
        print(f"CRITICAL: Cannot read target annotations: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        source_annots = get_annotations(SOURCE_PATH, PAGE_IDX)
    except Exception as e:
        print(f"CRITICAL: Cannot read source annotations: {e}")
        print("REWARD: 0.0")
        return 0.0

    print(f"Source annotations on page {PAGE_IDX + 1}: {len(source_annots)}")
    print(f"Target annotations on page {PAGE_IDX + 1}: {len(target_annots)}")

    # Component 1: Correct annotation count — 4 annotations on target page 5 (0.25 points)
    try:
        if len(target_annots) == 4:
            print(f"PASS: Component 1 — Target has exactly 4 annotations (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Expected 4 annotations on target page 5, found {len(target_annots)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Correct annotation types — 2 Highlight + 2 Text (0.25 points)
    try:
        highlight_count = sum(1 for a in target_annots if a["type_name"] == "Highlight")
        text_count = sum(1 for a in target_annots if a["type_name"] == "Text")
        if highlight_count == 2 and text_count == 2:
            print(f"PASS: Component 2 — 2 Highlights + 2 Text annotations found (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Expected 2 Highlight + 2 Text, found {highlight_count} Highlight + {text_count} Text")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Annotation positions match source within tolerance (0.25 points)
    try:
        if len(target_annots) == 0:
            print(f"FAIL: Component 3 — No target annotations to compare positions")
        else:
            matched_positions = 0
            for src in source_annots:
                for tgt in target_annots:
                    if src["type_name"] == tgt["type_name"] and rects_match(src["rect"], tgt["rect"]):
                        matched_positions += 1
                        break
            if matched_positions == 4:
                print(f"PASS: Component 3 — All 4 annotation positions match source (0.25 pts)")
                total_score += 0.25
            elif matched_positions >= 2:
                partial = round(0.25 * matched_positions / 4, 2)
                print(f"PARTIAL: Component 3 — {matched_positions}/4 positions match ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — Only {matched_positions}/4 positions match source")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Annotation content and colors match source (0.25 points)
    try:
        if len(target_annots) == 0:
            print(f"FAIL: Component 4 — No target annotations to compare content/colors")
        else:
            matched_content = 0
            for src in source_annots:
                for tgt in target_annots:
                    if src["type_name"] != tgt["type_name"]:
                        continue
                    if not rects_match(src["rect"], tgt["rect"]):
                        continue
                    # Check content matches
                    content_ok = (src["content"] == tgt["content"])
                    # Check stroke color matches (with tolerance)
                    # Compare stroke colors (both None, or both match within tolerance)
                    color_ok = (
                        (src["stroke"] is None and tgt["stroke"] is None)
                        or (
                            src["stroke"] is not None
                            and tgt["stroke"] is not None
                            and len(src["stroke"]) == len(tgt["stroke"])
                            and all(abs(a - b) < 0.05 for a, b in zip(src["stroke"], tgt["stroke"]))
                        )
                    )
                    if content_ok and color_ok:
                        matched_content += 1
                        break
                    else:
                        if not content_ok:
                            print(f"  Detail: content mismatch for {src['type_name']} at {src['rect'][:2]}: src='{src['content'][:40]}...' tgt='{tgt['content'][:40]}...'")
                        if not color_ok:
                            print(f"  Detail: color mismatch for {src['type_name']} at {src['rect'][:2]}: src={src['stroke']} tgt={tgt['stroke']}")

            if matched_content == 4:
                print(f"PASS: Component 4 — All 4 annotations match content and color (0.25 pts)")
                total_score += 0.25
            elif matched_content >= 1:
                partial = round(0.25 * matched_content / 4, 2)
                print(f"PARTIAL: Component 4 — {matched_content}/4 match content+color ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 — No annotations match content and color")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

"""
Reward Script: Add squiggly underline annotations for proofreading review
Task ID: pdf_res_043
Domain: pdf
Scoring:
  Component 1 (0.20): Output PDF preserves all 8 pages
  Component 2 (0.20): All annotations are Squiggly type
  Component 3 (0.35): At least 15 squiggly annotations present
  Component 4 (0.25): Annotations distributed across at least 5 pages
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_043'

def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: Output file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import fitz
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect annotation data across all pages
    page_count = len(doc)
    all_annots = []
    pages_with_squiggly = set()

    try:
        for i, page in enumerate(doc):
            annot_iter = page.annots()
            if annot_iter:
                for annot in annot_iter:
                    annot_type_name = annot.type[1]
                    all_annots.append({
                        "page": i,
                        "type_name": annot_type_name,
                        "type_code": annot.type[0],
                    })
                    if annot_type_name == "Squiggly":
                        pages_with_squiggly.add(i)
    except Exception as e:
        print(f"ERROR: Failed to iterate annotations: {e}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    squiggly_count = sum(1 for a in all_annots if a["type_name"] == "Squiggly")
    non_squiggly_count = len(all_annots) - squiggly_count

    print(f"INFO: Pages={page_count}, Total annotations={len(all_annots)}, "
          f"Squiggly={squiggly_count}, Non-squiggly={non_squiggly_count}, "
          f"Pages with squiggly={sorted(pages_with_squiggly)}")

    # Component 1: Output PDF preserves all 8 pages (0.20 points)
    try:
        if page_count == 8:
            print(f"PASS: Component 1 -- PDF has 8 pages (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 -- Expected 8 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: All annotations are Squiggly type (0.20 points)
    # This verifies that the task used squiggly underlines specifically, not highlights or other types
    try:
        if len(all_annots) > 0 and non_squiggly_count == 0:
            print(f"PASS: Component 2 -- All {len(all_annots)} annotations are Squiggly type (0.20 pts)")
            total_score += 0.20
        elif len(all_annots) == 0:
            print(f"FAIL: Component 2 -- No annotations found in the PDF")
        else:
            print(f"FAIL: Component 2 -- {non_squiggly_count} non-Squiggly annotations found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: At least 15 squiggly annotations present (0.35 points)
    # Task says 18 total instances; ground truth requires at least 15
    try:
        if squiggly_count >= 15:
            print(f"PASS: Component 3 -- {squiggly_count} squiggly annotations found (>= 15) (0.35 pts)")
            total_score += 0.35
        elif squiggly_count >= 10:
            partial = 0.35 * (squiggly_count - 9) / 6.0  # partial credit from 10 to 15
            print(f"PARTIAL: Component 3 -- {squiggly_count} squiggly annotations (>= 10 but < 15) ({partial:.2f} pts)")
            total_score += round(partial, 2)
        else:
            print(f"FAIL: Component 3 -- Only {squiggly_count} squiggly annotations found (need >= 15)")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Annotations distributed across at least 5 pages (0.25 points)
    # Task covers 8 pages, annotations should appear across most of them
    try:
        num_pages_with_annots = len(pages_with_squiggly)
        if num_pages_with_annots >= 5:
            print(f"PASS: Component 4 -- Squiggly annotations on {num_pages_with_annots} pages (>= 5) (0.25 pts)")
            total_score += 0.25
        elif num_pages_with_annots >= 3:
            partial = 0.25 * (num_pages_with_annots - 2) / 3.0
            print(f"PARTIAL: Component 4 -- Squiggly annotations on {num_pages_with_annots} pages (>= 3 but < 5) ({partial:.2f} pts)")
            total_score += round(partial, 2)
        else:
            print(f"FAIL: Component 4 -- Squiggly annotations only on {num_pages_with_annots} pages (need >= 5)")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/papers/proofreading_draft_marked.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

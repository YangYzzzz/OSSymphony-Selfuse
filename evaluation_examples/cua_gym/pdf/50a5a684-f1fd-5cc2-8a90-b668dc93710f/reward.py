"""
Reward Script: Count and catalog all images in presentation.pdf
Task ID: pdf_cr_052
Domain: pdf
Scoring:
  Component 1 (0.25): Total image count correct (13)
  Component 2 (0.15): Page count in summary correct (8 pages)
  Component 3 (0.35): Per-image entries present with correct format and page numbers
  Component 4 (0.25): Image dimensions accuracy vs actual PDF metadata
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_052'
CATALOG_PATH = os.path.join(WORKDIR, 'Desktop', 'image_catalog.txt')
PDF_PATH = os.path.join(WORKDIR, 'Desktop', 'presentation.pdf')


def get_pdf_image_metadata(pdf_path):
    """Extract ground-truth image metadata from the PDF using PyMuPDF."""
    import fitz
    images = []
    doc = fitz.open(pdf_path)
    for page_idx in range(len(doc)):
        page_num = page_idx + 1
        page_images = doc[page_idx].get_images(full=True)
        for img_idx, img in enumerate(page_images):
            # Tuple: (xref, smask, width, height, bpc, colorspace, altcs, name, filter, extra)
            xref = img[0]
            width = img[2]
            height = img[3]
            bpc = img[4]
            colorspace = img[5]
            images.append({
                'page': page_num,
                'img_num': img_idx + 1,
                'width': width,
                'height': height,
                'bpc': bpc,
                'colorspace': colorspace,
            })
    doc.close()
    return images


def verify_task(catalog_path, pdf_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: catalog file must exist
    if not os.path.exists(catalog_path):
        print(f"CRITICAL: Catalog file not found: {catalog_path}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: PDF must exist (needed for ground-truth comparison)
    if not os.path.exists(pdf_path):
        print(f"CRITICAL: PDF not found: {pdf_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(catalog_path, 'r') as f:
            catalog_content = f.read()
        catalog_lines = catalog_content.strip().split('\n')
    except Exception as e:
        print(f"CRITICAL: Cannot read catalog file: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get ground truth from PDF
    try:
        gt_images = get_pdf_image_metadata(pdf_path)
        gt_total = len(gt_images)
        gt_pages = len(set(img['page'] for img in gt_images))
    except Exception as e:
        print(f"CRITICAL: Cannot extract PDF metadata: {e}")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Ground truth — {gt_total} images across {gt_pages} pages")

    # Component 1: Total image count correct in summary (0.25 points)
    # Look for a summary line like "Total images: 13 ..."
    try:
        total_match = re.search(r'[Tt]otal\s+images[:\s]+(\d+)', catalog_content)
        if total_match:
            reported_total = int(total_match.group(1))
            if reported_total == gt_total:
                print(f"PASS: Component 1 — Total image count is {reported_total} (correct) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 — Total image count is {reported_total}, expected {gt_total}")
        else:
            print(f"FAIL: Component 1 — No 'Total images' summary line found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Page count in summary correct (0.15 points)
    # Look for "across N pages" in summary
    try:
        pages_match = re.search(r'across\s+(\d+)\s+pages', catalog_content)
        if pages_match:
            reported_pages = int(pages_match.group(1))
            if reported_pages == gt_pages:
                print(f"PASS: Component 2 — Page count is {reported_pages} (correct) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 — Page count is {reported_pages}, expected {gt_pages}")
        else:
            print(f"FAIL: Component 2 — No 'across N pages' summary found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Per-image entries with correct page numbers (0.35 points)
    # Expected format: "Page X, Image Y: WxH pixels, colorspace: CS, bpc: N"
    try:
        # Parse all "Page X, Image Y" entries from catalog
        entry_pattern = re.compile(
            r'[Pp]age\s+(\d+)[,\s]+[Ii]mage\s+(\d+)[:\s]+(\d+)\s*x\s*(\d+)\s*pixels?',
            re.IGNORECASE
        )
        entries = entry_pattern.findall(catalog_content)
        reported_entries = []
        for m in entries:
            reported_entries.append({
                'page': int(m[0]),
                'img_num': int(m[1]),
                'width': int(m[2]),
                'height': int(m[3]),
            })

        # Check: correct number of entries
        if len(reported_entries) == gt_total:
            # Check page numbers match ground truth
            gt_page_img_pairs = set((img['page'], img['img_num']) for img in gt_images)
            reported_pairs = set((e['page'], e['img_num']) for e in reported_entries)
            matching_pairs = gt_page_img_pairs & reported_pairs
            pair_ratio = len(matching_pairs) / len(gt_page_img_pairs) if gt_page_img_pairs else 0

            if pair_ratio >= 0.9:
                print(f"PASS: Component 3 — {len(reported_entries)} entries, {len(matching_pairs)}/{len(gt_page_img_pairs)} page/image pairs match (0.35 pts)")
                total_score += 0.35
            elif pair_ratio >= 0.5:
                partial = round(0.35 * pair_ratio, 2)
                print(f"PARTIAL: Component 3 — {len(matching_pairs)}/{len(gt_page_img_pairs)} pairs match ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — Only {len(matching_pairs)}/{len(gt_page_img_pairs)} pairs match")
        else:
            # Partial credit based on how many entries exist
            entry_ratio = min(len(reported_entries), gt_total) / gt_total if gt_total > 0 else 0
            if entry_ratio > 0:
                partial = round(0.35 * entry_ratio * 0.5, 2)  # half credit for wrong count
                print(f"PARTIAL: Component 3 — Found {len(reported_entries)} entries, expected {gt_total} ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — No per-image entries found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Image dimensions accuracy (0.25 points)
    # Check if reported dimensions match actual PDF image dimensions
    try:
        if not reported_entries:
            print(f"FAIL: Component 4 — No entries to check dimensions against")
        else:
            # Build lookup from ground truth
            gt_lookup = {}
            for img in gt_images:
                key = (img['page'], img['img_num'])
                gt_lookup[key] = (img['width'], img['height'])

            correct_dims = 0
            total_checked = 0
            for entry in reported_entries:
                key = (entry['page'], entry['img_num'])
                if key in gt_lookup:
                    total_checked += 1
                    gt_w, gt_h = gt_lookup[key]
                    if entry['width'] == gt_w and entry['height'] == gt_h:
                        correct_dims += 1

            if total_checked > 0:
                dim_ratio = correct_dims / gt_total
                if dim_ratio >= 0.9:
                    print(f"PASS: Component 4 — {correct_dims}/{gt_total} dimensions correct (0.25 pts)")
                    total_score += 0.25
                elif dim_ratio >= 0.5:
                    partial = round(0.25 * dim_ratio, 2)
                    print(f"PARTIAL: Component 4 — {correct_dims}/{gt_total} dimensions correct ({partial} pts)")
                    total_score += partial
                else:
                    print(f"FAIL: Component 4 — Only {correct_dims}/{gt_total} dimensions correct")
            else:
                print(f"FAIL: Component 4 — No matching page/image pairs for dimension check")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(CATALOG_PATH):
    print(f"File not found: {CATALOG_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(CATALOG_PATH, PDF_PATH)

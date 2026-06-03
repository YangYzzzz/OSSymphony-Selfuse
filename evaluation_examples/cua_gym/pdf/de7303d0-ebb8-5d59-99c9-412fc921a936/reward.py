"""
Reward Script: Batch process PDFs with 'PAID' stamp
Task ID: pdf_gf1_031
Domain: pdf
Scoring:
  - Component 1 (0.30): All 6 stamped files exist in invoices_paid/
  - Component 2 (0.30): Page counts match between originals and stamped files
  - Component 3 (0.25): Every page of every stamped file contains 'PAID' text
  - Component 4 (0.15): PAID text is red and rotated (~45 degrees diagonal)
"""

import os
import math
import pymupdf

WORKDIR = '/home/user'
INVOICES_DIR = os.path.join(WORKDIR, 'Documents', 'invoices')
PAID_DIR = os.path.join(WORKDIR, 'Documents', 'invoices_paid')

EXPECTED_FILES = [
    'invoice_001.pdf',
    'invoice_002.pdf',
    'invoice_003.pdf',
    'invoice_004.pdf',
    'invoice_005.pdf',
    'invoice_006.pdf',
]


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: invoices_paid directory must exist
    if not os.path.isdir(PAID_DIR):
        print(f"CRITICAL: Directory not found: {PAID_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: invoices directory must exist (for page count comparison)
    if not os.path.isdir(INVOICES_DIR):
        print(f"CRITICAL: Original invoices directory not found: {INVOICES_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: All 6 stamped files exist in invoices_paid/ (0.30 points)
    try:
        existing_files = os.listdir(PAID_DIR)
        files_found = sum(1 for f in EXPECTED_FILES if f in existing_files)
        if files_found == 6:
            print(f"PASS: Component 1 — All 6 stamped files present in invoices_paid/ (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — Only {files_found}/6 expected files found. Present: {sorted(existing_files)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # If no files found, stop early
    if files_found == 0:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Page counts match between originals and stamped files (0.30 points)
    try:
        matching_count = 0
        total_checked = 0
        for fname in EXPECTED_FILES:
            orig_path = os.path.join(INVOICES_DIR, fname)
            paid_path = os.path.join(PAID_DIR, fname)
            if not os.path.exists(paid_path):
                continue
            total_checked += 1
            orig_doc = pymupdf.open(orig_path)
            paid_doc = pymupdf.open(paid_path)
            if orig_doc.page_count == paid_doc.page_count:
                matching_count += 1
            else:
                print(f"  MISMATCH: {fname} orig={orig_doc.page_count} paid={paid_doc.page_count}")
            orig_doc.close()
            paid_doc.close()

        if total_checked > 0 and matching_count == total_checked:
            print(f"PASS: Component 2 — All {matching_count} files have matching page counts (0.30 pts)")
            total_score += 0.30
        elif total_checked > 0:
            # Partial credit proportional to matching files
            partial = 0.30 * (matching_count / total_checked)
            print(f"PARTIAL: Component 2 — {matching_count}/{total_checked} files match page counts ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No files to check page counts")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Every page of every stamped file contains 'PAID' text (0.25 points)
    try:
        total_pages = 0
        pages_with_paid = 0
        for fname in EXPECTED_FILES:
            paid_path = os.path.join(PAID_DIR, fname)
            if not os.path.exists(paid_path):
                continue
            doc = pymupdf.open(paid_path)
            for i in range(doc.page_count):
                total_pages += 1
                text = doc[i].get_text('text')
                if 'PAID' in text:
                    pages_with_paid += 1
                else:
                    print(f"  MISSING: {fname} page {i} does not contain 'PAID' text")
            doc.close()

        if total_pages > 0 and pages_with_paid == total_pages:
            print(f"PASS: Component 3 — All {total_pages} pages contain 'PAID' text (0.25 pts)")
            total_score += 0.25
        elif total_pages > 0:
            partial = 0.25 * (pages_with_paid / total_pages)
            print(f"PARTIAL: Component 3 — {pages_with_paid}/{total_pages} pages contain 'PAID' ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No pages to check")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: PAID text is red and rotated approximately 45 degrees (0.15 points)
    # Check that at least one page per file has red, rotated PAID text
    try:
        files_with_red_rotated = 0
        files_checked = 0
        for fname in EXPECTED_FILES:
            paid_path = os.path.join(PAID_DIR, fname)
            if not os.path.exists(paid_path):
                continue
            files_checked += 1
            doc = pymupdf.open(paid_path)
            found_red_rotated = False
            for i in range(doc.page_count):
                page = doc[i]
                data = page.get_text('dict')
                for block in data['blocks']:
                    if block.get('type') != 0:
                        continue
                    for line in block['lines']:
                        wdir = line.get('dir', (1.0, 0.0))
                        for span in line['spans']:
                            if 'PAID' in span['text']:
                                # Check color is red: high R, low G, low B
                                c = span['color']
                                r_val = (c >> 16) & 0xFF
                                g_val = (c >> 8) & 0xFF
                                b_val = c & 0xFF
                                is_red = r_val > 180 and g_val < 80 and b_val < 80

                                # Check rotation: dir vector should indicate ~45 degree angle
                                # dir = (cos(angle), -sin(angle)) for ~45 deg:
                                # cos(45) ~ 0.707, sin(45) ~ 0.707
                                # So dir ~ (0.707, -0.707) or similar non-(1,0) direction
                                dx, dy = wdir
                                is_rotated = abs(dx) < 0.95  # not purely horizontal

                                if is_red and is_rotated:
                                    found_red_rotated = True
                                    break
                        if found_red_rotated:
                            break
                    if found_red_rotated:
                        break
                if found_red_rotated:
                    break
            doc.close()
            if found_red_rotated:
                files_with_red_rotated += 1
            else:
                print(f"  ISSUE: {fname} — PAID text not red and/or not rotated")

        if files_checked > 0 and files_with_red_rotated == files_checked:
            print(f"PASS: Component 4 — All {files_checked} files have red, rotated PAID stamp (0.15 pts)")
            total_score += 0.15
        elif files_checked > 0:
            partial = 0.15 * (files_with_red_rotated / files_checked)
            print(f"PARTIAL: Component 4 — {files_with_red_rotated}/{files_checked} files have red rotated stamp ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No files to check")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

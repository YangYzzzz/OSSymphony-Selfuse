"""
Reward Script: Verify visa application form filling and flattening
Task ID: pdf_fm_036
Domain: pdf
Scoring:
  Component 1: Final PDF file exists (0.10)
  Component 2: Form is flattened - no interactive widgets (0.15)
  Component 3: Page count is 2 (0.05)
  Component 4: Field values verified via reference rendering comparison (0.70)
    - Fills the original form with expected values, renders both to pixmaps,
      compares pixel similarity to verify correct content
"""

import os
import pymupdf  # PyMuPDF

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_036'

# Paths
FINAL_PATH = os.path.join(WORKDIR, 'Documents', 'forms', 'visa_application_final.pdf')
INITIAL_FORM_PATH = os.path.join(WORKDIR, 'Documents', 'forms', 'visa_application.pdf')

# Expected field values from task instruction
EXPECTED_FIELDS = {
    'surname': 'NAKAMURA',
    'given_names': 'Yuki',
    'nationality': 'Japanese',
    'passport_no': 'TK4521876',
    'dob': '1990-03-22',
    'gender': 'Female',
    'purpose': 'Business',
    'arrival_date': '2025-10-01',
    'departure_date': '2025-10-15',
    'accommodation': 'Grand Hyatt Singapore',
    'declaration_agreed': 'Yes',
    'info_correct': 'Yes',
}


def create_reference_pixmaps():
    """
    Fill the original form with expected values and render pages as pixmaps.
    Returns list of pixmaps (one per page) or None on failure.
    """
    try:
        doc = pymupdf.open(INITIAL_FORM_PATH)
        for page in doc:
            for widget in page.widgets():
                name = widget.field_name
                if name in EXPECTED_FIELDS:
                    widget.field_value = EXPECTED_FIELDS[name]
                    widget.update()

        # Render each page as a pixmap
        pixmaps = []
        for pn in range(len(doc)):
            pix = doc[pn].get_pixmap(dpi=150)
            pixmaps.append(pix)

        doc.close()
        return pixmaps
    except Exception as e:
        print(f"WARN: Could not create reference pixmaps: {e}")
        return None


def compare_pixmaps(pix1, pix2):
    """
    Compare two pixmaps and return a similarity score (0.0 to 1.0).
    Uses mean absolute difference of pixel values.
    """
    try:
        if pix1.width != pix2.width or pix1.height != pix2.height:
            print(f"  Size mismatch: {pix1.width}x{pix1.height} vs {pix2.width}x{pix2.height}")
            return 0.0

        samples1 = pix1.samples
        samples2 = pix2.samples

        total_pixels = len(samples1)
        if total_pixels == 0:
            return 0.0

        # Count matching bytes
        matching = sum(1 for a, b in zip(samples1, samples2) if abs(a - b) < 20)
        similarity = matching / total_pixels
        return similarity
    except Exception as e:
        print(f"  Pixmap comparison error: {e}")
        return 0.0


def compare_with_blank_pixmaps(golden_pixmaps):
    """
    Compare golden pixmaps against blank (unfilled) form pixmaps.
    Returns the average difference — should be significant if form was filled.
    """
    try:
        doc = pymupdf.open(INITIAL_FORM_PATH)
        differences = []
        for pn in range(min(len(doc), len(golden_pixmaps))):
            blank_pix = doc[pn].get_pixmap(dpi=150)
            sim = compare_pixmaps(blank_pix, golden_pixmaps[pn])
            diff = 1.0 - sim
            differences.append(diff)
            print(f"  Page {pn}: blank-vs-golden difference = {diff:.4f}")
        doc.close()
        return sum(differences) / len(differences) if differences else 0.0
    except Exception as e:
        print(f"  Blank comparison error: {e}")
        return 0.0


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Final PDF file exists (0.10 points)
    try:
        if os.path.exists(FINAL_PATH):
            fsize = os.path.getsize(FINAL_PATH)
            if fsize > 1000:  # Must be non-trivial (>1KB)
                print(f"PASS: Component 1 — Final PDF exists at {FINAL_PATH} (size={fsize} bytes) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 1 — File exists but too small ({fsize} bytes)")
        else:
            print(f"FAIL: Component 1 — Final PDF not found at {FINAL_PATH}")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: Form is flattened — no interactive widgets (0.15 points)
    try:
        doc = pymupdf.open(FINAL_PATH)
        widget_count = 0
        for page in doc:
            widget_count += len(list(page.widgets()))
        doc.close()

        if widget_count == 0:
            print(f"PASS: Component 2 — Form is flattened (0 widgets found) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Form not fully flattened ({widget_count} widgets remain)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Correct page count (0.05 points)
    try:
        doc = pymupdf.open(FINAL_PATH)
        page_count = len(doc)
        doc.close()

        if page_count == 2:
            print(f"PASS: Component 3 — Page count is 2 (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 3 — Expected 2 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Field values verified via reference rendering comparison (0.70 points)
    # Strategy: Fill the original form programmatically with expected values,
    # render both reference and golden as pixmaps, compare similarity.
    # Also compare golden against blank form to ensure content was added.
    try:
        # Load golden pages as pixmaps
        golden_doc = pymupdf.open(FINAL_PATH)
        golden_pixmaps = []
        for pn in range(len(golden_doc)):
            golden_pixmaps.append(golden_doc[pn].get_pixmap(dpi=150))
        golden_doc.close()

        if not os.path.exists(INITIAL_FORM_PATH):
            print(f"FAIL: Component 4 — Original form not found at {INITIAL_FORM_PATH}")
        else:
            # Sub-check 4a: Golden differs from blank form (0.20 points)
            # Confirms that content was actually added to the form
            print("  Sub-check 4a: Verifying golden differs from blank form...")
            avg_diff = compare_with_blank_pixmaps(golden_pixmaps)
            if avg_diff > 0.001:
                print(f"  PASS: Sub-check 4a — Golden differs from blank (avg diff={avg_diff:.4f}) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"  FAIL: Sub-check 4a — Golden too similar to blank form (avg diff={avg_diff:.4f})")

            # Sub-check 4b: Golden matches reference filled form (0.50 points)
            # Fill the original form with expected values and compare rendered output
            print("  Sub-check 4b: Comparing golden with reference-filled form...")
            ref_pixmaps = create_reference_pixmaps()
            if ref_pixmaps is None:
                print("  FAIL: Sub-check 4b — Could not create reference pixmaps")
            else:
                page_scores = []
                for pn in range(min(len(golden_pixmaps), len(ref_pixmaps))):
                    sim = compare_pixmaps(golden_pixmaps[pn], ref_pixmaps[pn])
                    page_scores.append(sim)
                    print(f"  Page {pn}: golden-vs-reference similarity = {sim:.4f}")

                if page_scores:
                    avg_sim = sum(page_scores) / len(page_scores)
                    print(f"  Average similarity: {avg_sim:.4f}")

                    # Award points based on similarity
                    # The golden is rasterized (image) while reference is vector+widget render,
                    # so they won't be pixel-identical. But high similarity (>0.85) means
                    # correct values. Use graduated scoring.
                    if avg_sim >= 0.85:
                        print(f"  PASS: Sub-check 4b — High similarity ({avg_sim:.4f} >= 0.85) (0.50 pts)")
                        total_score += 0.50
                    elif avg_sim >= 0.75:
                        partial = 0.35
                        print(f"  PARTIAL: Sub-check 4b — Moderate similarity ({avg_sim:.4f} >= 0.75) ({partial} pts)")
                        total_score += partial
                    elif avg_sim >= 0.60:
                        partial = 0.20
                        print(f"  PARTIAL: Sub-check 4b — Low similarity ({avg_sim:.4f} >= 0.60) ({partial} pts)")
                        total_score += partial
                    else:
                        print(f"  FAIL: Sub-check 4b — Too dissimilar ({avg_sim:.4f} < 0.60)")
                else:
                    print("  FAIL: Sub-check 4b — No pages to compare")

    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

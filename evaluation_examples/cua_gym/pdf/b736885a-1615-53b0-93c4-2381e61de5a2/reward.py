"""
Reward Script: Reorder pages of a PDF
Task ID: pdf_gf1_015
Domain: pdf
Scoring:
  Component 1: Output file exists and is a valid PDF with exactly 5 pages (0.2 pts)
  Component 2-6: Each output page matches the expected input page by content (0.16 pts each, 0.8 total)
    - Output page 1 should match Input page 3 (Customer Acquisition Strategy)
    - Output page 2 should match Input page 1 (Q3 2025 Revenue Overview)
    - Output page 3 should match Input page 4 (Infrastructure and Security Updates)
    - Output page 4 should match Input page 2 (Product Development Milestones)
    - Output page 5 should match Input page 5 (Hiring and Team Growth)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf1_015'

INPUT_PATH = os.path.join(WORKDIR, 'Documents', 'shuffled_slides.pdf')
OUTPUT_PATH = os.path.join(WORKDIR, 'Documents', 'shuffled_slides_reordered.pdf')

# Expected mapping: output_page_index -> input_page_index (0-indexed)
# Task says: page 3, page 1, page 4, page 2, page 5 (1-indexed)
# So: output[0]=input[2], output[1]=input[0], output[2]=input[3], output[3]=input[1], output[4]=input[4]
EXPECTED_MAPPING = {
    0: 2,
    1: 0,
    2: 3,
    3: 1,
    4: 4,
}

# Distinctive heading text for each input page (used as content fingerprint)
INPUT_PAGE_SIGNATURES = {
    0: "Q3 2025 Revenue Overview",
    1: "Product Development Milestones",
    2: "Customer Acquisition Strategy",
    3: "Infrastructure and Security Updates",
    4: "Hiring and Team Growth",
}


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists, is valid PDF, has exactly 5 pages (0.2 pts)
    # This is a task-introduced change: the file does NOT exist in initial_env
    try:
        if not os.path.exists(OUTPUT_PATH):
            print(f"FAIL: Component 1 — Output file does not exist: {OUTPUT_PATH}")
            print("REWARD: 0.0")
            return 0.0

        doc = pymupdf.open(OUTPUT_PATH)
        page_count = doc.page_count

        if page_count != 5:
            print(f"FAIL: Component 1 — Expected 5 pages, found {page_count}")
            doc.close()
            print("REWARD: 0.0")
            return 0.0

        if page_count == 5:
            print(f"PASS: Component 1 — Output file exists and has 5 pages (0.2 pts)")
            total_score += 0.2
    except Exception as e:
        print(f"ERROR: Component 1 — Cannot load output PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Load input PDF for comparison
    try:
        input_doc = pymupdf.open(INPUT_PATH)
    except Exception as e:
        print(f"ERROR: Cannot load input PDF for comparison: {e}")
        # Still give points for file existence
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Components 2-6: Verify each output page matches expected input page (0.16 pts each)
    for out_idx in range(5):
        comp_num = out_idx + 2
        expected_input_idx = EXPECTED_MAPPING[out_idx]
        expected_signature = INPUT_PAGE_SIGNATURES[expected_input_idx]

        try:
            out_page = doc[out_idx]
            out_text = out_page.get_text("text").strip()

            # Check if the expected heading/signature text is present in the output page
            if expected_signature in out_text:
                # Additional verification: compare text content more thoroughly
                in_page = input_doc[expected_input_idx]
                in_text = in_page.get_text("text").strip()

                # Normalize whitespace for comparison
                import re
                out_norm = re.sub(r'\s+', ' ', out_text).strip()
                in_norm = re.sub(r'\s+', ' ', in_text).strip()

                if out_norm == in_norm:
                    print(f"PASS: Component {comp_num} — Output page {out_idx+1} matches input page {expected_input_idx+1} ('{expected_signature}') (0.16 pts)")
                    total_score += 0.16
                elif expected_signature in out_text:
                    # Partial: heading matches but full text differs slightly
                    print(f"PARTIAL: Component {comp_num} — Output page {out_idx+1} has correct heading '{expected_signature}' but text content differs slightly (0.08 pts)")
                    total_score += 0.08
            else:
                # Check what page this actually is
                actual_sig = "unknown"
                for sig_idx, sig_text in INPUT_PAGE_SIGNATURES.items():
                    if sig_text in out_text:
                        actual_sig = f"input page {sig_idx+1} ('{sig_text}')"
                        break
                print(f"FAIL: Component {comp_num} — Output page {out_idx+1} should be input page {expected_input_idx+1} ('{expected_signature}'), but found {actual_sig}")
        except Exception as e:
            print(f"ERROR: Component {comp_num} — {e}")

    doc.close()
    input_doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

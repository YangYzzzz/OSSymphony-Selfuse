"""
Reward Script: Add sequential figure labels below images in a PDF
Task ID: pdf_res_075
Domain: pdf
Scoring:
  - Component 1 (0.7 pts): Each of 6 figure labels ('Fig. 1' .. 'Fig. 6') found in document text (~0.117 each)
  - Component 2 (0.3 pts): Each label appears on the correct page (same page as its respective image)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_075'
OUTPUT_FILE = os.path.join(WORKDIR, 'papers', 'unlabeled_paper_labeled.pdf')

# The 6 expected figure labels
EXPECTED_LABELS = ['Fig. 1', 'Fig. 2', 'Fig. 3', 'Fig. 4', 'Fig. 5', 'Fig. 6']
# Pages (0-indexed) that have images in the PDF (one image per page, pages 1-6)
IMAGE_PAGES = [1, 2, 3, 4, 5, 6]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    import pymupdf

    total_score = 0.0

    # Precondition: load the PDF
    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract full text for label presence check
    full_text = ""
    page_texts = {}
    try:
        for i, page in enumerate(doc):
            pt = page.get_text("text")
            page_texts[i] = pt
            full_text += pt
    except Exception as e:
        print(f"ERROR: Failed to extract text: {e}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Figure labels present in document text (0.7 points total)
    # Each label found earns ~0.1167 points
    COMP1_WEIGHT = 0.7
    per_label_weight = COMP1_WEIGHT / len(EXPECTED_LABELS)
    labels_found = 0

    for label in EXPECTED_LABELS:
        try:
            if label in full_text:
                print(f"PASS: '{label}' found in document text ({per_label_weight:.4f} pts)")
                total_score += per_label_weight
                labels_found += 1
            else:
                # Also try regex for slight formatting variations (e.g., extra space)
                pattern = re.escape(label).replace(r'\.\ ', r'\.\s+')
                if re.search(pattern, full_text):
                    print(f"PASS: '{label}' found via regex in document text ({per_label_weight:.4f} pts)")
                    total_score += per_label_weight
                    labels_found += 1
                else:
                    print(f"FAIL: '{label}' not found in document text")
        except Exception as e:
            print(f"ERROR: Checking '{label}': {e}")

    print(f"Component 1 summary: {labels_found}/{len(EXPECTED_LABELS)} labels found")

    # Component 2: Labels on correct pages (0.3 points total)
    # Each label on the correct page earns 0.05 points
    COMP2_WEIGHT = 0.3
    per_page_weight = COMP2_WEIGHT / len(EXPECTED_LABELS)
    correct_pages = 0

    for idx, (label, expected_page) in enumerate(zip(EXPECTED_LABELS, IMAGE_PAGES)):
        try:
            page_text = page_texts.get(expected_page, "")
            if label in page_text:
                print(f"PASS: '{label}' on page {expected_page} (correct) ({per_page_weight:.4f} pts)")
                total_score += per_page_weight
                correct_pages += 1
            else:
                # Check with regex for slight variations
                pattern = re.escape(label).replace(r'\.\ ', r'\.\s+')
                if re.search(pattern, page_text):
                    print(f"PASS: '{label}' on page {expected_page} via regex ({per_page_weight:.4f} pts)")
                    total_score += per_page_weight
                    correct_pages += 1
                else:
                    print(f"FAIL: '{label}' not found on expected page {expected_page}")
        except Exception as e:
            print(f"ERROR: Checking '{label}' on page {expected_page}: {e}")

    print(f"Component 2 summary: {correct_pages}/{len(EXPECTED_LABELS)} labels on correct pages")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_FILE):
    print(f"File not found: {OUTPUT_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_FILE)

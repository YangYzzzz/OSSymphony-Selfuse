"""
Reward Script: Batch update metadata for 8 PDFs
Task ID: pdf_res_084
Domain: pdf
Scoring:
  Component 1 (0.15): batch_updated/ contains exactly 8 PDFs with correct filenames
  Component 2 (0.35): All 8 PDFs have author = 'Research Lab Alpha'
  Component 3 (0.35): All 8 PDFs have 'internal-review-2026' in keywords
  Component 4 (0.15): Page counts match original files (content integrity)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_084'

# Expected 8 PDF filenames and their original page counts
EXPECTED_FILES = {
    'autonomous_vehicles_safety.pdf': 1,
    'blockchain_scalability.pdf': 2,
    'climate_modeling_advances.pdf': 3,
    'medical_imaging_ai.pdf': 3,
    'neural_networks_survey.pdf': 2,
    'nlp_transformers_efficiency.pdf': 1,
    'quantum_computing_review.pdf': 1,
    'robotics_manipulation.pdf': 2,
}

BATCH_UPDATED_DIR = os.path.join(WORKDIR, 'papers', 'batch_updated')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: batch_updated/ directory exists and contains exactly 8 expected PDFs (0.15 pts)
    try:
        if not os.path.isdir(BATCH_UPDATED_DIR):
            print(f"FAIL: Component 1 -- directory {BATCH_UPDATED_DIR} does not exist")
        else:
            pdf_files = [f for f in os.listdir(BATCH_UPDATED_DIR) if f.endswith('.pdf')]
            missing = [f for f in EXPECTED_FILES if f not in pdf_files]
            if len(pdf_files) == 8 and len(missing) == 0:
                print(f"PASS: Component 1 -- batch_updated/ contains all 8 expected PDFs (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 -- found {len(pdf_files)} PDFs, missing: {missing}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Early exit if directory doesn't exist or has no files
    if total_score == 0.0:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Import fitz for PDF verification
    try:
        import fitz
    except ImportError:
        print("CRITICAL: PyMuPDF (fitz) not available")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: All 8 PDFs have author = 'Research Lab Alpha' (0.35 pts)
    try:
        author_pass_count = 0
        for fname in EXPECTED_FILES:
            fpath = os.path.join(BATCH_UPDATED_DIR, fname)
            if not os.path.isfile(fpath):
                print(f"  SKIP: {fname} not found for author check")
                continue
            doc = fitz.open(fpath)
            meta = doc.metadata
            doc.close()
            author = (meta.get('author') or '').strip()
            if author == 'Research Lab Alpha':
                author_pass_count += 1
            else:
                print(f"  FAIL: {fname} author = '{author}', expected 'Research Lab Alpha'")
        if author_pass_count == 8:
            print(f"PASS: Component 2 -- all 8 PDFs have author 'Research Lab Alpha' (0.35 pts)")
            total_score += 0.35
        elif author_pass_count > 0:
            partial = round(0.35 * (author_pass_count / 8), 4)
            if partial > 0:
                print(f"PARTIAL: Component 2 -- {author_pass_count}/8 PDFs have correct author (+{partial} pts)")
                total_score += partial
        else:
            print(f"FAIL: Component 2 -- 0/8 PDFs have correct author")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: All 8 PDFs have 'internal-review-2026' in keywords (0.35 pts)
    try:
        keyword_pass_count = 0
        for fname in EXPECTED_FILES:
            fpath = os.path.join(BATCH_UPDATED_DIR, fname)
            if not os.path.isfile(fpath):
                print(f"  SKIP: {fname} not found for keyword check")
                continue
            doc = fitz.open(fpath)
            meta = doc.metadata
            doc.close()
            keywords = (meta.get('keywords') or '').strip()
            if 'internal-review-2026' in keywords:
                keyword_pass_count += 1
            else:
                print(f"  FAIL: {fname} keywords = '{keywords}', missing 'internal-review-2026'")
        if keyword_pass_count == 8:
            print(f"PASS: Component 3 -- all 8 PDFs have 'internal-review-2026' in keywords (0.35 pts)")
            total_score += 0.35
        elif keyword_pass_count > 0:
            partial = round(0.35 * (keyword_pass_count / 8), 4)
            print(f"PARTIAL: Component 3 -- {keyword_pass_count}/8 PDFs have correct keyword (+{partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 -- 0/8 PDFs have 'internal-review-2026' in keywords")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Page counts match originals (content integrity) (0.15 pts)
    try:
        page_pass_count = 0
        for fname, expected_pages in EXPECTED_FILES.items():
            fpath = os.path.join(BATCH_UPDATED_DIR, fname)
            if not os.path.isfile(fpath):
                print(f"  SKIP: {fname} not found for page count check")
                continue
            doc = fitz.open(fpath)
            actual_pages = doc.page_count
            doc.close()
            if actual_pages == expected_pages:
                page_pass_count += 1
            else:
                print(f"  FAIL: {fname} has {actual_pages} pages, expected {expected_pages}")
        if page_pass_count == 8:
            print(f"PASS: Component 4 -- all 8 PDFs have correct page counts (0.15 pts)")
            total_score += 0.15
        elif page_pass_count > 0:
            partial = round(0.15 * (page_pass_count / 8), 4)
            print(f"PARTIAL: Component 4 -- {page_pass_count}/8 PDFs have correct page count (+{partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 -- 0/8 PDFs have correct page counts")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

"""
Reward Script: Merge PDFs by folder using ~/scripts/merge_by_folder.sh
Task ID: pdf_cross_094
Domain: pdf
Scoring:
  Component 1 (0.25): ~/scripts/merge_by_folder.sh exists and is executable
  Component 2 (0.25): ~/Documents/merged_output/ contains all 4 expected merged PDFs
  Component 3 (0.25): merged_alpha.pdf has >= 5 pages AND merged_beta.pdf has >= 4 pages
  Component 4 (0.25): merged_gamma.pdf has >= 6 pages AND merged_delta.pdf has >= 2 pages

Ground truth (from initial_env source PDFs):
  alpha/: 3 PDFs totaling 5 pages (report_q1: 2, report_q2: 1, report_q3: 2)
  beta/:  2 PDFs totaling 4 pages (budget_2024: 3, budget_2025: 1)
  gamma/: 4 PDFs totaling 6 pages (plan_a: 2, plan_b: 1, plan_c: 2, plan_d: 1)
  delta/: 1 PDF  totaling 2 pages (summary: 2)
"""

import os

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

SCRIPTS_DIR = '/home/user/scripts'
MERGE_SCRIPT = os.path.join(SCRIPTS_DIR, 'merge_by_folder.sh')
OUTPUT_DIR = '/home/user/Documents/merged_output'

EXPECTED_MERGED = {
    'merged_alpha.pdf': 5,   # 3 source PDFs -> at least 5 pages total
    'merged_beta.pdf':  4,   # 2 source PDFs -> at least 4 pages total
    'merged_gamma.pdf': 6,   # 4 source PDFs -> at least 6 pages total
    'merged_delta.pdf': 2,   # 1 source PDF  -> at least 2 pages total
}


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: ~/scripts/merge_by_folder.sh exists and is executable (0.25 points)
    # This FAILS on initial_env (no script exists) and PASSES on golden_env.
    try:
        script_exists = os.path.isfile(MERGE_SCRIPT)
        script_executable = script_exists and os.access(MERGE_SCRIPT, os.X_OK)
        if script_exists and script_executable:
            print(f"PASS: Component 1 — {MERGE_SCRIPT} exists and is executable (0.25 pts)")
            total_score += 0.25
        elif script_exists and not script_executable:
            print(f"FAIL: Component 1 — {MERGE_SCRIPT} exists but is NOT executable")
        else:
            print(f"FAIL: Component 1 — {MERGE_SCRIPT} does not exist")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: ~/Documents/merged_output/ contains all 4 expected merged PDFs (0.25 points)
    # This FAILS on initial_env (merged_output is empty) and PASSES on golden_env.
    try:
        all_files_present = all(
            os.path.isfile(os.path.join(OUTPUT_DIR, fname))
            for fname in EXPECTED_MERGED
        )
        if all_files_present:
            print(f"PASS: Component 2 — All 4 merged PDFs present in {OUTPUT_DIR} (0.25 pts)")
            total_score += 0.25
        else:
            missing = [
                fname for fname in EXPECTED_MERGED
                if not os.path.isfile(os.path.join(OUTPUT_DIR, fname))
            ]
            print(f"FAIL: Component 2 — Missing merged PDFs: {missing}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: merged_alpha.pdf >= 5 pages AND merged_beta.pdf >= 4 pages (0.25 points)
    # This FAILS on initial_env (files don't exist) and PASSES on golden_env.
    try:
        alpha_path = os.path.join(OUTPUT_DIR, 'merged_alpha.pdf')
        beta_path  = os.path.join(OUTPUT_DIR, 'merged_beta.pdf')

        alpha_ok = False
        beta_ok  = False

        if os.path.isfile(alpha_path):
            doc = pymupdf.open(alpha_path)
            alpha_pages = doc.page_count
            doc.close()
            alpha_ok = alpha_pages >= EXPECTED_MERGED['merged_alpha.pdf']
            print(f"  INFO: merged_alpha.pdf has {alpha_pages} pages (need >= {EXPECTED_MERGED['merged_alpha.pdf']})")
        else:
            print(f"  INFO: merged_alpha.pdf not found — cannot check page count")

        if os.path.isfile(beta_path):
            doc = pymupdf.open(beta_path)
            beta_pages = doc.page_count
            doc.close()
            beta_ok = beta_pages >= EXPECTED_MERGED['merged_beta.pdf']
            print(f"  INFO: merged_beta.pdf has {beta_pages} pages (need >= {EXPECTED_MERGED['merged_beta.pdf']})")
        else:
            print(f"  INFO: merged_beta.pdf not found — cannot check page count")

        if alpha_ok and beta_ok:
            print(f"PASS: Component 3 — merged_alpha.pdf and merged_beta.pdf have sufficient pages (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — alpha_ok={alpha_ok}, beta_ok={beta_ok}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: merged_gamma.pdf >= 6 pages AND merged_delta.pdf >= 2 pages (0.25 points)
    # This FAILS on initial_env (files don't exist) and PASSES on golden_env.
    try:
        gamma_path = os.path.join(OUTPUT_DIR, 'merged_gamma.pdf')
        delta_path = os.path.join(OUTPUT_DIR, 'merged_delta.pdf')

        gamma_ok = False
        delta_ok = False

        if os.path.isfile(gamma_path):
            doc = pymupdf.open(gamma_path)
            gamma_pages = doc.page_count
            doc.close()
            gamma_ok = gamma_pages >= EXPECTED_MERGED['merged_gamma.pdf']
            print(f"  INFO: merged_gamma.pdf has {gamma_pages} pages (need >= {EXPECTED_MERGED['merged_gamma.pdf']})")
        else:
            print(f"  INFO: merged_gamma.pdf not found — cannot check page count")

        if os.path.isfile(delta_path):
            doc = pymupdf.open(delta_path)
            delta_pages = doc.page_count
            doc.close()
            delta_ok = delta_pages >= EXPECTED_MERGED['merged_delta.pdf']
            print(f"  INFO: merged_delta.pdf has {delta_pages} pages (need >= {EXPECTED_MERGED['merged_delta.pdf']})")
        else:
            print(f"  INFO: merged_delta.pdf not found — cannot check page count")

        if gamma_ok and delta_ok:
            print(f"PASS: Component 4 — merged_gamma.pdf and merged_delta.pdf have sufficient pages (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — gamma_ok={gamma_ok}, delta_ok={delta_ok}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

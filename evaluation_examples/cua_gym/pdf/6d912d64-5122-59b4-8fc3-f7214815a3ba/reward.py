"""
Reward Script: Verify PDF/A compliance check and result file creation
Task ID: pdf_mbc_032
Domain: pdf
Scoring:
  - Component 1 (0.4): pdfa_check.txt exists at ~/Documents/pdfa_check.txt
  - Component 2 (0.3): File contains the text 'PDF/A-1b compliant' (exact match)
  - Component 3 (0.3): Content correctly reflects the actual PDF/A metadata in compliant.pdf
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_032'

CHECK_FILE = os.path.join(WORKDIR, 'Documents', 'pdfa_check.txt')
PDF_FILE = os.path.join(WORKDIR, 'Documents', 'compliant.pdf')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: pdfa_check.txt exists (0.4 points)
    # This file does NOT exist in initial_env, so it scores the task-introduced change
    try:
        if os.path.isfile(CHECK_FILE):
            print(f"PASS: Component 1 — pdfa_check.txt exists at {CHECK_FILE} (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — pdfa_check.txt not found at {CHECK_FILE}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: File contains 'PDF/A-1b compliant' (0.3 points)
    # The golden_env file should have exactly this text
    try:
        if os.path.isfile(CHECK_FILE):
            with open(CHECK_FILE, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            if content == 'PDF/A-1b compliant':
                print(f"PASS: Component 2 — File contains exact text 'PDF/A-1b compliant' (0.3 pts)")
                total_score += 0.3
            elif 'pdf/a-1b' in content.lower() and 'compliant' in content.lower():
                # Partial credit for close match with different casing
                print(f"PARTIAL: Component 2 — Content has PDF/A-1b and compliant but not exact match: '{content}' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 — Expected 'PDF/A-1b compliant', found: '{content}'")
        else:
            print(f"FAIL: Component 2 — Cannot check content, file does not exist")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Content correctly reflects the actual PDF/A metadata (0.3 points)
    # Verify the answer is consistent with the PDF's actual XMP metadata
    try:
        if os.path.isfile(CHECK_FILE) and os.path.isfile(PDF_FILE):
            with open(CHECK_FILE, 'r', encoding='utf-8') as f:
                check_content = f.read().strip()

            # Read actual PDF/A metadata from the PDF
            import pikepdf
            pdf = pikepdf.open(PDF_FILE)
            pdfa_part = None
            pdfa_conformance = None
            with pdf.open_metadata() as meta:
                for k, v in meta.items():
                    if 'pdfa' in k.lower() or 'pdfaid' in k.lower():
                        if 'part' in k.lower():
                            pdfa_part = str(v)
                        elif 'conformance' in k.lower():
                            pdfa_conformance = str(v)
            pdf.close()

            # The PDF should have pdfaid:part=1 and pdfaid:conformance=B
            # and the check file should say 'PDF/A-1b compliant'
            if pdfa_part and pdfa_conformance:
                expected_level = f"PDF/A-{pdfa_part}{pdfa_conformance.lower()}"
                if expected_level.lower() in check_content.lower():
                    print(f"PASS: Component 3 — Content '{check_content}' matches PDF metadata (part={pdfa_part}, conformance={pdfa_conformance}) (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 3 — Content '{check_content}' does not match PDF metadata level '{expected_level}'")
            else:
                # PDF has no PDF/A metadata; check file should say 'Not PDF/A compliant'
                if 'not' in check_content.lower() and 'compliant' in check_content.lower():
                    print(f"PASS: Component 3 — Correctly identified as not compliant (no PDF/A metadata) (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 3 — PDF has no PDF/A metadata but check file says: '{check_content}'")
        else:
            if not os.path.isfile(CHECK_FILE):
                print(f"FAIL: Component 3 — Cannot verify, pdfa_check.txt does not exist")
            elif not os.path.isfile(PDF_FILE):
                print(f"FAIL: Component 3 — Cannot verify, compliant.pdf does not exist")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

"""
Reward Script: PDF QA Pipeline Verification
Task ID: pdf_gf3_032
Domain: pdf
Scoring:
  Component 1 — Script exists at /home/user/scripts/qa_pipeline.py (0.15)
  Component 2 — incoming/ is empty (all 20 PDFs processed) (0.15)
  Component 3 — Correct PDFs in passed/ directory (0.25)
  Component 4 — Correct PDFs in failed/ directory (0.20)
  Component 5 — QA report .txt files exist for each failed PDF (0.15)
  Component 6 — QA reports contain meaningful failure descriptions (0.10)
"""

import os

WORKDIR = '/home/user'

# Expected file distribution based on QA rules:
# Rules: min_pages=3, required_bookmarks=['Chapter 1'], max_size_mb=10,
#         required_metadata=['Title','Author'], no_javascript=true
EXPECTED_PASSED = sorted([
    'annual_report_2024.pdf',
    'compliance_audit_2024.pdf',
    'data_governance_policy.pdf',
    'employee_handbook_v3.pdf',
    'project_charter_phoenix.pdf',
    'quarterly_review_q4.pdf',
    'safety_guidelines_2025.pdf',
    'strategic_plan_2025.pdf',
    'training_materials_q1.pdf',
    'vendor_agreement_template.pdf',
])

EXPECTED_FAILED = sorted([
    'cover_letter_draft.pdf',
    'design_spec_aurora.pdf',
    'draft_proposal_unsigned.pdf',
    'interactive_form_legacy.pdf',
    'meeting_notes_march.pdf',
    'one_pager_summary.pdf',
    'quick_memo_parking.pdf',
    'technical_bulletin_007.pdf',
    'temp_report_unreviewed.pdf',
    'unlabeled_scan_batch3.pdf',
])


def verify_task():
    """
    Verify QA pipeline task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Script exists at /home/user/scripts/qa_pipeline.py (0.15 points)
    try:
        script_path = os.path.join(WORKDIR, 'scripts', 'qa_pipeline.py')
        if os.path.isfile(script_path):
            size = os.path.getsize(script_path)
            if size > 100:  # Must be a real script, not just a stub
                print(f"PASS: Component 1 — qa_pipeline.py exists ({size} bytes) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — qa_pipeline.py too small ({size} bytes), likely stub")
        else:
            print(f"FAIL: Component 1 — qa_pipeline.py not found at {script_path}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: incoming/ is empty — all 20 PDFs processed (0.15 points)
    try:
        incoming_dir = os.path.join(WORKDIR, 'qa', 'incoming')
        if os.path.isdir(incoming_dir):
            remaining = [f for f in os.listdir(incoming_dir) if f.endswith('.pdf')]
            if len(remaining) == 0:
                print(f"PASS: Component 2 — incoming/ is empty, all PDFs processed (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 — {len(remaining)} PDFs still in incoming/")
        else:
            print(f"FAIL: Component 2 — incoming/ directory not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Correct PDFs in passed/ directory (0.25 points)
    try:
        passed_dir = os.path.join(WORKDIR, 'qa', 'passed')
        if os.path.isdir(passed_dir):
            actual_passed = sorted([f for f in os.listdir(passed_dir) if f.endswith('.pdf')])
            if actual_passed == EXPECTED_PASSED:
                print(f"PASS: Component 3 — All 10 correct PDFs in passed/ (0.25 pts)")
                total_score += 0.25
            else:
                # Partial credit: proportional to correctly placed files
                correct = len(set(actual_passed) & set(EXPECTED_PASSED))
                wrong = len(set(actual_passed) - set(EXPECTED_PASSED))
                missing = len(set(EXPECTED_PASSED) - set(actual_passed))
                partial = 0.25 * (correct / 10) * (1 - wrong / max(len(actual_passed), 1))
                partial = max(0, partial)
                if partial > 0:
                    print(f"PARTIAL: Component 3 — {correct}/10 correct, {wrong} wrong, {missing} missing in passed/ ({partial:.3f} pts)")
                    total_score += partial
                else:
                    print(f"FAIL: Component 3 — passed/ has {len(actual_passed)} PDFs; expected 10 specific files")
                    print(f"  Expected: {EXPECTED_PASSED}")
                    print(f"  Actual:   {actual_passed}")
        else:
            print(f"FAIL: Component 3 — passed/ directory not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Correct PDFs in failed/ directory (0.20 points)
    try:
        failed_dir = os.path.join(WORKDIR, 'qa', 'failed')
        if os.path.isdir(failed_dir):
            actual_failed = sorted([f for f in os.listdir(failed_dir) if f.endswith('.pdf')])
            if actual_failed == EXPECTED_FAILED:
                print(f"PASS: Component 4 — All 10 correct PDFs in failed/ (0.20 pts)")
                total_score += 0.20
            else:
                correct = len(set(actual_failed) & set(EXPECTED_FAILED))
                wrong = len(set(actual_failed) - set(EXPECTED_FAILED))
                partial = 0.20 * (correct / 10) * (1 - wrong / max(len(actual_failed), 1))
                partial = max(0, partial)
                if partial > 0:
                    print(f"PARTIAL: Component 4 — {correct}/10 correct in failed/ ({partial:.3f} pts)")
                    total_score += partial
                else:
                    print(f"FAIL: Component 4 — failed/ has wrong PDFs")
        else:
            print(f"FAIL: Component 4 — failed/ directory not found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: QA report .txt files exist for each failed PDF (0.15 points)
    try:
        failed_dir = os.path.join(WORKDIR, 'qa', 'failed')
        if os.path.isdir(failed_dir):
            actual_failed_pdfs = [f for f in os.listdir(failed_dir) if f.endswith('.pdf')]
            reports_found = 0
            for pdf_name in actual_failed_pdfs:
                base = pdf_name.replace('.pdf', '')
                report_name = f"{base}_qa_report.txt"
                report_path = os.path.join(failed_dir, report_name)
                if os.path.isfile(report_path) and os.path.getsize(report_path) > 10:
                    reports_found += 1

            if len(actual_failed_pdfs) > 0:
                ratio = reports_found / len(actual_failed_pdfs)
                points = 0.15 * ratio
                if ratio == 1.0:
                    print(f"PASS: Component 5 — All {reports_found} QA reports found for failed PDFs (0.15 pts)")
                    total_score += points
                elif ratio > 0:
                    print(f"PARTIAL: Component 5 — {reports_found}/{len(actual_failed_pdfs)} QA reports found ({points:.3f} pts)")
                    total_score += points
                else:
                    print(f"FAIL: Component 5 — No QA reports found for failed PDFs")
            else:
                print(f"FAIL: Component 5 — No failed PDFs found, cannot check reports")
        else:
            print(f"FAIL: Component 5 — failed/ directory not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: QA reports contain meaningful failure descriptions (0.10 points)
    # Check that reports mention specific failure reasons, not just generic text
    try:
        failed_dir = os.path.join(WORKDIR, 'qa', 'failed')
        if os.path.isdir(failed_dir):
            reports = [f for f in os.listdir(failed_dir) if f.endswith('_qa_report.txt')]
            meaningful_count = 0
            # Keywords that indicate real QA validation was done
            failure_keywords = [
                'page', 'bookmark', 'metadata', 'javascript', 'size',
                'fail', 'missing', 'below', 'minimum', 'required',
                'title', 'author', 'chapter',
            ]
            for report_name in reports:
                report_path = os.path.join(failed_dir, report_name)
                try:
                    with open(report_path, 'r') as f:
                        content = f.read().lower()
                    # A meaningful report should mention at least one failure keyword
                    if any(kw in content for kw in failure_keywords):
                        meaningful_count += 1
                except Exception:
                    pass

            if len(reports) > 0:
                ratio = meaningful_count / len(reports)
                points = 0.10 * ratio
                if ratio == 1.0:
                    print(f"PASS: Component 6 — All {meaningful_count} QA reports have meaningful content (0.10 pts)")
                    total_score += points
                elif ratio > 0:
                    print(f"PARTIAL: Component 6 — {meaningful_count}/{len(reports)} reports meaningful ({points:.3f} pts)")
                    total_score += points
                else:
                    print(f"FAIL: Component 6 — No QA reports have meaningful content")
            else:
                print(f"FAIL: Component 6 — No QA reports to check")
        else:
            print(f"FAIL: Component 6 — failed/ directory not found")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

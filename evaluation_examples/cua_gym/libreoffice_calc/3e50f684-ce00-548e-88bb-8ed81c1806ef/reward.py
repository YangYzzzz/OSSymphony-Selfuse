"""
Reward Script: PDF Visual Regression Testing Framework
Task ID: pdf_gf3_049
Domain: libreoffice_calc (actually PDF/Python scripting)
Scoring:
  C1: Script exists and is non-trivial (0.10)
  C2: Script uses correct DPI rendering (fitz.Matrix 1.5) (0.15)
  C3: Script uses correct pixel diff formula (numpy abs/mean/255) (0.10)
  C4: Script runs and flags exactly 3 pages (0.20)
  C5: Diff images generated for flagged pages (0.15)
  C6: regression_report.html exists with valid HTML structure (0.10)
  C7: Report contains correct summary stats (10 total, 7 passed, 3 failed) (0.10)
  C8: Report shows side-by-side images for flagged pages (0.10)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_049'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    script_path = f'{WORKDIR}/scripts/pdf_regression.py'
    report_path = f'{WORKDIR}/test/regression_report.html'
    diffs_dir = f'{WORKDIR}/test/diffs'

    # === Component 1: Script exists and is non-trivial (0.10 points) ===
    try:
        if os.path.exists(script_path):
            with open(script_path, 'r') as f:
                script_content = f.read()
            # Must be a real script, not a stub — at least 500 chars with key imports
            if len(script_content) >= 500 and ('import' in script_content) and ('def ' in script_content):
                print(f"PASS: Component 1 — Script exists ({len(script_content)} chars, has imports and functions) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 1 — Script too short or missing structure (len={len(script_content)})")
        else:
            print(f"FAIL: Component 1 — Script not found at {script_path}")
            # Without the script, nothing else can pass
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # === Component 2: Script uses correct DPI rendering with fitz.Matrix(1.5, 1.5) (0.15 points) ===
    try:
        # Check that the script references fitz/pymupdf and uses Matrix(1.5, 1.5) for 150 DPI
        has_fitz = ('fitz' in script_content or 'pymupdf' in script_content)
        has_matrix = bool(re.search(r'Matrix\s*\(\s*1\.5\s*,\s*1\.5\s*\)', script_content))
        # Also accept DPI=150 with a scale factor computation
        has_dpi_ref = ('150' in script_content)

        if has_fitz and has_matrix:
            print(f"PASS: Component 2 — Uses fitz/pymupdf with Matrix(1.5, 1.5) for 150 DPI (0.15 pts)")
            total_score += 0.15
        elif has_fitz and has_dpi_ref:
            print(f"PARTIAL: Component 2 — Uses fitz with DPI reference but Matrix pattern not found (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 2 — Missing fitz/pymupdf or Matrix(1.5, 1.5) rendering")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # === Component 3: Script uses correct pixel diff formula (numpy abs/mean/255) (0.10 points) ===
    try:
        has_numpy = ('numpy' in script_content or 'np.' in script_content)
        # Check for the pixel diff formula pattern: abs(...).mean() / 255
        has_abs = ('abs(' in script_content or 'np.abs(' in script_content)
        has_mean_255 = bool(re.search(r'\.mean\(\).*(/\s*255|/\s*255\.)', script_content))

        if has_numpy and has_abs and has_mean_255:
            print(f"PASS: Component 3 — Uses numpy abs/mean/255 pixel diff formula (0.10 pts)")
            total_score += 0.10
        elif has_numpy and has_abs:
            print(f"PARTIAL: Component 3 — Has numpy and abs but mean/255 pattern not clear (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 3 — Missing correct pixel diff formula (numpy={has_numpy}, abs={has_abs})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # === Component 4: Script runs and flags exactly 3 pages (0.20 points) ===
    try:
        # Run the script and check output
        import io
        import sys
        from contextlib import redirect_stdout, redirect_stderr

        # Save original state
        orig_argv = sys.argv[:]
        sys.argv = [script_path]

        captured_out = io.StringIO()
        captured_err = io.StringIO()
        execution_result = "pending"
        flagged_count = 0

        try:
            # Execute the script in a controlled way
            exec_globals = {'__name__': '__main__', '__file__': script_path}
            with redirect_stdout(captured_out), redirect_stderr(captured_err):
                try:
                    exec(compile(open(script_path).read(), script_path, 'exec'), exec_globals)
                except SystemExit:
                    pass  # Script calls sys.exit(), that's fine
            execution_result = "success"
        except Exception as run_err:
            execution_result = "failed"
            print(f"FAIL: Component 4 — Script execution error: {run_err}")
        finally:
            sys.argv = orig_argv

        if execution_result == "success":
            output = captured_out.getvalue()
            # Count FAIL lines in output (each flagged page prints [FAIL])
            fail_lines = re.findall(r'\bFAIL\b', output)
            flagged_count = len(fail_lines)

            # Also try to parse "X failed" from output
            failed_match = re.search(r'(\d+)\s+failed', output)
            if failed_match:
                flagged_count = int(failed_match.group(1))

            if flagged_count == 3:
                print(f"PASS: Component 4 — Script runs and flags exactly 3 pages (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 — Expected 3 flagged pages, got {flagged_count}")
                # Partial credit if it runs but count is wrong
                if flagged_count > 0:
                    total_score += 0.05
                    print(f"  (partial credit: 0.05 pts for running)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # === Component 5: Diff images generated for flagged pages (0.15 points) ===
    try:
        expected_diffs = []
        # Pages 3, 6, 9 are the flagged pages per the golden state
        # But we check generically: any 3 pages with diff images
        if os.path.isdir(diffs_dir):
            diff_files = os.listdir(diffs_dir)
            # Look for page_X_diff.png pattern
            diff_images = [f for f in diff_files if re.match(r'page_\d+_diff\.png', f)]

            if len(diff_images) >= 3:
                # Verify they are actual image files (not empty)
                non_empty = 0
                for img_name in diff_images:
                    img_path = os.path.join(diffs_dir, img_name)
                    if os.path.getsize(img_path) > 100:
                        non_empty += 1

                if non_empty >= 3:
                    print(f"PASS: Component 5 — {non_empty} non-empty diff images found (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 5 — Diff images exist but {non_empty} are non-empty (need >= 3)")
            else:
                print(f"FAIL: Component 5 — Only {len(diff_images)} diff images found (need >= 3)")
        else:
            print(f"FAIL: Component 5 — Diffs directory not found at {diffs_dir}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # === Component 6: regression_report.html exists with valid HTML structure (0.10 points) ===
    try:
        if os.path.exists(report_path):
            with open(report_path, 'r') as f:
                report_content = f.read()

            if len(report_content) < 100:
                print(f"FAIL: Component 6 — Report exists but too short ({len(report_content)} chars)")
            elif '<html' in report_content.lower() and '</html>' in report_content.lower():
                print(f"PASS: Component 6 — Valid HTML report exists ({len(report_content)} chars) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 6 — Report exists but missing <html> structure")
        else:
            print(f"FAIL: Component 6 — Report not found at {report_path}")
            report_content = ""
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")
        report_content = ""

    # === Component 7: Report contains correct summary stats (0.10 points) ===
    try:
        if report_content:
            # Check for total pages = 10, passed = 7, failed = 3
            has_total_10 = bool(re.search(r'10.*[Tt]otal|[Tt]otal.*10', report_content))
            has_passed_7 = bool(re.search(r'7.*[Pp]assed|[Pp]assed.*7', report_content))
            has_failed_3 = bool(re.search(r'3.*[Ff]ailed|[Ff]ailed.*3', report_content))

            # Also check for just the numbers in stat boxes
            if not has_total_10:
                has_total_10 = '>10<' in report_content
            if not has_passed_7:
                has_passed_7 = '>7<' in report_content
            if not has_failed_3:
                has_failed_3 = '>3<' in report_content

            if has_total_10 and has_passed_7 and has_failed_3:
                print(f"PASS: Component 7 — Report shows 10 total, 7 passed, 3 failed (0.10 pts)")
                total_score += 0.10
            else:
                count = sum([has_total_10, has_passed_7, has_failed_3])
                partial = round(count * 0.033, 3)
                print(f"FAIL: Component 7 — Summary stats incomplete (total_10={has_total_10}, passed_7={has_passed_7}, failed_3={has_failed_3})")
                if partial > 0:
                    total_score += partial
                    print(f"  (partial credit: {partial} pts)")
        else:
            print(f"FAIL: Component 7 — No report content to check")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    # === Component 8: Report shows side-by-side images for flagged pages (0.10 points) ===
    try:
        if report_content:
            # Check that the report references diff images for flagged pages
            img_refs = re.findall(r'<img\s+[^>]*src="[^"]*diff[^"]*"', report_content)
            golden_refs = re.findall(r'<img\s+[^>]*src="[^"]*golden[^"]*"', report_content)
            candidate_refs = re.findall(r'<img\s+[^>]*src="[^"]*candidate[^"]*"', report_content)

            # Each flagged page should have 3 images: golden, candidate, diff
            has_diff_imgs = len(img_refs) >= 3
            has_golden_imgs = len(golden_refs) >= 3
            has_candidate_imgs = len(candidate_refs) >= 3

            if has_diff_imgs and has_golden_imgs and has_candidate_imgs:
                print(f"PASS: Component 8 — Report has side-by-side images (golden={len(golden_refs)}, candidate={len(candidate_refs)}, diff={len(img_refs)}) (0.10 pts)")
                total_score += 0.10
            elif has_diff_imgs:
                print(f"PARTIAL: Component 8 — Has diff images but missing golden/candidate refs (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 8 — Report missing image references for flagged pages")
        else:
            print(f"FAIL: Component 8 — No report content to check")
    except Exception as e:
        print(f"ERROR: Component 8 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

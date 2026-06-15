"""
Reward Script: Batch convert .ppt and .pptx files to PDF on Desktop
Task ID: osworld_multi_apps_batch_convert_015
Domain: os (multi-apps)
Scoring:
  Component 1: All .ppt files have corresponding valid PDFs (0.5 pts)
  Component 2: All .pptx files have corresponding valid PDFs (0.5 pts)
  Total: 1.0
"""

import os

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_batch_convert_015'


def is_valid_pdf(path: str) -> bool:
    """Check that a file exists, is non-empty, and starts with the PDF magic header."""
    try:
        if not os.path.isfile(path):
            return False
        if os.path.getsize(path) == 0:
            return False
        with open(path, 'rb') as f:
            header = f.read(4)
        return header == b'%PDF'
    except Exception:
        return False


def verify_task(desktop_dir: str) -> float:
    """
    Verify task completion: every .ppt and .pptx file on the Desktop has a
    corresponding valid PDF produced by batch conversion commands.
    Returns a float between 0.0 and 1.0.
    """
    total_score = 0.0

    # Discover source files
    try:
        all_files = os.listdir(desktop_dir)
    except Exception as e:
        print(f"CRITICAL: Cannot list Desktop directory {desktop_dir}: {e}")
        print("REWARD: 0.0")
        return 0.0

    ppt_files = sorted([f for f in all_files if f.endswith('.ppt') and not f.endswith('.pptx')])
    pptx_files = sorted([f for f in all_files if f.endswith('.pptx')])

    print(f"Found .ppt files:  {ppt_files}")
    print(f"Found .pptx files: {pptx_files}")

    # Precondition gate: there must be at least one source file to evaluate
    if not ppt_files and not pptx_files:
        print("FAIL: No .ppt or .pptx files found on Desktop — cannot evaluate.")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: All .ppt files have a corresponding valid PDF (0.5 points)
    # Partial credit: each .ppt file conversion earns equal fraction within 0.5 pts.
    # This FAILS on initial_env (no PDFs) and PASSES on golden_env (all PDFs present).
    try:
        if not ppt_files:
            # No .ppt files: vacuous pass for this component
            print("SKIP: No .ppt files present, skipping Component 1.")
            total_score += 0.5
        else:
            ppt_passed = 0
            for ppt in ppt_files:
                base = os.path.splitext(ppt)[0]
                expected_pdf = os.path.join(desktop_dir, base + '.pdf')
                if is_valid_pdf(expected_pdf):
                    print(f"PASS: {ppt} -> {base}.pdf exists and is valid")
                    ppt_passed += 1
                else:
                    print(f"FAIL: {ppt} -> {base}.pdf missing or invalid")

            # Award partial credit proportionally
            if ppt_passed > 0:
                component1_score = 0.5 * ppt_passed / len(ppt_files)
                print(f"Component 1: {ppt_passed}/{len(ppt_files)} .ppt conversions succeeded ({component1_score:.4f}/0.5 pts)")
                total_score += component1_score
            else:
                print(f"Component 1: 0/{len(ppt_files)} .ppt conversions succeeded (0.0/0.5 pts)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All .pptx files have a corresponding valid PDF (0.5 points)
    # Partial credit: each .pptx file conversion earns equal fraction within 0.5 pts.
    # This FAILS on initial_env (no PDFs) and PASSES on golden_env (all PDFs present).
    try:
        if not pptx_files:
            # No .pptx files: vacuous pass for this component
            print("SKIP: No .pptx files present, skipping Component 2.")
            total_score += 0.5
        else:
            pptx_passed = 0
            for pptx in pptx_files:
                base = os.path.splitext(pptx)[0]
                expected_pdf = os.path.join(desktop_dir, base + '.pdf')
                if is_valid_pdf(expected_pdf):
                    print(f"PASS: {pptx} -> {base}.pdf exists and is valid")
                    pptx_passed += 1
                else:
                    print(f"FAIL: {pptx} -> {base}.pdf missing or invalid")

            # Award partial credit proportionally
            if pptx_passed > 0:
                component2_score = 0.5 * pptx_passed / len(pptx_files)
                print(f"Component 2: {pptx_passed}/{len(pptx_files)} .pptx conversions succeeded ({component2_score:.4f}/0.5 pts)")
                total_score += component2_score
            else:
                print(f"Component 2: 0/{len(pptx_files)} .pptx conversions succeeded (0.0/0.5 pts)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: verify the Desktop directory
if not os.path.isdir(WORKDIR):
    print(f"Desktop directory not found: {WORKDIR}")
    print("REWARD: 0.0")
else:
    verify_task(WORKDIR)

"""
Reward Script: Fix IEEE citation format in research_paper.docx references section
Task ID: osworld_multi_apps_misc_042
Domain: libreoffice_writer (docx)
Scoring:
  Component 1 (0.40): All references use [N] bracket numbering format
  Component 2 (0.20): Book reference includes publisher info
  Component 3 (0.20): References contain proper comma-separated vol/no/pp metadata
  Component 4 (0.20): References use expanded IEEE venue names ("in Proc. IEEE/CVF")
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_misc_042'
FILE_PATH = '/home/user/Desktop/submissions/research_paper.docx'


def verify_task(file_path):
    """
    Verify that references section in research_paper.docx is corrected
    to IEEE citation format.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load document
    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract all paragraphs
    paragraphs = [p.text for p in doc.paragraphs]

    # Find references section start
    ref_start = None
    for i, text in enumerate(paragraphs):
        if text.strip() == 'References':
            ref_start = i
            break

    if ref_start is None:
        print("FAIL: Could not find 'References' section heading in document")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Extract reference paragraphs (all after the heading)
    ref_paragraphs = [p.strip() for p in paragraphs[ref_start + 1:] if p.strip()]
    print(f"INFO: Found {len(ref_paragraphs)} reference entries starting at paragraph {ref_start + 1}")

    # -----------------------------------------------------------------------
    # Component 1: All references use [N] bracket numbering (0.40 points)
    # In the initial file, references use "1." style (period, no brackets).
    # The corrected IEEE format requires "[1]" style (square brackets).
    # We check that ALL references start with [N] format and NONE start with "N."
    # -----------------------------------------------------------------------
    try:
        bracket_pattern = re.compile(r'^\[\d+\]')
        period_pattern = re.compile(r'^\d+\.')

        bracket_count = sum(1 for p in ref_paragraphs if bracket_pattern.match(p))
        period_count = sum(1 for p in ref_paragraphs if period_pattern.match(p))

        print(f"INFO Component 1: bracket-format refs={bracket_count}, period-format refs={period_count}, total refs={len(ref_paragraphs)}")

        if len(ref_paragraphs) >= 10 and bracket_count == len(ref_paragraphs) and period_count == 0:
            print(f"PASS: Component 1 — All {bracket_count} references use [N] IEEE bracket format (0.40 pts)")
            total_score += 0.40
        elif bracket_count > 0 and bracket_count > period_count:
            # Partial: some converted but not all
            print(f"PARTIAL: Component 1 — {bracket_count}/{len(ref_paragraphs)} refs use bracket format, {period_count} still use period format")
        else:
            print(f"FAIL: Component 1 — Expected [N] bracket format for all references, found {period_count} period-format and {bracket_count} bracket-format")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: Book reference includes publisher info (0.20 points)
    # Initial ref [2]: "Probabilistic Robotics, 2005." (missing publisher)
    # Golden ref [2]: "Probabilistic Robotics. Cambridge, MA: MIT Press, 2005."
    # We check that the Probabilistic Robotics entry contains publisher info.
    # -----------------------------------------------------------------------
    try:
        prob_robotics_ref = None
        for p in ref_paragraphs:
            if 'Probabilistic Robotics' in p:
                prob_robotics_ref = p
                break

        if prob_robotics_ref is None:
            print("FAIL: Component 2 — Could not find 'Probabilistic Robotics' reference entry")
        elif 'MIT Press' in prob_robotics_ref or 'Cambridge' in prob_robotics_ref:
            print(f"PASS: Component 2 — Probabilistic Robotics entry includes publisher info (MIT Press/Cambridge) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — Probabilistic Robotics entry missing publisher info. Found: {repr(prob_robotics_ref[:100])}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: References contain proper comma-separated vol/no/pp metadata (0.20 points)
    # Initial ref [1]: "vol. 3 no. 2 pp. 98-107" (missing commas)
    # Golden ref [1]: "vol. 3, no. 2, pp. 98-107" (proper comma separation)
    # We check the first reference (Fridman) contains commas in vol/no/pp fields.
    # -----------------------------------------------------------------------
    try:
        fridman_ref = None
        for p in ref_paragraphs:
            if 'Fridman' in p:
                fridman_ref = p
                break

        if fridman_ref is None:
            print("FAIL: Component 3 — Could not find Fridman reference entry")
        else:
            # Check for proper comma-separated vol/no/pp pattern
            # Pattern: "vol. X, no. Y, pp." with commas
            comma_pattern = re.search(r'vol\.\s*\d+,\s*no\.\s*\d+,\s*pp\.', fridman_ref)
            # Also check that entry [8] (YOLOv8) uses "[Online]." with period (not just "[Online]")
            yolov8_ref = None
            for p in ref_paragraphs:
                if 'YOLOv8' in p or 'Ultralytics' in p.lower():
                    yolov8_ref = p
                    break

            yolov8_ok = yolov8_ref and '[Online].' in yolov8_ref

            if comma_pattern and yolov8_ok:
                print(f"PASS: Component 3 — References use proper comma-separated vol/no/pp metadata and [Online]. format (0.20 pts)")
                total_score += 0.20
            elif comma_pattern:
                print(f"PASS: Component 3 — Fridman ref has proper comma-separated vol/no/pp (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — Fridman reference missing commas in vol/no/pp. Found: {repr(fridman_ref[:150])}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -----------------------------------------------------------------------
    # Component 4: References use expanded IEEE venue names (0.20 points)
    # Initial refs use short venue names: "CVPR 2022", "ECCV 2022", "ICCV 2019"
    # Golden refs use expanded: "in Proc. IEEE/CVF Conf. on Computer Vision and Pattern Recognition (CVPR)"
    # We check that at least 5 references contain "IEEE/CVF" (expanded venue name).
    # -----------------------------------------------------------------------
    try:
        ieee_cvf_count = sum(1 for p in ref_paragraphs if 'IEEE/CVF' in p)
        # Also check for "in Proc." pattern which is the standard IEEE lead-in
        in_proc_count = sum(1 for p in ref_paragraphs if re.search(r'in Proc\.', p))

        print(f"INFO Component 4: refs with 'IEEE/CVF'={ieee_cvf_count}, refs with 'in Proc.'={in_proc_count}")

        if ieee_cvf_count >= 5:
            print(f"PASS: Component 4 — {ieee_cvf_count} references use expanded IEEE/CVF venue names (0.20 pts)")
            total_score += 0.20
        elif ieee_cvf_count >= 3:
            print(f"PARTIAL: Component 4 — Only {ieee_cvf_count} refs have IEEE/CVF venue names (need >= 5)")
        else:
            print(f"FAIL: Component 4 — Too few references use expanded IEEE venue names (found {ieee_cvf_count}, expected >= 5)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

"""
Reward Script: Copy Fade transition (1.5s) from slide 2 to slides 4 and 6
Task ID: impress_tm_040
Domain: libreoffice_impress
Scoring:
  - Component 1 (0.35): Slide 4 has Fade transition with 1500ms duration
  - Component 2 (0.35): Slide 6 has Fade transition with 1500ms duration
  - Component 3 (0.30): Other slides (1,3,5,7,8) retain original transitions unchanged
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_tm_040'

# Expected transitions for slides that should NOT change (0-indexed)
# These are the initial-state transitions that must be preserved
EXPECTED_UNCHANGED = {
    0: {'type': 'push', 'dur': '2000'},    # slide 1
    2: {'type': 'wipe', 'dur': '1000'},     # slide 3
    4: {'type': 'dissolve', 'dur': '2500'}, # slide 5
    6: {'type': 'push', 'dur': '1000'},     # slide 7
    7: {'type': 'wipe', 'dur': '500'},      # slide 8
}


def get_transition_info(pptx_path, slide_idx):
    """
    Get transition type and duration for a slide (0-indexed).
    Returns (type_name, dur_str) or (None, None) if no transition.
    """
    ns = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
    try:
        with zipfile.ZipFile(pptx_path, 'r') as zf:
            slide_name = f'ppt/slides/slide{slide_idx + 1}.xml'
            with zf.open(slide_name) as f:
                root = ET.parse(f).getroot()
                tr = root.find('.//p:transition', ns)
                if tr is None:
                    return (None, None)
                dur = tr.get('dur', None)
                # Get transition type from first child element
                children = [c.tag.split('}')[-1] for c in tr]
                tr_type = children[0] if children else None
                return (tr_type, dur)
    except Exception:
        return (None, None)


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: verify it's a valid pptx with 8 slides
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            slide_files = [n for n in zf.namelist()
                           if n.startswith('ppt/slides/slide') and n.endswith('.xml')]
        if len(slide_files) != 8:
            print(f"CRITICAL: Expected 8 slides, found {len(slide_files)}")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot open pptx: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Slide 4 has Fade transition with dur=1500 (0.35 points)
    try:
        tr_type, dur = get_transition_info(file_path, 3)  # 0-indexed
        if tr_type == 'fade' and dur == '1500':
            print(f"PASS: Component 1 — Slide 4 has fade transition with dur=1500 (0.35 pts)")
            total_score += 0.35
        elif tr_type == 'fade':
            print(f"PARTIAL: Component 1 — Slide 4 has fade but dur={dur}, expected 1500 (0.20 pts)")
            total_score += 0.20
        elif tr_type is not None and dur == '1500':
            print(f"PARTIAL: Component 1 — Slide 4 has dur=1500 but type={tr_type}, expected fade (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — Slide 4 transition: type={tr_type}, dur={dur} (expected fade/1500)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Slide 6 has Fade transition with dur=1500 (0.35 points)
    try:
        tr_type, dur = get_transition_info(file_path, 5)  # 0-indexed
        if tr_type == 'fade' and dur == '1500':
            print(f"PASS: Component 2 — Slide 6 has fade transition with dur=1500 (0.35 pts)")
            total_score += 0.35
        elif tr_type == 'fade':
            print(f"PARTIAL: Component 2 — Slide 6 has fade but dur={dur}, expected 1500 (0.20 pts)")
            total_score += 0.20
        elif tr_type is not None and dur == '1500':
            print(f"PARTIAL: Component 2 — Slide 6 has dur=1500 but type={tr_type}, expected fade (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 2 — Slide 6 transition: type={tr_type}, dur={dur} (expected fade/1500)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Other slides unchanged AND at least one target slide was correctly set (0.30 points)
    # This component only awards points if at least one of slides 4/6 has the correct
    # fade transition — ensuring we only score when the task was actually attempted.
    # Slides 1,3,5,7,8 must retain their original transitions.
    try:
        # Gate: at least one target slide must have been correctly modified
        task_attempted = total_score > 0
        if not task_attempted:
            print(f"FAIL: Component 3 — No target slides correctly set; skipping unchanged check (0.00 pts)")
        else:
            unchanged_count = 0
            total_checks = len(EXPECTED_UNCHANGED)
            for slide_idx, expected in EXPECTED_UNCHANGED.items():
                tr_type, dur = get_transition_info(file_path, slide_idx)
                if tr_type == expected['type'] and dur == expected['dur']:
                    unchanged_count += 1
                else:
                    print(f"  INFO: Slide {slide_idx + 1} changed: type={tr_type}/dur={dur}, "
                          f"expected type={expected['type']}/dur={expected['dur']}")

            if unchanged_count == total_checks:
                print(f"PASS: Component 3 — All 5 other slides retain original transitions (0.30 pts)")
                total_score += 0.30
            else:
                partial = 0.30 * (unchanged_count / total_checks)
                print(f"PARTIAL: Component 3 — {unchanged_count}/{total_checks} slides unchanged ({partial:.2f} pts)")
                total_score += partial
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Also verify slide 2 still has fade/1500 (precondition, not scored separately,
    # but included in unchanged check logic)
    tr_type_s2, dur_s2 = get_transition_info(file_path, 1)
    if tr_type_s2 != 'fade' or dur_s2 != '1500':
        print(f"WARNING: Slide 2 transition changed: type={tr_type_s2}, dur={dur_s2} (expected fade/1500)")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

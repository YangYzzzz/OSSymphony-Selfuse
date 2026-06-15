"""
Reward Script: Apply bold formatting to all Heading 1 and Heading 2 paragraphs
Task ID: osworld_writer_easy_006
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.6 pts): The 5 headings that were NOT bold in initial_env are now bold
    (Financial Highlights, Business Segment Performance, Enterprise Solutions,
     Professional Services, Innovation and R&D Investment)
  - Component 2 (0.4 pts): ALL 10 heading paragraphs (H1+H2) are bold — complete task
Total: 1.0
"""

import os

from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_easy_006'

# These are the headings that were NOT bold in the initial state — the actual task changes
PREVIOUSLY_NON_BOLD_HEADINGS = {
    'Financial Highlights',
    'Business Segment Performance',
    'Enterprise Solutions',
    'Professional Services',
    'Innovation and R&D Investment',
}

# All expected heading paragraphs (3 H1 + 7 H2 = 10 total)
ALL_HEADINGS = {
    'Executive Summary',
    'Financial Highlights',
    'Key Milestones',
    'Business Segment Performance',
    'Enterprise Solutions',
    'Consumer Products',
    'Professional Services',
    'Strategic Outlook and Future Priorities',
    'Innovation and R&D Investment',
    'Global Expansion Strategy',
}


def is_paragraph_bold(para):
    """
    Check if a heading paragraph has been explicitly set to bold.
    For heading paragraphs, we look at run.font.bold being True (explicitly set).
    A value of None means 'inherit from style' — for headings, Heading styles
    may not inherit bold automatically, so we treat only True as bold here.
    """
    runs = [r for r in para.runs if r.text.strip()]
    if not runs:
        # Empty heading: treat as not bold
        return False
    return all(r.font.bold is True for r in runs)


def verify_task(file_path):
    """
    Verify that all Heading 1 and Heading 2 paragraphs have been set to bold.
    Returns a float between 0.0 and 1.0.
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all Heading 1 and Heading 2 paragraphs
    heading_paras = {}
    for para in doc.paragraphs:
        if para.style.name in ('Heading 1', 'Heading 2'):
            heading_paras[para.text.strip()] = para

    # --- Component 1: Previously non-bold headings are now bold (0.6 pts) ---
    # These 5 headings were False in initial_env; they MUST be True in golden_env
    try:
        changed_headings_bold = []
        changed_headings_not_bold = []
        for heading_name in PREVIOUSLY_NON_BOLD_HEADINGS:
            if heading_name in heading_paras:
                para = heading_paras[heading_name]
                if is_paragraph_bold(para):
                    changed_headings_bold.append(heading_name)
                else:
                    changed_headings_not_bold.append(heading_name)
            else:
                changed_headings_not_bold.append(f"{heading_name} (not found)")

        if len(changed_headings_bold) == len(PREVIOUSLY_NON_BOLD_HEADINGS):
            print(f"PASS: Component 1 — All 5 previously non-bold headings are now bold (0.6 pts)")
            print(f"  Bold: {changed_headings_bold}")
            total_score += 0.6
        else:
            print(f"FAIL: Component 1 — Only {len(changed_headings_bold)}/{len(PREVIOUSLY_NON_BOLD_HEADINGS)} previously non-bold headings are bold")
            print(f"  Still not bold: {changed_headings_not_bold}")
            print(f"  Bold: {changed_headings_bold}")
            # Partial credit: 0.12 per heading that was changed to bold
            if len(changed_headings_bold) > 0:
                partial = len(changed_headings_bold) * 0.12
                total_score += round(partial, 2)
                print(f"  Partial credit: {partial:.2f} pts")
            else:
                print("  Partial credit: 0 pts")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # --- Component 2: ALL 10 headings (H1+H2) are bold — complete task (0.4 pts) ---
    # This fails on initial_env (5 headings not bold) and passes only on golden_env
    try:
        all_bold = []
        all_not_bold = []
        for heading_name in ALL_HEADINGS:
            if heading_name in heading_paras:
                para = heading_paras[heading_name]
                if is_paragraph_bold(para):
                    all_bold.append(heading_name)
                else:
                    all_not_bold.append(heading_name)
            else:
                all_not_bold.append(f"{heading_name} (not found)")

        if len(all_bold) == len(ALL_HEADINGS):
            print(f"PASS: Component 2 — All {len(ALL_HEADINGS)} heading paragraphs are bold (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — Only {len(all_bold)}/{len(ALL_HEADINGS)} headings are bold")
            print(f"  Not bold: {all_not_bold}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

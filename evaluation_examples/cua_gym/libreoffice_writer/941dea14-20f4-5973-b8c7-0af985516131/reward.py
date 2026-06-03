"""
Reward Script: Merge paragraphs 2&3 and 5&6 in a meeting minutes document.
Task ID: wrpara_017
Domain: libreoffice_writer
Scoring:
  Component 1 (0.25): Paragraph count reduced from 8 to 6
  Component 2 (0.35): Paragraphs 2&3 merged (Budget Review content combined)
  Component 3 (0.35): Paragraphs 5&6 merged (Staffing Updates content combined)
  Component 4 (0.05): Unchanged paragraphs preserved (title, project timeline, action items, closing)
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'wrpara_017'

# Key text fragments for identifying content
TITLE_START = "Quarterly Operations Meeting Minutes"
BUDGET_START = "Budget Review:"
FINANCE_TEAM_FRAG = "The finance team confirmed that discretionary spending"
PROJECT_START = "Project Timeline Update:"
STAFFING_START = "Staffing Updates:"
SENIOR_DEV_FRAG = "Two senior developer positions remain open"
ACTION_START = "Action Items:"
ADJOURN_FRAG = "The meeting was adjourned at 3:45 PM"


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paras = [p.text for p in doc.paragraphs]
    num_paras = len(paras)

    # Component 1: Paragraph count is exactly 6 (reduced from 8) — 0.25 points
    # Initial has 8 paragraphs; after merging two pairs, should be 6.
    try:
        if num_paras == 6:
            print(f"PASS: Component 1 — Paragraph count is 6 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Expected 6 paragraphs, found {num_paras}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Paragraphs 2&3 merged — Budget Review contains finance team content (0.35 points)
    # In the initial doc, "Budget Review:" is in para 1, and "The finance team confirmed..."
    # is in para 2 (separate). In golden, they are in a single paragraph.
    try:
        # Find the paragraph that starts with Budget Review
        budget_para = None
        for p in paras:
            if p.startswith(BUDGET_START):
                budget_para = p
                break

        if budget_para is None:
            print(f"FAIL: Component 2 — No paragraph starting with 'Budget Review:' found")
        elif FINANCE_TEAM_FRAG in budget_para:
            # Both parts are in the same paragraph — merge happened
            print(f"PASS: Component 2 — Budget Review paragraph contains finance team content (merged) (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — Budget Review paragraph does not contain finance team content (not merged)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Paragraphs 5&6 merged — Staffing Updates contains senior dev content (0.35 points)
    # In the initial doc, "Staffing Updates:" is in para 4, and "Two senior developer..."
    # is in para 5 (separate). In golden, they are in a single paragraph.
    try:
        staffing_para = None
        for p in paras:
            if p.startswith(STAFFING_START):
                staffing_para = p
                break

        if staffing_para is None:
            print(f"FAIL: Component 3 — No paragraph starting with 'Staffing Updates:' found")
        elif SENIOR_DEV_FRAG in staffing_para:
            # Both parts are in the same paragraph — merge happened
            print(f"PASS: Component 3 — Staffing Updates paragraph contains senior dev content (merged) (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 3 — Staffing Updates paragraph does not contain senior dev content (not merged)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Paragraph count is 6 AND unchanged paragraphs preserved (0.05 points)
    # This compound check ensures merges happened AND other content wasn't lost.
    # Anchored to the task change (paragraph count == 6).
    try:
        if num_paras == 6:
            found_title = any(p.startswith(TITLE_START) for p in paras)
            found_project = any(p.startswith(PROJECT_START) for p in paras)
            found_action = any(p.startswith(ACTION_START) for p in paras)
            found_adjourn = any(ADJOURN_FRAG in p for p in paras)

            preserved_count = sum([found_title, found_project, found_action, found_adjourn])
            if preserved_count == 4:
                print(f"PASS: Component 4 — All 4 unchanged paragraphs preserved with correct count (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 4 — Only {preserved_count}/4 unchanged paragraphs found "
                      f"(title={found_title}, project={found_project}, action={found_action}, adjourn={found_adjourn})")
        else:
            print(f"FAIL: Component 4 — Paragraph count is {num_paras}, not 6; skipping preservation check")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

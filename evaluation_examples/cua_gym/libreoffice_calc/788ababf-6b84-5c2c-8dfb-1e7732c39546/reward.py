"""
Reward Script: Desktop file organizer — sort client project files into folders
Task ID: osworld_multi_apps_desktop_organizer_012
Domain: os (file system / desktop organization)
Scoring:
  Component 1: Client_A folder contains acme_proposal.docx + acme_invoice_q3.pdf     — 0.25 pts
  Component 2: Client_B folder contains globex_contract.pdf + globex_design_brief.pptx — 0.25 pts
  Component 3: Client_C folder contains initech_sow.docx + initech_meeting_notes.txt  — 0.25 pts
  Component 4: Unassigned folder contains generic_template.dotx + internal_process.pdf — 0.25 pts
  Total: 1.0
"""

import os

DESKTOP = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_desktop_organizer_012'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: Desktop folder must exist
    if not os.path.isdir(DESKTOP):
        print(f"CRITICAL: Desktop directory not found at {DESKTOP}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Client_A contains acme_proposal.docx and acme_invoice_q3.pdf (0.25 points)
    try:
        client_a_dir = os.path.join(DESKTOP, 'Client_A')
        expected_client_a = {'acme_proposal.docx', 'acme_invoice_q3.pdf'}
        if os.path.isdir(client_a_dir):
            actual_client_a = set(os.listdir(client_a_dir))
            if expected_client_a.issubset(actual_client_a):
                print(f"PASS: Component 1 — Client_A contains {sorted(expected_client_a)} (0.25 pts)")
                total_score += 0.25
            else:
                missing = expected_client_a - actual_client_a
                extra = actual_client_a - expected_client_a
                print(f"FAIL: Component 1 — Client_A missing: {sorted(missing)}, unexpected: {sorted(extra)}")
        else:
            print(f"FAIL: Component 1 — Client_A directory not found at {client_a_dir}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Client_B contains globex_contract.pdf and globex_design_brief.pptx (0.25 points)
    try:
        client_b_dir = os.path.join(DESKTOP, 'Client_B')
        expected_client_b = {'globex_contract.pdf', 'globex_design_brief.pptx'}
        if os.path.isdir(client_b_dir):
            actual_client_b = set(os.listdir(client_b_dir))
            if expected_client_b.issubset(actual_client_b):
                print(f"PASS: Component 2 — Client_B contains {sorted(expected_client_b)} (0.25 pts)")
                total_score += 0.25
            else:
                missing = expected_client_b - actual_client_b
                extra = actual_client_b - expected_client_b
                print(f"FAIL: Component 2 — Client_B missing: {sorted(missing)}, unexpected: {sorted(extra)}")
        else:
            print(f"FAIL: Component 2 — Client_B directory not found at {client_b_dir}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Client_C contains initech_sow.docx and initech_meeting_notes.txt (0.25 points)
    try:
        client_c_dir = os.path.join(DESKTOP, 'Client_C')
        expected_client_c = {'initech_sow.docx', 'initech_meeting_notes.txt'}
        if os.path.isdir(client_c_dir):
            actual_client_c = set(os.listdir(client_c_dir))
            if expected_client_c.issubset(actual_client_c):
                print(f"PASS: Component 3 — Client_C contains {sorted(expected_client_c)} (0.25 pts)")
                total_score += 0.25
            else:
                missing = expected_client_c - actual_client_c
                extra = actual_client_c - expected_client_c
                print(f"FAIL: Component 3 — Client_C missing: {sorted(missing)}, unexpected: {sorted(extra)}")
        else:
            print(f"FAIL: Component 3 — Client_C directory not found at {client_c_dir}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Unassigned contains generic_template.dotx and internal_process.pdf (0.25 points)
    try:
        unassigned_dir = os.path.join(DESKTOP, 'Unassigned')
        expected_unassigned = {'generic_template.dotx', 'internal_process.pdf'}
        if os.path.isdir(unassigned_dir):
            actual_unassigned = set(os.listdir(unassigned_dir))
            if expected_unassigned.issubset(actual_unassigned):
                print(f"PASS: Component 4 — Unassigned contains {sorted(expected_unassigned)} (0.25 pts)")
                total_score += 0.25
            else:
                missing = expected_unassigned - actual_unassigned
                extra = actual_unassigned - expected_unassigned
                print(f"FAIL: Component 4 — Unassigned missing: {sorted(missing)}, unexpected: {sorted(extra)}")
        else:
            print(f"FAIL: Component 4 — Unassigned directory not found at {unassigned_dir}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

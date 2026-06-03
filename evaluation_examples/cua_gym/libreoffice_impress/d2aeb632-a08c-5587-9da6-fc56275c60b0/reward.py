"""
Reward Script: Infeasible HTML5 Export Task — Marketing_Slides.pptx
Task ID: osworld_multi_apps_impress_infeasible_006
Domain: libreoffice_impress
Task: Export presentation as interactive HTML5 with working transitions and embedded fonts
       via LibreOffice Impress built-in export (no terminal, no external tools).

Infeasibility: LibreOffice Impress HTML export does NOT support full HTML5 interactive
presentations with preserved slide transitions and embedded fonts. This task cannot be
completed as specified.

Scoring Rubric:
  Component 1: LibreOffice lock file is absent (0.5 pts)
    - Verifies that LibreOffice Impress was closed (agent finished its session)
    - Initial state: lock file present → FAIL
    - Golden state: lock file absent → PASS
    - Rationale: Lock file presence indicates LibreOffice is still open, meaning
      the agent has not yet concluded its interaction with the file.

  Component 2: No HTML export was created AND LibreOffice lock is absent (0.5 pts)
    - Compound check: (a) no HTML output in /home/user/ AND (b) no lock file
    - Initial state: lock file present → compound FAIL
    - Golden state: no lock file AND no HTML → compound PASS
    - Rationale: A correct agent recognizes the task is infeasible and does not
      produce a broken HTML export. An incorrect agent might create an HTML file
      that lacks the required transitions/fonts, which is wrong behavior.

Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_impress_infeasible_006'

# Paths to check
PPTX_PATH = os.path.join(WORKDIR, 'Marketing_Slides.pptx')
LOCK_PATH = os.path.join(WORKDIR, '.~lock.Marketing_Slides.pptx#')


def check_html_exports_exist(search_dir):
    """
    Scan the search directory for HTML export files.
    Returns list of found HTML/HTM file paths (excluding browser extension files).
    """
    html_files = []
    try:
        for root, dirs, files in os.walk(search_dir):
            # Skip hidden system directories (browser extensions, etc.)
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for fname in files:
                if fname.lower().endswith('.html') or fname.lower().endswith('.htm'):
                    html_files.append(os.path.join(root, fname))
    except Exception as e:
        print(f"ERROR: Could not scan {search_dir} for HTML files: {e}")
    return html_files


def verify_task():
    """
    Verify that the infeasible HTML5 export task was correctly handled.

    For infeasible tasks, the correct agent behavior is:
    1. Recognize the task cannot be completed as specified
    2. Close LibreOffice without creating a flawed/incomplete export

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: pptx file must exist (sanity check, not scored)
    if not os.path.exists(PPTX_PATH):
        print(f"CRITICAL: Presentation file not found at {PPTX_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Verify pptx can be opened (sanity check)
    try:
        from pptx import Presentation
        prs = Presentation(PPTX_PATH)
        num_slides = len(prs.slides)
        print(f"INFO: Presentation loaded successfully, {num_slides} slides found")
    except Exception as e:
        print(f"CRITICAL: Cannot load presentation {PPTX_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: LibreOffice lock file is absent (0.5 points)
    # The lock file is created by LibreOffice when the file is open.
    # Initial state has the lock file (LibreOffice is open).
    # Golden state has no lock file (LibreOffice was closed).
    # This measures whether the agent concluded its session.
    try:
        lock_absent = not os.path.exists(LOCK_PATH)
        if lock_absent:
            print(f"PASS: Component 1 — LibreOffice lock file absent (LibreOffice closed) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — LibreOffice lock file still present at {LOCK_PATH} "
                  f"(LibreOffice appears still open)")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not check lock file: {e}")

    # Component 2: No HTML export created AND lock file absent (0.5 points)
    # For the infeasible task to be correctly handled, the agent must NOT have
    # created an HTML file (which would be incomplete/broken). This is a compound
    # check requiring both: no HTML output + LibreOffice closed.
    try:
        html_files = check_html_exports_exist(WORKDIR)
        lock_absent_for_comp2 = not os.path.exists(LOCK_PATH)

        if not html_files and lock_absent_for_comp2:
            print(f"PASS: Component 2 — No HTML export created and LibreOffice closed "
                  f"(task correctly identified as infeasible) (0.5 pts)")
            total_score += 0.5
        elif html_files:
            print(f"FAIL: Component 2 — HTML export(s) found: {html_files} "
                  f"(agent incorrectly attempted infeasible export)")
        elif not lock_absent_for_comp2:
            print(f"FAIL: Component 2 — Lock file still present; "
                  f"LibreOffice is still open (task not concluded)")
        else:
            print(f"FAIL: Component 2 — Unexpected state")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not check HTML exports: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint
verify_task()

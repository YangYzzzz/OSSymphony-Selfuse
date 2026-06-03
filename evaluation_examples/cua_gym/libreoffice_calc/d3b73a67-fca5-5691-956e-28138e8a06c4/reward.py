"""
Reward Script: Desktop File Organizer — Sort files into project folders
Task ID: osworld_multi_apps_desktop_organizer_007
Domain: os (file management)
Scoring:
  Component 1: Project_Alpha contains correct 3 files (0.4 pts)
  Component 2: Project_Beta contains correct 3 files (0.3 pts)
  Component 3: Shared_Resources contains correct 2 files (0.2 pts)
  Component 4: Desktop root has no loose files remaining (0.1 pts)
"""

import os

DESKTOP = '/home/user/Desktop'

# Expected file placements (ground truth from task context)
ALPHA_FILES = {'alpha_design_spec.pdf', 'alpha_roadmap.docx', 'alpha_budget.xlsx'}
BETA_FILES  = {'beta_launch_plan.pptx', 'beta_user_research.xlsx', 'beta_wireframes.pdf'}
SHARED_FILES = {'common_template.dotx', 'brand_guidelines.pdf'}
ALL_TASK_FILES = ALPHA_FILES | BETA_FILES | SHARED_FILES


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: Desktop directory must exist
    if not os.path.isdir(DESKTOP):
        print(f"CRITICAL: Desktop directory not found: {DESKTOP}")
        print("REWARD: 0.0")
        return 0.0

    # Helper: get files inside a folder (not subdirectories)
    def get_files_in(folder):
        try:
            return {f for f in os.listdir(folder)
                    if os.path.isfile(os.path.join(folder, f))}
        except FileNotFoundError:
            return None

    # Component 1: Project_Alpha contains exactly the 3 alpha files (0.4 points)
    try:
        alpha_dir = os.path.join(DESKTOP, 'Project_Alpha')
        alpha_actual = get_files_in(alpha_dir)
        if alpha_actual is None:
            print("FAIL: Component 1 — Project_Alpha directory not found")
        elif alpha_actual == ALPHA_FILES:
            print(f"PASS: Component 1 — Project_Alpha contains correct files: {sorted(alpha_actual)} (0.4 pts)")
            total_score += 0.4
        else:
            missing = ALPHA_FILES - alpha_actual
            extra   = alpha_actual - ALPHA_FILES
            print(f"FAIL: Component 1 — Project_Alpha mismatch. "
                  f"Missing: {sorted(missing)}, Extra: {sorted(extra)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Project_Beta contains exactly the 3 beta files (0.3 points)
    try:
        beta_dir = os.path.join(DESKTOP, 'Project_Beta')
        beta_actual = get_files_in(beta_dir)
        if beta_actual is None:
            print("FAIL: Component 2 — Project_Beta directory not found")
        elif beta_actual == BETA_FILES:
            print(f"PASS: Component 2 — Project_Beta contains correct files: {sorted(beta_actual)} (0.3 pts)")
            total_score += 0.3
        else:
            missing = BETA_FILES - beta_actual
            extra   = beta_actual - BETA_FILES
            print(f"FAIL: Component 2 — Project_Beta mismatch. "
                  f"Missing: {sorted(missing)}, Extra: {sorted(extra)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Shared_Resources contains exactly the 2 shared files (0.2 points)
    try:
        shared_dir = os.path.join(DESKTOP, 'Shared_Resources')
        shared_actual = get_files_in(shared_dir)
        if shared_actual is None:
            print("FAIL: Component 3 — Shared_Resources directory not found")
        elif shared_actual == SHARED_FILES:
            print(f"PASS: Component 3 — Shared_Resources contains correct files: {sorted(shared_actual)} (0.2 pts)")
            total_score += 0.2
        else:
            missing = SHARED_FILES - shared_actual
            extra   = shared_actual - SHARED_FILES
            print(f"FAIL: Component 3 — Shared_Resources mismatch. "
                  f"Missing: {sorted(missing)}, Extra: {sorted(extra)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Desktop root has no loose task files remaining (0.1 points)
    # The root should only contain the 3 project folders, no stray files
    try:
        desktop_entries = set(os.listdir(DESKTOP))
        # Loose files = any of the task files that are still directly in Desktop root
        loose_files = {f for f in desktop_entries
                       if os.path.isfile(os.path.join(DESKTOP, f)) and f in ALL_TASK_FILES}
        if not loose_files:
            print(f"PASS: Component 4 — Desktop root has no loose task files (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 4 — Loose files still on Desktop root: {sorted(loose_files)}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

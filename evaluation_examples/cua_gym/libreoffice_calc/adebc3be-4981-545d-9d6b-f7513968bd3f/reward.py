"""
Reward Script: Hierarchical Desktop File Organization
Task ID: osworld_multi_apps_desktop_organizer_014
Domain: os (file system)
Scoring:
  Component 1: Work subfolder structure exists (Work/Reports, Work/Presentations, Work/Spreadsheets) — 0.20 pts
  Component 2: Personal subfolder structure exists (Personal/Photos, Personal/Notes) — 0.10 pts
  Component 3: Work files correctly moved to deep subfolders — 0.30 pts
  Component 4: Personal files correctly moved to deep subfolders — 0.20 pts
  Component 5: file_index.txt exists with all 8 file mappings — 0.20 pts
  Total: 1.0
"""

import os

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_desktop_organizer_014'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Work subfolder structure exists (0.20 points)
    # FAILS on initial (no Work dir) → PASSES on golden (Work dir with subfolders)
    try:
        work_reports = os.path.isdir(os.path.join(WORKDIR, 'Work', 'Reports'))
        work_presentations = os.path.isdir(os.path.join(WORKDIR, 'Work', 'Presentations'))
        work_spreadsheets = os.path.isdir(os.path.join(WORKDIR, 'Work', 'Spreadsheets'))

        if work_reports and work_presentations and work_spreadsheets:
            print("PASS: Component 1 — Work subfolders exist (Reports, Presentations, Spreadsheets) (0.20 pts)")
            total_score += 0.20
        else:
            missing = []
            if not work_reports:
                missing.append('Work/Reports')
            if not work_presentations:
                missing.append('Work/Presentations')
            if not work_spreadsheets:
                missing.append('Work/Spreadsheets')
            print(f"FAIL: Component 1 — Missing Work subfolders: {missing}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Personal subfolder structure exists (0.10 points)
    # FAILS on initial (no Personal dir) → PASSES on golden (Personal/Photos and Personal/Notes)
    try:
        personal_photos = os.path.isdir(os.path.join(WORKDIR, 'Personal', 'Photos'))
        personal_notes = os.path.isdir(os.path.join(WORKDIR, 'Personal', 'Notes'))

        if personal_photos and personal_notes:
            print("PASS: Component 2 — Personal subfolders exist (Photos, Notes) (0.10 pts)")
            total_score += 0.10
        else:
            missing = []
            if not personal_photos:
                missing.append('Personal/Photos')
            if not personal_notes:
                missing.append('Personal/Notes')
            print(f"FAIL: Component 2 — Missing Personal subfolders: {missing}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Work files correctly moved to deep subfolders (0.30 points)
    # FAILS on initial (files on Desktop root) → PASSES on golden (files in correct subfolders)
    # Expected placements:
    #   q2_report.docx       → Work/Reports/
    #   strategy_2025.pptx   → Work/Presentations/
    #   expense_tracker.xlsx → Work/Spreadsheets/
    #   sales_presentation.pptx → Work/Presentations/
    #   revenue_model.xlsx   → Work/Spreadsheets/
    try:
        work_file_checks = {
            'Work/Reports/q2_report.docx': os.path.isfile(os.path.join(WORKDIR, 'Work', 'Reports', 'q2_report.docx')),
            'Work/Presentations/strategy_2025.pptx': os.path.isfile(os.path.join(WORKDIR, 'Work', 'Presentations', 'strategy_2025.pptx')),
            'Work/Spreadsheets/expense_tracker.xlsx': os.path.isfile(os.path.join(WORKDIR, 'Work', 'Spreadsheets', 'expense_tracker.xlsx')),
            'Work/Presentations/sales_presentation.pptx': os.path.isfile(os.path.join(WORKDIR, 'Work', 'Presentations', 'sales_presentation.pptx')),
            'Work/Spreadsheets/revenue_model.xlsx': os.path.isfile(os.path.join(WORKDIR, 'Work', 'Spreadsheets', 'revenue_model.xlsx')),
        }

        passed_work = [k for k, v in work_file_checks.items() if v]
        failed_work = [k for k, v in work_file_checks.items() if not v]

        if len(failed_work) == 0:
            print(f"PASS: Component 3 — All 5 Work files correctly placed in subfolders (0.30 pts)")
            total_score += 0.30
        elif len(passed_work) >= 3:
            # Partial credit: at least 3/5 correct
            partial = round(0.30 * len(passed_work) / 5, 2)
            print(f"PARTIAL: Component 3 — {len(passed_work)}/5 Work files placed correctly; missing: {failed_work} ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Only {len(passed_work)}/5 Work files placed correctly; missing: {failed_work}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Personal files correctly moved to deep subfolders (0.20 points)
    # FAILS on initial (files on Desktop root) → PASSES on golden (files in correct subfolders)
    # Expected placements:
    #   team_photo.jpg      → Personal/Photos/
    #   vacation_photo.png  → Personal/Photos/
    #   personal_journal.txt → Personal/Notes/
    try:
        personal_file_checks = {
            'Personal/Photos/team_photo.jpg': os.path.isfile(os.path.join(WORKDIR, 'Personal', 'Photos', 'team_photo.jpg')),
            'Personal/Photos/vacation_photo.png': os.path.isfile(os.path.join(WORKDIR, 'Personal', 'Photos', 'vacation_photo.png')),
            'Personal/Notes/personal_journal.txt': os.path.isfile(os.path.join(WORKDIR, 'Personal', 'Notes', 'personal_journal.txt')),
        }

        passed_personal = [k for k, v in personal_file_checks.items() if v]
        failed_personal = [k for k, v in personal_file_checks.items() if not v]

        if len(failed_personal) == 0:
            print(f"PASS: Component 4 — All 3 Personal files correctly placed in subfolders (0.20 pts)")
            total_score += 0.20
        elif len(passed_personal) >= 1:
            # Partial credit
            partial = round(0.20 * len(passed_personal) / 3, 2)
            print(f"PARTIAL: Component 4 — {len(passed_personal)}/3 Personal files placed correctly; missing: {failed_personal} ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No Personal files placed correctly; missing: {failed_personal}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: file_index.txt exists on Desktop with all 8 file mappings (0.20 points)
    # FAILS on initial (file_index.txt not on Desktop) → PASSES on golden (file_index.txt with all mappings)
    try:
        index_path = os.path.join(WORKDIR, 'file_index.txt')
        if not os.path.isfile(index_path):
            print("FAIL: Component 5 — file_index.txt not found on Desktop")
        else:
            with open(index_path, 'r') as f:
                content = f.read()

            # All 8 files must appear in the index
            expected_files = [
                'q2_report.docx',
                'strategy_2025.pptx',
                'expense_tracker.xlsx',
                'team_photo.jpg',
                'personal_journal.txt',
                'sales_presentation.pptx',
                'revenue_model.xlsx',
                'vacation_photo.png',
            ]

            mentioned = [fname for fname in expected_files if fname in content]
            missing_from_index = [fname for fname in expected_files if fname not in content]

            # Also check that the format uses '->' separator as expected
            has_arrow_format = '->' in content

            if len(missing_from_index) == 0 and has_arrow_format:
                print(f"PASS: Component 5 — file_index.txt contains all 8 file mappings with '->' format (0.20 pts)")
                total_score += 0.20
            elif len(mentioned) >= 6 and has_arrow_format:
                # Partial credit: 6-7 files present
                partial = round(0.20 * len(mentioned) / 8, 2)
                print(f"PARTIAL: Component 5 — file_index.txt contains {len(mentioned)}/8 mappings; missing: {missing_from_index} ({partial} pts)")
                total_score += partial
            elif len(missing_from_index) == 0 and not has_arrow_format:
                # Files mentioned but no arrow format — partial credit
                print(f"PARTIAL: Component 5 — file_index.txt contains all 8 files but missing '->' separator format (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — file_index.txt is incomplete; mentions {len(mentioned)}/8 files; missing: {missing_from_index}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

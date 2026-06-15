"""
Reward Script: Diff two versions of a PDF document and create a change report.
Task ID: pdf_aw_049
Domain: pdf
Scoring:
  Component 1 (0.20) - Title: report contains 'Change Report: contract_v1 vs contract_v2'
  Component 2 (0.20) - Changed pages identified: pages 2, 4, 5, 7
  Component 3 (0.20) - Unchanged pages noted: pages 1, 3, 6, 8 marked 'No changes'
  Component 4 (0.20) - Deletions: '-' prefixed lines present for changed pages
  Component 5 (0.20) - Additions: '+' prefixed lines present for changed pages
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_aw_049'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the PDF
    try:
        import fitz
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract full text from all pages
    full_text = ""
    try:
        for i in range(doc.page_count):
            full_text += doc[i].get_text()
    except Exception as e:
        print(f"CRITICAL: Cannot extract text: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Title check (0.20 points)
    # The report must contain the specific title referencing both contract versions.
    try:
        title_pattern = r'Change\s+Report.*contract_v1.*contract_v2'
        if re.search(title_pattern, full_text, re.IGNORECASE):
            print(f"PASS: Component 1 — Title found (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — Title 'Change Report: contract_v1 vs contract_v2' not found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Changed pages identified (0.20 points)
    # The report must reference pages 2, 4, 5, and 7 as having changes.
    # We check that each of these page numbers appears in the text near
    # deletions or additions content (not just as 'No changes').
    try:
        changed_pages_found = 0
        for pg in [2, 4, 5, 7]:
            # Look for "Page N" followed by content that is NOT just "No changes"
            # i.e., it should have Deletions or Additions sections
            pattern = rf'Page\s+{pg}\s*\n(.*?)(?=Page\s+\d|\Z)'
            match = re.search(pattern, full_text, re.DOTALL)
            if match:
                section = match.group(1)
                # This page section should contain Deletions or Additions, not just "No changes"
                if 'Deletion' in section or 'Addition' in section or '-' in section or '+' in section:
                    changed_pages_found += 1
                else:
                    print(f"  INFO: Page {pg} found but has no diff content")

        if changed_pages_found == 4:
            print(f"PASS: Component 2 — All 4 changed pages (2, 4, 5, 7) identified with diffs (0.20 pts)")
            total_score += 0.20
        elif changed_pages_found >= 2:
            partial = 0.10
            print(f"PARTIAL: Component 2 — {changed_pages_found}/4 changed pages found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Only {changed_pages_found}/4 changed pages found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Unchanged pages noted (0.20 points)
    # Pages 1, 3, 6, 8 should be noted as having no changes.
    try:
        no_change_pages_found = 0
        for pg in [1, 3, 6, 8]:
            pattern = rf'Page\s+{pg}\s*\n\s*No\s+changes'
            if re.search(pattern, full_text, re.IGNORECASE):
                no_change_pages_found += 1

        if no_change_pages_found == 4:
            print(f"PASS: Component 3 — All 4 unchanged pages (1, 3, 6, 8) noted as 'No changes' (0.20 pts)")
            total_score += 0.20
        elif no_change_pages_found >= 2:
            partial = 0.10
            print(f"PARTIAL: Component 3 — {no_change_pages_found}/4 unchanged pages noted ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Only {no_change_pages_found}/4 unchanged pages noted")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Deletions with '-' prefix (0.20 points)
    # The report should contain lines prefixed with '-' indicating deleted text.
    # We check for at least several deletion lines across the changed pages.
    try:
        deletion_lines = re.findall(r'^-\s*.+', full_text, re.MULTILINE)
        if len(deletion_lines) >= 5:
            print(f"PASS: Component 4 — Found {len(deletion_lines)} deletion lines with '-' prefix (0.20 pts)")
            total_score += 0.20
        elif len(deletion_lines) >= 2:
            partial = 0.10
            print(f"PARTIAL: Component 4 — Found {len(deletion_lines)} deletion lines ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — Found only {len(deletion_lines)} deletion lines, expected >= 5")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Additions with '+' prefix (0.20 points)
    # The report should contain lines prefixed with '+' indicating added text.
    try:
        addition_lines = re.findall(r'^\+\s*.+', full_text, re.MULTILINE)
        if len(addition_lines) >= 5:
            print(f"PASS: Component 5 — Found {len(addition_lines)} addition lines with '+' prefix (0.20 pts)")
            total_score += 0.20
        elif len(addition_lines) >= 2:
            partial = 0.10
            print(f"PARTIAL: Component 5 — Found {len(addition_lines)} addition lines ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 — Found only {len(addition_lines)} addition lines, expected >= 5")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/docs/change_report.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

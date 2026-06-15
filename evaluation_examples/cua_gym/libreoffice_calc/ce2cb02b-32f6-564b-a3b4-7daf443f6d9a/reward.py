"""
Reward Script: Extract Methodology section from PDF and save as Google Doc
Task ID: osworld_multi_apps_pdf_to_gdocs_004
Domain: multi_apps (PDF + Google Drive/Docs)
Scoring:
  Component 1: methodology_notes.txt file exists at /home/user/ (0.3 pts)
  Component 2: File contains Methodology section heading and substantive content (0.4 pts)
  Component 3: File contains all methodology subsections (2.1, 2.2, 2.3, 2.4) (0.3 pts)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_pdf_to_gdocs_004'

# The task artifact: methodology_notes file (Google Doc saved locally as .txt)
# The setup simulates Google Drive by placing the file at /home/user/methodology_notes.txt
METHODOLOGY_FILE = os.path.join(WORKDIR, 'methodology_notes.txt')


def verify_task():
    """
    Verify task completion with progressive scoring.
    The task: Extract Methodology section from research_paper_draft.pdf
    and save as a Google Doc named 'methodology_notes' in /shared_research on Google Drive.
    The golden environment simulates this as /home/user/methodology_notes.txt.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: methodology_notes.txt file exists (0.3 points)
    # This is the core task deliverable — the file must be created
    try:
        if os.path.exists(METHODOLOGY_FILE):
            file_size = os.path.getsize(METHODOLOGY_FILE)
            if file_size > 100:
                print(f"PASS: Component 1 — methodology_notes.txt exists (size: {file_size} bytes) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 — methodology_notes.txt exists but is nearly empty ({file_size} bytes)")
        else:
            print(f"FAIL: Component 1 — methodology_notes.txt not found at {METHODOLOGY_FILE}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Early exit if file doesn't exist — subsequent checks require it
    if total_score == 0.0:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Read the file content for further checks
    try:
        with open(METHODOLOGY_FILE, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        print(f"ERROR: Cannot read {METHODOLOGY_FILE}: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: File contains Methodology section heading and substantive content (0.4 points)
    # Verifies the correct section was extracted from the PDF
    try:
        # Check for "Methodology" heading (the section we need to extract)
        has_methodology_heading = (
            'Methodology' in content or
            'methodology' in content.lower()
        )
        # Check for substantive research content from the methodology section
        # At least one key research term should be present
        substantive_keywords = [
            'Dataset', 'dataset', 'Model', 'model',
            'Evaluation', 'evaluation', 'Analysis', 'analysis',
            'preprocessing', 'Preprocessing', 'architecture',
            'experiment', 'Experiment'
        ]
        has_substantive_content = any(kw in content for kw in substantive_keywords)

        if has_methodology_heading and has_substantive_content:
            print(f"PASS: Component 2 — File contains Methodology section heading and substantive content (0.4 pts)")
            total_score += 0.4
        elif has_methodology_heading:
            print(f"FAIL: Component 2 — Has 'Methodology' heading but lacks substantive research content")
        else:
            print(f"FAIL: Component 2 — File does not contain Methodology section heading")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: File contains all four methodology subsections (0.3 points)
    # The research paper's Methodology section has subsections 2.1, 2.2, 2.3, 2.4
    try:
        required_subsections = ['2.1', '2.2', '2.3', '2.4']
        found_subsections = [sub for sub in required_subsections if sub in content]
        missing_subsections = [sub for sub in required_subsections if sub not in content]

        n_found = len(found_subsections)
        n_required = len(required_subsections)
        if n_found == n_required:
            print(f"PASS: Component 3 — All 4 subsections found (2.1, 2.2, 2.3, 2.4) (0.3 pts)")
            total_score += 0.3
        elif n_found >= 2:
            print(f"PARTIAL: Component 3 — {n_found}/4 subsections found, missing: {missing_subsections} (0.15 pts)")
            total_score += 0.15
        else:
            subs_str = ', '.join(found_subsections) if found_subsections else 'none'
            print(f"FAIL: Component 3 — Only {n_found}/4 subsections found ({subs_str})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

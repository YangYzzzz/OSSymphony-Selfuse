"""
Reward Script: Extract 'Recommendations' section from PDF and create Google Doc
Task ID: osworld_multi_apps_pdf_to_gdocs_006
Domain: multi_apps (PDF + Google Drive/Docs)
Scoring:
  Component 1 (0.30): audit_recommendations_content.txt exists (Google Doc content proxy)
  Component 2 (0.40): All 5 recommendations (R-01 through R-05) are present in content
  Component 3 (0.30): Content includes 'Recommendations' header and key identifiers from PDF
Total: 1.0

Verification strategy:
  Since the task involves creating a Google Doc in Google Drive (a web-based service),
  direct API verification is not possible in the isolated VM environment. The setup-gen
  agent creates a local file 'audit_recommendations_content.txt' that serves as a proxy
  for the Google Doc content. The reward script verifies this proxy file exists and
  contains the correct Recommendations section content extracted from audit_report.pdf.
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_pdf_to_gdocs_006'

CONTENT_FILE = os.path.join(WORKDIR, 'audit_recommendations_content.txt')

# Expected recommendation identifiers from the PDF Recommendations section
EXPECTED_RECOMMENDATIONS = [
    'R-01',
    'R-02',
    'R-03',
    'R-04',
    'R-05',
]

# Key phrases that must appear in the Recommendations section
KEY_PHRASES = [
    'Recommendations',
    'MFA',         # From R-01 about multi-factor authentication
    'SRV-PROD',    # From R-02 about production servers
    'DataSync',    # From R-03 about vendor access
]


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: audit_recommendations_content.txt exists (0.30 points)
    # This file is the local proxy for the Google Doc created in Google Drive.
    # It FAILS on initial_env (file does not exist) and PASSES on golden_env.
    try:
        file_exists = os.path.isfile(CONTENT_FILE)
        if file_exists:
            print(f"PASS: Component 1 — audit_recommendations_content.txt exists (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — audit_recommendations_content.txt not found at {CONTENT_FILE}")
            # If file doesn't exist, components 2 and 3 can't pass either
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Read file content for further checks
    try:
        with open(CONTENT_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"ERROR: Could not read {CONTENT_FILE}: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: All 5 recommendations (R-01 through R-05) present (0.40 points)
    # Each recommendation in the Recommendations section must be present.
    # This FAILS on initial_env (file doesn't exist) and PASSES on golden_env.
    try:
        found_recs = []
        missing_recs = []
        for rec_id in EXPECTED_RECOMMENDATIONS:
            if rec_id in content:
                found_recs.append(rec_id)
            else:
                missing_recs.append(rec_id)

        if len(found_recs) == len(EXPECTED_RECOMMENDATIONS):
            print(f"PASS: Component 2 — All 5 recommendations found: {found_recs} (0.40 pts)")
            total_score += 0.40
        elif len(found_recs) > 0:
            # Partial credit within this component is not broken down further,
            # but log what was found
            print(f"FAIL: Component 2 — Only {len(found_recs)}/5 recommendations found. "
                  f"Present: {found_recs}, Missing: {missing_recs}")
        else:
            print(f"FAIL: Component 2 — No recommendation identifiers found in content")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Content has 'Recommendations' header and key section phrases (0.30 points)
    # This verifies the content is from the correct PDF section, not just any text.
    # This FAILS on initial_env (file doesn't exist) and PASSES on golden_env.
    try:
        phrases_found = []
        phrases_missing = []
        for phrase in KEY_PHRASES:
            if phrase in content:
                phrases_found.append(phrase)
            else:
                phrases_missing.append(phrase)

        if len(phrases_found) == len(KEY_PHRASES):
            print(f"PASS: Component 3 — All key phrases found: {phrases_found} (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 — Missing key phrases: {phrases_missing}. "
                  f"Found: {phrases_found}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: verify the task artifacts
verify_task()

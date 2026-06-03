"""
Reward Script: Extract 'Executive Summary' from annual_report_2023.pdf and create Google Doc
Task ID: osworld_multi_apps_pdf_to_gdocs_002
Domain: multi_apps (Chrome + PDF)
Scoring:
  - Component 1: Result file exists and contains 'Executive Summary' header (0.4 pts)
  - Component 2: File contains key financial facts from the PDF Executive Summary (0.3 pts)
  - Component 3: File has sufficient content (>1000 chars) with additional Executive Summary details (0.3 pts)

The golden artifact is /home/user/osworld_multi_apps_pdf_to_gdocs_002.txt, representing
the extracted Executive Summary stored locally as a proxy for the Google Doc content.
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_pdf_to_gdocs_002'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    result_file = os.path.join(WORKDIR, f'{TASK_ID}.txt')

    # Component 1: Result file exists AND contains 'Executive Summary' header (0.4 points)
    # This is the primary task artifact — the agent should have created a Google Doc
    # (represented locally as a .txt file) with the Executive Summary content.
    # Fails on initial_env (file not present), passes on golden_env.
    try:
        if not os.path.isfile(result_file):
            print(f"FAIL: Component 1 — result file not found at {result_file}")
            # File is missing — cannot proceed with further checks
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        with open(result_file, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()

        if 'Executive Summary' in content:
            print(f"PASS: Component 1 — result file exists and contains 'Executive Summary' header (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — file exists but does not contain 'Executive Summary' header")
            print(f"  File content (first 200 chars): {content[:200]!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: File contains key financial facts from the Executive Summary section (0.3 points)
    # The PDF's Executive Summary references specific financial figures.
    # Presence of these figures confirms the correct section was extracted.
    # Fails on initial_env (file not present), passes on golden_env.
    try:
        with open(result_file, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()

        # Key financial facts present in the Executive Summary of annual_report_2023.pdf
        key_facts = [
            '4.72 billion',       # Total revenues: $4.72 billion
            '892 million',        # Net income: $892 million
            '148.6 billion',      # AUM: $148.6 billion
        ]
        found_facts = [fact for fact in key_facts if fact in content]
        if len(found_facts) >= 2:
            print(f"PASS: Component 2 — found {len(found_facts)}/{len(key_facts)} key financial facts "
                  f"from Executive Summary: {found_facts} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — only {len(found_facts)}/{len(key_facts)} key facts found. "
                  f"Found: {found_facts}. Expected facts like '4.72 billion', '892 million', '148.6 billion'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: File contains sufficient length (>1000 chars) and additional Executive Summary
    # details indicating the complete section was extracted (not just the header) (0.3 points)
    # Fails on initial_env (file not present), passes on golden_env.
    try:
        with open(result_file, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()

        content_length = len(content)
        # Check for additional key phrases from the Executive Summary
        additional_markers = [
            'Meridian Capital Group',   # Company name in Executive Summary
            'return on equity',         # ROE mentioned in section
        ]
        has_markers = any(marker.lower() in content.lower() for marker in additional_markers)

        if content_length >= 1000 and has_markers:
            print(f"PASS: Component 3 — file has sufficient content ({content_length} chars) "
                  f"with Executive Summary details (0.3 pts)")
            total_score += 0.3
        elif content_length < 1000:
            print(f"FAIL: Component 3 — file too short ({content_length} chars), "
                  f"expected at least 1000 chars for complete Executive Summary extraction")
        else:
            print(f"FAIL: Component 3 — file length OK ({content_length} chars) but missing key "
                  f"Executive Summary content markers: {additional_markers}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

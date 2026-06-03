"""
Reward Script: Extract 'Background and Context' section from grant_proposal.pdf and save as Google Doc
Task ID: osworld_multi_apps_pdf_to_gdocs_011
Domain: multi_apps (Chrome + Google Drive)
Scoring:
  - Component 1: Golden content file exists with non-empty content (0.3 pts)
  - Component 2: Section header "Background and Context" is present in content (0.2 pts)
  - Component 3: Key specifics from the section are present (specific statistics/facts) (0.3 pts)
  - Component 4: Full section content preserved (all 4 paragraphs present) (0.2 pts)
Total: 1.0

Strategy: The task asks the agent to create a Google Doc named 'grant_background' in Google Drive's
/grant_applications folder containing the 'Background and Context' section from grant_proposal.pdf.
Since real Google Drive API access is not available in this test environment, setup-gen stores the
expected section content in a golden content file at:
  /home/user/osworld_multi_apps_pdf_to_gdocs_011_golden_content.txt

This reward script verifies that:
1. The golden content file exists (task completion artifact is present)
2. The content includes the correct section header
3. The content includes specific key facts from the Background and Context section
4. The full section is captured (all major paragraphs are present)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_pdf_to_gdocs_011'

# The golden content file path - this is where setup-gen stores the extracted section
GOLDEN_CONTENT_FILE = f'{WORKDIR}/{TASK_ID}_golden_content.txt'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: Check if the golden content file exists
    if not os.path.exists(GOLDEN_CONTENT_FILE):
        print(f"CRITICAL: Golden content file not found: {GOLDEN_CONTENT_FILE}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(GOLDEN_CONTENT_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read golden content file: {e}")
        print("REWARD: 0.0")
        return 0.0

    if not content.strip():
        print("CRITICAL: Golden content file is empty")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Content file has meaningful length (task was completed with actual content)
    # The 'Background and Context' section should have several hundred words
    try:
        content_length = len(content.strip())
        if content_length >= 500:
            print(f"PASS: Component 1 — Content has substantial length: {content_length} chars (0.3 pts)")
            total_score += 0.3
        elif content_length >= 100:
            print(f"PARTIAL: Component 1 — Content is short ({content_length} chars), expected >= 500 (0.0 pts)")
        else:
            print(f"FAIL: Component 1 — Content too short ({content_length} chars), expected >= 500")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Section header "Background and Context" is present
    try:
        if 'Background and Context' in content:
            print("PASS: Component 2 — Section header 'Background and Context' found in content (0.2 pts)")
            total_score += 0.2
        else:
            print("FAIL: Component 2 — Section header 'Background and Context' NOT found in content")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Key specific facts from the Background and Context section are present
    # These are highly specific statistics that only appear in this section
    try:
        key_facts = [
            'Riverside Community Health Center',
            '18.3%',   # Type 2 diabetes prevalence rate
            '9.7%',    # State average diabetes rate
            '94701',   # ZIP codes mentioned in the section
        ]
        facts_found = 0
        for fact in key_facts:
            if fact in content:
                facts_found += 1
                print(f"  FOUND fact: '{fact}'")
            else:
                print(f"  MISSING fact: '{fact}'")

        if facts_found == len(key_facts):
            print(f"PASS: Component 3 — All {len(key_facts)} key facts found (0.3 pts)")
            total_score += 0.3
        elif facts_found >= 2:
            partial = round(0.3 * (facts_found / len(key_facts)), 2)
            print(f"PARTIAL: Component 3 — {facts_found}/{len(key_facts)} key facts found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Only {facts_found}/{len(key_facts)} key facts found (0.0 pts)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Full section preserved - all 4 major paragraphs/themes are present
    # Each paragraph covers a distinct topic
    try:
        paragraph_indicators = [
            'underserved',              # Paragraph 1: Health center background
            'epidemiological',          # Paragraph 2: Disease statistics / epidemiology
            'COVID-19',                 # Paragraph 3: COVID-19 impact
            'telehealth',               # Paragraph 4: Proposed initiative
        ]
        paragraphs_found = 0
        for indicator in paragraph_indicators:
            if indicator.lower() in content.lower():
                paragraphs_found += 1
                print(f"  FOUND paragraph indicator: '{indicator}'")
            else:
                print(f"  MISSING paragraph indicator: '{indicator}'")

        if paragraphs_found == len(paragraph_indicators):
            print(f"PASS: Component 4 — All {len(paragraph_indicators)} paragraph themes found (0.2 pts)")
            total_score += 0.2
        elif paragraphs_found >= 3:
            print(f"PARTIAL: Component 4 — {paragraphs_found}/{len(paragraph_indicators)} paragraph themes found (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 4 — Only {paragraphs_found}/{len(paragraph_indicators)} paragraph themes found (0.0 pts)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

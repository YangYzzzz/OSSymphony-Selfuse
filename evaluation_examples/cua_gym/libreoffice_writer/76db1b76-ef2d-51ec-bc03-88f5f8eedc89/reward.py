"""
Reward Script: Apply Heading 1 to 3 main section titles and Heading 2 to 6 subsection titles
Task ID: osworld_writer_heading_styles_002
Domain: libreoffice_writer
Scoring:
  Component 1: All 3 main section titles have Heading 1 style (0.5 pts)
  Component 2: All 6 subsection titles have Heading 2 style (0.5 pts)
  Total: 1.0
"""

import os

from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_heading_styles_002'

# Expected section titles (main) — should be Heading 1 in golden
MAIN_SECTION_TITLES = [
    'Section 1: Network Architecture Overview',
    'Section 2: Security Policies and Access Control',
    'Section 3: Incident Response and Recovery',
]

# Expected subsection titles — should be Heading 2 in golden
SUBSECTION_TITLES = [
    '1.1 Core Network Components',
    '1.2 IP Addressing and VLAN Design',
    '2.1 Authentication and Authorization',
    '2.2 Firewall and Intrusion Prevention',
    '3.1 Incident Classification and Escalation',
    '3.2 Backup and Disaster Recovery',
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.

    The task requires converting plain bold Normal-style paragraphs to
    proper heading styles: Heading 1 for main section titles (3 total)
    and Heading 2 for subsection titles (6 total).

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Build a mapping from paragraph text -> style name for all non-empty paragraphs
    para_styles = {}
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            para_styles[text] = para.style.name

    # Component 1: All 3 main section titles have Heading 1 style (0.5 points)
    # In initial_env these are Normal style with bold formatting.
    # In golden_env these must be Heading 1 style.
    try:
        h1_count = 0
        for title in MAIN_SECTION_TITLES:
            actual_style = para_styles.get(title, None)
            if actual_style == 'Heading 1':
                print(f"PASS: Main section title '{title}' has Heading 1 style")
                h1_count += 1
            else:
                print(f"FAIL: Main section title '{title}' has style '{actual_style}', expected 'Heading 1'")

        if h1_count == 3:
            print(f"PASS: Component 1 — All 3 main section titles have Heading 1 style (0.5 pts)")
            total_score += 0.5
        elif h1_count > 0:
            partial = round(h1_count / 3 * 0.5, 4)
            print(f"PARTIAL: Component 1 — {h1_count}/3 main section titles have Heading 1 style ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No main section titles have Heading 1 style (0.0 pts)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 6 subsection titles have Heading 2 style (0.5 points)
    # In initial_env these are Normal style with bold formatting.
    # In golden_env these must be Heading 2 style.
    try:
        h2_count = 0
        for title in SUBSECTION_TITLES:
            actual_style = para_styles.get(title, None)
            if actual_style == 'Heading 2':
                print(f"PASS: Subsection title '{title}' has Heading 2 style")
                h2_count += 1
            else:
                print(f"FAIL: Subsection title '{title}' has style '{actual_style}', expected 'Heading 2'")

        if h2_count == 6:
            print(f"PASS: Component 2 — All 6 subsection titles have Heading 2 style (0.5 pts)")
            total_score += 0.5
        elif h2_count > 0:
            partial = round(h2_count / 6 * 0.5, 4)
            print(f"PARTIAL: Component 2 — {h2_count}/6 subsection titles have Heading 2 style ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No subsection titles have Heading 2 style (0.0 pts)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in the VM environment
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

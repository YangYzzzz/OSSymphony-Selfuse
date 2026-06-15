"""
Reward Script: Apply bullet list formatting to first 5 paragraphs and numbered list to last 5
Task ID: writer_list_032
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): Paragraphs 1-5 (index 0-4) use 'List Bullet' style
  Component 2 (0.5): Paragraphs 6-10 (index 5-9) use 'List Number' style
"""

import os

from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_list_032'

# Expected paragraph texts (from task context, for sanity check)
EXPECTED_TEXTS = [
    "Important considerations for the project",
    "Budget constraints must be addressed early",
    "Stakeholder communication is critical",
    "Risk assessment should be ongoing",
    "Quality assurance cannot be compromised",
    "Gather requirements from all departments",
    "Create detailed design specifications",
    "Implement core features first",
    "Conduct thorough testing",
    "Deploy to production environment",
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the document
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: verify document has exactly 10 paragraphs with correct text
    paragraphs = [p for p in doc.paragraphs]
    non_empty_paragraphs = [p for p in paragraphs if p.text.strip()]

    if len(non_empty_paragraphs) != 10:
        print(f"PRECONDITION FAIL: Expected 10 non-empty paragraphs, found {len(non_empty_paragraphs)}")
        print("REWARD: 0.0")
        return 0.0

    # Use first 10 non-empty paragraphs for verification
    target_paragraphs = non_empty_paragraphs[:10]

    # Component 1: Paragraphs 1-5 (index 0-4) should use 'List Bullet' style (0.5 points)
    try:
        bullet_paras = target_paragraphs[:5]
        bullet_pass_count = 0
        bullet_failures = []

        for i, para in enumerate(bullet_paras):
            style_name = para.style.name
            if style_name == 'List Bullet':
                bullet_pass_count += 1
            else:
                bullet_failures.append(f"Para {i+1} ('{para.text[:30]}...'): expected 'List Bullet', found '{style_name}'")

        if bullet_pass_count == 5:
            print(f"PASS: Component 1 — All 5 first paragraphs use 'List Bullet' style (0.5 pts)")
            total_score += 0.5
        elif bullet_pass_count > 0:
            partial = round(0.5 * bullet_pass_count / 5, 2)
            print(f"PARTIAL: Component 1 — {bullet_pass_count}/5 first paragraphs use 'List Bullet' style ({partial} pts)")
            print(f"  Failures: {bullet_failures}")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No paragraphs in 1-5 use 'List Bullet' style")
            print(f"  Failures: {bullet_failures}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Paragraphs 6-10 (index 5-9) should use 'List Number' style (0.5 points)
    try:
        number_paras = target_paragraphs[5:]
        number_pass_count = 0
        number_failures = []

        for i, para in enumerate(number_paras):
            style_name = para.style.name
            if style_name == 'List Number':
                number_pass_count += 1
            else:
                number_failures.append(f"Para {i+6} ('{para.text[:30]}...'): expected 'List Number', found '{style_name}'")

        if number_pass_count == 5:
            print(f"PASS: Component 2 — All 5 last paragraphs use 'List Number' style (0.5 pts)")
            total_score += 0.5
        elif number_pass_count > 0:
            partial = round(0.5 * number_pass_count / 5, 2)
            print(f"PARTIAL: Component 2 — {number_pass_count}/5 last paragraphs use 'List Number' style ({partial} pts)")
            print(f"  Failures: {number_failures}")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No paragraphs in 6-10 use 'List Number' style")
            print(f"  Failures: {number_failures}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

"""
Reward Script: Clean employee skills inventory by removing duplicate skill entries
Task ID: osworld_writer_duplicate_line_removal_006
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.5 pts): Correct skill entry count (13 unique skills, down from 20)
  - Component 2 (0.3 pts): No duplicate skill entries remain
  - Component 3 (0.2 pts): Skills appear in correct first-occurrence order
"""

import os

from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_duplicate_line_removal_006'

# Expected unique skills in first-occurrence order (derived from task description and initial doc)
EXPECTED_SKILLS = [
    'Python Programming',
    'Data Analysis',
    'Project Management',
    'SQL Database Management',
    'Machine Learning',
    'Communication Skills',
    'Team Leadership',
    'Cloud Computing (AWS)',
    'JavaScript Development',
    'Financial Reporting',
    'Problem Solving',
    'Agile Methodology',
    'Customer Relations',
]

# The number of non-skill header paragraphs before the skill list begins
# (Heading 1 title, Normal description, Heading 2 section header)
HEADER_PARA_COUNT = 3


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract skill entries (paragraphs after the header section)
    # The document has: Heading1, Normal (description), Heading2, then skill paragraphs
    all_paras = doc.paragraphs
    skill_paras = all_paras[HEADER_PARA_COUNT:]
    skill_texts = [p.text.strip() for p in skill_paras if p.text.strip()]

    print(f"INFO: Total paragraphs in document: {len(all_paras)}")
    print(f"INFO: Skill entries found: {len(skill_texts)}")
    print(f"INFO: Skill entries: {skill_texts}")

    # Component 1: Correct number of skill entries — exactly 13 unique skills (0.5 points)
    # Initial env has 20 skills with duplicates; golden should have 13 unique ones.
    # This check FAILS on initial (20 != 13) and PASSES on golden (13 == 13).
    try:
        expected_count = len(EXPECTED_SKILLS)  # 13
        actual_count = len(skill_texts)
        if actual_count == expected_count:
            print(f"PASS: Component 1 — skill count is {actual_count} (expected {expected_count}) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — expected {expected_count} skill entries, found {actual_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: No duplicate skill entries remain (0.3 points)
    # Initial env has 7 duplicated skills; golden should have no duplicates.
    # This check FAILS on initial (duplicates exist) and PASSES on golden (no duplicates).
    try:
        unique_skills = list(dict.fromkeys(skill_texts))  # preserve order, deduplicate
        has_no_duplicates = len(skill_texts) == len(set(skill_texts))
        if has_no_duplicates:
            print(f"PASS: Component 2 — no duplicate skills found ({len(skill_texts)} entries, all unique) (0.3 pts)")
            total_score += 0.3
        else:
            duplicates = [s for s in skill_texts if skill_texts.count(s) > 1]
            dupes_unique = list(set(duplicates))
            print(f"FAIL: Component 2 — duplicate skills still present: {dupes_unique}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Skills appear in correct first-occurrence order (0.2 points)
    # Verifies the skills match the expected list exactly in order.
    # This check FAILS on initial (wrong entries/order) and PASSES on golden.
    try:
        if skill_texts == EXPECTED_SKILLS:
            print(f"PASS: Component 3 — skills are in correct first-occurrence order (0.2 pts)")
            total_score += 0.2
        else:
            # Compute difference for useful debug output
            mismatches = []
            for i, (expected, actual) in enumerate(zip(EXPECTED_SKILLS, skill_texts)):
                if expected != actual:
                    mismatches.append(f"  pos {i+1}: expected={repr(expected)}, actual={repr(actual)}")
            extra = skill_texts[len(EXPECTED_SKILLS):]
            missing = EXPECTED_SKILLS[len(skill_texts):]
            msg = f"FAIL: Component 3 — skill order/content does not match expected list"
            if mismatches:
                msg += f"\n  Mismatches: {'; '.join(mismatches)}"
            if extra:
                msg += f"\n  Extra skills in doc: {extra}"
            if missing:
                msg += f"\n  Missing skills: {missing}"
            print(msg)
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in the VM
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

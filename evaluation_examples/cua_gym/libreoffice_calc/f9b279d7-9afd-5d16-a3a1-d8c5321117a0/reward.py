"""
Reward Script: Extract text from research_paper.pdf to research_paper_text.txt
Task ID: pdf_gf1_016
Domain: libreoffice_calc (actually PDF text extraction)
Scoring:
  Component 1: Output file exists and is non-empty (>= 2000 chars) — 0.20 pts
  Component 2: Contains key section headings (Abstract, References) — 0.20 pts
  Component 3: Paragraph breaks (double newlines) present — 0.20 pts
  Component 4: Valid UTF-8 encoding and no binary garbage characters — 0.20 pts
  Component 5: Sufficient content coverage (Introduction, Methods, Results, Discussion) — 0.20 pts
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf1_016'

OUTPUT_PATH = os.path.join(WORKDIR, 'Documents', 'research_paper_text.txt')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: output file must exist
    if not os.path.exists(OUTPUT_PATH):
        print(f"CRITICAL: Output file not found: {OUTPUT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Read the file content
    try:
        with open(OUTPUT_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        print("CRITICAL: File is not valid UTF-8 encoded")
        print("REWARD: 0.0")
        return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot read output file: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: File is non-empty and has sufficient content (>= 2000 chars) (0.20 points)
    # This checks that meaningful text was extracted, not just a stub file.
    # FAILS on initial_env because the file does not exist (caught above).
    try:
        char_count = len(content)
        if char_count >= 2000:
            print(f"PASS: Component 1 — File has {char_count} characters (>= 2000 required) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — File has only {char_count} characters (need >= 2000)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Contains key section headings 'Abstract' and 'References' (0.20 points)
    # These are the required section headings per ground truth.
    # FAILS on initial_env because the file does not exist.
    try:
        has_abstract = 'Abstract' in content
        has_references = 'References' in content
        if has_abstract and has_references:
            print(f"PASS: Component 2 — Found 'Abstract' and 'References' headings (0.20 pts)")
            total_score += 0.20
        else:
            missing = []
            if not has_abstract:
                missing.append('Abstract')
            if not has_references:
                missing.append('References')
            print(f"FAIL: Component 2 — Missing section headings: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Paragraph breaks (double newlines) present (0.20 points)
    # Task requires preserving paragraph structure with blank lines between paragraphs.
    # FAILS on initial_env because the file does not exist.
    try:
        double_newline_count = content.count('\n\n')
        if double_newline_count >= 5:
            print(f"PASS: Component 3 — Found {double_newline_count} paragraph breaks (double newlines) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Only {double_newline_count} paragraph breaks found (need >= 5)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: No binary garbage characters (0.20 points)
    # Task says output should be clean text without binary garbage.
    # FAILS on initial_env because the file does not exist.
    try:
        # Check for control characters (excluding \t, \n, \r which are normal text)
        binary_chars = re.findall(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', content)
        if len(binary_chars) == 0:
            print(f"PASS: Component 4 — No binary garbage characters found (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — Found {len(binary_chars)} binary garbage characters")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Sufficient content coverage — multiple sections present (0.20 points)
    # Ground truth says paper has: Abstract, Introduction, Methods, Results, Discussion, References
    # We require at least 4 of the 6 sections (besides Abstract and References already checked).
    # FAILS on initial_env because the file does not exist.
    try:
        sections = ['Abstract', 'Introduction', 'Methods', 'Results', 'Discussion', 'References']
        found_sections = [s for s in sections if s in content]
        if len(found_sections) >= 4:
            print(f"PASS: Component 5 — Found {len(found_sections)}/6 sections: {', '.join(found_sections)} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 5 — Only found {len(found_sections)}/6 sections: {', '.join(found_sections)} (need >= 4)")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

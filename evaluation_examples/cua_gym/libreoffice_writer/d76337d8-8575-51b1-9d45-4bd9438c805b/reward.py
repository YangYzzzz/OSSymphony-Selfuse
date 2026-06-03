"""
Reward Script: Use regex Find & Replace to wrap all standalone numbers with square brackets
Task ID: writer_edit_047
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.6): All standalone integers are wrapped in [N] format (59 total),
                        and no unbracketed standalone numbers remain
  - Component 2 (0.2): Numbers embedded in words (H2O, F16, B2O3) are NOT wrapped
                        (only awarded if Component 1 passes — confirms correct regex was used)
  - Component 3 (0.2): Spot-check key sentences for exact expected bracket format
"""

import os
import re

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_edit_047'
FILE_PATH = f'{WORKDIR}/data_report.docx'


def get_all_text(doc):
    """Extract all paragraph texts as a list."""
    return [para.text for para in doc.paragraphs]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    comp1_passed = False

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    texts = get_all_text(doc)
    full_text = '\n'.join(texts)

    # Component 1: All standalone integers are wrapped in [N] format (0.6 points)
    # Task: regex Find & Replace with pattern \b(\d+)\b → [$1]
    # This means every standalone number should appear as [number] in golden
    # and there should be NO bare standalone integers left (except those within words)
    try:
        # Count bracketed integers: [N] pattern
        bracketed = re.findall(r'\[\d+\]', full_text)
        # Count unbracketed standalone integers (not part of a word, not already in brackets)
        # \b\d+\b that is NOT preceded by [ or followed by ]
        unbracketed_standalone = re.findall(r'(?<!\[)\b\d+\b(?!\])', full_text)

        expected_bracketed_count = 59  # from golden state analysis

        if len(bracketed) == expected_bracketed_count and len(unbracketed_standalone) == 0:
            print(f"PASS: Component 1 — All {len(bracketed)} standalone numbers are wrapped in brackets, "
                  f"0 unbracketed standalone numbers remain. (0.6 pts)")
            total_score += 0.6
            comp1_passed = True
        elif len(bracketed) > 0 and len(unbracketed_standalone) == 0:
            # All found standalone numbers are bracketed, but count differs from expected
            print(f"PARTIAL: Component 1 — {len(bracketed)} bracketed numbers found (expected {expected_bracketed_count}), "
                  f"0 unbracketed. Awarding partial credit. (0.3 pts)")
            total_score += 0.3
            comp1_passed = True
        elif len(bracketed) > 0 and len(unbracketed_standalone) > 0:
            ratio = len(bracketed) / (len(bracketed) + len(unbracketed_standalone))
            print(f"PARTIAL: Component 1 — {len(bracketed)} bracketed, {len(unbracketed_standalone)} unbracketed standalone. "
                  f"ratio={ratio:.2f}")
            if ratio >= 0.5:
                print(f"PARTIAL: Component 1 — majority bracketed (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 1 — Minority bracketed.")
            print(f"FAIL: Component 1 — Unbracketed examples: {unbracketed_standalone[:5]}")
        else:
            print(f"FAIL: Component 1 — No bracketed numbers found. "
                  f"Unbracketed standalone: {len(unbracketed_standalone)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Numbers within alphanumeric words (H2O, F16, B2O3) are NOT modified (0.2 points)
    # This component is ONLY awarded if Component 1 passed (all standalones bracketed),
    # which distinguishes a correct regex (\b\d+\b) from an incorrect one that wraps all digits.
    # On initial_env, Component 1 always fails (no brackets), so this component never awards on initial.
    try:
        if comp1_passed:
            preserved_tokens = ['H2O', 'F16', 'B2O3']
            preserved_ok = True
            for token in preserved_tokens:
                if token not in full_text:
                    print(f"FAIL: Component 2 — Token '{token}' not found (may have been modified)")
                    preserved_ok = False
                else:
                    # Verify the token is NOT like H[2]O or F[16] etc.
                    broken = False
                    if token == 'H2O' and 'H[2]O' in full_text:
                        broken = True
                    if token == 'F16' and 'F[16]' in full_text:
                        broken = True
                    if token == 'B2O3' and ('B[2]O3' in full_text or 'B2O[3]' in full_text):
                        broken = True
                    if broken:
                        print(f"FAIL: Component 2 — Token '{token}' was incorrectly modified")
                        preserved_ok = False

            if preserved_ok:
                print(f"PASS: Component 2 — All embedded-number tokens (H2O, F16, B2O3) preserved intact. (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2 — Some embedded-number tokens were incorrectly modified.")
        else:
            print(f"SKIP: Component 2 — Component 1 not passed; skipping word-boundary preservation check.")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Spot-check key sentences match the expected bracketed format (0.2 points)
    # Verify specific known sentences from the task context
    try:
        expected_sentences = [
            'There were [42] participants',
            'The cost was [150] dollars',
            'Section [3] covers',
            'Response rates improved by [18] percentage points',
            'with [312] valid submissions received out of [350] distributed',
        ]
        passed_count = 0
        for expected in expected_sentences:
            if expected in full_text:
                passed_count += 1
            else:
                print(f"FAIL: Component 3 — Expected phrase not found: '{expected}'")

        if passed_count == len(expected_sentences):
            print(f"PASS: Component 3 — All {passed_count}/{len(expected_sentences)} spot-check phrases found. (0.2 pts)")
            total_score += 0.2
        elif passed_count >= 3:
            print(f"PARTIAL: Component 3 — {passed_count}/{len(expected_sentences)} spot-check phrases found. (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 3 — Only {passed_count}/{len(expected_sentences)} spot-check phrases found.")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

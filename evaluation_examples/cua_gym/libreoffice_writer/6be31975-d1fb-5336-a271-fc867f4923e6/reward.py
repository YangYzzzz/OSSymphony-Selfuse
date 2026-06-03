"""
Reward Script: Deduplicate library borrowing log ISBNs
Task ID: osworld_writer_dedup_009
Domain: libreoffice_writer
Scoring:
  Component 1: No duplicate ISBNs in the document (each ISBN appears exactly once) — 0.5 pts
  Component 2: Exact unique count of 35 ISBNs — 0.2 pts
  Component 3: First-occurrence order maintained (matches order ISBNs first appeared in the original log) — 0.3 pts
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_dedup_009'

# Ground truth: first-occurrence ordered unique ISBNs from the original log
# These are the 35 unique ISBNs in the order they first appeared in the initial 246-line borrow log.
EXPECTED_UNIQUE_ISBNS = [
    'ISBN-978-0-062-98659-2',
    'ISBN-978-0-061-96436-9',
    'ISBN-978-0-316-76948-0',
    'ISBN-978-0-735-21500-4',
    'ISBN-978-0-385-54754-2',
    'ISBN-978-0-385-54734-4',
    'ISBN-978-0-062-31609-7',
    'ISBN-978-0-062-96173-5',
    'ISBN-978-1-982-10891-7',
    'ISBN-978-1-982-13526-5',
    'ISBN-978-0-593-31012-3',
    'ISBN-978-1-982-10793-4',
    'ISBN-978-0-307-47441-4',
    'ISBN-978-0-385-53764-2',
    'ISBN-978-0-316-31609-6',
    'ISBN-978-0-385-49031-1',
    'ISBN-978-1-250-30185-3',
    'ISBN-978-1-982-11238-9',
    'ISBN-978-0-735-22447-1',
    'ISBN-978-0-062-69021-5',
    'ISBN-978-1-250-62233-4',
    'ISBN-978-1-501-15643-9',
    'ISBN-978-0-525-55360-5',
    'ISBN-978-0-316-17922-7',
    'ISBN-978-0-525-51916-8',
    'ISBN-978-0-385-33348-1',
    'ISBN-978-0-525-55946-1',
    'ISBN-978-0-593-18896-3',
    'ISBN-978-0-062-89418-4',
    'ISBN-978-0-743-27356-5',
    'ISBN-978-1-250-17788-8',
    'ISBN-978-0-316-45691-3',
    'ISBN-978-1-250-79097-2',
    'ISBN-978-0-593-08924-7',
    'ISBN-978-0-385-54585-2',
]

EXPECTED_UNIQUE_COUNT = 35


def verify_task(file_path):
    """
    Verify task completion: library borrowing log has been deduplicated.
    The task requires:
      - All duplicate ISBN lines removed
      - Each unique ISBN appears exactly once
      - First-occurrence order maintained (35 unique ISBNs in original order)
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must be loadable
    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract all non-empty lines (paragraph texts) from the document
    try:
        lines = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        print(f"INFO: Document has {len(lines)} non-empty lines")
    except Exception as e:
        print(f"CRITICAL: Cannot read paragraphs: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: No duplicate ISBNs — each ISBN appears exactly once (0.5 points)
    # This FAILS on initial_env (246 lines with heavy duplicates) and PASSES on golden_env (35 unique lines)
    try:
        unique_lines = list(dict.fromkeys(lines))
        has_duplicates = len(lines) != len(unique_lines)
        all_isbn_format = all(line.startswith('ISBN-') for line in lines) if lines else False

        if not has_duplicates and all_isbn_format and len(lines) > 0:
            print(f"PASS: Component 1 — No duplicates detected. All {len(lines)} lines are unique ISBN entries (0.5 pts)")
            total_score += 0.5
        elif has_duplicates:
            print(f"FAIL: Component 1 — Document still has duplicates. {len(lines)} total lines, {len(unique_lines)} unique. Duplicates count: {len(lines) - len(unique_lines)}")
        else:
            print(f"FAIL: Component 1 — Lines do not match expected ISBN format or document is empty. Lines: {lines[:3]}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Exact unique count of 35 ISBNs (0.2 points)
    # The original log had exactly 35 distinct books. After dedup the document must have exactly 35 lines.
    # This FAILS on initial_env (246 lines) and PASSES on golden_env (35 lines).
    try:
        if len(lines) == EXPECTED_UNIQUE_COUNT:
            print(f"PASS: Component 2 — Exactly {EXPECTED_UNIQUE_COUNT} unique ISBNs in document (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — Expected {EXPECTED_UNIQUE_COUNT} lines, found {len(lines)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: First-occurrence order maintained (0.3 points)
    # The task specifies "First occurrence order maintained". The golden file preserves the
    # order in which ISBNs first appeared in the original chronological borrow log.
    # This FAILS on initial_env (246 lines, wrong count/order) and PASSES on golden_env.
    try:
        if lines == EXPECTED_UNIQUE_ISBNS:
            print(f"PASS: Component 3 — ISBNs are in correct first-occurrence order (0.3 pts)")
            total_score += 0.3
        else:
            # Provide informative diff for debugging
            mismatches = []
            for i, (expected, actual) in enumerate(zip(EXPECTED_UNIQUE_ISBNS, lines)):
                if expected != actual:
                    mismatches.append(f"  Position {i+1}: expected '{expected}', found '{actual}'")
                if len(mismatches) >= 3:
                    break
            if len(lines) != len(EXPECTED_UNIQUE_ISBNS):
                print(f"FAIL: Component 3 — Wrong number of lines ({len(lines)} vs {len(EXPECTED_UNIQUE_ISBNS)} expected), cannot verify order")
            elif mismatches:
                print(f"FAIL: Component 3 — Order mismatch. First {len(mismatches)} differences:")
                for m in mismatches:
                    print(m)
            else:
                print(f"FAIL: Component 3 — Lists differ in content despite same length")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against the canonical artifact path on the VM
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

"""
Reward Script: PDF text replacement tool verification
Task ID: pdf_gf3_044
Domain: pdf
Scoring:
  C1 (0.15): Script exists and is valid Python
  C2 (0.15): replaced.pdf exists, is valid PDF with 10 pages
  C3 (0.30): All 5 replacement texts present in replaced.pdf
  C4 (0.25): None of the 5 original search texts remain in replaced.pdf
  C5 (0.15): original.pdf is still intact (same page count, has original text)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_044'

SCRIPT_PATH = f'{WORKDIR}/scripts/pdf_find_replace.py'
REPLACED_PATH = f'{WORKDIR}/docs/replaced.pdf'
ORIGINAL_PATH = f'{WORKDIR}/docs/original.pdf'
PATTERNS_PATH = f'{WORKDIR}/config/replace_patterns.json'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load patterns config for reference
    try:
        with open(PATTERNS_PATH, 'r') as f:
            patterns = json.load(f)
        print(f"INFO: Loaded {len(patterns)} replacement patterns")
    except Exception as e:
        print(f"ERROR: Cannot load patterns config: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Script exists and is valid Python (0.15 points)
    try:
        if os.path.exists(SCRIPT_PATH):
            # Check it's valid Python by compiling it
            with open(SCRIPT_PATH, 'r') as f:
                source = f.read()
            compile(source, SCRIPT_PATH, 'exec')
            if len(source) > 50:  # non-trivial script
                print(f"PASS: Component 1 — Script exists and is valid Python ({len(source)} bytes) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — Script too small ({len(source)} bytes), likely placeholder")
        else:
            print(f"FAIL: Component 1 — Script not found at {SCRIPT_PATH}")
    except SyntaxError as e:
        print(f"FAIL: Component 1 — Script has syntax errors: {e}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: replaced.pdf exists, is valid PDF with 10 pages (0.15 points)
    try:
        import pymupdf
        if os.path.exists(REPLACED_PATH):
            doc = pymupdf.open(REPLACED_PATH)
            page_count = doc.page_count
            doc.close()
            if page_count == 10:
                print(f"PASS: Component 2 — replaced.pdf exists with {page_count} pages (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 — replaced.pdf has {page_count} pages, expected 10")
        else:
            print(f"FAIL: Component 2 — replaced.pdf not found at {REPLACED_PATH}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Extract full text from replaced.pdf for Components 3 and 4
    replaced_text = ""
    try:
        import pymupdf
        if os.path.exists(REPLACED_PATH):
            doc = pymupdf.open(REPLACED_PATH)
            for page in doc:
                replaced_text += page.get_text("text")
            doc.close()
    except Exception as e:
        print(f"ERROR: Could not extract text from replaced.pdf: {e}")

    # Component 3: All 5 replacement texts present in replaced.pdf (0.30 points)
    # Each replacement found earns 0.06 points
    try:
        if replaced_text:
            found_count = 0
            for p in patterns:
                replace_text = p['replace']
                if replace_text in replaced_text:
                    found_count += 1
                    print(f"  PASS: Replacement text '{replace_text}' found in replaced.pdf")
                else:
                    print(f"  FAIL: Replacement text '{replace_text}' NOT found in replaced.pdf")
            pts = round(found_count * 0.06, 2)
            if found_count == len(patterns):
                print(f"PASS: Component 3 — All {found_count}/{len(patterns)} replacement texts present ({pts} pts)")
                total_score += pts
            elif found_count > 0:
                print(f"PARTIAL: Component 3 — {found_count}/{len(patterns)} replacement texts present ({pts} pts)")
                total_score += pts
            else:
                print(f"FAIL: Component 3 — 0/{len(patterns)} replacement texts present")
        else:
            print(f"FAIL: Component 3 — No text extracted from replaced.pdf (file missing or empty)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: None of the original search texts remain in replaced.pdf (0.25 points)
    # Each fully removed pattern earns 0.05 points
    try:
        if replaced_text:
            removed_count = 0
            for p in patterns:
                search_pattern = p['search']
                # Use regex matching since search patterns are regex
                matches = re.findall(search_pattern, replaced_text)
                if not matches:
                    removed_count += 1
                    print(f"  PASS: Original text matching '{search_pattern}' fully removed")
                else:
                    print(f"  FAIL: Original text matching '{search_pattern}' still present ({len(matches)} occurrences)")
            pts = round(removed_count * 0.05, 2)
            if removed_count == len(patterns):
                print(f"PASS: Component 4 — All {removed_count}/{len(patterns)} original texts removed ({pts} pts)")
                total_score += pts
            elif removed_count > 0:
                print(f"PARTIAL: Component 4 — {removed_count}/{len(patterns)} original texts removed ({pts} pts)")
                total_score += pts
            else:
                print(f"FAIL: Component 4 — 0/{len(patterns)} original texts removed")
        else:
            print(f"FAIL: Component 4 — No text extracted from replaced.pdf (file missing or empty)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: original.pdf is still intact (0.15 points)
    # Verify original.pdf hasn't been corrupted — still has 10 pages and contains
    # original text (e.g. "Nexora Technologies"). This is a compound check:
    # we only award points if the REPLACED PDF also exists (i.e., this check gates on
    # task completion to avoid scoring a precondition alone).
    try:
        import pymupdf
        if os.path.exists(REPLACED_PATH) and os.path.exists(ORIGINAL_PATH):
            doc = pymupdf.open(ORIGINAL_PATH)
            orig_pages = doc.page_count
            orig_text = ""
            for page in doc:
                orig_text += page.get_text("text")
            doc.close()
            if orig_pages == 10 and "Nexora Technologies" in orig_text:
                print(f"PASS: Component 5 — original.pdf intact (10 pages, original text present) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 — original.pdf may be corrupted (pages={orig_pages})")
        else:
            if not os.path.exists(REPLACED_PATH):
                print(f"FAIL: Component 5 — Skipped (replaced.pdf does not exist, task not attempted)")
            else:
                print(f"FAIL: Component 5 — original.pdf not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

"""
Reward Script: Convert all fully uppercase words (3+ letters) to title case
Task ID: writer_af_043
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): No uppercase words (3+ letters) remain in the document
  Component 2 (0.3): Known uppercase words appear as title case AND non-uppercase text preserved
  Component 3 (0.2): Conversion is complete — at least 60 distinct words converted AND short acronyms preserved
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_af_043'

# Known uppercase words from the initial document (3+ letters).
KNOWN_UPPERCASE_WORDS = {
    'PERFORMANCE', 'DEPARTMENT', 'OPERATIONS', 'ASSESSMENT', 'MANAGEMENT',
    'SUMMARY', 'ANALYSIS', 'COMMITTEE', 'LEADERSHIP', 'REVENUE', 'EMPLOYEE',
    'EFFICIENCY', 'EXPANSION', 'OVERVIEW', 'FINANCE', 'QUARTER', 'BUDGET',
    'MARKETING', 'SEGMENT', 'LOGISTICS', 'OPTIMIZATION', 'WAREHOUSE',
    'INVENTORY', 'ALGORITHMS', 'TRANSPORTATION', 'RESOURCES', 'RECRUITMENT',
    'COMPLIANCE', 'SATISFACTION', 'COMPENSATION', 'BENEFITS', 'RETENTION',
    'TECHNOLOGY', 'INNOVATION', 'ENGINEERING', 'CYBERSECURITY', 'ARCHITECTURE',
    'DEVELOPMENT', 'IMPLEMENTATION', 'INTEGRATION', 'CRM', 'OUTLOOK',
    'EXECUTIVE', 'CONSOLIDATION', 'ACCELERATION', 'INVESTMENT', 'PARTNERSHIP',
    'DISTRIBUTION', 'NEGOTIATION', 'ACQUISITION', 'DILIGENCE', 'CONCLUSION',
    'RECOMMENDATIONS', 'MOMENTUM', 'ORGANIZATION', 'OBJECTIVES',
    'CONSIDERATION', 'ALLOCATION', 'MIGRATION', 'ERP', 'COLLABORATION',
    'GOVERNANCE', 'DOCUMENTATION', 'CERTIFICATION', 'ISO', 'REGULATORY',
    'MONITORING', 'SURVEILLANCE', 'PROCUREMENT', 'STAKEHOLDERS',
    'ADVERTISING', 'EXPECTATIONS', 'AWARENESS', 'STRATEGY', 'ENGAGEMENT',
    'COMMUNICATIONS', 'NEWSLETTER', 'COVERAGE', 'BRANDING',
}


def persist_app_state():
    """Save any unsaved LibreOffice changes via Ctrl+S."""
    try:
        os.environ["DISPLAY"] = ":0"
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        import time
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    all_texts = [para.text for para in doc.paragraphs]
    full_text = '\n'.join(all_texts)

    # Pre-compute shared data
    uppercase_words_found = re.findall(r'\b[A-Z]{3,}\b', full_text)
    title_case_words_in_doc = set(re.findall(r'\b[A-Z][a-z]{2,}\b', full_text))
    expected_title = {w.title() for w in KNOWN_UPPERCASE_WORDS}

    # Component 1: No uppercase words (3+ letters) remain (0.5 points)
    # INITIAL: 97 uppercase words -> FAIL
    # GOLDEN: 0 uppercase words -> PASS
    try:
        if len(uppercase_words_found) == 0:
            print(f"PASS: Component 1 — No uppercase words (3+ letters) remain (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — Found {len(uppercase_words_found)} uppercase words: {uppercase_words_found[:10]}...")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Known uppercase words are now in title case AND text integrity (0.3 points)
    # Both sub-conditions must pass: the uppercase words must be converted to title case,
    # AND the rest of the text must be preserved. This ensures this component only passes
    # when the conversion actually happened (fails on initial because conversion hasn't happened).
    # INITIAL: uppercase words are still uppercase, not title case -> distinct_found < 30 -> FAIL
    # GOLDEN: uppercase words are now title case -> distinct_found >= 30 -> PASS
    try:
        distinct_found = expected_title.intersection(title_case_words_in_doc)

        # Also verify non-uppercase text is preserved (sub-condition, not standalone score)
        expected_preserved = [
            'Quarterly', 'Review', 'Report', 'Strategic', 'Fiscal', 'Year',
            'Prepared', 'Team', 'comprehensive', 'overall', 'conducted',
        ]
        preserved_count = sum(1 for w in expected_preserved if w in full_text)
        text_intact = preserved_count >= len(expected_preserved) - 2

        if len(distinct_found) >= 30 and text_intact:
            print(f"PASS: Component 2 — {len(distinct_found)} words converted to title case, text intact ({preserved_count}/{len(expected_preserved)}) (0.3 pts)")
            total_score += 0.3
        elif len(distinct_found) >= 15 and text_intact:
            print(f"PARTIAL: Component 2 — {len(distinct_found)} words converted, text intact (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — {len(distinct_found)} words in title case, text preserved: {preserved_count}/{len(expected_preserved)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Completeness — high coverage of conversions AND short acronyms preserved (0.2 points)
    # This checks that the conversion is thorough (at least 60 distinct words) and that
    # short acronyms (IT, AI) were correctly left untouched.
    # INITIAL: uppercase words haven't been converted -> distinct_found < 60 -> FAIL
    # GOLDEN: all 79 words converted -> PASS
    try:
        # Re-use distinct_found from Component 2
        has_it = bool(re.search(r'\bIT\b', full_text))
        has_ai = bool(re.search(r'\bAI\b', full_text))
        acronyms_ok = has_it and has_ai

        if len(distinct_found) >= 60 and acronyms_ok:
            print(f"PASS: Component 3 — {len(distinct_found)} distinct words converted, IT/AI preserved (0.2 pts)")
            total_score += 0.2
        elif len(distinct_found) >= 60:
            print(f"PARTIAL: Component 3 — {len(distinct_found)} words converted but acronyms not all preserved (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 3 — Only {len(distinct_found)} distinct words converted (need >= 60), IT={has_it}, AI={has_ai}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist any unsaved state before verifying
persist_app_state()

# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

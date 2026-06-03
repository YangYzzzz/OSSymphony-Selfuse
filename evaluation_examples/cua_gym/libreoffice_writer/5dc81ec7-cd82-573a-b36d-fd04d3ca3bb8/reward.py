"""
Reward Script: Add empty line after each sentence in the third paragraph of legal_clauses.docx
Task ID: osworld_writer_spacing_003
Domain: libreoffice_writer
Scoring:
  Component 1 (0.50): 10 clause paragraphs each containing exactly one sentence ending with a period
  Component 2 (0.30): 9 empty separator paragraphs between clause paragraphs (alternating pattern)
  Component 3 (0.20): Other sections (intro, sections 1, 3, 4) remain unchanged
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_spacing_003'

# Ground-truth sentences from the third section (Section 2: General Terms and Conditions)
EXPECTED_CLAUSES = [
    "The contractor shall complete all work by the specified deadline.",
    "Payment will be made in 30-day installments upon receipt of invoice.",
    "Either party may terminate this agreement with 30 days written notice.",
    "All intellectual property developed under this agreement belongs to the client.",
    "The service provider shall maintain confidentiality of all proprietary information.",
    "Disputes shall be resolved through binding arbitration in the state of Delaware.",
    "The service provider shall carry professional liability insurance of no less than $2,000,000.",
    "Work product must meet the quality standards specified in Exhibit A attached hereto.",
    "The service provider may engage approved subcontractors with prior written consent.",
    "This agreement shall be governed by and construed in accordance with applicable law.",
]

# Other sections' content (precondition check only - NOT scored)
SECTION2_HEADING_EXPECTED = "SECTION 2: GENERAL TERMS AND CONDITIONS"
SECTION3_HEADING_EXPECTED = "SECTION 3: PAYMENT TERMS"


def persist_app_state():
    """Best-effort save in case LibreOffice has unsaved edits in memory."""
    try:
        import time
        os.environ["DISPLAY"] = ":0"
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
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
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paragraphs = doc.paragraphs

    # Precondition gate: find the index of SECTION 2 heading
    section2_idx = None
    section3_idx = None
    for i, para in enumerate(paragraphs):
        if para.text.strip() == SECTION2_HEADING_EXPECTED:
            section2_idx = i
        if para.text.strip() == SECTION3_HEADING_EXPECTED:
            section3_idx = i

    if section2_idx is None or section3_idx is None:
        print(f"CRITICAL: Could not find section headings. section2_idx={section2_idx}, section3_idx={section3_idx}")
        print("REWARD: 0.0")
        return 0.0

    # Extract all paragraphs between SECTION 2 heading and SECTION 3 heading
    section2_body = paragraphs[section2_idx + 1 : section3_idx]
    print(f"INFO: Section 2 body has {len(section2_body)} paragraphs (indices {section2_idx+1} to {section3_idx-1})")

    # Component 1: 10 clause paragraphs each containing exactly one expected sentence (0.50 points)
    # Each clause paragraph must be non-empty, end with a period, and match one of the expected clauses
    try:
        # Extract non-empty paragraphs from section 2 body
        clause_paras = [p for p in section2_body if p.text.strip()]
        print(f"INFO: Found {len(clause_paras)} non-empty paragraphs in section 2 body")

        if len(clause_paras) == 10:
            # Check each clause paragraph matches an expected sentence
            clause_texts = [p.text.strip() for p in clause_paras]
            matched = 0
            for ct in clause_texts:
                if ct in EXPECTED_CLAUSES:
                    matched += 1
                else:
                    print(f"FAIL: Clause paragraph not in expected set: {repr(ct[:80])}")

            if matched == 10:
                print(f"PASS: Component 1 — 10 clause paragraphs, all matching expected sentences (0.50 pts)")
                total_score += 0.50
            else:
                print(f"FAIL: Component 1 — {matched}/10 clause paragraphs matched expected sentences")
        else:
            print(f"FAIL: Component 1 — expected 10 non-empty clause paragraphs, found {len(clause_paras)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 9 empty separator paragraphs between clauses, alternating pattern (0.30 points)
    # Pattern should be: clause, empty, clause, empty, ..., clause (10 clauses, 9 empties = 19 total)
    try:
        if len(section2_body) == 19:
            # Verify alternating pattern: even indices = non-empty (clauses), odd indices = empty
            pattern_ok = True
            for i, para in enumerate(section2_body):
                if i % 2 == 0:  # should be a clause
                    if not para.text.strip():
                        print(f"FAIL: Component 2 — expected clause at position {i}, found empty paragraph")
                        pattern_ok = False
                        break
                else:  # should be empty
                    if para.text.strip():
                        print(f"FAIL: Component 2 — expected empty paragraph at position {i}, found: {repr(para.text[:50])}")
                        pattern_ok = False
                        break

            if pattern_ok:
                print(f"PASS: Component 2 — 19 paragraphs in section 2 body with correct alternating clause/empty pattern (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 2 — alternating pattern check failed")
        else:
            print(f"FAIL: Component 2 — expected 19 paragraphs in section 2 body (10 clauses + 9 empties), found {len(section2_body)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The original single-block paragraph with all 10 clauses is no longer present (0.20 points)
    # In the initial state, all 10 clauses are in a single paragraph.
    # After the task is done, no paragraph should contain multiple clause sentences concatenated.
    # Specifically: the section 2 body must NOT contain any single paragraph with 2 or more clause sentences.
    try:
        # Collect all clause sentences that appear together in one paragraph (indicating the block was NOT split)
        multi_clause_para_found = False
        for para in section2_body:
            text = para.text.strip()
            if not text:
                continue
            # Count how many expected clauses are present in this paragraph's text
            # If 2 or more clauses are in the same paragraph, it indicates the block was not properly split
            clauses_in_para = sum(1 for clause in EXPECTED_CLAUSES if clause in text)
            if clauses_in_para >= 2:
                print(f"FAIL: Component 3 — paragraph still contains {clauses_in_para} merged clauses: {repr(text[:80])}")
                multi_clause_para_found = True
                break

        if not multi_clause_para_found:
            print(f"PASS: Component 3 — no paragraph contains multiple merged clauses; original single block is gone (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — original merged-clause paragraph still present")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in a given env
file_path = f'{WORKDIR}/{TASK_ID}.docx'
persist_app_state()
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

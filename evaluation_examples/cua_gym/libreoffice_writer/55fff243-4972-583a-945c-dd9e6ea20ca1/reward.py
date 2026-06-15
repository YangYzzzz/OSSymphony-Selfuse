"""
Reward Script: Convert manually numbered definitions to auto-numbered list
Task ID: writer_legal_028
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): All 15 definition paragraphs use 'List Number' style
  Component 2 (0.3): Manual number prefixes removed from all 15 definitions
  Component 3 (0.3): All 15 definition texts preserved (content integrity anchored to style change)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_legal_028'

# The 15 definition terms expected in the document (in order)
EXPECTED_TERMS = [
    '"Affiliate"',
    '"Agreement"',
    '"Authorized Users"',
    '"Confidential Information"',
    '"Documentation"',
    '"Effective Date"',
    '"Intellectual Property Rights"',
    '"License Fee"',
    '"Licensed Territory"',
    '"Maintenance Services"',
    '"Permitted Purpose"',
    '"Software"',
    '"Source Code"',
    '"Term"',
    '"Update"',
]


def find_definition_paragraphs(doc):
    """Find the 15 definition paragraphs by looking for paragraphs containing the expected terms."""
    def_paras = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        # Check if this paragraph starts with one of the expected terms
        # (possibly preceded by a manual number like "1. ")
        clean_text = re.sub(r'^\d+\.\s*', '', text)
        for term in EXPECTED_TERMS:
            if clean_text.startswith(term):
                def_paras.append(para)
                break
    return def_paras


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

    # Find the definition paragraphs
    def_paras = find_definition_paragraphs(doc)
    print(f"INFO: Found {len(def_paras)} definition paragraphs (expected 15)")

    if len(def_paras) < 15:
        print(f"WARNING: Only found {len(def_paras)} of 15 expected definitions")

    # Component 1: All 15 definition paragraphs use 'List Number' style (0.4 points)
    # This checks the core task requirement: automatic numbering via paragraph style.
    # Initial state: all are 'Normal' style -> FAIL
    # Golden state: all are 'List Number' style -> PASS
    try:
        list_number_count = 0
        for para in def_paras:
            style_name = para.style.name if para.style else 'None'
            if style_name == 'List Number':
                list_number_count += 1
            else:
                print(f"DETAIL: Paragraph starting with '{para.text[:40]}...' has style '{style_name}', expected 'List Number'")

        if len(def_paras) >= 15 and list_number_count == len(def_paras):
            print(f"PASS: Component 1 — All {list_number_count} definitions use 'List Number' style (0.4 pts)")
            total_score += 0.4
        elif list_number_count > 0:
            # Partial credit: proportional to how many were converted
            partial = 0.4 * (list_number_count / 15)
            print(f"PARTIAL: Component 1 — {list_number_count}/15 definitions use 'List Number' style ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No definitions use 'List Number' style (0/{len(def_paras)})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Manual number prefixes removed (0.3 points)
    # Initial state: text starts with "1. ", "2. ", etc. -> FAIL
    # Golden state: text starts directly with the quoted term -> PASS
    try:
        no_manual_num_count = 0
        for para in def_paras:
            text = para.text.strip()
            has_manual_num = bool(re.match(r'^\d+\.\s+', text))
            if not has_manual_num:
                no_manual_num_count += 1
            else:
                print(f"DETAIL: Still has manual number: '{text[:40]}...'")

        if len(def_paras) >= 15 and no_manual_num_count == len(def_paras):
            print(f"PASS: Component 2 — All {no_manual_num_count} definitions have manual numbers removed (0.3 pts)")
            total_score += 0.3
        elif no_manual_num_count > 0:
            partial = 0.3 * (no_manual_num_count / 15)
            print(f"PARTIAL: Component 2 — {no_manual_num_count}/15 definitions have manual numbers removed ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — All definitions still have manual number prefixes")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Definition content preserved AND has List Number style (0.3 points)
    # This is a compound check: we verify the content is intact AND anchored to the style change.
    # Initial state: style is 'Normal' so compound check FAILS even though content exists.
    # Golden state: style is 'List Number' AND content is intact -> PASS
    try:
        found_terms_with_style = 0
        for i, term in enumerate(EXPECTED_TERMS):
            found = False
            for para in def_paras:
                text = re.sub(r'^\d+\.\s*', '', para.text.strip())
                style_name = para.style.name if para.style else 'None'
                if text.startswith(term) and style_name == 'List Number':
                    found = True
                    break
            if found:
                found_terms_with_style += 1
            else:
                print(f"DETAIL: Term {term} not found with 'List Number' style")

        if found_terms_with_style == 15:
            print(f"PASS: Component 3 — All 15 definition terms present with correct style (0.3 pts)")
            total_score += 0.3
        elif found_terms_with_style > 0:
            partial = 0.3 * (found_terms_with_style / 15)
            print(f"PARTIAL: Component 3 — {found_terms_with_style}/15 terms present with correct style ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No definition terms found with 'List Number' style")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

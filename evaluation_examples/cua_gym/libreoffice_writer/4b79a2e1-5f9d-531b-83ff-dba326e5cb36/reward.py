"""
Reward Script: Index of Defined Terms for Legal Agreement
Task ID: writer_legal_058
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): XE index entry fields exist for all 25 defined terms
  Component 2 (0.2): INDEX field exists in the document
  Component 3 (0.3): "INDEX OF DEFINED TERMS" heading exists at end of document
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_legal_058'

# The 25 defined terms from Article I of the agreement
EXPECTED_TERMS = [
    "Affiliate",
    "Agreement",
    "Applicable Law",
    "Business Day",
    "Change of Control",
    "Claim",
    "Confidential Information",
    "Damages",
    "Deliverables",
    "Effective Date",
    "Fee Schedule",
    "Force Majeure Event",
    "Governing Law",
    "Indemnified Party",
    "Intellectual Property",
    "Key Personnel",
    "Liability Cap",
    "Material Breach",
    "Notice",
    "Party",
    "Permitted Subcontractor",
    "Service Level Agreement",
    "Statement of Work",
    "Term",
    "Termination for Convenience",
]


def persist_app_state(domain):
    """Save any unsaved LibreOffice edits before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.0)
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

    # Namespace for XML parsing
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    body = doc.element.body

    # Component 1: XE index entry fields for the 25 defined terms (0.5 points)
    # Each term marked as index entry earns 0.5/25 = 0.02 points
    try:
        instr_fields = body.findall('.//w:instrText', ns)
        xe_terms_found = set()
        for field in instr_fields:
            text = (field.text or '').strip()
            if 'XE' in text:
                # Extract term name from XE "TermName" or XE "TermName: " format
                # Remove 'XE' prefix, strip quotes, colons, and whitespace
                import re
                match = re.search(r'XE\s+"([^"]+)"', text)
                if match:
                    term_text = match.group(1).rstrip(': ').strip()
                    if term_text:
                        xe_terms_found.add(term_text)

        matched_count = 0
        for term in EXPECTED_TERMS:
            if term in xe_terms_found:
                matched_count += 1

        if matched_count > 0:
            component1_score = 0.5 * (matched_count / len(EXPECTED_TERMS))
            total_score += component1_score
            print(f"PASS: Component 1 — {matched_count}/{len(EXPECTED_TERMS)} XE index entries found ({component1_score:.3f} pts)")
            if matched_count < len(EXPECTED_TERMS):
                missing = [t for t in EXPECTED_TERMS if t not in xe_terms_found]
                print(f"  Missing terms: {missing[:5]}{'...' if len(missing) > 5 else ''}")
        else:
            print(f"FAIL: Component 1 — No XE index entries found (0 of {len(EXPECTED_TERMS)} expected)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: INDEX field exists in the document (0.2 points)
    # This is the field code that generates the actual index
    try:
        index_field_count = sum(
            1 for field in instr_fields
            if 'INDEX' in (field.text or '') and 'XE' not in (field.text or '')
        )

        if index_field_count > 0:
            print(f"PASS: Component 2 — INDEX field code found ({0.2} pts)")
            total_score += 0.2
        else:
            print("FAIL: Component 2 — No INDEX field code found in document")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: "INDEX OF DEFINED TERMS" heading exists at the end of the document (0.3 points)
    # The task requires an alphabetical index at the back of the agreement
    try:
        # Look for the heading in the last 10 paragraphs
        paras = doc.paragraphs
        heading_matches = [
            p for p in paras[-10:]
            if 'INDEX OF DEFINED TERMS' in p.text.strip().upper()
        ]

        if len(heading_matches) > 0:
            print(f"PASS: Component 3 — 'INDEX OF DEFINED TERMS' heading found at end of document ({0.3} pts)")
            total_score += 0.3
        else:
            print("FAIL: Component 3 — 'INDEX OF DEFINED TERMS' heading not found in last 10 paragraphs")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

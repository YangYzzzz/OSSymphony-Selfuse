"""
Reward Script: NDA document creation in LibreOffice Writer
Task ID: writer_wf_023
Domain: libreoffice_writer
Scoring:
  C1: Title "NON-DISCLOSURE AGREEMENT" centered + bold (0.15)
  C2: Effective date field present (0.05)
  C3: Party identification - Disclosing/Receiving Party lines (0.15)
  C4: 7 numbered clauses with correct titles (0.30)
  C5: Clause body text present (min 2 sentences each) (0.15)
  C6: Dual signature blocks with date lines (0.20)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_wf_023'


def persist_app_state(domain):
    """Try to save any unsaved document in LibreOffice."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify NDA document creation with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
    except ImportError as e:
        print(f"CRITICAL: Cannot import python-docx: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paragraphs = doc.paragraphs
    all_text = [p.text.strip() for p in paragraphs]
    non_empty = [t for t in all_text if t]

    # Precondition: document must have meaningful content
    if len(non_empty) < 5:
        print(f"FAIL: Document has only {len(non_empty)} non-empty paragraphs — too few for an NDA")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Title "NON-DISCLOSURE AGREEMENT" centered and bold (0.15 points)
    try:
        title_found = False
        for p in paragraphs:
            text_upper = p.text.strip().upper()
            if 'NON-DISCLOSURE AGREEMENT' in text_upper or 'NONDISCLOSURE AGREEMENT' in text_upper:
                # Check centered
                is_centered = (p.paragraph_format.alignment == WD_PARAGRAPH_ALIGNMENT.CENTER)
                # Check bold — at least one run with the title text is bold
                has_bold = any(r.font.bold for r in p.runs if r.text.strip())
                if is_centered and has_bold:
                    print(f"PASS: Component 1 — Title found, centered and bold (0.15 pts)")
                    total_score += 0.15
                    title_found = True
                elif is_centered:
                    print(f"PARTIAL: Component 1 — Title found and centered but not bold (0.07 pts)")
                    total_score += 0.07
                    title_found = True
                elif has_bold:
                    print(f"PARTIAL: Component 1 — Title found and bold but not centered (0.07 pts)")
                    total_score += 0.07
                    title_found = True
                else:
                    print(f"PARTIAL: Component 1 — Title text found but not centered or bold (0.03 pts)")
                    total_score += 0.03
                    title_found = True
                break
        if not title_found:
            print(f"FAIL: Component 1 — No 'NON-DISCLOSURE AGREEMENT' title found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Effective date field (0.05 points)
    try:
        date_found = False
        for t in all_text:
            if re.search(r'effective\s+date', t, re.IGNORECASE):
                date_found = True
                break
        if date_found:
            print(f"PASS: Component 2 — Effective date field found (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 2 — No effective date field found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Party identification — Disclosing Party and Receiving Party (0.15 points)
    try:
        has_disclosing = False
        has_receiving = False
        for t in all_text:
            if re.search(r'disclosing\s+party', t, re.IGNORECASE):
                has_disclosing = True
            if re.search(r'receiving\s+party', t, re.IGNORECASE):
                has_receiving = True
        party_score = 0.0
        if has_disclosing:
            party_score += 0.075
        if has_receiving:
            party_score += 0.075
        if party_score > 0:
            print(f"{'PASS' if party_score == 0.15 else 'PARTIAL'}: Component 3 — "
                  f"Disclosing={has_disclosing}, Receiving={has_receiving} ({party_score} pts)")
            total_score += party_score
        else:
            print(f"FAIL: Component 3 — No party identification found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: 7 numbered clauses with correct titles (0.30 points)
    try:
        expected_clauses = [
            (1, r'definition\s+of\s+confidential\s+information'),
            (2, r'obligations'),
            (3, r'exclusions'),
            (4, r'term'),
            (5, r'return\s+of\s+materials'),
            (6, r'remedies'),
            (7, r'governing\s+law'),
        ]
        clauses_found = 0
        for num, pattern in expected_clauses:
            clause_found = False
            for t in all_text:
                # Match numbered clause: "1. Definition..." or "1) Definition..."
                if re.search(rf'(^|\s){num}\s*[\.\)]\s*', t) and re.search(pattern, t, re.IGNORECASE):
                    clause_found = True
                    break
            if clause_found:
                clauses_found += 1
            else:
                print(f"  Clause {num} ({pattern}): not found")

        clause_score = (clauses_found / 7) * 0.30
        if clauses_found == 7:
            print(f"PASS: Component 4 — All 7 numbered clauses found ({clause_score:.2f} pts)")
        elif clauses_found > 0:
            print(f"PARTIAL: Component 4 — {clauses_found}/7 clauses found ({clause_score:.2f} pts)")
        else:
            print(f"FAIL: Component 4 — No numbered clauses found")
        total_score += clause_score
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Clause body text (each clause should have 2-3 sentences) (0.15 points)
    try:
        # Find clause heading indices and check that text follows
        clause_heading_indices = []
        for i, t in enumerate(all_text):
            if re.match(r'\s*\d\s*[\.\)]\s+\S', t):
                clause_heading_indices.append(i)

        clauses_with_body = 0
        for idx in clause_heading_indices:
            # Look at the next paragraph(s) for body text
            body_text = ""
            for j in range(idx + 1, min(idx + 4, len(all_text))):
                # Stop if we hit another clause heading
                if re.match(r'\s*\d\s*[\.\)]\s+\S', all_text[j]):
                    break
                body_text += " " + all_text[j]
            body_text = body_text.strip()
            # Count sentences (roughly by periods followed by space or end)
            sentences = len(re.findall(r'[.!?](?:\s|$)', body_text))
            if sentences >= 2:
                clauses_with_body += 1

        if clause_heading_indices:
            body_ratio = clauses_with_body / max(len(clause_heading_indices), 1)
            body_score = body_ratio * 0.15
            if clauses_with_body == len(clause_heading_indices) and clauses_with_body >= 7:
                print(f"PASS: Component 5 — All {clauses_with_body} clauses have 2+ sentence bodies ({body_score:.2f} pts)")
            elif clauses_with_body > 0:
                print(f"PARTIAL: Component 5 — {clauses_with_body}/{len(clause_heading_indices)} clauses have 2+ sentence bodies ({body_score:.2f} pts)")
            else:
                print(f"FAIL: Component 5 — No clause bodies with 2+ sentences found")
            total_score += body_score
        else:
            print(f"FAIL: Component 5 — No clause headings found to check bodies")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Dual signature blocks with date lines (0.20 points)
    try:
        full_text = "\n".join(all_text)
        # Check for signature lines for both parties
        has_sig_disclosing = bool(re.search(r'disclosing\s+party.*signature', full_text, re.IGNORECASE | re.DOTALL))
        has_sig_receiving = bool(re.search(r'receiving\s+party.*signature', full_text, re.IGNORECASE | re.DOTALL))

        # Also check for date lines in signature blocks (after the signature section)
        # Look for "Date:" or "Date: ___" appearing in the signature area
        sig_section_match = re.search(r'(disclosing\s+party|receiving\s+party|signature|in\s+witness)', full_text, re.IGNORECASE)
        has_date_lines = False
        if sig_section_match:
            sig_section = full_text[sig_section_match.start():]
            date_count = len(re.findall(r'date\s*[:.]?\s*[_]*', sig_section, re.IGNORECASE))
            has_date_lines = date_count >= 2

        sig_score = 0.0
        if has_sig_disclosing:
            sig_score += 0.05
        if has_sig_receiving:
            sig_score += 0.05
        if has_date_lines:
            sig_score += 0.10
        elif date_count >= 1:
            sig_score += 0.05

        if sig_score > 0:
            print(f"{'PASS' if sig_score == 0.20 else 'PARTIAL'}: Component 6 — "
                  f"Disclosing sig={has_sig_disclosing}, Receiving sig={has_sig_receiving}, "
                  f"Date lines={has_date_lines} ({sig_score:.2f} pts)")
            total_score += sig_score
        else:
            print(f"FAIL: Component 6 — No signature blocks found")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(round(total_score, 2), 1.0)
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

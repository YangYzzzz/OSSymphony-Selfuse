"""
Reward Script: Legal Services Contract in LibreOffice Writer
Task ID: writer_wf_006
Domain: libreoffice_writer
Scoring:
  Component 1: Title 'SERVICE AGREEMENT' centered and bold (0.2 pts)
  Component 2: 8 numbered clauses with correct names (0.4 pts)
  Component 3: Each clause has body text (2+ sentences) (0.2 pts)
  Component 4: Signature block for Client and Service Provider (0.2 pts)
"""

import os
import re
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

WORKDIR = '/home/user'
TASK_ID = 'writer_wf_006'

EXPECTED_CLAUSES = [
    '1. Parties',
    '2. Scope of Services',
    '3. Term and Termination',
    '4. Payment Terms',
    '5. Confidentiality',
    '6. Liability',
    '7. Dispute Resolution',
    '8. General Provisions',
]

SIGNATURE_PARTIES = ['Client', 'Service Provider']
SIGNATURE_FIELDS = ['Name', 'Title', 'Date', 'Signature']


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
    if len(paragraphs) == 0:
        print("FAIL: Document is empty (0 paragraphs)")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Title 'SERVICE AGREEMENT' centered and bold (0.2 points)
    try:
        # Look for title in first few paragraphs (skip leading blanks)
        title_found = False
        for p in paragraphs[:5]:
            text = p.text.strip()
            if not text:
                continue
            # Check if text contains SERVICE AGREEMENT
            if 'SERVICE AGREEMENT' in text.upper():
                # Check centering
                is_centered = (p.paragraph_format.alignment == WD_PARAGRAPH_ALIGNMENT.CENTER)
                # Check bold - at least one run with the title text should be bold
                has_bold = any(r.bold for r in p.runs if r.text.strip())
                if is_centered and has_bold:
                    print(f"PASS: Component 1 — Title 'SERVICE AGREEMENT' is centered and bold (0.2 pts)")
                    total_score += 0.2
                    title_found = True
                elif is_centered:
                    print(f"PARTIAL: Component 1 — Title is centered but not bold (0.1 pts)")
                    total_score += 0.1
                    title_found = True
                elif has_bold:
                    print(f"PARTIAL: Component 1 — Title is bold but not centered (0.1 pts)")
                    total_score += 0.1
                    title_found = True
                else:
                    print(f"FAIL: Component 1 — Title found but not centered or bold")
                    title_found = True
                break
        if not title_found:
            print("FAIL: Component 1 — 'SERVICE AGREEMENT' title not found in document")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 8 numbered clauses with correct names (0.4 points)
    # Award 0.05 per clause found = 0.4 total
    try:
        all_text = [p.text.strip() for p in paragraphs]
        clauses_found = 0
        for clause in EXPECTED_CLAUSES:
            # Check if any paragraph contains this clause text (case-insensitive match)
            clause_lower = clause.lower()
            found = False
            for text in all_text:
                if clause_lower in text.lower():
                    found = True
                    break
            if found:
                clauses_found += 1
            else:
                print(f"FAIL: Component 2 — Clause '{clause}' not found")

        clause_score = clauses_found * 0.05
        if clauses_found == 8:
            print(f"PASS: Component 2 — All 8 numbered clauses found (0.4 pts)")
        else:
            print(f"PARTIAL: Component 2 — {clauses_found}/8 clauses found ({clause_score:.2f} pts)")
        total_score += clause_score
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Each clause has body text with 2+ sentences (0.2 points)
    # For each clause, check the paragraph(s) following it for body text
    try:
        clauses_with_body = 0
        for idx, p in enumerate(paragraphs):
            text = p.text.strip()
            # Check if this paragraph is a clause heading
            is_clause_heading = False
            for clause in EXPECTED_CLAUSES:
                if clause.lower() in text.lower() and text.lower().startswith(clause[0].lower()):
                    is_clause_heading = True
                    break
            if is_clause_heading:
                # Look at the next paragraph(s) for body text
                body_text = ''
                for j in range(idx + 1, min(idx + 4, len(paragraphs))):
                    next_text = paragraphs[j].text.strip()
                    # Stop if we hit the next clause or a signature section
                    if any(c.lower() in next_text.lower() for c in EXPECTED_CLAUSES):
                        break
                    if next_text:
                        body_text += ' ' + next_text
                # Count sentences (rough: split by period followed by space or end)
                sentences = [s.strip() for s in re.split(r'[.!?]+', body_text) if len(s.strip()) > 10]
                if len(sentences) >= 2:
                    clauses_with_body += 1
                else:
                    print(f"FAIL: Component 3 — Clause '{text[:30]}' has < 2 sentences in body")

        body_score = (clauses_with_body / 8.0) * 0.2 if clauses_with_body > 0 else 0.0
        if clauses_with_body == 8:
            print(f"PASS: Component 3 — All 8 clauses have body text with 2+ sentences (0.2 pts)")
        else:
            print(f"PARTIAL: Component 3 — {clauses_with_body}/8 clauses have adequate body text ({body_score:.2f} pts)")
        total_score += body_score
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Signature block for Client and Service Provider (0.2 points)
    # Check for both party labels and their fields (Name, Title, Date, Signature)
    try:
        full_text = '\n'.join(p.text for p in paragraphs)
        full_text_lower = full_text.lower()
        parties_found = 0
        fields_found = 0
        total_expected_fields = len(SIGNATURE_PARTIES) * len(SIGNATURE_FIELDS)

        for party in SIGNATURE_PARTIES:
            if party.lower() in full_text_lower:
                parties_found += 1
            else:
                print(f"FAIL: Component 4 — Party '{party}' not found in signature block")

        # Check fields appear at least twice (once per party) or at least exist
        for field in SIGNATURE_FIELDS:
            # Count occurrences in the lower half of the document (signature area)
            sig_area = '\n'.join(p.text for p in paragraphs[len(paragraphs)//2:])
            count = sig_area.lower().count(field.lower())
            if count >= 2:
                fields_found += 2
            elif count >= 1:
                fields_found += 1

        # Score: 0.1 for parties present, 0.1 for fields present
        party_score = 0.0
        if parties_found == 2:
            party_score = 0.1
            print(f"PASS: Component 4a — Both parties found in signature block (0.1 pts)")
        elif parties_found == 1:
            party_score = 0.05
            print(f"PARTIAL: Component 4a — Only {parties_found}/2 parties found (0.05 pts)")
        else:
            print(f"FAIL: Component 4a — No party labels found in signature block")

        field_score = 0.0
        field_ratio = fields_found / total_expected_fields if total_expected_fields > 0 else 0
        if field_ratio >= 0.9:
            field_score = 0.1
            print(f"PASS: Component 4b — Signature fields present ({fields_found}/{total_expected_fields}) (0.1 pts)")
        elif field_ratio >= 0.5:
            field_score = 0.05
            print(f"PARTIAL: Component 4b — Some signature fields present ({fields_found}/{total_expected_fields}) (0.05 pts)")
        else:
            print(f"FAIL: Component 4b — Insufficient signature fields ({fields_found}/{total_expected_fields})")

        total_score += party_score + field_score
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

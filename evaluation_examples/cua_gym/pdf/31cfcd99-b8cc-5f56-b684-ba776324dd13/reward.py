"""
Reward Script: Create a Legal-size PDF with NDA content
Task ID: pdf_cr_023
Domain: pdf
Scoring:
  Component 1 (0.25) - Legal-size PDF exists with correct dimensions (612x1008)
  Component 2 (0.25) - Heading "Non-Disclosure Agreement" in 22pt bold
  Component 3 (0.30) - All 5 numbered clauses present
  Component 4 (0.20) - Signature lines for Disclosing Party and Receiving Party
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_023'
FILE_PATH = os.path.join(WORKDIR, 'Desktop', 'legal_doc.pdf')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import fitz
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Legal-size page dimensions (0.25 points)
    # Legal size = 612 x 1008 points (8.5 x 14 inches)
    try:
        if len(doc) < 1:
            print("FAIL: Component 1 -- PDF has no pages")
        else:
            page = doc[0]
            w = page.rect.width
            h = page.rect.height
            # Allow small tolerance (5 points) for rounding
            width_ok = abs(w - 612.0) < 5.0
            height_ok = abs(h - 1008.0) < 5.0
            if width_ok and height_ok:
                print(f"PASS: Component 1 -- Legal-size page dimensions {w:.1f}x{h:.1f} (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 -- Expected ~612x1008, found {w:.1f}x{h:.1f}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Heading "Non-Disclosure Agreement" in 22pt bold (0.25 points)
    try:
        page = doc[0]
        blocks = page.get_text('dict')['blocks']
        heading_spans = []

        for block in blocks:
            if 'lines' not in block:
                continue
            for line in block['lines']:
                for span in line['spans']:
                    text = span['text'].strip()
                    if 'Non-Disclosure Agreement' in text:
                        heading_spans.append(span)

        heading_found = len(heading_spans) > 0
        # Derive bold/size from actual span properties
        heading_size_ok = any(abs(s['size'] - 22.0) < 2.0 for s in heading_spans)
        heading_bold = any(
            (s['flags'] & 16) or 'Bold' in s.get('font', '')
            for s in heading_spans
        )

        if heading_found and heading_bold and heading_size_ok:
            print(f"PASS: Component 2 -- 'Non-Disclosure Agreement' heading in ~22pt bold (0.25 pts)")
            total_score += 0.25
        elif heading_found and heading_bold:
            print(f"FAIL: Component 2 -- Heading found and bold but wrong size")
        elif heading_found:
            print(f"FAIL: Component 2 -- Heading found but not bold or wrong size")
        else:
            print(f"FAIL: Component 2 -- 'Non-Disclosure Agreement' heading not found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: All 5 numbered clauses present (0.30 points)
    # Each clause gets 0.06 points (5 * 0.06 = 0.30)
    try:
        page = doc[0]
        full_text = ' '.join(page.get_text().split())  # normalize whitespace for wrapped lines

        clause_keywords = [
            "strict confidentiality",
            "trade secrets, business plans",
            "two (2) years",
            "third parties without prior written consent",
            "legal action and monetary damages",
        ]

        clauses_found = 0
        for i, keyword in enumerate(clause_keywords, 1):
            if keyword.lower() in full_text.lower():
                clauses_found += 1
                print(f"  Clause {i}: FOUND (keyword: '{keyword}')")
            else:
                print(f"  Clause {i}: MISSING (keyword: '{keyword}')")

        clause_score = clauses_found * 0.06
        if clauses_found == 5:
            print(f"PASS: Component 3 -- All 5 clauses found (0.30 pts)")
            total_score += clause_score
        elif clauses_found > 0:
            print(f"PARTIAL: Component 3 -- {clauses_found}/5 clauses found ({clause_score:.2f} pts)")
            total_score += clause_score
        else:
            print(f"FAIL: Component 3 -- No clauses found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Signature lines for "Disclosing Party" and "Receiving Party" (0.20 points)
    try:
        page = doc[0]
        full_text = page.get_text()  # raw text fine for simple label checks

        disclosing_found = 'Disclosing Party' in full_text
        receiving_found = 'Receiving Party' in full_text

        if disclosing_found and receiving_found:
            print(f"PASS: Component 4 -- Both signature party labels found (0.20 pts)")
            total_score += 0.20
        elif disclosing_found or receiving_found:
            found = 'Disclosing' if disclosing_found else 'Receiving'
            missing = 'Receiving' if disclosing_found else 'Disclosing'
            print(f"PARTIAL: Component 4 -- '{found} Party' found, '{missing} Party' missing (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 -- Neither 'Disclosing Party' nor 'Receiving Party' found")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

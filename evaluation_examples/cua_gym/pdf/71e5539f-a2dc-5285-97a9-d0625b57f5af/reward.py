"""
Reward Script: Batch payment receipt PDF generation
Task ID: pdf_fin_032
Domain: pdf
Scoring:
  Component 1 (0.20): All 5 PDF files exist with correct names
  Component 2 (0.10): Each PDF is exactly 1 page
  Component 3 (0.10): Company name 'PayStream Financial' present in each
  Component 4 (0.20): Correct receipt numbers (PAY-2024-0101 through PAY-2024-0105)
  Component 5 (0.15): Correct dates (March 1-5, 2024)
  Component 6 (0.15): Correct amounts per receipt
  Component 7 (0.10): Correct payee names per receipt
"""

import os
try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

WORKDIR = '/home/user'
RECEIPTS_DIR = os.path.join(WORKDIR, 'finance', 'receipts')
TASK_ID = 'pdf_fin_032'

# Ground truth for each receipt
RECEIPTS = {
    'receipt_0101.pdf': {
        'receipt_num': 'PAY-2024-0101',
        'date': 'March 1, 2024',
        'amount': '$1,250.00',
        'payee': 'Acme Supplies',
    },
    'receipt_0102.pdf': {
        'receipt_num': 'PAY-2024-0102',
        'date': 'March 2, 2024',
        'amount': '$3,400.00',
        'payee': 'DataTech Inc',
    },
    'receipt_0103.pdf': {
        'receipt_num': 'PAY-2024-0103',
        'date': 'March 3, 2024',
        'amount': '$890.50',
        'payee': 'Office Depot',
    },
    'receipt_0104.pdf': {
        'receipt_num': 'PAY-2024-0104',
        'date': 'March 4, 2024',
        'amount': '$5,675.25',
        'payee': 'CloudServe LLC',
    },
    'receipt_0105.pdf': {
        'receipt_num': 'PAY-2024-0105',
        'date': 'March 5, 2024',
        'amount': '$2,100.00',
        'payee': 'Premier Staffing',
    },
}


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ── Component 1: All 5 PDF files exist with correct names (0.20 pts) ──
    try:
        existing_files = []
        if os.path.isdir(RECEIPTS_DIR):
            for fname in RECEIPTS:
                fpath = os.path.join(RECEIPTS_DIR, fname)
                if os.path.isfile(fpath):
                    existing_files.append(fname)
        if len(existing_files) == 5:
            print(f"PASS: Component 1 — All 5 PDF files exist (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — Expected 5 files, found {len(existing_files)}: {existing_files}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # If no files found at all, short-circuit
    if not os.path.isdir(RECEIPTS_DIR) or len(existing_files) == 0:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Load all PDFs and extract text
    pdf_texts = {}
    pdf_pages = {}
    for fname in RECEIPTS:
        fpath = os.path.join(RECEIPTS_DIR, fname)
        if os.path.isfile(fpath):
            try:
                doc = fitz.open(fpath)
                pdf_pages[fname] = len(doc)
                full_text = ''
                for page in doc:
                    full_text += page.get_text()
                pdf_texts[fname] = full_text
                doc.close()
            except Exception as e:
                print(f"WARNING: Could not read {fname}: {e}")
                pdf_texts[fname] = ''
                pdf_pages[fname] = 0

    # ── Component 2: Each PDF is exactly 1 page (0.10 pts) ──
    try:
        single_page_count = sum(1 for f in RECEIPTS if pdf_pages.get(f) == 1)
        if single_page_count == 5:
            print(f"PASS: Component 2 — All 5 PDFs are single-page (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 2 — {single_page_count}/5 PDFs are single-page. Pages: {pdf_pages}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ── Component 3: Company name 'PayStream Financial' in each (0.10 pts) ──
    try:
        company_count = 0
        for fname in RECEIPTS:
            text = pdf_texts.get(fname, '')
            if 'PayStream Financial' in text:
                company_count += 1
        if company_count == 5:
            print(f"PASS: Component 3 — 'PayStream Financial' found in all 5 PDFs (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 — 'PayStream Financial' found in {company_count}/5 PDFs")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ── Component 4: Correct receipt numbers (0.20 pts) ──
    try:
        receipt_num_ok = 0
        for fname, gt in RECEIPTS.items():
            text = pdf_texts.get(fname, '')
            if gt['receipt_num'] in text:
                receipt_num_ok += 1
            else:
                print(f"  DETAIL: {fname} missing receipt number '{gt['receipt_num']}'")
        if receipt_num_ok == 5:
            print(f"PASS: Component 4 — All 5 receipt numbers correct (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — {receipt_num_ok}/5 receipt numbers correct")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ── Component 5: Correct dates (0.15 pts) ──
    try:
        date_ok = 0
        for fname, gt in RECEIPTS.items():
            text = pdf_texts.get(fname, '')
            if gt['date'] in text:
                date_ok += 1
            else:
                print(f"  DETAIL: {fname} missing date '{gt['date']}'")
        if date_ok == 5:
            print(f"PASS: Component 5 — All 5 dates correct (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — {date_ok}/5 dates correct")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # ── Component 6: Correct amounts (0.15 pts) ──
    try:
        amount_ok = 0
        for fname, gt in RECEIPTS.items():
            text = pdf_texts.get(fname, '')
            if gt['amount'] in text:
                amount_ok += 1
            else:
                print(f"  DETAIL: {fname} missing amount '{gt['amount']}'")
        if amount_ok == 5:
            print(f"PASS: Component 6 — All 5 amounts correct (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 6 — {amount_ok}/5 amounts correct")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # ── Component 7: Correct payee names (0.10 pts) ──
    try:
        payee_ok = 0
        for fname, gt in RECEIPTS.items():
            text = pdf_texts.get(fname, '')
            if gt['payee'] in text:
                payee_ok += 1
            else:
                print(f"  DETAIL: {fname} missing payee '{gt['payee']}'")
        if payee_ok == 5:
            print(f"PASS: Component 7 — All 5 payee names correct (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 7 — {payee_ok}/5 payee names correct")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

"""
Reward Script: Multi-language PDF invoice generator
Task ID: pdf_gf3_043
Domain: pdf (libreoffice_calc listed but actually PDF generation)
Scoring:
  Component 1: Script exists at /home/user/scripts/multilang_invoice.py (0.10)
  Component 2: English invoice exists with correct labels and US date format (0.20)
  Component 3: Spanish invoice exists with correct labels and ES date format (0.20)
  Component 4: French invoice exists with correct labels and FR date format (0.20)
  Component 5: Financial amounts consistent across all 3 invoices (0.15)
  Component 6: Locale-specific number formatting (0.15)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_043'

SCRIPT_PATH = f'{WORKDIR}/scripts/multilang_invoice.py'
INVOICE_DIR = f'{WORKDIR}/output/invoices'
EN_PATH = f'{INVOICE_DIR}/invoice_EN.pdf'
ES_PATH = f'{INVOICE_DIR}/invoice_ES.pdf'
FR_PATH = f'{INVOICE_DIR}/invoice_FR.pdf'


def extract_text(pdf_path):
    """Extract all text from a PDF file."""
    import pymupdf
    doc = pymupdf.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text")
    doc.close()
    return text


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Script exists at /home/user/scripts/multilang_invoice.py (0.10 pts)
    # This file does NOT exist in initial_env (empty scripts dir), only in golden_env
    try:
        if os.path.isfile(SCRIPT_PATH):
            # Verify it's a real Python script with meaningful content
            content = open(SCRIPT_PATH).read()
            if len(content) > 100 and ('pdf' in content.lower() or 'PDF' in content or 'invoice' in content.lower()):
                print(f"PASS: Component 1 — Script exists at {SCRIPT_PATH} ({len(content)} bytes) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 1 — Script exists but appears trivial ({len(content)} bytes)")
        else:
            print(f"FAIL: Component 1 — Script not found at {SCRIPT_PATH}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: English invoice with correct labels and US date format (0.20 pts)
    # Initial_env has no PDFs in output/invoices/, so this only passes on golden
    try:
        if not os.path.isfile(EN_PATH):
            print(f"FAIL: Component 2 — invoice_EN.pdf not found")
        else:
            en_text = extract_text(EN_PATH)
            en_score = 0.0

            # Check English title "INVOICE"
            if 'INVOICE' in en_text and 'FACTURA' not in en_text and 'FACTURE' not in en_text:
                en_score += 0.05
            else:
                print(f"FAIL: Component 2a — Missing English title 'INVOICE'")

            # Check US date format MM/DD/YYYY for invoice date (03/15/2025)
            if re.search(r'03/15/2025', en_text):
                en_score += 0.05
            else:
                print(f"FAIL: Component 2b — Missing US date format (expected 03/15/2025)")

            # Check English column headers
            en_headers_found = 0
            for header in ['Description', 'Qty', 'Unit Price', 'Amount']:
                if header in en_text:
                    en_headers_found += 1
            if en_headers_found >= 3:
                en_score += 0.05
            else:
                print(f"FAIL: Component 2c — Missing English headers (found {en_headers_found}/4)")

            # Check invoice number present
            if 'INV-2025-0847' in en_text:
                en_score += 0.05
            else:
                print(f"FAIL: Component 2d — Missing invoice number INV-2025-0847")

            if en_score > 0:
                print(f"PASS: Component 2 — English invoice verified ({en_score:.2f} pts)")
            total_score += en_score
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Spanish invoice with correct labels and ES date format (0.20 pts)
    try:
        if not os.path.isfile(ES_PATH):
            print(f"FAIL: Component 3 — invoice_ES.pdf not found")
        else:
            es_text = extract_text(ES_PATH)
            es_score = 0.0

            # Check Spanish title "FACTURA"
            if 'FACTURA' in es_text:
                es_score += 0.05
            else:
                print(f"FAIL: Component 3a — Missing Spanish title 'FACTURA'")

            # Check ES date format DD/MM/YYYY (15/03/2025)
            if re.search(r'15/03/2025', es_text):
                es_score += 0.05
            else:
                print(f"FAIL: Component 3b — Missing ES date format (expected 15/03/2025)")

            # Check Spanish labels
            es_labels_found = 0
            for label in ['Cantidad', 'Precio', 'Importe', 'Descripcion']:
                if label in es_text:
                    es_labels_found += 1
            if es_labels_found >= 2:
                es_score += 0.05
            else:
                print(f"FAIL: Component 3c — Missing Spanish labels (found {es_labels_found}/4)")

            # Check invoice number present
            if 'INV-2025-0847' in es_text:
                es_score += 0.05
            else:
                print(f"FAIL: Component 3d — Missing invoice number INV-2025-0847")

            if es_score > 0:
                print(f"PASS: Component 3 — Spanish invoice verified ({es_score:.2f} pts)")
            total_score += es_score
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: French invoice with correct labels and FR date format (0.20 pts)
    try:
        if not os.path.isfile(FR_PATH):
            print(f"FAIL: Component 4 — invoice_FR.pdf not found")
        else:
            fr_text = extract_text(FR_PATH)
            fr_score = 0.0

            # Check French title "FACTURE"
            if 'FACTURE' in fr_text:
                fr_score += 0.05
            else:
                print(f"FAIL: Component 4a — Missing French title 'FACTURE'")

            # Check FR date format DD/MM/YYYY (15/03/2025)
            if re.search(r'15/03/2025', fr_text):
                fr_score += 0.05
            else:
                print(f"FAIL: Component 4b — Missing FR date format (expected 15/03/2025)")

            # Check French labels
            fr_labels_found = 0
            for label in ['Montant', 'Quantite', 'Prix', 'Facture']:
                if label in fr_text:
                    fr_labels_found += 1
            if fr_labels_found >= 2:
                fr_score += 0.05
            else:
                print(f"FAIL: Component 4c — Missing French labels (found {fr_labels_found}/4)")

            # Check invoice number present
            if 'INV-2025-0847' in fr_text:
                fr_score += 0.05
            else:
                print(f"FAIL: Component 4d — Missing invoice number INV-2025-0847")

            if fr_score > 0:
                print(f"PASS: Component 4 — French invoice verified ({fr_score:.2f} pts)")
            total_score += fr_score
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Financial amounts consistent across all 3 invoices (0.15 pts)
    # All three should contain the same total amount ($48,849.50 equivalent)
    # This checks that the financial data is consistent even though formatting differs
    try:
        if not (os.path.isfile(EN_PATH) and os.path.isfile(ES_PATH) and os.path.isfile(FR_PATH)):
            print(f"FAIL: Component 5 — Not all 3 PDFs exist, cannot compare amounts")
        else:
            en_text = extract_text(EN_PATH)
            es_text = extract_text(ES_PATH)
            fr_text = extract_text(FR_PATH)

            # Extract total amounts - look for the TOTAL line value
            # EN uses: $48,849.50
            # ES uses: $48.849,50
            # FR uses: 48 849,50 $
            amounts_ok = 0

            # Check EN total: $48,849.50
            if re.search(r'\$48[,.]849[,.]50', en_text):
                amounts_ok += 1
            else:
                print(f"FAIL: Component 5a — EN total not found (expected ~$48,849.50)")

            # Check ES total: $48.849,50
            if re.search(r'\$48[.\s]849[,.]50', es_text):
                amounts_ok += 1
            else:
                print(f"FAIL: Component 5b — ES total not found (expected ~$48.849,50)")

            # Check FR total: 48 849,50 $ or 48 849,50$
            if re.search(r'48[\s\u00a0]849[,.]50', fr_text):
                amounts_ok += 1
            else:
                print(f"FAIL: Component 5c — FR total not found (expected ~48 849,50 $)")

            if amounts_ok == 3:
                print(f"PASS: Component 5 — All 3 invoices have consistent total amounts (0.15 pts)")
                total_score += 0.15
            elif amounts_ok >= 2:
                partial = 0.10
                print(f"PARTIAL: Component 5 — {amounts_ok}/3 totals correct ({partial} pts)")
                total_score += partial
            elif amounts_ok == 1:
                partial = 0.05
                print(f"PARTIAL: Component 5 — {amounts_ok}/3 totals correct ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 5 — No totals found in expected formats")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Locale-specific number formatting (0.15 pts)
    # EN: comma as thousand separator, period as decimal ($12,500.00)
    # ES: period as thousand separator, comma as decimal ($12.500,00)
    # FR: space as thousand separator, comma as decimal (12 500,00)
    try:
        if not (os.path.isfile(EN_PATH) and os.path.isfile(ES_PATH) and os.path.isfile(FR_PATH)):
            print(f"FAIL: Component 6 — Not all 3 PDFs exist, cannot verify formatting")
        else:
            en_text = extract_text(EN_PATH)
            es_text = extract_text(ES_PATH)
            fr_text = extract_text(FR_PATH)

            format_ok = 0

            # EN: $12,500.00 (comma thousands, period decimal)
            if re.search(r'\$12,500\.00', en_text):
                format_ok += 1
            else:
                print(f"FAIL: Component 6a — EN number format incorrect (expected $12,500.00)")

            # ES: $12.500,00 (period thousands, comma decimal)
            if re.search(r'\$12\.500,00', es_text):
                format_ok += 1
            else:
                print(f"FAIL: Component 6b — ES number format incorrect (expected $12.500,00)")

            # FR: 12 500,00 (space thousands, comma decimal, currency after)
            if re.search(r'12[\s\u00a0]500,00', fr_text):
                format_ok += 1
            else:
                print(f"FAIL: Component 6c — FR number format incorrect (expected 12 500,00)")

            if format_ok == 3:
                print(f"PASS: Component 6 — All 3 locales use correct number formatting (0.15 pts)")
                total_score += 0.15
            elif format_ok >= 2:
                partial = 0.10
                print(f"PARTIAL: Component 6 — {format_ok}/3 locale formats correct ({partial} pts)")
                total_score += partial
            elif format_ok == 1:
                partial = 0.05
                print(f"PARTIAL: Component 6 — {format_ok}/3 locale formats correct ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 6 — No locale-specific number formats found")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

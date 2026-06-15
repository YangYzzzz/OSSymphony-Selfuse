"""
Reward Script: Invoice Automation Macro for LibreOffice Writer
Task ID: writer_gf4_047
Domain: libreoffice_writer
Scoring:
  Component 1 (0.15): FillInvoice macro exists in the ODT
  Component 2 (0.25): ODT bookmark fields populated with JSON data
  Component 3 (0.20): Calculations correct (subtotal, tax, grand total)
  Component 4 (0.15): Invoice date filled (not a placeholder)
  Component 5 (0.25): PDF exported to /home/user/invoices/INV-2025-0384.pdf with correct content
"""

import os
import json
import zipfile

WORKDIR = '/home/user'
TASK_ID = 'writer_gf4_047'


def get_odt_text_paragraphs(odt_path):
    """Extract all text paragraphs from an ODT file using odfpy."""
    from odf.opendocument import load
    from odf.text import P

    doc = load(odt_path)
    paragraphs = []
    for para in doc.getElementsByType(P):
        text_parts = []
        for node in para.childNodes:
            if node.nodeType == node.TEXT_NODE:
                text_parts.append(str(node))
            elif hasattr(node, 'childNodes'):
                for child in node.childNodes:
                    if child.nodeType == child.TEXT_NODE:
                        text_parts.append(str(child))
        paragraphs.append(''.join(text_parts))
    return paragraphs


def verify_task(odt_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the JSON config for reference values
    json_path = os.path.join(WORKDIR, 'invoice_config.json')
    try:
        with open(json_path, 'r') as f:
            config = json.load(f)
    except Exception as e:
        print(f"CRITICAL: Cannot load JSON config {json_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    invoice_number = config.get('InvoiceNumber', 'INV-2025-0384')
    client_name = config.get('ClientName', 'Greenleaf Consulting Partners')
    line_items = config.get('LineItems', [])
    tax_rate = config.get('TaxRate', 0.085)

    # Expected calculations
    expected_subtotal = sum(item['amount'] for item in line_items)  # 16200.0
    expected_tax = expected_subtotal * tax_rate  # 1377.0
    expected_grand_total = expected_subtotal + expected_tax  # 17577.0

    # ---------------------------------------------------------------
    # Component 1: FillInvoice macro exists in ODT (0.15 points)
    # This is a task-introduced change: initial ODT has no macro.
    # ---------------------------------------------------------------
    try:
        has_macro = False
        if os.path.exists(odt_path):
            with zipfile.ZipFile(odt_path, 'r') as z:
                for name in z.namelist():
                    if 'FillInvoice' in name and name.startswith('Basic/'):
                        has_macro = True
                        break
        if has_macro:
            print(f"PASS: Component 1 — FillInvoice macro found in ODT (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — FillInvoice macro not found in ODT")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ---------------------------------------------------------------
    # Component 2: ODT bookmark fields populated from JSON (0.25 points)
    # Initial has placeholders like [invoice number], [client name], etc.
    # Golden should have actual values from the JSON.
    # ---------------------------------------------------------------
    try:
        paragraphs = get_odt_text_paragraphs(odt_path)
        full_text = '\n'.join(paragraphs)

        fields_found = 0
        total_fields = 3  # invoice number, client name, at least one line item description

        # Check invoice number populated
        if invoice_number in full_text:
            fields_found += 1
            print(f"  Invoice number '{invoice_number}' found in ODT")
        else:
            print(f"  Invoice number '{invoice_number}' NOT found in ODT")

        # Check client name populated
        if client_name in full_text:
            fields_found += 1
            print(f"  Client name '{client_name}' found in ODT")
        else:
            print(f"  Client name '{client_name}' NOT found in ODT")

        # Check at least 3 of 5 line item descriptions present
        li_count = 0
        for item in line_items:
            if item['description'] in full_text:
                li_count += 1
        if li_count >= 3:
            fields_found += 1
            print(f"  {li_count}/5 line item descriptions found in ODT")
        else:
            print(f"  Only {li_count}/5 line item descriptions found in ODT")

        # Also verify NO placeholders remain
        has_placeholders = any(
            placeholder in full_text
            for placeholder in ['[invoice number]', '[client name]', '[line item']
        )
        if has_placeholders:
            print(f"  WARNING: Placeholder text still present in ODT")
            fields_found = max(0, fields_found - 1)

        if fields_found == total_fields:
            print(f"PASS: Component 2 — All key fields populated from JSON (0.25 pts)")
            total_score += 0.25
        elif fields_found >= 2:
            partial = round(0.25 * fields_found / total_fields, 2)
            print(f"PARTIAL: Component 2 — {fields_found}/{total_fields} fields populated ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Only {fields_found}/{total_fields} fields populated")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ---------------------------------------------------------------
    # Component 3: Calculations correct (0.20 points)
    # Subtotal = 16200.00, Tax = 1377.00, Grand Total = 17577.00
    # These values should NOT exist in the initial template.
    # ---------------------------------------------------------------
    try:
        paragraphs = get_odt_text_paragraphs(odt_path)
        full_text = '\n'.join(paragraphs)

        calc_checks = 0
        total_calc = 3

        # Check subtotal
        if '16,200' in full_text or '16200' in full_text:
            calc_checks += 1
            print(f"  Subtotal $16,200.00 found")
        else:
            print(f"  Subtotal $16,200.00 NOT found")

        # Check tax amount
        if '1,377' in full_text or '1377' in full_text:
            calc_checks += 1
            print(f"  Tax amount $1,377.00 found")
        else:
            print(f"  Tax amount $1,377.00 NOT found")

        # Check grand total
        if '17,577' in full_text or '17577' in full_text:
            calc_checks += 1
            print(f"  Grand total $17,577.00 found")
        else:
            print(f"  Grand total $17,577.00 NOT found")

        if calc_checks == total_calc:
            print(f"PASS: Component 3 — All calculations correct (0.20 pts)")
            total_score += 0.20
        elif calc_checks > 0:
            partial = round(0.20 * calc_checks / total_calc, 2)
            print(f"PARTIAL: Component 3 — {calc_checks}/{total_calc} calculations correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No correct calculations found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ---------------------------------------------------------------
    # Component 4: Invoice date filled (0.15 points)
    # Initial has "[date]" placeholder; golden should have an actual date.
    # ---------------------------------------------------------------
    try:
        paragraphs = get_odt_text_paragraphs(odt_path)
        full_text = '\n'.join(paragraphs)

        # The date should NOT be a placeholder
        has_placeholder_date = '[date]' in full_text
        # Check for a real date — look for month names or date patterns
        import re
        date_pattern = re.compile(
            r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}'
            r'|\d{1,2}/\d{1,2}/\d{4}'
            r'|\d{4}-\d{2}-\d{2}'
        )
        has_real_date = bool(date_pattern.search(full_text))

        if not has_placeholder_date and has_real_date:
            print(f"PASS: Component 4 — Invoice date filled with real date (0.15 pts)")
            total_score += 0.15
        elif has_placeholder_date:
            print(f"FAIL: Component 4 — Date placeholder '[date]' still present")
        else:
            print(f"FAIL: Component 4 — No recognizable date found in document")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ---------------------------------------------------------------
    # Component 5: PDF exported to correct path (0.25 points)
    # /home/user/invoices/INV-2025-0384.pdf should exist with correct content
    # ---------------------------------------------------------------
    try:
        pdf_dir = os.path.join(WORKDIR, 'invoices')
        pdf_path = os.path.join(pdf_dir, f'{invoice_number}.pdf')

        if not os.path.exists(pdf_path):
            print(f"FAIL: Component 5 — PDF not found at {pdf_path}")
        else:
            pdf_size = os.path.getsize(pdf_path)
            if pdf_size < 500:
                print(f"FAIL: Component 5 — PDF exists but too small ({pdf_size} bytes), likely corrupted")
            else:
                # Verify PDF has meaningful content by checking it's a real PDF
                with open(pdf_path, 'rb') as f:
                    header = f.read(5)
                if header == b'%PDF-':
                    # Try to extract text and verify key content is present
                    pdf_has_content = False
                    try:
                        import fitz
                        pdf_doc = fitz.open(pdf_path)
                        pdf_text = ''
                        for page in pdf_doc:
                            pdf_text += page.get_text()
                        pdf_doc.close()
                        # Verify PDF contains the invoice number and at least one line item
                        if invoice_number in pdf_text and any(item['description'] in pdf_text for item in line_items[:2]):
                            pdf_has_content = True
                    except ImportError:
                        # If fitz not available, accept valid PDF header + reasonable size
                        if pdf_size > 5000:
                            pdf_has_content = True

                    if pdf_has_content:
                        print(f"PASS: Component 5 — PDF exported correctly at {pdf_path} ({pdf_size} bytes) with invoice content (0.25 pts)")
                        total_score += 0.25
                    else:
                        # Partial credit: PDF exists and is valid but content unclear
                        print(f"PARTIAL: Component 5 — PDF exists at {pdf_path} but content verification inconclusive (0.15 pts)")
                        total_score += 0.15
                else:
                    print(f"FAIL: Component 5 — File at {pdf_path} is not a valid PDF")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
odt_path = f'{WORKDIR}/{TASK_ID}.odt'
if not os.path.exists(odt_path):
    print(f"File not found: {odt_path}")
    print("REWARD: 0.0")
else:
    verify_task(odt_path)

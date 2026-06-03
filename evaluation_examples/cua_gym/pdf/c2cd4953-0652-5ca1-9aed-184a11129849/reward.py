"""
FINAL REWARD SCRIPT - SUCCESS
Task: Please perform OCR on the invoice 'scanned_invoice.pdf' in /home/user/Documents/Finance and extract key fields (Invoice #, Date, Amount, Vendor) to 'invoice_data.json'.
Generated: 2025-11-29 10:08:44
Status: success
Model: o3
Total Steps: 7
"""

import json
import re
from pathlib import Path
from typing import Dict
from PyPDF2 import PdfReader

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------
PDF_PATH = Path('/home/user/Documents/Finance/scanned_invoice.pdf')
JSON_PATH = Path('/home/user/Documents/Finance/invoice_data.json')

# Regex patterns to pull values out of OCR-extracted text
FIELD_PATTERNS: Dict[str, str] = {
    'Invoice #': r'Invoice\s*#\s*([A-Za-z0-9\-]+)',
    'Date':       r'Date\s*([0-9]{4}[-/][0-9]{2}[-/][0-9]{2})',
    'Vendor':     r'Vendor\s*([A-Za-z][A-Za-z0-9 &,.]+)',
    'Amount':     r'Amount\s*\$?([0-9,]+\.?[0-9]*)'
}

# Acceptable JSON key variants for each logical field
KEY_SYNONYMS: Dict[str, list[str]] = {
    'Invoice #': ['Invoice #', 'InvoiceNumber', 'Invoice_No'],
    'Date':       ['Date', 'InvoiceDate'],
    'Vendor':     ['Vendor', 'Supplier'],
    'Amount':     ['Amount', 'Total', 'TotalAmount']
}

# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def normalize_amount(value: str) -> str:
    """Strip everything except digits & dots for reliable numeric comparison."""
    return re.sub(r'[^0-9.]', '', value or '')


def extract_pdf_text(pdf_path: Path) -> str:
    """Concatenate text from all PDF pages using PyPDF2 OCR output."""
    reader = PdfReader(str(pdf_path))
    texts = []
    for idx, page in enumerate(reader.pages):
        page_text = page.extract_text() or ''
        texts.append(page_text)
        print(f"Page {idx+1} extracted chars: {len(page_text)}")
    return "\n".join(texts)


def extract_fields_from_text(text: str) -> Dict[str, str]:
    """Apply regex patterns to pull required field values from the OCR text."""
    extracted: Dict[str, str] = {}
    for field, pattern in FIELD_PATTERNS.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            extracted[field] = match.group(1).strip()
            print(f"✓ Extracted {field}: {extracted[field]}")
        else:
            print(f"✗ Failed to extract {field}")
    return extracted


def lookup_json_value(data: Dict, field: str):
    """Return the value from JSON using any accepted key variant for the field."""
    for key in KEY_SYNONYMS.get(field, [field]):
        if key in data:
            return data[key]
    return None

# --------------------------------------------------
# MAIN VERIFICATION LOGIC
# --------------------------------------------------

def verify_task() -> float:
    print("Verifying OCR extraction task…")
    total_score = 0.0  # Progressive scoring up to 1.0

    # ---------- 1. Verify OCR text extraction quality (0.3) ----------
    if not PDF_PATH.exists():
        print(f"✗ Missing PDF at {PDF_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        ocr_text = extract_pdf_text(PDF_PATH)
    except Exception as e:
        print(f"✗ Error reading PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    key_labels_present = [lbl for lbl in ['Invoice', 'Date', 'Vendor', 'Amount'] if lbl.lower() in ocr_text.lower()]
    if len(ocr_text.strip()) > 30 and len(key_labels_present) >= 3:
        print("✓ OCR text appears sufficiently populated")
        total_score += 0.3
    else:
        print("✗ OCR text seems incomplete (quality sub-score lost)")

    # ---------- 2. Extract required fields from OCR text (0.3) ----------
    extracted_fields = extract_fields_from_text(ocr_text)
    field_extraction_score = 0.075 * sum(1 for f in FIELD_PATTERNS if f in extracted_fields)
    total_score += field_extraction_score  # up to 0.3

    # ---------- 3. Verify JSON file exists & includes keys (0.2) ----------
    json_data = None
    if JSON_PATH.exists():
        try:
            json_data = json.loads(JSON_PATH.read_text())
            print(f"✓ Found & parsed JSON at {JSON_PATH}")
        except Exception as e:
            print(f"✗ Failed to parse JSON: {e}")
    else:
        print(f"✗ JSON file not found at {JSON_PATH}")

    if json_data is not None:
        json_key_score = 0.05 * sum(1 for f in FIELD_PATTERNS if lookup_json_value(json_data, f) is not None)
        total_score += json_key_score  # up to 0.2
        for f in FIELD_PATTERNS:
            if lookup_json_value(json_data, f) is not None:
                print(f"✓ JSON contains value for {f}")
            else:
                print(f"✗ JSON missing value for {f}")

    # ---------- 4. Compare PDF-extracted values with JSON values (0.2) ----------
    if json_data is not None and extracted_fields:
        match_count = 0
        for field, pdf_val in extracted_fields.items():
            json_val = lookup_json_value(json_data, field)
            if json_val is None:
                continue
            if field == 'Amount':
                pdf_norm, json_norm = normalize_amount(pdf_val), normalize_amount(json_val)
            else:
                pdf_norm = pdf_val.strip().upper().replace('$', '')
                json_norm = str(json_val).strip().upper().replace('$', '')
            if pdf_norm == json_norm:
                print(f"✓ {field} matches between PDF and JSON")
                match_count += 1
            else:
                print(f"✗ {field} mismatch (PDF='{pdf_val}' vs JSON='{json_val}')")
        total_score += 0.05 * match_count  # up to 0.2

    # ---------- Final score ----------
    final_score = round(min(total_score, 1.0), 2)
    print(f"Total computed score: {final_score}")
    print(f"REWARD: {final_score}")
    return final_score

# Run verification when executed directly
if __name__ == "__main__":
    verify_task()

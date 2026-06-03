"""
Reward Script: Redact phone numbers from client contact PDF
Task ID: pdf_fin_057
Domain: pdf (libreoffice_calc tagged but actually PDF task)
Scoring:
  Component 1: Redacted file exists and has 3 pages (0.15)
  Component 2: Zero phone numbers in redacted text (0.40)
  Component 3: Client names preserved (0.15)
  Component 4: Non-phone text preserved (email, addresses) (0.15)
  Component 5: Black redaction rectangles present (0.15)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_057'

# Phone number patterns to check
PHONE_PATTERNS = [
    r'\(\d{3}\)\s*\d{3}-\d{4}',   # (XXX) XXX-XXXX
    r'\d{3}-\d{3}-\d{4}',          # XXX-XXX-XXXX
    r'\d{3}\.\d{3}\.\d{4}',        # XXX.XXX.XXXX
]

# Known client names from the contact directory (sample to verify preservation)
EXPECTED_NAMES = [
    'Sarah Chen',
    'Marcus Johnson',
    'Elena Rodriguez',
    'David Kim',
    'Lisa Chang',
    'Robert Martinez',
    'Jennifer Lee',
    'Christopher Davis',
]

def count_phone_numbers(text):
    """Count all phone number matches across all patterns."""
    total = 0
    for pat in PHONE_PATTERNS:
        total += len(re.findall(pat, text))
    return total

def verify_task(file_path):
    """
    Verify phone number redaction with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    import fitz
    total_score = 0.0

    # Precondition: file must exist (gate, not scoring)
    if not os.path.exists(file_path):
        print(f"CRITICAL: Redacted file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Redacted file has exactly 3 pages (0.15 points)
    # This verifies the output file structure matches the original
    try:
        page_count = len(doc)
        if page_count == 3:
            print(f"PASS: Component 1 - PDF has 3 pages (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 - Expected 3 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Extract all text from the redacted PDF
    all_text = ''
    for page in doc:
        all_text += page.get_text()

    # Component 2: Zero phone numbers in redacted text (0.40 points)
    # This is the core task requirement - all phone numbers must be redacted
    try:
        phone_count = count_phone_numbers(all_text)
        if phone_count == 0:
            print(f"PASS: Component 2 - Zero phone numbers found in redacted PDF (0.40 pts)")
            total_score += 0.40
        else:
            # Partial credit proportional to removal ratio
            if phone_count < 24:
                partial = round(0.40 * max(0, (24 - phone_count) / 24), 2)
                total_score += partial
                print(f"FAIL: Component 2 - Found {phone_count} remaining (partial: {partial} pts)")
            else:
                print(f"FAIL: Component 2 - All {phone_count} phone numbers still present")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Client names preserved in redacted PDF (0.15 points)
    # Verifies that non-phone data was not accidentally removed
    try:
        names_found = 0
        for name in EXPECTED_NAMES:
            if name in all_text:
                names_found += 1
        name_ratio = names_found / len(EXPECTED_NAMES)
        if name_ratio >= 0.75:
            print(f"PASS: Component 3 - {names_found}/{len(EXPECTED_NAMES)} client names preserved (0.15 pts)")
            total_score += 0.15
        elif name_ratio > 0:
            partial = round(0.15 * name_ratio, 2)
            print(f"FAIL: Component 3 - Only {names_found}/{len(EXPECTED_NAMES)} client names found (partial: {partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 - No client names found in redacted PDF")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Non-phone text preserved (emails and addresses) (0.15 points)
    # Check that emails and addresses survived the redaction
    try:
        # Check for email addresses that should still be present
        email_pattern = r'[\w.]+@[\w.]+\.\w+'
        emails_found = len(re.findall(email_pattern, all_text))
        # Check for address-like content (street names)
        has_addresses = any(word in all_text for word in ['Street', 'Ave', 'Dr', 'Blvd', 'St,'])

        if emails_found >= 6 and has_addresses:
            print(f"PASS: Component 4 - {emails_found} emails and addresses preserved (0.15 pts)")
            total_score += 0.15
        elif emails_found >= 3 or has_addresses:
            print(f"PARTIAL: Component 4 - {emails_found} emails, addresses={'present' if has_addresses else 'missing'} (0.08 pts)")
            total_score += 0.08
        else:
            print(f"FAIL: Component 4 - Non-phone content appears to be missing ({emails_found} emails found)")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Redaction marks (black rectangles/drawings) present (0.15 points)
    # Verifies that proper redaction was applied, not just text deletion
    try:
        total_drawings = 0
        for page in doc:
            drawings = page.get_drawings()
            total_drawings += len(drawings)

        if total_drawings >= 20:
            print(f"PASS: Component 5 - {total_drawings} redaction drawings found across pages (0.15 pts)")
            total_score += 0.15
        elif total_drawings > 0:
            partial = round(0.15 * min(total_drawings / 20, 1.0), 2)
            print(f"PARTIAL: Component 5 - Only {total_drawings} drawings found (partial: {partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 - No redaction drawings/rectangles found")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/finance/client_contacts_redacted.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

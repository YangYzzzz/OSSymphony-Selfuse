"""
Reward Script: Mail merge with filter — only records where InvoiceAmount > 500
Task ID: writer_mt_022
Domain: libreoffice_writer
Scoring:
  Component 1 (0.30): Merge executed — document contains multiple merged letters (not just template)
  Component 2 (0.30): Correct number of merged letters (exactly 22)
  Component 3 (0.25): All merged amounts are > 500 (filter correctly applied)
  Component 4 (0.15): Each merged letter preserves template structure (heading, Dear line, invoice fields)
"""

import os
import re
import csv

WORKDIR = '/home/user'
TASK_ID = 'writer_mt_022'


def persist_app_state(domain: str):
    """Save any unsaved GUI state before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_writer", "libreoffice_calc", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify mail merge task completion with progressive scoring.
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

    # Extract key structural elements from the document
    all_paragraphs = doc.paragraphs
    heading_paragraphs = [p for p in all_paragraphs
                          if p.style.name == 'Heading 1' and p.text.strip() == 'Payment Reminder']
    dear_paragraphs = [p for p in all_paragraphs if p.text.strip().startswith('Dear ')]
    amount_paragraphs = [p for p in all_paragraphs if p.text.strip().startswith('Invoice Amount:')]

    num_headings = len(heading_paragraphs)
    num_dear = len(dear_paragraphs)
    num_amounts = len(amount_paragraphs)

    print(f"INFO: Found {num_headings} 'Payment Reminder' headings")
    print(f"INFO: Found {num_dear} 'Dear ...' lines")
    print(f"INFO: Found {num_amounts} 'Invoice Amount:' lines")

    # =========================================================================
    # Component 1: Merge executed — multiple merged letters exist (0.30 points)
    # The initial template has exactly 1 heading. A merged doc must have > 1.
    # =========================================================================
    try:
        if num_headings > 1 and num_dear > 1 and num_amounts > 1:
            print(f"PASS: Component 1 — Merge executed, {num_headings} letters found (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — No merge detected. Headings={num_headings}, "
                  f"Dear lines={num_dear}, Amounts={num_amounts}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # =========================================================================
    # Component 2: Correct number of merged letters — exactly 22 (0.30 points)
    # Task says 22 records have InvoiceAmount > 500, so 22 letters expected.
    # Award partial credit: 0.15 if within +/-3, full 0.30 if exactly 22.
    # =========================================================================
    try:
        if num_headings == 22:
            print(f"PASS: Component 2 — Exactly 22 merged letters (0.30 pts)")
            total_score += 0.30
        elif num_headings > 1 and abs(num_headings - 22) <= 3:
            print(f"PARTIAL: Component 2 — {num_headings} letters (expected 22), within tolerance (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Expected 22 merged letters, found {num_headings}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # =========================================================================
    # Component 3: All merged amounts are > 500 — filter applied (0.25 points)
    # Extract dollar amounts and verify every one exceeds 500.
    # =========================================================================
    try:
        if num_amounts > 1:
            amounts = []
            parse_failures = 0
            for p in amount_paragraphs:
                text = p.text.strip()
                # Extract numeric value from "Invoice Amount: $X.XX" or "Invoice Amount: X.XX"
                match = re.search(r'[\$]?\s*([\d,]+\.?\d*)', text.split(':')[-1])
                if match:
                    val = float(match.group(1).replace(',', ''))
                    amounts.append(val)
                else:
                    parse_failures += 1

            if parse_failures > 0:
                print(f"WARN: Could not parse {parse_failures} amount lines")

            if len(amounts) > 0:
                all_above_500 = all(a > 500 for a in amounts)
                min_amount = min(amounts)
                if all_above_500:
                    print(f"PASS: Component 3 — All {len(amounts)} amounts > 500 "
                          f"(min={min_amount:.2f}) (0.25 pts)")
                    total_score += 0.25
                else:
                    below = [a for a in amounts if a <= 500]
                    print(f"FAIL: Component 3 — {len(below)} amounts <= 500. "
                          f"Min amount: {min_amount:.2f}")
            else:
                print(f"FAIL: Component 3 — No amounts could be parsed")
        else:
            print(f"FAIL: Component 3 — Not enough amount lines to verify filter ({num_amounts})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # =========================================================================
    # Component 4: Template structure preserved in each letter (0.15 points)
    # Each merged letter should have: heading, Dear line, Invoice Number,
    # Invoice Amount, Due Date, and closing signature.
    # Check that counts of key elements are consistent (all == num_headings).
    # =========================================================================
    try:
        invoice_num_paras = [p for p in all_paragraphs
                             if p.text.strip().startswith('Invoice Number:')]
        due_date_paras = [p for p in all_paragraphs
                          if p.text.strip().startswith('Due Date:')]
        sincerely_paras = [p for p in all_paragraphs
                           if p.text.strip() == 'Sincerely,']

        num_inv_nums = len(invoice_num_paras)
        num_due_dates = len(due_date_paras)
        num_sincerely = len(sincerely_paras)

        if (num_headings > 1 and
                num_inv_nums == num_headings and
                num_due_dates == num_headings and
                num_dear == num_headings and
                num_amounts == num_headings and
                num_sincerely == num_headings):
            print(f"PASS: Component 4 — All {num_headings} letters have consistent structure (0.15 pts)")
            total_score += 0.15
        elif num_headings > 1 and num_inv_nums >= num_headings - 2:
            # Partial: mostly intact structure
            print(f"PARTIAL: Component 4 — Structure mostly preserved. "
                  f"InvNums={num_inv_nums}, DueDates={num_due_dates}, "
                  f"Dear={num_dear}, Sincerely={num_sincerely} (0.08 pts)")
            total_score += 0.08
        else:
            print(f"FAIL: Component 4 — Structure not preserved. "
                  f"Headings={num_headings}, InvNums={num_inv_nums}, "
                  f"DueDates={num_due_dates}, Dear={num_dear}, "
                  f"Sincerely={num_sincerely}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
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

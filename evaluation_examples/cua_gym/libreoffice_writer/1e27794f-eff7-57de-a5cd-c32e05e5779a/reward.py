"""
Reward Script: Thank-you letter in LibreOffice Writer
Task ID: writer_wf_044
Domain: libreoffice_writer
Scoring:
  Component 1: Margins set to 2.54cm all around (0.15)
  Component 2: Right-aligned sender address block at top (0.15)
  Component 3: Date, recipient address, salutation present (0.20)
  Component 4: Two body paragraphs with thank-you content (0.20)
  Component 5: Complimentary close "Sincerely," and sender name "Emily Roberts" (0.15)
  Component 6: Times New Roman 12pt font throughout (0.15)
"""

import os
from docx import Document
from docx.shared import Pt, Emu
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

WORKDIR = '/home/user'
TASK_ID = 'writer_wf_044'


def emu_to_cm(val):
    """Convert EMU to centimeters."""
    if val is None:
        return None
    return round(val / 360000, 2)


def persist_app_state(domain):
    """Try to save any unsaved document via Ctrl+S."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print(f"PERSIST: ctrl+s sent for {domain}")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


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

    paras = doc.paragraphs
    # Filter to non-empty paragraphs for structural checks
    non_empty = [p for p in paras if p.text.strip()]

    # Precondition: document must have meaningful content (at least 5 non-empty paragraphs)
    if len(non_empty) < 5:
        print(f"FAIL: Document has only {len(non_empty)} non-empty paragraphs, expected at least 5 for a letter")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Margins set to 2.54cm all around (0.15 points)
    # Initial has 3.17cm left/right margins; task requires 2.54cm all around
    try:
        s = doc.sections[0]
        left_cm = emu_to_cm(s.left_margin)
        right_cm = emu_to_cm(s.right_margin)
        top_cm = emu_to_cm(s.top_margin)
        bottom_cm = emu_to_cm(s.bottom_margin)
        tolerance = 0.1  # allow small rounding differences
        margins_ok = (
            abs(left_cm - 2.54) <= tolerance and
            abs(right_cm - 2.54) <= tolerance and
            abs(top_cm - 2.54) <= tolerance and
            abs(bottom_cm - 2.54) <= tolerance
        )
        # Additional check: left/right must NOT be ~3.17 (initial default)
        left_not_default = abs(left_cm - 3.17) > tolerance
        right_not_default = abs(right_cm - 3.17) > tolerance
        if margins_ok and left_not_default and right_not_default:
            print(f"PASS: Component 1 — Margins all 2.54cm (L={left_cm}, R={right_cm}, T={top_cm}, B={bottom_cm}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Margins not 2.54cm: L={left_cm}, R={right_cm}, T={top_cm}, B={bottom_cm}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Right-aligned sender address block at top (0.15 points)
    # The first few paragraphs should be right-aligned (sender address)
    try:
        right_aligned_count = 0
        for p in non_empty:
            if p.paragraph_format.alignment == WD_PARAGRAPH_ALIGNMENT.RIGHT:
                right_aligned_count += 1
            else:
                break  # stop at first non-right-aligned paragraph

        if right_aligned_count >= 2:
            # Check that at least one contains address-like content
            first_right_texts = [p.text.strip() for p in non_empty[:right_aligned_count]
                                 if p.paragraph_format.alignment == WD_PARAGRAPH_ALIGNMENT.RIGHT]
            print(f"PASS: Component 2 — {right_aligned_count} right-aligned sender lines at top: {first_right_texts[:2]}... (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Expected right-aligned sender block at top, found {right_aligned_count} right-aligned paragraphs")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Date, recipient address, and salutation "Dear Ms. Johnson," (0.20 points)
    try:
        all_text = '\n'.join(p.text.strip() for p in non_empty)
        all_text_lower = all_text.lower()
        sub_score = 0.0

        # 3a: Salutation "Dear Ms. Johnson," must be present (0.10)
        has_salutation = 'dear ms. johnson' in all_text_lower
        if has_salutation:
            print(f"PASS: Component 3a — Salutation 'Dear Ms. Johnson' found (0.10 pts)")
            sub_score += 0.10
        else:
            print(f"FAIL: Component 3a — Salutation 'Dear Ms. Johnson' not found")

        # 3b: Recipient address block (at least 2 left-aligned lines between right-aligned block and salutation) (0.05)
        # Find the salutation paragraph index in non_empty
        salutation_idx = None
        for i, p in enumerate(non_empty):
            if 'dear ms. johnson' in p.text.lower():
                salutation_idx = i
                break
        # Count left-aligned paragraphs between right-aligned block and salutation
        if salutation_idx and salutation_idx > right_aligned_count + 1:
            # There should be date + recipient lines between sender block end and salutation
            recipient_lines = non_empty[right_aligned_count:salutation_idx]
            left_recipient = [p for p in recipient_lines if p.paragraph_format.alignment in (WD_PARAGRAPH_ALIGNMENT.LEFT, None)]
            if len(left_recipient) >= 2:
                print(f"PASS: Component 3b — {len(left_recipient)} recipient/date lines found (0.05 pts)")
                sub_score += 0.05
            else:
                print(f"FAIL: Component 3b — Only {len(left_recipient)} lines between sender and salutation, expected >= 2")
        else:
            print(f"FAIL: Component 3b — Cannot identify recipient block (salutation_idx={salutation_idx}, right_count={right_aligned_count})")

        # 3c: Date present (some date-like text) (0.05)
        import re
        date_pattern = re.compile(r'(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2}', re.IGNORECASE)
        if date_pattern.search(all_text):
            print(f"PASS: Component 3c — Date found in document (0.05 pts)")
            sub_score += 0.05
        else:
            # Also check numeric date formats
            numeric_date = re.compile(r'\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4}')
            if numeric_date.search(all_text):
                print(f"PASS: Component 3c — Date (numeric) found in document (0.05 pts)")
                sub_score += 0.05
            else:
                print(f"FAIL: Component 3c — No date found in document")

        total_score += sub_score
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Two body paragraphs with thank-you/interview content (0.20 points)
    try:
        # Body paragraphs should be after salutation and before close
        # They should mention thanking for interview and reiterating interest
        body_paras = []
        if salutation_idx is not None:
            # Look for paragraphs after salutation that are not the close/signature
            for p in non_empty[salutation_idx + 1:]:
                text_lower = p.text.strip().lower()
                if text_lower.startswith('sincerely') or text_lower.startswith('yours') or text_lower.startswith('best') or text_lower.startswith('regards'):
                    break
                if len(p.text.strip()) > 30:  # body paragraphs should be substantial
                    body_paras.append(p)

        sub_score = 0.0
        if len(body_paras) >= 2:
            print(f"PASS: Component 4a — {len(body_paras)} body paragraphs found (0.10 pts)")
            sub_score += 0.10
        elif len(body_paras) == 1:
            print(f"PARTIAL: Component 4a — Only 1 body paragraph found (0.05 pts)")
            sub_score += 0.05
        else:
            print(f"FAIL: Component 4a — No substantial body paragraphs found")

        # Check content relevance: should mention thank/interview/interest
        body_text = ' '.join(p.text.lower() for p in body_paras)
        has_thank = 'thank' in body_text
        has_interview_or_interest = 'interview' in body_text or 'interest' in body_text or 'opportunity' in body_text
        if has_thank and has_interview_or_interest:
            print(f"PASS: Component 4b — Body mentions thanking and interview/interest (0.10 pts)")
            sub_score += 0.10
        elif has_thank or has_interview_or_interest:
            print(f"PARTIAL: Component 4b — Body partially relevant (0.05 pts)")
            sub_score += 0.05
        else:
            print(f"FAIL: Component 4b — Body does not mention thank-you or interview content")

        total_score += sub_score
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Complimentary close "Sincerely," and sender name "Emily Roberts" (0.15 points)
    try:
        sub_score = 0.0
        has_sincerely = any('sincerely' in p.text.lower() for p in non_empty)
        has_emily = any('emily roberts' in p.text.lower() for p in non_empty)

        if has_sincerely:
            print(f"PASS: Component 5a — 'Sincerely,' found (0.075 pts)")
            sub_score += 0.075
        else:
            print(f"FAIL: Component 5a — 'Sincerely,' not found")

        if has_emily:
            print(f"PASS: Component 5b — 'Emily Roberts' found (0.075 pts)")
            sub_score += 0.075
        else:
            print(f"FAIL: Component 5b — 'Emily Roberts' not found")

        total_score += sub_score
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Times New Roman 12pt font throughout (0.15 points)
    try:
        runs_with_font = []
        runs_with_size = []
        wrong_font = []
        wrong_size = []

        for p in non_empty:
            for run in p.runs:
                if not run.text.strip():
                    continue
                if run.font.name:
                    runs_with_font.append(run.font.name)
                    if run.font.name != 'Times New Roman':
                        wrong_font.append(run.font.name)
                if run.font.size:
                    runs_with_size.append(run.font.size.pt)
                    if abs(run.font.size.pt - 12.0) > 0.5:
                        wrong_size.append(run.font.size.pt)

        sub_score = 0.0
        if runs_with_font and not wrong_font:
            print(f"PASS: Component 6a — All {len(runs_with_font)} runs use Times New Roman (0.075 pts)")
            sub_score += 0.075
        elif wrong_font:
            print(f"FAIL: Component 6a — Found non-TNR fonts: {set(wrong_font)}")
        else:
            print(f"FAIL: Component 6a — No explicit font names found on runs")

        if runs_with_size and not wrong_size:
            print(f"PASS: Component 6b — All {len(runs_with_size)} runs are 12pt (0.075 pts)")
            sub_score += 0.075
        elif wrong_size:
            print(f"FAIL: Component 6b — Found non-12pt sizes: {set(wrong_size)}")
        else:
            print(f"FAIL: Component 6b — No explicit font sizes found on runs")

        total_score += sub_score
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(round(total_score, 4), 1.0)
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

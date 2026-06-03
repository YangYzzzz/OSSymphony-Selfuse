"""
Reward Script: Mail merge holiday greeting letter
Task ID: writer_mt_032
Domain: libreoffice_writer
Scoring:
  Component 1 (0.25): First paragraph starts with "Dear <ClientName>,"
  Component 2 (0.25): Body has holiday greeting content (at least 2 sentences)
  Component 3 (0.25): Closing contains "Warm regards," and "Global Solutions Inc."
  Component 4 (0.25): All text uses 12pt serif font (Times New Roman)
"""

import os
import re
from docx import Document
from docx.shared import Pt

WORKDIR = '/home/user'
TASK_ID = 'writer_mt_032'

# Known serif font families
SERIF_FONTS = {
    'times new roman', 'times', 'georgia', 'garamond', 'palatino',
    'palatino linotype', 'book antiqua', 'century', 'century schoolbook',
    'cambria', 'serif', 'liberation serif', 'dejavu serif',
}


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

    paragraphs = [p for p in doc.paragraphs if p.text.strip()]
    num_paras = len(paragraphs)

    if num_paras == 0:
        print("FAIL: Document is empty (no non-blank paragraphs)")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: First paragraph starts with "Dear <ClientName>," (0.25 points)
    # This checks the mail merge salutation line
    try:
        first_text = paragraphs[0].text.strip()
        # Accept variants: "Dear <ClientName>,", "Dear {ClientName},", etc.
        # The key requirement is "Dear" + some placeholder for ClientName + comma
        if re.match(r'^Dear\s+.*ClientName.*,', first_text, re.IGNORECASE):
            print(f"PASS: Component 1 — First line is '{first_text}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Expected 'Dear <ClientName>,' but found: '{first_text}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Body contains holiday greeting content with at least 2 sentences (0.25 points)
    # The body paragraphs (between salutation and closing) should have holiday-related content
    try:
        # Gather body text (paragraphs between first and closing)
        body_texts = []
        for p in paragraphs[1:]:
            t = p.text.strip().lower()
            # Stop at closing lines
            if t.startswith('warm regards') or t == 'global solutions inc.':
                break
            body_texts.append(p.text.strip())

        body_combined = ' '.join(body_texts)
        # Count sentences (rough: split by period, exclamation, question mark)
        sentences = [s.strip() for s in re.split(r'[.!?]+', body_combined) if s.strip()]
        num_sentences = len(sentences)

        # Check for holiday-related keywords
        holiday_keywords = ['holiday', 'season', 'wish', 'gratitude', 'new year',
                            'greeting', 'celebration', 'joy', 'warm', 'happy',
                            'festive', 'thankful', 'appreciate', 'prosper']
        body_lower = body_combined.lower()
        keyword_hits = sum(1 for kw in holiday_keywords if kw in body_lower)

        if num_sentences >= 2 and keyword_hits >= 2:
            print(f"PASS: Component 2 — Body has {num_sentences} sentences, {keyword_hits} holiday keywords (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Body has {num_sentences} sentences (need >=2), {keyword_hits} holiday keywords (need >=2)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Closing contains "Warm regards," and "Global Solutions Inc." (0.25 points)
    # These should appear at the end of the document
    try:
        all_text = '\n'.join(p.text.strip() for p in paragraphs)
        all_text_lower = all_text.lower()

        has_warm_regards = 'warm regards' in all_text_lower
        has_company = 'global solutions inc' in all_text_lower

        if has_warm_regards and has_company:
            print(f"PASS: Component 3 — Found 'Warm regards' and 'Global Solutions Inc.' in closing (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — Warm regards: {has_warm_regards}, Global Solutions Inc.: {has_company}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: All text uses 12pt serif font (0.25 points)
    # Task requires "12pt serif font" — verify font name is serif and size is 12pt
    try:
        runs_checked = 0
        runs_correct_size = 0
        runs_correct_font = 0

        for para in paragraphs:
            for run in para.runs:
                if not run.text.strip():
                    continue
                runs_checked += 1

                # Check size
                if run.font.size is not None and abs(run.font.size.pt - 12.0) < 0.5:
                    runs_correct_size += 1

                # Check serif font
                if run.font.name and run.font.name.lower() in SERIF_FONTS:
                    runs_correct_font += 1

        if runs_checked == 0:
            print("FAIL: Component 4 — No runs with text found")
        else:
            size_ratio = runs_correct_size / runs_checked
            font_ratio = runs_correct_font / runs_checked

            if size_ratio >= 0.8 and font_ratio >= 0.8:
                print(f"PASS: Component 4 — {runs_correct_size}/{runs_checked} runs at 12pt, {runs_correct_font}/{runs_checked} runs serif (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 — Size OK: {runs_correct_size}/{runs_checked} ({size_ratio:.0%}), Serif OK: {runs_correct_font}/{runs_checked} ({font_ratio:.0%})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

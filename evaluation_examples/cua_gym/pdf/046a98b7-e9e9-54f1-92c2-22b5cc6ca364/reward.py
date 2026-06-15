"""
Reward Script: Create a PDF form with specific fields
Task ID: pdf_cr_018
Domain: pdf
Scoring:
  - Component 1 (0.15): PDF exists with 1 page and title text
  - Component 2 (0.25): 'full_name' Text widget with value 'John Doe'
  - Component 3 (0.15): 'email' Text widget exists
  - Component 4 (0.20): 'agree_terms' CheckBox widget, unchecked
  - Component 5 (0.25): 'department' ComboBox widget with 5 choices
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_018'
FILE_PATH = os.path.join(WORKDIR, 'Desktop', 'application.pdf')


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
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: PDF has 1 page and contains title 'Job Application Form' (0.15 pts)
    try:
        page_count = len(doc)
        has_one_page = (page_count == 1)
        text = doc[0].get_text('text') if page_count > 0 else ''
        has_title = 'Job Application Form' in text
        if has_one_page and has_title:
            print(f"PASS: Component 1 -- 1 page with title 'Job Application Form' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- pages={page_count}, title_found={has_title}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Build widget lookup from all pages
    widgets = {}
    try:
        for page_idx in range(len(doc)):
            page = doc[page_idx]
            for w in page.widgets():
                widgets[w.field_name] = {
                    'type': w.field_type_string,
                    'value': w.field_value,
                    'choices': w.choice_values,
                    'rect': tuple(w.rect),
                }
        print(f"INFO: Found {len(widgets)} widget(s): {list(widgets.keys())}")
    except Exception as e:
        print(f"ERROR: Could not enumerate widgets: {e}")

    # Component 2: 'full_name' widget exists, type Text, value 'John Doe' (0.25 pts)
    try:
        if 'full_name' in widgets:
            w = widgets['full_name']
            is_text = (w['type'] == 'Text')
            has_value = (w['value'] == 'John Doe')
            if is_text and has_value:
                print(f"PASS: Component 2 -- 'full_name' Text widget with value 'John Doe' (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 -- full_name type={w['type']}, value={repr(w['value'])}")
        else:
            print(f"FAIL: Component 2 -- 'full_name' widget not found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: 'email' widget exists with type Text (0.15 pts)
    try:
        if 'email' in widgets:
            w = widgets['email']
            if w['type'] == 'Text':
                print(f"PASS: Component 3 -- 'email' Text widget exists (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 -- email type={w['type']}, expected Text")
        else:
            print(f"FAIL: Component 3 -- 'email' widget not found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: 'agree_terms' CheckBox widget, unchecked (0.20 pts)
    try:
        if 'agree_terms' in widgets:
            w = widgets['agree_terms']
            is_checkbox = (w['type'] == 'CheckBox')
            # Unchecked checkbox has value 'Off' or empty string
            is_unchecked = (w['value'] in ('Off', '', 'No', None))
            if is_checkbox and is_unchecked:
                print(f"PASS: Component 4 -- 'agree_terms' CheckBox, unchecked (value={repr(w['value'])}) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 -- agree_terms type={w['type']}, value={repr(w['value'])}")
        else:
            print(f"FAIL: Component 4 -- 'agree_terms' widget not found")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: 'department' ComboBox widget with 5 choices (0.25 pts)
    try:
        if 'department' in widgets:
            w = widgets['department']
            is_combo = (w['type'] == 'ComboBox')
            choices = w.get('choices') or []
            has_five_choices = (len(choices) == 5)
            expected_choices = {'Engineering', 'Marketing', 'Finance', 'HR', 'Operations'}
            choices_match = (set(choices) == expected_choices) if choices else False
            if is_combo and has_five_choices and choices_match:
                print(f"PASS: Component 5 -- 'department' ComboBox with 5 correct choices (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 5 -- department type={w['type']}, choices={choices}")
        else:
            print(f"FAIL: Component 5 -- 'department' widget not found")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

"""
Reward Script: Create a PDF form (Customer Satisfaction Survey)
Task ID: pdf_ro_029
Domain: pdf
Scoring:
  Component 1 (0.10): PDF file exists and is a valid single-page PDF
  Component 2 (0.15): Title 'Customer Satisfaction Survey' present on page
  Component 3 (0.25): Three text fields exist: 'name', 'email', 'feedback'
  Component 4 (0.15): 'feedback' field is multi-line and ~3 inches tall
  Component 5 (0.20): Five radio buttons for rating (1-5)
  Component 6 (0.15): Push button labeled 'Submit Survey'
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_029'

def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist (this IS a task change -- file doesn't exist initially)
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import pymupdf
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Valid single-page PDF (0.10 points)
    # This fails on initial_env (no file) and passes on golden_env
    try:
        page_count = doc.page_count
        if page_count >= 1:
            print(f"PASS: Component 1 -- Valid PDF with {page_count} page(s) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 -- PDF has no pages")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    page = doc[0]

    # Component 2: Title 'Customer Satisfaction Survey' present (0.15 points)
    try:
        text = page.get_text()
        if 'Customer Satisfaction Survey' in text:
            print(f"PASS: Component 2 -- Title 'Customer Satisfaction Survey' found (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 -- Title not found in page text: {text[:200]!r}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Collect all form fields
    try:
        fields = []
        for w in page.widgets():
            fields.append({
                "name": w.field_name,
                "type_str": w.field_type_string,
                "type": w.field_type,
                "rect": tuple(w.rect),
                "flags": w.field_flags,
                "button_caption": w.button_caption if hasattr(w, 'button_caption') else None,
            })
    except Exception as e:
        print(f"ERROR: Could not enumerate widgets: {e}")
        fields = []

    # Component 3: Three text fields: 'name', 'email', 'feedback' (0.25 points)
    try:
        text_fields = [f for f in fields if f["type_str"] == "Text"]
        text_field_names = {f["name"] for f in text_fields}
        required_names = {"name", "email", "feedback"}
        found = required_names & text_field_names
        if found == required_names:
            print(f"PASS: Component 3 -- All 3 text fields found: {found} (0.25 pts)")
            total_score += 0.25
        else:
            missing = required_names - found
            print(f"FAIL: Component 3 -- Missing text fields: {missing}. Found: {text_field_names}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: 'feedback' field is multi-line and ~3 inches tall (0.15 points)
    # 3 inches = 216 points. Allow tolerance of +/- 36 pts (0.5 inch)
    try:
        feedback_fields = [f for f in fields if f["name"] == "feedback" and f["type_str"] == "Text"]
        if feedback_fields:
            fb = feedback_fields[0]
            rect = fb["rect"]  # (x0, y0, x1, y1)
            height = rect[3] - rect[1]
            is_multiline = (fb["flags"] & 4096) != 0  # PDF_TX_FIELD_IS_MULTILINE = 4096
            height_ok = abs(height - 216.0) <= 36.0  # ~3 inches with 0.5 inch tolerance

            if is_multiline and height_ok:
                print(f"PASS: Component 4 -- feedback is multi-line, height={height:.1f}pt (~{height/72:.1f}in) (0.15 pts)")
                total_score += 0.15
            elif is_multiline:
                # Partial: multi-line but wrong height
                print(f"PARTIAL: Component 4 -- feedback is multi-line but height={height:.1f}pt (~{height/72:.1f}in), expected ~216pt (0.07 pts)")
                total_score += 0.07
            else:
                print(f"FAIL: Component 4 -- feedback field not multi-line (flags={fb['flags']}), height={height:.1f}pt")
        else:
            print(f"FAIL: Component 4 -- No 'feedback' text field found")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Five radio buttons for rating (0.20 points)
    try:
        radio_fields = [f for f in fields if f["type_str"] == "RadioButton"]
        radio_count = len(radio_fields)
        if radio_count == 5:
            print(f"PASS: Component 5 -- 5 radio buttons found (0.20 pts)")
            total_score += 0.20
        elif radio_count >= 3:
            partial = 0.10
            print(f"PARTIAL: Component 5 -- {radio_count} radio buttons found, expected 5 ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 -- {radio_count} radio buttons found, expected 5")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: Push button labeled 'Submit Survey' (0.15 points)
    try:
        buttons = [f for f in fields if f["type_str"] == "Button"]
        # Check button captions for 'Submit Survey'
        submit_captions = [btn.get("button_caption", "") or "" for btn in buttons]
        has_submit_btn = any("Submit Survey" in c for c in submit_captions)
        # Fallback: check page text if a button exists but caption extraction failed
        if not has_submit_btn and buttons:
            has_submit_btn = "Submit Survey" in (page.get_text() or "")

        if has_submit_btn:
            print(f"PASS: Component 6 -- Submit Survey button found (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 6 -- No button with 'Submit Survey' label. Buttons: {[(b['name'], b.get('button_caption')) for b in buttons]}")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/forms/survey.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

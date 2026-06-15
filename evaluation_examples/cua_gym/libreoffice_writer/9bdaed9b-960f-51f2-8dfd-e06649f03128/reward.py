"""
Reward Script: Add checkbox form controls to survey questionnaire
Task ID: writer_rd_038
Domain: libreoffice_writer
Scoring:
  Component 1 (0.30): Checkbox form fields exist (>=16 w:checkBox elements)
  Component 2 (0.30): Each question followed by Yes/No label paragraph
  Component 3 (0.25): Checkboxes named with Yes/No pattern
  Component 4 (0.15): All 8 original questions preserved
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_rd_038'

# The 8 expected survey questions (key phrases to match)
QUESTION_PHRASES = [
    "satisfied with our overall service",
    "recommend our company",
    "respond to your inquiries",
    "range of products",
    "pricing is fair",
    "checkout process",
    "issues with product delivery",
    "purchasing from us again",
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
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

    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    body = doc.element.body

    # Component 1: Checkbox form fields exist (0.30 points)
    # The golden doc should have 16 checkbox form fields (2 per question x 8 questions)
    # Initial doc has 0. This is a task-introduced change.
    try:
        checkboxes = body.findall('.//w:checkBox', ns)
        num_checkboxes = len(checkboxes)
        if num_checkboxes >= 16:
            print(f"PASS: Component 1 — Found {num_checkboxes} checkbox form fields (>=16 required) (0.30 pts)")
            total_score += 0.30
        elif num_checkboxes >= 8:
            partial = 0.15
            print(f"PARTIAL: Component 1 — Found {num_checkboxes} checkbox form fields (>=16 required, >=8 for partial) ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — Found {num_checkboxes} checkbox form fields, need >=16")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Each question is followed by a paragraph with Yes and No labels (0.30 points)
    # In initial doc, questions are NOT followed by Yes/No paragraphs. This is task-introduced.
    try:
        paras = doc.paragraphs
        para_texts = [p.text for p in paras]
        questions_with_yn = 0

        for q_idx, phrase in enumerate(QUESTION_PHRASES):
            # Find the paragraph containing this question
            q_para_idx = None
            for i, text in enumerate(para_texts):
                if phrase.lower() in text.lower():
                    q_para_idx = i
                    break

            if q_para_idx is not None and q_para_idx + 1 < len(para_texts):
                next_text = para_texts[q_para_idx + 1].lower()
                if 'yes' in next_text and 'no' in next_text:
                    questions_with_yn += 1

        if questions_with_yn >= 8:
            print(f"PASS: Component 2 — All {questions_with_yn}/8 questions have Yes/No paragraphs (0.30 pts)")
            total_score += 0.30
        elif questions_with_yn >= 4:
            partial = round(0.30 * questions_with_yn / 8, 2)
            print(f"PARTIAL: Component 2 — {questions_with_yn}/8 questions have Yes/No paragraphs ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Only {questions_with_yn}/8 questions have Yes/No paragraphs")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Checkboxes are named with Yes/No pattern (0.25 points)
    # The golden has names like Check1_Yes, Check1_No, etc.
    # We check that ffData elements have names containing 'yes' or 'no' (case-insensitive).
    try:
        ffdata_elements = body.findall('.//w:ffData', ns)
        w_ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
        yes_count = 0
        no_count = 0
        for ff in ffdata_elements:
            name_el = ff.find('w:name', ns)
            if name_el is not None:
                name_val = name_el.get(f'{{{w_ns}}}val') or ''
                name_lower = name_val.lower()
                if 'yes' in name_lower:
                    yes_count += 1
                elif 'no' in name_lower:
                    no_count += 1

        # Also check via the text labels next to checkboxes in paragraphs that have form fields
        # The naming convention is the primary check
        if yes_count >= 8 and no_count >= 8:
            print(f"PASS: Component 3 — Found {yes_count} 'Yes' and {no_count} 'No' named checkboxes (0.25 pts)")
            total_score += 0.25
        elif yes_count >= 4 and no_count >= 4:
            partial = round(0.25 * min(yes_count, no_count) / 8, 2)
            print(f"PARTIAL: Component 3 — Found {yes_count} 'Yes' and {no_count} 'No' named checkboxes ({partial} pts)")
            total_score += partial
        else:
            # Fallback: check if checkboxes exist in paragraphs that contain Yes/No text
            # Some implementations may not name them but still have labels
            cb_paras_with_labels = 0
            for p in paras:
                p_xml = p._element
                has_cb = len(p_xml.findall('.//w:checkBox', ns)) > 0
                text = p.text.lower()
                if has_cb and ('yes' in text or 'no' in text):
                    cb_paras_with_labels += 1
            if cb_paras_with_labels >= 8:
                print(f"PASS: Component 3 — {cb_paras_with_labels} paragraphs have checkboxes with Yes/No text labels (0.25 pts)")
                total_score += 0.25
            elif cb_paras_with_labels >= 4:
                partial = round(0.25 * cb_paras_with_labels / 8, 2)
                print(f"PARTIAL: Component 3 — {cb_paras_with_labels} paragraphs have checkboxes with labels ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — Only {yes_count} 'Yes' and {no_count} 'No' named checkboxes, {cb_paras_with_labels} labeled paragraphs")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: All 8 original questions preserved (0.15 points)
    # This is a compound check: questions must still exist AND have checkboxes nearby.
    # The question text itself exists in initial too, but we combine with checkbox presence
    # to make this a task-change check (questions + form controls = task done).
    try:
        questions_found = 0
        questions_with_nearby_cb = 0
        for phrase in QUESTION_PHRASES:
            for i, text in enumerate(para_texts):
                if phrase.lower() in text.lower():
                    questions_found += 1
                    # Check if the next paragraph has checkboxes
                    if i + 1 < len(paras):
                        next_p_xml = paras[i + 1]._element
                        cbs_in_next = next_p_xml.findall('.//w:checkBox', ns)
                        if len(cbs_in_next) > 0:
                            questions_with_nearby_cb += 1
                    break

        if questions_with_nearby_cb >= 8:
            print(f"PASS: Component 4 — All {questions_with_nearby_cb}/8 questions preserved with adjacent checkboxes (0.15 pts)")
            total_score += 0.15
        elif questions_with_nearby_cb >= 4:
            partial = round(0.15 * questions_with_nearby_cb / 8, 2)
            print(f"PARTIAL: Component 4 — {questions_with_nearby_cb}/8 questions have adjacent checkboxes ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — Only {questions_with_nearby_cb}/8 questions have adjacent checkboxes (questions found: {questions_found})")
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

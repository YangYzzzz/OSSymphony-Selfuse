"""
Reward Script: Create an interactive fillable PDF form (employee survey)
Task ID: pdf_gf3_011
Domain: pdf
Scoring:
  - Component 1 (0.10): PDF file exists and is valid
  - Component 2 (0.30): 5 text input fields present (Name, Department, Manager, Start Date, Years of Service)
  - Component 3 (0.30): 3 radio button groups with correct option counts (Performance:4, Satisfaction:5, Recommend:2)
  - Component 4 (0.15): Multiline comments text area present
  - Component 5 (0.15): Submit button present
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_011'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: PDF file exists and is a valid, loadable PDF (0.10 points)
    # NOTE: File does NOT exist on initial_env, so this scores the task-introduced change.
    try:
        doc = pymupdf.open(file_path)
        if doc.page_count >= 1:
            print(f"PASS: Component 1 — PDF is valid with {doc.page_count} page(s) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — PDF has 0 pages")
            doc.close()
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all widgets across all pages
    all_widgets = []
    for pi in range(doc.page_count):
        page = doc[pi]
        for w in page.widgets():
            all_widgets.append({
                "name": w.field_name,
                "type_name": w.field_type_string,
                "type": w.field_type,
                "value": w.field_value,
                "flags": w.field_flags,
                "rect": tuple(w.rect),
                "choices": w.choice_values,
            })

    # Component 2: 5 text input fields for personal information (0.30 points)
    # Expected field names (flexible matching — check for keywords)
    expected_text_keywords = ["name", "department", "manager", "start_date", "years"]
    try:
        text_widgets = [w for w in all_widgets if w["type_name"] == "Text"]
        # Filter out multiline fields (comments) and button-like fields
        # We look for single-line text fields that match expected personal info fields
        single_line_text = [w for w in text_widgets if not (w["flags"] & 4096)]  # 4096 = multiline flag

        matched_fields = 0
        matched_names = []
        for keyword in expected_text_keywords:
            for w in single_line_text:
                wname = (w["name"] or "").lower()
                if keyword in wname:
                    matched_fields += 1
                    matched_names.append(w["name"])
                    break

        if matched_fields >= 5:
            print(f"PASS: Component 2 — All 5 text fields found: {matched_names} (0.30 pts)")
            total_score += 0.30
        elif matched_fields >= 3:
            partial = round(0.30 * matched_fields / 5, 2)
            print(f"PARTIAL: Component 2 — {matched_fields}/5 text fields found: {matched_names} ({partial} pts)")
            total_score += partial
        else:
            # Fallback: just count text fields that aren't multiline
            # Some implementations may use different naming conventions
            if len(single_line_text) >= 5:
                print(f"PASS: Component 2 — Found {len(single_line_text)} single-line text fields (names may differ) (0.30 pts)")
                total_score += 0.30
            elif len(single_line_text) >= 3:
                partial = round(0.30 * min(len(single_line_text), 5) / 5, 2)
                print(f"PARTIAL: Component 2 — Found {len(single_line_text)} single-line text fields ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — Expected 5 text fields, found {len(single_line_text)} single-line text widgets")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 3 radio button groups with correct counts (0.30 points)
    # Expected: Performance (4 options), Satisfaction (5 options), Recommend (2 options)
    try:
        radio_widgets = [w for w in all_widgets if w["type_name"] == "RadioButton"]
        # Group by field name
        radio_groups = {}
        for w in radio_widgets:
            name = w["name"] or "unknown"
            radio_groups.setdefault(name, []).append(w)

        group_score = 0.0
        group_details = []

        # Check performance group (4 options)
        perf_found = False
        for gname, buttons in radio_groups.items():
            if "perform" in gname.lower():
                if len(buttons) == 4:
                    group_score += 0.10
                    group_details.append(f"Performance({len(buttons)}):OK")
                    perf_found = True
                elif len(buttons) >= 2:
                    group_score += 0.05
                    group_details.append(f"Performance({len(buttons)}):partial")
                    perf_found = True
                break

        # Check satisfaction group (5 options)
        sat_found = False
        for gname, buttons in radio_groups.items():
            if "satisf" in gname.lower():
                if len(buttons) == 5:
                    group_score += 0.10
                    group_details.append(f"Satisfaction({len(buttons)}):OK")
                    sat_found = True
                elif len(buttons) >= 2:
                    group_score += 0.05
                    group_details.append(f"Satisfaction({len(buttons)}):partial")
                    sat_found = True
                break

        # Check recommend group (2 options)
        rec_found = False
        for gname, buttons in radio_groups.items():
            if "recommend" in gname.lower() or "rec" in gname.lower():
                if len(buttons) == 2:
                    group_score += 0.10
                    group_details.append(f"Recommend({len(buttons)}):OK")
                    rec_found = True
                elif len(buttons) >= 1:
                    group_score += 0.05
                    group_details.append(f"Recommend({len(buttons)}):partial")
                    rec_found = True
                break

        # Fallback: if names don't match but we have 3 radio groups with roughly right counts
        if not (perf_found and sat_found and rec_found):
            if len(radio_groups) >= 3:
                group_counts = sorted([len(v) for v in radio_groups.values()], reverse=True)
                # We expect groups of sizes 5, 4, 2 (or similar)
                if not perf_found and any(c == 4 for c in group_counts):
                    group_score += 0.10
                    group_details.append("Performance(4):name-mismatch-OK")
                if not sat_found and any(c == 5 for c in group_counts):
                    group_score += 0.10
                    group_details.append("Satisfaction(5):name-mismatch-OK")
                if not rec_found and any(c == 2 for c in group_counts):
                    group_score += 0.10
                    group_details.append("Recommend(2):name-mismatch-OK")

        group_score = min(group_score, 0.30)
        if group_score >= 0.30:
            print(f"PASS: Component 3 — All 3 radio groups correct: {group_details} (0.30 pts)")
        elif group_score > 0:
            print(f"PARTIAL: Component 3 — Radio groups: {group_details} ({group_score} pts)")
        else:
            print(f"FAIL: Component 3 — Found {len(radio_groups)} radio groups: {[(k, len(v)) for k, v in radio_groups.items()]}")
        total_score += group_score
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Multiline comments textarea (0.15 points)
    try:
        multiline_widgets = [w for w in all_widgets if w["type_name"] == "Text" and (w["flags"] & 4096)]
        # Also check by name
        comment_widgets = [w for w in all_widgets if w["type_name"] == "Text"
                           and ("comment" in (w["name"] or "").lower()
                                or "note" in (w["name"] or "").lower()
                                or "feedback" in (w["name"] or "").lower())]

        if multiline_widgets:
            print(f"PASS: Component 4 — Multiline text area found: {[w['name'] for w in multiline_widgets]} (0.15 pts)")
            total_score += 0.15
        elif comment_widgets:
            # Has a comment field but not flagged as multiline — partial credit
            # Check if the field rect is tall enough to be a textarea (height > 40 pts)
            tall_comment = [w for w in comment_widgets if (w["rect"][3] - w["rect"][1]) > 40]
            if tall_comment:
                print(f"PASS: Component 4 — Comments field with large area found: {[w['name'] for w in tall_comment]} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"PARTIAL: Component 4 — Comments field found but not multiline ({0.08} pts)")
                total_score += 0.08
        else:
            print(f"FAIL: Component 4 — No multiline text area or comments field found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Submit button present (0.15 points)
    try:
        # Check for Button-type widgets
        button_widgets = [w for w in all_widgets if w["type_name"] == "Button"]
        # Also check for text fields acting as buttons (by name)
        submit_by_name = [w for w in all_widgets if "submit" in (w["name"] or "").lower()
                          or "button" in (w["name"] or "").lower()]
        # Also check page text for "Submit"
        all_text = ""
        for pi in range(doc.page_count):
            all_text += doc[pi].get_text("text")

        has_submit_text = "submit" in all_text.lower()

        if button_widgets:
            submit_buttons = [w for w in button_widgets if "submit" in (w["name"] or "").lower()]
            if submit_buttons:
                print(f"PASS: Component 5 — Submit button found: {[w['name'] for w in submit_buttons]} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"PASS: Component 5 — Button widget found: {[w['name'] for w in button_widgets]} (0.15 pts)")
                total_score += 0.15
        elif submit_by_name:
            print(f"PASS: Component 5 — Submit widget found by name: {[w['name'] for w in submit_by_name]} (0.15 pts)")
            total_score += 0.15
        elif has_submit_text:
            # There's submit text on the page — could be a decorative button
            print(f"PARTIAL: Component 5 — 'Submit' text found on page but no widget (0.08 pts)")
            total_score += 0.08
        else:
            print(f"FAIL: Component 5 — No submit button or widget found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/forms/employee_survey.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

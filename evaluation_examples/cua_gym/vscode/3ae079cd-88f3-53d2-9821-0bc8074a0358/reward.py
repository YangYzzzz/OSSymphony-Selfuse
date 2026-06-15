"""
Reward Script: Emmet form expansion in VSCode
Task ID: vscode_code_058
Domain: vs_code
Scoring:
  - Component 1: form element with action=/submit and method=post (0.2 pts)
  - Component 2: fieldset with legend 'User Info' (0.2 pts)
  - Component 3: name label + input (type=text, id=name, name=name) (0.2 pts)
  - Component 4: email label + input (type=email, id=email, name=email) (0.2 pts)
  - Component 5: submit button (type=submit, text=Submit) (0.2 pts)
Total: 1.0
"""

import os
import re

WORKDIR = '/home/user/web'
TASK_ID = 'vscode_code_058'
FILE_PATH = '/home/user/web/form.html'


def verify_task(file_path):
    """
    Verify that Emmet expansion produced the correct form structure in form.html.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load file content — precondition gate
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Normalize whitespace for easier regex matching
    # Collapse all whitespace sequences to single space for attribute checks
    content_flat = re.sub(r'\s+', ' ', content)

    # Component 1: form element with action="/submit" and method="post" (0.2 points)
    # This verifies the top-level Emmet expansion produced the correct form element
    try:
        # Check for <form ... action="/submit" ... method="post" ...> or
        # <form ... method="post" ... action="/submit" ...>
        form_pattern = re.search(
            r'<form\b[^>]*\baction\s*=\s*["\']?/submit["\']?[^>]*\bmethod\s*=\s*["\']?post["\']?[^>]*>',
            content_flat, re.IGNORECASE
        ) or re.search(
            r'<form\b[^>]*\bmethod\s*=\s*["\']?post["\']?[^>]*\baction\s*=\s*["\']?/submit["\']?[^>]*>',
            content_flat, re.IGNORECASE
        )
        if form_pattern:
            print("PASS: Component 1 — form element with action='/submit' and method='post' found (0.2 pts)")
            total_score += 0.2
        else:
            # Check if form exists at all for better diagnostics
            form_exists = re.search(r'<form\b', content_flat, re.IGNORECASE)
            if form_exists:
                print(f"FAIL: Component 1 — form element found but missing action='/submit' or method='post'")
            else:
                print("FAIL: Component 1 — no <form> element found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: fieldset with legend "User Info" (0.2 points)
    # Verifies the Emmet child operator produced the fieldset and legend text content
    try:
        fieldset_exists = re.search(r'<fieldset\b', content_flat, re.IGNORECASE)
        legend_text = re.search(r'<legend[^>]*>\s*User Info\s*</legend>', content_flat, re.IGNORECASE)
        if fieldset_exists and legend_text:
            print("PASS: Component 2 — fieldset and legend 'User Info' found (0.2 pts)")
            total_score += 0.2
        else:
            missing = []
            if not fieldset_exists:
                missing.append('<fieldset>')
            if not legend_text:
                missing.append('<legend>User Info</legend>')
            print(f"FAIL: Component 2 — missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: name label + input (type=text, id=name, name=name) (0.2 points)
    # Verifies Emmet produced the correct label for 'name' and an input with the right attributes
    try:
        # label[for=name] with text "Name: "
        label_name = re.search(
            r'<label\b[^>]*\bfor\s*=\s*["\']?name["\']?[^>]*>\s*Name:\s*</label>',
            content_flat, re.IGNORECASE
        )
        # input#name[type=text name=name] — check all three attributes
        input_name_type = re.search(
            r'<input\b[^>]*\btype\s*=\s*["\']?text["\']?[^>]*>',
            content_flat, re.IGNORECASE
        )
        input_name_id = re.search(
            r'<input\b[^>]*\bid\s*=\s*["\']?name["\']?[^>]*>',
            content_flat, re.IGNORECASE
        )
        input_name_attr = re.search(
            r'<input\b[^>]*\bname\s*=\s*["\']?name["\']?[^>]*>',
            content_flat, re.IGNORECASE
        )
        if label_name and input_name_type and input_name_id and input_name_attr:
            print("PASS: Component 3 — name label and input[type=text, id=name, name=name] found (0.2 pts)")
            total_score += 0.2
        else:
            missing = []
            if not label_name:
                missing.append('label[for=name] with text "Name: "')
            if not (input_name_type and input_name_id and input_name_attr):
                attrs_missing = []
                if not input_name_type:
                    attrs_missing.append('type=text')
                if not input_name_id:
                    attrs_missing.append('id=name')
                if not input_name_attr:
                    attrs_missing.append('name=name')
                missing.append(f'input with attrs: {", ".join(attrs_missing)}')
            print(f"FAIL: Component 3 — missing: {'; '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: email label + input (type=email, id=email, name=email) (0.2 points)
    # Verifies Emmet produced the correct label for 'email' and an input with the right attributes
    try:
        # label[for=email] with text "Email: "
        label_email = re.search(
            r'<label\b[^>]*\bfor\s*=\s*["\']?email["\']?[^>]*>\s*Email:\s*</label>',
            content_flat, re.IGNORECASE
        )
        # input#email[type=email name=email] — check all three attributes
        input_email_type = re.search(
            r'<input\b[^>]*\btype\s*=\s*["\']?email["\']?[^>]*>',
            content_flat, re.IGNORECASE
        )
        input_email_id = re.search(
            r'<input\b[^>]*\bid\s*=\s*["\']?email["\']?[^>]*>',
            content_flat, re.IGNORECASE
        )
        input_email_attr = re.search(
            r'<input\b[^>]*\bname\s*=\s*["\']?email["\']?[^>]*>',
            content_flat, re.IGNORECASE
        )
        if label_email and input_email_type and input_email_id and input_email_attr:
            print("PASS: Component 4 — email label and input[type=email, id=email, name=email] found (0.2 pts)")
            total_score += 0.2
        else:
            missing = []
            if not label_email:
                missing.append('label[for=email] with text "Email: "')
            if not (input_email_type and input_email_id and input_email_attr):
                attrs_missing = []
                if not input_email_type:
                    attrs_missing.append('type=email')
                if not input_email_id:
                    attrs_missing.append('id=email')
                if not input_email_attr:
                    attrs_missing.append('name=email')
                missing.append(f'input with attrs: {", ".join(attrs_missing)}')
            print(f"FAIL: Component 4 — missing: {'; '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: submit button with type=submit and text "Submit" (0.2 points)
    # Verifies Emmet produced button[type=submit]{Submit}
    try:
        button_submit = re.search(
            r'<button\b[^>]*\btype\s*=\s*["\']?submit["\']?[^>]*>\s*Submit\s*</button>',
            content_flat, re.IGNORECASE
        )
        if button_submit:
            print("PASS: Component 5 — button[type=submit] with text 'Submit' found (0.2 pts)")
            total_score += 0.2
        else:
            button_exists = re.search(r'<button\b', content_flat, re.IGNORECASE)
            if button_exists:
                print("FAIL: Component 5 — button found but missing type=submit or text 'Submit'")
            else:
                print("FAIL: Component 5 — no <button> element found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

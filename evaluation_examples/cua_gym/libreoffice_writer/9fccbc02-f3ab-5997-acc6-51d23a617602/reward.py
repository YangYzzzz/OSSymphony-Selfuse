"""
Reward Script: Format discovery response document with alternating paragraph styles
Task ID: writer_legal_092
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): REQUEST NO. paragraphs are bold and italic
  Component 2 (0.3): RESPONSE: paragraphs have 0.5in left indent
  Component 3 (0.3): Response body paragraphs have 0.5in left indent
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_legal_092'

# Tolerance for indent comparison: 0.5 inches = 457200 EMU; allow +/- 5%
EXPECTED_INDENT_EMU = 457200
INDENT_TOLERANCE = 0.05  # 5% tolerance


def persist_app_state(domain):
    """Save any unsaved changes in LibreOffice Writer."""
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
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Identify REQUEST NO. paragraphs, RESPONSE: paragraphs, and response body paragraphs
    request_paras = []
    response_label_paras = []
    response_body_paras = []

    paragraphs = doc.paragraphs
    i = 0
    while i < len(paragraphs):
        text = paragraphs[i].text.strip()
        # Match "REQUEST NO. X:" pattern
        if re.match(r'REQUEST\s+NO\.\s*\d+', text):
            request_paras.append(paragraphs[i])
            # Look for the description paragraph after REQUEST NO. (skip it, not scored for indent)
            # Then find the RESPONSE: paragraph and its body
            j = i + 1
            # Skip request description paragraphs (no indent expected)
            while j < len(paragraphs):
                resp_text = paragraphs[j].text.strip()
                if resp_text.startswith('RESPONSE'):
                    response_label_paras.append(paragraphs[j])
                    # The next non-empty paragraph is the response body
                    k = j + 1
                    while k < len(paragraphs):
                        body_text = paragraphs[k].text.strip()
                        if body_text:
                            # Check if this is NOT a new REQUEST (meaning it's response body)
                            if not re.match(r'REQUEST\s+NO\.\s*\d+', body_text):
                                response_body_paras.append(paragraphs[k])
                            break
                        k += 1
                    break
                elif resp_text == '':
                    j += 1
                    continue
                else:
                    j += 1
                    continue
        i += 1

    print(f"Found {len(request_paras)} REQUEST paragraphs")
    print(f"Found {len(response_label_paras)} RESPONSE label paragraphs")
    print(f"Found {len(response_body_paras)} RESPONSE body paragraphs")
    print()

    # Component 1: REQUEST NO. paragraphs are bold AND italic (0.4 points)
    # Each of the 15 REQUEST paragraphs should have all runs bold+italic
    try:
        request_correct = 0
        for idx, para in enumerate(request_paras):
            runs_with_text = [r for r in para.runs if r.text.strip()]
            if runs_with_text:
                all_bold = all(r.bold for r in runs_with_text)
                all_italic = all(r.italic for r in runs_with_text)
                if all_bold and all_italic:
                    request_correct += 1
                else:
                    print(f"FAIL: REQUEST {idx+1} — bold={all_bold}, italic={all_italic}")
            else:
                print(f"FAIL: REQUEST {idx+1} — no runs with text")

        if len(request_paras) > 0 and request_correct > 0:
            fraction = request_correct / max(len(request_paras), 15)
            comp1_score = 0.4 * fraction
            print(f"PASS: Component 1 — {request_correct}/{len(request_paras)} REQUEST paragraphs are bold+italic ({comp1_score:.3f} pts)")
            total_score += comp1_score
        else:
            print(f"FAIL: Component 1 — No REQUEST paragraphs are bold+italic")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: RESPONSE: label paragraphs have 0.5in left indent (0.3 points)
    try:
        response_label_correct = 0
        for idx, para in enumerate(response_label_paras):
            left_indent = para.paragraph_format.left_indent
            if left_indent is not None:
                lower = EXPECTED_INDENT_EMU * (1 - INDENT_TOLERANCE)
                upper = EXPECTED_INDENT_EMU * (1 + INDENT_TOLERANCE)
                if lower <= left_indent <= upper:
                    response_label_correct += 1
                else:
                    actual_in = left_indent / 914400.0
                    print(f"FAIL: RESPONSE label {idx+1} — left_indent={actual_in:.3f}in (expected ~0.500in)")
            else:
                print(f"FAIL: RESPONSE label {idx+1} — no left indent set")

        if len(response_label_paras) > 0 and response_label_correct > 0:
            fraction = response_label_correct / max(len(response_label_paras), 15)
            comp2_score = 0.3 * fraction
            print(f"PASS: Component 2 — {response_label_correct}/{len(response_label_paras)} RESPONSE labels have 0.5in indent ({comp2_score:.3f} pts)")
            total_score += comp2_score
        else:
            print(f"FAIL: Component 2 — No RESPONSE labels have correct indent")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Response body paragraphs have 0.5in left indent (0.3 points)
    try:
        response_body_correct = 0
        for idx, para in enumerate(response_body_paras):
            left_indent = para.paragraph_format.left_indent
            if left_indent is not None:
                lower = EXPECTED_INDENT_EMU * (1 - INDENT_TOLERANCE)
                upper = EXPECTED_INDENT_EMU * (1 + INDENT_TOLERANCE)
                if lower <= left_indent <= upper:
                    response_body_correct += 1
                else:
                    actual_in = left_indent / 914400.0
                    print(f"FAIL: RESPONSE body {idx+1} — left_indent={actual_in:.3f}in (expected ~0.500in)")
            else:
                print(f"FAIL: RESPONSE body {idx+1} — no left indent set")

        if len(response_body_paras) > 0 and response_body_correct > 0:
            fraction = response_body_correct / max(len(response_body_paras), 15)
            comp3_score = 0.3 * fraction
            print(f"PASS: Component 3 — {response_body_correct}/{len(response_body_paras)} RESPONSE bodies have 0.5in indent ({comp3_score:.3f} pts)")
            total_score += comp3_score
        else:
            print(f"FAIL: Component 3 — No RESPONSE body paragraphs have correct indent")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.3f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist app state before verification
persist_app_state("libreoffice_writer")

# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

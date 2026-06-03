"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m editing a contract in LibreOffice Writer and the compliance team wants every numeric value (dates, amounts, section numbers—anything made of 0-9) in the second paragraph double-underlined, while leaving the rest of the document untouched. Is there a quick way to apply that double underline to just the numbers in paragraph 2 instead of doing each one by hand?
Generated: 2025-09-10 18:56:37
Status: success
Model: azure-o3
Total Steps: 1
"""

from docx import Document
from docx.enum.text import WD_UNDERLINE
import os, glob, re

def is_double_underline(run):
    """Return True if the run is double-underlined."""
    u = run.font.underline
    if u is None or u is False:
        return False
    # python-docx stores underline as enumeration, bool, or string
    if u == WD_UNDERLINE.DOUBLE:
        return True
    if isinstance(u, str):
        return u.lower() == 'double'
    try:
        return int(u) == WD_UNDERLINE.DOUBLE  # numeric enum value
    except Exception:
        return False

def find_target_file():
    """Pick the most recently modified non-golden DOCX in /home/user, else any DOCX."""
    candidates = [p for p in glob.glob('/home/user/*.docx') if 'golden' not in p.lower()]
    if not candidates:
        candidates = glob.glob('/home/user/*.docx')
    if not candidates:
        return None
    candidates.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return candidates[0]

def verify_double_underline_numbers(file_path):
    """Progressively score the document for correct double-underline formatting."""
    max_score = 1.0
    score = 0.0

    # ---------- Load document (no points – prerequisite) ----------
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Could not load DOCX file: {e}")
        return 0.0

    paragraphs = doc.paragraphs
    if len(paragraphs) < 2:
        print("✗ Document has less than 2 paragraphs")
        return 0.0

    p2 = paragraphs[1]
    runs_p2 = p2.runs
    if not runs_p2:
        print("✗ Second paragraph has no runs")
        return 0.0

    # ---------- Requirement 1 (0.4) ----------
    # Every run containing at least one digit in paragraph 2 must be double-underlined
    digit_runs = [run for run in runs_p2 if re.search(r"[0-9]", run.text)]
    cond1 = True
    for run in digit_runs:
        if not is_double_underline(run):
            cond1 = False
            print(f"✗ Run with digits not double-underlined: '{run.text}'")
            break
    if cond1 and digit_runs:
        score += 0.4
        print("✓ All numeric runs in paragraph 2 are double-underlined (0.4)")
    elif not digit_runs:
        print("! No numeric values found in paragraph 2 – cannot award points for Req.1")

    # ---------- Requirement 2 (0.3) ----------
    # Runs with NO digits in paragraph 2 must NOT be double-underlined
    cond2 = True
    for run in runs_p2:
        if not re.search(r"[0-9]", run.text):
            if is_double_underline(run):
                cond2 = False
                print(f"✗ Non-numeric run wrongly double-underlined: '{run.text}'")
                break
    if cond2:
        score += 0.3
        print("✓ Non-numeric runs in paragraph 2 are not double-underlined (0.3)")

    # ---------- Requirement 3 (0.3) ----------
    # No double-underline anywhere outside paragraph 2
    cond3 = True
    for idx, para in enumerate(paragraphs):
        if idx == 1:
            continue  # skip paragraph 2
        for run in para.runs:
            if is_double_underline(run):
                cond3 = False
                snippet = run.text.strip()[:30]
                print(f"✗ Double underline found outside paragraph 2 (para {idx+1}): '{snippet}'")
                break
        if not cond3:
            break
    if cond3:
        score += 0.3
        print("✓ No double underline found outside paragraph 2 (0.3)")

    # ---------- Final score ----------
    final_score = min(score, max_score)
    print(f"Total Score: {final_score}")
    return final_score

# -------------------- Main --------------------
file_path = find_target_file()
if not file_path:
    print("✗ No DOCX file found for verification in /home/user")
    reward = 0.0
else:
    print(f"Verifying file: {file_path}")
    reward = verify_double_underline_numbers(file_path)

print(f"REWARD: {reward}")


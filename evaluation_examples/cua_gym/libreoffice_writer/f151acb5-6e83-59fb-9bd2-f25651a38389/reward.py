"""
Reward script for wrpara_036: Verify keep_together settings on paragraphs
based on estimated line count.

- Paragraphs shorter than 4 lines: keep_together should be True
- Paragraphs 4 lines or longer: keep_together should be explicitly False
"""

import sys
sys.path.insert(0, '/usr/lib/python3/dist-packages')

try:
    from docx import Document
except ImportError:
    import subprocess
    subprocess.run(['pip3', 'install', 'python-docx'], capture_output=True)
    from docx import Document

import math

DOC_PATH = "/home/user/wrpara_036.docx"
CHARS_PER_LINE = 85
LINE_THRESHOLD = 4


def estimate_lines(text):
    """Estimate the number of lines a paragraph occupies."""
    if len(text) == 0:
        return 1
    return max(1, math.ceil(len(text) / CHARS_PER_LINE))


def main():
    try:
        doc = Document(DOC_PATH)
    except Exception as e:
        print(f"ERROR: Cannot open document: {e}")
        print("REWARD: 0.0")
        return

    paragraphs = doc.paragraphs
    if len(paragraphs) == 0:
        print("ERROR: No paragraphs found in document.")
        print("REWARD: 0.0")
        return

    correct = 0
    total = 0

    for i, para in enumerate(paragraphs):
        text = para.text
        est_lines = estimate_lines(text)
        kt = para.paragraph_format.keep_together

        if est_lines < LINE_THRESHOLD:
            # Short paragraph: should have keep_together = True
            expected = True
            is_correct = (kt is True)
        else:
            # Long paragraph: should have keep_together = False (explicitly)
            expected = False
            is_correct = (kt is False)

        total += 1
        if is_correct:
            correct += 1
        else:
            print(f"MISMATCH P{i}: est_lines={est_lines}, keep_together={kt}, expected={expected}, text='{text[:60]}...'")

    if total == 0:
        print("ERROR: No paragraphs to evaluate.")
        print("REWARD: 0.0")
        return

    score = correct / total
    # Round to 2 decimal places
    score = round(score, 2)

    print(f"Score: {correct}/{total} paragraphs correct")
    print(f"REWARD: {score}")


if __name__ == "__main__":
    main()

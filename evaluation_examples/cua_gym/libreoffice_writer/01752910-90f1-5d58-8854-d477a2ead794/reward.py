"""
Reward Script: Accept all tracked insertions, reject all tracked deletions
Task ID: writer_rm_038
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.2): No tracked changes remain in the document
  - Component 2 (0.4): All 11 insertion texts are present (accepted into body)
  - Component 3 (0.4): All 9 deletion texts are present (rejecting deletions keeps original text)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_038'


def persist_app_state(domain: str):
    """Save any unsaved LibreOffice edits before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
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

    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    body = doc.element.body

    # Component 1: No tracked changes remain (0.2 points)
    # In the initial file there are 11 insertions + 9 deletions = 20 tracked changes.
    # After accepting insertions and rejecting deletions, there should be 0.
    try:
        insertions = body.findall('.//w:ins', ns)
        deletions = body.findall('.//w:del', ns)
        num_tracked = len(insertions) + len(deletions)
        if num_tracked == 0:
            print(f"PASS: Component 1 — No tracked changes remain (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Found {num_tracked} tracked changes ({len(insertions)} ins, {len(deletions)} del), expected 0")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All insertion texts are present in the body (0.4 points)
    # These were tracked insertions that should be accepted (become permanent text).
    # In the initial file, para.text does NOT include tracked insertion text.
    # In the golden file, the insertion text is part of regular paragraph text.
    try:
        full_text = ' '.join(p.text for p in doc.paragraphs)

        insertion_snippets = [
            'AI-powered noise cancellation',
            'Intel Core Ultra 9 processor',
            'Thunderbolt 5',
            'Bluetooth 5.3 with LC3plus',
            'ECG monitoring feature',
            'fall detection and automatic emergency SOS',
            'Matter and Thread protocol',
            'on-device AI processing',
            'USB4 ports',
            'Tri-mode connectivity',
            '140W USB-C PD 3.1',
        ]

        ins_found = 0
        for snippet in insertion_snippets:
            if snippet in full_text:
                ins_found += 1
            else:
                print(f"  MISS insertion: '{snippet}'")

        ins_ratio = ins_found / len(insertion_snippets)
        ins_score = 0.4 * ins_ratio

        if ins_found == len(insertion_snippets):
            print(f"PASS: Component 2 — All {len(insertion_snippets)} insertion texts present ({ins_score:.2f} pts)")
            total_score += ins_score
        elif ins_found > 0:
            print(f"PARTIAL: Component 2 — {ins_found}/{len(insertion_snippets)} insertion texts present ({ins_score:.2f} pts)")
            total_score += ins_score
        else:
            print(f"FAIL: Component 2 — 0/{len(insertion_snippets)} insertion texts present")

    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All deletion texts are preserved in the body (0.4 points)
    # These were tracked deletions that should be REJECTED (original text restored/kept).
    # In the initial file, para.text does NOT include tracked deletion text.
    # In the golden file, the deletion text is part of regular paragraph text.
    try:
        deletion_snippets = [
            '3G CDMA networks',
            'Intel Core i5-1135G7',
            'Bluetooth 4.2 with aptX',
            '3.5mm input and micro-USB',
            'Android 8.0 or iOS 12',
            'Zigbee protocol',
            'USB 3.0 Type-A',
            'USB-A cable only',
            'Qualcomm Quick Charge 3.0',
        ]

        del_found = 0
        for snippet in deletion_snippets:
            if snippet in full_text:
                del_found += 1
            else:
                print(f"  MISS deletion: '{snippet}'")

        del_ratio = del_found / len(deletion_snippets)
        del_score = 0.4 * del_ratio

        if del_found == len(deletion_snippets):
            print(f"PASS: Component 3 — All {len(deletion_snippets)} deletion texts preserved ({del_score:.2f} pts)")
            total_score += del_score
        elif del_found > 0:
            print(f"PARTIAL: Component 3 — {del_found}/{len(deletion_snippets)} deletion texts preserved ({del_score:.2f} pts)")
            total_score += del_score
        else:
            print(f"FAIL: Component 3 — 0/{len(deletion_snippets)} deletion texts preserved")

    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist unsaved edits before verification
persist_app_state("libreoffice_writer")

# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

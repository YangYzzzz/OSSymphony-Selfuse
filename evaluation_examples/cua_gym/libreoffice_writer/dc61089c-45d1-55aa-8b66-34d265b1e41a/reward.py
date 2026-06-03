"""
Reward Script: POSTNET barcode for ZIP 90210 on envelope
Task ID: writer_lec_047
Domain: libreoffice_writer
Scoring:
  Component 1 (0.30): Barcode paragraph exists after delivery address with block chars
  Component 2 (0.30): Correct POSTNET encoding for ZIP 90210 (32 bars, valid pattern)
  Component 3 (0.20): Barcode uses monospaced font
  Component 4 (0.20): ZIP code "90210" text appears below the barcode
"""

import os
from docx import Document
from docx.shared import Pt

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_047'

# POSTNET encoding table: digit -> 5-bit pattern (1=tall, 0=short)
POSTNET_TABLE = {
    0: (1, 1, 0, 0, 0),
    1: (0, 0, 0, 1, 1),
    2: (0, 0, 1, 0, 1),
    3: (0, 0, 1, 1, 0),
    4: (0, 1, 0, 0, 1),
    5: (0, 1, 0, 1, 0),
    6: (0, 1, 1, 0, 0),
    7: (1, 0, 0, 0, 1),
    8: (1, 0, 0, 1, 0),
    9: (1, 0, 1, 0, 0),
}


def compute_postnet_pattern(zip_str):
    """Compute expected POSTNET bar pattern for a ZIP code string."""
    digits = [int(c) for c in zip_str]
    check_digit = (10 - (sum(digits) % 10)) % 10
    digits_with_check = digits + [check_digit]

    # Frame bar + digit bars + frame bar
    pattern = [1]  # start frame bar
    for d in digits_with_check:
        pattern.extend(POSTNET_TABLE[d])
    pattern.append(1)  # end frame bar
    return pattern


def classify_bar(char):
    """Classify a barcode character as tall (1) or short (0).
    Full block = tall bar, lower-half block = short bar.
    Also accept pipe | or I as tall, period . or colon : as short."""
    if char in ('\u2588', '|', 'I', '\u2503'):  # full block, pipe, etc.
        return 1
    elif char in ('\u2584', '.', ':', '_', '\u2581'):  # lower half block, etc.
        return 0
    return None


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

    paragraphs = doc.paragraphs
    num_paras = len(paragraphs)

    # Precondition: document should have at least the original 7 paragraphs
    if num_paras < 7:
        print(f"FAIL: Document has only {num_paras} paragraphs, expected at least 7")
        print("REWARD: 0.0")
        return 0.0

    # Find the delivery address paragraph containing "90210"
    delivery_addr_idx = None
    for i, para in enumerate(paragraphs):
        if '90210' in para.text and 'Beverly Hills' in para.text:
            delivery_addr_idx = i
            break

    if delivery_addr_idx is None:
        print("FAIL: Could not find delivery address paragraph with 'Beverly Hills' and '90210'")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Delivery address found at paragraph {delivery_addr_idx}")

    # Look for barcode paragraph(s) AFTER the delivery address
    barcode_para_idx = None
    barcode_bars = []

    for i in range(delivery_addr_idx + 1, num_paras):
        para = paragraphs[i]
        text = para.text.strip()
        if not text:
            continue

        # Check if this paragraph contains barcode-like characters
        bar_chars = []
        for ch in text:
            classified = classify_bar(ch)
            if classified is not None:
                bar_chars.append(classified)

        if len(bar_chars) >= 10:  # A barcode should have many bar characters
            barcode_para_idx = i
            barcode_bars = bar_chars
            break

    # Component 1: Barcode paragraph exists after delivery address (0.30 points)
    try:
        if barcode_para_idx is not None and len(barcode_bars) >= 10:
            print(f"PASS: Component 1 -- Barcode paragraph found at P{barcode_para_idx} with {len(barcode_bars)} bars (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 -- No barcode paragraph found after delivery address")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Correct POSTNET encoding for ZIP 90210 (0.30 points)
    try:
        expected_pattern = compute_postnet_pattern("90210")
        # 32 bars for 5-digit ZIP: 1 frame + 5*5 digit + 5 check + 1 frame
        if len(barcode_bars) == len(expected_pattern) and barcode_bars == expected_pattern:
            print(f"PASS: Component 2 -- POSTNET encoding matches ZIP 90210 perfectly ({len(barcode_bars)} bars) (0.30 pts)")
            total_score += 0.30
        elif len(barcode_bars) == len(expected_pattern):
            # Partial: right length but wrong pattern
            matching = sum(1 for a, b in zip(barcode_bars, expected_pattern) if a == b)
            ratio = matching / len(expected_pattern)
            if ratio >= 0.8:
                partial = 0.15
                print(f"PARTIAL: Component 2 -- {matching}/{len(expected_pattern)} bars match ({ratio:.0%}) ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 -- Pattern mismatch: {matching}/{len(expected_pattern)} bars match")
        elif len(barcode_bars) > 0:
            print(f"FAIL: Component 2 -- Expected {len(expected_pattern)} bars, found {len(barcode_bars)}")
        else:
            print(f"FAIL: Component 2 -- No barcode bars detected")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Barcode uses monospaced font (0.20 points)
    try:
        if barcode_para_idx is not None:
            para = paragraphs[barcode_para_idx]
            monospace_fonts = {'courier new', 'courier', 'consolas', 'lucida console',
                               'monospace', 'dejavu sans mono', 'liberation mono',
                               'noto mono', 'ubuntu mono', 'fira mono', 'fira code'}
            fonts_found = set()
            bar_runs_with_mono = 0
            bar_runs_total = 0
            for run in para.runs:
                if run.text.strip() and classify_bar(run.text.strip()) is not None:
                    bar_runs_total += 1
                    if run.font.name:
                        fonts_found.add(run.font.name.lower())
                        if run.font.name.lower() in monospace_fonts:
                            bar_runs_with_mono += 1

            if bar_runs_total > 0 and bar_runs_with_mono / bar_runs_total >= 0.8:
                print(f"PASS: Component 3 -- Barcode uses monospaced font: {fonts_found} (0.20 pts)")
                total_score += 0.20
            elif fonts_found:
                print(f"FAIL: Component 3 -- Barcode fonts: {fonts_found}, not monospaced")
            else:
                print(f"FAIL: Component 3 -- No font info found on barcode runs")
        else:
            print(f"FAIL: Component 3 -- No barcode paragraph to check font")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: ZIP code "90210" text appears below barcode (0.20 points)
    try:
        if barcode_para_idx is not None:
            zip_para_idx = next(
                (i for i in range(barcode_para_idx + 1, num_paras)
                 if '90210' in paragraphs[i].text.strip()),
                None
            )
            if zip_para_idx is not None:
                print(f"PASS: Component 4 -- ZIP '90210' found below barcode at P{zip_para_idx}: '{paragraphs[zip_para_idx].text.strip()}' (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 -- No '90210' text found below barcode paragraph")
        else:
            print(f"FAIL: Component 4 -- No barcode paragraph found, cannot check ZIP text")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook for LibreOffice Writer
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    persist_app_state()
    verify_task(file_path)

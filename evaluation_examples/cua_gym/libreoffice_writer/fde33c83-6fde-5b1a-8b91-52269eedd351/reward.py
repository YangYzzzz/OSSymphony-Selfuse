"""
Reward Script: Create a 'Subtitle' paragraph style based on 'Heading 1'
Task ID: writer_bs_092
Domain: libreoffice_writer
Scoring:
  Component 1 (0.15): Subtitle style exists and is based on Heading 1
  Component 2 (0.15): Font = Calibri Light, Size = 16pt
  Component 3 (0.15): Not bold, color = #546E7A
  Component 4 (0.15): Center alignment
  Component 5 (0.15): Spacing above ~0.1cm, below ~0.8cm
  Component 6 (0.25): Subtitle paragraph uses the Subtitle style
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_bs_092'


def persist_app_state(domain):
    """Best-effort save of any unsaved LibreOffice edits."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
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
        from docx.shared import Pt, Emu
        from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
    except ImportError as e:
        print(f"CRITICAL: Missing python-docx: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # --- Locate the Subtitle paragraph style ---
    subtitle_style = None
    for s in doc.styles:
        if s.name == 'Subtitle' and s.type == 1:  # PARAGRAPH type
            subtitle_style = s
            break

    if subtitle_style is None:
        print("FAIL: No 'Subtitle' paragraph style found in document")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Subtitle style exists and is based on Heading 1 (0.15 points)
    try:
        base_name = subtitle_style.base_style.name if subtitle_style.base_style else None
        if base_name == 'Heading 1':
            print(f"PASS: Component 1 -- Subtitle style based on 'Heading 1' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- Subtitle style based on '{base_name}', expected 'Heading 1'")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Font = Calibri Light, Size = 16pt (0.15 points)
    try:
        font_name = subtitle_style.font.name
        font_size = subtitle_style.font.size
        font_size_pt = font_size.pt if font_size else None

        name_ok = font_name is not None and 'calibri light' in font_name.lower()
        size_ok = font_size_pt is not None and abs(font_size_pt - 16.0) < 0.5

        if name_ok and size_ok:
            print(f"PASS: Component 2 -- Font='{font_name}', Size={font_size_pt}pt (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 -- Font='{font_name}' (expect Calibri Light), Size={font_size_pt}pt (expect 16)")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Not bold and color = #546E7A (0.15 points)
    try:
        is_bold = subtitle_style.font.bold
        color_rgb = subtitle_style.font.color.rgb if subtitle_style.font.color and subtitle_style.font.color.rgb else None

        # bold should be False (explicitly not bold). None means inherit from base;
        # since base is Heading 1 which is bold, we need explicit False.
        bold_ok = is_bold is False  # explicitly set to not bold
        color_ok = color_rgb is not None and str(color_rgb).upper() == '546E7A'

        if bold_ok and color_ok:
            print(f"PASS: Component 3 -- Bold={is_bold}, Color=#{color_rgb} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 -- Bold={is_bold} (expect False), Color=#{color_rgb} (expect #546E7A)")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Centered alignment (0.15 points)
    try:
        alignment = subtitle_style.paragraph_format.alignment
        if alignment == WD_PARAGRAPH_ALIGNMENT.CENTER:
            print(f"PASS: Component 4 -- Alignment=CENTER (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 -- Alignment={alignment}, expected CENTER")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Spacing above ~0.1cm, below ~0.8cm (0.15 points)
    try:
        space_before = subtitle_style.paragraph_format.space_before
        space_after = subtitle_style.paragraph_format.space_after

        # Convert EMU to cm: 1 cm = 360000 EMU
        before_cm = space_before / 360000 if space_before else None
        after_cm = space_after / 360000 if space_after else None

        # Allow tolerance of 0.05cm
        before_ok = before_cm is not None and abs(before_cm - 0.1) < 0.05
        after_ok = after_cm is not None and abs(after_cm - 0.8) < 0.05

        if before_ok and after_ok:
            print(f"PASS: Component 5 -- Space before={before_cm:.3f}cm, after={after_cm:.3f}cm (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 -- Space before={before_cm}cm (expect ~0.1), after={after_cm}cm (expect ~0.8)")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: The subtitle paragraph uses the 'Subtitle' style (0.25 points)
    try:
        # Find the subtitle paragraph by content
        subtitle_para = None
        for p in doc.paragraphs:
            if 'A Comprehensive Analysis of Modern Approaches' in p.text:
                subtitle_para = p
                break

        if subtitle_para is None:
            print("FAIL: Component 6 -- Could not find subtitle paragraph")
        elif subtitle_para.style.name == 'Subtitle':
            print(f"PASS: Component 6 -- Subtitle paragraph uses 'Subtitle' style (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 6 -- Subtitle paragraph uses '{subtitle_para.style.name}', expected 'Subtitle'")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state('libreoffice_writer')

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

"""
Reward Script: Change all bullets to checkmark character
Task ID: impstruct_034
Domain: libreoffice_impress
Scoring:
  Component 1 (0.35): Slide 2 bullets all use checkmark
  Component 2 (0.35): Slide 3 bullets all use checkmark
  Component 3 (0.30): Slide 4 bullets all use checkmark
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impstruct_034'
CHECKMARK = '\u2713'  # The expected checkmark character

NS = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}


def get_bullet_chars(pptx_path, slide_number):
    """
    Extract bullet characters from a slide (1-indexed).
    Returns a list of (char, text) tuples for each bulleted paragraph with text.
    """
    bullets = []
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        fname = f'ppt/slides/slide{slide_number}.xml'
        try:
            with zf.open(fname) as f:
                root = ET.parse(f).getroot()
                for para in root.findall('.//a:p', NS):
                    pPr = para.find('a:pPr', NS)
                    text = ''.join(t.text or '' for t in para.findall('.//a:t', NS))
                    if not text.strip():
                        continue
                    buChar = pPr.find('a:buChar', NS) if pPr is not None else None
                    char = buChar.get('char') if buChar is not None else None
                    if char is not None:
                        bullets.append((char, text.strip()[:50]))
        except KeyError:
            pass
    return bullets


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Verify it's a valid PPTX
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            namelist = zf.namelist()
            if 'ppt/slides/slide1.xml' not in namelist:
                print("CRITICAL: Not a valid PPTX file")
                print("REWARD: 0.0")
                return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot open PPTX: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Slide 2 bullets all use checkmark (0.35 points)
    # Expected: 7 bulleted paragraphs, all with char=checkmark
    try:
        bullets = get_bullet_chars(file_path, 2)
        if len(bullets) == 0:
            print("FAIL: Component 1 — No bullets found on slide 2")
        else:
            checkmark_count = sum(1 for char, _ in bullets if char == CHECKMARK)
            if checkmark_count == len(bullets):
                print(f"PASS: Component 1 — All {len(bullets)} bullets on slide 2 use checkmark (0.35 pts)")
                total_score += 0.35
            elif checkmark_count > 0:
                # Partial credit proportional to how many bullets were changed
                partial = 0.35 * (checkmark_count / len(bullets))
                chars_found = [char for char, _ in bullets]
                print(f"PARTIAL: Component 1 — {checkmark_count}/{len(bullets)} bullets on slide 2 use checkmark. Found: {chars_found} ({partial:.3f} pts)")
                if partial > 0:
                    total_score += partial
            else:
                chars_found = [char for char, _ in bullets]
                print(f"FAIL: Component 1 — 0/{len(bullets)} bullets on slide 2 use checkmark. Found: {chars_found}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Slide 3 bullets all use checkmark (0.35 points)
    # Expected: 6 bulleted paragraphs, all with char=checkmark
    try:
        bullets = get_bullet_chars(file_path, 3)
        if len(bullets) == 0:
            print("FAIL: Component 2 — No bullets found on slide 3")
        else:
            checkmark_count = sum(1 for char, _ in bullets if char == CHECKMARK)
            if checkmark_count == len(bullets):
                print(f"PASS: Component 2 — All {len(bullets)} bullets on slide 3 use checkmark (0.35 pts)")
                total_score += 0.35
            elif checkmark_count > 0:
                partial = 0.35 * (checkmark_count / len(bullets))
                chars_found = [char for char, _ in bullets]
                print(f"PARTIAL: Component 2 — {checkmark_count}/{len(bullets)} bullets on slide 3 use checkmark. Found: {chars_found} ({partial:.3f} pts)")
                if partial > 0:
                    total_score += partial
            else:
                chars_found = [char for char, _ in bullets]
                print(f"FAIL: Component 2 — 0/{len(bullets)} bullets on slide 3 use checkmark. Found: {chars_found}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Slide 4 bullets all use checkmark (0.30 points)
    # Expected: 7 bulleted paragraphs, all with char=checkmark
    try:
        bullets = get_bullet_chars(file_path, 4)
        if len(bullets) == 0:
            print("FAIL: Component 3 — No bullets found on slide 4")
        else:
            checkmark_count = sum(1 for char, _ in bullets if char == CHECKMARK)
            if checkmark_count == len(bullets):
                print(f"PASS: Component 3 — All {len(bullets)} bullets on slide 4 use checkmark (0.30 pts)")
                total_score += 0.30
            elif checkmark_count > 0:
                partial = 0.30 * (checkmark_count / len(bullets))
                chars_found = [char for char, _ in bullets]
                print(f"PARTIAL: Component 3 — {checkmark_count}/{len(bullets)} bullets on slide 4 use checkmark. Found: {chars_found} ({partial:.3f} pts)")
                if partial > 0:
                    total_score += partial
            else:
                chars_found = [char for char, _ in bullets]
                print(f"FAIL: Component 3 — 0/{len(bullets)} bullets on slide 4 use checkmark. Found: {chars_found}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook: save any unsaved LibreOffice edits
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_impress")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


# Entry point
persist_app_state()

file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

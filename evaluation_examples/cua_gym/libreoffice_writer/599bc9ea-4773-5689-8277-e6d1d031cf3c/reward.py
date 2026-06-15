"""
Reward Script: Verify automatic hyphenation settings in LibreOffice Writer document
Task ID: writer_rd_042
Domain: libreoffice_writer
Scoring:
  Component 1: autoHyphenation enabled + paragraphs not suppressed (0.40 pts)
  Component 2: consecutiveHyphenLimit == 3 in settings.xml (0.30 pts)
  Component 3: hyphenationZone ~ 283 twips (0.5 cm) in settings.xml (0.30 pts)
"""

import os
import zipfile
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_rd_042'

NSw = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def persist_app_state(domain):
    """Attempt to save any unsaved changes in LibreOffice."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print("PERSIST: ctrl+s sent for", domain)
        except Exception as e:
            print("PERSIST_WARN: save hook failed:", e)


def verify_task(file_path):
    """
    Verify hyphenation settings in the docx file.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the docx as a zip to inspect raw XML
    try:
        zf = zipfile.ZipFile(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # --- Parse settings.xml ---
    settings_root = None
    try:
        if 'word/settings.xml' in zf.namelist():
            settings_xml = zf.read('word/settings.xml')
            settings_root = etree.fromstring(settings_xml)
        else:
            print("WARN: No word/settings.xml found in docx")
    except Exception as e:
        print(f"ERROR: Failed to parse settings.xml: {e}")

    # --- Parse document.xml for paragraph-level checks ---
    doc_root = None
    try:
        doc_xml = zf.read('word/document.xml')
        doc_root = etree.fromstring(doc_xml)
    except Exception as e:
        print(f"ERROR: Failed to parse document.xml: {e}")

    # Component 1: autoHyphenation enabled AND all paragraphs allow hyphenation (0.40 pts)
    # In the initial file, autoHyphenation may appear as a LO default on re-save,
    # but paragraphs have suppressAutoHyphens=1 (suppressed). The compound check
    # ensures both conditions are met — which only happens after the task is completed.
    try:
        auto_hyph_enabled = False
        if settings_root is not None:
            auto_hyph = settings_root.findall(f'{{{NSw}}}autoHyphenation')
            if auto_hyph:
                val = auto_hyph[0].get(f'{{{NSw}}}val', '')
                if val in ('1', 'true'):
                    auto_hyph_enabled = True

        paras_allow_hyph = False
        if doc_root is not None:
            suppress_elems = doc_root.findall(f'.//{{{NSw}}}suppressAutoHyphens')
            if len(suppress_elems) == 0:
                # No suppressAutoHyphens means default (not suppressed)
                paras_allow_hyph = True
            else:
                all_allowed = True
                for elem in suppress_elems:
                    val = elem.get(f'{{{NSw}}}val', '')
                    if val not in ('0', 'false', ''):
                        all_allowed = False
                        break
                paras_allow_hyph = all_allowed

        if auto_hyph_enabled and paras_allow_hyph:
            print("PASS: Component 1 — autoHyphenation enabled AND all paragraphs allow hyphenation (0.40 pts)")
            total_score += 0.40
        elif auto_hyph_enabled and not paras_allow_hyph:
            print("FAIL: Component 1 — autoHyphenation enabled but paragraphs still suppress hyphenation")
        elif not auto_hyph_enabled and paras_allow_hyph:
            print("FAIL: Component 1 — paragraphs allow hyphenation but autoHyphenation not enabled in settings")
        else:
            print("FAIL: Component 1 — autoHyphenation not enabled and paragraphs suppress hyphenation")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: consecutiveHyphenLimit == 3 (0.30 pts)
    try:
        if settings_root is not None:
            consec = settings_root.findall(f'{{{NSw}}}consecutiveHyphenLimit')
            if consec:
                val = consec[0].get(f'{{{NSw}}}val', '')
                if val == '3':
                    print(f"PASS: Component 2 — consecutiveHyphenLimit={val} (0.30 pts)")
                    total_score += 0.30
                else:
                    print(f"FAIL: Component 2 — consecutiveHyphenLimit={val}, expected '3'")
            else:
                print("FAIL: Component 2 — consecutiveHyphenLimit element not found in settings.xml")
        else:
            print("FAIL: Component 2 — settings.xml not available")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: hyphenationZone ~ 283 twips (0.5 cm = 283.5 twips) (0.30 pts)
    try:
        if settings_root is not None:
            hz = settings_root.findall(f'{{{NSw}}}hyphenationZone')
            if hz:
                val = hz[0].get(f'{{{NSw}}}val', '')
                try:
                    val_int = int(val)
                    # 0.5 cm = 283.5 twips; allow tolerance of +/- 15 twips
                    if 268 <= val_int <= 300:
                        print(f"PASS: Component 3 — hyphenationZone={val} twips (~0.5 cm) (0.30 pts)")
                        total_score += 0.30
                    else:
                        print(f"FAIL: Component 3 — hyphenationZone={val} twips, expected ~283 (0.5 cm)")
                except ValueError:
                    print(f"FAIL: Component 3 — hyphenationZone val not an integer: {val}")
            else:
                print("FAIL: Component 3 — hyphenationZone element not found in settings.xml")
        else:
            print("FAIL: Component 3 — settings.xml not available")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    zf.close()

    final_score = min(total_score, 1.0)
    final_score = round(final_score, 2)
    print(f"\nScore: {round(total_score, 2)}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

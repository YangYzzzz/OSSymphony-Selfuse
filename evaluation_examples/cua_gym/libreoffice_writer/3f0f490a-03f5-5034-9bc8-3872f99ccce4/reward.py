"""
Reward Script: Insert a table of figures after the table of contents
Task ID: writer_tech_051
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): "Table of Figures" heading exists with Heading 1 style
  Component 2 (0.2): Heading is positioned after the Table of Contents section
  Component 3 (0.3): All 6 figure captions are listed in the table of figures
  Component 4 (0.2): Figure captions in table of figures match actual captions in the document
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_tech_051'


def persist_app_state(domain):
    """Attempt to save any unsaved LibreOffice edits."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.0)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify that a Table of Figures has been inserted after the Table of Contents.
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

    # Collect all paragraphs with their styles and text
    paragraphs = [(p.style.name if p.style else 'None', p.text) for p in doc.paragraphs]

    # Find "Table of Contents" heading index
    toc_index = None
    for i, (style, text) in enumerate(paragraphs):
        if 'table of contents' in text.lower() and 'Heading' in style:
            toc_index = i
            break

    # Find "Table of Figures" heading index
    tof_index = None
    tof_style = None
    for i, (style, text) in enumerate(paragraphs):
        if 'table of figures' in text.lower() and text.strip():
            tof_index = i
            tof_style = style
            break

    # Collect actual figure captions from the document body (style='Caption' and starts with 'Figure')
    actual_captions = []
    for style, text in paragraphs:
        if style == 'Caption' and text.strip().lower().startswith('figure'):
            actual_captions.append(text.strip())

    # Component 1: "Table of Figures" heading exists with a Heading style (0.3 points)
    try:
        if tof_index is not None and tof_style is not None and 'Heading' in tof_style:
            print(f"PASS: Component 1 — 'Table of Figures' heading found at paragraph {tof_index} with style '{tof_style}' (0.3 pts)")
            total_score += 0.3
        elif tof_index is not None:
            print(f"FAIL: Component 1 — 'Table of Figures' found but style is '{tof_style}', expected a Heading style")
        else:
            print("FAIL: Component 1 — No 'Table of Figures' heading found in document")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Table of Figures heading is positioned after the Table of Contents (0.2 points)
    try:
        if tof_index is not None and toc_index is not None:
            # Find the first major content heading after TOC (e.g., "1. Introduction")
            first_content_index = None
            for i, (style, text) in enumerate(paragraphs):
                if i > toc_index and 'Heading' in style and text.strip() and 'table of' not in text.lower():
                    # Check if this looks like a content heading (starts with a number or is after TOF)
                    if re.match(r'^\d+\.', text.strip()):
                        first_content_index = i
                        break

            if tof_index > toc_index and (first_content_index is None or tof_index < first_content_index):
                print(f"PASS: Component 2 — Table of Figures (para {tof_index}) is after TOC (para {toc_index}) and before main content (para {first_content_index}) (0.2 pts)")
                total_score += 0.2
            elif tof_index > toc_index:
                print(f"PARTIAL: Component 2 — Table of Figures is after TOC but not before main content")
                total_score += 0.1
            else:
                print(f"FAIL: Component 2 — Table of Figures (para {tof_index}) is NOT after TOC (para {toc_index})")
        elif tof_index is None:
            print("FAIL: Component 2 — No Table of Figures found to check position")
        else:
            print("FAIL: Component 2 — No Table of Contents found to check position against")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 6 figure captions are listed in the table of figures (0.3 points)
    try:
        if tof_index is not None:
            # The table of figures content should be in paragraphs following the TOF heading
            # Look at paragraphs after TOF heading until we hit the next Heading
            tof_content = []
            for i in range(tof_index + 1, len(paragraphs)):
                style, text = paragraphs[i]
                if 'Heading' in style and text.strip():
                    break
                if text.strip():
                    tof_content.append(text)

            tof_text = '\n'.join(tof_content)

            # Count how many figure references appear (Figure 1 through Figure 6)
            figures_found = 0
            for fig_num in range(1, 7):
                pattern = f'Figure {fig_num}'
                if pattern in tof_text:
                    figures_found += 1

            if figures_found == 6:
                print(f"PASS: Component 3 — All 6 figure references found in Table of Figures (0.3 pts)")
                total_score += 0.3
            elif figures_found >= 4:
                partial = round(0.3 * (figures_found / 6), 2)
                print(f"PARTIAL: Component 3 — {figures_found}/6 figure references found ({partial} pts)")
                total_score += partial
            elif figures_found > 0:
                partial = round(0.3 * (figures_found / 6), 2)
                print(f"PARTIAL: Component 3 — Only {figures_found}/6 figure references found ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — No figure references found in Table of Figures content")
        else:
            print("FAIL: Component 3 — No Table of Figures found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Figure captions in TOF match actual captions in document body (0.2 points)
    try:
        if tof_index is not None and len(actual_captions) > 0:
            tof_content = []
            for i in range(tof_index + 1, len(paragraphs)):
                style, text = paragraphs[i]
                if 'Heading' in style and text.strip():
                    break
                if text.strip():
                    tof_content.append(text)

            tof_text = '\n'.join(tof_content)

            # Check how many actual captions appear (at least partially) in the TOF text
            matched = 0
            for caption in actual_captions:
                # Check if the caption text (or at least the key identifier like "Figure N: <description>")
                # appears in the TOF
                # Extract "Figure N:" prefix and first few words
                caption_key = caption.split(':')[0].strip() if ':' in caption else caption[:20]
                if caption_key in tof_text:
                    matched += 1

            if matched == len(actual_captions) and len(actual_captions) >= 6:
                print(f"PASS: Component 4 — All {matched} figure captions match between TOF and document body (0.2 pts)")
                total_score += 0.2
            elif matched > 0:
                partial = round(0.2 * (matched / max(len(actual_captions), 6)), 2)
                print(f"PARTIAL: Component 4 — {matched}/{len(actual_captions)} captions match ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 — No caption matches found between TOF and document body")
        elif tof_index is None:
            print("FAIL: Component 4 — No Table of Figures found")
        else:
            print(f"FAIL: Component 4 — No Caption-styled paragraphs found in document")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(round(total_score, 2), 1.0)
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

"""
Reward Script: Format employee handbook 'Anti-Harassment Policy' with heading hierarchy and horizontal line
Task ID: writer_hr_040
Domain: libreoffice_writer
Scoring:
  Component 1: Title is Heading 1 (0.2 pts)
  Component 2: Horizontal line after title (0.2 pts)
  Component 3: 4 subsections are Heading 2 (0.3 pts)
  Component 4: Sub-subsections are Heading 3 (0.3 pts)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_hr_040'

# Expected subsection titles (Heading 2)
HEADING2_TITLES = ['Definition', 'Reporting Procedures', 'Investigation Process', 'Consequences']

# Expected sub-subsection titles (Heading 3)
HEADING3_TITLES = [
    'Verbal Harassment', 'Physical Harassment', 'Digital Harassment',
    'Internal Reporting Channels', 'External Reporting Options', 'Confidentiality Protections',
    'Initial Assessment', 'Formal Investigation Steps',
    'Disciplinary Actions', 'Repeat Offenses',
]

def persist_app_state(domain):
    """Try to save any open LibreOffice document before verification."""
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
    except ImportError:
        print("CRITICAL: python-docx not installed")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paragraphs = doc.paragraphs

    # Component 1: Title "Anti-Harassment Policy" is Heading 1 (0.2 points)
    try:
        title_para = None
        for para in paragraphs:
            if 'Anti-Harassment Policy' in para.text:
                title_para = para
                break
        if title_para is not None and title_para.style.name == 'Heading 1':
            print(f"PASS: Component 1 — Title 'Anti-Harassment Policy' is Heading 1 (0.2 pts)")
            total_score += 0.2
        else:
            style_found = title_para.style.name if title_para else 'not found'
            print(f"FAIL: Component 1 — Expected Heading 1 for title, found: {style_found}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Horizontal line (bottom border) after title, before first subsection (0.2 points)
    # In docx, a horizontal line is typically an empty paragraph with a bottom border
    try:
        from lxml import etree
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

        # Find the title paragraph index
        title_idx = None
        for i, para in enumerate(paragraphs):
            if 'Anti-Harassment Policy' in para.text:
                title_idx = i
                break

        # Find first Heading 2 index
        first_h2_idx = None
        for i, para in enumerate(paragraphs):
            if para.style.name == 'Heading 2':
                first_h2_idx = i
                break

        hr_count = 0
        if title_idx is not None:
            # Check paragraphs between title and first H2 (or next few paragraphs) for a bottom border
            search_end = first_h2_idx if first_h2_idx is not None else min(title_idx + 5, len(paragraphs))
            for i in range(title_idx + 1, search_end):
                para_el = paragraphs[i]._element
                pBdr = para_el.find('.//w:pBdr', ns)
                if pBdr is not None:
                    bottom = pBdr.find('w:bottom', ns)
                    if bottom is not None:
                        val = bottom.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val', '')
                        if val and val != 'none':
                            hr_count += 1
                            break

        if hr_count > 0:
            print(f"PASS: Component 2 — Horizontal line found after title (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — No horizontal line (bottom border) found after title")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 4 subsections are Heading 2 (0.3 points — 0.075 each)
    try:
        h2_found = []
        for para in paragraphs:
            if para.style.name == 'Heading 2':
                h2_found.append(para.text.strip())

        matched_h2 = 0
        for expected in HEADING2_TITLES:
            if any(expected.lower() in h.lower() for h in h2_found):
                matched_h2 += 1

        pts_per_h2 = 0.3 / len(HEADING2_TITLES)
        h2_score = matched_h2 * pts_per_h2
        if matched_h2 == len(HEADING2_TITLES):
            print(f"PASS: Component 3 — All 4 subsections are Heading 2: {h2_found} (0.3 pts)")
            total_score += 0.3
        elif matched_h2 > 0:
            print(f"PARTIAL: Component 3 — {matched_h2}/4 subsections are Heading 2: {h2_found} ({h2_score:.3f} pts)")
            total_score += h2_score
        else:
            print(f"FAIL: Component 3 — No subsections are Heading 2. H2 paragraphs found: {h2_found}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Sub-subsections are Heading 3 (0.3 points — 0.03 each)
    try:
        h3_found = []
        for para in paragraphs:
            if para.style.name == 'Heading 3':
                h3_found.append(para.text.strip())

        matched_h3 = 0
        for expected in HEADING3_TITLES:
            if any(expected.lower() in h.lower() for h in h3_found):
                matched_h3 += 1

        pts_per_h3 = 0.3 / len(HEADING3_TITLES)
        h3_score = matched_h3 * pts_per_h3
        if matched_h3 == len(HEADING3_TITLES):
            print(f"PASS: Component 4 — All {len(HEADING3_TITLES)} sub-subsections are Heading 3: {h3_found} (0.3 pts)")
            total_score += 0.3
        elif matched_h3 > 0:
            print(f"PARTIAL: Component 4 — {matched_h3}/{len(HEADING3_TITLES)} sub-subsections are Heading 3: {h3_found} ({h3_score:.3f} pts)")
            total_score += h3_score
        else:
            print(f"FAIL: Component 4 — No sub-subsections are Heading 3. H3 paragraphs found: {h3_found}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
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

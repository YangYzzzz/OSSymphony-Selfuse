"""
Reward Script: Apply Internet Link character style to all URLs in a Writer document
Task ID: osworld_writer_character_style_003
Domain: libreoffice_writer
Scoring:
  Component 1: URL 'https://www.asana.com/teams' has InternetLink character style (0.25 pts)
  Component 2: URL 'https://docs.github.com/en/get-started' has InternetLink character style (0.25 pts)
  Component 3: URL 'https://www.figma.com/community/resources' has InternetLink character style (0.25 pts)
  Component 4: URL 'https://www.coursera.org/browse/computer-science' has InternetLink character style (0.25 pts)
  Total: 1.0
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_character_style_003'

# The 4 URLs that must have the InternetLink character style applied
EXPECTED_URLS = [
    'https://www.asana.com/teams',
    'https://docs.github.com/en/get-started',
    'https://www.figma.com/community/resources',
    'https://www.coursera.org/browse/computer-science',
]


def get_run_char_style(run):
    """
    Returns the character style name (w:rStyle w:val) applied to this run,
    or None if no character style is set.
    """
    rPr = run._element.rPr
    if rPr is None:
        return None
    rStyle = rPr.find(qn('w:rStyle'))
    if rStyle is None:
        return None
    return rStyle.get(qn('w:val'))


def verify_task(file_path):
    """
    Verify that all 4 URL runs have the 'InternetLink' character style applied.
    Returns a progressive float between 0.0 and 1.0.
    Each URL contributes 0.25 points.
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Build a dict mapping URL text -> list of runs containing that URL
    url_runs = {url: [] for url in EXPECTED_URLS}
    for para in doc.paragraphs:
        for run in para.runs:
            for url in EXPECTED_URLS:
                if url in run.text:
                    url_runs[url].append(run)

    # Verify each URL — each worth 0.25 points
    for idx, url in enumerate(EXPECTED_URLS, start=1):
        component_pts = 0.25
        try:
            runs = url_runs[url]
            if not runs:
                print(f"FAIL: Component {idx} — URL '{url}' not found in document")
                continue

            # Check if at least one run containing this URL has InternetLink style
            styled = False
            for run in runs:
                style_val = get_run_char_style(run)
                if style_val == 'InternetLink':
                    styled = True
                    break

            if styled:
                print(f"PASS: Component {idx} — URL '{url}' has InternetLink character style ({component_pts} pts)")
                total_score += component_pts
            else:
                # Report what style (if any) was found
                found_styles = [get_run_char_style(r) for r in runs]
                print(f"FAIL: Component {idx} — URL '{url}' does NOT have InternetLink style; found styles: {found_styles}")
        except Exception as e:
            print(f"ERROR: Component {idx} — Could not check URL '{url}': {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

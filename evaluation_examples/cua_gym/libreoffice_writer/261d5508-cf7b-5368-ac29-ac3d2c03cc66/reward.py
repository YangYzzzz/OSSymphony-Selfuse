"""
Reward Script: Promote 'Data Analysis' subsection from Heading 2 to Heading 1
Task ID: writer_fp_029
Domain: libreoffice_writer
Scoring:
  Component 1 (0.30) - 'Data Analysis' is Heading 1
  Component 2 (0.25) - 'Quantitative Methods' and 'Qualitative Methods' are Heading 2
  Component 3 (0.25) - Total Heading 1 count is 7
  Component 4 (0.20) - Chapter numbering updated correctly
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_fp_029'


def persist_app_state(domain):
    """Save any unsaved GUI edits before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in ("libreoffice_calc", "libreoffice_writer", "libreoffice_impress"):
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print("PERSIST: ctrl+s sent for %s" % domain)
        except Exception as e:
            print("PERSIST_WARN: save hook failed: %s" % e)


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    from docx import Document

    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print("CRITICAL: Cannot load file %s: %s" % (file_path, e))
        print("REWARD: 0.0")
        return 0.0

    # Build heading structure for analysis
    headings = []
    for para in doc.paragraphs:
        if para.style.name.startswith('Heading'):
            level = int(para.style.name.replace('Heading ', ''))
            headings.append({'text': para.text.strip(), 'level': level})

    print("INFO: Found %d headings total" % len(headings))
    for h in headings:
        print("  Level %d: %s" % (h['level'], h['text']))

    # Component 1: 'Data Analysis' is Heading 1 (0.30 points)
    # In initial, 'Data Analysis' is Heading 2. In golden, it must be Heading 1.
    try:
        da_level = None
        da_text = None
        for h in headings:
            if 'Data Analysis' in h['text']:
                da_level = h['level']
                da_text = h['text']
                break

        if da_level is not None and da_level == 1:
            print("PASS: Component 1 -- 'Data Analysis' is Heading 1: '%s' (0.30 pts)" % da_text)
            total_score += 0.30
        elif da_level is not None:
            print("FAIL: Component 1 -- 'Data Analysis' is Heading %d, expected Heading 1" % da_level)
        else:
            print("FAIL: Component 1 -- 'Data Analysis' heading not found")
    except Exception as e:
        print("ERROR: Component 1 -- %s" % e)

    # Component 2: 'Quantitative Methods' and 'Qualitative Methods' are Heading 2 (0.25 points)
    # In initial these are Heading 3. In golden they must be promoted to Heading 2.
    try:
        quant_level = None
        qual_level = None

        for h in headings:
            if 'Quantitative Methods' in h['text']:
                quant_level = h['level']
            if 'Qualitative Methods' in h['text']:
                qual_level = h['level']

        if quant_level == 2 and qual_level == 2:
            print("PASS: Component 2 -- Both sub-sections are Heading 2 (0.25 pts)")
            total_score += 0.25
        else:
            print("FAIL: Component 2 -- Quantitative level=%s, Qualitative level=%s; expected both 2"
                  % (quant_level, qual_level))
    except Exception as e:
        print("ERROR: Component 2 -- %s" % e)

    # Component 3: Total number of Heading 1 chapters is 7 (0.25 points)
    # Initial has 6 Heading 1. Golden must have 7.
    try:
        h1_count = sum(1 for h in headings if h['level'] == 1)
        if h1_count == 7:
            print("PASS: Component 3 -- Heading 1 count is 7 (0.25 pts)")
            total_score += 0.25
        else:
            print("FAIL: Component 3 -- Heading 1 count is %d, expected 7" % h1_count)
    except Exception as e:
        print("ERROR: Component 3 -- %s" % e)

    # Component 4: Chapter numbering updated correctly (0.20 points)
    # After promotion, chapters should be renumbered: Data Analysis=4, Results=5, Discussion=6, Conclusion=7
    try:
        h1_headings = [h for h in headings if h['level'] == 1]
        expected_keywords = ['Introduction', 'Literature Review', 'Methodology',
                             'Data Analysis', 'Results', 'Discussion', 'Conclusion']

        matched = 0
        for idx, expected_kw in enumerate(expected_keywords):
            chapter_num = idx + 1
            for h1 in h1_headings:
                if expected_kw in h1['text']:
                    if h1['text'].startswith("%d." % chapter_num) or h1['text'].startswith("%d " % chapter_num):
                        matched += 1
                    else:
                        print("  DETAIL: '%s' does not start with '%d.'" % (h1['text'], chapter_num))
                    break

        if matched == 7:
            print("PASS: Component 4 -- All 7 chapters correctly numbered (0.20 pts)")
            total_score += 0.20
        elif matched >= 5:
            partial = round(0.20 * (matched / 7), 2)
            print("PARTIAL: Component 4 -- %d/7 chapters correctly numbered (%s pts)" % (matched, partial))
            total_score += partial
        else:
            print("FAIL: Component 4 -- Only %d/7 chapters correctly numbered" % matched)
    except Exception as e:
        print("ERROR: Component 4 -- %s" % e)

    final_score = round(min(total_score, 1.0), 2)
    print("\nScore: %s/1.0" % total_score)
    print("REWARD: %s" % final_score)
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = '%s/%s.docx' % (WORKDIR, TASK_ID)
if not os.path.exists(file_path):
    print("File not found: %s" % file_path)
    print("REWARD: 0.0")
else:
    verify_task(file_path)

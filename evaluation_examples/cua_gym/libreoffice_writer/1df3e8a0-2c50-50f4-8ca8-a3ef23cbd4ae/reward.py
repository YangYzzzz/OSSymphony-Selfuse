"""
Reward Script: Enable track changes and insert footnote in Section 3
Task ID: writer_rm_037
Domain: libreoffice_writer
Scoring:
  - Component 1: Track changes enabled (0.35 pts)
  - Component 2: Footnote with correct text exists (0.40 pts)
  - Component 3: Footnote placed in correct paragraph (0.25 pts)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_037'

WNS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print("CRITICAL: Cannot open file %s: %s" % (file_path, e))
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Track changes is enabled (0.35 points)
    # In initial_env: no trackChanges element. In golden_env: trackChanges present.
    try:
        if 'word/settings.xml' in zf.namelist():
            settings_xml = zf.read('word/settings.xml')
            settings_root = ET.fromstring(settings_xml)
            tc_elements = settings_root.findall('.//{%s}trackChanges' % WNS)
            if len(tc_elements) > 0:
                print("PASS: Component 1 - trackChanges element found in settings.xml (0.35 pts)")
                total_score += 0.35
            else:
                print("FAIL: Component 1 - No trackChanges element in settings.xml")
        else:
            print("FAIL: Component 1 - word/settings.xml not found in docx")
    except Exception as e:
        print("ERROR: Component 1 - %s" % e)

    # Component 2: Footnote with correct text exists (0.40 points)
    # In initial_env: no footnotes.xml at all. In golden_env: footnote with expected text.
    expected_footnote_text = 'See Appendix B for detailed statistical analysis.'
    footnote_found = False
    try:
        if 'word/footnotes.xml' in zf.namelist():
            fn_xml = zf.read('word/footnotes.xml')
            fn_root = ET.fromstring(fn_xml)
            footnotes = fn_root.findall('{%s}footnote' % WNS)
            for fn in footnotes:
                fn_id = fn.attrib.get('{%s}id' % WNS, '-1')
                # Skip separator footnotes (id -1 and 0)
                if fn_id in ('-1', '0'):
                    continue
                # Extract text from this footnote
                texts = []
                for t_elem in fn.iter('{%s}t' % WNS):
                    if t_elem.text:
                        texts.append(t_elem.text)
                fn_text = ''.join(texts).strip()
                print("  Found footnote id=%s text='%s'" % (fn_id, fn_text))
                if expected_footnote_text in fn_text:
                    footnote_found = True
                    break

            if footnote_found:
                print("PASS: Component 2 - Footnote with correct text found (0.40 pts)")
                total_score += 0.40
            else:
                print("FAIL: Component 2 - No footnote matching expected text '%s'" % expected_footnote_text)
        else:
            print("FAIL: Component 2 - word/footnotes.xml not found (no footnotes in document)")
    except Exception as e:
        print("ERROR: Component 2 - %s" % e)

    # Component 3: Footnote reference is in the correct paragraph - Section 3 first sentence (0.25 points)
    # The footnote must be in the paragraph starting with "The primary dataset comprised 2,500 survey responses"
    try:
        if 'word/document.xml' in zf.namelist():
            doc_xml = zf.read('word/document.xml')
            doc_root = ET.fromstring(doc_xml)
            paras = doc_root.findall('.//{%s}p' % WNS)

            footnote_in_correct_para = False
            for para in paras:
                fn_refs = para.findall('.//{%s}footnoteReference' % WNS)
                if fn_refs:
                    # Get the full text of this paragraph
                    texts = []
                    for t_elem in para.iter('{%s}t' % WNS):
                        if t_elem.text:
                            texts.append(t_elem.text)
                    para_text = ''.join(texts).strip()
                    print("  Footnote ref in paragraph: '%s...'" % para_text[:80])

                    # Check if this is the Section 3 first paragraph
                    if 'primary dataset comprised 2,500 survey responses' in para_text:
                        footnote_in_correct_para = True
                        break

            if footnote_in_correct_para:
                print("PASS: Component 3 - Footnote reference in correct paragraph (Section 3 first sentence) (0.25 pts)")
                total_score += 0.25
            else:
                print("FAIL: Component 3 - Footnote reference not found in Section 3 first paragraph")
        else:
            print("FAIL: Component 3 - word/document.xml not found")
    except Exception as e:
        print("ERROR: Component 3 - %s" % e)

    zf.close()

    final_score = min(total_score, 1.0)
    print("")
    print("Score: %.2f/1.0" % total_score)
    print("REWARD: %.1f" % final_score)
    return final_score


# Persistence hook: save any unsaved LibreOffice changes
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.0)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print("PERSIST_WARN: save hook failed: %s" % e)


# Main entrypoint
file_path = os.path.join(WORKDIR, TASK_ID + '.docx')
if not os.path.exists(file_path):
    print("File not found: %s" % file_path)
    print("REWARD: 0.0")
else:
    persist_app_state()
    verify_task(file_path)

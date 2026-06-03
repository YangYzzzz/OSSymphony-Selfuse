"""
Reward Script: Insert four endnotes in a LibreOffice Writer document
Task ID: writer_struct_050
Domain: libreoffice_writer
Scoring:
  Component 1 (0.30): endnotes.xml exists and contains exactly 4 normal endnotes
  Component 2 (0.40): all 4 endnote texts match the specified content (exact match)
  Component 3 (0.30): document body contains exactly 4 endnote references
"""

import os
import zipfile
from xml.etree import ElementTree as ET

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_struct_050'
FILE_PATH = os.path.join(WORKDIR, 'global_economics_survey.docx')

# Namespace
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

# Expected endnote texts (in order, ids 1-4)
EXPECTED_ENDNOTE_TEXTS = [
    'Source: World Bank Report, 2024.',
    'Source: IMF Fiscal Monitor, 2024.',
    'Source: Federal Reserve Bulletin, Q3 2024.',
    'Source: European Central Bank Annual Review, 2024.',
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid docx
    if not os.path.exists(file_path):
        print('CRITICAL: File not found: %s' % file_path)
        print('REWARD: 0.0')
        return 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
        zip_files = zf.namelist()
        zf.close()
    except Exception as e:
        print('CRITICAL: Cannot open docx zip: %s' % e)
        print('REWARD: 0.0')
        return 0.0

    # ------------------------------------------------------------------
    # Component 1: endnotes.xml exists and contains exactly 4 normal
    # endnotes (ids 1-4, excluding separator elements with id -1 and 0)
    # (0.30 points)
    # ------------------------------------------------------------------
    normal_endnotes = []
    try:
        if 'word/endnotes.xml' not in zip_files:
            print('FAIL: Component 1 — word/endnotes.xml does not exist in document; no endnotes added')
        else:
            with zipfile.ZipFile(file_path, 'r') as zf:
                end_xml = zf.read('word/endnotes.xml').decode('utf-8')
            end_root = ET.fromstring(end_xml)
            endnotes_all = end_root.findall('{%s}endnote' % W_NS)

            # Collect only normal endnotes (exclude separator elements type=-1, 0)
            for e in endnotes_all:
                etype = e.get('{%s}type' % W_NS, 'normal')
                eid = e.get('{%s}id' % W_NS, '')
                if etype == 'normal' or eid not in ('-1', '0'):
                    # Separator entries have type attribute set; normal ones have no type attr or type='normal'
                    if etype not in ('separator', 'continuationSeparator'):
                        normal_endnotes.append(e)

            if len(normal_endnotes) == 4:
                print('PASS: Component 1 — endnotes.xml exists with exactly 4 normal endnotes (%.2f pts)' % 0.30)
                total_score += 0.30
            else:
                print('FAIL: Component 1 — expected 4 normal endnotes, found %d' % len(normal_endnotes))
    except Exception as e:
        print('ERROR: Component 1 — %s' % e)

    # ------------------------------------------------------------------
    # Component 2: All 4 endnote texts match the required content exactly
    # (0.40 points — 0.10 per endnote, each checked independently)
    # ------------------------------------------------------------------
    # Component 2a: endnote 1 text matches 'Source: World Bank Report, 2024.' (0.10 pts)
    try:
        if len(normal_endnotes) >= 1:
            text_nodes = normal_endnotes[0].findall('.//{%s}t' % W_NS)
            combined = ''.join(t.text for t in text_nodes if t.text).strip()
            if combined == EXPECTED_ENDNOTE_TEXTS[0]:
                print('PASS: Component 2a — endnote 1 text correct: %r (0.10 pts)' % combined)
                total_score += 0.10
            else:
                print('FAIL: Component 2a — endnote 1 expected %r, found %r' % (EXPECTED_ENDNOTE_TEXTS[0], combined))
        else:
            print('FAIL: Component 2a — endnote 1 does not exist')
    except Exception as e:
        print('ERROR: Component 2a — %s' % e)

    # Component 2b: endnote 2 text matches 'Source: IMF Fiscal Monitor, 2024.' (0.10 pts)
    try:
        if len(normal_endnotes) >= 2:
            text_nodes = normal_endnotes[1].findall('.//{%s}t' % W_NS)
            combined = ''.join(t.text for t in text_nodes if t.text).strip()
            if combined == EXPECTED_ENDNOTE_TEXTS[1]:
                print('PASS: Component 2b — endnote 2 text correct: %r (0.10 pts)' % combined)
                total_score += 0.10
            else:
                print('FAIL: Component 2b — endnote 2 expected %r, found %r' % (EXPECTED_ENDNOTE_TEXTS[1], combined))
        else:
            print('FAIL: Component 2b — endnote 2 does not exist')
    except Exception as e:
        print('ERROR: Component 2b — %s' % e)

    # Component 2c: endnote 3 text matches 'Source: Federal Reserve Bulletin, Q3 2024.' (0.10 pts)
    try:
        if len(normal_endnotes) >= 3:
            text_nodes = normal_endnotes[2].findall('.//{%s}t' % W_NS)
            combined = ''.join(t.text for t in text_nodes if t.text).strip()
            if combined == EXPECTED_ENDNOTE_TEXTS[2]:
                print('PASS: Component 2c — endnote 3 text correct: %r (0.10 pts)' % combined)
                total_score += 0.10
            else:
                print('FAIL: Component 2c — endnote 3 expected %r, found %r' % (EXPECTED_ENDNOTE_TEXTS[2], combined))
        else:
            print('FAIL: Component 2c — endnote 3 does not exist')
    except Exception as e:
        print('ERROR: Component 2c — %s' % e)

    # Component 2d: endnote 4 text matches 'Source: European Central Bank Annual Review, 2024.' (0.10 pts)
    try:
        if len(normal_endnotes) >= 4:
            text_nodes = normal_endnotes[3].findall('.//{%s}t' % W_NS)
            combined = ''.join(t.text for t in text_nodes if t.text).strip()
            if combined == EXPECTED_ENDNOTE_TEXTS[3]:
                print('PASS: Component 2d — endnote 4 text correct: %r (0.10 pts)' % combined)
                total_score += 0.10
            else:
                print('FAIL: Component 2d — endnote 4 expected %r, found %r' % (EXPECTED_ENDNOTE_TEXTS[3], combined))
        else:
            print('FAIL: Component 2d — endnote 4 does not exist')
    except Exception as e:
        print('ERROR: Component 2d — %s' % e)

    # ------------------------------------------------------------------
    # Component 3: Document body contains exactly 4 endnote references
    # (0.30 points)
    # ------------------------------------------------------------------
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            doc_xml = zf.read('word/document.xml').decode('utf-8')
        doc_root = ET.fromstring(doc_xml)
        refs = doc_root.findall('.//{%s}endnoteReference' % W_NS)
        ref_count = len(refs)

        if ref_count == 4:
            print('PASS: Component 3 — document body has exactly 4 endnote references (%.2f pts)' % 0.30)
            total_score += 0.30
        else:
            print('FAIL: Component 3 — expected 4 endnote references in document body, found %d' % ref_count)
    except Exception as e:
        print('ERROR: Component 3 — %s' % e)

    final_score = round(min(total_score, 1.0), 2)
    print('')
    print('Score: %.2f/1.0' % total_score)
    print('REWARD: %.1f' % final_score)
    return final_score


if not os.path.exists(FILE_PATH):
    print('File not found: %s' % FILE_PATH)
    print('REWARD: 0.0')
else:
    verify_task(FILE_PATH)

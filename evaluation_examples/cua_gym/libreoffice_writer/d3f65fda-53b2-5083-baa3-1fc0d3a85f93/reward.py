"""
Reward Script: Add a new endnote to the document for the sentence
               'The regulation was first introduced in 1998.'
Task ID: osworld_writer_bibliography_crossref_004
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): New endnote reference placed after anchor sentence in body
  Component 2 (0.4): New endnote text contains the required citation
  Component 3 (0.2): Original endnote (id=2) preserved AND new endnote present
"""

import os
import zipfile
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_bibliography_crossref_004'

# Required endnote citation text (from task specification)
REQUIRED_ENDNOTE_TEXT = 'Regulatory Framework Act, Section 4.2, Government Publications Office, 1998.'

# The anchor sentence in Section 2 where the new endnote ref must be added
ANCHOR_SENTENCE = 'The regulation was first introduced in 1998.'


def parse_endnotes(endnotes_xml):
    """Extract endnote id -> text mappings (excluding separator ids 0 and 1)."""
    result = {}
    pattern = re.compile(
        r'<w:endnote\s[^>]*w:id="(\d+)"[^>]*>(.*?)</w:endnote>',
        re.DOTALL
    )
    for match in pattern.finditer(endnotes_xml):
        en_id = int(match.group(1))
        if en_id >= 2:
            en_content = match.group(2)
            text_parts = re.findall(r'<w:t[^>]*>([^<]*)</w:t>', en_content)
            result[en_id] = ''.join(text_parts).strip()
    return result


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: ensure file is readable as a docx zip
    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print('CRITICAL: Cannot open file as zip: ' + str(e))
        print('REWARD: 0.0')
        return 0.0

    # Read endnotes.xml and document.xml from the zip
    try:
        endnotes_xml = zf.read('word/endnotes.xml').decode('utf-8', errors='replace')
        document_xml = zf.read('word/document.xml').decode('utf-8', errors='replace')
        zf.close()
    except Exception as e:
        print('CRITICAL: Cannot read XML parts from docx: ' + str(e))
        zf.close()
        print('REWARD: 0.0')
        return 0.0

    # Parse endnotes
    endnotes = parse_endnotes(endnotes_xml)
    print('Found endnotes (id >= 2): ' + str(endnotes))

    # Component 1: New endnote reference placed in the paragraph containing anchor sentence (0.4 pts)
    # Checks that an endnoteReference element appears in the paragraph with ANCHOR_SENTENCE
    comp1_passed = False
    comp1_new_id = None
    try:
        para_pattern = re.compile(r'<w:p[ >].*?</w:p>', re.DOTALL)
        paragraphs = para_pattern.findall(document_xml)

        anchor_para_xml = None
        for para_xml in paragraphs:
            text_parts = re.findall(r'<w:t[^>]*>([^<]*)</w:t>', para_xml)
            para_text = ''.join(text_parts)
            if ANCHOR_SENTENCE in para_text:
                anchor_para_xml = para_xml
                break

        if anchor_para_xml is None:
            print('FAIL: Component 1 - Anchor sentence not found in body paragraphs')
        else:
            refs_in_para = re.findall(
                r'<w:endnoteReference\s[^>]*w:id="(\d+)"[^>]*/>', anchor_para_xml
            )
            if refs_in_para:
                comp1_new_id = int(refs_in_para[0])
                comp1_passed = True
                print('PASS: Component 1 - Endnote reference id=' + str(comp1_new_id) +
                      ' found in anchor sentence paragraph (0.4 pts)')
                total_score += 0.4
            else:
                print('FAIL: Component 1 - No endnoteReference in anchor sentence paragraph')
                print('  Para snippet: ' + anchor_para_xml[:400])

    except Exception as e:
        print('ERROR: Component 1 - ' + str(e))

    # Component 2: The new endnote text contains the required citation string (0.4 pts)
    # Looks for any endnote with id != 2 (new ones) whose text matches the required citation.
    comp2_passed = False
    try:
        matching_id = None
        matching_text = None
        for en_id, en_text in endnotes.items():
            if en_id == 2:
                continue
            if REQUIRED_ENDNOTE_TEXT.lower() in en_text.lower():
                matching_id = en_id
                matching_text = en_text
                break

        if matching_id is not None:
            comp2_passed = True
            print('PASS: Component 2 - Endnote id=' + str(matching_id) +
                  ' contains required citation: ' + repr(matching_text) + ' (0.4 pts)')
            total_score += 0.4
        else:
            # Check for partial match to give informative failure message
            required_parts = [
                'Regulatory Framework Act',
                'Section 4.2',
                'Government Publications Office',
                '1998'
            ]
            partial_count = 0
            for en_id, en_text in endnotes.items():
                if en_id == 2:
                    continue
                for part in required_parts:
                    if part.lower() in en_text.lower():
                        partial_count += 1
            new_endnote_texts = {k: v for k, v in endnotes.items() if k != 2}
            print('FAIL: Component 2 - Required citation not found in any new endnote')
            print('  Required: ' + repr(REQUIRED_ENDNOTE_TEXT))
            print('  New endnotes: ' + str(new_endnote_texts))
            if partial_count > 0:
                print('  Partial match: ' + str(partial_count) + '/4 required parts found')

    except Exception as e:
        print('ERROR: Component 2 - ' + str(e))

    # Component 3: Original endnote (id=2) preserved intact AND new endnote was added (0.2 pts)
    # This component only awards points when Component 1 passed (new endnote added),
    # ensuring it does not fire on the initial env where no new endnote exists.
    try:
        original_intact = (2 in endnotes and 'Corporate Governance Act' in endnotes[2])
        has_new_endnote = any(en_id > 2 for en_id in endnotes)

        if original_intact and has_new_endnote:
            print('PASS: Component 3 - Original endnote id=2 intact and new endnote present (0.2 pts)')
            total_score += 0.2
        elif not original_intact:
            print('FAIL: Component 3 - Original endnote id=2 missing or corrupted')
            print('  Endnotes: ' + str(endnotes))
        else:
            print('FAIL: Component 3 - No new endnote found (task not completed)')

    except Exception as e:
        print('ERROR: Component 3 - ' + str(e))

    final_score = min(total_score, 1.0)
    print('\nScore: ' + str(total_score) + '/1.0')
    print('REWARD: ' + str(final_score))
    return final_score


# Default: test against canonical artifact path on VM
file_path = WORKDIR + '/' + TASK_ID + '.docx'
if not os.path.exists(file_path):
    print('File not found: ' + file_path)
    print('REWARD: 0.0')
else:
    verify_task(file_path)

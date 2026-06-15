"""
Reward Script: Reject specific tracked change replacing '$10,000' with '$15,000'
Task ID: writer_struct_045
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5 pts): The '$15,000' insertion tracked change is absent (rejected)
  Component 2 (0.3 pts): The '$10,000' deletion tracked change is absent (rejected)
  Component 3 (0.2 pts): '$10,000' appears as plain (non-tracked) text in the document body
  Total: 1.0
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_struct_045'
FILE_PATH = '/home/user/Desktop/grant_application.docx'


def verify_task(file_path):
    """
    Verify that the tracked change replacing '$10,000' with '$15,000' has been rejected,
    restoring the original '$10,000' amount, while leaving all other tracked changes intact.

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load document — gate on success
    try:
        doc = Document(file_path)
    except Exception as e:
        print('CRITICAL: Cannot load file ' + file_path + ': ' + str(e))
        print('REWARD: 0.0')
        return 0.0

    root = doc.element
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    # Gather all tracked insertions (w:ins) and deletions (w:del)
    insertions = root.findall('.//w:ins', ns)
    deletions = root.findall('.//w:del', ns)

    # Build lists of inserted text values and deleted text values
    ins_texts = []
    for elem in insertions:
        parts = []
        for t in elem.findall('.//w:t', ns):
            parts.append(t.text or '')
        ins_texts.append(''.join(parts))

    del_texts = []
    for elem in deletions:
        parts = []
        for t in elem.findall('.//w:delText', ns):
            parts.append(t.text or '')
        del_texts.append(''.join(parts))

    # Component 1: '$15,000' insertion tracked change has been removed (0.5 points)
    # In initial_env, there is a w:ins with text '$15,000'.
    # After rejecting the change, this insertion must no longer exist.
    try:
        ins_15k_found = any('$15,000' in t for t in ins_texts)
        if not ins_15k_found:
            print('PASS: Component 1 — No w:ins tracked change with "$15,000" found (rejected correctly) (0.5 pts)')
            total_score += 0.5
        else:
            print('FAIL: Component 1 — w:ins tracked change with "$15,000" still present; should have been rejected')
    except Exception as e:
        print('ERROR: Component 1 — ' + str(e))

    # Component 2: '$10,000' deletion tracked change has been removed (0.3 points)
    # In initial_env, there is a w:del with delText '$10,000'.
    # After rejecting the change, this deletion must no longer exist (original text restored).
    try:
        del_10k_found = any('$10,000' in t for t in del_texts)
        if not del_10k_found:
            print('PASS: Component 2 — No w:del tracked change with "$10,000" found (deletion rejected, original restored) (0.3 pts)')
            total_score += 0.3
        else:
            print('FAIL: Component 2 — w:del tracked change with "$10,000" still present; original text should have been restored')
    except Exception as e:
        print('ERROR: Component 2 — ' + str(e))

    # Component 3: '$10,000' appears as plain (non-tracked) text in document body (0.2 points)
    # After rejecting the change, the paragraph should now contain '$10,000' as regular text,
    # not wrapped in any tracked change element.
    try:
        plain_10k_found = False
        for para in doc.paragraphs:
            # para.text concatenates all runs (including those inside tracked changes via python-docx),
            # so we must check the XML directly for plain runs containing '$10,000'
            para_xml = para._element.xml
            # Look for plain w:t containing 10,000 (not inside w:ins or w:del)
            # Strategy: collect all w:r runs at the paragraph level that are NOT inside w:ins/w:del
            plain_runs = para._element.findall('.//w:r', ns)
            for run in plain_runs:
                # Check if this run has a w:ins or w:del ancestor
                parent = run.getparent()
                is_tracked = False
                while parent is not None:
                    tag = parent.tag
                    if tag == qn('w:ins') or tag == qn('w:del'):
                        is_tracked = True
                        break
                    if tag == qn('w:p'):
                        break
                    parent = parent.getparent()
                if not is_tracked:
                    # Check text content
                    run_texts = []
                    for t in run.findall('.//w:t', ns):
                        run_texts.append(t.text or '')
                    run_text = ''.join(run_texts)
                    if '$10,000' in run_text:
                        plain_10k_found = True
                        break
            if plain_10k_found:
                break

        if plain_10k_found:
            print('PASS: Component 3 — "$10,000" present as plain (non-tracked) text in document body (0.2 pts)')
            total_score += 0.2
        else:
            print('FAIL: Component 3 — "$10,000" not found as plain text in document body')
    except Exception as e:
        print('ERROR: Component 3 — ' + str(e))

    # Sanity check: other tracked changes should still be present (not used for scoring)
    try:
        total_ins = len(insertions)
        total_del = len(deletions)
        print('')
        print('INFO: Remaining tracked insertions: ' + str(total_ins))
        print('INFO: Remaining tracked deletions: ' + str(total_del))
        print('INFO: Insertion texts: ' + str(ins_texts))
        print('INFO: Deletion texts: ' + str(del_texts))
    except Exception as e:
        print('INFO: Could not enumerate remaining changes: ' + str(e))

    final_score = min(total_score, 1.0)
    print('')
    print('Score: ' + str(total_score) + '/1.0')
    print('REWARD: ' + str(final_score))
    return final_score


if not os.path.exists(FILE_PATH):
    print('File not found: ' + FILE_PATH)
    print('REWARD: 0.0')
else:
    verify_task(FILE_PATH)

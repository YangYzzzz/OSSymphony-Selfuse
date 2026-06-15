"""
Reward Script: Convert footnotes to endnotes
Task ID: writer_bs_009
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): No footnotes remain in the document
  Component 2 (0.4): All 3 endnotes present with correct text
  Component 3 (0.3): Body contains 3 endnoteReference elements (no footnoteReference)
"""

import os
import zipfile
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_bs_009'
NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

EXPECTED_ENDNOTE_TEXTS = [
    'Source: World Bank, 2022',
    'Adjusted for inflation',
    'See Appendix B for full data',
]


def qn(tag):
    return '{%s}%s' % (NS, tag)


def verify_task(file_path):
    """
    Verify that all three footnotes have been converted to endnotes.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print("CRITICAL: Cannot open file %s: %s" % (file_path, e))
        print("REWARD: 0.0")
        return 0.0

    # Parse all needed XML parts
    try:
        footnotes_root = None
        endnotes_root = None
        body_root = None

        if 'word/footnotes.xml' in zf.namelist():
            footnotes_root = etree.fromstring(zf.read('word/footnotes.xml'))
        if 'word/endnotes.xml' in zf.namelist():
            endnotes_root = etree.fromstring(zf.read('word/endnotes.xml'))
        if 'word/document.xml' in zf.namelist():
            body_root = etree.fromstring(zf.read('word/document.xml'))

        zf.close()
    except Exception as e:
        print("CRITICAL: Cannot parse XML in %s: %s" % (file_path, e))
        print("REWARD: 0.0")
        return 0.0

    # ---------------------------------------------------------------
    # Component 1: No footnotes remain (0.3 points)
    # In initial_env there are 3 normal footnotes; in golden they must be gone.
    # ---------------------------------------------------------------
    try:
        normal_footnotes = []
        if footnotes_root is not None:
            for fn in footnotes_root.findall(qn('footnote')):
                ftype = fn.get(qn('type'), 'normal')
                if ftype == 'normal':
                    normal_footnotes.append(fn)

        # Also check body for footnoteReference elements
        body_fn_refs = []
        if body_root is not None:
            body_fn_refs = body_root.findall('.//' + qn('footnoteReference'))

        if len(normal_footnotes) == 0 and len(body_fn_refs) == 0:
            print("PASS: Component 1 -- No footnotes remain (0 normal footnotes, 0 footnoteReference in body) (0.3 pts)")
            total_score += 0.3
        else:
            print("FAIL: Component 1 -- Found %d normal footnotes, %d footnoteReference in body" % (
                len(normal_footnotes), len(body_fn_refs)))
    except Exception as e:
        print("ERROR: Component 1 -- %s" % e)

    # ---------------------------------------------------------------
    # Component 2: All 3 endnotes present with correct text (0.4 points)
    # Check endnotes.xml for 3 normal endnotes matching the expected texts.
    # ---------------------------------------------------------------
    try:
        normal_endnotes = []
        if endnotes_root is not None:
            for en in endnotes_root.findall(qn('endnote')):
                etype = en.get(qn('type'), 'normal')
                if etype == 'normal':
                    text = ''.join(en.itertext()).strip()
                    normal_endnotes.append(text)

        matched_count = 0
        for expected in EXPECTED_ENDNOTE_TEXTS:
            match_hit = any(expected in actual for actual in normal_endnotes)
            if match_hit:
                matched_count += 1
            else:
                print("FAIL: Component 2 -- Endnote text not found: '%s'" % expected)

        if matched_count == 3:
            print("PASS: Component 2 -- All 3 endnotes present with correct text (0.4 pts)")
            total_score += 0.4
        elif matched_count > 0:
            partial = round(0.4 * matched_count / 3.0, 2)
            print("PARTIAL: Component 2 -- %d/3 endnotes found (%.2f pts)" % (matched_count, partial))
            total_score += partial
        else:
            print("FAIL: Component 2 -- No matching endnotes found. Normal endnotes: %s" % normal_endnotes)
    except Exception as e:
        print("ERROR: Component 2 -- %s" % e)

    # ---------------------------------------------------------------
    # Component 3: Body has 3 endnoteReference elements (0.3 points)
    # In initial_env there are 0; in golden there should be 3.
    # ---------------------------------------------------------------
    try:
        body_en_refs = []
        if body_root is not None:
            body_en_refs = body_root.findall('.//' + qn('endnoteReference'))

        if len(body_en_refs) == 3:
            print("PASS: Component 3 -- Body has 3 endnoteReference elements (0.3 pts)")
            total_score += 0.3
        elif len(body_en_refs) > 0:
            partial = round(0.3 * min(len(body_en_refs), 3) / 3.0, 2)
            print("PARTIAL: Component 3 -- Body has %d endnoteReference (expected 3) (%.2f pts)" % (
                len(body_en_refs), partial))
            if partial > 0:
                total_score += partial
        else:
            print("FAIL: Component 3 -- Body has 0 endnoteReference elements")
    except Exception as e:
        print("ERROR: Component 3 -- %s" % e)

    final_score = min(total_score, 1.0)
    print("\nScore: %.2f/1.0" % total_score)
    print("REWARD: %.1f" % final_score)
    return final_score


# Entry point
file_path = os.path.join(WORKDIR, TASK_ID + '.docx')
if not os.path.exists(file_path):
    print("File not found: %s" % file_path)
    print("REWARD: 0.0")
else:
    verify_task(file_path)

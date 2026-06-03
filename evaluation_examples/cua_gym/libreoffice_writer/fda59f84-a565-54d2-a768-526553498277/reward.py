"""
Reward Script: Insert five footnotes in the literature review section with academic citations.
Task ID: writer_struct_066
Domain: libreoffice_writer
Scoring:
  Component 1: Exactly 5 footnotes exist in the document (0.3 points)
  Component 2: Footnote content matches all 5 required citations (0.5 points, 0.1 per citation)
  Component 3: Exactly 5 footnote references appear in the document body (0.2 points)
  Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_struct_066'
FILE_NAME = 'psychology_thesis.docx'

# Expected citation texts (as stored in footnotes.xml)
EXPECTED_CITATIONS = [
    'Smith, J., Journal of Psychology, Vol. 12, 2019, pp. 34-56.',
    'Brown & Lee, Clinical Review, 2020, pp. 78-92.',
    'Chen et al., Psychological Bulletin, Vol. 45, 2021, pp. 123-145.',
    'Davis, R., Developmental Psychology, 2022, pp. 67-89.',
    'Wilson & Park, Science, 2024, pp. 201-215.',
]


def verify_task(file_path):
    """
    Verify that five academic footnotes were inserted into the literature review
    section of the psychology_thesis.docx document.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate check: verify file exists and is a valid docx
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
        namelist = zf.namelist()
        zf.close()
    except Exception as e:
        print(f"CRITICAL: Cannot open docx file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Exactly 5 normal footnotes exist in word/footnotes.xml (0.3 points)
    # This fails on initial_env (no footnotes.xml) and passes on golden_env (5 footnotes)
    try:
        if 'word/footnotes.xml' not in namelist:
            print("FAIL: Component 1 — word/footnotes.xml not found in document (no footnotes inserted)")
        else:
            with zipfile.ZipFile(file_path, 'r') as zf:
                footnotes_xml = zf.read('word/footnotes.xml').decode('utf-8')

            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            fn_root = ET.fromstring(footnotes_xml)
            fn_type_attr = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}type'

            # Count normal footnotes (exclude separator and continuationSeparator types)
            normal_footnotes = [
                fn for fn in fn_root.findall('w:footnote', ns)
                if fn.attrib.get(fn_type_attr, 'normal') == 'normal'
                   or fn_type_attr not in fn.attrib
            ]
            # Filter: IDs -1 and 0 are special separator footnotes even without explicit type
            normal_footnotes = [
                fn for fn in normal_footnotes
                if fn.attrib.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}id') not in ('-1', '0')
                   and fn.attrib.get(fn_type_attr, 'normal') not in ('separator', 'continuationSeparator')
            ]

            fn_count = len(normal_footnotes)
            if fn_count == 5:
                print(f"PASS: Component 1 — Found exactly 5 footnotes (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 — Expected 5 footnotes, found {fn_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Footnote content matches all 5 required academic citations (0.5 points, 0.1 each)
    # Each citation that matches earns 0.1 points
    try:
        if 'word/footnotes.xml' not in namelist:
            print("FAIL: Component 2 — word/footnotes.xml not present, cannot verify citations")
        else:
            with zipfile.ZipFile(file_path, 'r') as zf:
                footnotes_xml = zf.read('word/footnotes.xml').decode('utf-8')

            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            fn_root = ET.fromstring(footnotes_xml)
            fn_type_attr = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}type'

            # Extract text from each normal footnote
            footnote_texts = []
            for fn in fn_root.findall('w:footnote', ns):
                fn_id = fn.attrib.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}id')
                fn_type_val = fn.attrib.get(fn_type_attr, 'normal')
                # Skip separator footnotes
                if fn_type_val in ('separator', 'continuationSeparator'):
                    continue
                if fn_id in ('-1', '0'):
                    continue
                # Get all text nodes
                text_parts = []
                for t in fn.findall('.//w:t', ns):
                    text_parts.append(t.text or '')
                text = ''.join(text_parts).strip()
                footnote_texts.append(text)

            # Check each expected citation against actual footnote texts
            citations_matched = 0
            for expected in EXPECTED_CITATIONS:
                citation_matched = any(
                    expected.strip() in actual
                    or actual in expected.strip()
                    or expected.replace('&', '&amp;').strip() in actual
                    for actual in footnote_texts
                )
                if citation_matched:
                    print(f"PASS: Component 2 — Citation found: '{expected[:60]}...' (+0.1 pts)")
                    citations_matched += 1
                else:
                    print(f"FAIL: Component 2 — Citation not found: '{expected[:60]}...'")
                    print(f"      Available footnotes: {footnote_texts}")

            if citations_matched > 0:
                total_score += round(citations_matched * 0.1, 2)
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Exactly 5 footnote references appear in the document body (0.2 points)
    # Initial env has 0 footnote references; golden env has 5
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            doc_xml = zf.read('word/document.xml').decode('utf-8')

        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        doc_root = ET.fromstring(doc_xml)
        fn_refs = doc_root.findall('.//w:footnoteReference', ns)
        ref_count = len(fn_refs)

        if ref_count == 5:
            print(f"PASS: Component 3 — Found exactly 5 footnote references in document body (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Expected 5 footnote references in document body, found {ref_count}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{FILE_NAME}'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

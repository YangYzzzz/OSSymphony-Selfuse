"""
Reward Script: Remove all hyperlinks from resource_guide.docx
Task ID: osworld_writer_easy_032
Domain: libreoffice_writer
Scoring:
  Component 1: All 12 hyperlink XML elements removed from document body (0.5 pts)
  Component 2: All hyperlink relationships removed from document part (0.2 pts)
  Component 3: Link text preserved as plain text in document (0.3 pts)
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_easy_032'
FILE_PATH = f'{WORKDIR}/resource_guide.docx'

# The 12 link texts that must remain as plain text after hyperlinks are removed
EXPECTED_LINK_TEXTS = [
    'https://edu.gcfglobal.org/en/',
    'click here',
    'https://www.khanacademy.org/computing',
    'https://www.linkedin.com/jobs/',
    'learn more here',
    'https://www.careeronestop.org/',
    'https://www.benefits.gov/',
    'Get coverage now',
    'https://www.irs.gov/filing/free-file-do-your-federal-taxes-for-free',
    'https://medlineplus.gov/',
    "visit SAMHSA's helpline page",
    'https://www.volunteermatch.org/',
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the document - precondition gate
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Namespaces for XML parsing
    ns = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    }

    # Component 1: All hyperlink XML elements removed from document body (0.5 points)
    # The task requires removing all clickable hyperlinks — meaning no <w:hyperlink> elements
    # should remain in the document body. Initial env has 12; golden env should have 0.
    try:
        hyperlinks = doc.element.body.findall('.//w:hyperlink', ns)
        num_hyperlinks = len(hyperlinks)
        if num_hyperlinks == 0:
            print(f"PASS: Component 1 — All hyperlink XML elements removed (found 0) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — Expected 0 hyperlink elements, found {num_hyperlinks}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All hyperlink relationships removed from document part (0.2 points)
    # Proper removal also cleans up the relationships table. Initial env has 12 hyperlink rels;
    # golden env should have 0.
    try:
        rels = doc.part.rels
        hyperlink_rels = [
            rel for rel in rels.values()
            if 'hyperlink' in rel.reltype.lower()
        ]
        num_hl_rels = len(hyperlink_rels)
        if num_hl_rels == 0:
            print(f"PASS: Component 2 — All hyperlink relationships removed (found 0) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — Expected 0 hyperlink relationships, found {num_hl_rels}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Link text preserved as plain non-hyperlink text (0.3 points)
    # This is a COMPOUND check: hyperlinks must be absent AND the link text must still
    # appear in the document body as plain runs (not inside <w:hyperlink> elements).
    # This fails on initial_env because the text there is INSIDE hyperlinks (not plain).
    # This passes on golden_env because hyperlinks are gone but text remains as plain runs.
    try:
        # Collect text from plain runs (not inside hyperlink elements)
        # We extract runs that are NOT children of <w:hyperlink> nodes
        plain_run_text = []
        for para in doc.element.body.findall('.//w:p', ns):
            # Get all runs directly in the paragraph (exclude runs inside hyperlinks)
            for run in para.findall('w:r', ns):
                t_elems = run.findall('w:t', ns)
                for t in t_elems:
                    if t.text:
                        plain_run_text.append(t.text)

        plain_text_joined = ' '.join(plain_run_text)

        # Count how many of the expected link texts appear as plain (non-hyperlink) runs
        preserved_count = 0
        missing_texts = []
        for link_text in EXPECTED_LINK_TEXTS:
            if link_text.lower() in plain_text_joined.lower():
                preserved_count += 1
            else:
                missing_texts.append(link_text)

        if preserved_count == len(EXPECTED_LINK_TEXTS):
            print(f"PASS: Component 3 — All {len(EXPECTED_LINK_TEXTS)} link texts preserved as plain (non-hyperlink) text (0.3 pts)")
            total_score += 0.3
        elif preserved_count >= int(len(EXPECTED_LINK_TEXTS) * 0.75):
            # Partial credit: most texts preserved as plain text (9 or more out of 12)
            print(f"PARTIAL: Component 3 — {preserved_count}/{len(EXPECTED_LINK_TEXTS)} plain texts found; missing: {missing_texts[:3]} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — Only {preserved_count}/{len(EXPECTED_LINK_TEXTS)} link texts preserved as plain text; "
                  f"missing: {missing_texts[:3]}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint: test against canonical artifact on the VM
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

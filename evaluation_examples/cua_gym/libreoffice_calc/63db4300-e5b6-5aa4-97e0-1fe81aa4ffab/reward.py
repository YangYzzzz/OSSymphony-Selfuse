"""
Reward Script: Correct bibliography in thesis_chapter.docx to Chicago author-date style
Task ID: osworld_multi_apps_misc_043
Domain: libreoffice_writer
Scoring:
  Component 1: Bergmann entry fully corrected (year format, article title, journal format) — 0.20
  Component 2: Kumar entry fully corrected (year format + multi-author format) — 0.20
  Component 3: Chen multi-author format corrected — 0.10
  Component 4: Morris multi-author format corrected — 0.15
  Component 5: Okafor multi-author format corrected — 0.10
  Component 6: Nakamura period after author name corrected — 0.10
  Component 7: Yamamoto period after author name corrected — 0.10
  Component 8: Rivera journal volume/issue spacing corrected — 0.05
  Total: 1.00

Note: Component 9 (all entries present) is used as a PRECONDITION GATE only,
not as a scored component, since entries are present in both initial and golden environments.
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_misc_043'
FILE_PATH = '/home/user/Desktop/drafts/thesis_chapter.docx'

# Expected golden text for each corrected bibliography entry (Chicago author-date style)
GOLDEN_BERGMANN  = 'Bergmann, Klaus. 2023. "Automated Metadata Extraction Using Neural Networks." Journal of Digital Humanities 12 (3): 88-107.'
GOLDEN_KUMAR     = 'Kumar, Arjun, and Soo-Jin Lee. 2022. Machine Learning Applications in Archival Research. Boston: MIT Press.'
GOLDEN_CHEN      = 'Chen, Mei, and Robert Williams. 2020. "Colonial Networks in the Digital Age." Pacific Historical Review 89 (2): 210-245.'
GOLDEN_MORRIS    = 'Morris, James, and Anita Patel. 2016. Preservation Standards in Digital Libraries. London: Routledge.'
GOLDEN_OKAFOR   = 'Okafor, Chidinma, and Harbhajan Singh. 2019. Cross-Institutional Data Consistency in Digital Archives. Cambridge: Cambridge University Press.'
GOLDEN_NAKAMURA  = 'Nakamura, Yuki. 2018. Metadata Frameworks for Historical Digitization Projects. New York: Columbia University Press.'
GOLDEN_YAMAMOTO  = 'Yamamoto, Hiroshi. 2017. OCR Errors and Textual Analysis: A Methodological Study. Edinburgh: Edinburgh University Press.'
GOLDEN_RIVERA    = 'Rivera, Maria. 2021. "Challenges in Multi-Institutional Cataloging Projects." Library Quarterly 91 (4): 312-330.'


def get_bibliography_entries(doc):
    """
    Extract all paragraph texts in the Bibliography section.
    Returns a dict keyed by first author surname.
    """
    bib_entries = {}
    in_bib = False
    for para in doc.paragraphs:
        if 'Bibliography' in para.text and para.style.name.startswith('Heading'):
            in_bib = True
            continue
        if in_bib and para.text.strip():
            # Key by first word (surname before comma)
            key = para.text.strip().split(',')[0].strip()
            bib_entries[key] = para.text.strip()
    return bib_entries


def verify_task(file_path):
    """
    Verify bibliography corrections in thesis_chapter.docx for Chicago author-date style.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract bibliography entries
    try:
        bib_entries = get_bibliography_entries(doc)
        print(f"INFO: Found {len(bib_entries)} bibliography entries")
        for k, v in bib_entries.items():
            print(f"  [{k}]: {v}")
    except Exception as e:
        print(f"CRITICAL: Cannot extract bibliography: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: verify the bibliography section exists and has all expected entries.
    # This checks a pre-existing property (both envs have 10 entries) so it is NOT scored.
    expected_authors = {'Bergmann', 'Chen', 'Henderson', 'Kumar', 'Morris', 'Nakamura', 'Okafor', 'Rivera', 'Thompson', 'Yamamoto'}
    found_authors = set(bib_entries.keys())
    missing = expected_authors - found_authors
    if missing:
        print(f"PRECONDITION FAIL: Missing bibliography entries: {missing}")
        print("REWARD: 0.0")
        return 0.0
    print(f"PRECONDITION PASS: All 10 expected entries present")

    # Component 1: Bergmann entry fully corrected (0.20 pts)
    # Fixes: parenthetical year → period-year, article title in double quotes,
    #        journal volume format (no comma before volume, space before issue, colon before pages)
    try:
        actual = bib_entries.get('Bergmann', '')
        if actual == GOLDEN_BERGMANN:
            print(f"PASS: Component 1 — Bergmann entry correctly formatted (0.20 pts)")
            print(f"  Found: {actual}")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — Bergmann entry not correctly formatted")
            print(f"  Expected: {GOLDEN_BERGMANN}")
            print(f"  Found:    {actual}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Kumar entry fully corrected (0.20 pts)
    # Fixes: parenthetical year → period-year, multi-author "and Lee, Soo-Jin" → ", and Soo-Jin Lee"
    try:
        actual = bib_entries.get('Kumar', '')
        if actual == GOLDEN_KUMAR:
            print(f"PASS: Component 2 — Kumar entry correctly formatted (0.20 pts)")
            print(f"  Found: {actual}")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — Kumar entry not correctly formatted")
            print(f"  Expected: {GOLDEN_KUMAR}")
            print(f"  Found:    {actual}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Chen multi-author format corrected (0.10 pts)
    # Fix: "Chen, Mei and Williams, Robert." → "Chen, Mei, and Robert Williams."
    try:
        actual = bib_entries.get('Chen', '')
        if actual == GOLDEN_CHEN:
            print(f"PASS: Component 3 — Chen entry correctly formatted (0.10 pts)")
            print(f"  Found: {actual}")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 — Chen entry not correctly formatted")
            print(f"  Expected: {GOLDEN_CHEN}")
            print(f"  Found:    {actual}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Morris multi-author format corrected (0.15 pts)
    # Fix: "Morris, James and Patel, Anita, 2016." → "Morris, James, and Anita Patel. 2016."
    try:
        actual = bib_entries.get('Morris', '')
        if actual == GOLDEN_MORRIS:
            print(f"PASS: Component 4 — Morris entry correctly formatted (0.15 pts)")
            print(f"  Found: {actual}")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — Morris entry not correctly formatted")
            print(f"  Expected: {GOLDEN_MORRIS}")
            print(f"  Found:    {actual}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Okafor multi-author format corrected (0.10 pts)
    # Fix: "Okafor, Chidinma and Singh, Harbhajan." → "Okafor, Chidinma, and Harbhajan Singh."
    try:
        actual = bib_entries.get('Okafor', '')
        if actual == GOLDEN_OKAFOR:
            print(f"PASS: Component 5 — Okafor entry correctly formatted (0.10 pts)")
            print(f"  Found: {actual}")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 — Okafor entry not correctly formatted")
            print(f"  Expected: {GOLDEN_OKAFOR}")
            print(f"  Found:    {actual}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Nakamura period after author name corrected (0.10 pts)
    # Fix: "Nakamura, Yuki 2018." → "Nakamura, Yuki. 2018."
    try:
        actual = bib_entries.get('Nakamura', '')
        if actual == GOLDEN_NAKAMURA:
            print(f"PASS: Component 6 — Nakamura entry correctly formatted (0.10 pts)")
            print(f"  Found: {actual}")
            total_score += 0.10
        else:
            print(f"FAIL: Component 6 — Nakamura entry not correctly formatted")
            print(f"  Expected: {GOLDEN_NAKAMURA}")
            print(f"  Found:    {actual}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: Yamamoto period after author name corrected (0.10 pts)
    # Fix: "Yamamoto, Hiroshi 2017." → "Yamamoto, Hiroshi. 2017."
    try:
        actual = bib_entries.get('Yamamoto', '')
        if actual == GOLDEN_YAMAMOTO:
            print(f"PASS: Component 7 — Yamamoto entry correctly formatted (0.10 pts)")
            print(f"  Found: {actual}")
            total_score += 0.10
        else:
            print(f"FAIL: Component 7 — Yamamoto entry not correctly formatted")
            print(f"  Expected: {GOLDEN_YAMAMOTO}")
            print(f"  Found:    {actual}")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    # Component 8: Rivera journal volume/issue spacing corrected (0.05 pts)
    # Fix: "Library Quarterly 91(4): 312-330" → "Library Quarterly 91 (4): 312-330"
    try:
        actual = bib_entries.get('Rivera', '')
        if actual == GOLDEN_RIVERA:
            print(f"PASS: Component 8 — Rivera entry correctly formatted (0.05 pts)")
            print(f"  Found: {actual}")
            total_score += 0.05
        else:
            print(f"FAIL: Component 8 — Rivera entry not correctly formatted")
            print(f"  Expected: {GOLDEN_RIVERA}")
            print(f"  Found:    {actual}")
    except Exception as e:
        print(f"ERROR: Component 8 — {e}")

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {round(total_score, 4)}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

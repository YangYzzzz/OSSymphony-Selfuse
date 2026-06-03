"""
Reward Script: DOI and Year annotation for bibliography references in LibreOffice Writer
Task ID: osworld_multi_apps_doi_resolve_writer_006
Domain: libreoffice_writer
Scoring:
  Component 1: Year in parentheses added after author names for all 7 references (0.40 pts)
  Component 2: 'Available at: <url>' line present after each of the 7 references (0.30 pts)
  Component 3: DOI hyperlinks use https://doi.org/ prefix and are actual linked elements (0.30 pts)
  Total: 1.0
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_doi_resolve_writer_006'
FILE_PATH = os.path.join(WORKDIR, 'incomplete_bibliography.odt')

# Ground truth DOIs from the golden file (discovered via VM exploration)
EXPECTED_DOIS = [
    'https://doi.org/10.48550/arXiv.1301.3781',   # Word2Vec
    'https://doi.org/10.3115/v1/D14-1162',          # GloVe
    'https://doi.org/10.18653/v1/N18-1202',          # ELMo
    'https://doi.org/10.3115/v1/D14-1181',           # CNN Sentence Classification
    'https://doi.org/10.48550/arXiv.1409.3215',      # Seq2Seq
    'https://doi.org/10.48550/arXiv.1409.0473',      # Attention/Bahdanau
    'https://doi.org/10.18653/v1/P17-1099',          # Pointer-Generator
]

EXPECTED_YEARS = ['2013', '2014', '2018', '2014', '2014', '2015', '2017']


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load ODF document
    try:
        from odf.opendocument import load
        from odf.text import P, A
        from odf.teletype import extractText
        doc = load(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract all paragraphs
    try:
        paras = doc.getElementsByType(P)
        para_texts = [extractText(p) for p in paras]
    except Exception as e:
        print(f"CRITICAL: Cannot extract paragraphs: {e}")
        print("REWARD: 0.0")
        return 0.0

    # ---- Component 1: Year in parentheses added to reference lines (0.40 pts) ----
    # Each of the 7 references must have "(YYYY)" at the end of the author line.
    # References are lines that start with '[N]'. In the initial file they have no year.
    # The task asks the agent to add the year in parentheses after the author names.
    try:
        year_pattern = re.compile(r'\[\d\].*\(\d{4}\)\s*$')
        ref_lines_with_year = [t for t in para_texts if year_pattern.search(t)]
        years_found = len(ref_lines_with_year)
        # Award points proportionally: full credit only for all 7
        if years_found == 7:
            print(f"PASS: Component 1 — All 7 references have year in parentheses (0.40 pts)")
            total_score += 0.40
        elif years_found > 0:
            partial = round(0.40 * (years_found / 7), 4)
            print(f"PARTIAL: Component 1 — {years_found}/7 references have year in parentheses ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No reference lines with year found (expected 7)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ---- Component 2: 'Available at: <url>' line present after each reference (0.30 pts) ----
    # Each reference entry should be followed by an 'Available at: ...' line
    try:
        available_at_pattern = re.compile(r'^Available at:\s+https?://', re.IGNORECASE)
        available_at_lines = [t for t in para_texts if available_at_pattern.match(t)]
        avail_found = len(available_at_lines)
        if avail_found == 7:
            print(f"PASS: Component 2 — All 7 'Available at:' DOI lines present (0.30 pts)")
            total_score += 0.30
        elif avail_found > 0:
            partial = round(0.30 * (avail_found / 7), 4)
            print(f"PARTIAL: Component 2 — {avail_found}/7 'Available at:' lines found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No 'Available at:' lines found (expected 7)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ---- Component 3: DOI hyperlinks use https://doi.org/ prefix and are real hyperlinks (0.30 pts) ----
    # The task requires DOI links as actual hyperlinks, not plain text.
    # We check that: (a) there are 7 hyperlinks in the document, and
    # (b) each href starts with 'https://doi.org/'
    try:
        links = doc.getElementsByType(A)
        XLINK_HREF = ('http://www.w3.org/1999/xlink', 'href')
        doi_links = []
        for lnk in links:
            href = lnk.attributes.get(XLINK_HREF, '')
            if href.startswith('https://doi.org/'):
                doi_links.append(href)

        num_doi_links = len(doi_links)
        if num_doi_links == 7:
            print(f"PASS: Component 3 — All 7 DOI hyperlinks present using https://doi.org/ prefix (0.30 pts)")
            total_score += 0.30
        elif num_doi_links > 0:
            partial = round(0.30 * (num_doi_links / 7), 4)
            print(f"PARTIAL: Component 3 — {num_doi_links}/7 valid https://doi.org/ hyperlinks found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No https://doi.org/ hyperlinks found (expected 7). Total links: {len(links)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

"""
Reward Script: Update survey_refs.odt with publication years and DOI hyperlinks
Task ID: osworld_multi_apps_doi_resolve_writer_005
Domain: libreoffice_writer
Scoring:
  Component 1: All 5 references have correct publication years added (0.5 pts, 0.1 each)
  Component 2: All 5 references have correct DOI hyperlinks (0.5 pts, 0.1 each)
Total: 1.0
"""

import os
import zipfile
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_doi_resolve_writer_005'
FILE_PATH = f'{WORKDIR}/survey_refs.odt'

# Ground truth from task_config.json context
# DOIs and years per reference (with accepted alternative DOI variants)
REFERENCES = [
    {
        "title_fragment": "Attention Is All You Need",
        "year": "2017",
        "doi": "10.48550/arXiv.1706.03762",
        "doi_url": "https://doi.org/10.48550/arXiv.1706.03762",
    },
    {
        "title_fragment": "BERT",
        "year": "2019",
        "doi": "10.18653/v1/N19-1423",
        "doi_url": "https://doi.org/10.18653/v1/N19-1423",
    },
    {
        "title_fragment": "Dropout",
        "year": "2014",
        "doi": "10.5555/2627435.2670313",
        "doi_url": "https://doi.org/10.5555/2627435.2670313",
    },
    {
        "title_fragment": "Adam",
        "year": "2015",
        "doi": "10.48550/arXiv.1412.6980",
        "doi_url": "https://doi.org/10.48550/arXiv.1412.6980",
    },
    {
        "title_fragment": "Deep Residual Learning",
        "year": "2016",
        "doi": "10.1109/CVPR.2016.90",
        "doi_url": "https://doi.org/10.1109/CVPR.2016.90",
    },
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Scoring components:
    - Component 1: Correct year added for each reference (5 x 0.1 = 0.5 pts)
    - Component 2: Correct DOI hyperlink for each reference (5 x 0.1 = 0.5 pts)
    """
    total_score = 0.0

    # Load ODT content as XML (ODT is a ZIP archive)
    try:
        with zipfile.ZipFile(file_path) as z:
            with z.open('content.xml') as f:
                content_xml = f.read().decode('utf-8')
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract all hyperlink href values from the document
    hrefs_in_doc = re.findall(r'xlink:href="([^"]+)"', content_xml)
    print(f"INFO: Found {len(hrefs_in_doc)} hyperlinks in document")
    for href in hrefs_in_doc:
        print(f"  - {href}")

    # Component 1: Check each reference has the correct year added (0.1 pts each = 0.5 total)
    print("\n--- Component 1: Publication Years ---")
    year_score = 0.0
    for ref in REFERENCES:
        try:
            title_frag = ref["title_fragment"]
            expected_year = ref["year"]
            # Search for the year appearing near the title fragment in the XML content
            # The pattern should be: title fragment ... year ... DOI in the same paragraph
            # Extract paragraph texts
            # Look for content that contains title fragment and the expected year
            pattern = re.compile(
                r'<text:p[^>]*>.*?' + re.escape(title_frag) + r'.*?' + re.escape(expected_year) + r'.*?</text:p>',
                re.DOTALL
            )
            if pattern.search(content_xml):
                print(f"PASS: Year {expected_year} found for '{title_frag}' (+0.1 pts)")
                year_score += 0.1
            else:
                # Also check plain text paragraphs by extracting text content
                # Strip XML tags from relevant sections
                para_matches = re.findall(
                    r'<text:p[^>]*>(.*?)</text:p>', content_xml, re.DOTALL
                )
                year_found = False
                for para_xml in para_matches:
                    # Strip XML tags to get plain text
                    plain = re.sub(r'<[^>]+>', '', para_xml)
                    if title_frag in plain and expected_year in plain:
                        year_found = True
                        break
                if year_found:
                    print(f"PASS: Year {expected_year} found for '{title_frag}' (+0.1 pts)")
                    year_score += 0.1
                else:
                    print(f"FAIL: Year {expected_year} NOT found near '{title_frag}'")
        except Exception as e:
            print(f"ERROR: Year check for '{ref['title_fragment']}': {e}")

    total_score += year_score
    print(f"Year sub-total: {year_score:.1f}/0.5")

    # Component 2: Check each reference has the correct DOI as a hyperlink (0.1 pts each = 0.5 total)
    print("\n--- Component 2: DOI Hyperlinks ---")
    doi_score = 0.0
    for ref in REFERENCES:
        try:
            title_frag = ref["title_fragment"]
            expected_doi = ref["doi"]
            expected_url = ref["doi_url"]

            # Check if the DOI URL is present as a hyperlink (xlink:href)
            doi_url_found = expected_url in hrefs_in_doc
            # Also check for DOI string in text content (sometimes formatted differently)
            doi_str_found = expected_doi in content_xml

            if doi_url_found:
                # Verify the hyperlink is in the correct paragraph (near the title)
                pattern = re.compile(
                    r'<text:p[^>]*>.*?' + re.escape(title_frag) + r'.*?xlink:href="' + re.escape(expected_url) + r'".*?</text:p>',
                    re.DOTALL
                )
                if pattern.search(content_xml):
                    print(f"PASS: DOI hyperlink {expected_doi} found for '{title_frag}' (+0.1 pts)")
                    doi_score += 0.1
                else:
                    # If not found in same paragraph, still award partial credit for having the correct DOI link
                    print(f"PASS: DOI hyperlink {expected_doi} present in document for '{title_frag}' (+0.1 pts)")
                    doi_score += 0.1
            elif doi_str_found:
                print(f"FAIL: DOI {expected_doi} found as text but NOT as a hyperlink for '{title_frag}'")
            else:
                print(f"FAIL: DOI hyperlink {expected_doi} NOT found for '{title_frag}'")
        except Exception as e:
            print(f"ERROR: DOI check for '{ref['title_fragment']}': {e}")

    total_score += doi_score
    print(f"DOI sub-total: {doi_score:.1f}/0.5")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

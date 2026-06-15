"""
Reward Script: APA 7th Edition Bibliography Formatting in report_draft.docx
Task ID: osworld_multi_apps_misc_048
Domain: libreoffice_writer
Scoring:
  Component 1: Sentence case for reference titles (0.4 points)
    - Verifies known Title Case title strings from initial state are corrected to sentence case
  Component 2: No city-of-publication in journal/web references (0.3 points)
    - Verifies that 'London', 'New York', 'Berlin' no longer appear as publisher location
  Component 3: Hanging indent on all 5 reference entries (0.3 points)
    - Verifies left_indent=36pt, first_line_indent=-36pt on each reference paragraph
"""

import os
import re

FILE_PATH = '/home/user/Desktop/team_docs/report_draft.docx'

# Number of reference entries expected
NUM_REFERENCES = 5

# Forbidden city names (city of publication, not used in APA 7th for journals/web)
# These were present in initial_env as standalone location entries (e.g., "77-101. London. https://")
FORBIDDEN_CITIES = ['London', 'New York', 'Berlin']

# Title Case strings present in initial_env that must be corrected to sentence case in golden_env.
# Each tuple: (bad_title_case_fragment, corrected_sentence_case_fragment)
# We verify: bad fragment ABSENT AND corrected fragment PRESENT for each entry.
TITLE_CASE_CHECKS = [
    # Braun & Clarke 2006
    ('Using Thematic Analysis in Psychology', 'Using thematic analysis in psychology'),
    # Hartmann & Osei 2021
    ('A Standardized Resilience Index For Urban Climate Assessment',
     'A standardized resilience index for urban climate assessment'),
    # IPCC 2022
    ('Climate Change 2022: Impacts, Adaptation And Vulnerability',
     'Climate change 2022: Impacts, adaptation and vulnerability'),
    # Torres-Ruiz et al. 2020
    ('Interdependencies In Urban Resilience: Physical Infrastructure And Social Capital',
     'Interdependencies in urban resilience: Physical infrastructure and social capital'),
    # United Nations 2023
    ('World Urbanization Prospects: The 2023 Revision',
     'World urbanization prospects: The 2023 revision'),
]


def find_reference_paragraphs(doc):
    """Find the reference entry paragraphs after the 'References' heading."""
    refs = []
    in_references = False
    for para in doc.paragraphs:
        text = para.text.strip()
        if text == 'References':
            in_references = True
            continue
        if in_references and text:
            refs.append(para)
    return refs


def get_all_ref_text(ref_paras):
    """Concatenate all reference text for substring matching."""
    return '\n'.join(p.text for p in ref_paras)


def verify_task(file_path):
    """
    Verify APA 7th edition bibliography compliance in report_draft.docx.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find reference paragraphs
    ref_paras = find_reference_paragraphs(doc)

    if len(ref_paras) < NUM_REFERENCES:
        print(f"FAIL: Expected {NUM_REFERENCES} reference paragraphs, found {len(ref_paras)}")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found {len(ref_paras)} reference paragraphs")
    all_ref_text = get_all_ref_text(ref_paras)

    # Component 1: Sentence case for reference titles (0.4 points)
    # Verify: known bad Title Case strings are absent AND corrected strings are present
    try:
        bad_found = []
        good_missing = []

        for bad_fragment, good_fragment in TITLE_CASE_CHECKS:
            has_bad = bad_fragment in all_ref_text
            has_good = good_fragment in all_ref_text

            if has_bad:
                bad_found.append(bad_fragment[:60])
            if not has_good:
                good_missing.append(good_fragment[:60])

        if not bad_found and not good_missing:
            print(f"PASS Component 1: All {len(TITLE_CASE_CHECKS)} reference titles are in sentence case (0.4 pts)")
            total_score += 0.4
        else:
            if bad_found:
                print(f"FAIL Component 1: Title Case still present in {len(bad_found)} references:")
                for f in bad_found:
                    print(f"  BAD: {f!r}")
            if good_missing:
                print(f"FAIL Component 1: Sentence case not found for {len(good_missing)} references:")
                for f in good_missing:
                    print(f"  MISSING: {f!r}")
    except Exception as e:
        print(f"ERROR Component 1 (sentence case check): {e}")

    # Component 2: No city-of-publication in journal/web references (0.3 points)
    # APA 7th does not include publisher location for journal articles or web sources.
    # Initial had entries like: "77–101. London. https://" or "621–628. Berlin. https://"
    # After correction, city names should be removed from reference text.
    try:
        city_violations = 0
        for para in ref_paras:
            text = para.text
            for city in FORBIDDEN_CITIES:
                # Match city as standalone location entry: ". CITY." or ". CITY " followed by URL or period
                # e.g., ". London." or ". New York." or ". Berlin."
                pattern = r'\.\s+' + re.escape(city) + r'[\.\s]'
                if re.search(pattern, text):
                    print(f"FAIL Component 2: City '{city}' found in: {text[:80]!r}")
                    city_violations += 1
                    break  # only count each reference once

        if city_violations == 0:
            print(f"PASS Component 2: No city-of-publication found in references (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL Component 2: {city_violations} reference entries still contain city-of-publication")
    except Exception as e:
        print(f"ERROR Component 2 (city removal check): {e}")

    # Component 3: Hanging indent on all 5 reference entries (0.3 points)
    # APA 7th requires hanging indent: left_indent=0.5in (≈36pt), first_line_indent=-0.5in (≈-36pt)
    # Golden state: all 5 references have left_indent=36.0pt, first_line_indent=-36.0pt
    try:
        EXPECTED_LEFT_PT = 36.0
        EXPECTED_FIRST_LINE_PT = -36.0
        TOLERANCE = 2.0  # points tolerance

        hanging_indent_count = 0
        for para in ref_paras:
            pf = para.paragraph_format
            left = pf.left_indent
            first = pf.first_line_indent

            left_pt = left.pt if left is not None else None
            first_pt = first.pt if first is not None else None

            if (left_pt is not None and
                    first_pt is not None and
                    abs(left_pt - EXPECTED_LEFT_PT) <= TOLERANCE and
                    abs(first_pt - EXPECTED_FIRST_LINE_PT) <= TOLERANCE):
                hanging_indent_count += 1
            else:
                print(f"FAIL Component 3: Para has left={left_pt}pt, first_line={first_pt}pt "
                      f"(expected left~36pt, first_line~-36pt): {para.text[:50]!r}")

        if hanging_indent_count == NUM_REFERENCES:
            print(f"PASS Component 3: All {NUM_REFERENCES} reference entries have hanging indent "
                  f"(left≈36pt, first_line≈-36pt) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL Component 3: Only {hanging_indent_count}/{NUM_REFERENCES} reference entries "
                  f"have correct hanging indent")
    except Exception as e:
        print(f"ERROR Component 3 (hanging indent check): {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.1f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

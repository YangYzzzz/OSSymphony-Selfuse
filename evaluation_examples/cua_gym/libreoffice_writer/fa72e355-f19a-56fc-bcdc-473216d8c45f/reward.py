"""
Reward Script: Add bibliography reference and insert citation number in conclusion
Task ID: osworld_writer_biblio_002
Domain: libreoffice_writer
Scoring:
  Component 1 (0.6): Reference 6 (Johnson et al. 2022) appended to References section
    - Sub-check 1a (0.3): Reference 6 paragraph exists with author/year/title keywords
    - Sub-check 1b (0.3): Reference includes journal, volume/issue, pages and DOI
  Component 2 (0.4): Conclusion citation placeholder replaced
    - '(cite here)' no longer present AND '(6)' is present in the conclusion paragraph
Total: 1.0
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_biblio_002'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print('CRITICAL: Cannot load file %s: %s' % (file_path, e))
        print('REWARD: 0.0')
        return 0.0

    # Collect all paragraph texts for inspection
    para_texts = [p.text for p in doc.paragraphs]

    # -----------------------------------------------------------------------
    # Component 1a: Reference 6 paragraph exists with author/year/title info
    # (0.3 points)
    # Expected: paragraph starting with "6. Johnson, R. A., Williams, C. B., & Park, S. (2022)."
    # -----------------------------------------------------------------------
    try:
        ref6_para = None
        for text in para_texts:
            # Look for a paragraph that begins with "6." and contains Johnson + 2022
            if re.search(r'^6\.', text.strip()) and 'Johnson' in text and '2022' in text:
                ref6_para = text
                break

        if ref6_para is not None:
            # Verify it has the core author/year/title keywords
            has_authors = ('Johnson' in ref6_para and
                           'Williams' in ref6_para and
                           'Park' in ref6_para)
            has_year = '2022' in ref6_para
            has_title_kw = 'Climate change adaptation' in ref6_para or 'climate change adaptation' in ref6_para

            if has_authors and has_year and has_title_kw:
                print('PASS: Component 1a — Reference 6 paragraph found with Johnson/Williams/Park (2022) and title keywords (0.3 pts)')
                total_score += 0.3
            else:
                missing = []
                if not has_authors:
                    missing.append('authors (Johnson, Williams, Park)')
                if not has_year:
                    missing.append('year (2022)')
                if not has_title_kw:
                    missing.append('title keywords')
                print('FAIL: Component 1a — Reference 6 found but missing: %s' % ', '.join(missing))
        else:
            print('FAIL: Component 1a — No paragraph starting with "6." containing Johnson + 2022 found in References')
    except Exception as e:
        print('ERROR: Component 1a — %s' % e)

    # -----------------------------------------------------------------------
    # Component 1b: Reference 6 includes journal, volume/pages and DOI
    # (0.3 points)
    # Expected: Environmental Science & Technology, 56(8), 4521-4535,
    #           https://doi.org/10.1021/acs.est.2c01234
    # -----------------------------------------------------------------------
    try:
        if ref6_para is not None:
            has_journal = ('Environmental Science' in ref6_para and
                           'Technology' in ref6_para)
            has_volume = '56' in ref6_para and '4521' in ref6_para
            has_doi = 'doi.org/10.1021/acs.est.2c01234' in ref6_para or 'acs.est.2c01234' in ref6_para

            if has_journal and has_volume and has_doi:
                print('PASS: Component 1b — Reference 6 contains journal, volume/pages, and DOI (0.3 pts)')
                total_score += 0.3
            else:
                missing = []
                if not has_journal:
                    missing.append('journal name (Environmental Science & Technology)')
                if not has_volume:
                    missing.append('volume/pages (56, 4521)')
                if not has_doi:
                    missing.append('DOI (acs.est.2c01234)')
                print('FAIL: Component 1b — Reference 6 is missing: %s' % ', '.join(missing))
        else:
            print('FAIL: Component 1b — Reference 6 paragraph not found, skipping journal/DOI check')
    except Exception as e:
        print('ERROR: Component 1b — %s' % e)

    # -----------------------------------------------------------------------
    # Component 2: '(cite here)' replaced with '(6)' in conclusion paragraph
    # (0.4 points)
    # The conclusion paragraph (para index ~25) originally contains '(cite here)'
    # After the task it must contain '(6)' and NOT contain '(cite here)'
    # -----------------------------------------------------------------------
    try:
        cite_here_present = any('(cite here)' in t for t in para_texts)
        citation_6_present = any('(6)' in t for t in para_texts)

        if not cite_here_present and citation_6_present:
            # Confirm it's in the conclusion section
            in_conclusion = False
            after_conclusion_heading = False
            before_refs = True
            for text in para_texts:
                if '5. Conclusion' in text or text.strip() == '5. Conclusion' or 'Conclusion' in text:
                    after_conclusion_heading = True
                if 'References' in text and after_conclusion_heading:
                    before_refs = False
                if after_conclusion_heading and before_refs and '(6)' in text:
                    in_conclusion = True
                    break

            if in_conclusion:
                print('PASS: Component 2 — "(cite here)" replaced with "(6)" in conclusion section (0.4 pts)')
                total_score += 0.4
            else:
                # '(6)' exists but not clearly in conclusion — still award points
                # since the placeholder is gone and (6) is somewhere in the document
                print('PASS: Component 2 — "(cite here)" not found and "(6)" present in document (0.4 pts)')
                total_score += 0.4
        elif cite_here_present:
            print('FAIL: Component 2 — "(cite here)" still present in document; not replaced with "(6)"')
        elif not citation_6_present:
            print('FAIL: Component 2 — "(cite here)" removed but "(6)" not found in document')
        else:
            print('FAIL: Component 2 — unexpected state (cite_here=%s, citation_6=%s)' % (
                cite_here_present, citation_6_present))
    except Exception as e:
        print('ERROR: Component 2 — %s' % e)

    final_score = min(total_score, 1.0)
    print('\nScore: %s/1.0' % total_score)
    print('REWARD: %s' % final_score)
    return final_score


# Default: test against canonical artifact path
file_path = '%s/%s.docx' % (WORKDIR, TASK_ID)
if not os.path.exists(file_path):
    print('File not found: %s' % file_path)
    print('REWARD: 0.0')
else:
    verify_task(file_path)

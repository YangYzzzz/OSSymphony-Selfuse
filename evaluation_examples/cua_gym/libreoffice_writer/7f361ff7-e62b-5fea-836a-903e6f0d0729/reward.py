"""
Reward Script: Annotated Bibliography with APA Citations, DOI Hyperlinks, Annotations, and Statistics
Task ID: osworld_multi_apps_doi_resolve_writer_014
Domain: libreoffice_writer
Scoring:
  Component 1: APA citations added for all 10 papers (0.40 pts)
  Component 2: DOI/URL hyperlinks present for citations (0.30 pts)
  Component 3: Annotation paragraphs (3-sentence descriptions) for each paper (0.20 pts)
  Component 4: Bibliography Statistics section filled in (not placeholder text) (0.10 pts)
  Total: 1.0
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_doi_resolve_writer_014'

PAPER_TITLES = [
    "Attention Is All You Need",
    "BERT",
    "GPT-2",
    "GPT-3",
    "T5",
    "RoBERTa",
    "ELECTRA",
    "BART",
    "LLaMA",
    "Mistral 7B",
]

# Author surname markers unique to each paper's APA citation
# These do NOT appear in the title-only initial state
EXPECTED_APA_MARKERS = [
    "Vaswani",   # Attention Is All You Need
    "Devlin",    # BERT
    "Radford",   # GPT-2
    "Brown",     # GPT-3
    "Raffel",    # T5
    "Liu",       # RoBERTa (Liu, Y., Ott...)
    "Clark",     # ELECTRA
    "Lewis",     # BART
    "Touvron",   # LLaMA
    "Jiang",     # Mistral 7B
]


def get_all_paragraphs_from_odt(file_path):
    """Extract all paragraph text strings from an ODT file."""
    try:
        from odf.opendocument import load
        from odf.text import P
        doc = load(file_path)
        paragraphs = doc.getElementsByType(P)
        result = []
        for para in paragraphs:
            text_parts = []
            for node in para.childNodes:
                if node.nodeType == node.TEXT_NODE:
                    text_parts.append(str(node.data))
                elif node.nodeType == node.ELEMENT_NODE:
                    for child in node.childNodes:
                        if child.nodeType == child.TEXT_NODE:
                            text_parts.append(str(child.data))
                        elif child.nodeType == child.ELEMENT_NODE:
                            for gchild in child.childNodes:
                                if gchild.nodeType == gchild.TEXT_NODE:
                                    text_parts.append(str(gchild.data))
            result.append(''.join(text_parts))
        return result
    except Exception as e:
        print(f"ERROR: get_all_paragraphs_from_odt: {e}")
        return None


def get_hyperlinks_from_odt(file_path):
    """Extract all hyperlink hrefs from an ODT file."""
    try:
        from odf.opendocument import load
        from odf.text import A
        doc = load(file_path)
        links = doc.getElementsByType(A)
        hrefs = []
        for link in links:
            href = link.getAttribute('href')
            if href:
                hrefs.append(href)
        return hrefs
    except Exception as e:
        print(f"ERROR: get_hyperlinks_from_odt: {e}")
        return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load ODT paragraphs
    paragraphs = get_all_paragraphs_from_odt(file_path)
    if paragraphs is None:
        print(f"CRITICAL: Cannot load ODT file {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Combine all paragraphs into a single searchable text
    full_text = '\n'.join(paragraphs)

    # -----------------------------------------------------------------------
    # Component 1: APA citations present for all 10 papers (0.40 pts)
    # The initial file only has titles. The golden file has full APA citations
    # with author surnames, years, and publication details.
    # We check for author surname markers that only appear in full APA citations.
    # Partial credit: proportional to citations_found / 10
    # -----------------------------------------------------------------------
    try:
        citations_found = 0
        for marker in EXPECTED_APA_MARKERS:
            # APA citations format: "Surname, Initials. (year)..."
            if (marker + ",") in full_text or (marker + " et al") in full_text:
                citations_found += 1

        if citations_found == len(EXPECTED_APA_MARKERS):
            print(f"PASS: Component 1 — All {citations_found} APA citations found (0.40 pts)")
            total_score += 0.40
        elif citations_found > 0:
            partial = 0.40 * (citations_found / len(EXPECTED_APA_MARKERS))
            print(f"PARTIAL: Component 1 — {citations_found}/{len(EXPECTED_APA_MARKERS)} APA citations found ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No APA citations found (0.00 pts)")

    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: DOI/URL hyperlinks for each citation (0.30 pts)
    # The initial file has 0 hyperlinks. The golden file has 10 hyperlinks
    # (one per paper citation).
    # Partial credit: proportional to doi_links_found / 10
    # -----------------------------------------------------------------------
    try:
        hrefs = get_hyperlinks_from_odt(file_path)
        if hrefs is None:
            print("FAIL: Component 2 — Could not read hyperlinks (0.00 pts)")
        else:
            # Count hyperlinks that are research DOI or URL links
            doi_links = [h for h in hrefs if (
                'doi.org' in h or
                'arxiv.org' in h or
                'openai.com' in h or
                'semanticscholar.org' in h or
                h.startswith('http')
            )]
            if len(doi_links) >= 10:
                print(f"PASS: Component 2 — {len(doi_links)} DOI/URL hyperlinks found (0.30 pts)")
                total_score += 0.30
            elif len(doi_links) > 0:
                partial = 0.30 * (len(doi_links) / 10.0)
                print(f"PARTIAL: Component 2 — {len(doi_links)}/10 DOI/URL hyperlinks found ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — No DOI/URL hyperlinks found (0.00 pts)")

    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: Annotation paragraphs for each paper (0.20 pts)
    # The initial file has no annotations. The golden file has 10 annotation
    # paragraphs, each multi-sentence covering contribution, methodology,
    # and limitation. We count substantive paragraphs (>100 chars) that are
    # not citations, headers, stats lines, or title lines.
    # Partial credit: proportional to annotation_count / 10
    # -----------------------------------------------------------------------
    try:
        annotation_count = 0
        headers = {
            'Annotated Bibliography',
            'Natural Language Processing',
            'References',
            'Bibliography Statistics'
        }

        for para_text in paragraphs:
            text = para_text.strip()
            # Must be substantive length for a real annotation
            if len(text) < 100:
                continue
            # Skip citation paragraphs (have a URL/DOI with author marker)
            if ('http' in text) and any((m + ',') in text for m in EXPECTED_APA_MARKERS):
                continue
            # Skip header lines
            if any(text.startswith(h) for h in headers):
                continue
            # Skip statistics list items
            if text.startswith('- '):
                continue
            # Skip numbered title-only lines from initial state
            matched_title = any(
                text == title or text == (str(i + 1) + '. ' + title)
                for i, title in enumerate(PAPER_TITLES)
            )
            if matched_title:
                continue
            # This qualifies as an annotation paragraph
            annotation_count += 1

        if annotation_count >= 10:
            print(f"PASS: Component 3 — {annotation_count} annotation paragraphs found (0.20 pts)")
            total_score += 0.20
        elif annotation_count > 0:
            partial = 0.20 * (annotation_count / 10.0)
            print(f"PARTIAL: Component 3 — {annotation_count}/10 annotation paragraphs found ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No annotation paragraphs found (0.00 pts)")

    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -----------------------------------------------------------------------
    # Component 4: Bibliography Statistics section filled in (0.10 pts)
    # The initial file has placeholder text like "[To be filled...]".
    # The golden file has actual values: total count, year range, venue, ratio.
    # We check that placeholders are GONE and real values are present.
    # -----------------------------------------------------------------------
    try:
        placeholder_indicators = [
            '[To be filled',
            '[number]',
            '[year]',
            '[venue name]',
            '[ratio]',
        ]
        has_placeholder = any(p in full_text for p in placeholder_indicators)

        if has_placeholder:
            print(f"FAIL: Component 4 — Placeholder text still present in statistics section (0.00 pts)")
        else:
            # Verify statistics section has actual content
            has_total = bool(re.search(r'Total references:\s*\d+', full_text))
            has_year_range = bool(re.search(r'Date range.*\d{4}', full_text))
            has_venue = bool(re.search(r'Most common venue:\s*\S', full_text))
            has_ratio = bool(re.search(r'(ratio|academic|industry)', full_text, re.IGNORECASE))

            stats_components_met = sum([has_total, has_year_range, has_venue, has_ratio])

            stats_detail = f"total={has_total}, year_range={has_year_range}, venue={has_venue}, ratio={has_ratio}"
            if stats_components_met >= 3:
                print(f"PASS: Component 4 — Bibliography Statistics filled in ({stats_detail}) (0.10 pts)")
                total_score += 0.10
            elif stats_components_met >= 1:
                partial = 0.10 * (stats_components_met / 4.0)
                print(f"PARTIAL: Component 4 — Statistics partially filled ({stats_components_met}/4 items) ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 — Statistics section missing expected content (0.00 pts)")

    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


# Entry point: test against canonical artifact path
file_path = f'{WORKDIR}/annotated_bibliography.odt'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

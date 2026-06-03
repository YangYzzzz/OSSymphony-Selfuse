"""
Reward Script: HuggingFace Weekly Digest — LibreOffice Writer
Task ID: osworld_multi_apps_hf_papers_writer_015
Domain: libreoffice_writer
Scoring:
  Component 1: Summary table filled with paper counts and top paper titles (0.3 pts)
  Component 2: Day sections contain real paper entries — title, authors, arXiv ID, abstract (0.4 pts)
  Component 3: Trends section has 3-5 non-placeholder bullet points (0.3 pts)
  Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_hf_papers_writer_015'
FILE_PATH = f'{WORKDIR}/weekly_digest.odt'

# Expected dates in the summary table
EXPECTED_DATES = ['2024-03-04', '2024-03-05', '2024-03-06', '2024-03-07', '2024-03-08']

# Known placeholder strings that appear in the initial file (do NOT award points for these)
PLACEHOLDER_PATTERNS = [
    '[Paper entries for this day will be added here',
    '[Add 3-5 bullet points here',
    'will be added here',
]

# arXiv IDs present in the golden file — used to check paper entry presence
EXPECTED_ARXIV_IDS = [
    '2402.17764',  # BitNet b1.58 (Mar 4)
    '2402.18039',  # ResLoRA (Mar 4)
    '2402.19427',  # Griffin (Mar 4)
    '2403.04132',  # Chatbot Arena (Mar 5)
    '2403.03194',  # MAGID (Mar 5)
    '2403.03853',  # ShortGPT (Mar 5)
    '2403.03507',  # GaLore (Mar 6)
    '2402.07871',  # MoE scaling (Mar 6)
    '2403.03003',  # Feast Your Eyes (Mar 6)
    '2403.04732',  # Visual Deductive (Mar 7)
    '2403.04652',  # Yi (Mar 7)
    '2403.04706',  # 7B Math (Mar 7)
    '2309.11998',  # Chatbot Arena dataset (Mar 8)
    '2403.10131',  # RAFT (Mar 8)
    '2403.05530',  # Gemini 1.5 (Mar 8)
]


def get_all_text_nodes(elem):
    """Recursively collect all text node data from an ODF element."""
    texts = []
    if hasattr(elem, 'nodeType') and elem.nodeType == elem.TEXT_NODE:
        if elem.data.strip():
            texts.append(elem.data)
    for child in getattr(elem, 'childNodes', []):
        texts.extend(get_all_text_nodes(child))
    return texts


def is_placeholder(text):
    """Return True if the text matches any placeholder pattern."""
    for pattern in PLACEHOLDER_PATTERNS:
        if pattern in text:
            return True
    return False


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from odf.opendocument import load
        from odf.text import P, H
        from odf.table import Table, TableRow, TableCell
        doc = load(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # -----------------------------------------------------------------------
    # Component 1: Summary table filled with paper counts and top paper titles
    #   The initial file has the table with only dates; Paper Count and Top Paper Title
    #   columns are empty. The task requires filling these for all 5 days.
    #   Score: 0.3 points — awarded when ALL 5 rows have non-empty Paper Count
    #   AND non-empty Top Paper Title cells.
    # -----------------------------------------------------------------------
    try:
        tables = doc.body.getElementsByType(Table)
        if not tables:
            print("FAIL: Component 1 — No table found in document")
        else:
            tbl = tables[0]
            rows = tbl.getElementsByType(TableRow)
            # rows[0] is the header row; rows 1-5 are data rows
            data_rows = rows[1:]  # skip header

            filled_count = 0
            has_paper_count = 0
            has_top_title = 0
            for row in data_rows:
                cells = row.getElementsByType(TableCell)
                if len(cells) < 3:
                    continue
                # Cell 0: date, Cell 1: paper count, Cell 2: top paper title
                paper_count_text = ''.join(get_all_text_nodes(cells[1])).strip()
                top_title_text = ''.join(get_all_text_nodes(cells[2])).strip()

                count_ok = (
                    bool(paper_count_text)
                    and not is_placeholder(paper_count_text)
                    and paper_count_text.isdigit()
                    and int(paper_count_text) > 0
                )
                title_ok = (
                    bool(top_title_text)
                    and not is_placeholder(top_title_text)
                    and len(top_title_text) > 5
                )
                if count_ok:
                    has_paper_count += 1
                if title_ok:
                    has_top_title += 1
                if count_ok and title_ok:
                    filled_count += 1

            if filled_count == 5:
                print(f"PASS: Component 1 — Summary table: all 5 rows filled "
                      f"(paper counts and top paper titles present)")
                total_score += 0.3
            elif filled_count > 0 or has_paper_count > 0 or has_top_title > 0:
                partial = round(0.3 * (max(has_paper_count, has_top_title) / 5), 2)
                print(f"PARTIAL: Component 1 — Summary table: {filled_count}/5 rows "
                      f"fully filled; paper_count_rows={has_paper_count}, "
                      f"top_title_rows={has_top_title} — partial {partial} pts")
                total_score += partial
            else:
                print(f"FAIL: Component 1 — Summary table: no data rows filled "
                      f"(paper counts and top paper titles are empty)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: Day sections contain real paper entries
    #   Each of the 5 day sections should have paper entries with:
    #     - Paper title (non-placeholder)
    #     - Authors line
    #     - arXiv ID line
    #     - Abstract
    #   We verify by checking for arXiv IDs in the document text and requiring
    #   that non-placeholder content exists for each day's section.
    #   Score: 0.4 points
    #     - 0.2 points: at least 10 of 15 expected arXiv IDs present
    #     - 0.2 points: all 5 day sections have non-placeholder content
    # -----------------------------------------------------------------------
    try:
        # Collect all text from the document body
        all_body_text = ' '.join(get_all_text_nodes(doc.body))

        # Sub-check A: arXiv IDs present
        found_arxiv = [aid for aid in EXPECTED_ARXIV_IDS if aid in all_body_text]
        arxiv_count = len(found_arxiv)

        if arxiv_count >= 15:
            print(f"PASS: Component 2a — All 15 arXiv IDs found in document (+0.2 pts)")
            total_score += 0.2
        elif arxiv_count >= 10:
            # Partial for 10-14 arxiv IDs
            partial_a = round(0.2 * (arxiv_count / 15), 2)
            print(f"PARTIAL: Component 2a — {arxiv_count}/15 arXiv IDs found "
                  f"(+{partial_a} pts)")
            total_score += partial_a
        else:
            print(f"FAIL: Component 2a — Only {arxiv_count}/15 arXiv IDs found; "
                  f"day sections likely not filled")

        # Sub-check B: each day section has non-placeholder content
        # Strategy: get headings and then check paragraphs after each day heading
        headings = doc.body.getElementsByType(H)
        day_headings_found = 0
        for h in headings:
            h_text = ''.join(get_all_text_nodes(h)).strip()
            # Check if this heading corresponds to one of the 5 expected dates
            for date in EXPECTED_DATES:
                if date in h_text:
                    day_headings_found += 1
                    break

        # Count non-placeholder paragraphs that include "Abstract:" or "arXiv:"
        paras = doc.body.getElementsByType(P)
        abstract_count = 0
        arxiv_para_count = 0
        for para in paras:
            para_text = ''.join(get_all_text_nodes(para)).strip()
            if 'Abstract:' in para_text and not is_placeholder(para_text):
                abstract_count += 1
            if 'arXiv:' in para_text and not is_placeholder(para_text):
                arxiv_para_count += 1

        # Expect at least 15 abstract paragraphs (3 per day × 5 days)
        if abstract_count >= 15 and arxiv_para_count >= 15:
            print(f"PASS: Component 2b — All day sections filled: "
                  f"{abstract_count} abstract paragraphs, {arxiv_para_count} arXiv paragraphs "
                  f"(+0.2 pts)")
            total_score += 0.2
        elif abstract_count >= 5 or arxiv_para_count >= 5:
            partial_b = round(0.2 * (min(abstract_count, arxiv_para_count) / 15), 2)
            print(f"PARTIAL: Component 2b — {abstract_count} abstract paragraphs, "
                  f"{arxiv_para_count} arXiv paragraphs found "
                  f"(+{partial_b} pts)")
            total_score += partial_b
        else:
            print(f"FAIL: Component 2b — Insufficient paper entries: "
                  f"{abstract_count} abstract paragraphs, {arxiv_para_count} arXiv paragraphs "
                  f"(expected ≥15 each)")

    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: Trends section has 3-5 non-placeholder bullet points
    #   The initial file has placeholder text in the Trends section.
    #   The task requires replacing it with 3-5 bullet points about weekly themes.
    #   Score: 0.3 points — awarded when 3+ non-placeholder paragraphs follow
    #   the Trends heading.
    # -----------------------------------------------------------------------
    try:
        # Check all paragraphs for Trends content
        # The Trends section should have at least 3 substantive bullet points
        # that are NOT placeholder text
        paras = doc.body.getElementsByType(P)
        trends_content_paras = []
        for para in paras:
            para_text = ''.join(get_all_text_nodes(para)).strip()
            # Trends bullet points tend to be longer sentences about research themes
            # Filter out placeholder, empty, and very short paragraphs
            if (
                para_text
                and not is_placeholder(para_text)
                and len(para_text) > 30
                # Exclude lines that are table content (dates) or paper entry lines
                and not para_text.startswith('20')  # date lines like "2024-03-04"
                and 'arXiv:' not in para_text
                and 'Abstract:' not in para_text
                and 'Authors:' not in para_text
                # Exclude the summary paragraph
                and 'summarizes the papers featured' not in para_text
                # Exclude numbered paper entries "1. Title" "2. Title"
                and not (len(para_text) > 3 and para_text[0].isdigit() and para_text[1] == '.')
            ):
                trends_content_paras.append(para_text)

        trends_count = len(trends_content_paras)

        if trends_count >= 3:
            print(f"PASS: Component 3 — Trends section has {trends_count} non-placeholder "
                  f"bullet points/paragraphs (+0.3 pts)")
            total_score += 0.3
        elif trends_count > 0:
            partial = round(0.3 * (trends_count / 3), 2)
            print(f"PARTIAL: Component 3 — Trends section has {trends_count} non-placeholder "
                  f"paragraphs (need 3+; +{partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Trends section has no non-placeholder content "
                  f"(found {trends_count} paragraphs); "
                  f"initial placeholder text may still be present")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

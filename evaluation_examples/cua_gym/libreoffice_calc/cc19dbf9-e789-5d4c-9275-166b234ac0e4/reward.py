"""
Reward Script: Foundation Models Research Database & Reference List
Task ID: osworld_multi_apps_web_papers_015
Domain: multi_apps (libreoffice_calc + libreoffice_writer)

Task: Collect foundation model papers from ArXiv/PapersWithCode/ICML 2024,
build a LibreOffice Calc database (foundation_models_db.ods) and
a LibreOffice Writer reference list (foundation_models_refs.odt).

Scoring Rubric:
  Component 1 (0.25): foundation_models_db.ods exists with all 8 required columns
  Component 2 (0.25): foundation_models_db.ods has >=20 papers, sorted by Citation_Count
                       descending, Sub_topic values valid
  Component 3 (0.25): foundation_models_refs.odt exists with H1 heading
                       'Foundation Models — Reference List'
  Component 4 (0.25): foundation_models_refs.odt has >=20 APA-style reference paragraphs
                       sorted by author last name
  Total: 1.0
"""

import os

WORKDIR = '/home/user/Documents'
TASK_ID = 'osworld_multi_apps_web_papers_015'

ODS_PATH = os.path.join(WORKDIR, 'foundation_models_db.ods')
ODT_PATH = os.path.join(WORKDIR, 'foundation_models_refs.odt')

REQUIRED_COLUMNS = {'Title', 'Authors', 'Year', 'Venue', 'Sub_topic', 'Citation_Count', 'Abstract', 'Source_URL'}
VALID_SUBTOPICS = {'Vision', 'Language', 'Multimodal', 'Code', 'Science'}
HEADING_TEXT = 'Foundation Models — Reference List'
MIN_PAPERS = 20


def get_cell_text(cell):
    """Extract text from an ODF table cell."""
    try:
        from odf.text import P
        ps = cell.getElementsByType(P)
        if ps:
            return str(ps[0]).strip()
        return ''
    except Exception:
        return ''


def get_element_text(elem):
    """Recursively extract all text from an ODF element."""
    if hasattr(elem, 'data'):
        return elem.data
    result = ''
    for child in elem.childNodes:
        result += get_element_text(child)
    return result


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # -------------------------------------------------------------------------
    # Component 1: foundation_models_db.ods exists with all 8 required columns
    # (0.25 points)
    # -------------------------------------------------------------------------
    try:
        if not os.path.exists(ODS_PATH):
            print(f"FAIL: Component 1 — {ODS_PATH} does not exist")
        else:
            from odf.opendocument import load as odf_load
            from odf.table import Table, TableRow, TableCell

            ods_doc = odf_load(ODS_PATH)
            sheets = ods_doc.spreadsheet.getElementsByType(Table)

            if not sheets:
                print("FAIL: Component 1 — No sheets found in ODS file")
            else:
                sheet = sheets[0]
                rows = sheet.getElementsByType(TableRow)
                if not rows:
                    print("FAIL: Component 1 — No rows in sheet")
                else:
                    header_row = rows[0]
                    header_cells = header_row.getElementsByType(TableCell)
                    found_headers = set()
                    for cell in header_cells:
                        val = get_cell_text(cell)
                        if val:
                            found_headers.add(val)

                    missing_cols = REQUIRED_COLUMNS - found_headers
                    if missing_cols:
                        print(f"FAIL: Component 1 — Missing columns: {sorted(missing_cols)}")
                        print(f"  Found columns: {sorted(found_headers)}")
                    else:
                        print(f"PASS: Component 1 — All 8 required columns found: {sorted(found_headers & REQUIRED_COLUMNS)} (0.25 pts)")
                        total_score += 0.25
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------------
    # Component 2: foundation_models_db.ods has >=20 papers, Citation_Count
    # sorted descending, all Sub_topic values are valid
    # (0.25 points)
    # -------------------------------------------------------------------------
    try:
        if not os.path.exists(ODS_PATH):
            print(f"FAIL: Component 2 — {ODS_PATH} does not exist")
        else:
            from odf.opendocument import load as odf_load
            from odf.table import Table, TableRow, TableCell

            ods_doc = odf_load(ODS_PATH)
            sheets = ods_doc.spreadsheet.getElementsByType(Table)
            sheet = sheets[0]
            rows = sheet.getElementsByType(TableRow)

            if len(rows) < 2:
                print("FAIL: Component 2 — Fewer than 2 rows (no data rows found)")
            else:
                # Find column indices from header
                header_cells = rows[0].getElementsByType(TableCell)
                col_index = {}
                for i, cell in enumerate(header_cells):
                    val = get_cell_text(cell)
                    if val:
                        col_index[val] = i

                subtopic_col = col_index.get('Sub_topic', -1)
                citation_col = col_index.get('Citation_Count', -1)
                title_col = col_index.get('Title', -1)

                # Collect data rows
                data_papers = []
                invalid_subtopics = []
                citation_values = []

                for row in rows[1:]:
                    cells = row.getElementsByType(TableCell)
                    if not cells:
                        continue
                    title_val = get_cell_text(cells[title_col]) if title_col >= 0 and len(cells) > title_col else ''
                    if not title_val:
                        continue  # skip empty rows

                    data_papers.append(title_val)

                    # Check subtopic
                    if subtopic_col >= 0 and len(cells) > subtopic_col:
                        subtopic_val = get_cell_text(cells[subtopic_col])
                        if subtopic_val and subtopic_val not in VALID_SUBTOPICS:
                            invalid_subtopics.append(subtopic_val)

                    # Collect citation count
                    if citation_col >= 0 and len(cells) > citation_col:
                        cit_val = get_cell_text(cells[citation_col])
                        try:
                            citation_values.append(int(cit_val))
                        except ValueError:
                            citation_values.append(None)

                paper_count = len(data_papers)
                enough_papers = paper_count >= MIN_PAPERS

                # Check citation sort order (descending, skip None values)
                numeric_citations = [v for v in citation_values if v is not None]
                sorted_descending = all(
                    numeric_citations[i] >= numeric_citations[i + 1]
                    for i in range(len(numeric_citations) - 1)
                ) if len(numeric_citations) > 1 else True

                valid_subtopics_ok = len(invalid_subtopics) == 0

                issues = []
                if not enough_papers:
                    issues.append(f"only {paper_count} papers (need >= {MIN_PAPERS})")
                if not sorted_descending:
                    issues.append("Citation_Count not sorted descending")
                if not valid_subtopics_ok:
                    issues.append(f"invalid Sub_topic values: {set(invalid_subtopics)}")

                if issues:
                    print(f"FAIL: Component 2 — {'; '.join(issues)}")
                    print(f"  Paper count: {paper_count}, Sorted: {sorted_descending}, Valid subtopics: {valid_subtopics_ok}")
                else:
                    print(f"PASS: Component 2 — {paper_count} papers, sorted by citation descending, valid subtopics (0.25 pts)")
                    total_score += 0.25

    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Component 3: foundation_models_refs.odt exists with H1 heading
    # 'Foundation Models — Reference List'
    # (0.25 points)
    # -------------------------------------------------------------------------
    try:
        if not os.path.exists(ODT_PATH):
            print(f"FAIL: Component 3 — {ODT_PATH} does not exist")
        else:
            from odf.opendocument import load as odf_load
            from odf.text import H

            odt_doc = odf_load(ODT_PATH)
            body = odt_doc.text
            children = body.childNodes

            # Find any H (heading) element containing the expected text
            heading_found = False
            found_heading_text = None
            for child in children:
                qname = child.qname[1] if hasattr(child, 'qname') else ''
                if qname == 'h':
                    text = get_element_text(child).strip()
                    if HEADING_TEXT in text:
                        heading_found = True
                        found_heading_text = text
                        break
                    elif found_heading_text is None:
                        found_heading_text = text  # capture first heading for debug

            if heading_found:
                print(f"PASS: Component 3 — H1 heading found: {found_heading_text!r} (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — Expected heading {HEADING_TEXT!r} not found")
                if found_heading_text:
                    print(f"  First heading found: {found_heading_text!r}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -------------------------------------------------------------------------
    # Component 4: foundation_models_refs.odt has >=20 APA-style reference
    # paragraphs sorted by author last name (first letter ascending)
    # (0.25 points)
    # -------------------------------------------------------------------------
    try:
        if not os.path.exists(ODT_PATH):
            print(f"FAIL: Component 4 — {ODT_PATH} does not exist")
        else:
            from odf.opendocument import load as odf_load

            odt_doc = odf_load(ODT_PATH)
            body = odt_doc.text
            children = body.childNodes

            # Collect paragraphs (type='p') that look like APA references.
            # APA pattern: "Author(s), A. (YEAR). Title. Venue."
            # We detect APA by checking for "(YEAR)" pattern.
            import re
            apa_year_pattern = re.compile(r'\(\d{4}\)')

            ref_paragraphs = []
            for child in children:
                qname = child.qname[1] if hasattr(child, 'qname') else ''
                if qname == 'p':
                    text = get_element_text(child).strip()
                    if text and apa_year_pattern.search(text):
                        ref_paragraphs.append(text)

            para_count = len(ref_paragraphs)
            enough_refs = para_count >= MIN_PAPERS

            # Check author-last-name sort: extract first word of each paragraph
            # (which should be the first author's last name in APA style)
            first_words = []
            for para in ref_paragraphs:
                first_word = para.split(',')[0].split()[0] if para else ''
                first_words.append(first_word.lower())

            sorted_alpha = all(
                first_words[i] <= first_words[i + 1]
                for i in range(len(first_words) - 1)
            ) if len(first_words) > 1 else True

            issues = []
            if not enough_refs:
                issues.append(f"only {para_count} APA-style paragraphs (need >= {MIN_PAPERS})")
            if not sorted_alpha:
                # Find first violation
                for i in range(len(first_words) - 1):
                    if first_words[i] > first_words[i + 1]:
                        issues.append(f"sort order violated: {first_words[i]!r} > {first_words[i+1]!r}")
                        break

            if issues:
                print(f"FAIL: Component 4 — {'; '.join(issues)}")
                print(f"  APA paragraph count: {para_count}, Sorted: {sorted_alpha}")
                if first_words[:5]:
                    print(f"  First author words: {first_words[:5]}")
            else:
                print(f"PASS: Component 4 — {para_count} APA-style refs, sorted by author last name (0.25 pts)")
                total_score += 0.25

    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()

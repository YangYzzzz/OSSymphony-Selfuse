"""
Reward Script: Build complete reference manager - fill papers_incomplete.ods,
               create references_apa.odt, create references.bib
Task ID: osworld_multi_apps_web_references_011
Domain: libreoffice_calc (multi-app: calc + writer + file)
Scoring:
  Component 1: ODS DOI column filled for all 12 papers (0.30 pts)
  Component 2: ODS Citation_Count + Venue columns filled for all 12 papers (0.20 pts)
  Component 3: ODT file in Documents with 'References' H1 heading + 12 APA entries (0.30 pts)
  Component 4: BibTeX file in Documents with 12 valid entries (0.20 pts)
  Total: 1.0
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_references_011'

ODS_PATH = '/home/user/Desktop/papers_incomplete.ods'
ODT_PATH = '/home/user/Documents/references_apa.odt'
BIB_PATH = '/home/user/Documents/references.bib'

EXPECTED_PAPER_COUNT = 12


def get_ods_cell_text(cell):
    """Extract text from ODF cell element."""
    try:
        from odf.text import P
        ps = cell.getElementsByType(P)
        if ps:
            parts = []
            for p in ps:
                for child in p.childNodes:
                    if child.nodeType == child.TEXT_NODE:
                        parts.append(child.data)
                    elif hasattr(child, 'childNodes'):
                        for sub in child.childNodes:
                            if sub.nodeType == sub.TEXT_NODE:
                                parts.append(sub.data)
            return " ".join(parts).strip()
        return ""
    except Exception:
        return ""


def verify_task():
    """Verify task completion with progressive scoring."""
    total_score = 0.0

    # ---------------------------------------------------------------
    # Precondition gate: ODS file must exist
    # ---------------------------------------------------------------
    if not os.path.exists(ODS_PATH):
        print(f"CRITICAL: ODS file not found: {ODS_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # ---------------------------------------------------------------
    # Component 1: DOI column filled for all 12 data rows (0.30 pts)
    # Task requires finding DOI via CrossRef for each paper.
    # Initial state: all DOI cells are empty.
    # Golden state: all DOI cells contain a DOI or 'N/A'.
    # ---------------------------------------------------------------
    try:
        from odf.opendocument import load
        from odf.table import Table, TableRow, TableCell

        doc = load(ODS_PATH)
        tables = doc.getElementsByType(Table)
        if not tables:
            print("FAIL: Component 1 — No table found in ODS")
        else:
            table = tables[0]
            rows = table.getElementsByType(TableRow)
            # Find header row to get column indices
            header_row = rows[0]
            header_cells = header_row.getElementsByType(TableCell)
            header_names = [get_ods_cell_text(c) for c in header_cells]
            print(f"Headers found: {header_names}")

            doi_col = None
            oa_col = None
            cite_col = None
            venue_col = None
            for i, h in enumerate(header_names):
                if 'DOI' in h:
                    doi_col = i
                if 'OA_PDF' in h or 'OA PDF' in h:
                    oa_col = i
                if 'Citation' in h or 'citation' in h:
                    cite_col = i
                if 'Venue' in h or 'venue' in h:
                    venue_col = i

            print(f"Column indices: DOI={doi_col}, OA_PDF={oa_col}, Citation={cite_col}, Venue={venue_col}")

            data_rows = list(rows[1:])
            # Only count rows that have a title (non-empty first cell)
            valid_data_rows = []
            for row in data_rows:
                cells = row.getElementsByType(TableCell)
                if cells:
                    title = get_ods_cell_text(cells[0])
                    if title.strip():
                        valid_data_rows.append(row)

            print(f"Valid data rows (with title): {len(valid_data_rows)}")

            # Component 1: DOI column filled (0.30 pts)
            doi_filled = 0
            if doi_col is not None:
                for row in valid_data_rows:
                    cells = row.getElementsByType(TableCell)
                    if doi_col < len(cells):
                        val = get_ods_cell_text(cells[doi_col])
                        if val.strip():  # non-empty
                            doi_filled += 1

                if doi_filled >= EXPECTED_PAPER_COUNT:
                    print(f"PASS: Component 1 — DOI column filled for all {doi_filled} papers (0.30 pts)")
                    total_score += 0.30
                elif doi_filled > 0:
                    partial = round(0.30 * doi_filled / EXPECTED_PAPER_COUNT, 4)
                    print(f"PARTIAL: Component 1 — DOI filled for {doi_filled}/{EXPECTED_PAPER_COUNT} papers ({partial} pts)")
                    total_score += partial
                else:
                    print(f"FAIL: Component 1 — DOI column empty for all rows (expected {EXPECTED_PAPER_COUNT} filled)")
            else:
                print("FAIL: Component 1 — DOI column not found in headers")

            # Component 2: Citation_Count + Venue columns filled (0.20 pts)
            cite_filled = 0
            venue_filled = 0
            if cite_col is not None:
                for row in valid_data_rows:
                    cells = row.getElementsByType(TableCell)
                    if cite_col < len(cells):
                        val = get_ods_cell_text(cells[cite_col])
                        if val.strip():
                            cite_filled += 1
            if venue_col is not None:
                for row in valid_data_rows:
                    cells = row.getElementsByType(TableCell)
                    if venue_col < len(cells):
                        val = get_ods_cell_text(cells[venue_col])
                        if val.strip():
                            venue_filled += 1

            both_filled = min(cite_filled, venue_filled)
            if both_filled >= EXPECTED_PAPER_COUNT:
                print(f"PASS: Component 2 — Citation_Count+Venue filled for all {EXPECTED_PAPER_COUNT} papers (0.20 pts)")
                total_score += 0.20
            elif both_filled > 0:
                partial = round(0.20 * both_filled / EXPECTED_PAPER_COUNT, 4)
                print(f"PARTIAL: Component 2 — Both fields filled for {both_filled}/{EXPECTED_PAPER_COUNT} papers ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — Citation_Count ({cite_filled}) or Venue ({venue_filled}) columns empty")

    except Exception as e:
        print(f"ERROR: Components 1-2 — Could not read ODS: {e}")
        import traceback
        traceback.print_exc()

    # ---------------------------------------------------------------
    # Component 3: ODT file in Documents with 'References' heading
    #              and 12 APA-formatted numbered citations (0.30 pts)
    # Initial state: file does not exist.
    # Golden state: file exists with H1 'References' + 12 numbered paragraphs.
    # ---------------------------------------------------------------
    try:
        if not os.path.exists(ODT_PATH):
            print(f"FAIL: Component 3 — ODT file not found: {ODT_PATH}")
        else:
            from odf.opendocument import load as odf_load
            from odf.text import P, H

            odt_doc = odf_load(ODT_PATH)

            # Check for H1 heading 'References'
            headings = odt_doc.getElementsByType(H)
            heading_found = False
            for h in headings:
                text = ""
                for child in h.childNodes:
                    if child.nodeType == child.TEXT_NODE:
                        text += child.data
                    elif hasattr(child, 'childNodes'):
                        for sub in child.childNodes:
                            if sub.nodeType == sub.TEXT_NODE:
                                text += sub.data
                if 'References' in text:
                    heading_found = True
                    print(f"  Found heading: '{text}'")
                    break

            # Check for 12 numbered paragraphs (APA citations)
            paras = odt_doc.getElementsByType(P)
            numbered_paras = 0
            for p in paras:
                text = ""
                for child in p.childNodes:
                    if child.nodeType == child.TEXT_NODE:
                        text += child.data
                    elif hasattr(child, 'childNodes'):
                        for sub in child.childNodes:
                            if sub.nodeType == sub.TEXT_NODE:
                                text += sub.data
                text = text.strip()
                # Look for numbered format like "1. " or "12. "
                if re.match(r'^\d+\.', text) and len(text) > 10:
                    numbered_paras += 1

            print(f"  ODT: heading_found={heading_found}, numbered_paras={numbered_paras}")

            if heading_found and numbered_paras >= EXPECTED_PAPER_COUNT:
                print(f"PASS: Component 3 — ODT 'References' H1 heading + {numbered_paras} APA entries (0.30 pts)")
                total_score += 0.30
            elif heading_found and numbered_paras > 0:
                partial = round(0.30 * (0.5 + 0.5 * numbered_paras / EXPECTED_PAPER_COUNT), 4)
                print(f"PARTIAL: Component 3 — Heading found but only {numbered_paras}/{EXPECTED_PAPER_COUNT} numbered entries ({partial} pts)")
                total_score += partial
            elif not heading_found:
                print(f"FAIL: Component 3 — ODT file missing 'References' H1 heading")
                if numbered_paras >= EXPECTED_PAPER_COUNT:
                    # Has entries but no heading — give partial credit
                    print(f"  (Note: {numbered_paras} numbered entries found without heading)")
                    total_score += 0.10
            else:
                print(f"FAIL: Component 3 — ODT heading found but {numbered_paras} numbered APA entries (need {EXPECTED_PAPER_COUNT})")

    except Exception as e:
        print(f"ERROR: Component 3 — Could not verify ODT: {e}")
        import traceback
        traceback.print_exc()

    # ---------------------------------------------------------------
    # Component 4: BibTeX file in Documents with 12 valid entries (0.20 pts)
    # Initial state: file does not exist.
    # Golden state: file exists with 12 @article/@inproceedings entries.
    # ---------------------------------------------------------------
    try:
        if not os.path.exists(BIB_PATH):
            print(f"FAIL: Component 4 — BibTeX file not found: {BIB_PATH}")
        else:
            with open(BIB_PATH, 'r', encoding='utf-8', errors='replace') as f:
                bib_content = f.read()

            # Count valid BibTeX entries
            entry_matches = re.findall(r'@(article|inproceedings|misc|techreport|phdthesis|book)\s*\{', bib_content, re.IGNORECASE)
            entry_count = len(entry_matches)

            # Check for title and author fields in entries
            has_title = bool(re.search(r'\btitle\s*=', bib_content, re.IGNORECASE))
            has_author = bool(re.search(r'\bauthor\s*=', bib_content, re.IGNORECASE))

            print(f"  BibTeX: {entry_count} entries, types={set(e.lower() for e in entry_matches)}, has_title={has_title}, has_author={has_author}")

            if entry_count >= EXPECTED_PAPER_COUNT and has_title and has_author:
                print(f"PASS: Component 4 — BibTeX file with {entry_count} valid entries (0.20 pts)")
                total_score += 0.20
            elif entry_count > 0 and has_title:
                partial = round(0.20 * entry_count / EXPECTED_PAPER_COUNT, 4)
                print(f"PARTIAL: Component 4 — BibTeX has {entry_count}/{EXPECTED_PAPER_COUNT} entries ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 — BibTeX invalid or missing entries (found {entry_count})")

    except Exception as e:
        print(f"ERROR: Component 4 — Could not verify BibTeX: {e}")

    # Final score
    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

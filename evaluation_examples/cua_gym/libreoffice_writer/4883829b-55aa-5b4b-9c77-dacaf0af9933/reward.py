"""
Reward Script: Paper Comparison Table - HuggingFace Featured vs ArXiv cs.CL (2024-02-05)
Task ID: osworld_multi_apps_hf_papers_writer_014
Domain: libreoffice_writer
Scoring:
  Component 1: HuggingFace column filled with papers (0.3 pts)
  Component 2: ArXiv cs.CL column filled with papers (0.3 pts)
  Component 3: Overlap section populated with papers found in both columns (0.4 pts)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_hf_papers_writer_014'


def get_cell_text(cell):
    """Extract text content from an ODF table cell."""
    from odf.text import P
    cell_text = ''
    for para in cell.getElementsByType(P):
        for node in para.childNodes:
            if node.nodeType == node.TEXT_NODE:
                cell_text += node.data
            elif hasattr(node, 'childNodes'):
                for child in node.childNodes:
                    if child.nodeType == child.TEXT_NODE:
                        cell_text += child.data
    return cell_text.strip()


def get_elem_text(elem):
    """Extract text content from any ODF element."""
    full_text = ''
    for node in elem.childNodes:
        if node.nodeType == node.TEXT_NODE:
            full_text += node.data
        elif hasattr(node, 'childNodes'):
            for child in node.childNodes:
                if child.nodeType == child.TEXT_NODE:
                    full_text += child.data
    return full_text.strip()


def extract_arxiv_ids(text_list):
    """Extract arXiv IDs (e.g., 2402.01680) from a list of strings."""
    ids = set()
    for text in text_list:
        matches = re.findall(r'\b(\d{4}\.\d{4,5})\b', text)
        ids.update(matches)
    return ids


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load ODT file
    try:
        from odf.opendocument import load
        from odf.text import P, H
        from odf.table import Table, TableRow, TableCell

        doc = load(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # -------------------------------------------------------------------------
    # Component 1: HuggingFace column filled with papers (0.3 points)
    # Initial state: column 1 (HuggingFace Featured) is empty.
    # Golden state: column 1 contains at least 1 entry with an arXiv-style ID.
    # -------------------------------------------------------------------------
    try:
        tables = doc.getElementsByType(Table)
        hf_papers = []
        arxiv_papers = []
        found_table = False

        for table in tables:
            rows = table.getElementsByType(TableRow)
            if len(rows) > 0:
                # Check first row for expected headers
                first_row_cells = rows[0].getElementsByType(TableCell)
                if len(first_row_cells) >= 2:
                    header_col1 = get_cell_text(first_row_cells[0]).lower()
                    header_col2 = get_cell_text(first_row_cells[1]).lower()
                    if 'huggingface' in header_col1 and ('arxiv' in header_col2 or 'cs.cl' in header_col2.lower()):
                        found_table = True
                        for r_idx, row in enumerate(rows):
                            if r_idx == 0:
                                continue  # skip header
                            cells = row.getElementsByType(TableCell)
                            if len(cells) >= 2:
                                col1_text = get_cell_text(cells[0])
                                col2_text = get_cell_text(cells[1])
                                if col1_text:
                                    hf_papers.append(col1_text)
                                if col2_text:
                                    arxiv_papers.append(col2_text)
                        break

        if not found_table:
            print("FAIL: Component 1 — Could not find the 2-column table with HuggingFace and ArXiv headers")
        elif len(hf_papers) == 0:
            print("FAIL: Component 1 — HuggingFace column is empty (0 papers)")
        else:
            hf_ids = extract_arxiv_ids(hf_papers)
            if len(hf_ids) > 0:
                print(f"PASS: Component 1 — HuggingFace column filled with {len(hf_papers)} papers, {len(hf_ids)} arXiv IDs found (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 — HuggingFace column has {len(hf_papers)} entries but no valid arXiv IDs found")

    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------------
    # Component 2: ArXiv cs.CL column filled with papers (0.3 points)
    # Initial state: column 2 (ArXiv cs.CL Total) is empty.
    # Golden state: column 2 contains at least 1 entry with an arXiv-style ID.
    # -------------------------------------------------------------------------
    try:
        if not found_table:
            print("FAIL: Component 2 — Table not found (see Component 1)")
        elif len(arxiv_papers) == 0:
            print("FAIL: Component 2 — ArXiv cs.CL column is empty (0 papers)")
        else:
            arxiv_ids = extract_arxiv_ids(arxiv_papers)
            if len(arxiv_ids) > 0:
                print(f"PASS: Component 2 — ArXiv cs.CL column filled with {len(arxiv_papers)} papers, {len(arxiv_ids)} arXiv IDs found (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — ArXiv column has {len(arxiv_papers)} entries but no valid arXiv IDs found")

    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Component 3: Overlap section populated (0.4 points)
    # Initial state: "Overlap" heading exists but no overlap papers are listed below it.
    # Golden state: After the "Overlap" heading, at least 1 paper is listed that appears
    #   in both the HuggingFace and ArXiv columns (matched by arXiv ID).
    # -------------------------------------------------------------------------
    try:
        headings = doc.getElementsByType(H)
        overlap_heading_found = False
        for h in headings:
            h_text = get_elem_text(h).strip().lower()
            if 'overlap' in h_text:
                overlap_heading_found = True
                break

        if not overlap_heading_found:
            print("FAIL: Component 3 — No 'Overlap' heading found in document")
        else:
            # Get all paragraphs in the document body after the table
            # We look at all body-level elements to find what comes after the 'Overlap' heading
            body = doc.text
            overlap_section_texts = []
            in_overlap = False

            for child in body.childNodes:
                if not hasattr(child, 'tagName'):
                    continue
                tag = child.tagName
                if tag == 'text:h':
                    child_text = get_elem_text(child).strip().lower()
                    if 'overlap' in child_text:
                        in_overlap = True
                    else:
                        in_overlap = False
                elif tag == 'text:p' and in_overlap:
                    para_text = get_elem_text(child).strip()
                    if para_text:
                        overlap_section_texts.append(para_text)

            # Check if overlap section has papers with arXiv IDs
            overlap_section_ids = extract_arxiv_ids(overlap_section_texts)

            # Also check: these IDs should appear in both columns
            hf_ids_set = extract_arxiv_ids(hf_papers) if hf_papers else set()
            arxiv_ids_set = extract_arxiv_ids(arxiv_papers) if arxiv_papers else set()
            true_overlap = hf_ids_set & arxiv_ids_set

            if len(overlap_section_texts) == 0:
                print("FAIL: Component 3 — 'Overlap' heading exists but no text entries follow it")
            elif len(overlap_section_ids) == 0:
                # Check if there's a 'no overlap' statement
                combined_text = ' '.join(overlap_section_texts).lower()
                if 'no overlap' in combined_text or 'none' in combined_text:
                    # Only valid if actual overlap is empty
                    if len(true_overlap) == 0:
                        print(f"PASS: Component 3 — Overlap section correctly states no overlap (0.4 pts)")
                        total_score += 0.4
                    else:
                        print(f"FAIL: Component 3 — Overlap section says 'no overlap' but actual overlap exists: {sorted(true_overlap)}")
                else:
                    print(f"FAIL: Component 3 — Overlap section has text but no recognizable arXiv IDs: {overlap_section_texts[:3]}")
            else:
                # Papers with IDs are listed in the overlap section
                overlap_in_both = overlap_section_ids & true_overlap if true_overlap else overlap_section_ids
                print(f"PASS: Component 3 — Overlap section lists {len(overlap_section_texts)} paper(s), {len(overlap_section_ids)} arXiv IDs found (0.4 pts)")
                if true_overlap:
                    print(f"  Correctly matched IDs: {sorted(overlap_in_both)}")
                total_score += 0.4

    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/comparison.odt'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

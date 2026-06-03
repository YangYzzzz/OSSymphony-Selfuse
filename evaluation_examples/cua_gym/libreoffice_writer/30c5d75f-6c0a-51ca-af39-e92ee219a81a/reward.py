"""
Reward Script: Annotated Bibliography in LibreOffice Writer
Task ID: osworld_multi_apps_hf_papers_writer_013
Domain: libreoffice_writer
Scoring:
  Component 1: 8-10 numbered bibliography entries present      (0.3 pts)
  Component 2: Each entry title has bold formatting            (0.3 pts)
  Component 3: Each entry has clickable arXiv hyperlink        (0.2 pts)
  Component 4: Each entry has author line and annotation text  (0.2 pts)
  Total: 1.0
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_hf_papers_writer_013'

FILE_PATH = os.path.join(WORKDIR, 'annotated_bib.odt')


def get_para_text(para):
    """Extract full text from an ODT paragraph node."""
    parts = []
    for node in para.childNodes:
        if hasattr(node, 'data'):
            parts.append(node.data)
        elif hasattr(node, 'childNodes'):
            for child in node.childNodes:
                if hasattr(child, 'data'):
                    parts.append(child.data)
    return ''.join(parts)


def verify_task(file_path):
    """
    Verify task completion for annotated bibliography.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the ODT document
    try:
        from odf.opendocument import load
        from odf.text import P, H, A, Span
        doc = load(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Gather all paragraphs
    try:
        all_paras = doc.getElementsByType(P)
    except Exception as e:
        print(f"CRITICAL: Cannot read paragraphs: {e}")
        print("REWARD: 0.0")
        return 0.0

    # -------------------------------------------------------------------------
    # Component 1: 8-10 numbered bibliography entries (0.3 points)
    # An entry is a paragraph starting with '[N]' where N is a digit.
    # The initial_env has 0 such paragraphs; golden_env has 8.
    # -------------------------------------------------------------------------
    try:
        entry_paras = []
        for para in all_paras:
            text = get_para_text(para)
            # Match paragraphs starting with [1], [2], ... [10]
            if re.match(r'^\[\d+\]', text.strip()):
                entry_paras.append((para, text))

        num_entries = len(entry_paras)
        if 8 <= num_entries <= 10:
            print(f"PASS: Component 1 — found {num_entries} numbered bibliography entries (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — expected 8-10 numbered entries, found {num_entries}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------------
    # Component 2: Entry titles have bold formatting (0.3 points)
    # Each title paragraph should contain a span with a bold style (BoldTitle
    # or equivalent automatic style with font-weight=bold).
    # First, determine which automatic styles are bold.
    # -------------------------------------------------------------------------
    try:
        # Collect all auto-style names that have font-weight=bold
        bold_style_names = set()
        try:
            for style in doc.automaticstyles.childNodes:
                style_name = style.getAttribute('name')
                if not style_name:
                    continue
                for child in style.childNodes:
                    tag = child.tagName if hasattr(child, 'tagName') else ''
                    if 'text-properties' in tag:
                        fw = child.getAttribute('fontweight')
                        if fw and fw.lower() == 'bold':
                            bold_style_names.add(style_name)
        except Exception:
            pass

        # Also check named styles from doc.styles
        try:
            for style in doc.styles.childNodes:
                style_name = style.getAttribute('name')
                if not style_name:
                    continue
                for child in style.childNodes:
                    tag = child.tagName if hasattr(child, 'tagName') else ''
                    if 'text-properties' in tag:
                        fw = child.getAttribute('fontweight')
                        if fw and fw.lower() == 'bold':
                            bold_style_names.add(style_name)
        except Exception:
            pass

        entries_with_bold_title = 0
        for para, text in entry_paras:
            # Check if any span in this paragraph uses a bold style
            has_bold = False
            for node in para.childNodes:
                tag = getattr(node, 'tagName', '')
                if 'span' in tag.lower():
                    span_style = node.getAttribute('stylename')
                    if span_style and span_style in bold_style_names:
                        has_bold = True
                        break
                    # Also check inline font-weight on the span itself
                    for child in node.childNodes:
                        child_tag = getattr(child, 'tagName', '')
                        if 'text-properties' in child_tag:
                            fw = child.getAttribute('fontweight')
                            if fw and fw.lower() == 'bold':
                                has_bold = True
                                break
                    if has_bold:
                        break
            if has_bold:
                entries_with_bold_title += 1

        if entries_with_bold_title == num_entries and num_entries >= 8:
            print(f"PASS: Component 2 — all {entries_with_bold_title} entry titles have bold formatting (0.3 pts)")
            total_score += 0.3
        elif entries_with_bold_title >= max(1, num_entries - 1) and num_entries >= 8:
            # Partial: allow one entry to lack bold
            pts = round(0.3 * entries_with_bold_title / max(num_entries, 1), 2)
            print(f"PARTIAL: Component 2 — {entries_with_bold_title}/{num_entries} titles bold ({pts} pts)")
            total_score += pts
        else:
            print(f"FAIL: Component 2 — only {entries_with_bold_title}/{num_entries} entry titles have bold spans")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Component 3: Each entry has a clickable arXiv hyperlink (0.2 points)
    # -------------------------------------------------------------------------
    try:
        all_links = doc.getElementsByType(A)
        arxiv_hrefs = []
        for link in all_links:
            href = link.getAttribute('href') or ''
            if 'arxiv.org' in href.lower():
                arxiv_hrefs.append(href)

        num_arxiv_links = len(arxiv_hrefs)
        if num_arxiv_links >= 8:
            print(f"PASS: Component 3 — found {num_arxiv_links} clickable arXiv hyperlinks (0.2 pts)")
            total_score += 0.2
        elif num_arxiv_links > 0:
            pts = round(0.2 * num_arxiv_links / max(num_entries, 8), 2)
            print(f"PARTIAL: Component 3 — found {num_arxiv_links} arXiv links, expected {num_entries} ({pts} pts)")
            total_score += pts
        else:
            print(f"FAIL: Component 3 — no arXiv hyperlinks found (expected {num_entries})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -------------------------------------------------------------------------
    # Component 4: Each entry has author + year line AND annotation text (0.2 pts)
    # Structure per entry: [title para, authors para, arXiv para, annotation para, blank para]
    # Check that: (a) at least one para per entry contains '. 2024' (authors+year)
    #             (b) at least one para per entry contains sentence-like annotation (>50 chars)
    # -------------------------------------------------------------------------
    try:
        # Build a map: for each entry starting index, collect subsequent BibNormal paras until blank
        para_texts = [(get_para_text(p), p.getAttribute('stylename') or '') for p in all_paras]

        entries_with_authors = 0
        entries_with_annotation = 0

        for entry_idx, (entry_para, entry_text) in enumerate(entry_paras):
            # Find this paragraph in the full list
            target_text = entry_text
            start_idx = None
            for k, (pt, ps) in enumerate(para_texts):
                if pt.strip() == target_text.strip():
                    start_idx = k
                    break

            if start_idx is None:
                continue

            # Collect following BibNormal paragraphs until blank/next entry
            sibling_texts = []
            for k in range(start_idx + 1, min(start_idx + 6, len(para_texts))):
                pt, ps = para_texts[k]
                if re.match(r'^\[\d+\]', pt.strip()):
                    break  # next entry
                if pt.strip() == '':
                    break  # separator
                sibling_texts.append(pt)

            # Check for author+year line (contains '. 2024.' or '. 2024' pattern)
            has_authors = any(
                re.search(r'\.\s*202[0-9]\.?', t) for t in sibling_texts
            )
            # Check for annotation (a paragraph with >50 chars that is not a URL line)
            has_annotation = any(
                len(t) > 50 and 'arxiv.org' not in t.lower()
                for t in sibling_texts
            )

            if has_authors:
                entries_with_authors += 1
            if has_annotation:
                entries_with_annotation += 1

        # Score: need both conditions for all entries
        author_ratio = entries_with_authors / max(num_entries, 1)
        annot_ratio = entries_with_annotation / max(num_entries, 1)
        comp4_score = 0.2 * min(author_ratio, annot_ratio)
        comp4_score = round(comp4_score, 2)

        if comp4_score >= 0.19:  # ~1.0 ratio
            print(f"PASS: Component 4 — all {num_entries} entries have author/year and annotation (0.2 pts)")
            total_score += 0.2
        elif comp4_score > 0:
            print(f"PARTIAL: Component 4 — {entries_with_authors} author lines, {entries_with_annotation} annotations ({comp4_score} pts)")
            total_score += comp4_score
        else:
            print(f"FAIL: Component 4 — author lines: {entries_with_authors}/{num_entries}, annotations: {entries_with_annotation}/{num_entries}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

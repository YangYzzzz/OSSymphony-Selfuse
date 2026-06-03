"""
Reward Script: Add DOI hyperlinks to APA-formatted references
Task ID: osworld_multi_apps_doi_resolve_writer_004
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): Document has 10 paragraphs (5 original refs + 5 DOI lines added)
  Component 2 (0.5): All 5 DOI paragraphs contain correct clickable hyperlinks
                     (text:a element with correct https://doi.org/[DOI] href)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_doi_resolve_writer_004'

# Expected DOIs in order (corresponding to the 5 APA references)
EXPECTED_DOIS = [
    "https://doi.org/10.48550/arXiv.1706.03762",  # Ref 1: Attention Is All You Need
    "https://doi.org/10.18653/v1/N19-1423",        # Ref 2: BERT: Pre-training
    "https://doi.org/10.48550/arXiv.2005.14165",   # Ref 3: Language Models are Few-Shot Learners
    "https://doi.org/10.48550/arXiv.2203.02155",   # Ref 4: Training language models to follow instructions
    "https://doi.org/10.48550/arXiv.2302.13971",   # Ref 5: LLaMA: Open and Efficient
]


def get_para_text(para):
    """Recursively extract all text from a paragraph node."""
    text = ""
    for node in para.childNodes:
        if node.nodeType == node.TEXT_NODE:
            text += node.data
        elif hasattr(node, "childNodes"):
            for child in node.childNodes:
                if child.nodeType == child.TEXT_NODE:
                    text += child.data
                elif hasattr(child, "childNodes"):
                    for gc in child.childNodes:
                        if gc.nodeType == gc.TEXT_NODE:
                            text += gc.data
    return text


def find_hyperlinks_in_para(para):
    """Return list of (href, display_text) for all text:a hyperlinks in a paragraph."""
    results = []

    def recurse(node):
        if hasattr(node, "tagName") and node.tagName == "text:a":
            href = node.getAttribute("href") or ""
            text = ""
            for child in node.childNodes:
                if child.nodeType == child.TEXT_NODE:
                    text += child.data
                elif hasattr(child, "childNodes"):
                    for gc in child.childNodes:
                        if gc.nodeType == gc.TEXT_NODE:
                            text += gc.data
            results.append((href, text.strip()))
        if hasattr(node, "childNodes"):
            for child in node.childNodes:
                recurse(child)

    recurse(para)
    return results


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from odf.opendocument import load
        from odf.text import P
        odt_doc = load(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get all paragraphs
    try:
        paras = odt_doc.getElementsByType(P)
        num_paras = len(paras)
        print(f"INFO: Document has {num_paras} paragraphs")
    except Exception as e:
        print(f"CRITICAL: Cannot read paragraphs: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Document now has 10 paragraphs (5 refs + 5 DOI lines added) (0.5 points)
    # Initial document has 5 paragraphs; task adds 5 DOI paragraphs → 10 total.
    # This FAILS on initial_env (5 paragraphs) and PASSES on golden_env (10 paragraphs).
    try:
        if num_paras == 10:
            print(f"PASS: Component 1 — Document has 10 paragraphs (5 refs + 5 DOI lines added) (0.5 pts)")
            total_score += 0.5
        elif num_paras > 5:
            # Partial credit for partially adding DOI lines (some but not all)
            doi_lines_added = num_paras - 5
            partial = round(doi_lines_added / 5 * 0.5, 2) if doi_lines_added > 0 else 0.0
            print(f"PARTIAL: Component 1 — {doi_lines_added}/5 DOI lines added ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — Expected 10 paragraphs (5 DOI lines added), found {num_paras}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 5 DOI paragraphs have correct clickable hyperlinks (0.5 points)
    # In golden_env, odd-indexed paragraphs (1, 3, 5, 7, 9) each contain a text:a hyperlink
    # with href == https://doi.org/[DOI]. This FAILS on initial_env (no hyperlinks at all).
    try:
        doi_correct_count = 0

        if num_paras == 10:
            # Structured check: DOI paragraphs are at positions 1, 3, 5, 7, 9
            doi_para_indices = [1, 3, 5, 7, 9]
            for list_idx, para_idx in enumerate(doi_para_indices):
                para = paras[para_idx]
                hyperlinks = find_hyperlinks_in_para(para)
                expected_doi = EXPECTED_DOIS[list_idx]
                if hyperlinks:
                    found_correct = any(
                        href == expected_doi or link_text == expected_doi
                        for href, link_text in hyperlinks
                    )
                    if found_correct:
                        doi_correct_count += 1
                        print(f"PASS: DOI hyperlink {list_idx+1} — href={expected_doi}")
                    else:
                        found_hrefs = [h for h, t in hyperlinks]
                        print(f"FAIL: DOI hyperlink {list_idx+1} — Expected {expected_doi}, got {found_hrefs}")
                else:
                    para_text = get_para_text(para)
                    print(f"FAIL: DOI hyperlink {list_idx+1} — No hyperlink element. Text: {repr(para_text[:80])}")
        else:
            # Flexible fallback: search all paragraphs for hyperlinks matching expected DOIs
            doi_indices_found = set()
            for para in paras:
                for href, link_text in find_hyperlinks_in_para(para):
                    for idx, expected_doi in enumerate(EXPECTED_DOIS):
                        if href == expected_doi or link_text == expected_doi:
                            doi_indices_found.add(idx)
            doi_correct_count = len(doi_indices_found)
            print(f"INFO: Flexible search found {doi_correct_count}/5 correct DOI hyperlinks")

        if doi_correct_count == 5:
            print(f"PASS: Component 2 — All 5 DOI hyperlinks correct (0.5 pts)")
            total_score += 0.5
        elif doi_correct_count >= 1:
            partial = round(doi_correct_count / 5 * 0.5, 2)
            print(f"PARTIAL: Component 2 — {doi_correct_count}/5 DOI hyperlinks correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No correct DOI hyperlinks found (expected 5)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in a given env
file_path = f'{WORKDIR}/formatted_refs.odt'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

"""
Reward Script: LibreOffice Writer paper_list.odt — Append arXiv URLs to paper titles
Task ID: osworld_multi_apps_doi_resolve_writer_003
Domain: libreoffice_writer
Scoring:
  Component 1: Chain-of-Thought paper has correct arXiv URL appended (0.25 pts)
  Component 2: Self-Consistency paper has correct arXiv URL appended (0.25 pts)
  Component 3: Tree of Thoughts paper has correct arXiv URL appended (0.25 pts)
  Component 4: ReAct paper has correct arXiv URL appended (0.25 pts)
  Total: 1.0

Each component checks that the paragraph text ends with the paper title followed by the
bracketed arXiv URL in format: "Title [https://arxiv.org/abs/ID]"
This FAILS on initial_env (no URLs) and PASSES on golden_env (URLs appended).
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_doi_resolve_writer_003'
FILE_PATH = f'{WORKDIR}/paper_list.odt'

# Ground truth: paper title fragments and their expected arXiv IDs
PAPERS = [
    {
        "title_fragment": "Chain-of-Thought Prompting Elicits Reasoning",
        "arxiv_id": "2201.11903",
        "expected_url": "https://arxiv.org/abs/2201.11903",
    },
    {
        "title_fragment": "Self-Consistency Improves Chain of Thought Reasoning",
        "arxiv_id": "2203.11171",
        "expected_url": "https://arxiv.org/abs/2203.11171",
    },
    {
        "title_fragment": "Tree of Thoughts",
        "arxiv_id": "2305.10601",
        "expected_url": "https://arxiv.org/abs/2305.10601",
    },
    {
        "title_fragment": "ReAct: Synergizing Reasoning and Acting",
        "arxiv_id": "2210.03629",
        "expected_url": "https://arxiv.org/abs/2210.03629",
    },
]


def get_paragraph_texts(file_path):
    """
    Load an ODT file and extract full text from each paragraph (P element).
    Returns a list of paragraph text strings.
    """
    from odf.opendocument import load
    from odf.text import P

    doc = load(file_path)
    paras = doc.getElementsByType(P)
    texts = []
    for para in paras:
        text_parts = []
        for node in para.childNodes:
            if node.nodeType == node.TEXT_NODE:
                text_parts.append(node.data)
            elif hasattr(node, 'tagName') and node.tagName == 'text:span':
                for child in node.childNodes:
                    if child.nodeType == child.TEXT_NODE:
                        text_parts.append(child.data)
            elif hasattr(node, 'tagName') and node.tagName == 'text:a':
                # Hyperlink anchor text
                for child in node.childNodes:
                    if child.nodeType == child.TEXT_NODE:
                        text_parts.append(child.data)
                    elif hasattr(child, 'tagName') and child.tagName == 'text:span':
                        for grandchild in child.childNodes:
                            if grandchild.nodeType == grandchild.TEXT_NODE:
                                text_parts.append(grandchild.data)
        texts.append(''.join(text_parts))
    return texts


def verify_task(file_path):
    """
    Verify that each paper title in paper_list.odt has the correct arXiv URL appended
    in the format: 'Title [https://arxiv.org/abs/ID]'

    Returns a float between 0.0 and 1.0.
    """
    total_score = 0.0

    # Load document paragraphs
    try:
        para_texts = get_paragraph_texts(file_path)
        print(f"INFO: Loaded {len(para_texts)} paragraphs from {file_path}")
        for i, t in enumerate(para_texts):
            print(f"  Para {i}: {repr(t)}")
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if len(para_texts) < 4:
        print(f"FAIL: Expected at least 4 paragraphs, found {len(para_texts)}")
        print("REWARD: 0.0")
        return 0.0

    # Check each paper independently
    for idx, paper in enumerate(PAPERS, start=1):
        title_fragment = paper["title_fragment"]
        expected_url = paper["expected_url"]
        expected_suffix = f"[{expected_url}]"

        # Component idx: paper has correct arXiv URL appended (0.25 pts)
        try:
            # Find the paragraph that contains this paper's title fragment
            matching_para = None
            for para_text in para_texts:
                if title_fragment in para_text:
                    matching_para = para_text
                    break

            if matching_para is None:
                print(f"FAIL: Component {idx} — No paragraph found containing '{title_fragment}'")
                continue

            # Check that the paragraph ends with [https://arxiv.org/abs/ID]
            # Strip trailing whitespace for comparison
            stripped = matching_para.strip()
            if stripped.endswith(expected_suffix):
                print(f"PASS: Component {idx} — '{title_fragment}' has correct URL [{expected_url}] (0.25 pts)")
                total_score += 0.25
            else:
                # Check if any URL is present (even if wrong)
                if "[https://arxiv.org/abs/" in stripped:
                    print(f"FAIL: Component {idx} — '{title_fragment}' has an arXiv URL but not the expected one.")
                    print(f"  Expected suffix: {expected_suffix}")
                    print(f"  Actual text: {repr(stripped[-80:])}")
                else:
                    print(f"FAIL: Component {idx} — '{title_fragment}' does not have the arXiv URL appended.")
                    print(f"  Expected suffix: {expected_suffix}")
                    print(f"  Actual text: {repr(stripped[-80:])}")
        except Exception as e:
            print(f"ERROR: Component {idx} — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint: verify the canonical artifact on this VM
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

"""
Reward Script: HuggingFace Daily Papers - Copy paper titles and authors to LibreOffice Writer
Task ID: osworld_multi_apps_hf_papers_writer_005
Domain: libreoffice_writer
Scoring:
  - Component 1: At least 5 numbered paper entries present (0.4 pts)
  - Component 2: Author lines present for at least 3 entries (0.3 pts)
  - Component 3: Entries are numbered sequentially starting from 1 (0.3 pts)
  Total: 1.0
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_hf_papers_writer_005'

def get_text_from_node(node):
    """Recursively extract text from an ODT node."""
    text = ''
    for child in node.childNodes:
        if child.nodeType == child.TEXT_NODE:
            text += child.data
        else:
            text += get_text_from_node(child)
    return text


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Task: The agent should have copied the first 5 papers (titles + authors)
    from HuggingFace daily papers for 2024-01-15 into hf_papers.odt as a
    numbered list under the existing heading.
    """
    total_score = 0.0

    # Load the ODT file
    try:
        from odf.opendocument import load
        doc = load(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract all paragraph texts
    try:
        paragraphs = []
        for elem in doc.body.childNodes:
            if hasattr(elem, 'childNodes'):
                for para in elem.childNodes:
                    if hasattr(para, 'qname') and para.qname[1] in ('h', 'p', 'list'):
                        txt = get_text_from_node(para)
                        paragraphs.append(txt)

        print(f"Found {len(paragraphs)} paragraphs total")
        for i, p in enumerate(paragraphs):
            print(f"  Para[{i}]: {repr(p[:100])}")
    except Exception as e:
        print(f"CRITICAL: Cannot parse paragraphs: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Verify heading is intact (precondition gate)
    heading_found = any('HuggingFace Daily Papers' in p for p in paragraphs)
    if not heading_found:
        print("FAIL: Heading 'HuggingFace Daily Papers' not found — file may be corrupted")
        print("REWARD: 0.0")
        return 0.0
    print("PASS (gate): Heading 'HuggingFace Daily Papers' is present")

    # Component 1: At least 5 numbered paper entries present (0.4 points)
    # A numbered entry starts with "1." / "2." / ... etc.
    try:
        numbered_entries = []
        for p in paragraphs:
            stripped = p.strip()
            if re.match(r'^\d+\.', stripped):
                numbered_entries.append(stripped)

        print(f"Found {len(numbered_entries)} numbered entries")
        if len(numbered_entries) >= 5:
            print(f"PASS: Component 1 — {len(numbered_entries)} numbered paper entries found (>=5) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — expected >=5 numbered entries, found {len(numbered_entries)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Author lines present for at least 3 entries (0.3 points)
    # Author lines contain "Authors:" prefix
    try:
        author_lines = []
        for p in paragraphs:
            stripped = p.strip()
            if stripped.lower().startswith('authors:') or ('authors:' in stripped.lower()):
                author_lines.append(stripped)

        print(f"Found {len(author_lines)} author lines")
        if len(author_lines) >= 3:
            print(f"PASS: Component 2 — {len(author_lines)} author lines found (>=3) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — expected >=3 author lines, found {len(author_lines)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Entries are numbered sequentially starting from 1 (0.3 points)
    # Check that we have entries numbered 1, 2, 3, 4, 5 in order
    try:
        entry_numbers = []
        for entry in numbered_entries:
            m = re.match(r'^(\d+)\.', entry)
            if m:
                entry_numbers.append(int(m.group(1)))

        # Entries must start at 1 and cover at least 1..5 sequentially
        expected_sequence = list(range(1, min(len(entry_numbers), 5) + 1))
        if len(entry_numbers) >= 5 and entry_numbers[:5] == expected_sequence:
            print(f"PASS: Component 3 — entries numbered sequentially {entry_numbers[:5]} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — expected sequential numbering 1..5, found: {entry_numbers}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/hf_papers.odt'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

"""
Reward Script: Convert PDF to tagged PDF with proper heading structure
Task ID: pdf_res_077
Domain: pdf
Scoring:
  - Component 1: StructTreeRoot present in catalog (0.25 pts)
  - Component 2: MarkInfo/Marked = True (0.15 pts)
  - Component 3: H1 element in structure tree (0.20 pts)
  - Component 4: H2 elements in structure tree (>= 2) (0.20 pts)
  - Component 5: P (paragraph) elements in structure tree (>= 2) (0.20 pts)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_077'
TARGET_FILE = os.path.join(WORKDIR, 'papers', 'thesis_abstract_tagged.pdf')


def collect_structure_tags(node, tags=None):
    """Recursively collect all /S (structure type) tags from the structure tree."""
    import pikepdf
    if tags is None:
        tags = []
    try:
        if hasattr(node, 'keys'):
            if '/S' in node:
                tags.append(str(node['/S']))
            if '/K' in node:
                children = node['/K']
                if isinstance(children, pikepdf.Array):
                    for child in children:
                        collect_structure_tags(child, tags)
                elif hasattr(children, 'keys'):
                    collect_structure_tags(children, tags)
    except Exception as e:
        print(f"WARN: Error traversing structure tree node: {e}")
    return tags


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    import pikepdf
    total_score = 0.0

    # Precondition: file must exist and be a valid PDF
    try:
        pdf = pikepdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: StructTreeRoot present in catalog (0.25 points)
    try:
        has_struct_tree = '/StructTreeRoot' in pdf.Root
        if has_struct_tree:
            print(f"PASS: Component 1 — StructTreeRoot found in catalog (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — StructTreeRoot not found in catalog. Keys: {list(pdf.Root.keys())}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: MarkInfo with Marked=True (0.15 points)
    try:
        has_markinfo = '/MarkInfo' in pdf.Root
        if has_markinfo:
            mark_info = pdf.Root['/MarkInfo']
            is_marked = '/Marked' in mark_info and bool(mark_info['/Marked'])
            if is_marked:
                print(f"PASS: Component 2 — MarkInfo/Marked is True (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 — MarkInfo exists but Marked is not True")
        else:
            print(f"FAIL: Component 2 — MarkInfo not found in catalog")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Collect all structure tags for components 3-5
    all_tags = []
    try:
        if '/StructTreeRoot' in pdf.Root:
            struct_root = pdf.Root['/StructTreeRoot']
            if '/K' in struct_root:
                all_tags = collect_structure_tags(struct_root['/K'])
                print(f"INFO: Found structure tags: {all_tags}")
    except Exception as e:
        print(f"WARN: Could not collect structure tags: {e}")

    # Component 3: H1 element exists in structure tree (0.20 points)
    try:
        h1_count = sum(1 for t in all_tags if t == '/H1')
        if h1_count >= 1:
            print(f"PASS: Component 3 — Found {h1_count} H1 element(s) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — No H1 elements found in structure tree. Tags: {all_tags}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: H2 elements exist (>= 2) in structure tree (0.20 points)
    try:
        h2_count = sum(1 for t in all_tags if t == '/H2')
        if h2_count >= 2:
            print(f"PASS: Component 4 — Found {h2_count} H2 element(s) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — Found {h2_count} H2 element(s), expected >= 2. Tags: {all_tags}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: P (paragraph) elements exist (>= 2) in structure tree (0.20 points)
    try:
        p_count = sum(1 for t in all_tags if t == '/P')
        if p_count >= 2:
            print(f"PASS: Component 5 — Found {p_count} P element(s) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 5 — Found {p_count} P element(s), expected >= 2. Tags: {all_tags}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    pdf.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(TARGET_FILE):
    print(f"File not found: {TARGET_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(TARGET_FILE)

"""
Reward Script: Verify Mermaid flowchart diagram added to system_design.md
Task ID: vscode_rf_027
Domain: vscode
Scoring:
  - Component 1 (0.3): Mermaid fenced code block exists with proper syntax
  - Component 2 (0.3): Flowchart direction declared (graph LR or graph TD)
  - Component 3 (0.4): Three nodes Ingestion --> Processing --> Storage connected in sequence
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_rf_027'
FILE_PATH = os.path.join(WORKDIR, 'projects', 'architecture', 'system_design.md')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be readable
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract mermaid code blocks from the markdown content
    # Pattern: ```mermaid ... ``` (with optional whitespace variations)
    mermaid_pattern = re.compile(
        r'```\s*mermaid\s*\n(.*?)```',
        re.DOTALL | re.IGNORECASE
    )
    mermaid_blocks = mermaid_pattern.findall(content)

    # Component 1: Mermaid fenced code block exists (0.3 points)
    try:
        if len(mermaid_blocks) > 0:
            print(f"PASS: Component 1 — Found {len(mermaid_blocks)} mermaid code block(s) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — No mermaid fenced code block found in file")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Flowchart direction declared (0.3 points)
    # The mermaid block should contain 'graph LR' or 'graph TD' or 'graph TB'
    try:
        mermaid_content = ""
        for block in mermaid_blocks:
            if re.search(r'graph\s+(LR|TD|TB|RL|BT)', block, re.IGNORECASE):
                mermaid_content = block
                break
        if mermaid_content:
            direction = re.search(r'graph\s+(LR|TD|TB|RL|BT)', mermaid_content, re.IGNORECASE).group(1)
            print(f"PASS: Component 2 — Flowchart direction 'graph {direction}' found (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — No flowchart direction (graph LR/TD/TB) found in mermaid blocks")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Three nodes connected in sequence (0.4 points)
    # Must have Ingestion, Processing, and Storage nodes connected with arrows
    try:
        if mermaid_content:
            # Normalize whitespace in the mermaid content for matching
            normalized = mermaid_content.strip()

            # Check for presence of all three node names
            has_ingestion = bool(re.search(r'\bIngestion\b', normalized, re.IGNORECASE))
            has_processing = bool(re.search(r'\bProcessing\b', normalized, re.IGNORECASE))
            has_storage = bool(re.search(r'\bStorage\b', normalized, re.IGNORECASE))

            # Check for sequential connections using arrow syntax (-->, --->, etc.)
            # Ingestion --> Processing
            ing_to_proc = bool(re.search(
                r'Ingestion\s*(?:\[.*?\])?\s*-+>+\s*Processing',
                normalized, re.IGNORECASE
            ))
            # Alternative: Ingestion[label] --> Processing[label]
            if not ing_to_proc:
                ing_to_proc = bool(re.search(
                    r'Ingestion.*?-+>+.*?Processing',
                    normalized, re.IGNORECASE
                ))

            # Processing --> Storage
            proc_to_stor = bool(re.search(
                r'Processing\s*(?:\[.*?\])?\s*-+>+\s*Storage',
                normalized, re.IGNORECASE
            ))
            if not proc_to_stor:
                proc_to_stor = bool(re.search(
                    r'Processing.*?-+>+.*?Storage',
                    normalized, re.IGNORECASE
                ))

            all_nodes = has_ingestion and has_processing and has_storage
            all_connections = ing_to_proc and proc_to_stor

            if all_nodes and all_connections:
                print(f"PASS: Component 3 — Ingestion --> Processing --> Storage sequence verified (0.4 pts)")
                total_score += 0.4
            else:
                details = []
                if not has_ingestion:
                    details.append("missing 'Ingestion' node")
                if not has_processing:
                    details.append("missing 'Processing' node")
                if not has_storage:
                    details.append("missing 'Storage' node")
                if not ing_to_proc:
                    details.append("missing Ingestion-->Processing connection")
                if not proc_to_stor:
                    details.append("missing Processing-->Storage connection")
                print(f"FAIL: Component 3 — {', '.join(details)}")
                print(f"  Mermaid content: {normalized[:200]}")
        else:
            print(f"FAIL: Component 3 — No mermaid flowchart block to check for nodes")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

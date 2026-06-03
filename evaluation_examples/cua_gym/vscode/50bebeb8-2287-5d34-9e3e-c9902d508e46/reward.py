"""
Reward Script: Convert code cell to markdown and markdown cell to code in Jupyter notebook
Task ID: vscode_prod_010
Domain: vscode
Scoring:
  Component 1 (0.50): Cell 2 (0-indexed) is markdown type (0.30) AND content preserved (0.20)
  Component 2 (0.50): Cell 3 (0-indexed) is code type (0.30) AND content preserved (0.20)
  Content preservation is only scored when the type change is correct.
"""

import json
import os

WORKDIR = '/home/user'
TASK_ID = 'vscode_prod_010'
NOTEBOOK_PATH = os.path.join(WORKDIR, 'projects', 'data-science', 'exploration.ipynb')

# Expected content for cell 2 (originally code cell with comments)
EXPECTED_CELL2_SOURCE = [
    "# Data Exploration Summary\n",
    "# \n",
    "# This section analyzes the quarterly sales performance\n",
    "# across different regions. Key metrics include:\n",
    "# - Revenue trends over the past 5 quarters\n",
    "# - Expense-to-revenue ratio analysis\n",
    "# - Customer acquisition rates by region\n",
    "# \n",
    "# The analysis below focuses on identifying seasonal\n",
    "# patterns and regional performance differences."
]

# Expected content for cell 3 (originally markdown cell with Python code)
EXPECTED_CELL3_SOURCE = [
    "summary_stats = df.describe()\n",
    "avg_profit_by_region = df.groupby('Region')['Profit'].mean()\n",
    "growth_rate = (df['Revenue'].iloc[-1] - df['Revenue'].iloc[0]) / df['Revenue'].iloc[0] * 100\n",
    "print(f'Average profit margin: {df[\"Profit\"].mean():.2f}')\n",
    "print(f'Revenue growth rate: {growth_rate:.1f}%')"
]


def normalize_source(source_lines):
    """Normalize cell source for comparison: join, strip trailing whitespace."""
    if isinstance(source_lines, list):
        text = "".join(source_lines)
    else:
        text = source_lines
    return text.strip()


def verify_task(notebook_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        with open(notebook_path, 'r') as f:
            nb = json.load(f)
    except Exception as e:
        print(f"CRITICAL: Cannot load notebook {notebook_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    cells = nb.get('cells', [])
    if len(cells) < 5:
        print(f"CRITICAL: Expected at least 5 cells, found {len(cells)}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Cell 2 (0-indexed) is markdown AND content preserved (0.50 points)
    # Initially this was a code cell; after task it should be markdown with same content
    try:
        cell2_type = cells[2].get('cell_type', '')
        cell2_source = normalize_source(cells[2].get('source', []))
        expected_cell2 = normalize_source(EXPECTED_CELL2_SOURCE)

        if cell2_type == 'markdown':
            # Type is correct - award base points
            print(f"PASS: Component 1a -- Cell 2 is markdown type (0.30 pts)")
            total_score += 0.30

            # Check content preservation (only scored if type is correct)
            core_phrases = [
                "Data Exploration Summary",
                "quarterly sales performance",
                "Revenue trends",
                "Customer acquisition rates"
            ]
            if cell2_source == expected_cell2:
                print(f"PASS: Component 1b -- Cell 2 content preserved exactly (0.20 pts)")
                total_score += 0.20
            else:
                matches = sum(1 for phrase in core_phrases if phrase in cell2_source)
                if matches >= 3:
                    print(f"PASS: Component 1b -- Cell 2 content mostly preserved ({matches}/4 key phrases) (0.20 pts)")
                    total_score += 0.20
                else:
                    print(f"FAIL: Component 1b -- Cell 2 content not preserved. Found {matches}/4 key phrases")
                    print(f"  Actual (first 200 chars): {cell2_source[:200]}")
        else:
            print(f"FAIL: Component 1 -- Cell 2 type is '{cell2_type}', expected 'markdown'")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Cell 3 (0-indexed) is code AND content preserved (0.50 points)
    # Initially this was a markdown cell; after task it should be code with same content
    try:
        cell3_type = cells[3].get('cell_type', '')
        cell3_source = normalize_source(cells[3].get('source', []))
        expected_cell3 = normalize_source(EXPECTED_CELL3_SOURCE)

        if cell3_type == 'code':
            # Type is correct - award base points
            print(f"PASS: Component 2a -- Cell 3 is code type (0.30 pts)")
            total_score += 0.30

            # Check content preservation (only scored if type is correct)
            core_phrases = [
                "df.describe()",
                "groupby('Region')",
                "growth_rate",
                "Average profit margin"
            ]
            if cell3_source == expected_cell3:
                print(f"PASS: Component 2b -- Cell 3 content preserved exactly (0.20 pts)")
                total_score += 0.20
            else:
                matches = sum(1 for phrase in core_phrases if phrase in cell3_source)
                if matches >= 3:
                    print(f"PASS: Component 2b -- Cell 3 content mostly preserved ({matches}/4 key phrases) (0.20 pts)")
                    total_score += 0.20
                else:
                    print(f"FAIL: Component 2b -- Cell 3 content not preserved. Found {matches}/4 key phrases")
                    print(f"  Actual (first 200 chars): {cell3_source[:200]}")
        else:
            print(f"FAIL: Component 2 -- Cell 3 type is '{cell3_type}', expected 'code'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(NOTEBOOK_PATH):
    print(f"File not found: {NOTEBOOK_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(NOTEBOOK_PATH)

"""
Reward Script: PDF Document Intelligence Pipeline
Task ID: pdf_gf3_050
Domain: pdf
Scoring:
  - Component 1: doc_intelligence.py script exists and is valid Python (0.15)
  - Component 2: knowledge_graph.json exists and is valid JSON (0.15)
  - Component 3: JSON has all 6 required sections (0.20)
  - Component 4: Outline section has meaningful bookmark entries (0.15)
  - Component 5: Equations detected with math patterns (0.10)
  - Component 6: Code blocks detected (0.05)
  - Component 7: Tables detected (0.05)
  - Component 8: Figures detected (0.05)
  - Component 9: Citations detected with bracket references (0.10)
"""

import os
import json
import ast

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_050'

SCRIPT_PATH = f'{WORKDIR}/scripts/doc_intelligence.py'
JSON_PATH = f'{WORKDIR}/docs/knowledge_graph.json'
PDF_PATH = f'{WORKDIR}/docs/technical_paper.pdf'

REQUIRED_SECTIONS = ['outline', 'equations', 'code_blocks', 'tables', 'figures', 'citations']


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: source PDF must exist
    if not os.path.exists(PDF_PATH):
        print(f"CRITICAL: Source PDF not found at {PDF_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: doc_intelligence.py exists and is valid Python (0.15 points)
    try:
        if os.path.exists(SCRIPT_PATH):
            with open(SCRIPT_PATH, 'r') as f:
                script_content = f.read()
            # Verify it's valid Python by parsing the AST
            ast.parse(script_content)
            # Check it's non-trivial (at least has some imports and function defs)
            if len(script_content) > 100 and ('import' in script_content or 'def ' in script_content):
                print(f"PASS: Component 1 — doc_intelligence.py exists, valid Python, {len(script_content)} bytes (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — script too short or missing imports/functions ({len(script_content)} bytes)")
        else:
            print(f"FAIL: Component 1 — {SCRIPT_PATH} does not exist")
    except SyntaxError as e:
        print(f"FAIL: Component 1 — script has syntax error: {e}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: knowledge_graph.json exists and is valid JSON (0.15 points)
    data = None
    try:
        if os.path.exists(JSON_PATH):
            with open(JSON_PATH, 'r') as f:
                data = json.load(f)
            if isinstance(data, dict) and len(data) > 0:
                print(f"PASS: Component 2 — knowledge_graph.json exists, valid JSON with {len(data)} top-level keys (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 — JSON is not a non-empty dict")
        else:
            print(f"FAIL: Component 2 — {JSON_PATH} does not exist")
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 2 — invalid JSON: {e}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    if data is None:
        # Cannot proceed without valid JSON
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 3: JSON has all 6 required sections (0.20 points)
    try:
        present_sections = [s for s in REQUIRED_SECTIONS if s in data]
        missing_sections = [s for s in REQUIRED_SECTIONS if s not in data]
        if len(missing_sections) == 0:
            print(f"PASS: Component 3 — all 6 required sections present: {present_sections} (0.20 pts)")
            total_score += 0.20
        else:
            # Partial credit: proportional to sections found
            partial = 0.20 * (len(present_sections) / len(REQUIRED_SECTIONS))
            print(f"PARTIAL: Component 3 — {len(present_sections)}/6 sections present, missing: {missing_sections} ({partial:.2f} pts)")
            total_score += partial
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Outline section has meaningful bookmark entries (0.15 points)
    try:
        outline = data.get('outline', [])
        if isinstance(outline, list) and len(outline) >= 3:
            # Check entries have expected structure (level, title, page)
            valid_entries = 0
            for entry in outline:
                if isinstance(entry, dict):
                    has_title = 'title' in entry and isinstance(entry.get('title'), str) and len(entry.get('title', '')) > 0
                    has_page = 'page' in entry
                    has_level = 'level' in entry
                    if has_title and (has_page or has_level):
                        valid_entries += 1
            if valid_entries >= 3:
                print(f"PASS: Component 4 — outline has {valid_entries} valid bookmark entries (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — outline has only {valid_entries} valid entries (need >= 3)")
        else:
            print(f"FAIL: Component 4 — outline missing or has fewer than 3 entries (got {len(outline) if isinstance(outline, list) else 'non-list'})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Equations detected with math-like content (0.10 points)
    try:
        equations = data.get('equations', [])
        if isinstance(equations, list) and len(equations) >= 1:
            # Verify at least one equation has text content
            has_content = False
            for eq in equations:
                if isinstance(eq, dict):
                    text = str(eq.get('text', '') or eq.get('content', '') or eq.get('formula', ''))
                    if len(text) > 2:
                        has_content = True
                        break
            if has_content:
                print(f"PASS: Component 5 — {len(equations)} equations detected with content (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — equations list has items but no meaningful text content")
        else:
            print(f"FAIL: Component 5 — no equations detected (got {len(equations) if isinstance(equations, list) else 'non-list'})")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Code blocks detected (0.05 points)
    try:
        code_blocks = data.get('code_blocks', [])
        if isinstance(code_blocks, list) and len(code_blocks) >= 1:
            # Verify at least one code block has content
            has_content = False
            for cb in code_blocks:
                if isinstance(cb, dict):
                    code_text = str(cb.get('code', '') or cb.get('text', '') or cb.get('content', ''))
                    if len(code_text) > 5:
                        has_content = True
                        break
            if has_content:
                print(f"PASS: Component 6 — {len(code_blocks)} code blocks detected (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 6 — code_blocks list exists but no meaningful content")
        else:
            print(f"FAIL: Component 6 — no code blocks detected")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: Tables detected (0.05 points)
    try:
        tables = data.get('tables', [])
        if isinstance(tables, list) and len(tables) >= 1:
            # Verify at least one table has structure info
            has_structure = False
            for tbl in tables:
                if isinstance(tbl, dict):
                    has_rows = 'num_rows' in tbl or 'rows' in tbl or 'data' in tbl or 'headers' in tbl
                    has_page = 'page' in tbl
                    if has_rows or has_page:
                        has_structure = True
                        break
            if has_structure:
                print(f"PASS: Component 7 — {len(tables)} tables detected with structure info (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 7 — tables list exists but entries lack structure info")
        else:
            print(f"FAIL: Component 7 — no tables detected")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    # Component 8: Figures detected (0.05 points)
    try:
        figures = data.get('figures', [])
        if isinstance(figures, list) and len(figures) >= 1:
            # Verify at least one figure has relevant info
            has_info = False
            for fig in figures:
                if isinstance(fig, dict):
                    has_page = 'page' in fig
                    has_caption = 'caption' in fig or 'description' in fig
                    has_dims = 'width' in fig or 'height' in fig
                    if has_page or has_caption or has_dims:
                        has_info = True
                        break
            if has_info:
                print(f"PASS: Component 8 — {len(figures)} figures detected (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 8 — figures list exists but entries lack useful info")
        else:
            print(f"FAIL: Component 8 — no figures detected")
    except Exception as e:
        print(f"ERROR: Component 8 — {e}")

    # Component 9: Citations detected with bracket-style references (0.10 points)
    try:
        citations = data.get('citations', [])
        if isinstance(citations, list) and len(citations) >= 5:
            # Verify citations contain bracket-style [N] or (Author, Year) references
            bracket_count = 0
            for cit in citations:
                if isinstance(cit, dict):
                    ref_num = cit.get('reference_number', cit.get('number', ''))
                    cit_type = str(cit.get('type', ''))
                    context = str(cit.get('context', '') or cit.get('text', ''))
                    if ref_num or 'bracket' in cit_type.lower() or '[' in context:
                        bracket_count += 1
            if bracket_count >= 5:
                print(f"PASS: Component 9 — {len(citations)} citations detected, {bracket_count} with reference info (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 9 — only {bracket_count} citations with reference info (need >= 5)")
        else:
            print(f"FAIL: Component 9 — insufficient citations detected (got {len(citations) if isinstance(citations, list) else 'non-list'}, need >= 5)")
    except Exception as e:
        print(f"ERROR: Component 9 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

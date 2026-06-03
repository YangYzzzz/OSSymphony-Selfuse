"""
Reward Script: Extract Jupyter notebook code cells and create GMM report
Task ID: osworld_multi_apps_code_to_writer_file_011
Domain: libreoffice_writer (multi-app: browser, vscode, writer)
Scoring:
  Component 1: gmm_code.py on Desktop with '# Cell N — [first line]' format headers (0.40)
  Component 2: gmm_report.odt on Desktop contains summary table with cell counts (0.35)
  Component 3: gmm_report.odt mentions syntax issues section (0.25)
  Total: 1.0
"""

import os
import re

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_code_to_writer_file_011'

CODE_FILE = os.path.join(WORKDIR, 'gmm_code.py')
REPORT_FILE = os.path.join(WORKDIR, 'gmm_report.odt')


def extract_odt_text(file_path):
    """Extract all text from an ODT file using odfpy."""
    try:
        from odf.opendocument import load
        from odf.text import P
        doc = load(file_path)
        paras = doc.getElementsByType(P)
        all_text = []
        for p in paras:
            text = ''
            for node in p.childNodes:
                if node.nodeType == node.TEXT_NODE:
                    text += node.data
                elif node.nodeType == node.ELEMENT_NODE:
                    # spans and other inline elements
                    for child in node.childNodes:
                        if child.nodeType == child.TEXT_NODE:
                            text += child.data
            all_text.append(text)
        return '\n'.join(all_text)
    except Exception as e:
        print(f"ERROR: Could not extract ODT text: {e}")
        return ""


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ---- Precondition Gate ----
    # Both files must exist for meaningful verification
    code_exists = os.path.isfile(CODE_FILE)
    report_exists = os.path.isfile(REPORT_FILE)

    if not code_exists and not report_exists:
        print(f"GATE FAIL: Neither {CODE_FILE} nor {REPORT_FILE} found on Desktop.")
        print("REWARD: 0.0")
        return 0.0

    # ------------------------------------------------------------------
    # Component 1: gmm_code.py has correct '# Cell N — [first line]'
    #              header format comments (0.40 points)
    # This FAILS on initial_env (file doesn't exist) and
    # PASSES on golden_env (file has 24 properly formatted headers).
    # ------------------------------------------------------------------
    try:
        if not code_exists:
            print(f"FAIL: Component 1 — gmm_code.py not found on Desktop")
        else:
            with open(CODE_FILE, 'r', encoding='utf-8', errors='replace') as f:
                code_content = f.read()

            # Match '# Cell N — ...' where N is digits and separator is em-dash
            header_pattern = re.compile(r'^# Cell \d+ \u2014 .+$', re.MULTILINE)
            headers = header_pattern.findall(code_content)

            if len(headers) >= 5:
                # At least 5 well-formed headers means the format is correct
                print(f"PASS: Component 1 — {len(headers)} '# Cell N — ...' headers found in gmm_code.py (0.40 pts)")
                total_score += 0.40
            else:
                # Try alternative dash formats (plain hyphen, en-dash)
                alt_pattern = re.compile(r'^# Cell \d+ [-\u2013\u2014] .+$', re.MULTILINE)
                alt_headers = alt_pattern.findall(code_content)
                if len(alt_headers) >= 5:
                    print(f"PASS: Component 1 — {len(alt_headers)} '# Cell N - ...' headers found (alt dash) (0.40 pts)")
                    total_score += 0.40
                else:
                    print(f"FAIL: Component 1 — expected at least 5 '# Cell N — ...' headers, found {len(headers)} (em-dash) / {len(alt_headers)} (any dash)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ------------------------------------------------------------------
    # Component 2: gmm_report.odt contains summary with cell count
    #              information: Total cells, Code cells, Markdown cells
    #              (0.35 points)
    # This FAILS on initial_env (file doesn't exist) and
    # PASSES on golden_env (report has the summary table with counts).
    # ------------------------------------------------------------------
    try:
        if not report_exists:
            print(f"FAIL: Component 2 — gmm_report.odt not found on Desktop")
        else:
            odt_text = extract_odt_text(REPORT_FILE)
            odt_lower = odt_text.lower()

            # Check for the three required summary fields
            has_total = 'total cells' in odt_lower or 'total cell' in odt_lower
            has_code = 'code cells' in odt_lower or 'code cell' in odt_lower
            has_markdown = 'markdown cells' in odt_lower or 'markdown cell' in odt_lower

            # Check for numeric values (at least one digit > 0 near each label)
            # We look for any number in the report
            numbers_found = re.findall(r'\b(\d+)\b', odt_text)
            has_numeric = len(numbers_found) > 0

            if has_total and has_code and has_markdown and has_numeric:
                print(f"PASS: Component 2 — summary table found with Total cells, Code cells, Markdown cells and numeric values (0.35 pts)")
                total_score += 0.35
            elif (has_total or has_code or has_markdown) and has_numeric:
                # Partial: some fields present
                fields_count = sum([has_total, has_code, has_markdown])
                partial = round(0.35 * fields_count / 3, 2)
                if partial > 0:
                    print(f"PARTIAL: Component 2 — {fields_count}/3 summary fields found, partial credit {partial} pts")
                    total_score += partial
            else:
                print(f"FAIL: Component 2 — summary table missing. has_total={has_total}, has_code={has_code}, has_markdown={has_markdown}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ------------------------------------------------------------------
    # Component 3: gmm_report.odt mentions syntax issues
    #              (0.25 points)
    # This FAILS on initial_env (file doesn't exist) and
    # PASSES on golden_env (report describes '%matplotlib inline'
    # as a syntax issue / IPython magic).
    # ------------------------------------------------------------------
    try:
        if not report_exists:
            print(f"FAIL: Component 3 — gmm_report.odt not found on Desktop")
        else:
            odt_text = extract_odt_text(REPORT_FILE)
            odt_lower = odt_text.lower()

            # Syntax issues section must mention "syntax" and either:
            # - "issue" / "error" / "problem"  AND reference to something like magic, matplotlib, or 'none'
            has_syntax = 'syntax' in odt_lower
            has_issue_keyword = any(kw in odt_lower for kw in ['issue', 'error', 'problem', 'invalid', 'none'])

            if has_syntax and has_issue_keyword:
                print(f"PASS: Component 3 — syntax issues section found in gmm_report.odt (0.25 pts)")
                total_score += 0.25
            elif has_syntax:
                # Partial: mentions syntax but not with enough context
                print(f"PARTIAL: Component 3 — 'syntax' mentioned but no issue/error/none keyword; awarding 0.10 pts")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 — no syntax issues section found in gmm_report.odt")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: verify Desktop files on the VM
verify_task()

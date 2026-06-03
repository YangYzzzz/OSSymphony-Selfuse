"""
Reward Script: GDPR PDF Compliance Scanner
Task ID: pdf_gf3_048
Domain: pdf
Scoring:
  C1 (0.15): gdpr_scanner.py exists and is a valid Python file
  C2 (0.15): Script runs without errors and produces output
  C3 (0.15): Script source defines regex patterns for all 6 personal data types
  C4 (0.20): gdpr_report.json exists, is valid JSON, has correct top-level structure
  C5 (0.15): Each finding has required keys (filename, page, pattern_type, masked_preview)
  C6 (0.20): Report covers all 6 categories with non-zero counts
"""

import os
import json
import re
import ast

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_048'

SCRIPT_PATH = f'{WORKDIR}/scripts/gdpr_scanner.py'
REPORT_PATH = f'{WORKDIR}/scan/gdpr_report.json'

REQUIRED_CATEGORIES = {
    'email', 'phone', 'postal', 'date', 'iban', 'ip'
}


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: gdpr_scanner.py exists and is a valid Python file (0.15 pts)
    try:
        if os.path.isfile(SCRIPT_PATH):
            with open(SCRIPT_PATH, 'r') as f:
                source_code = f.read()
            # Verify it's valid Python by parsing the AST
            ast.parse(source_code)
            if len(source_code) > 100:
                print(f"PASS: Component 1 — gdpr_scanner.py exists and is valid Python ({len(source_code)} chars) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — Script is too short ({len(source_code)} chars), likely incomplete")
        else:
            print(f"FAIL: Component 1 — {SCRIPT_PATH} does not exist")
            source_code = None
    except SyntaxError as e:
        print(f"FAIL: Component 1 — Script has syntax error: {e}")
        source_code = None
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        source_code = None

    # Component 2: Script runs without errors (0.15 pts)
    # We test this by checking if executing it would succeed — but since we cannot use
    # subprocess, we check for key imports and callable main structure
    try:
        if source_code:
            # Check that the script imports necessary modules and has a main-like structure
            has_pymupdf_import = ('pymupdf' in source_code or 'fitz' in source_code)
            has_re_import = ('import re' in source_code or 'from re' in source_code)
            has_json_import = ('import json' in source_code or 'from json' in source_code)
            has_scan_logic = ('get_text' in source_code or 'extract_text' in source_code or
                              'page.get_text' in source_code or 'extract' in source_code)

            if has_pymupdf_import and has_re_import and has_json_import and has_scan_logic:
                print(f"PASS: Component 2 — Script imports pymupdf/fitz, re, json and has text extraction logic (0.15 pts)")
                total_score += 0.15
            else:
                missing = []
                if not has_pymupdf_import:
                    missing.append('pymupdf/fitz import')
                if not has_re_import:
                    missing.append('re import')
                if not has_json_import:
                    missing.append('json import')
                if not has_scan_logic:
                    missing.append('text extraction (get_text/extract)')
                print(f"FAIL: Component 2 — Script missing: {', '.join(missing)}")
        else:
            print(f"FAIL: Component 2 — No valid script to check")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Script defines regex patterns for all 6 data types (0.15 pts)
    try:
        if source_code:
            pattern_keywords = {
                'email': [r'email', r'@.*\\.'],
                'phone': [r'phone', r'\\\+'],
                'postal': [r'postal', r'postcode', r'zip'],
                'date_of_birth': [r'dob', r'date.?of.?birth', r'born'],
                'iban': [r'iban', r'\[A-Z\]\{2\}'],
                'ip_address': [r'ip.?addr', r'25\[0-5\]', r'\d+\\\.\d+'],
            }
            source_lower = source_code.lower()
            found_categories = 0
            for cat, keywords in pattern_keywords.items():
                for kw in keywords:
                    if re.search(kw, source_lower):
                        found_categories += 1
                        break

            if found_categories >= 6:
                print(f"PASS: Component 3 — All 6 pattern types defined ({found_categories}/6) (0.15 pts)")
                total_score += 0.15
            elif found_categories >= 4:
                partial = round(0.15 * found_categories / 6, 3)
                print(f"PARTIAL: Component 3 — {found_categories}/6 pattern types defined ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — Only {found_categories}/6 pattern types found")
        else:
            print(f"FAIL: Component 3 — No valid script to check")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: gdpr_report.json exists, is valid JSON, has correct structure (0.20 pts)
    report_data = None
    try:
        if os.path.isfile(REPORT_PATH):
            with open(REPORT_PATH, 'r') as f:
                report_data = json.load(f)

            # Check top-level structure
            has_findings = 'findings' in report_data and isinstance(report_data['findings'], list)
            has_summary = 'summary' in report_data and isinstance(report_data['summary'], dict)

            if has_findings and has_summary:
                print(f"PASS: Component 4 — gdpr_report.json is valid JSON with findings ({len(report_data['findings'])}) and summary (0.20 pts)")
                total_score += 0.20
            elif has_findings:
                print(f"PARTIAL: Component 4 — Has findings but missing summary structure (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 4 — Missing required top-level keys (findings, summary)")
        else:
            print(f"FAIL: Component 4 — {REPORT_PATH} does not exist")
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 4 — gdpr_report.json is not valid JSON: {e}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Each finding has required keys (0.15 pts)
    try:
        if report_data and 'findings' in report_data and len(report_data['findings']) > 0:
            required_keys = {'filename', 'page', 'pattern_type', 'masked_preview'}
            total_findings = len(report_data['findings'])
            valid_findings = 0
            for finding in report_data['findings']:
                if isinstance(finding, dict) and required_keys.issubset(finding.keys()):
                    # Also check that values are sensible
                    if (isinstance(finding['filename'], str) and finding['filename'].endswith('.pdf') and
                            isinstance(finding['page'], int) and finding['page'] >= 1 and
                            isinstance(finding['pattern_type'], str) and len(finding['pattern_type']) > 0 and
                            isinstance(finding['masked_preview'], str) and len(finding['masked_preview']) > 0):
                        valid_findings += 1

            ratio = valid_findings / total_findings if total_findings > 0 else 0
            if ratio >= 0.9:
                print(f"PASS: Component 5 — {valid_findings}/{total_findings} findings have correct structure (0.15 pts)")
                total_score += 0.15
            elif ratio >= 0.5:
                partial = round(0.15 * ratio, 3)
                print(f"PARTIAL: Component 5 — {valid_findings}/{total_findings} findings valid ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 5 — Only {valid_findings}/{total_findings} findings have correct structure")
        else:
            print(f"FAIL: Component 5 — No findings in report to validate")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Report covers all 6 categories with non-zero counts (0.20 pts)
    try:
        if report_data and 'findings' in report_data and len(report_data['findings']) > 0:
            # Extract categories from findings
            found_types = set()
            for finding in report_data['findings']:
                if isinstance(finding, dict) and 'pattern_type' in finding:
                    pt = finding['pattern_type'].lower()
                    # Map to canonical categories
                    for canon in REQUIRED_CATEGORIES:
                        if canon in pt:
                            found_types.add(canon)

            # Also check the summary if available
            if 'summary' in report_data:
                summary = report_data['summary']
                cats = summary.get('findings_by_category', summary)
                if isinstance(cats, dict):
                    for key in cats:
                        key_lower = key.lower()
                        for canon in REQUIRED_CATEGORIES:
                            if canon in key_lower:
                                found_types.add(canon)

            if len(found_types) >= 6:
                print(f"PASS: Component 6 — All 6 categories found: {sorted(found_types)} (0.20 pts)")
                total_score += 0.20
            elif len(found_types) >= 4:
                partial = round(0.20 * len(found_types) / 6, 3)
                missing = REQUIRED_CATEGORIES - found_types
                print(f"PARTIAL: Component 6 — {len(found_types)}/6 categories, missing: {missing} ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 6 — Only {len(found_types)}/6 categories found: {sorted(found_types)}")
        else:
            print(f"FAIL: Component 6 — No findings to check categories")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

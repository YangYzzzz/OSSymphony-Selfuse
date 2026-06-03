"""
Reward Script: PDF Security Audit Tool Verification
Task ID: pdf_gf3_030
Domain: pdf (libreoffice_calc listed but task is actually pdf/scripting)
Scoring:
  Component 1: Script exists and is valid Python (0.15)
  Component 2: Security report JSON exists and is valid with structure (0.15)
  Component 3: Encryption section correct (0.15)
  Component 4: Permissions section correct (0.15)
  Component 5: JavaScript detection section present (0.10)
  Component 6: Embedded files section correct (0.10)
  Component 7: External URLs section present (0.10)
  Component 8: Metadata section correct (0.10)
"""

import os
import json
import ast

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_030'

SCRIPT_PATH = f'{WORKDIR}/scripts/pdf_security_audit.py'
REPORT_PATH = f'{WORKDIR}/audit/security_report.json'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Script exists and is valid Python (0.15 points)
    try:
        if os.path.exists(SCRIPT_PATH):
            with open(SCRIPT_PATH, 'r') as f:
                script_content = f.read()
            # Verify it is valid Python by parsing the AST
            ast.parse(script_content)
            # Check it contains relevant security audit logic (not just an empty file)
            has_fitz_or_pikepdf = ('fitz' in script_content or 'pymupdf' in script_content.lower()
                                   or 'pikepdf' in script_content)
            has_json_output = 'json' in script_content
            if has_fitz_or_pikepdf and has_json_output:
                print(f"PASS: Component 1 — Script exists, valid Python, uses PDF libs and JSON (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — Script exists but missing PDF library usage or JSON output")
        else:
            print(f"FAIL: Component 1 — Script not found at {SCRIPT_PATH}")
    except SyntaxError as e:
        print(f"FAIL: Component 1 — Script has syntax errors: {e}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Security report JSON exists and is valid with expected structure (0.15 points)
    report = None
    try:
        if os.path.exists(REPORT_PATH):
            with open(REPORT_PATH, 'r') as f:
                report = json.load(f)
            # Check for expected top-level structure
            # Report should have sections for the various security checks
            # Accept flexible structure: look for key security sections anywhere in the JSON
            report_str = json.dumps(report).lower()
            has_encryption_key = 'encrypt' in report_str
            has_permissions_key = 'permission' in report_str
            has_metadata_key = 'metadata' in report_str
            if has_encryption_key and has_permissions_key and has_metadata_key:
                print(f"PASS: Component 2 — Report is valid JSON with security sections (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 — Report JSON missing required sections. "
                      f"encryption={has_encryption_key}, permissions={has_permissions_key}, metadata={has_metadata_key}")
        else:
            print(f"FAIL: Component 2 — Report not found at {REPORT_PATH}")
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 2 — Report is not valid JSON: {e}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    if report is None:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Helper: navigate report flexibly (could be nested under 'analysis_sections' or flat)
    def get_section(report, key_variants):
        """Search for a section in the report by trying multiple key paths."""
        # Try direct top-level
        for key in key_variants:
            if key in report:
                return report[key]
        # Try under 'analysis_sections'
        if 'analysis_sections' in report:
            sections = report['analysis_sections']
            for key in key_variants:
                if key in sections:
                    return sections[key]
        # Try under 'sections'
        if 'sections' in report:
            sections = report['sections']
            for key in key_variants:
                if key in sections:
                    return sections[key]
        # Try under 'results'
        if 'results' in report:
            sections = report['results']
            for key in key_variants:
                if key in sections:
                    return sections[key]
        return None

    # Component 3: Encryption section with correct data (0.15 points)
    try:
        enc = get_section(report, ['encryption', 'encryption_info', 'encryption_analysis'])
        if enc is not None:
            enc_str = json.dumps(enc).lower()
            # Should detect encryption and report algorithm type and key length
            has_algo = ('aes' in enc_str or 'rc4' in enc_str or 'algorithm' in enc_str)
            has_key_length = ('256' in enc_str or '128' in enc_str or 'key_length' in enc_str
                             or 'key_size' in enc_str or 'keylength' in enc_str)
            has_encrypted_flag = ('encrypted' in enc_str or 'is_encrypted' in enc_str)
            if has_algo and has_key_length and has_encrypted_flag:
                print(f"PASS: Component 3 — Encryption section has algorithm, key length, encrypted status (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — Encryption section incomplete. "
                      f"algo={has_algo}, key_length={has_key_length}, encrypted={has_encrypted_flag}")
        else:
            print(f"FAIL: Component 3 — No encryption section found in report")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Permissions section with flags (0.15 points)
    try:
        perms = get_section(report, ['permissions', 'permission_flags', 'permissions_info'])
        if perms is not None:
            perms_str = json.dumps(perms).lower()
            # Should have permission flags for print, copy, modify, etc.
            has_print = 'print' in perms_str
            has_copy_or_extract = ('copy' in perms_str or 'extract' in perms_str)
            has_modify = 'modify' in perms_str or 'edit' in perms_str
            if has_print and has_copy_or_extract and has_modify:
                print(f"PASS: Component 4 — Permissions section has print, copy/extract, modify flags (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — Permissions section incomplete. "
                      f"print={has_print}, copy/extract={has_copy_or_extract}, modify={has_modify}")
        else:
            print(f"FAIL: Component 4 — No permissions section found in report")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: JavaScript detection section (0.10 points)
    try:
        js = get_section(report, ['javascript', 'javascript_analysis', 'js', 'javascript_detection'])
        if js is not None:
            js_str = json.dumps(js).lower()
            # Should indicate whether JavaScript was found
            has_js_indicator = ('has_javascript' in js_str or 'javascript' in js_str
                               or 'found' in js_str or 'detected' in js_str
                               or 'count' in js_str)
            if has_js_indicator:
                print(f"PASS: Component 5 — JavaScript detection section present (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — JavaScript section exists but lacks detection indicators")
        else:
            print(f"FAIL: Component 5 — No JavaScript section found in report")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Embedded files section with file listings (0.10 points)
    try:
        emb = get_section(report, ['embedded_files', 'attachments', 'embedded_files_analysis'])
        if emb is not None:
            emb_str = json.dumps(emb).lower()
            # Should list embedded files (we know there are 2: remediation_timeline.txt and scan_results.csv)
            has_files_list = ('files' in emb_str or 'attachments' in emb_str or 'name' in emb_str)
            has_specific_files = ('remediation_timeline' in emb_str or 'scan_results' in emb_str)
            if has_files_list and has_specific_files:
                print(f"PASS: Component 6 — Embedded files section lists actual embedded files (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 6 — Embedded files section incomplete. "
                      f"has_list={has_files_list}, has_specific={has_specific_files}")
        else:
            print(f"FAIL: Component 6 — No embedded files section found in report")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: External URLs section (0.10 points)
    try:
        urls = get_section(report, ['external_urls', 'urls', 'links', 'url_analysis', 'external_links'])
        if urls is not None:
            urls_str = json.dumps(urls).lower()
            # Should list external URLs found in the document
            has_url_list = ('url' in urls_str or 'http' in urls_str or 'link' in urls_str)
            has_specific_url = ('cybershield' in urls_str or 'owasp' in urls_str
                               or 'nvd.nist.gov' in urls_str or 'pcisecurity' in urls_str)
            if has_url_list and has_specific_url:
                print(f"PASS: Component 7 — External URLs section lists actual URLs (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 7 — URLs section incomplete. "
                      f"has_urls={has_url_list}, has_specific={has_specific_url}")
        else:
            print(f"FAIL: Component 7 — No external URLs section found in report")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    # Component 8: Metadata section with author/creator/producer (0.10 points)
    try:
        meta = get_section(report, ['metadata', 'document_metadata', 'metadata_info'])
        if meta is not None:
            meta_str = json.dumps(meta).lower()
            # Should report author, creator, producer from the PDF metadata
            has_author = ('author' in meta_str or 'vasquez' in meta_str or 'elena' in meta_str)
            has_creator = ('creator' in meta_str or 'cybershield' in meta_str)
            has_producer = ('producer' in meta_str)
            if has_author and has_creator:
                print(f"PASS: Component 8 — Metadata section has author and creator info (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 8 — Metadata section incomplete. "
                      f"author={has_author}, creator={has_creator}, producer={has_producer}")
        else:
            print(f"FAIL: Component 8 — No metadata section found in report")
    except Exception as e:
        print(f"ERROR: Component 8 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

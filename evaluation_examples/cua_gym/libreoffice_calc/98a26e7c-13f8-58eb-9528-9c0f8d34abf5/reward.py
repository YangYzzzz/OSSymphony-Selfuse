"""
Reward Script: Fix RSS feed parser to handle malformed XML gracefully
Task ID: osworld_multi_apps_vscode_debug_crash_011
Domain: vscode / python code editing
Scoring:
  Component 1 (0.4): parse_feeds has try/except for ET.ParseError around parse_feed call
  Component 2 (0.3): malformed URLs are collected and printed in an error summary
  Component 3 (0.3): behavioral test - parse_feeds skips malformed feeds, returns valid items
"""

import os
import sys
import re
import importlib.util
import uuid

WORKDIR = '/home/user/Desktop/rss_reader'
TASK_ID = 'osworld_multi_apps_vscode_debug_crash_011'

PARSER_PATH = os.path.join(WORKDIR, 'parser.py')


def verify_task():
    """
    Verify that parser.py has been fixed to handle malformed XML:
      1. try/except ET.ParseError wraps parse_feed() call in parse_feeds()
      2. Malformed URLs are collected and printed in error summary
      3. Behavioral: parse_feeds skips malformed feed, returns valid items
    Returns a float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: parser.py must exist
    if not os.path.isfile(PARSER_PATH):
        print(f"CRITICAL: parser.py not found at {PARSER_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Read the source code for static analysis
    try:
        with open(PARSER_PATH, 'r') as f:
            source = f.read()
    except Exception as e:
        print(f"CRITICAL: Could not read parser.py: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: parse_feeds function contains a try/except for ET.ParseError (0.4 points)
    # The fix requires catching xml.etree.ElementTree.ParseError around parse_feed() calls
    try:
        # Look for 'except' clause catching ParseError
        parse_error_except = re.search(
            r'except\s+(ET\.ParseError|xml\.etree\.ElementTree\.ParseError)',
            source
        )

        # Find the parse_feeds function body (from def to next def or end of file)
        parse_feeds_match = re.search(
            r'def parse_feeds\s*\(.*?\).*?(?=\ndef |\Z)',
            source,
            re.DOTALL
        )

        feeds_body = parse_feeds_match.group(0) if parse_feeds_match else ""
        component1_pass = (parse_feeds_match is not None and
                           parse_error_except is not None and
                           'try:' in feeds_body and
                           'parse_feed(' in feeds_body)
        if component1_pass:
            print("PASS: Component 1 — try/except ET.ParseError wraps parse_feed() in parse_feeds() (0.4 pts)")
            total_score += 0.4
        else:
            print("FAIL: Component 1 — No try/except ET.ParseError found wrapping parse_feed() inside parse_feeds()")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: malformed URLs are collected and printed in error summary (0.3 points)
    # Task requires: malformed feed URLs are reported in a summary section
    try:
        # Check for a list variable being appended with url on ParseError
        malformed_append_match = re.search(
            r'(malformed[_\w]*|error[_\w]*urls?|failed[_\w]*urls?)\s*\.\s*append\s*\(\s*url\s*\)',
            source
        )

        # Check for printing an error summary mentioning "summary" or "malformed" or "Error Summary"
        summary_print_match = re.search(
            r'print\s*\(.*?(summary|[Mm]alformed|[Ee]rror\s+[Ss]ummary).*?\)',
            source
        )

        if malformed_append_match and summary_print_match:
            print("PASS: Component 2 — malformed URLs collected and printed in error summary (0.3 pts)")
            total_score += 0.3
        elif malformed_append_match and not summary_print_match:
            print("FAIL: Component 2 — malformed URLs collected but error summary not printed")
        elif summary_print_match and not malformed_append_match:
            print("FAIL: Component 2 — error summary print found but malformed URL collection missing")
        else:
            print("FAIL: Component 2 — no malformed URL collection or error summary printing found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Behavioral test — parse_feeds handles mixed valid/malformed input (0.3 points)
    # Import parser module and call parse_feeds with one malformed and one valid feed
    try:
        module_name = f"parser_{uuid.uuid4().hex[:8]}"
        original_cwd = os.getcwd()
        original_path = sys.path.copy()

        try:
            os.chdir(WORKDIR)
            if WORKDIR not in sys.path:
                sys.path.insert(0, WORKDIR)

            spec = importlib.util.spec_from_file_location(module_name, PARSER_PATH)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            # Test input: one valid RSS feed and one malformed XML
            valid_rss = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Test Feed</title>
    <item>
      <title>Item 1</title>
      <link>http://example.com/1</link>
      <description>Description 1</description>
    </item>
  </channel>
</rss>"""
            # Malformed: closing tags in wrong order
            malformed_xml = "<rss><channel><item><title>Broken</title></channel></item></rss>"

            test_input = {
                "http://valid.example.com/feed": valid_rss,
                "http://broken.example.com/feed": malformed_xml,
            }

            # Capture stdout to suppress the error summary during testing
            import io
            from contextlib import redirect_stdout
            captured = io.StringIO()
            with redirect_stdout(captured):
                results = module.parse_feeds(test_input)

            # Verify: valid feed returns items, malformed feed returns empty list (not exception)
            valid_items = results.get("http://valid.example.com/feed", None)
            broken_items = results.get("http://broken.example.com/feed", None)

            component3_pass = (valid_items is not None and len(valid_items) == 1 and
                               broken_items is not None and isinstance(broken_items, list) and
                               len(broken_items) == 0)
            if component3_pass:
                print("PASS: Component 3 — parse_feeds returns valid items for good feed, empty list for malformed (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — unexpected behavior: valid_items={valid_items}, broken_items={broken_items}")

        finally:
            if module_name in sys.modules:
                del sys.modules[module_name]
            os.chdir(original_cwd)
            sys.path[:] = original_path

    except Exception as e:
        print(f"ERROR: Component 3 — behavioral test raised exception: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

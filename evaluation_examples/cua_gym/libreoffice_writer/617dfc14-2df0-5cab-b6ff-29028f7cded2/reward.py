"""
Reward Script: Transfer experiment data from ODS to Writer document with journal formatting
Task ID: osworld_multi_apps_doc_calc_to_writer_012
Domain: libreoffice_writer
Scoring:
  Component 1: results_section.odt exists and is readable (gate + 0.1 pts)
  Component 2: H1 heading 'Results' present (0.15 pts)
  Component 3: 3 tables with correct column headers including units (0.30 pts)
  Component 4: Table captions: 'Table 1/2/3. ...' present (0.20 pts)
  Component 5: Footnote '* p < 0.05' after each table (0.15 pts)
  Component 6: Narrative paragraph referencing Table 1, Table 2, Table 3 (0.10 pts)
  Total: 1.0
"""

import os
import zipfile
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_doc_calc_to_writer_012'
TARGET_FILE = '/home/user/Documents/results_section.odt'


def get_odt_content_xml(odt_path):
    """Extract content.xml from an ODT file."""
    with zipfile.ZipFile(odt_path, 'r') as z:
        return z.read('content.xml').decode('utf-8')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: File exists and is readable (0.1 pts)
    # This acts as gate — all further checks depend on it
    content_xml = None
    try:
        content_xml = get_odt_content_xml(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot read ODT file {file_path}: {e}")

    if content_xml is None:
        print("FAIL: results_section.odt not readable")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # File is readable — award file existence points
    if content_xml is not None:
        print("PASS: results_section.odt exists and is readable (0.1 pts)")
        total_score += 0.1

    # Pre-compute plain text (stripped of XML tags) for text searches
    plain_text = re.sub(r'<[^>]+>', ' ', content_xml)
    plain_text = re.sub(r'\s+', ' ', plain_text)

    # Component 2: H1 heading 'Results' present (0.15 pts)
    try:
        h1_matches = re.findall(
            r'<text:h[^>]*text:outline-level="1"[^>]*>(.*?)</text:h>',
            content_xml,
            re.DOTALL
        )
        h1_texts = [re.sub(r'<[^>]+>', '', h).strip() for h in h1_matches]
        if any('Results' in h for h in h1_texts):
            print(f"PASS: H1 heading 'Results' found (0.15 pts). H1 headings: {h1_texts}")
            total_score += 0.15
        else:
            print(f"FAIL: H1 heading 'Results' not found. H1 headings found: {h1_texts}")
    except Exception as e:
        print(f"ERROR: Component 2 (heading check) — {e}")

    # Component 3: 3 tables with correct column headers including units (0.30 pts)
    # Expected headers: Sample_ID, Measurement_1 (mg/mL), Measurement_2 (units), p_value, Significant (*p<0.05)
    try:
        table_count = len(re.findall(r'<table:table\s', content_xml))
        has_3_tables = table_count >= 3
        has_m1_units = 'Measurement_1 (mg/mL)' in plain_text
        has_m2_units = 'Measurement_2 (units)' in plain_text
        has_sample_id = 'Sample_ID' in plain_text
        has_p_value = 'p_value' in plain_text
        # Check for Significant (*p<0.05) — in XML encoded as &lt;
        has_significant = ('Significant (*p&lt;0.05)' in content_xml or
                           'Significant (*p<0.05)' in plain_text)

        headers_score = 0.0
        if has_3_tables:
            headers_score += 0.10
            print(f"PASS: {table_count} tables found (0.10 pts)")
        else:
            print(f"FAIL: Expected 3 tables, found {table_count}")

        if has_m1_units:
            headers_score += 0.05
            print("PASS: Column header 'Measurement_1 (mg/mL)' found (0.05 pts)")
        else:
            print("FAIL: Column header 'Measurement_1 (mg/mL)' not found")

        if has_m2_units:
            headers_score += 0.05
            print("PASS: Column header 'Measurement_2 (units)' found (0.05 pts)")
        else:
            print("FAIL: Column header 'Measurement_2 (units)' not found")

        if has_sample_id and has_p_value:
            headers_score += 0.05
            print("PASS: Column headers 'Sample_ID' and 'p_value' found (0.05 pts)")
        else:
            print(f"FAIL: Missing column headers (Sample_ID={has_sample_id}, p_value={has_p_value})")

        if has_significant:
            headers_score += 0.05
            print("PASS: Column header 'Significant (*p<0.05)' found (0.05 pts)")
        else:
            print("FAIL: Column header 'Significant (*p<0.05)' not found")

        if headers_score > 0:
            total_score += headers_score
        print(f"Component 3 subtotal: {headers_score}/0.30")
    except Exception as e:
        print(f"ERROR: Component 3 (table/header check) — {e}")

    # Component 4: Table captions in correct format (0.20 pts)
    # Expected: 'Table 1. Treatment A Results (n=20)', 'Table 2. Treatment B Results (n=20)', 'Table 3. Control Results (n=10)'
    try:
        caption1_found = bool(re.search(r'Table\s+1\.\s+Treatment\s+A\s+Results\s*\(n=20\)', plain_text))
        caption2_found = bool(re.search(r'Table\s+2\.\s+Treatment\s+B\s+Results\s*\(n=20\)', plain_text))
        caption3_found = bool(re.search(r'Table\s+3\.\s+Control\s+Results\s*\(n=10\)', plain_text))

        captions_found = sum([caption1_found, caption2_found, caption3_found])
        caption_score = round(captions_found * (0.20 / 3), 4)

        if caption1_found:
            print("PASS: Caption 'Table 1. Treatment A Results (n=20)' found")
        else:
            print("FAIL: Caption 'Table 1. Treatment A Results (n=20)' not found")
        if caption2_found:
            print("PASS: Caption 'Table 2. Treatment B Results (n=20)' found")
        else:
            print("FAIL: Caption 'Table 2. Treatment B Results (n=20)' not found")
        if caption3_found:
            print("PASS: Caption 'Table 3. Control Results (n=10)' found")
        else:
            print("FAIL: Caption 'Table 3. Control Results (n=10)' not found")

        if caption_score > 0:
            total_score += caption_score
        print(f"Component 4 subtotal: {caption_score}/0.20 ({captions_found}/3 captions)")
    except Exception as e:
        print(f"ERROR: Component 4 (caption check) — {e}")

    # Component 5: Footnote '* p < 0.05' present after each table (0.15 pts)
    # In golden file: 3 occurrences, one per table, rendered as italic text
    try:
        # In ODT XML, < is encoded as &lt;
        footnote_count_xml = len(re.findall(r'\*\s*p\s*&lt;\s*0\.05', content_xml))
        # Also check plain text
        footnote_count_plain = len(re.findall(r'\*\s*p\s*<\s*0\.05', plain_text))
        footnote_count = max(footnote_count_xml, footnote_count_plain)

        if footnote_count >= 3:
            print(f"PASS: Footnote '* p < 0.05' found {footnote_count} times (0.15 pts)")
            total_score += 0.15
        elif footnote_count == 2:
            print(f"PARTIAL: Footnote '* p < 0.05' found {footnote_count}/3 times (0.10 pts)")
            total_score += 0.10
        elif footnote_count == 1:
            print(f"PARTIAL: Footnote '* p < 0.05' found {footnote_count}/3 times (0.05 pts)")
            total_score += 0.05
        else:
            print("FAIL: Footnote '* p < 0.05' not found")
    except Exception as e:
        print(f"ERROR: Component 5 (footnote check) — {e}")

    # Component 6: Narrative paragraph referencing all 3 tables (0.10 pts)
    # Expected: "Table 1 shows...", "Table 2 shows...", "Compared to the control (Table 3)..."
    try:
        has_table1_ref = bool(re.search(r'Table\s+1\s+shows', plain_text))
        has_table2_ref = bool(re.search(r'Table\s+2\s+shows', plain_text))
        has_table3_ref = bool(
            re.search(r'Table\s+3', plain_text) and re.search(r'[Cc]ontrol', plain_text)
        )

        narrative_refs = sum([has_table1_ref, has_table2_ref, has_table3_ref])
        narrative_score = round(narrative_refs * (0.10 / 3), 4)

        if has_table1_ref:
            print("PASS: Narrative contains 'Table 1 shows'")
        else:
            print("FAIL: Narrative missing 'Table 1 shows'")
        if has_table2_ref:
            print("PASS: Narrative contains 'Table 2 shows'")
        else:
            print("FAIL: Narrative missing 'Table 2 shows'")
        if has_table3_ref:
            print("PASS: Narrative references 'Table 3' with 'control'")
        else:
            print("FAIL: Narrative missing 'Table 3' reference with 'control'")

        if narrative_score > 0:
            total_score += narrative_score
        print(f"Component 6 subtotal: {narrative_score}/0.10 ({narrative_refs}/3 references)")
    except Exception as e:
        print(f"ERROR: Component 6 (narrative check) — {e}")

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {total_score:.4f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(TARGET_FILE):
    print(f"File not found: {TARGET_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(TARGET_FILE)

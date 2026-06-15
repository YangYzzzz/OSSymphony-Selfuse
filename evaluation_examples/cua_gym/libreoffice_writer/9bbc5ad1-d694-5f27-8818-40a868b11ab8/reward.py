"""
Reward Script: Conditional text with user variable in LibreOffice Writer
Task ID: writer_rd_073
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35): User variable 'audience' exists with value 'internal'
  Component 2 (0.35): Conditional text field exists in header
  Component 3 (0.30): Conditional text has correct condition and then/else values
"""

import os
import zipfile
from xml.etree import ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_rd_073'

# ODF namespaces
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
    'fo': 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
    'ooow': 'http://openoffice.org/2004/writer',
}


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the ODT file (ZIP archive)
    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open ODT file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse content.xml and styles.xml
    try:
        content_xml = zf.read('content.xml').decode('utf-8')
        content_tree = ET.fromstring(content_xml)
    except Exception as e:
        print(f"CRITICAL: Cannot parse content.xml: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        styles_xml = zf.read('styles.xml').decode('utf-8')
        styles_tree = ET.fromstring(styles_xml)
    except Exception as e:
        print(f"CRITICAL: Cannot parse styles.xml: {e}")
        print("REWARD: 0.0")
        return 0.0

    zf.close()

    # Component 1: User variable 'audience' exists with value 'internal' (0.35 points)
    # In ODF, user fields are declared in content.xml under text:user-field-decls
    try:
        user_field_decls = content_tree.findall('.//text:user-field-decl', NS)
        audience_field = None
        for field in user_field_decls:
            name = field.get('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}name', '')
            if name.lower() == 'audience':
                audience_field = field
                break

        if audience_field is not None:
            # Check value - could be in office:string-value or office:value
            str_val = audience_field.get('{urn:oasis:names:tc:opendocument:xmlns:office:1.0}string-value', '')
            if str_val.lower() == 'internal':
                print(f"PASS: Component 1 — User variable 'audience' found with value 'internal' (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 1 — User variable 'audience' found but value is '{str_val}', expected 'internal'")
        else:
            print(f"FAIL: Component 1 — No user variable named 'audience' found in content.xml")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Conditional text field exists in the header (0.35 points)
    # In ODF, the header is in styles.xml under office:master-styles > style:master-page > style:header
    try:
        # Find all conditional-text elements in the header section of styles.xml
        headers = styles_tree.findall('.//style:master-page/style:header', NS)
        cond_text_in_header = []
        for header in headers:
            conds = header.findall('.//text:conditional-text', NS)
            cond_text_in_header.extend(conds)

        if len(cond_text_in_header) > 0:
            print(f"PASS: Component 2 — Conditional text field found in header ({len(cond_text_in_header)} instance(s)) (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — No conditional text field found in any header")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Conditional text has correct condition and then/else values (0.30 points)
    # The condition should reference 'audience' and compare to 'internal'
    # Then value: 'Internal Use Only', Else value: 'Public Release'
    try:
        if len(cond_text_in_header) > 0:
            ct = cond_text_in_header[0]
            condition = ct.get('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}condition', '')
            then_val = ct.get('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}string-value-if-true', '')
            else_val = ct.get('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}string-value-if-false', '')

            sub_score = 0.0
            # Check condition references audience and internal
            cond_lower = condition.lower()
            if 'audience' in cond_lower and 'internal' in cond_lower:
                sub_score += 0.10
                print(f"  PASS: Condition references audience/internal: '{condition}'")
            else:
                print(f"  FAIL: Condition does not reference audience/internal: '{condition}'")

            # Check 'then' value
            if then_val.strip().lower() == 'internal use only':
                sub_score += 0.10
                print(f"  PASS: Then value is '{then_val}'")
            else:
                print(f"  FAIL: Then value is '{then_val}', expected 'Internal Use Only'")

            # Check 'else' value
            if else_val.strip().lower() == 'public release':
                sub_score += 0.10
                print(f"  PASS: Else value is '{else_val}'")
            else:
                print(f"  FAIL: Else value is '{else_val}', expected 'Public Release'")

            if sub_score > 0:
                print(f"PASS: Component 3 — Conditional text properties verified ({sub_score} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 3 — No conditional text sub-checks passed")
        else:
            print(f"FAIL: Component 3 — No conditional text field to verify (depends on Component 2)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.odt'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

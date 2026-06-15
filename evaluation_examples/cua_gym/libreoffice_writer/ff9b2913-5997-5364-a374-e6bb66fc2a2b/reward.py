"""
Reward Script: Create an AutoText entry with a date field
Task ID: writer_frd_048
Domain: libreoffice_writer
Scoring:
  Component 1 (0.30): A .bau file with a 'ReportDate' section exists in autotext dirs
  Component 2 (0.35): The ReportDate section contains 'Report Date: ' static text
  Component 3 (0.35): The ReportDate section contains a dynamic date field
"""

import os
import glob
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_frd_048'

# LibreOffice AutoText directories where .bau files may reside
AUTOTEXT_DIRS = [
    os.path.expanduser('~/.config/libreoffice/user/autotext'),
    os.path.expanduser('~/.config/libreoffice/4/user/autotext'),
    '/usr/share/libreoffice/share/autotext',
]


def find_bau_with_reportdate():
    """
    Search all known autotext directories for .bau files that contain
    a section named 'ReportDate'. Returns (bau_path, content_xml_str) or (None, None).
    """
    for d in AUTOTEXT_DIRS:
        if not os.path.isdir(d):
            continue
        for bau_path in glob.glob(os.path.join(d, '*.bau')):
            try:
                zf = zipfile.ZipFile(bau_path, 'r')
                names = zf.namelist()

                # Approach 1: Check content.xml for <text:section text:name="ReportDate">
                if 'content.xml' in names:
                    content = zf.read('content.xml').decode('utf-8', errors='replace')
                    if 'ReportDate' in content:
                        zf.close()
                        return bau_path, content

                # Approach 2: Check BlockList.xml for a block named ReportDate
                if 'BlockList.xml' in names:
                    bl = zf.read('BlockList.xml').decode('utf-8', errors='replace')
                    if 'ReportDate' in bl:
                        # Also try to get content.xml
                        content = ''
                        if 'content.xml' in names:
                            content = zf.read('content.xml').decode('utf-8', errors='replace')
                        zf.close()
                        return bau_path, content

                zf.close()
            except Exception:
                continue
    return None, None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    bau_path, content_xml = find_bau_with_reportdate()

    # Component 1: A .bau file with 'ReportDate' section exists (0.30 points)
    try:
        if bau_path is not None:
            print(f"PASS: Component 1 — Found .bau with ReportDate at {bau_path} (0.30 pts)")
            total_score += 0.30
        else:
            print("FAIL: Component 1 — No .bau file found with a ReportDate entry in any autotext dir")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # If no bau found, remaining checks cannot pass
    if content_xml is None or content_xml == '':
        print("FAIL: Component 2 — No content.xml to inspect")
        print("FAIL: Component 3 — No content.xml to inspect")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: The ReportDate section contains 'Report Date: ' text (0.35 points)
    try:
        # Parse the content.xml and look for text content within the ReportDate section
        # We need to handle ODF namespaces
        found_text = False
        # Simple approach: search for 'Report Date' text near the ReportDate section
        # The XML has <text:section text:name="ReportDate"> containing <text:p> with the text
        if 'Report Date' in content_xml:
            found_text = True

        if found_text:
            print(f"PASS: Component 2 — ReportDate section contains 'Report Date' text (0.35 pts)")
            total_score += 0.35
        else:
            print("FAIL: Component 2 — ReportDate section does not contain 'Report Date' text")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The ReportDate section contains a dynamic date field (0.35 points)
    try:
        # Look for <text:date> element in the content
        has_date_field = False
        is_dynamic = False

        if 'text:date' in content_xml:
            has_date_field = True
            # Check if it's dynamic (text:fixed="false" or absence of text:fixed which defaults to dynamic)
            # text:fixed="true" means static, "false" means dynamic
            if 'text:fixed="true"' not in content_xml:
                is_dynamic = True
            elif 'text:fixed="false"' in content_xml:
                is_dynamic = True

        if has_date_field and is_dynamic:
            print(f"PASS: Component 3 — ReportDate contains dynamic date field (text:date with fixed=false) (0.35 pts)")
            total_score += 0.35
        elif has_date_field:
            print(f"FAIL: Component 3 — Date field found but is static (text:fixed='true'), expected dynamic")
        else:
            print("FAIL: Component 3 — No date field (<text:date>) found in ReportDate section")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

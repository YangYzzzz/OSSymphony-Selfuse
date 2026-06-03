"""
Reward Script: Insert a Table of Contents at the beginning of a user manual
Task ID: writer_tech_024
Domain: libreoffice_writer
Scoring:
  Component 1 (0.25): TOC heading exists at beginning with Heading 1 style
  Component 2 (0.25): TOC content includes all Heading 1 entries
  Component 3 (0.25): TOC content includes all Heading 2 entries
  Component 4 (0.25): TOC content includes all Heading 3 entries
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_tech_024'

# Expected headings from the document (these are the headings in the body content)
EXPECTED_H1 = [
    'Introduction',
    'Installation',
    'Configuration',
    'Dashboard Operations',
    'Data Pipeline Management',
    'Troubleshooting',
]

EXPECTED_H2 = [
    'Purpose of This Manual',
    'System Requirements',
    'Pre-Installation Checklist',
    'Graphical Installation',
    'Command-Line Installation',
    'Data Source Management',
    'User and Role Management',
    'Security Configuration',
    'Creating a New Dashboard',
    'Dashboard Sharing and Permissions',
    'Pipeline Architecture',
    'Pipeline Monitoring',
    'Common Installation Issues',
    'Performance Issues',
    'Log Files and Diagnostics',
]

EXPECTED_H3 = [
    'Document Conventions',
    'Revision History',
    'Hardware Requirements',
    'Software Requirements',
    'Downloading the Installer',
    'Verifying the Download',
    'License Agreement Screen',
    'Database Configuration Screen',
    'Configuration File Format',
    'Adding a Database Connection',
    'Configuring Data Refresh Schedules',
    'Creating User Accounts',
    'Permission Matrix',
    'Authentication Methods',
    'Encryption Settings',
    'Widget Types',
    'Adding and Configuring Widgets',
    'Export and Scheduling',
    'Dashboard Templates',
    'Extraction Stage',
    'Transformation Stage',
    'Setting Up Alerts',
    'Error Handling and Recovery',
    'Database Connection Failures',
    'Insufficient Disk Space',
    'Slow Dashboard Loading',
    'High Memory Usage',
    'Collecting Support Bundles',
    'Interpreting Log Messages',
]


def persist_app_state(domain):
    """Save any unsaved changes in LibreOffice Writer."""
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all body headings (after the TOC section) to distinguish TOC from content
    paragraphs = doc.paragraphs

    # Component 1: TOC heading exists at the beginning (0.25 points)
    # The first paragraph should be a "Table of Contents" heading (Heading 1 style)
    try:
        toc_heading_idx = -1
        # Check first few paragraphs for a TOC heading
        for i, p in enumerate(paragraphs[:5]):
            text_lower = p.text.strip().lower()
            style_name = p.style.name if p.style else ''
            if ('table of contents' in text_lower or 'toc' == text_lower) and 'Heading' in style_name:
                toc_heading_idx = i
                break

        if toc_heading_idx >= 0:
            print(f"PASS: Component 1 -- TOC heading found at paragraph {toc_heading_idx} "
                  f"with style '{paragraphs[toc_heading_idx].style.name}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 -- No 'Table of Contents' heading found at beginning of document")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Gather TOC text content: look at paragraphs between the TOC heading and the
    # first content heading (a heading that is NOT "Table of Contents")
    toc_text = ""
    try:
        if toc_heading_idx >= 0:
            # Collect text from paragraphs after TOC heading until we hit a body heading
            for i in range(toc_heading_idx + 1, min(toc_heading_idx + 10, len(paragraphs))):
                p = paragraphs[i]
                style_name = p.style.name if p.style else ''
                # Stop when we hit a real Heading paragraph that isn't the TOC heading
                if 'Heading' in style_name:
                    break
                toc_text += p.text + "\n"
        toc_text = toc_text.strip()
        if toc_text:
            print(f"INFO: TOC text extracted, length={len(toc_text)} chars")
        else:
            print("INFO: No TOC text body found (may use field codes)")
            # Try checking XML for TOC field codes as fallback
            from lxml import etree
            body_xml = doc.element.body.xml
            if 'TOC' in body_xml or 'HYPERLINK' in body_xml:
                # Extract all text from TOC-related paragraphs
                for i in range(toc_heading_idx + 1, len(paragraphs)):
                    p = paragraphs[i]
                    if p.style and 'Heading' in p.style.name:
                        break
                    # Use paragraph XML text extraction including field results
                    full_text = p.text
                    if full_text.strip():
                        toc_text += full_text + "\n"
                toc_text = toc_text.strip()
    except Exception as e:
        print(f"WARNING: TOC text extraction issue: {e}")

    # Component 2: TOC includes all Heading 1 entries (0.25 points)
    try:
        if toc_text:
            h1_found = 0
            h1_missing = []
            for h in EXPECTED_H1:
                if h in toc_text:
                    h1_found += 1
                else:
                    h1_missing.append(h)
            h1_ratio = h1_found / len(EXPECTED_H1) if EXPECTED_H1 else 0
            if h1_ratio >= 0.8:
                pts = 0.25 * h1_ratio
                print(f"PASS: Component 2 -- {h1_found}/{len(EXPECTED_H1)} Heading 1 entries in TOC ({pts:.3f} pts)")
                total_score += pts
            else:
                print(f"FAIL: Component 2 -- Only {h1_found}/{len(EXPECTED_H1)} Heading 1 entries in TOC. "
                      f"Missing: {h1_missing}")
        else:
            print(f"FAIL: Component 2 -- No TOC text content to check")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: TOC includes all Heading 2 entries (0.25 points)
    try:
        if toc_text:
            h2_found = 0
            h2_missing = []
            for h in EXPECTED_H2:
                if h in toc_text:
                    h2_found += 1
                else:
                    h2_missing.append(h)
            h2_ratio = h2_found / len(EXPECTED_H2) if EXPECTED_H2 else 0
            if h2_ratio >= 0.8:
                pts = 0.25 * h2_ratio
                print(f"PASS: Component 3 -- {h2_found}/{len(EXPECTED_H2)} Heading 2 entries in TOC ({pts:.3f} pts)")
                total_score += pts
            else:
                print(f"FAIL: Component 3 -- Only {h2_found}/{len(EXPECTED_H2)} Heading 2 entries in TOC. "
                      f"Missing: {h2_missing}")
        else:
            print(f"FAIL: Component 3 -- No TOC text content to check")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: TOC includes all Heading 3 entries (0.25 points)
    try:
        if toc_text:
            h3_found = 0
            h3_missing = []
            for h in EXPECTED_H3:
                if h in toc_text:
                    h3_found += 1
                else:
                    h3_missing.append(h)
            h3_ratio = h3_found / len(EXPECTED_H3) if EXPECTED_H3 else 0
            if h3_ratio >= 0.8:
                pts = 0.25 * h3_ratio
                print(f"PASS: Component 4 -- {h3_found}/{len(EXPECTED_H3)} Heading 3 entries in TOC ({pts:.3f} pts)")
                total_score += pts
            else:
                print(f"FAIL: Component 4 -- Only {h3_found}/{len(EXPECTED_H3)} Heading 3 entries in TOC. "
                      f"Missing: {h3_missing}")
        else:
            print(f"FAIL: Component 4 -- No TOC text content to check")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
persist_app_state('libreoffice_writer')
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

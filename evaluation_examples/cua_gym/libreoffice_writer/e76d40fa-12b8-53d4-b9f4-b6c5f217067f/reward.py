"""
Reward Script: Create an AutoText entry with page number field
Task ID: writer_frd_060
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): AutoText .bau file contains 'phdr'/'PageHeader' entry
  Component 2 (0.3): Entry content contains 'Page ' text
  Component 3 (0.3): Entry content contains a page-number field element
"""

import os
import glob
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_frd_060'

# AutoText .bau files can be in multiple locations depending on LO version
AUTOTEXT_SEARCH_PATHS = [
    os.path.join(WORKDIR, '.config/libreoffice/user/autotext'),
    os.path.join(WORKDIR, '.config/libreoffice/4/user/autotext'),
]


def find_bau_with_entry(shortcut='phdr', entry_name='PageHeader'):
    """
    Search all known autotext directories for a .bau file containing
    the specified AutoText entry. Returns (bau_path, matched) or (None, False).
    """
    for autotext_dir in AUTOTEXT_SEARCH_PATHS:
        if not os.path.isdir(autotext_dir):
            continue
        for bau_path in glob.glob(os.path.join(autotext_dir, '*.bau')):
            try:
                with zipfile.ZipFile(bau_path, 'r') as z:
                    if 'BlockList.xml' not in z.namelist():
                        continue
                    bl_xml = z.read('BlockList.xml').decode('utf-8')
                    # Check for the entry with correct shortcut and name
                    if f'abbreviated-name="{shortcut}"' in bl_xml and f'name="{entry_name}"' in bl_xml:
                        return bau_path, True
            except Exception:
                continue
    return None, False


def check_entry_content(bau_path, shortcut='phdr'):
    """
    Read the content.xml inside the AutoText entry's subdirectory
    within the .bau ZIP file. Returns the raw XML string or None.
    """
    content_path = f'{shortcut}/content.xml'
    try:
        with zipfile.ZipFile(bau_path, 'r') as z:
            if content_path in z.namelist():
                return z.read(content_path).decode('utf-8')
    except Exception:
        pass
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: AutoText entry 'PageHeader' with shortcut 'phdr' exists (0.4 points)
    try:
        bau_path, found = find_bau_with_entry(shortcut='phdr', entry_name='PageHeader')
        if found and bau_path:
            print(f"PASS: Component 1 -- AutoText entry 'PageHeader' (shortcut 'phdr') found in {bau_path} (0.4 pts)")
            total_score += 0.4
        else:
            print("FAIL: Component 1 -- No AutoText entry with name='PageHeader' and shortcut='phdr' found in any .bau file")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    if not (bau_path and found):
        # Cannot check content without the entry
        print("\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: Entry content contains 'Page ' text (0.3 points)
    try:
        content_xml = check_entry_content(bau_path, shortcut='phdr')
        if content_xml is None:
            print("FAIL: Component 2 -- Could not read phdr/content.xml from .bau file")
        else:
            # Check for 'Page ' text in the content (the literal text before the page number field)
            if 'Page ' in content_xml or 'Page\t' in content_xml or '>Page ' in content_xml:
                print(f"PASS: Component 2 -- Entry content contains 'Page ' text (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 -- Entry content does not contain 'Page ' text. Content snippet: {content_xml[:500]}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Entry content contains a page-number field element (0.3 points)
    try:
        content_xml = check_entry_content(bau_path, shortcut='phdr')
        if content_xml is None:
            print("FAIL: Component 3 -- Could not read phdr/content.xml from .bau file")
        else:
            # LibreOffice ODF AutoText stores page numbers as <text:page-number ...>
            has_page_number = 'page-number' in content_xml
            if has_page_number:
                print(f"PASS: Component 3 -- Entry content contains page-number field element (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 -- No page-number field found in entry content. Content snippet: {content_xml[:500]}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()

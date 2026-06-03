"""
Reward Script: Convert Complete_Manual.odt into master document with subdocuments
Task ID: writer_rm_060
Domain: libreoffice_writer
Scoring:
  Component 1 (0.15): Complete_Manual.odm exists with correct master document mimetype
  Component 2 (0.15): All 6 chapter .odt files exist with correct ODF text mimetype
  Component 3 (0.30): ODM contains 6 text:section elements linking to all 6 chapter files
  Component 4 (0.25): Each chapter .odt has the correct Heading 1 matching expected chapter name
  Component 5 (0.15): ODM has no text:section or xlink:href pointing to non-existent files
"""

import os
import zipfile
import xml.etree.ElementTree as ET
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_060'

# Expected chapter files and their Heading 1 titles
EXPECTED_CHAPTERS = {
    'Chapter01_Getting_Started.odt': 'Getting Started',
    'Chapter02_Installation.odt': 'Installation',
    'Chapter03_Configuration.odt': 'Configuration',
    'Chapter04_Usage.odt': 'Usage',
    'Chapter05_Troubleshooting.odt': 'Troubleshooting',
    'Chapter06_API_Reference.odt': 'API Reference',
}

ODM_PATH = os.path.join(WORKDIR, 'Complete_Manual.odm')

# ODF XML namespaces
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'xlink': 'http://www.w3.org/1999/xlink',
}


def get_mimetype(zip_path):
    """Read the mimetype from an ODF zip file."""
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            return z.read('mimetype').decode().strip()
    except Exception:
        return None


def get_content_xml(zip_path):
    """Read content.xml from an ODF zip file."""
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            return z.read('content.xml').decode()
    except Exception:
        return None


def extract_section_hrefs(content_xml):
    """Extract xlink:href values from text:section-source elements in content.xml."""
    hrefs = []
    try:
        root = ET.fromstring(content_xml)
        # Find all text:section-source elements
        for elem in root.iter():
            tag = elem.tag
            if tag.endswith('}section-source') or tag == 'text:section-source':
                href = elem.get('{http://www.w3.org/1999/xlink}href', '')
                if href:
                    hrefs.append(href)
        # Also check for section-source as attribute pattern
        if not hrefs:
            # Fallback: use regex to find xlink:href in text:section-source
            pattern = r'<text:section-source[^>]*xlink:href="([^"]*)"'
            hrefs = re.findall(pattern, content_xml)
    except Exception:
        # Fallback regex
        pattern = r'<text:section-source[^>]*xlink:href="([^"]*)"'
        hrefs = re.findall(pattern, content_xml)
    return hrefs


def extract_heading1_texts(content_xml):
    """Extract all Heading 1 (outline-level=1) text from content.xml."""
    headings = []
    try:
        # Use regex since odfpy namespace handling can be tricky
        # Match text:h with outline-level="1"
        pattern = r'<text:h[^>]*text:outline-level="1"[^>]*>(.*?)</text:h>'
        matches = re.findall(pattern, content_xml, re.DOTALL)
        for m in matches:
            # Strip inner XML tags to get plain text
            plain = re.sub(r'<[^>]+>', '', m).strip()
            if plain:
                headings.append(plain)
    except Exception:
        pass
    return headings


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Complete_Manual.odm exists with correct master document mimetype (0.15 pts)
    try:
        if os.path.exists(ODM_PATH):
            mime = get_mimetype(ODM_PATH)
            if mime == 'application/vnd.oasis.opendocument.text-master':
                print(f"PASS: Component 1 — ODM exists with correct mimetype: {mime} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — ODM mimetype is '{mime}', expected 'application/vnd.oasis.opendocument.text-master'")
        else:
            print(f"FAIL: Component 1 — Complete_Manual.odm does not exist at {ODM_PATH}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 6 chapter .odt files exist with correct mimetype (0.15 pts)
    try:
        existing_chapters = 0
        correct_mime_chapters = 0
        for chapter_file in EXPECTED_CHAPTERS:
            chapter_path = os.path.join(WORKDIR, chapter_file)
            if os.path.exists(chapter_path):
                existing_chapters += 1
                mime = get_mimetype(chapter_path)
                if mime == 'application/vnd.oasis.opendocument.text':
                    correct_mime_chapters += 1
                else:
                    print(f"  WARN: {chapter_file} has mimetype '{mime}' instead of ODF text")
            else:
                print(f"  WARN: {chapter_file} does not exist")

        if existing_chapters == 6 and correct_mime_chapters == 6:
            print(f"PASS: Component 2 — All 6 chapter files exist with correct ODF text mimetype (0.15 pts)")
            total_score += 0.15
        elif existing_chapters == 6:
            partial = 0.10
            print(f"PARTIAL: Component 2 — All 6 files exist but {6 - correct_mime_chapters} have wrong mimetype ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Only {existing_chapters}/6 chapter files exist")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: ODM contains text:section elements linking to all 6 chapter files (0.30 pts)
    try:
        content_xml = get_content_xml(ODM_PATH)
        if content_xml:
            hrefs = extract_section_hrefs(content_xml)
            # Normalize hrefs (remove ./ prefix if present)
            normalized_hrefs = [h.lstrip('./') for h in hrefs]
            linked_count = 0
            for chapter_file in EXPECTED_CHAPTERS:
                if chapter_file in normalized_hrefs:
                    linked_count += 1
                else:
                    print(f"  WARN: ODM does not link to {chapter_file}")

            if linked_count == 6:
                print(f"PASS: Component 3 — ODM links to all 6 chapter files via text:section-source (0.30 pts)")
                total_score += 0.30
            elif linked_count > 0:
                partial = round(0.30 * (linked_count / 6), 2)
                print(f"PARTIAL: Component 3 — ODM links to {linked_count}/6 chapters ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — ODM has no links to chapter files. Found hrefs: {hrefs}")
        else:
            print(f"FAIL: Component 3 — Cannot read content.xml from ODM")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Each chapter has correct Heading 1 content (0.25 pts)
    try:
        correct_headings = 0
        for chapter_file, expected_heading in EXPECTED_CHAPTERS.items():
            chapter_path = os.path.join(WORKDIR, chapter_file)
            if not os.path.exists(chapter_path):
                print(f"  WARN: Cannot check heading for missing {chapter_file}")
                continue
            content_xml = get_content_xml(chapter_path)
            if content_xml:
                headings = extract_heading1_texts(content_xml)
                if headings and expected_heading in headings[0]:
                    correct_headings += 1
                else:
                    # Also try without outline-level filter — check all headings
                    all_headings_pattern = r'<text:h[^>]*>(.*?)</text:h>'
                    all_matches = re.findall(all_headings_pattern, content_xml, re.DOTALL)
                    all_plain = [re.sub(r'<[^>]+>', '', m).strip() for m in all_matches]
                    if all_plain and expected_heading in all_plain[0]:
                        correct_headings += 1
                    else:
                        print(f"  WARN: {chapter_file} first heading is '{all_plain[0] if all_plain else 'NONE'}', expected '{expected_heading}'")

        if correct_headings == 6:
            print(f"PASS: Component 4 — All 6 chapters have correct Heading 1 content (0.25 pts)")
            total_score += 0.25
        elif correct_headings > 0:
            partial = round(0.25 * (correct_headings / 6), 2)
            print(f"PARTIAL: Component 4 — {correct_headings}/6 chapters have correct Heading 1 ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No chapters have the expected Heading 1")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Sections in ODM are in correct order (0.15 pts)
    try:
        content_xml = get_content_xml(ODM_PATH)
        if content_xml:
            hrefs = extract_section_hrefs(content_xml)
            normalized_hrefs = [h.lstrip('./') for h in hrefs]
            expected_order = list(EXPECTED_CHAPTERS.keys())
            if normalized_hrefs == expected_order:
                print(f"PASS: Component 5 — ODM sections are in correct chapter order (0.15 pts)")
                total_score += 0.15
            elif set(normalized_hrefs) == set(expected_order):
                print(f"PARTIAL: Component 5 — All chapters linked but order is wrong ({0.08} pts)")
                total_score += 0.08
            else:
                print(f"FAIL: Component 5 — ODM section order mismatch. Got: {normalized_hrefs}")
        else:
            print(f"FAIL: Component 5 — Cannot read ODM content.xml")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(ODM_PATH):
    # If ODM doesn't exist, check if there's still just the original .odt (initial state)
    odt_path = os.path.join(WORKDIR, 'Complete_Manual.odt')
    if os.path.exists(odt_path):
        print("Initial state detected: Complete_Manual.odt exists but no .odm file")
    else:
        print(f"File not found: {ODM_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()

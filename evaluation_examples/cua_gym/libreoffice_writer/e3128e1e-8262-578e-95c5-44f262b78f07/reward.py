"""
Reward Script: Add bibliography entry to Writer document
Task ID: writer_acad_031
Domain: libreoffice_writer
Scoring: 6 components checking bibliography entry fields in customXml/item1.xml
  - Component 1: At least one bibliography source exists (0.2)
  - Component 2: Source type is Book (0.15)
  - Component 3: Author is Smith, J. (0.2)
  - Component 4: Title is 'Introduction to Machine Learning' (0.2)
  - Component 5: Year is 2020 (0.1)
  - Component 6: Publisher is 'Cambridge University Press' (0.15)
"""

import os
import zipfile
import xml.etree.ElementTree as ET


WORKDIR = '/home/user'
TASK_ID = 'writer_acad_031'

# Namespace for bibliography XML in .docx
BIB_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/bibliography'
NS = {'b': BIB_NS}


def persist_app_state(domain: str):
    """Save any unsaved edits in LibreOffice before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def extract_bibliography_sources(file_path):
    """
    Extract bibliography source entries from the customXml/item1.xml
    inside a .docx file. Returns a list of dicts with source fields.
    """
    sources = []
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            # Find the bibliography customXml part
            bib_xml = None
            for name in z.namelist():
                if name.startswith('customXml/item') and name.endswith('.xml'):
                    content = z.read(name).decode('utf-8')
                    if 'bibliography' in content.lower() or 'Sources' in content:
                        bib_xml = content
                        break

            if bib_xml is None:
                print("INFO: No bibliography customXml found")
                return sources

            root = ET.fromstring(bib_xml)

            # Find all Source elements
            for source in root.findall('.//b:Source', NS):
                entry = {}

                # SourceType
                st = source.find('b:SourceType', NS)
                if st is not None:
                    entry['source_type'] = st.text

                # Title
                title = source.find('b:Title', NS)
                if title is not None:
                    entry['title'] = title.text

                # Year
                year = source.find('b:Year', NS)
                if year is not None:
                    entry['year'] = year.text

                # Publisher
                pub = source.find('b:Publisher', NS)
                if pub is not None:
                    entry['publisher'] = pub.text

                # Author - nested structure
                # b:Author/b:Author/b:NameList/b:Person with b:Last and b:First
                author_elem = source.find('.//b:Author/b:Author/b:NameList/b:Person', NS)
                if author_elem is None:
                    # Try alternate path without double Author nesting
                    author_elem = source.find('.//b:Author/b:NameList/b:Person', NS)
                if author_elem is not None:
                    last = author_elem.find('b:Last', NS)
                    first = author_elem.find('b:First', NS)
                    entry['author_last'] = last.text if last is not None else None
                    entry['author_first'] = first.text if first is not None else None

                # Tag
                tag = source.find('b:Tag', NS)
                if tag is not None:
                    entry['tag'] = tag.text

                sources.append(entry)
    except Exception as e:
        print(f"ERROR: Failed to extract bibliography: {e}")

    return sources


def verify_task(file_path):
    """
    Verify that the bibliography database contains the required entry.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid .docx
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            z.namelist()  # basic validity check
    except Exception as e:
        print(f"CRITICAL: Cannot open docx: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract bibliography sources
    sources = extract_bibliography_sources(file_path)
    print(f"INFO: Found {len(sources)} bibliography source(s)")
    for i, s in enumerate(sources):
        print(f"  Source {i}: {s}")

    # Component 1: At least one bibliography source exists (0.2 points)
    try:
        if len(sources) > 0:
            print(f"PASS: Component 1 - Bibliography source entry exists ({len(sources)} found) (0.2 pts)")
            total_score += 0.2
        else:
            print("FAIL: Component 1 - No bibliography source entries found")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    if len(sources) == 0:
        # No source means nothing else to check
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Find the best matching source (the one most likely to be the target entry)
    # Look for any source that matches at least one expected field
    target = None
    for s in sources:
        # Match on title or author last name
        title_match = s.get('title', '').strip().lower() == 'introduction to machine learning'
        author_match = s.get('author_last', '').strip().lower() == 'smith'
        if title_match or author_match:
            target = s
            break

    # If no match found by title/author, use the first source
    if target is None:
        target = sources[0]
        print("INFO: No exact title/author match found, using first source entry")

    # Component 2: Source type is Book (0.15 points)
    try:
        src_type = target.get('source_type', '')
        if src_type and src_type.strip().lower() == 'book':
            print(f"PASS: Component 2 - Source type is 'Book' (found: {src_type}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 - Expected source type 'Book', found: {src_type!r}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Author is Smith, J. (0.2 points)
    try:
        last = target.get('author_last', '')
        first = target.get('author_first', '')
        last_ok = last and last.strip().lower() == 'smith'
        # Accept "J." or "J" for first name
        first_ok = first and first.strip().lower().rstrip('.') == 'j'
        if last_ok and first_ok:
            print(f"PASS: Component 3 - Author is Smith, J. (found: {last}, {first}) (0.2 pts)")
            total_score += 0.2
        elif last_ok:
            print(f"PARTIAL: Component 3 - Last name matches but first name wrong (found: {last}, {first}) (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 3 - Expected author Smith, J., found: {last!r}, {first!r}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Title is 'Introduction to Machine Learning' (0.2 points)
    try:
        title = target.get('title', '')
        if title and title.strip().lower() == 'introduction to machine learning':
            print(f"PASS: Component 4 - Title matches (found: {title}) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 - Expected 'Introduction to Machine Learning', found: {title!r}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Year is 2020 (0.1 points)
    try:
        year = target.get('year', '')
        if year and year.strip() == '2020':
            print(f"PASS: Component 5 - Year is 2020 (found: {year}) (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 5 - Expected year '2020', found: {year!r}")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: Publisher is 'Cambridge University Press' (0.15 points)
    try:
        pub = target.get('publisher', '')
        if pub and pub.strip().lower() == 'cambridge university press':
            print(f"PASS: Component 6 - Publisher matches (found: {pub}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 6 - Expected 'Cambridge University Press', found: {pub!r}")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

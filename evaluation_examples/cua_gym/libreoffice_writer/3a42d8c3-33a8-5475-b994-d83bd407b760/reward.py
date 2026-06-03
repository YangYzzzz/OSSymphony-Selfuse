"""
Reward Script: Merge NDA template and export as individual .odt files
Task ID: writer_mt_046
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): 8 .odt files exist in ~/Desktop/NDA_Output/ with sequential naming
  Component 2 (0.3): All files are valid ODF documents (correct mimetype in ZIP)
  Component 3 (0.2): Each file contains the correct personalized PartyName, no placeholders
  Component 4 (0.2): Each file contains correct CompanyName, EffectiveDate, Jurisdiction per record
"""

import os
import re
import zipfile

WORKDIR = '/home/user'
TASK_ID = 'writer_mt_046'
OUTPUT_DIR = os.path.join(WORKDIR, 'Desktop', 'NDA_Output')

# Expected records from NDAParties.csv (in order)
RECORDS = [
    {'PartyName': 'Elena Vasquez', 'CompanyName': 'Meridian Dynamics LLC',
     'EffectiveDate': 'January 15, 2026', 'Jurisdiction': 'State of California'},
    {'PartyName': 'James Whitfield', 'CompanyName': 'Apex Innovations Inc.',
     'EffectiveDate': 'February 3, 2026', 'Jurisdiction': 'State of New York'},
    {'PartyName': 'Priya Sharma', 'CompanyName': 'NovaTech Solutions Pvt. Ltd.',
     'EffectiveDate': 'March 10, 2026', 'Jurisdiction': 'State of Delaware'},
    {'PartyName': 'Marcus Chen', 'CompanyName': 'Silverline Partners Group',
     'EffectiveDate': 'April 1, 2026', 'Jurisdiction': 'State of Texas'},
    {'PartyName': 'Olivia Brennan', 'CompanyName': 'Coastal Ventures Corp.',
     'EffectiveDate': 'May 22, 2026', 'Jurisdiction': 'State of Florida'},
    {'PartyName': 'David Kowalski', 'CompanyName': 'Pinnacle Research Labs',
     'EffectiveDate': 'June 8, 2026', 'Jurisdiction': 'State of Illinois'},
    {'PartyName': 'Aisha Patel', 'CompanyName': 'Horizon Analytics Ltd.',
     'EffectiveDate': 'July 14, 2026', 'Jurisdiction': 'State of Massachusetts'},
    {'PartyName': 'Robert Lindqvist', 'CompanyName': 'Nordic Bridge Consulting AB',
     'EffectiveDate': 'August 30, 2026', 'Jurisdiction': 'State of Washington'},
]


def extract_odt_text(path):
    """Extract plain text from an .odt file by parsing content.xml."""
    with zipfile.ZipFile(path) as z:
        content = z.read('content.xml').decode('utf-8')
    text = re.sub(r'<[^>]+>', ' ', content)
    text = re.sub(r'&quot;', '"', text)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def get_odt_mimetype(path):
    """Read the mimetype entry from the .odt ZIP archive."""
    with zipfile.ZipFile(path) as z:
        return z.read('mimetype').decode('utf-8').strip()


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: output directory exists
    if not os.path.isdir(OUTPUT_DIR):
        print(f"CRITICAL: Output directory not found: {OUTPUT_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: 8 .odt files exist with sequential naming NDA_Template_1..8.odt (0.3 points)
    try:
        expected_files = [f'NDA_Template_{i}.odt' for i in range(1, 9)]
        existing_files = os.listdir(OUTPUT_DIR)
        odt_files = [f for f in existing_files if f.endswith('.odt')]
        found_expected = [f for f in expected_files if f in existing_files]

        if len(found_expected) == 8:
            print(f"PASS: Component 1 -- All 8 expected .odt files found in NDA_Output (0.3 pts)")
            total_score += 0.3
        elif len(odt_files) == 8:
            # 8 odt files but different naming -- partial credit
            print(f"PARTIAL: Component 1 -- 8 .odt files found but naming differs: {sorted(odt_files)} (0.15 pts)")
            total_score += 0.15
        elif len(odt_files) > 0:
            ratio = min(len(odt_files), 8) / 8.0
            pts = round(0.3 * ratio * 0.5, 2)
            print(f"PARTIAL: Component 1 -- {len(odt_files)} .odt files found (expected 8) (0.0 pts)")
        else:
            print(f"FAIL: Component 1 -- No .odt files found in {OUTPUT_DIR}. Contents: {existing_files[:20]}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # For remaining components, build a mapping of index -> file path
    # Try expected naming first, fall back to sorted odt files
    file_map = {}
    for i in range(1, 9):
        expected_name = f'NDA_Template_{i}.odt'
        fpath = os.path.join(OUTPUT_DIR, expected_name)
        if os.path.isfile(fpath):
            file_map[i] = fpath
    # If expected naming not found, try sorted odt files
    if len(file_map) < 8:
        odt_files_sorted = sorted([f for f in os.listdir(OUTPUT_DIR) if f.endswith('.odt')])
        for idx, fname in enumerate(odt_files_sorted[:8], 1):
            if idx not in file_map:
                file_map[idx] = os.path.join(OUTPUT_DIR, fname)

    if len(file_map) == 0:
        print("FAIL: No .odt files to verify for Components 2-4")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: All files are valid ODF text documents (0.3 points)
    try:
        valid_odf_count = 0
        for i in sorted(file_map.keys()):
            fpath = file_map[i]
            try:
                mime = get_odt_mimetype(fpath)
                if mime == 'application/vnd.oasis.opendocument.text':
                    valid_odf_count += 1
                else:
                    print(f"  File {i}: wrong mimetype '{mime}'")
            except Exception as e:
                print(f"  File {i}: not a valid ZIP/ODT: {e}")

        if valid_odf_count == len(file_map) and valid_odf_count >= 8:
            print(f"PASS: Component 2 -- All {valid_odf_count} files are valid ODF text documents (0.3 pts)")
            total_score += 0.3
        elif valid_odf_count > 0:
            ratio = valid_odf_count / max(len(file_map), 8)
            if ratio > 0:
                pts = round(0.3 * ratio, 2)
                print(f"PARTIAL: Component 2 -- {valid_odf_count}/{len(file_map)} files are valid ODF ({pts} pts)")
                total_score += pts
        else:
            print(f"FAIL: Component 2 -- No files are valid ODF documents")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Each file contains the correct PartyName, no placeholders remain (0.2 points)
    try:
        party_match_count = 0
        placeholders_detected = 0
        for i in sorted(file_map.keys()):
            if i > 8:
                break
            fpath = file_map[i]
            try:
                text = extract_odt_text(fpath)
                record = RECORDS[i - 1]
                # Check PartyName present
                if record['PartyName'] in text:
                    party_match_count += 1
                else:
                    print(f"  File {i}: PartyName '{record['PartyName']}' not found")
                # Check no merge field placeholders
                for placeholder in ['<PartyName>', '<CompanyName>', '<EffectiveDate>', '<Jurisdiction>']:
                    if placeholder in text:
                        placeholders_detected += 1
                        print(f"  File {i}: placeholder '{placeholder}' still present")
            except Exception as e:
                print(f"  File {i}: could not extract text: {e}")

        if party_match_count == 8 and placeholders_detected == 0:
            print(f"PASS: Component 3 -- All 8 files have correct PartyName, no placeholders (0.2 pts)")
            total_score += 0.2
        elif party_match_count > 0 and placeholders_detected == 0:
            pts = round(0.2 * party_match_count / 8, 2)
            print(f"PARTIAL: Component 3 -- {party_match_count}/8 files have correct PartyName ({pts} pts)")
            total_score += pts
        else:
            if placeholders_detected > 0:
                print(f"FAIL: Component 3 -- Merge field placeholders still present in files")
            else:
                print(f"FAIL: Component 3 -- PartyName not found in files")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Each file has correct CompanyName, EffectiveDate, Jurisdiction (0.2 points)
    try:
        full_match_count = 0
        for i in sorted(file_map.keys()):
            if i > 8:
                break
            fpath = file_map[i]
            try:
                text = extract_odt_text(fpath)
                record = RECORDS[i - 1]
                fields_ok = 0
                for field in ['CompanyName', 'EffectiveDate', 'Jurisdiction']:
                    if record[field] in text:
                        fields_ok += 1
                    else:
                        print(f"  File {i}: {field} '{record[field]}' not found")
                if fields_ok == 3:
                    full_match_count += 1
            except Exception as e:
                print(f"  File {i}: could not extract text: {e}")

        if full_match_count == 8:
            print(f"PASS: Component 4 -- All 8 files have correct CompanyName, EffectiveDate, Jurisdiction (0.2 pts)")
            total_score += 0.2
        elif full_match_count > 0:
            pts = round(0.2 * full_match_count / 8, 2)
            print(f"PARTIAL: Component 4 -- {full_match_count}/8 files fully match ({pts} pts)")
            total_score += pts
        else:
            print(f"FAIL: Component 4 -- No files have correct remaining merge fields")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

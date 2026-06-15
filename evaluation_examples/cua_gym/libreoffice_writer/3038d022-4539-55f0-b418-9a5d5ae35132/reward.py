"""
Reward Script: Mail merge output verification
Task ID: writer_mt_029
Domain: libreoffice_writer
Scoring:
  Component 1: 15 merged letters present (0.3 pts)
  Component 2: All merge fields replaced with actual data (0.2 pts)
  Component 3: All 15 party names present (0.3 pts)
  Component 4: Page breaks separate the letters (0.2 pts)
"""

import os
import zipfile

WORKDIR = '/home/user'
TASK_ID = 'writer_mt_029'
FILE_PATH = os.path.join(WORKDIR, 'Merged_Contracts.odt')

# The 15 party names from the data source
PARTY_NAMES = [
    "Meridian Technologies",
    "Cascade Financial",
    "Vertex Software",
    "Horizon Healthcare",
    "Atlas Construction",
    "Pinnacle Marketing",
    "Silverline Logistics",
    "Redwood Environmental",
    "Quantum Research",
    "Bluecrest Consulting",
    "Oakbridge Manufacturing",
    "Summit Legal",
    "Trident Aerospace",
    "Evergreen Energy",
    "Lighthouse Data",
]

# Merge fields that should NOT remain in the output
MERGE_FIELDS = ["<PartyName>", "<ContractValue>", "<EffectiveDate>", "<TermLength>"]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: File must exist and be a valid ODT (zip archive)
    if not os.path.exists(file_path):
        print("CRITICAL: File not found: " + file_path)
        print("REWARD: 0.0")
        return 0.0

    try:
        with zipfile.ZipFile(file_path) as z:
            if 'content.xml' not in z.namelist():
                print("CRITICAL: Not a valid ODT file (no content.xml)")
                print("REWARD: 0.0")
                return 0.0
            content = z.read('content.xml').decode('utf-8')
    except Exception as e:
        print("CRITICAL: Cannot read ODT file: " + str(e))
        print("REWARD: 0.0")
        return 0.0

    # Component 1: 15 merged letters present (0.3 pts)
    try:
        sa_count = content.count("SERVICE AGREEMENT")
        if sa_count >= 15:
            print("PASS: Component 1 - Found " + str(sa_count) + " SERVICE AGREEMENT headings (0.3 pts)")
            total_score += 0.3
        elif sa_count >= 10:
            partial = round(0.3 * (sa_count / 15.0), 2)
            print("PARTIAL: Component 1 - Found " + str(sa_count) + "/15 letters (" + str(partial) + " pts)")
            total_score += partial
        else:
            print("FAIL: Component 1 - Found " + str(sa_count) + " headings, expected 15")
    except Exception as e:
        print("ERROR: Component 1 - " + str(e))

    # Component 2: All merge fields replaced (0.2 pts)
    try:
        remaining = []
        for field in MERGE_FIELDS:
            if field in content:
                remaining.append(field)

        if len(remaining) == 0:
            print("PASS: Component 2 - No merge fields remain in document (0.2 pts)")
            total_score += 0.2
        else:
            print("FAIL: Component 2 - Unresolved merge fields: " + str(remaining))
    except Exception as e:
        print("ERROR: Component 2 - " + str(e))

    # Component 3: All 15 party names present (0.3 pts)
    try:
        found_names = []
        missing_names = []
        for name in PARTY_NAMES:
            if name in content:
                found_names.append(name)
            else:
                missing_names.append(name)

        if len(found_names) == 15:
            print("PASS: Component 3 - All 15 party names found (0.3 pts)")
            total_score += 0.3
        elif len(found_names) >= 10:
            partial = round(0.3 * (len(found_names) / 15.0), 2)
            print("PARTIAL: Component 3 - " + str(len(found_names)) + "/15 names (" + str(partial) + " pts)")
            total_score += partial
        else:
            print("FAIL: Component 3 - Only " + str(len(found_names)) + "/15 names found")
    except Exception as e:
        print("ERROR: Component 3 - " + str(e))

    # Component 4: Page breaks between letters (0.2 pts)
    # In ODT, page breaks are implemented via paragraph styles with fo:break-before="page"
    # or master-page-name references. We check for break-before="page" in the content.
    try:
        # Count page break style usage
        # The golden file uses a style called PageBreakCenterTitle with fo:break-before="page"
        # Count how many paragraphs reference a style with page break
        pb_keyword = 'break-before'
        has_page_break_style = pb_keyword in content

        # Count occurrences of PageBreak style references in text:p elements
        # Simple string counting approach
        pb_style_count = content.count('PageBreak')

        if has_page_break_style and pb_style_count >= 15:
            print("PASS: Component 4 - Page break style found with " + str(pb_style_count) + " refs (0.2 pts)")
            total_score += 0.2
        elif has_page_break_style and sa_count >= 15:
            # Page break mechanism exists and all 15 letters are present
            print("PASS: Component 4 - Page break style present with all 15 letters (0.2 pts)")
            total_score += 0.2
        else:
            print("FAIL: Component 4 - has_break=" + str(has_page_break_style) + " pb_refs=" + str(pb_style_count))
    except Exception as e:
        print("ERROR: Component 4 - " + str(e))

    final_score = round(min(total_score, 1.0), 1)
    print("")
    print("Score: " + str(total_score) + "/1.0")
    print("REWARD: " + str(final_score))
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print("File not found: " + FILE_PATH)
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

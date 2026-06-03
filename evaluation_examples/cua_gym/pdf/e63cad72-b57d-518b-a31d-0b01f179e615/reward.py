"""
Reward Script: Extract bibliography from PDF and create BibTeX file
Task ID: pdf_res_027
Domain: pdf
Scoring:
  Component 1 (0.20): references.bib exists and is non-empty BibTeX
  Component 2 (0.30): Contains at least 25 BibTeX entries
  Component 3 (0.25): All entries have required fields (author, title, year)
  Component 4 (0.25): All entries use valid BibTeX types (@article/@inproceedings/etc.)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_027'
BIB_PATH = os.path.join(WORKDIR, 'papers', 'references.bib')

# Valid BibTeX entry types
VALID_TYPES = {
    'article', 'inproceedings', 'book', 'incollection', 'phdthesis',
    'mastersthesis', 'techreport', 'misc', 'proceedings', 'unpublished',
    'manual', 'booklet', 'conference'
}

REQUIRED_FIELDS = ['author', 'title', 'year']


def parse_bib_entries(content):
    """Parse BibTeX content into list of (entry_type, cite_key, fields_dict)."""
    entries = []
    # Match @type{key, ... } blocks
    pattern = r'@(\w+)\{([^,]+),\s*(.*?)\n\}'
    for match in re.finditer(pattern, content, re.DOTALL):
        entry_type = match.group(1).lower()
        cite_key = match.group(2).strip()
        body = match.group(3)
        # Extract field names
        fields = re.findall(r'(\w+)\s*=\s*\{', body)
        fields_lower = [f.lower() for f in fields]
        entries.append((entry_type, cite_key, fields_lower))
    return entries


def verify_task(bib_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(bib_path):
        print(f"CRITICAL: File not found: {bib_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        content = open(bib_path, 'r', encoding='utf-8').read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {bib_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    entries = parse_bib_entries(content)

    # Component 1: File is non-empty and contains at least 1 valid BibTeX entry (0.20 pts)
    try:
        if len(entries) >= 1 and len(content.strip()) > 100:
            print(f"PASS: Component 1 — BibTeX file exists with {len(entries)} entries (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — File exists but has {len(entries)} entries or is too short")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: At least 25 BibTeX entries (0.30 pts)
    # Task says 30 references, ground truth says at least 25
    try:
        entry_count = len(entries)
        if entry_count >= 25:
            print(f"PASS: Component 2 — {entry_count} entries found (>= 25 required) (0.30 pts)")
            total_score += 0.30
        elif entry_count >= 15:
            partial = 0.30 * (entry_count - 15) / 10.0
            print(f"PARTIAL: Component 2 — {entry_count} entries (15-24 range, partial credit: {partial:.2f})")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Only {entry_count} entries found (need >= 25)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All entries have required fields: author, title, year (0.25 pts)
    try:
        if len(entries) == 0:
            print(f"FAIL: Component 3 — No entries to check")
        else:
            entries_with_all_fields = 0
            missing_details = []
            for entry_type, cite_key, fields in entries:
                missing = [f for f in REQUIRED_FIELDS if f not in fields]
                if not missing:
                    entries_with_all_fields += 1
                else:
                    if len(missing_details) < 3:  # Show first 3 failures
                        missing_details.append(f"  {cite_key}: missing {missing}")

            completeness_ratio = entries_with_all_fields / len(entries)
            if completeness_ratio >= 0.9:
                print(f"PASS: Component 3 — {entries_with_all_fields}/{len(entries)} entries have all required fields (0.25 pts)")
                total_score += 0.25
            elif completeness_ratio >= 0.5:
                partial = 0.25 * completeness_ratio
                total_score += partial
                print(f"PARTIAL: Component 3 — {entries_with_all_fields}/{len(entries)} entries have all fields ({partial:.2f} pts)")
                for d in missing_details:
                    print(d)
            else:
                print(f"FAIL: Component 3 — Only {entries_with_all_fields}/{len(entries)} entries have all required fields")
                for d in missing_details:
                    print(d)
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: All entries use valid BibTeX types (0.25 pts)
    try:
        if len(entries) == 0:
            print(f"FAIL: Component 4 — No entries to check")
        else:
            valid_type_count = 0
            invalid_types = []
            for entry_type, cite_key, fields in entries:
                if entry_type in VALID_TYPES:
                    valid_type_count += 1
                else:
                    if len(invalid_types) < 3:
                        invalid_types.append(f"  {cite_key}: type='{entry_type}'")

            type_ratio = valid_type_count / len(entries)
            if type_ratio >= 0.9:
                print(f"PASS: Component 4 — {valid_type_count}/{len(entries)} entries have valid BibTeX types (0.25 pts)")
                total_score += 0.25
            elif type_ratio >= 0.5:
                partial = 0.25 * type_ratio
                total_score += partial
                print(f"PARTIAL: Component 4 — {valid_type_count}/{len(entries)} entries have valid types ({partial:.2f} pts)")
                for d in invalid_types:
                    print(d)
            else:
                print(f"FAIL: Component 4 — Only {valid_type_count}/{len(entries)} entries have valid types")
                for d in invalid_types:
                    print(d)
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(BIB_PATH):
    print(f"File not found: {BIB_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(BIB_PATH)

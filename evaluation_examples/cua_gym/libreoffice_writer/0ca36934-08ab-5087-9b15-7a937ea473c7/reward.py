"""
Reward Script: Add custom hyphenation pattern for 'bioinformatics' to custom dictionary
Task ID: writer_fp_023
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): TechnicalTerms.dic contains a hyphenation entry for 'bioinformatics'
  Component 2 (0.3): The entry uses correct hyphenation points: bio=in=for=mat=ics
  Component 3 (0.3): Dictionary is properly formatted (header, separator, entry structure)
"""

import os
import glob

WORKDIR = '/home/user'
TASK_ID = 'writer_fp_023'

# Path to TechnicalTerms.dic in LibreOffice user profile
DICT_DIR = os.path.expanduser('~/.config/libreoffice/4/user/wordbook')
DICT_FILE = os.path.join(DICT_DIR, 'TechnicalTerms.dic')

# Also search common alternative locations
ALT_DICT_PATHS = [
    os.path.join(WORKDIR, '.config/libreoffice/4/user/wordbook/TechnicalTerms.dic'),
    '/home/user/.config/libreoffice/4/user/wordbook/TechnicalTerms.dic',
]

# The expected hyphenation pattern
EXPECTED_WORD = 'bioinformatics'
EXPECTED_ENTRY = 'bio=in=for=mat=ics'
EXPECTED_SYLLABLES = ['bio', 'in', 'for', 'mat', 'ics']


def find_dict_file():
    """Find the TechnicalTerms.dic file."""
    # Try primary path
    if os.path.exists(DICT_FILE):
        return DICT_FILE
    # Try alternatives
    for path in ALT_DICT_PATHS:
        if path and os.path.exists(path):
            return path
    # Search broadly
    search_patterns = [
        '/home/user/.config/libreoffice/*/user/wordbook/TechnicalTerms.dic',
        '/home/user/.config/libreoffice/*/user/wordbook/technicalterms.dic',
    ]
    for pattern in search_patterns:
        matches = glob.glob(pattern)
        if matches:
            return matches[0]
    return None


def verify_task():
    """
    Verify that the custom hyphenation pattern for 'bioinformatics' has been added
    to the TechnicalTerms custom dictionary.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Find the dictionary file
    dict_path = find_dict_file()
    if not dict_path:
        print(f"CRITICAL: TechnicalTerms.dic not found in any expected location")
        print("REWARD: 0.0")
        return 0.0

    print(f"Found dictionary file: {dict_path}")

    try:
        with open(dict_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        lines = content.strip().split('\n')
    except Exception as e:
        print(f"CRITICAL: Cannot read dictionary file: {e}")
        print("REWARD: 0.0")
        return 0.0

    print(f"Dictionary content ({len(lines)} lines):")
    for i, line in enumerate(lines):
        print(f"  Line {i}: '{line}'")

    # Separate header from entries: entries come after the '---' separator line
    separator_idx = None
    for i, line in enumerate(lines):
        if line.strip() == '---':
            separator_idx = i
            break

    if separator_idx is None:
        print("WARNING: No '---' separator found in dictionary file")
        # The entire file after the header lines might be entries
        # Standard format: first line is "OOoUserDict1", then lang/type lines, then "---", then entries
        entries = []
    else:
        entries = [line.strip() for line in lines[separator_idx + 1:] if line.strip()]

    print(f"Found {len(entries)} dictionary entries after separator")

    # Component 1 (0.4 pts): Dictionary contains a hyphenation entry for 'bioinformatics'
    # An entry containing 'bioinformatics' (with = separators) must exist
    try:
        found_bioinformatics_entry = None
        for entry in entries:
            # Remove = separators and check if it spells 'bioinformatics'
            word = entry.replace('=', '').lower().strip()
            if word == EXPECTED_WORD:
                found_bioinformatics_entry = entry
                break

        if found_bioinformatics_entry is not None:
            print(f"PASS: Component 1 — Found hyphenation entry for 'bioinformatics': '{found_bioinformatics_entry}' (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — No hyphenation entry for 'bioinformatics' found in dictionary entries: {entries}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2 (0.3 pts): The entry uses the correct hyphenation points: bio=in=for=mat=ics
    try:
        if found_bioinformatics_entry is not None:
            # Normalize: strip whitespace and compare
            normalized_entry = found_bioinformatics_entry.strip()
            if normalized_entry == EXPECTED_ENTRY:
                print(f"PASS: Component 2 — Exact hyphenation pattern matches '{EXPECTED_ENTRY}' (0.3 pts)")
                total_score += 0.3
            else:
                # Check if the syllable splits are correct even with different separator
                parts = []
                for sep in ['=', '-']:
                    parts = normalized_entry.split(sep)
                    if len(parts) > 1:
                        break
                if [p.lower() for p in parts] == EXPECTED_SYLLABLES:
                    print(f"PASS: Component 2 — Syllable pattern correct (separator differs): {parts} (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 2 — Expected '{EXPECTED_ENTRY}', found '{normalized_entry}'")
        else:
            print(f"FAIL: Component 2 — No entry found to verify hyphenation pattern")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3 (0.3 pts): Dictionary is properly structured with valid header and entry format
    # The entry must have exactly 4 hyphenation points (5 syllables) using = separator
    try:
        if found_bioinformatics_entry is not None:
            normalized_entry = found_bioinformatics_entry.strip()
            hyphen_count = normalized_entry.count('=')
            if hyphen_count == 4:
                # Verify each syllable part is non-empty
                parts = normalized_entry.split('=')
                all_nonempty = all(len(p) > 0 for p in parts)
                if all_nonempty and len(parts) == 5:
                    print(f"PASS: Component 3 — Entry has correct structure: 5 syllables, 4 hyphenation points (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 3 — Entry parts invalid: {parts}")
            else:
                print(f"FAIL: Component 3 — Expected 4 '=' separators, found {hyphen_count} in '{normalized_entry}'")
        else:
            print(f"FAIL: Component 3 — No entry found to verify structure")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

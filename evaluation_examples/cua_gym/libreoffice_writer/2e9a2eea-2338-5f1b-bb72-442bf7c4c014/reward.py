"""
Reward Script: Concordance file creation for alphabetical index
Task ID: writer_mt_090
Domain: libreoffice_writer
Scoring:
  Component 1 (0.2): terms.sdi file exists and is non-empty
  Component 2 (0.3): File has 50 entries with correct 6-field structure
  Component 3 (0.3): Entries follow concordance format (term;Alt;key1;key2;case;word)
  Component 4 (0.2): Known medical terms are present in the concordance file
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_mt_090'
SDI_PATH = os.path.join(WORKDIR, 'terms.sdi')

# Expected medical terms that should appear in the concordance file
EXPECTED_TERMS = [
    'hypertension', 'diabetes', 'asthma', 'pneumonia', 'tuberculosis',
    'stroke', 'epilepsy', 'arrhythmia', 'atherosclerosis', 'anemia',
    'cirrhosis', 'pancreatitis', 'osteoarthritis', 'osteoporosis', 'melanoma',
    'psoriasis', 'eczema', 'anaphylaxis', 'sepsis', 'leukemia',
    'lymphoma', 'influenza', 'emphysema', 'bronchitis', 'edema',
]


def verify_task():
    """
    Verify concordance file creation with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: terms.sdi file exists and is non-empty (0.2 points)
    try:
        if os.path.isfile(SDI_PATH):
            file_size = os.path.getsize(SDI_PATH)
            if file_size > 0:
                print(f"PASS: Component 1 — terms.sdi exists and is non-empty ({file_size} bytes) (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 1 — terms.sdi exists but is empty")
        else:
            print(f"FAIL: Component 1 — terms.sdi not found at {SDI_PATH}")
            # No file means nothing else to check
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Read all lines from the file
    try:
        with open(SDI_PATH, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except Exception as e:
        print(f"ERROR: Cannot read {SDI_PATH}: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: File has ~50 entries, each with exactly 6 semicolon-separated fields (0.3 points)
    try:
        valid_entries = 0
        for line in lines:
            parts = line.split(';')
            if len(parts) == 6:
                valid_entries += 1

        entry_count_ok = (45 <= len(lines) <= 55)  # Allow small tolerance around 50
        format_ratio = valid_entries / len(lines) if len(lines) > 0 else 0

        if entry_count_ok and format_ratio >= 0.9:
            print(f"PASS: Component 2 — {len(lines)} entries, {valid_entries} valid 6-field format (0.3 pts)")
            total_score += 0.3
        elif entry_count_ok or format_ratio >= 0.9:
            # Partial: either count or format is right but not both
            print(f"PARTIAL: Component 2 — {len(lines)} entries (need ~50), {valid_entries}/{len(lines)} valid format (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — {len(lines)} entries (need ~50), {valid_entries}/{len(lines)} valid format")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Entries follow concordance format correctly (0.3 points)
    # Format: search_term;alternative_entry;1st_key;2nd_key;match_case(0/1);word_only(0/1)
    try:
        well_formed = 0
        for line in lines:
            parts = line.split(';')
            if len(parts) != 6:
                continue
            search_term = parts[0].strip()
            alt_entry = parts[1].strip()
            key1 = parts[2].strip()
            key2 = parts[3].strip()
            match_case = parts[4].strip()
            word_only = parts[5].strip()

            # Validate: search_term is non-empty, match_case and word_only are 0 or 1
            if (search_term and
                alt_entry and
                key1 and
                match_case in ('0', '1') and
                word_only in ('0', '1')):
                well_formed += 1

        ratio = well_formed / len(lines) if len(lines) > 0 else 0
        if ratio >= 0.9:
            print(f"PASS: Component 3 — {well_formed}/{len(lines)} entries well-formed concordance format (0.3 pts)")
            total_score += 0.3
        elif ratio >= 0.5:
            print(f"PARTIAL: Component 3 — {well_formed}/{len(lines)} entries well-formed (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — only {well_formed}/{len(lines)} entries well-formed")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Known medical terms are present (0.2 points)
    try:
        # Extract search terms (first field) from all entries, lowercased
        found_terms = set()
        for line in lines:
            parts = line.split(';')
            if len(parts) >= 1:
                found_terms.add(parts[0].strip().lower())

        matched = sum(1 for t in EXPECTED_TERMS if t in found_terms)
        match_ratio = matched / len(EXPECTED_TERMS)

        if match_ratio >= 0.8:
            print(f"PASS: Component 4 — {matched}/{len(EXPECTED_TERMS)} expected medical terms found (0.2 pts)")
            total_score += 0.2
        elif match_ratio >= 0.4:
            print(f"PARTIAL: Component 4 — {matched}/{len(EXPECTED_TERMS)} expected medical terms found (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 4 — only {matched}/{len(EXPECTED_TERMS)} expected medical terms found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

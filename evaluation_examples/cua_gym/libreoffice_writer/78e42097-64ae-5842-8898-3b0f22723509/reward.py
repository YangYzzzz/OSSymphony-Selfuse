"""
Reward Script: Custom dictionary with product-specific terms for spell checker
Task ID: writer_tech_094
Domain: libreoffice_writer
Scoring: 0.2 points per term found in any custom dictionary file (5 terms x 0.2 = 1.0)
"""

import os
import glob

WORKDIR = '/home/user'
TASK_ID = 'writer_tech_094'

# The 5 product-specific terms that must be in a custom dictionary
REQUIRED_TERMS = ['CloudSync', 'DataMesh', 'AutoScale', 'NetGuard', 'LogStream']

# Points per term
POINTS_PER_TERM = 0.2

def get_all_dic_contents():
    """
    Read all .dic files from LibreOffice custom dictionary locations.
    Returns a set of all words found across all dictionary files.
    """
    all_words = set()

    # Primary location for LibreOffice user dictionaries
    wordbook_patterns = [
        os.path.join(WORKDIR, '.config/libreoffice/4/user/wordbook/*.dic'),
        os.path.join(WORKDIR, '.config/libreoffice/4/user/wordbook/*.DIC'),
        # Also check common alternative locations
        os.path.join(WORKDIR, '.config/libreoffice/*/user/wordbook/*.dic'),
    ]

    dic_files_found = []
    for pattern in wordbook_patterns:
        dic_files_found.extend(glob.glob(pattern))

    # Remove duplicates
    dic_files_found = list(set(dic_files_found))

    if not dic_files_found:
        print("INFO: No .dic files found in any wordbook directory")
        return all_words, []

    for dic_path in dic_files_found:
        try:
            with open(dic_path, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()
            print(f"INFO: Reading dictionary file: {dic_path} ({len(lines)} lines)")
            for line in lines:
                word = line.strip()
                # Skip header lines and empty lines
                if word and not word.startswith('OOoUserDict') and not word.startswith('lang:') and not word.startswith('type:') and word != '---':
                    all_words.add(word)
        except Exception as e:
            print(f"WARN: Could not read {dic_path}: {e}")

    return all_words, dic_files_found


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Collect all words from all custom dictionary files
    all_words, dic_files = get_all_dic_contents()

    if not dic_files:
        print("FAIL: No custom dictionary files found — no terms can be verified")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    print(f"INFO: Found {len(dic_files)} dictionary file(s) with {len(all_words)} unique word(s)")
    print(f"INFO: Words in dictionaries: {sorted(all_words)}")

    # Components 1-5: Each required term present in at least one dictionary (0.2 pts each)
    for i, term in enumerate(REQUIRED_TERMS, 1):
        try:
            if term in all_words:
                print(f"PASS: Component {i} — '{term}' found in custom dictionary ({POINTS_PER_TERM} pts)")
                total_score += POINTS_PER_TERM
            else:
                # Also check case-insensitive as a fallback
                lower_words = {w.lower() for w in all_words}
                if term.lower() in lower_words:
                    print(f"PASS: Component {i} — '{term}' found (case-insensitive match) ({POINTS_PER_TERM} pts)")
                    total_score += POINTS_PER_TERM
                else:
                    print(f"FAIL: Component {i} — '{term}' NOT found in any custom dictionary")
        except Exception as e:
            print(f"ERROR: Component {i} — could not check '{term}': {e}")

    # Round to avoid floating point issues
    total_score = round(total_score, 2)
    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

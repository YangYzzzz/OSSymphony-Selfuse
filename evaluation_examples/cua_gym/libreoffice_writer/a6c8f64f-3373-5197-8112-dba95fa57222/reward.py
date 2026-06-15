"""
Reward Script: Create a custom dictionary named 'LegalTerms' for legal jargon
Task ID: writer_fp_035
Domain: libreoffice_writer
Scoring:
  Component 1 (0.30): LegalTerms.dic file exists with correct name
  Component 2 (0.25): Dictionary language is set to en-US (not 'All')
  Component 3 (0.30): Dictionary contains at least 20 legal terms from the expected list
  Component 4 (0.15): Dictionary is registered in LibreOffice configuration
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_fp_035'

# The 20 expected legal terms from the task specification
EXPECTED_TERMS = {
    'indemnification', 'subrogation', 'estoppel', 'tortfeasor', 'demurrer',
    'adjudication', 'arbitrable', 'counterclaim', 'deposition', 'fiduciary',
    'habeas', 'injunctive', 'jurisprudence', 'lien', 'malfeasance',
    'negligence', 'obligee', 'plaintiff', 'quorum', 'rescission'
}

# Path where LibreOffice stores custom dictionaries
DIC_DIR = os.path.join(WORKDIR, '.config', 'libreoffice', '4', 'user', 'wordbook')
DIC_PATH = os.path.join(DIC_DIR, 'LegalTerms.dic')
REGISTRY_PATH = os.path.join(WORKDIR, '.config', 'libreoffice', '4', 'user', 'registrymodifications.xcu')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: LegalTerms.dic file exists (0.30 points)
    # This checks that a custom dictionary named 'LegalTerms' was created.
    # On initial_env, no .dic files exist in the wordbook directory.
    try:
        if os.path.isfile(DIC_PATH):
            # Read contents to verify it's a valid dictionary file
            with open(DIC_PATH, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read().strip()
            # Must have the OOoUserDict1 header to be a valid LO dictionary
            if 'OOoUserDict1' in content:
                print(f"PASS: Component 1 — LegalTerms.dic exists and is a valid LO dictionary (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 1 — LegalTerms.dic exists but missing OOoUserDict1 header")
        else:
            print(f"FAIL: Component 1 — LegalTerms.dic not found at {DIC_PATH}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Dictionary language is en-US (0.25 points)
    # Task requires dictionary assigned to English (US) only, not 'All' languages.
    # On initial_env, no dictionary file exists so this will fail.
    try:
        if os.path.isfile(DIC_PATH):
            with open(DIC_PATH, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()
            # The lang line should be "lang: en-US" or "lang: <EMPTY>" for All
            lang_found = False
            for line in lines:
                stripped = line.strip().lower()
                if stripped.startswith('lang:'):
                    lang_value = line.strip().split(':', 1)[1].strip()
                    if lang_value.lower() in ('en-us', 'en_us'):
                        print(f"PASS: Component 2 — Dictionary language is '{lang_value}' (English US) (0.25 pts)")
                        total_score += 0.25
                        lang_found = True
                    else:
                        print(f"FAIL: Component 2 — Dictionary language is '{lang_value}', expected 'en-US'")
                        lang_found = True
                    break
            if not lang_found:
                print(f"FAIL: Component 2 — No 'lang:' header found in dictionary file")
        else:
            print(f"FAIL: Component 2 — LegalTerms.dic not found, cannot check language")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Dictionary contains at least 20 legal terms (0.30 points)
    # On initial_env, no dictionary exists so this will fail.
    # Progressive: 0.15 for >=10 terms, 0.30 for >=20 terms
    try:
        if os.path.isfile(DIC_PATH):
            with open(DIC_PATH, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()
            # Words start after the header lines (OOoUserDict1, lang:, type:, ---)
            words = set()
            in_words = False
            for line in lines:
                stripped = line.strip().lower()
                if stripped == '---':
                    in_words = True
                    continue
                if in_words and stripped:
                    words.add(stripped)

            matched = words & {t.lower() for t in EXPECTED_TERMS}
            total_words = len(words)
            matched_count = len(matched)

            if total_words >= 20 and matched_count >= 15:
                print(f"PASS: Component 3 — Dictionary has {total_words} words, {matched_count} match expected terms (0.30 pts)")
                total_score += 0.30
            elif total_words >= 10 and matched_count >= 8:
                print(f"PARTIAL: Component 3 — Dictionary has {total_words} words, {matched_count} match expected terms (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — Dictionary has {total_words} words, {matched_count} match expected terms (need >=20 words, >=15 matches)")
        else:
            print(f"FAIL: Component 3 — LegalTerms.dic not found, cannot check terms")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Dictionary is registered in LibreOffice configuration (0.15 points)
    # On initial_env, there's no DictionaryList entry referencing LegalTerms.
    try:
        if os.path.isfile(REGISTRY_PATH):
            with open(REGISTRY_PATH, 'r', encoding='utf-8', errors='replace') as f:
                registry_content = f.read()
            if 'LegalTerms.dic' in registry_content:
                print(f"PASS: Component 4 — LegalTerms.dic is registered in LibreOffice config (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — LegalTerms.dic not found in registrymodifications.xcu")
        else:
            print(f"FAIL: Component 4 — registrymodifications.xcu not found at {REGISTRY_PATH}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

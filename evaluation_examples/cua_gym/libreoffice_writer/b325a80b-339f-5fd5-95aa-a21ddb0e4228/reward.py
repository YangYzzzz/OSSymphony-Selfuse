"""
Reward Script: Create an alphabetical index for the master document
Task ID: writer_rm_070
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): alphabetical-index element exists in the ODM
  Component 2 (0.3): index has sufficient entries (>=40 from all subdocuments)
  Component 3 (0.2): entries are sorted alphabetically (case-insensitive)
  Component 4 (0.2): entries span multiple subject disciplines (>=8 of 10)
"""

import os
import re
import zipfile

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_070'


def verify_task(file_path):
    """
    Verify that an alphabetical index has been inserted into the master document.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the ODM file (ODF format = ZIP archive)
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            content_xml = z.read('content.xml').decode('utf-8')
    except Exception as e:
        print(f"CRITICAL: Cannot load ODM file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: alphabetical-index element exists (0.3 points)
    # This is the core structural change — the initial file has no index at all.
    try:
        has_alpha_index = 'alphabetical-index' in content_xml
        # Also check for the index-body which contains the actual entries
        has_index_body = 'index-body' in content_xml
        if has_alpha_index and has_index_body:
            print(f"PASS: Component 1 — alphabetical-index element with index-body found (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — alphabetical-index element not found (has_alpha_index={has_alpha_index}, has_index_body={has_index_body})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: index has sufficient entries (0.3 points)
    # The golden file has 86 entries from all 10 subdocuments.
    # We expect at least 40 entries for a valid comprehensive index.
    try:
        # Extract text paragraphs inside the index-body
        # Pattern: entries are <text:p>TERM\tPAGE</text:p> inside <text:index-body>
        index_body_match = re.search(
            r'<text:index-body>(.*?)</text:index-body>',
            content_xml,
            re.DOTALL
        )
        if index_body_match:
            index_body_content = index_body_match.group(1)
            # Extract all entry paragraphs (skip the title paragraph)
            all_entries_raw = re.findall(r'<text:p[^>]*>([^<]+)</text:p>', index_body_content)
            # Filter out the title "Alphabetical Index" and any empty entries
            index_entries = []
            for entry in all_entries_raw:
                entry_stripped = entry.strip()
                if entry_stripped and entry_stripped.lower() != 'alphabetical index':
                    index_entries.append(entry_stripped)

            num_entries = len(index_entries)
            print(f"INFO: Found {num_entries} index entries")

            if num_entries >= 40:
                print(f"PASS: Component 2 — {num_entries} entries found (>=40 required) (0.3 pts)")
                total_score += 0.3
            elif num_entries >= 20:
                partial = 0.15
                print(f"PARTIAL: Component 2 — {num_entries} entries found (20-39 range) ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — only {num_entries} entries found (need >=40)")
        else:
            print(f"FAIL: Component 2 — no index-body found in the document")
            index_entries = []
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")
        index_entries = []

    # Component 3: entries are sorted alphabetically (0.2 points)
    # The task requires an alphabetical index, so entries should be in order.
    try:
        if len(index_entries) >= 10:
            # Extract just the term part (before the tab character for page number)
            terms = []
            for entry in index_entries:
                term = entry.split('\t')[0].strip()
                if term:
                    terms.append(term)

            # Check if terms are sorted case-insensitively
            sorted_terms = sorted(terms, key=lambda x: x.lower())
            is_sorted = (terms == sorted_terms)

            if is_sorted:
                print(f"PASS: Component 3 — {len(terms)} entries are alphabetically sorted (0.2 pts)")
                total_score += 0.2
            else:
                # Count how many are in correct position
                correct_positions = sum(1 for a, b in zip(terms, sorted_terms) if a == b)
                ratio = correct_positions / len(terms)
                if ratio >= 0.8:
                    partial = 0.1
                    print(f"PARTIAL: Component 3 — {ratio:.0%} of entries in correct position ({partial} pts)")
                    total_score += partial
                else:
                    print(f"FAIL: Component 3 — entries not alphabetically sorted (only {ratio:.0%} correct)")
                    # Show first few mismatches
                    mismatches = [(i, terms[i], sorted_terms[i]) for i in range(min(5, len(terms))) if terms[i] != sorted_terms[i]]
                    for idx, actual, expected in mismatches:
                        print(f"  Position {idx}: found '{actual}', expected '{expected}'")
        else:
            print(f"FAIL: Component 3 — too few entries ({len(index_entries)}) to evaluate sorting")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: entries span multiple subject disciplines (0.2 points)
    # The 10 subdocuments cover: astronomy, biology, chemistry, geography, history,
    # mathematics, physics, technology, medicine, ecology.
    # We check that the index includes terms recognizable from at least 8 disciplines.
    try:
        if len(index_entries) >= 10:
            all_terms_lower = ' '.join(index_entries).lower()

            # Representative keywords from each discipline
            discipline_markers = {
                'astronomy': ['astronomy', 'galaxies', 'stars', 'planets', 'nebulae', 'solar system', 'milky way', 'telescope', 'hubble'],
                'biology': ['biology', 'dna', 'enzymes', 'photosynthesis', 'chlorophyll', 'metabolism', 'molecular biology'],
                'chemistry': ['chemistry', 'chemical bonds', 'catalysts', 'periodic table', 'atomic number', 'covalent', 'molecules'],
                'geography': ['geography', 'tectonic', 'earthquakes', 'volcanic', 'amazon river', 'climate', 'physical geography'],
                'history': ['history', 'renaissance', 'mesopotamia', 'egypt', 'industrial revolution', 'cultural rebirth', 'writing systems'],
                'mathematics': ['mathematics', 'algebra', 'calculus', 'geometry', 'pythagorean', 'euclidean', 'probability', 'bayesian', 'statistics'],
                'physics': ['physics', 'gravity', 'forces', 'newton', 'quantum mechanics', 'relativity', 'einstein', 'uncertainty principle'],
                'technology': ['technology', 'artificial intelligence', 'machine learning', 'internet', 'transistor', 'integrated circuits', 'world wide web', 'tim berners-lee'],
                'medicine': ['medicine', 'antibiotics', 'vaccination', 'penicillin', 'smallpox', 'alexander fleming', 'dna sequencing', 'genomic medicine', 'precision medicine'],
                'ecology': ['ecology', 'ecosystems', 'biodiversity', 'food chains', 'food webs', 'trophic levels', 'habitat loss', 'conservation biology', 'endangered species', 'tropical rainforest'],
            }

            disciplines_covered = 0
            for discipline, markers in discipline_markers.items():
                if any(marker in all_terms_lower for marker in markers):
                    disciplines_covered += 1
                    print(f"  INFO: Discipline '{discipline}' represented in index")

            print(f"INFO: {disciplines_covered}/10 disciplines covered")

            if disciplines_covered >= 8:
                print(f"PASS: Component 4 — {disciplines_covered}/10 disciplines covered (>=8 required) (0.2 pts)")
                total_score += 0.2
            elif disciplines_covered >= 5:
                partial = 0.1
                print(f"PARTIAL: Component 4 — {disciplines_covered}/10 disciplines covered (5-7 range) ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 — only {disciplines_covered}/10 disciplines covered")
        else:
            print(f"FAIL: Component 4 — too few entries to evaluate discipline coverage")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.odm'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

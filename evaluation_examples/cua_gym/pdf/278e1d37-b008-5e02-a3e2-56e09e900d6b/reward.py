"""
Reward Script: Academic paper title page PDF creation
Task ID: pdf_res_046
Domain: pdf
Scoring:
  Component 1 (0.20): Title "Scalable Methods for Graph Neural Networks" present
  Component 2 (0.25): All three author names present
  Component 3 (0.15): Affiliation "Stanford University" present
  Component 4 (0.25): Abstract section with substantial text (~200 words)
  Component 5 (0.15): Keywords line with all three required keywords
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_046'
FILE_PATH = os.path.join(WORKDIR, 'papers', 'gnn_title_page.pdf')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be loadable
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import fitz
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: page count must be 1-2
    page_count = doc.page_count
    if page_count < 1 or page_count > 5:
        print(f"CRITICAL: Unexpected page count: {page_count} (expected 1-2)")
        print("REWARD: 0.0")
        doc.close()
        return 0.0

    # Extract all text from the document
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    doc.close()

    full_text_lower = full_text.lower()

    # Component 1: Title text present (0.20 points)
    try:
        title = "scalable methods for graph neural networks"
        if title in full_text_lower:
            print(f"PASS: Component 1 - Title found: 'Scalable Methods for Graph Neural Networks' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 - Title 'Scalable Methods for Graph Neural Networks' not found in text")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: All three author names present (0.25 points)
    try:
        authors = ["wei liu", "priya sharma", "thomas mueller"]
        found_authors = []
        missing_authors = []
        for author in authors:
            if author in full_text_lower:
                found_authors.append(author)
            else:
                missing_authors.append(author)

        if len(found_authors) == 3:
            print(f"PASS: Component 2 - All 3 authors found: {found_authors} (0.25 pts)")
            total_score += 0.25
        elif len(found_authors) >= 1:
            partial = round(0.25 * len(found_authors) / 3, 2)
            print(f"PARTIAL: Component 2 - Found {len(found_authors)}/3 authors. Missing: {missing_authors} ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 - No authors found. Expected: {authors}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Affiliation "Stanford University" present (0.15 points)
    try:
        if "stanford university" in full_text_lower:
            print(f"PASS: Component 3 - Affiliation 'Stanford University' found (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 - 'Stanford University' not found in text")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Abstract section with substantial text (~200 words) (0.25 points)
    try:
        has_abstract_label = "abstract" in full_text_lower
        # Extract text after "abstract" keyword to count words
        abstract_idx = full_text_lower.find("abstract")
        if abstract_idx >= 0:
            # Get text after the abstract heading
            abstract_text = full_text[abstract_idx + len("abstract"):].strip()
            # Remove the keywords section if present
            keywords_idx = abstract_text.lower().find("keywords")
            if keywords_idx >= 0:
                abstract_body = abstract_text[:keywords_idx].strip()
            else:
                abstract_body = abstract_text.strip()
            word_count = len(abstract_body.split())

            if word_count >= 150:
                print(f"PASS: Component 4 - Abstract found with {word_count} words (>= 150 threshold) (0.25 pts)")
                total_score += 0.25
            elif word_count >= 80:
                partial = 0.15
                print(f"PARTIAL: Component 4 - Abstract found but only {word_count} words (expected ~200) ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 - Abstract text too short: {word_count} words (expected ~200)")
        else:
            print(f"FAIL: Component 4 - No 'Abstract' section found in document")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Keywords line with all three required keywords (0.15 points)
    try:
        required_keywords = ["graph neural networks", "scalability", "distributed computing"]
        found_kw = []
        missing_kw = []
        for kw in required_keywords:
            if kw in full_text_lower:
                found_kw.append(kw)
            else:
                missing_kw.append(kw)

        if len(found_kw) == 3:
            print(f"PASS: Component 5 - All 3 keywords found: {found_kw} (0.15 pts)")
            total_score += 0.15
        elif len(found_kw) >= 1:
            partial = round(0.15 * len(found_kw) / 3, 2)
            print(f"PARTIAL: Component 5 - Found {len(found_kw)}/3 keywords. Missing: {missing_kw} ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 - No required keywords found. Expected: {required_keywords}")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

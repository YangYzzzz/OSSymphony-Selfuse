"""
Reward Script: Add two references to a literature review and insert reference numbers in conclusion
Task ID: osworld_writer_biblio_010
Domain: libreoffice_writer

Scoring:
  Component 1: Reference 11 (Brown et al. 2020) added to References section         — 0.35 pts
  Component 2: Reference 12 (Bommasani et al. 2021) added to References section      — 0.35 pts
  Component 3: '<cite A>' replaced with '(11)' in conclusion paragraph               — 0.15 pts
  Component 4: '<cite B>' replaced with '(12)' in conclusion paragraph               — 0.15 pts
  Total: 1.0
"""

import os
from docx import Document

WORKDIR = '/home/user'
FILE_PATH = os.path.join(WORKDIR, 'ai_literature_review.docx')


def find_paragraph_with(all_texts, starts_with, *contains_tokens):
    """Return first paragraph text that starts with the given prefix and contains all tokens."""
    for text in all_texts:
        t = text.strip()
        if t.startswith(starts_with) and all(token in t for token in contains_tokens):
            return t
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.

    Checks:
    1. Reference 11 (Brown et al. 2020) is present in the references section.
    2. Reference 12 (Bommasani et al. 2021) is present in the references section.
    3. '<cite A>' placeholder is replaced by '(11)' in the conclusion paragraph.
    4. '<cite B>' placeholder is replaced by '(12)' in the conclusion paragraph.

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all paragraph texts once for efficient searching
    all_texts = [para.text for para in doc.paragraphs]

    # ---- Component 1: Reference 11 (Brown et al. 2020) added (0.35 points) ----
    # The entry must start with '11.' and contain key identifying tokens for Brown 2020 GPT-3 paper
    try:
        ref11_match = find_paragraph_with(all_texts, '11.', 'Brown', '2020', 'few-shot')
        if ref11_match is None:
            # Looser match: just starts with 11. and has Brown + 2020
            ref11_match = find_paragraph_with(all_texts, '11.', 'Brown', '2020')

        if ref11_match is not None:
            print(f"PASS: Component 1 — Reference 11 found: {ref11_match[:90]}...")
            total_score += 0.35
        else:
            print("FAIL: Component 1 — Reference 11 not found. Expected paragraph starting with "
                  "'11. Brown, T. B., Mann, B., & Ryder, N. (2020). Language models are few-shot learners.'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ---- Component 2: Reference 12 (Bommasani et al. 2021) added (0.35 points) ----
    # The entry must start with '12.' and contain identifying tokens for Bommasani 2021 foundation models paper
    try:
        ref12_match = find_paragraph_with(all_texts, '12.', 'Bommasani', '2021', 'foundation models')
        if ref12_match is None:
            ref12_match = find_paragraph_with(all_texts, '12.', 'Bommasani', '2021')

        if ref12_match is not None:
            print(f"PASS: Component 2 — Reference 12 found: {ref12_match[:90]}...")
            total_score += 0.35
        else:
            print("FAIL: Component 2 — Reference 12 not found. Expected paragraph starting with "
                  "'12. Bommasani, R., Hudson, D. A., & Aditi, E. (2021). On the opportunities and risks...'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ---- Component 3: '<cite A>' replaced with '(11)' in conclusion (0.15 points) ----
    # Verify: placeholder is gone AND (11) appears in a conclusion-context sentence
    try:
        placeholder_a_gone = not any('<cite A>' in t or '<cite a>' in t.lower() for t in all_texts)
        citation_11_in_conclusion = any(
            '(11)' in t and ('few-shot' in t.lower() or 'foundation model' in t.lower())
            for t in all_texts
        )

        if placeholder_a_gone and citation_11_in_conclusion:
            print("PASS: Component 3 — '<cite A>' replaced with '(11)' in conclusion paragraph")
            total_score += 0.15
        elif not placeholder_a_gone:
            print("FAIL: Component 3 — '<cite A>' placeholder still present in document; not replaced")
        else:
            print("FAIL: Component 3 — '<cite A>' gone but '(11)' not found in expected conclusion context")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ---- Component 4: '<cite B>' replaced with '(12)' in conclusion (0.15 points) ----
    try:
        placeholder_b_gone = not any('<cite B>' in t or '<cite b>' in t.lower() for t in all_texts)
        citation_12_in_conclusion = any(
            '(12)' in t and ('foundation model' in t.lower() or 'few-shot' in t.lower())
            for t in all_texts
        )

        if placeholder_b_gone and citation_12_in_conclusion:
            print("PASS: Component 4 — '<cite B>' replaced with '(12)' in conclusion paragraph")
            total_score += 0.15
        elif not placeholder_b_gone:
            print("FAIL: Component 4 — '<cite B>' placeholder still present in document; not replaced")
        else:
            print("FAIL: Component 4 — '<cite B>' gone but '(12)' not found in expected conclusion context")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

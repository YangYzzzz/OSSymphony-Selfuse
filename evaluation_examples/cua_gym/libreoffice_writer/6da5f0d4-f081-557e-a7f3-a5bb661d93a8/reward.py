"""
Reward Script: Split first paragraph into one-sentence-per-paragraph with empty line separators
Task ID: osworld_writer_spacing_007
Domain: libreoffice_writer
Scoring:
  Component 1 (0.50): 11 individual sentence paragraphs found in passage section (was 1 block)
  Component 2 (0.30): At least 10 empty separator paragraphs between sentences
  Component 3 (0.20): Sentence text content integrity — each of the 11 passage paragraphs
                      matches one of the expected sentences from the original passage
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_spacing_007'

# Expected sentences from the original passage (first paragraph in initial document)
EXPECTED_SENTENCES = [
    "The Amazon rainforest covers over 5.5 million square kilometers.",
    "It is home to more than three million species of plants, animals, and insects.",
    "Scientists discover hundreds of new species in this region each year.",
    "The forest produces approximately 20 percent of the world's oxygen supply.",
    "Many indigenous communities have lived in the Amazon for thousands of years.",
    "Their traditional knowledge of medicinal plants is invaluable to modern medicine.",
    "Deforestation threatens the survival of both wildlife and human communities in the region.",
    "Each year, millions of acres of rainforest are lost to logging and agriculture.",
    "The loss of tree cover contributes significantly to global climate change.",
    "International conservation efforts have slowed but not stopped this destruction.",
    "Protecting the Amazon requires cooperation between governments, communities, and scientists worldwide.",
]

EXPECTED_SENTENCE_COUNT = 11
EXPECTED_EMPTY_SEPARATOR_MIN = 10  # Need at least 10 empty paragraphs between 11 sentences


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Task: Split the first paragraph (11-sentence passage) so each sentence
    is on its own paragraph with an empty paragraph separator between sentences.
    The passage goes from 1 block paragraph to 11 individual paragraphs.
    Questions section after the passage must remain unchanged.
    """
    total_score = 0.0

    # Load the document
    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paragraphs = doc.paragraphs
    if len(paragraphs) < 5:
        print(f"FAIL: Document has too few paragraphs ({len(paragraphs)})")
        print("REWARD: 0.0")
        return 0.0

    # Locate the "Questions:" paragraph to bound the passage section
    # The passage begins at paragraph index 3 (after title, subtitle, directions)
    passage_start = 3
    questions_idx = None
    for i, p in enumerate(paragraphs):
        if p.text.strip() == 'Questions:':
            questions_idx = i
            break

    if questions_idx is None:
        print("FAIL: 'Questions:' paragraph not found — document structure corrupted")
        print("REWARD: 0.0")
        return 0.0

    # Collect non-empty paragraphs in the passage section
    sentence_paras = []
    empty_count = 0
    for i in range(passage_start, questions_idx):
        p = paragraphs[i]
        if p.text.strip():
            sentence_paras.append(p.text.strip())
        else:
            empty_count += 1

    actual_sentence_count = len(sentence_paras)

    # --- Component 1: 11 individual sentence paragraphs in passage section (0.50 pts) ---
    # Initial state: 1 block paragraph containing all 11 sentences.
    # Golden state: 11 individual sentence paragraphs (count == 11).
    # This FAILS on initial (1 paragraph) and PASSES on golden (11 paragraphs).
    try:
        if actual_sentence_count == EXPECTED_SENTENCE_COUNT:
            print(f"PASS: Component 1 — {actual_sentence_count} sentence paragraphs found in passage section (0.5 pts)")
            total_score += 0.5
        elif actual_sentence_count >= 8:
            partial = 0.25
            print(f"PARTIAL: Component 1 — {actual_sentence_count}/{EXPECTED_SENTENCE_COUNT} sentence paragraphs found in passage ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — Expected {EXPECTED_SENTENCE_COUNT} sentence paragraphs, found {actual_sentence_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # --- Component 2: At least 10 empty separator paragraphs between sentences (0.30 pts) ---
    # Initial state: 1 empty paragraph exists (Para 4 in initial document — pre-existing blank line).
    # Golden state: 11 empty separator paragraphs between/after sentences.
    # This FAILS on initial (1 empty separator) and PASSES on golden (>= 10).
    try:
        if empty_count >= EXPECTED_EMPTY_SEPARATOR_MIN:
            print(f"PASS: Component 2 — {empty_count} empty separator paragraphs found (>= {EXPECTED_EMPTY_SEPARATOR_MIN}) (0.3 pts)")
            total_score += 0.3
        elif empty_count >= 5:
            partial = 0.15
            print(f"PARTIAL: Component 2 — {empty_count} empty separator paragraphs found (expected >= {EXPECTED_EMPTY_SEPARATOR_MIN}) ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Expected >= {EXPECTED_EMPTY_SEPARATOR_MIN} empty separator paragraphs, found {empty_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # --- Component 3: Sentence text integrity — all 11 expected sentences present (0.20 pts) ---
    # Each of the 11 sentence paragraphs should match one of the expected sentences.
    # Initial state: passage is in 1 block — no individual sentence paragraphs exist to match.
    # Golden state: 11 sentence paragraphs, each matching one expected sentence.
    # This FAILS on initial (single block != any individual sentence) and PASSES on golden.
    try:
        if actual_sentence_count == EXPECTED_SENTENCE_COUNT:
            # Check how many of the expected sentences are present (exact match)
            matched = 0
            for expected in EXPECTED_SENTENCES:
                if expected in sentence_paras:
                    matched += 1

            if matched == EXPECTED_SENTENCE_COUNT:
                print(f"PASS: Component 3 — All {matched} expected sentences present as individual paragraphs (0.2 pts)")
                total_score += 0.2
            elif matched >= 8:
                partial = 0.10
                print(f"PARTIAL: Component 3 — {matched}/{EXPECTED_SENTENCE_COUNT} expected sentences matched ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — Only {matched}/{EXPECTED_SENTENCE_COUNT} expected sentences matched individual paragraphs")
        else:
            print(f"FAIL: Component 3 — Skipped because sentence count ({actual_sentence_count}) != {EXPECTED_SENTENCE_COUNT}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

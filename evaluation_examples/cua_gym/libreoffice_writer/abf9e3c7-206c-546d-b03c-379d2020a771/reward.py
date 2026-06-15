"""
Reward Script: Add empty line after each sentence in first paragraph of study_guide_rules.docx
Task ID: osworld_writer_spacing_002
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): First paragraph split into exactly 6 individual sentence paragraphs
  Component 2 (0.3): Empty paragraph (blank line) inserted after each of the 6 sentences
  Component 3 (0.2): Remaining document sections (Heading 2 sections) are unchanged
    - Only passes if sentences were also split (compound check anchored to the task change)
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_spacing_002'

# The 6 expected sentences from the first paragraph (ground truth from context)
EXPECTED_SENTENCES = [
    'Always cite your sources.',
    'Use double spacing throughout.',
    'Margins must be 1 inch on all sides.',
    'Include a title page.',
    'Number all pages.',
    'Submit via the course portal.',
]

# Expected remaining section headings (should be unchanged after splitting)
EXPECTED_LATER_HEADINGS = [
    'Formatting Guidelines',
    'Citation Requirements',
    'Submission Instructions',
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print("CRITICAL: Cannot load file {}: {}".format(file_path, e))
        print("REWARD: 0.0")
        return 0.0

    paragraphs = doc.paragraphs

    # --- Component 1: First paragraph split into 6 individual sentence paragraphs (0.5 pts) ---
    # In initial state, all 6 sentences are in ONE paragraph.
    # In golden state, each sentence must be its own separate paragraph.
    # FAILS on initial (1 combined paragraph), PASSES on golden (6 separate paragraphs).
    try:
        # Collect all non-empty paragraph texts after the Heading 1 (Para[0])
        # up until the next Heading section
        sentence_paragraphs = []
        for para in paragraphs[1:]:
            if para.style.name.startswith('Heading'):
                break
            text = para.text.strip()
            if text:
                sentence_paragraphs.append(text)

        # Check: exactly 6 non-empty paragraphs, all matching the expected sentences
        matched_sentences = 0
        for expected in EXPECTED_SENTENCES:
            if expected in sentence_paragraphs:
                matched_sentences += 1

        if matched_sentences == 6 and len(sentence_paragraphs) == 6:
            print("PASS: Component 1 — all 6 sentences are individual paragraphs (0.5 pts)")
            total_score += 0.5
        elif matched_sentences >= 3:
            # Partial credit: some sentences split but not all
            partial = round(0.5 * matched_sentences / 6, 2)
            print("PARTIAL: Component 1 — {}/6 sentences split into individual paragraphs ({} pts)".format(
                matched_sentences, partial))
            total_score += partial
        else:
            print("FAIL: Component 1 — expected 6 individual sentence paragraphs, found {} non-empty paragraphs in first section".format(
                len(sentence_paragraphs)))
    except Exception as e:
        print("ERROR: Component 1 — {}".format(e))

    # --- Component 2: Empty paragraph after each sentence (0.3 pts) ---
    # After each sentence paragraph, there must be an empty paragraph (blank line).
    # Pattern in golden: [sentence, empty, sentence, empty, ..., sentence, empty] = 12 paragraphs
    # FAILS on initial (only 1 paragraph in section, no empty lines), PASSES on golden.
    try:
        # Find paragraphs from start of first section until next Heading
        start_idx = 1  # after the Heading 1
        section_paragraphs = []
        for i, para in enumerate(paragraphs[start_idx:], start=start_idx):
            if para.style.name.startswith('Heading'):
                break
            section_paragraphs.append((i, para.text.strip()))

        # Check alternating pattern: positions 0,2,4,6,8,10 should be sentence text
        # positions 1,3,5,7,9,11 should be empty strings
        empty_after_sentence_count = 0
        if len(section_paragraphs) >= 12:
            for j in range(0, 12, 2):
                sentence_text = section_paragraphs[j][1]
                empty_text = section_paragraphs[j + 1][1]
                if sentence_text and empty_text == '':
                    empty_after_sentence_count += 1

            if empty_after_sentence_count == 6:
                print("PASS: Component 2 — empty paragraph after each of 6 sentences (0.3 pts)")
                total_score += 0.3
            elif empty_after_sentence_count >= 3:
                partial = round(0.3 * empty_after_sentence_count / 6, 2)
                print("PARTIAL: Component 2 — {}/6 sentence-empty pairs found ({} pts)".format(
                    empty_after_sentence_count, partial))
                total_score += partial
            else:
                print("FAIL: Component 2 — only {}/6 empty paragraphs correctly placed after sentences".format(
                    empty_after_sentence_count))
        else:
            print("FAIL: Component 2 — expected at least 12 paragraphs (6 sentences + 6 empty lines) in first section, found {}".format(
                len(section_paragraphs)))
    except Exception as e:
        print("ERROR: Component 2 — {}".format(e))

    # --- Component 3: Remaining sections intact AND sentences were split (0.2 pts) ---
    # This is a COMPOUND check: section headings present + sentences were already split.
    # By requiring component 1 to have passed (matched_sentences == 6), this check
    # FAILS on initial (sentences not split, even if headings are present),
    # PASSES only on golden (sentences split AND sections intact).
    try:
        # Re-compute matched_sentences for compound check
        sentence_paragraphs_check = []
        for para in paragraphs[1:]:
            if para.style.name.startswith('Heading'):
                break
            text = para.text.strip()
            if text:
                sentence_paragraphs_check.append(text)

        matched_sentences_check = sum(1 for e in EXPECTED_SENTENCES if e in sentence_paragraphs_check)
        sentences_were_split = (matched_sentences_check == 6 and len(sentence_paragraphs_check) == 6)

        # Check that all 3 section headings are still present
        heading_texts = [p.text.strip() for p in paragraphs if p.style.name.startswith('Heading 2')]
        all_headings_present = all(h in heading_texts for h in EXPECTED_LATER_HEADINGS)

        if sentences_were_split and all_headings_present:
            print("PASS: Component 3 — sentences split AND all 3 section headings intact (0.2 pts)")
            total_score += 0.2
        elif sentences_were_split and not all_headings_present:
            missing = [h for h in EXPECTED_LATER_HEADINGS if h not in heading_texts]
            print("FAIL: Component 3 — sentences split but missing section headings: {}".format(missing))
        else:
            # sentences_were_split is False means Component 1 also failed
            print("FAIL: Component 3 — sentences were not fully split (compound condition not met)")
    except Exception as e:
        print("ERROR: Component 3 — {}".format(e))

    final_score = min(total_score, 1.0)
    print("\nScore: {}/1.0".format(round(total_score, 4)))
    print("REWARD: {}".format(round(final_score, 4)))
    return final_score


# Default: test against canonical artifact path
file_path = '{}/{}.docx'.format(WORKDIR, TASK_ID)
if not os.path.exists(file_path):
    print("File not found: {}".format(file_path))
    print("REWARD: 0.0")
else:
    verify_task(file_path)

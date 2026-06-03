"""
Reward Script: Insert empty paragraph after each sentence in the first paragraph
Task ID: osworld_writer_spacing_008
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.5 pts): All 7 sentences each exist as standalone paragraphs (not merged)
  - Component 2 (0.3 pts): At least 6 empty paragraphs inserted directly after sentence paragraphs
  - Component 3 (0.2 pts): Document structure complete: 7 sentence paras + 7 spacer paras + 2 escalation paras = 16 total,
                            with escalation text intact. This is a compound check requiring sentences to be split.
"""

import os

from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_spacing_008'

# Ground truth: the 7 sentences that should each become standalone paragraphs
EXPECTED_SENTENCES = [
    "Thank you for contacting us today.",
    "I understand your concern completely.",
    "Let me pull up your account right now.",
    "I can see the issue you are referring to and I sincerely apologize for the inconvenience.",
    "I will make sure this gets resolved for you as quickly as possible.",
    "Is there anything else I can help clarify while I work on this?",
    "Thank you for your patience and for being a valued customer.",
]

# Ground truth: escalation procedure paragraphs key phrases
ESCALATION_1_START = "Escalation Procedure Level 1:"
ESCALATION_2_START = "Escalation Procedure Level 2:"


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Task: Split first paragraph's 7 sentences into individual paragraphs,
          inserting an empty paragraph after each sentence.

    Initial state: 3 paragraphs (7 sentences in one block + 2 escalation paras)
    Golden state:  16 paragraphs (7 sentence paras + 7 empty spacer paras + 2 escalation paras)
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paragraphs = doc.paragraphs
    all_texts = [p.text.strip() for p in paragraphs]

    print(f"Document has {len(paragraphs)} paragraphs total.")
    for i, t in enumerate(all_texts):
        print(f"  Para {i}: {repr(t[:80])}")

    sentences_set = set(s.lower().strip() for s in EXPECTED_SENTENCES)

    # Component 1: All 7 sentences each exist as standalone paragraphs (0.5 points)
    # FAILS on initial (sentences all merged in one para), PASSES on golden (each sentence = own para)
    try:
        sentences_as_standalone = 0

        for sentence in EXPECTED_SENTENCES:
            sentence_lower = sentence.lower().strip()
            for para_text in all_texts:
                para_lower = para_text.lower().strip()
                if sentence_lower == para_lower:
                    sentences_as_standalone += 1
                    break

        print(f"Sentences as standalone paragraphs: {sentences_as_standalone}/7")

        if sentences_as_standalone == 7:
            print(f"PASS: Component 1 — all 7 sentences are standalone paragraphs (0.5 pts)")
            total_score += 0.5
        elif sentences_as_standalone >= 4:
            partial = 0.25
            print(f"PARTIAL: Component 1 — {sentences_as_standalone}/7 sentences as standalone paragraphs ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — only {sentences_as_standalone}/7 sentences are standalone paragraphs")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Empty paragraphs inserted after each sentence paragraph (0.3 points)
    # FAILS on initial (no sentence paras exist, so no empty paras after them)
    # PASSES on golden (7 empty paras each immediately after a sentence para)
    try:
        # Count empty paragraphs that appear directly after sentence paragraphs
        empty_after_sentence_count = 0
        sentence_para_count = 0

        for i, para_text in enumerate(all_texts):
            para_lower = para_text.lower().strip()
            if para_lower in sentences_set:
                sentence_para_count += 1
                # Check if the next paragraph is empty
                if i + 1 < len(all_texts) and all_texts[i + 1] == '':
                    empty_after_sentence_count += 1

        print(f"Sentence paragraphs found: {sentence_para_count}")
        print(f"Empty paragraphs directly after sentence paragraphs: {empty_after_sentence_count}")

        if empty_after_sentence_count >= 6:
            print(f"PASS: Component 2 — {empty_after_sentence_count} empty paragraphs inserted after sentences (0.3 pts)")
            total_score += 0.3
        elif empty_after_sentence_count >= 3:
            partial = 0.15
            print(f"PARTIAL: Component 2 — {empty_after_sentence_count} empty paragraphs after sentences ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — only {empty_after_sentence_count} empty paragraphs after sentences (need >= 6)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Full document structure integrity (0.2 points)
    # Compound check: sentences are split (16 total paras) AND escalation paras are intact.
    # This requires the task-change (splitting) to have occurred, so it FAILS on initial.
    # On initial: only 3 paragraphs, escalation present but sentences not split.
    # On golden: 16 paragraphs, escalation paragraphs present and unchanged.
    try:
        # Require that sentences have been split (Component 1 precondition for this compound check)
        if sentences_as_standalone < 7:
            print(f"FAIL: Component 3 — sentences not fully split, compound check requires all 7 split")
        else:
            # Find escalation paragraph texts by searching for prefix
            esc1_texts = [p for p in all_texts if p.startswith(ESCALATION_1_START)]
            esc2_texts = [p for p in all_texts if p.startswith(ESCALATION_2_START)]

            esc1_text = esc1_texts[0] if esc1_texts else ""
            esc2_text = esc2_texts[0] if esc2_texts else ""

            # Verify escalation paragraphs contain expected key phrases
            esc1_valid = (
                len(esc1_text) > 0 and
                "senior representative" in esc1_text and
                "case reference number" in esc1_text and
                "CRM system" in esc1_text
            )
            esc2_valid = (
                len(esc2_text) > 0 and
                "billing disputes" in esc2_text and
                "priority ticket" in esc2_text and
                "30 minutes" in esc2_text
            )

            # Also verify total paragraph count is correct (16)
            expected_para_count = 16  # 7 sentences + 7 empty spacers + 2 escalation
            actual_para_count = len(paragraphs)

            if esc1_valid and esc2_valid and actual_para_count == expected_para_count:
                print(f"PASS: Component 3 — full document structure intact: {actual_para_count} paragraphs, both escalation paras unchanged (0.2 pts)")
                total_score += 0.2
            elif esc1_valid and esc2_valid:
                # Escalation intact but paragraph count slightly off
                print(f"PARTIAL: Component 3 — escalation paras intact but para count {actual_para_count} != {expected_para_count} (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 3 — escalation paragraphs missing or modified")
                if not esc1_valid:
                    print(f"  - Level 1 escalation: found={len(esc1_texts) > 0}, content_valid={esc1_valid}")
                if not esc2_valid:
                    print(f"  - Level 2 escalation: found={len(esc2_texts) > 0}, content_valid={esc2_valid}")
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

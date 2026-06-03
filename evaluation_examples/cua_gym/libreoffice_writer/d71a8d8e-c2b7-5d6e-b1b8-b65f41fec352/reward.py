"""
Reward Script: Insert blank line after each sentence in the main body paragraph
Task ID: osworld_writer_blank_line_insertion_007
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): The dense body paragraph is split into exactly 8 sentence paragraphs
  Component 2 (0.3): Blank lines (empty paragraphs) appear after each sentence paragraph
  Component 3 (0.2): Sentence text content is preserved correctly (spot-check 3 key sentences)
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_blank_line_insertion_007'

# Expected sentences from the original dense paragraph (ground truth from task context)
EXPECTED_SENTENCES = [
    "This Remote Work Policy establishes the guidelines and expectations for employees who work outside of the primary office location.",
    "All eligible employees must submit a formal remote work agreement to their direct manager and receive written approval prior to commencing any remote arrangement.",
    "Employees are expected to maintain their standard working hours and remain reachable via company-approved communication channels throughout the business day.",
    "The company reserves the right to rescind remote work privileges at any time if performance standards are not consistently met or if business needs require on-site presence.",
    "Each employee working remotely is responsible for ensuring a safe, ergonomically appropriate, and distraction-free workspace at their designated remote location.",
    "All confidential company data and client information must be handled in strict accordance with the Information Security Policy, which includes the use of encrypted connections and VPN access.",
    "IT support for remote employees is available during standard business hours, and any hardware or software issues must be reported through the official helpdesk ticketing system.",
    "Compliance with this policy is mandatory for all staff in roles approved for remote work, and violations may result in disciplinary action up to and including termination of the remote work arrangement.",
]

NUM_SENTENCES = len(EXPECTED_SENTENCES)  # 8


def verify_task(file_path):
    """
    Verify that each sentence from the original dense body paragraph is now its own
    paragraph, followed by a blank line (empty paragraph).
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: document must have more paragraphs than the initial dense version
    # Initial doc has 6 paragraphs; after splitting 8 sentences each with blank line = 21 paragraphs
    paragraphs = doc.paragraphs
    if len(paragraphs) < 10:
        print(f"FAIL: Document has too few paragraphs ({len(paragraphs)}). "
              "The dense paragraph was not split (initial doc had 6 paragraphs).")
        print("REWARD: 0.0")
        return 0.0

    # Collect all paragraph texts for analysis
    all_texts = [p.text.strip() for p in paragraphs]

    # Locate the body region between "Policy Overview" heading and "Acknowledgment" heading
    # This ensures we only score the task-changed region
    body_start = None
    body_end = None
    for i, text in enumerate(all_texts):
        if text == "Policy Overview":
            body_start = i + 1
        if text == "Acknowledgment" and body_start is not None:
            body_end = i
            break

    if body_start is None or body_end is None:
        print("FAIL: Could not locate 'Policy Overview' or 'Acknowledgment' headings.")
        print("REWARD: 0.0")
        return 0.0

    body_paras = all_texts[body_start:body_end]
    print(f"INFO: Body region paragraphs[{body_start}:{body_end}], count={len(body_paras)}")

    # Component 1 (0.5 points): The body region contains exactly 8 non-empty sentence paragraphs
    # In initial_env, body contains exactly 1 dense paragraph (so this FAILS on initial)
    try:
        non_empty_body = [t for t in body_paras if t != ""]
        non_empty_count = len(non_empty_body)
        print(f"INFO: Non-empty body paragraphs: {non_empty_count}")
        if non_empty_count == NUM_SENTENCES:
            print(f"PASS: Component 1 — Body region has exactly {NUM_SENTENCES} "
                  "non-empty sentence paragraphs (0.5 pts)")
            total_score += 0.5
        elif non_empty_count >= 2:
            # Partial credit: some splitting occurred but not all 8 sentences separated
            comp1_partial = round(non_empty_count / NUM_SENTENCES * 0.5, 2)
            print(f"PARTIAL: Component 1 — Body has {non_empty_count} non-empty paragraphs "
                  f"(expected {NUM_SENTENCES}), partial credit: {comp1_partial} pts")
            if comp1_partial > 0:
                total_score += comp1_partial
        else:
            print(f"FAIL: Component 1 — Body has {non_empty_count} non-empty paragraph(s). "
                  "Dense paragraph was not split. (0.0 pts)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2 (0.3 points): Blank lines appear after each sentence paragraph
    # In initial_env, only 1 body paragraph exists, so no blank lines are present → FAILS
    try:
        blank_after_sentence_count = 0
        sentence_para_count = 0
        for idx, text in enumerate(body_paras):
            if text != "":
                sentence_para_count += 1
                # Each sentence paragraph should be immediately followed by a blank paragraph
                if idx + 1 < len(body_paras) and body_paras[idx + 1] == "":
                    blank_after_sentence_count += 1
        print(f"INFO: Sentence paragraphs followed by blank line: "
              f"{blank_after_sentence_count}/{sentence_para_count}")
        if sentence_para_count > 0 and blank_after_sentence_count == sentence_para_count:
            print(f"PASS: Component 2 — All {sentence_para_count} sentence paragraphs "
                  "have a blank line after them (0.3 pts)")
            total_score += 0.3
        elif sentence_para_count > 0 and blank_after_sentence_count >= 1:
            comp2_partial = round(
                blank_after_sentence_count / max(sentence_para_count, NUM_SENTENCES) * 0.3, 2
            )
            print(f"PARTIAL: Component 2 — {blank_after_sentence_count}/{sentence_para_count} "
                  f"sentences have blank line after them, partial: {comp2_partial} pts")
            if comp2_partial > 0:
                total_score += comp2_partial
        else:
            print("FAIL: Component 2 — No blank lines found after sentence paragraphs. (0.0 pts)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3 (0.2 points): Key sentence text content is preserved correctly
    # Spot-check 3 key sentences (first, middle, last) to verify text was not corrupted
    # In initial_env, sentences exist only as part of the dense paragraph → individual
    # paragraph match FAILS because the dense paragraph is longer than any single sentence
    try:
        key_checks = [
            (EXPECTED_SENTENCES[0], "first sentence"),
            (EXPECTED_SENTENCES[3], "fourth sentence"),
            (EXPECTED_SENTENCES[7], "eighth/last sentence"),
        ]
        passed_checks = 0
        for expected_text, label in key_checks:
            found_exact = any(t == expected_text.strip() for t in all_texts)
            if found_exact:
                print(f"PASS: Component 3 — {label} text preserved correctly")
                passed_checks += 1
            else:
                print(f"FAIL: Component 3 — {label} text NOT found as standalone paragraph")
                print(f"  Expected: {repr(expected_text[:80])}")
        if passed_checks == 3:
            print("PASS: Component 3 — All 3 key sentence texts verified as standalone "
                  "paragraphs (0.2 pts)")
            total_score += 0.2
        elif passed_checks >= 1:
            comp3_partial = round(passed_checks / 3 * 0.2, 2)
            print(f"PARTIAL: Component 3 — {passed_checks}/3 key sentences found, "
                  f"partial: {comp3_partial} pts")
            if comp3_partial > 0:
                total_score += comp3_partial
        else:
            print("FAIL: Component 3 — No key sentences found as standalone paragraphs. (0.0 pts)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in a given env
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

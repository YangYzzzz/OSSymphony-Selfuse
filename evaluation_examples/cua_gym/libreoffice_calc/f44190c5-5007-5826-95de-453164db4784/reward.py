"""
Reward Script: Compile grammar quiz questions into compiled_quiz.odt
Task ID: osworld_multi_apps_grammar_test_compile_001
Domain: libreoffice_writer (ODT file)
Scoring:
  Component 1: compiled_quiz.odt exists on Desktop with 10 questions (0.4 pts)
  Component 2: All questions are numbered sequentially 1-10 (0.3 pts)
  Component 3: Questions appear in correct order (part1 first, then part2) (0.3 pts)
  Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_grammar_test_compile_001'
ODT_FILE = '/home/user/Desktop/compiled_quiz.odt'

# Expected questions from quiz_part1.txt (in order)
PART1_QUESTIONS = [
    "Which sentence uses the correct subject-verb agreement?",
    "Choose the sentence that correctly uses a semicolon.",
    "Identify the sentence with a dangling modifier.",
    "Which of the following sentences is written in the passive voice?",
    "Select the sentence that correctly uses a comma after an introductory clause.",
]

# Expected questions from quiz_part2.txt (in order)
PART2_QUESTIONS = [
    "Which sentence contains a misplaced modifier?",
    "Choose the sentence that correctly uses the apostrophe for possession.",
    "Identify the sentence that contains a parallel structure error.",
    "Which sentence correctly uses 'whom' instead of 'who'?",
    "Select the sentence that avoids a double negative.",
]

ALL_QUESTIONS = PART1_QUESTIONS + PART2_QUESTIONS


def extract_odt_paragraphs(file_path):
    """Extract paragraph text content from an ODT file using zipfile + XML parsing."""
    try:
        zf = zipfile.ZipFile(file_path, 'r')
        content_xml = zf.read('content.xml').decode('utf-8')
        zf.close()
    except Exception as e:
        raise RuntimeError(f"Cannot open/read ODT file: {e}")

    # Parse XML namespaces
    ns = {
        'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
        'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    }

    root = ET.fromstring(content_xml)
    paragraphs = []

    # Find all text:p elements
    for p_elem in root.iter('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p'):
        # Collect all text from children including text:span, text:a etc.
        text_parts = []
        if p_elem.text:
            text_parts.append(p_elem.text)
        for child in p_elem:
            if child.text:
                text_parts.append(child.text)
            if child.tail:
                text_parts.append(child.tail)
        full_text = ''.join(text_parts).strip()
        paragraphs.append(full_text)

    return paragraphs


def normalize_question(text):
    """Strip leading number prefix like '1. ' or '1) ' from question text."""
    # Match patterns like "1. ", "1) ", "1 - ", "1: "
    stripped = re.sub(r'^\d+[\.\)\-\:]\s*', '', text).strip()
    return stripped


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate check: file must exist to proceed
    if not os.path.exists(file_path):
        print(f"FAIL: compiled_quiz.odt not found at {file_path}")
        print(f"\nScore: 0.0/1.0")
        print(f"REWARD: 0.0")
        return 0.0

    # Load paragraphs from ODT file
    try:
        paragraphs = extract_odt_paragraphs(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse ODT file: {e}")
        print(f"\nScore: 0.0/1.0")
        print(f"REWARD: 0.0")
        return 0.0

    # Filter out empty paragraphs
    non_empty = [p for p in paragraphs if p.strip()]
    print(f"INFO: Found {len(non_empty)} non-empty paragraphs in file")
    for i, p in enumerate(non_empty):
        print(f"  Para {i+1}: {repr(p)}")

    # Component 1: File contains exactly 10 questions (0.4 points)
    # The file must have all 10 questions (5 from part1 + 5 from part2)
    try:
        normalized_paragraphs = [normalize_question(p) for p in non_empty]
        # Check how many of the expected questions are present (regardless of numbering)
        present_count = 0
        for expected_q in ALL_QUESTIONS:
            # Normalize expected question text for comparison
            for norm_para in normalized_paragraphs:
                # Case-insensitive comparison, stripping punctuation from ends
                if expected_q.lower().rstrip('?').strip() in norm_para.lower().rstrip('?').strip():
                    present_count += 1
                    break

        if present_count == 10:
            print(f"PASS: Component 1 — All 10 questions present in file (0.4 pts)")
            total_score += 0.4
        elif present_count >= 7 and total_score < 0.4:
            print(f"PARTIAL: Component 1 — {present_count}/10 questions present")
            if present_count >= 7:
                total_score += round(0.4 * present_count / 10, 2)
        else:
            print(f"FAIL: Component 1 — Only {present_count}/10 expected questions found in file")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Questions are numbered sequentially 1-10 (0.3 points)
    # Each paragraph should start with the correct number (1. through 10.)
    try:
        numbering_correct = 0
        for i, expected_q in enumerate(ALL_QUESTIONS, start=1):
            for para in non_empty:
                # Check if paragraph starts with the number "i." or "i)"
                if re.match(rf'^{i}[\.\)]\s*', para):
                    # Found a paragraph with correct number prefix
                    norm_para = normalize_question(para)
                    if expected_q.lower().rstrip('?').strip() in norm_para.lower().rstrip('?').strip():
                        numbering_correct += 1
                        break

        if numbering_correct == 10:
            print(f"PASS: Component 2 — All 10 questions numbered sequentially 1-10 (0.3 pts)")
            total_score += 0.3
        elif numbering_correct >= 5:
            partial = round(0.3 * numbering_correct / 10, 2)
            print(f"PARTIAL: Component 2 — {numbering_correct}/10 questions correctly numbered ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Only {numbering_correct}/10 questions have correct sequential numbering")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Correct ordering - part1 questions (1-5) then part2 questions (6-10) (0.3 points)
    # First 5 questions should come from quiz_part1.txt, last 5 from quiz_part2.txt
    try:
        if len(non_empty) >= 10:
            # Check first 5 content matches part1 questions
            part1_order_correct = 0
            for i, expected_q in enumerate(PART1_QUESTIONS):
                # Find the paragraph with number i+1
                for para in non_empty:
                    if re.match(rf'^{i+1}[\.\)]\s*', para):
                        norm_para = normalize_question(para)
                        if expected_q.lower().rstrip('?').strip() in norm_para.lower().rstrip('?').strip():
                            part1_order_correct += 1
                        break

            # Check last 5 content matches part2 questions
            part2_order_correct = 0
            for i, expected_q in enumerate(PART2_QUESTIONS):
                num = i + 6  # Questions 6-10
                for para in non_empty:
                    if re.match(rf'^{num}[\.\)]\s*', para):
                        norm_para = normalize_question(para)
                        if expected_q.lower().rstrip('?').strip() in norm_para.lower().rstrip('?').strip():
                            part2_order_correct += 1
                        break

            total_order_correct = part1_order_correct + part2_order_correct
            if total_order_correct == 10:
                print(f"PASS: Component 3 — All questions in correct order (part1 first, part2 second) (0.3 pts)")
                total_score += 0.3
            elif total_order_correct >= 6:
                partial = round(0.3 * total_order_correct / 10, 2)
                print(f"PARTIAL: Component 3 — {total_order_correct}/10 questions in correct position ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — Only {total_order_correct}/10 questions in correct order "
                      f"(part1: {part1_order_correct}/5, part2: {part2_order_correct}/5)")
        else:
            print(f"FAIL: Component 3 — Not enough paragraphs ({len(non_empty)}) to verify ordering")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.1f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
if not os.path.exists(ODT_FILE):
    print(f"File not found: {ODT_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(ODT_FILE)

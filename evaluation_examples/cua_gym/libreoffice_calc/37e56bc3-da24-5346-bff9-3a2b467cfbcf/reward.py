"""
Reward Script: Compile 10 grammar exam files into exam_package_final.odt
Task ID: osworld_multi_apps_grammar_test_compile_012
Domain: libreoffice_writer (ODT)
Scoring:
  Component 1: Header with institution name on every page           0.15 pts
  Component 2: Footer with page numbers                             0.15 pts
  Component 3: Cover page (Heading 1 with exam title)              0.15 pts
  Component 4: Study guide summary (2 sections, 10 topic sentences) 0.20 pts
  Component 5: Full 100-question exam with Heading 2 per section    0.20 pts
  Component 6: Answer key appendix                                  0.10 pts
  Component 7: Statistical summary table (4 columns)                0.05 pts
  Total: 1.00
"""

import os
import zipfile
import re

WORKDIR = '/home/user/Documents'
TASK_ID = 'osworld_multi_apps_grammar_test_compile_012'
ODT_FILE = os.path.join(WORKDIR, 'exam_package_final.odt')


def get_odt_content(odt_path):
    """Extract content.xml and styles.xml from the ODT file (which is a ZIP)."""
    with zipfile.ZipFile(odt_path, 'r') as z:
        content_xml = z.read('content.xml').decode('utf-8')
        styles_xml = z.read('styles.xml').decode('utf-8') if 'styles.xml' in z.namelist() else ''
    return content_xml, styles_xml


def strip_xml_tags(xml_str):
    """Remove XML tags and return plain text."""
    return re.sub(r'<[^>]+>', ' ', xml_str)


def verify_task(odt_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: File must exist and be a valid ODT
    if not os.path.exists(odt_path):
        print(f"CRITICAL: File not found: {odt_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        content_xml, styles_xml = get_odt_content(odt_path)
    except Exception as e:
        print(f"CRITICAL: Cannot read ODT file {odt_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # -----------------------------------------------------------------------
    # Component 1: Header with institution name on every page (0.15 pts)
    # The header should contain an institution name (task requires it).
    # In ODT, headers are defined in styles.xml within <style:header>.
    # -----------------------------------------------------------------------
    try:
        # Check for header element in styles.xml
        has_header_element = '<style:header>' in styles_xml
        # Check header contains institution name (non-empty, meaningful text)
        header_match = re.search(
            r'<style:header>(.*?)</style:header>', styles_xml, re.DOTALL
        )
        if header_match:
            header_content = header_match.group(1)
            header_text = strip_xml_tags(header_content).strip()
            # Must have some institution-like text (not empty)
            if len(header_text) >= 5:
                print(f"PASS: Component 1 — Header with institution text found: '{header_text[:80]}' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — Header element found but content is empty or too short: '{header_text}'")
        else:
            print("FAIL: Component 1 — No <style:header> element found in styles.xml")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: Footer with page numbers (0.15 pts)
    # The footer should contain a page number field (text:page-number element).
    # -----------------------------------------------------------------------
    try:
        has_footer_element = '<style:footer>' in styles_xml
        footer_match = re.search(
            r'<style:footer>(.*?)</style:footer>', styles_xml, re.DOTALL
        )
        if footer_match:
            footer_content = footer_match.group(1)
            # Check for page-number field code in ODF
            has_page_number = 'text:page-number' in footer_content
            if has_page_number:
                print("PASS: Component 2 — Footer with page-number field found (0.15 pts)")
                total_score += 0.15
            else:
                footer_text = strip_xml_tags(footer_content).strip()
                print(f"FAIL: Component 2 — Footer found but no page-number field. Content: '{footer_text}'")
        else:
            print("FAIL: Component 2 — No <style:footer> element found in styles.xml")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: Cover page (first Heading 1 as cover page) (0.15 pts)
    # The document must start with a cover page. In ODT the cover page is
    # indicated by Heading 1 with page-break-before and a title or institution.
    # We verify that the first Heading 1 element exists and contains meaningful text.
    # -----------------------------------------------------------------------
    try:
        # Find all Heading 1 paragraphs in content.xml
        heading1_matches = re.findall(
            r'<text:p[^>]*text:style-name="Heading[_ ]?1[^"]*"[^>]*>(.*?)</text:p>',
            content_xml, re.DOTALL
        )
        if not heading1_matches:
            # Try with outline-level="1"
            heading1_matches = re.findall(
                r'<text:h[^>]*text:outline-level="1"[^>]*>(.*?)</text:h>',
                content_xml, re.DOTALL
            )

        if heading1_matches:
            first_heading_text = strip_xml_tags(heading1_matches[0]).strip()
            # Must contain exam-like or institution title keywords
            if len(first_heading_text) >= 5:
                print(f"PASS: Component 3 — Cover page heading found: '{first_heading_text[:80]}' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — First Heading 1 is too short: '{first_heading_text}'")
        else:
            print("FAIL: Component 3 — No Heading 1 (cover page) found in content.xml")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -----------------------------------------------------------------------
    # Component 4: Study guide summary with 10 topic sentences (0.20 pts)
    # The document must have a study guide section with exactly one sentence
    # per topic (10 topics total). We check for:
    # (a) "STUDY GUIDE" heading text present
    # (b) At least 10 topic summary entries (one per grammar topic)
    # Expected topics: verbs, nouns, adjectives, adverbs, prepositions,
    #   conjunctions, pronouns, tenses, articles, punctuation
    # -----------------------------------------------------------------------
    try:
        content_lower = content_xml.lower()
        content_text = strip_xml_tags(content_xml).lower()

        # Check for study guide heading
        has_study_guide = 'study guide' in content_text

        # Check for topic keywords that should appear in the study guide sentences
        expected_topics = [
            'verb', 'noun', 'adjective', 'adverb', 'preposition',
            'conjunction', 'pronoun', 'tense', 'article', 'punctuation'
        ]
        found_topics = sum(1 for t in expected_topics if t in content_text)

        if has_study_guide and found_topics >= 10:
            print(f"PASS: Component 4 — Study guide found with {found_topics}/10 topics (0.20 pts)")
            total_score += 0.20
        elif has_study_guide and found_topics >= 7:
            # Partial: study guide exists but missing some topics
            print(f"PARTIAL: Component 4 — Study guide found but only {found_topics}/10 topics (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 — Study guide missing or incomplete. "
                  f"has_study_guide={has_study_guide}, found_topics={found_topics}/10")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # -----------------------------------------------------------------------
    # Component 5: Full 100-question exam with Heading 2 per section (0.20 pts)
    # The document must contain 100 numbered questions (Q1 through Q100)
    # and 10 Heading 2 section headers.
    # -----------------------------------------------------------------------
    try:
        content_text_plain = strip_xml_tags(content_xml)

        # Count Heading 2 elements
        heading2_count = len(re.findall(
            r'<text:h[^>]*text:outline-level="2"[^>]*>',
            content_xml
        ))
        # Also count via style-name="Heading 2" in text:p
        heading2_count += len(re.findall(
            r'text:style-name="Heading[_ ]?2"',
            content_xml
        ))

        # Count questions Q1 through Q100 (match "Q1." through "Q100.")
        q_numbers = set()
        for m in re.finditer(r'\bQ(\d+)\.', content_text_plain):
            q_numbers.add(int(m.group(1)))

        question_count = len([n for n in q_numbers if 1 <= n <= 100])

        # We expect 10 sections (Heading 2 in exam body + answer key heading 2s)
        # Task requires Heading 2 per section = 10 sections minimum in the exam
        # heading2_count may include answer key sections too
        exam_sections_ok = heading2_count >= 10
        questions_ok = question_count >= 90  # allow some tolerance

        if exam_sections_ok and questions_ok:
            print(f"PASS: Component 5 — {heading2_count} Heading 2 sections, "
                  f"{question_count} questions found (0.20 pts)")
            total_score += 0.20
        elif questions_ok and not exam_sections_ok:
            print(f"PARTIAL: Component 5 — Questions present ({question_count}) but "
                  f"only {heading2_count}/10 Heading 2 sections (0.10 pts)")
            total_score += 0.10
        elif exam_sections_ok and not questions_ok:
            print(f"PARTIAL: Component 5 — {heading2_count} sections found but "
                  f"only {question_count}/100 questions (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 — Exam body incomplete. "
                  f"Heading 2 count={heading2_count}, questions found={question_count}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # -----------------------------------------------------------------------
    # Component 6: Answer key appendix (0.10 pts)
    # The document must have an "Answer Key" section after the main exam.
    # -----------------------------------------------------------------------
    try:
        content_text_plain_lower = strip_xml_tags(content_xml).lower()
        has_answer_key = 'answer key' in content_text_plain_lower

        # Must also contain actual answer entries (e.g., "Q1. runs" or "A1: runs")
        answer_entries = re.findall(
            r'\b(?:Q|A)(\d+)[.\:]?\s+\w+',
            strip_xml_tags(content_xml)
        )
        # Count unique question numbers in the answer key context
        # We look for answer-type content after "answer key" text position
        answer_key_pos = content_text_plain_lower.find('answer key')
        if answer_key_pos > 0:
            answer_section_text = strip_xml_tags(content_xml)[answer_key_pos:]
            answer_q_numbers = set()
            for m in re.finditer(r'\bQ(\d+)\.\s+\w+', answer_section_text):
                answer_q_numbers.add(int(m.group(1)))
            answer_count = len(answer_q_numbers)
        else:
            answer_count = 0

        if has_answer_key and answer_count >= 50:
            print(f"PASS: Component 6 — Answer key found with {answer_count} answers (0.10 pts)")
            total_score += 0.10
        elif has_answer_key and answer_count >= 10:
            print(f"PARTIAL: Component 6 — Answer key found but only {answer_count} answers (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 6 — Answer key missing or incomplete. "
                  f"has_answer_key={has_answer_key}, answer_count={answer_count}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # -----------------------------------------------------------------------
    # Component 7: Statistical summary table (0.05 pts)
    # The document must have a table with at least 4 columns:
    # Section, Topic, Difficulty, Question Count
    # -----------------------------------------------------------------------
    try:
        # Check for table element in content.xml
        has_table = '<table:table' in content_xml

        if has_table:
            # Check that table contains the required columns
            table_text = strip_xml_tags(content_xml).lower()
            required_cols = ['topic', 'difficulty', 'question']
            found_cols = [c for c in required_cols if c in table_text]

            # Check the table has at least 10 data rows (one per section)
            table_rows = content_xml.count('<table:table-row>')
            # 1 header row + 10 data rows + 1 total row = 12 rows minimum
            rows_ok = table_rows >= 10

            if len(found_cols) >= 3 and rows_ok:
                print(f"PASS: Component 7 — Statistics table found with {table_rows} rows "
                      f"and columns: {found_cols} (0.05 pts)")
                total_score += 0.05
            elif len(found_cols) >= 2:
                print(f"PARTIAL: Component 7 — Table found but missing columns or rows. "
                      f"cols={found_cols}, rows={table_rows} (0.025 pts)")
                total_score += 0.025
            else:
                print(f"FAIL: Component 7 — Table incomplete. "
                      f"found_cols={found_cols}, rows={table_rows}")
        else:
            print("FAIL: Component 7 — No table found in document")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path
if not os.path.exists(ODT_FILE):
    print(f"File not found: {ODT_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(ODT_FILE)

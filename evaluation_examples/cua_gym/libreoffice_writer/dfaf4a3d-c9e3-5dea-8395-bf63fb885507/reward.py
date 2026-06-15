"""
Reward Script: Create a proper TOC for a senior thesis with front matter (no page numbers)
                and body chapters (with page numbers).
Task ID: writer_mt_066
Domain: libreoffice_writer
Scoring:
  Component 1: TOC heading exists at beginning (0.15 pts)
  Component 2: Front matter entries present without page numbers (0.30 pts)
  Component 3: Body chapter entries present with page numbers (0.30 pts)
  Component 4: Sub-section entries present with page numbers (0.25 pts)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_mt_066'

# Front matter headings that should appear in TOC WITHOUT page numbers
FRONT_MATTER = ['Abstract', 'Acknowledgments', 'List of Abbreviations']

# Body chapter headings (Heading 1 level) that should appear in TOC WITH page numbers
BODY_CHAPTERS = [
    'Chapter 1: Introduction',
    'Chapter 2: Literature Review',
    'Chapter 3: Methodology',
    'Chapter 4: Results',
    'Chapter 5: Discussion and Conclusion',
]

# Sample of sub-section headings (Heading 2 level) that should appear with page numbers
BODY_SUBSECTIONS = [
    '1.1 Background and Motivation',
    '1.2 Problem Statement',
    '2.1 Traditional Maintenance Strategies',
    '3.1 Data Collection',
    '4.1 Baseline Comparisons',
    '5.1 Summary of Contributions',
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paras = doc.paragraphs

    # =========================================================================
    # Component 1: TOC heading exists at the beginning of the document (0.15 pts)
    # In the initial doc, paragraph[0] is 'Abstract' (Heading 1).
    # In the golden doc, there is a 'Table of Contents' heading before the content.
    # =========================================================================
    try:
        toc_heading_found = False
        # Search within the first 5 paragraphs for a TOC heading
        for i in range(min(5, len(paras))):
            text = paras[i].text.strip().lower()
            if 'table of contents' in text or 'toc' == text:
                toc_heading_found = True
                break
        if toc_heading_found:
            print(f"PASS: Component 1 -- TOC heading found (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- No 'Table of Contents' heading found in first 5 paragraphs")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # =========================================================================
    # Component 2: Front matter entries listed WITHOUT page numbers (0.30 pts)
    # The TOC should contain entries for Abstract, Acknowledgments, and
    # List of Abbreviations, and these should NOT have tab+number patterns.
    # In the initial doc, these are body headings, NOT TOC entries.
    # =========================================================================
    try:
        front_matter_correct = 0
        for fm_name in FRONT_MATTER:
            # Search for a TOC-like entry (Normal style paragraph) matching this name
            # It must appear BEFORE the body content headings
            found_as_toc_entry = False
            for p in paras:
                text = p.text.strip()
                style = p.style.name if p.style else ''
                # Stop searching if we hit actual body content (Heading 1 that is Abstract/etc)
                # The TOC entries are Normal style, not Heading 1
                if style == 'Heading 1' and text == fm_name:
                    break
                # A TOC entry for front matter: text matches name, no tab+number
                if text == fm_name and style != 'Heading 1':
                    # Verify no page number (no tab character followed by digits)
                    if '\t' not in text:
                        found_as_toc_entry = True
                        break
            if found_as_toc_entry:
                front_matter_correct += 1
                print(f"  PASS: Front matter TOC entry '{fm_name}' found without page number")
            else:
                print(f"  FAIL: Front matter TOC entry '{fm_name}' not found or has page number")

        if front_matter_correct == len(FRONT_MATTER):
            print(f"PASS: Component 2 -- All {len(FRONT_MATTER)} front matter entries correct (0.30 pts)")
            total_score += 0.30
        elif front_matter_correct > 0:
            partial = 0.30 * (front_matter_correct / len(FRONT_MATTER))
            print(f"PARTIAL: Component 2 -- {front_matter_correct}/{len(FRONT_MATTER)} front matter entries ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- No front matter entries found in TOC")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # =========================================================================
    # Component 3: Body chapter entries present WITH page numbers (0.30 pts)
    # Each chapter entry should have a tab + number pattern (e.g., "Chapter 1: Introduction\t1")
    # In the initial doc, these are just Heading 1 paragraphs with no TOC.
    # =========================================================================
    try:
        chapters_with_pages = 0
        for ch_name in BODY_CHAPTERS:
            for p in paras:
                text = p.text.strip()
                style = p.style.name if p.style else ''
                # Look for Normal-style paragraph that starts with the chapter name
                # and has a tab followed by a number (page number)
                if style != 'Heading 1' and text.startswith(ch_name) and '\t' in text:
                    after_tab = text.split('\t')[-1].strip()
                    if after_tab and re.match(r'^\d+$', after_tab):
                        chapters_with_pages += 1
                        print(f"  PASS: Chapter TOC entry '{ch_name}' has page number {after_tab}")
                        break
            else:
                print(f"  FAIL: Chapter TOC entry '{ch_name}' not found with page number")

        if chapters_with_pages == len(BODY_CHAPTERS):
            print(f"PASS: Component 3 -- All {len(BODY_CHAPTERS)} chapter entries have page numbers (0.30 pts)")
            total_score += 0.30
        elif chapters_with_pages > 0:
            partial = 0.30 * (chapters_with_pages / len(BODY_CHAPTERS))
            print(f"PARTIAL: Component 3 -- {chapters_with_pages}/{len(BODY_CHAPTERS)} chapter entries ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 -- No chapter entries with page numbers found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # =========================================================================
    # Component 4: Sub-section entries present WITH page numbers (0.25 pts)
    # Heading 2 entries should also appear in the TOC with page numbers.
    # =========================================================================
    try:
        subsections_with_pages = 0
        for sub_name in BODY_SUBSECTIONS:
            for p in paras:
                text = p.text.strip()
                style = p.style.name if p.style else ''
                if style != 'Heading 2' and text.startswith(sub_name) and '\t' in text:
                    after_tab = text.split('\t')[-1].strip()
                    if after_tab and re.match(r'^\d+$', after_tab):
                        subsections_with_pages += 1
                        print(f"  PASS: Sub-section TOC entry '{sub_name}' has page number {after_tab}")
                        break
            else:
                print(f"  FAIL: Sub-section TOC entry '{sub_name}' not found with page number")

        if subsections_with_pages == len(BODY_SUBSECTIONS):
            print(f"PASS: Component 4 -- All {len(BODY_SUBSECTIONS)} sub-section entries have page numbers (0.25 pts)")
            total_score += 0.25
        elif subsections_with_pages > 0:
            partial = 0.25 * (subsections_with_pages / len(BODY_SUBSECTIONS))
            print(f"PARTIAL: Component 4 -- {subsections_with_pages}/{len(BODY_SUBSECTIONS)} sub-section entries ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 -- No sub-section entries with page numbers found")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

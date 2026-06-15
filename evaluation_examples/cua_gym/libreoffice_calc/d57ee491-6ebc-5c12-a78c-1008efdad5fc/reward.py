"""
Reward Script: Research Profile in Writer Document
Task ID: osworld_multi_apps_paper_scholar_browse_015
Domain: libreoffice_writer (multi-app: Chrome + Writer)
Scoring:
  Component 1: Document has at least one non-empty paragraph (0.2 pts)
  Component 2: Document mentions the first author's name (Armando Solar-Lezama) (0.3 pts)
  Component 3: Document mentions the author's affiliation (MIT) (0.2 pts)
  Component 4: Document mentions h-index or research focus keywords (0.3 pts)
Total: 1.0
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_paper_scholar_browse_015'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.

    The task: identify the first author from a program synthesis PDF (Armando Solar-Lezama),
    navigate to their Google Scholar profile in Chrome, then write a one-paragraph research
    profile in the open Writer document with affiliation, research focus, h-index, and top
    research areas. Document must be saved.

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the document
    try:
        from docx import Document
        doc = Document(file_path)
    except ImportError:
        print("CRITICAL: python-docx not installed")
        print("REWARD: 0.0")
        return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Gather all text from the document
    all_paragraphs = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
    full_text = ' '.join(all_paragraphs)
    full_text_lower = full_text.lower()

    # Component 1: Document has at least one non-empty paragraph with substantial content (0.2 pts)
    # This should FAIL on initial (empty doc) and PASS on golden (has content paragraph)
    try:
        # Need at least 50 characters of text — enough to be a real research profile paragraph
        has_substantial_content = len(full_text) >= 50
        if has_substantial_content:
            print(f"PASS: Component 1 — Document has substantial content ({len(full_text)} chars, {len(all_paragraphs)} non-empty paragraphs) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Document is empty or has trivial content (text length: {len(full_text)})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Document mentions the first author's name — Armando Solar-Lezama (0.3 pts)
    # This should FAIL on initial (empty) and PASS on golden (contains the author's name)
    try:
        # The first author of the program synthesis paper on the desktop is Armando Solar-Lezama
        author_name_patterns = [
            'armando solar-lezama',
            'solar-lezama',
            'armando solar',
        ]
        author_mentioned = any(pattern in full_text_lower for pattern in author_name_patterns)
        if author_mentioned:
            # Find which pattern matched for logging
            matched = next(p for p in author_name_patterns if p in full_text_lower)
            print(f"PASS: Component 2 — Author name mentioned (matched: '{matched}') (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Author name 'Armando Solar-Lezama' not found in document")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Document mentions the author's affiliation (MIT or Massachusetts Institute of Technology) (0.2 pts)
    # This should FAIL on initial (empty) and PASS on golden
    try:
        affiliation_patterns = [
            'mit',
            'massachusetts institute of technology',
            'csail',
            'computer science and artificial intelligence',
        ]
        affiliation_mentioned = any(pattern in full_text_lower for pattern in affiliation_patterns)
        if affiliation_mentioned:
            matched = next(p for p in affiliation_patterns if p in full_text_lower)
            print(f"PASS: Component 3 — Affiliation mentioned (matched: '{matched}') (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Author affiliation (MIT/Massachusetts Institute of Technology) not found in document")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Document mentions research-specific details — h-index and/or research areas (0.3 pts)
    # The task requires: h-index, top research areas (program synthesis, etc.)
    # This should FAIL on initial (empty) and PASS on golden
    try:
        # Check for h-index mention
        has_hindex = 'h-index' in full_text_lower or 'h index' in full_text_lower

        # Check for research focus keywords related to program synthesis / the author's work
        research_keywords = [
            'program synthesis',
            'synthesis',
            'sketch',
            'cegis',
            'programming language',
            'research focus',
            'research area',
        ]
        research_keyword_count = sum(1 for kw in research_keywords if kw in full_text_lower)
        has_research_content = research_keyword_count >= 2

        if has_hindex and has_research_content:
            print(f"PASS: Component 4 — h-index mentioned AND research areas mentioned (keywords matched: {research_keyword_count}) (0.3 pts)")
            total_score += 0.3
        elif has_hindex:
            # Partial: h-index but no clear research areas
            print(f"PASS (partial): Component 4 — h-index mentioned but research area keywords low (count: {research_keyword_count}), awarding 0.15 pts")
            total_score += 0.15
        elif has_research_content:
            # Partial: research areas mentioned but no h-index
            print(f"PASS (partial): Component 4 — research area keywords found ({research_keyword_count}) but no h-index mention, awarding 0.15 pts")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — neither h-index nor sufficient research area keywords found (keyword count: {research_keyword_count})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path on VM
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

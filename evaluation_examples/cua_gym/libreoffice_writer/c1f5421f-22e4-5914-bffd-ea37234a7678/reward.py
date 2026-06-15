"""
Reward Script: Figure numbering consistency in master document
Task ID: writer_rm_073
Domain: libreoffice_writer
Scoring:
  Component 1 (0.20): All figure captions use "Figure" prefix (not Fig., Diagram, Exhibit, etc.)
  Component 2 (0.30): All figure captions use "X.Y" dot-separated numbering format
  Component 3 (0.25): Chapter numbers in captions match the chapter they belong to
  Component 4 (0.25): Sequential numbering within each chapter is correct (1, 2, 3, ...)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_073'

# Expected figure captions per chapter (chapter_num -> list of sequential figure numbers)
# Chapter 1: 3 figures (1.1, 1.2, 1.3)
# Chapter 2: 4 figures (2.1, 2.2, 2.3, 2.4)
# Chapter 3: 4 figures (3.1, 3.2, 3.3, 3.4)
# Chapter 4: 5 figures (4.1, 4.2, 4.3, 4.4, 4.5)
# Chapter 5: 4 figures (5.1, 5.2, 5.3, 5.4)
EXPECTED = {
    1: [1, 2, 3],
    2: [1, 2, 3, 4],
    3: [1, 2, 3, 4],
    4: [1, 2, 3, 4, 5],
    5: [1, 2, 3, 4],
}
TOTAL_FIGURES = 20


def find_caption_paragraphs(doc):
    """
    Identify figure caption paragraphs and which chapter they belong to.
    A caption paragraph is one that appears to reference a figure (contains
    image-related label text). Chapter headings use 'Heading 1' style.
    Returns list of (chapter_num, caption_text) tuples.
    """
    current_chapter = 0
    captions = []

    for para in doc.paragraphs:
        text = para.text.strip()
        style_name = para.style.name if para.style else ''

        # Detect chapter headings
        if style_name == 'Heading 1' and text.lower().startswith('chapter'):
            match = re.match(r'Chapter\s+(\d+)', text, re.IGNORECASE)
            if match:
                current_chapter = int(match.group(1))

        # Detect figure caption paragraphs: lines that start with a figure-like label
        # and contain a colon followed by descriptive text
        # Matches: "Figure X.Y: ...", "Fig. N: ...", "Diagram N: ...", etc.
        if current_chapter > 0 and text and not text.startswith('['):
            # Check if this looks like a caption line (not body text or headings)
            caption_pattern = re.match(
                r'^(figure|fig\.?|diagram|exhibit|FIGURE)\s*[\[\(#]?\s*'
                r'(.+?)\s*[\]\)]?\s*:\s*.+',
                text, re.IGNORECASE
            )
            if caption_pattern:
                captions.append((current_chapter, text))

    return captions


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    from docx import Document

    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    captions = find_caption_paragraphs(doc)
    print(f"Found {len(captions)} figure captions")

    if len(captions) == 0:
        print("FAIL: No figure captions found in document")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: All figure captions use "Figure" prefix (0.20 points)
    # In initial: mixed prefixes (Fig., Diagram, Exhibit, FIGURE, figure, etc.)
    # In golden: all use "Figure" (title case)
    try:
        correct_prefix_count = 0
        for ch, text in captions:
            if re.match(r'^Figure\s+\d', text):
                correct_prefix_count += 1
            else:
                print(f"  prefix_fail: ch{ch} -> {text[:60]!r}")

        prefix_ratio = correct_prefix_count / len(captions) if captions else 0
        if prefix_ratio >= 0.95:
            print(f"PASS: Component 1 — All {correct_prefix_count}/{len(captions)} captions use 'Figure' prefix (0.20 pts)")
            total_score += 0.20
        elif prefix_ratio >= 0.5:
            partial = 0.20 * prefix_ratio
            print(f"PARTIAL: Component 1 — {correct_prefix_count}/{len(captions)} captions use 'Figure' prefix ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — Only {correct_prefix_count}/{len(captions)} captions use 'Figure' prefix")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All captions use "X.Y" dot-separated numbering (0.30 points)
    # In initial: mixed formats (plain numbers, Roman numerals, letters, dashes, etc.)
    # In golden: all use "Figure X.Y:" format
    try:
        dot_format_count = 0
        dot_format_pattern = re.compile(r'^Figure\s+(\d+)\.(\d+)\s*:')
        parsed_captions = []  # (chapter_num_from_heading, chapter_in_caption, fig_num)

        for ch, text in captions:
            m = dot_format_pattern.match(text)
            if m:
                dot_format_count += 1
                parsed_captions.append((ch, int(m.group(1)), int(m.group(2))))
            else:
                parsed_captions.append((ch, None, None))

        format_ratio = dot_format_count / len(captions) if captions else 0
        if format_ratio >= 0.95:
            print(f"PASS: Component 2 — All {dot_format_count}/{len(captions)} captions use X.Y format (0.30 pts)")
            total_score += 0.30
        elif format_ratio >= 0.5:
            partial = 0.30 * format_ratio
            print(f"PARTIAL: Component 2 — {dot_format_count}/{len(captions)} captions use X.Y format ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Only {dot_format_count}/{len(captions)} captions use X.Y format")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Chapter numbers in captions match the chapter they're in (0.25 points)
    # In initial: some captions have wrong chapter refs (e.g., "Figure II-3" in chapter 2 uses Roman)
    # In golden: Figure 2.3 is in Chapter 2, Figure 3.1 is in Chapter 3, etc.
    try:
        correct_chapter_count = 0
        checked_count = 0
        for heading_ch, caption_ch, fig_num in parsed_captions:
            if caption_ch is not None:
                checked_count += 1
                if caption_ch == heading_ch:
                    correct_chapter_count += 1
                else:
                    print(f"  chapter_mismatch: caption says ch{caption_ch} but heading says ch{heading_ch}")

        if checked_count > 0:
            ch_ratio = correct_chapter_count / checked_count
            if ch_ratio >= 0.95:
                print(f"PASS: Component 3 — All {correct_chapter_count}/{checked_count} captions have correct chapter number (0.25 pts)")
                total_score += 0.25
            elif ch_ratio >= 0.5:
                partial = 0.25 * ch_ratio
                print(f"PARTIAL: Component 3 — {correct_chapter_count}/{checked_count} correct chapter numbers ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — Only {correct_chapter_count}/{checked_count} correct chapter numbers")
        else:
            print(f"FAIL: Component 3 — No captions with parseable X.Y format to check chapter numbers")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Sequential numbering within each chapter (0.25 points)
    # In golden: Chapter 1 has 1.1, 1.2, 1.3; Chapter 2 has 2.1, 2.2, 2.3, 2.4; etc.
    # In initial: numbering is inconsistent and non-sequential
    try:
        # Group parsed captions by chapter
        chapter_figs = {}
        for heading_ch, caption_ch, fig_num in parsed_captions:
            if caption_ch is not None and fig_num is not None and caption_ch == heading_ch:
                chapter_figs.setdefault(heading_ch, []).append(fig_num)

        chapters_correct = 0
        chapters_checked = 0

        for ch_num, expected_figs in EXPECTED.items():
            chapters_checked += 1
            actual_figs = chapter_figs.get(ch_num, [])
            if actual_figs == expected_figs:
                chapters_correct += 1
            else:
                print(f"  seq_mismatch: ch{ch_num} expected {expected_figs}, got {actual_figs}")

        if chapters_checked > 0:
            seq_ratio = chapters_correct / chapters_checked
            if seq_ratio >= 0.95:
                print(f"PASS: Component 4 — All {chapters_correct}/{chapters_checked} chapters have correct sequential numbering (0.25 pts)")
                total_score += 0.25
            elif seq_ratio >= 0.4:
                partial = 0.25 * seq_ratio
                print(f"PARTIAL: Component 4 — {chapters_correct}/{chapters_checked} chapters correct ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 — Only {chapters_correct}/{chapters_checked} chapters have correct sequential numbering")
        else:
            print(f"FAIL: Component 4 — No chapters to check sequential numbering")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

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

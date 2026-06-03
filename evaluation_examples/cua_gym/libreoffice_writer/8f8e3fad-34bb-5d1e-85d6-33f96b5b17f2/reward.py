"""
Reward Script: Table of Figures with chapter-based numbering
Task ID: writer_mt_088
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): Figure captions use chapter-based numbering (Figure X.Y)
  Component 2 (0.3): Table of Figures section exists with all 12 entries
  Component 3 (0.3): Correct chapter-figure mapping (Ch1: 1.1-1.4, Ch2: 2.1-2.3, Ch3: 3.1-3.5)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_mt_088'

# Expected chapter-based figure captions
EXPECTED_FIGURES = [
    'Figure 1.1', 'Figure 1.2', 'Figure 1.3', 'Figure 1.4',
    'Figure 2.1', 'Figure 2.2', 'Figure 2.3',
    'Figure 3.1', 'Figure 3.2', 'Figure 3.3', 'Figure 3.4', 'Figure 3.5',
]

# Expected figures per chapter
CHAPTER_FIGURES = {
    1: ['Figure 1.1', 'Figure 1.2', 'Figure 1.3', 'Figure 1.4'],
    2: ['Figure 2.1', 'Figure 2.2', 'Figure 2.3'],
    3: ['Figure 3.1', 'Figure 3.2', 'Figure 3.3', 'Figure 3.4', 'Figure 3.5'],
}


def persist_app_state(domain):
    """Save any unsaved changes in LibreOffice before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


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

    all_paras = doc.paragraphs

    # Extract all paragraph texts
    para_texts = [p.text.strip() for p in all_paras]

    # ----------------------------------------------------------------
    # Component 1: Figure captions in document body use chapter-based
    # numbering pattern "Figure X.Y" (0.4 points)
    # ----------------------------------------------------------------
    try:
        # Find figure caption paragraphs in the body (not in the Table of Figures)
        # Body captions start with "Figure X.Y:" pattern
        chapter_fig_pattern = re.compile(r'^Figure\s+(\d+)\.(\d+)\s*[:\-]')
        body_chapter_figs = []

        # We look for figure captions that are NOT inside the Table of Figures
        # The ToF entries typically have a tab + page number at the end
        for text in para_texts:
            if chapter_fig_pattern.match(text) and '\t' not in text:
                # This is a body caption with chapter numbering
                body_chapter_figs.append(text)

        found_count = len(body_chapter_figs)
        if found_count >= 12:
            print(f"PASS: Component 1 -- All 12 figure captions use chapter-based numbering ({found_count} found) (0.4 pts)")
            total_score += 0.4
        elif found_count >= 8:
            partial = round(0.4 * found_count / 12, 2)
            print(f"PARTIAL: Component 1 -- {found_count}/12 figure captions use chapter-based numbering ({partial} pts)")
            total_score += partial
        elif found_count >= 1:
            partial = round(0.4 * found_count / 12, 2)
            print(f"PARTIAL: Component 1 -- {found_count}/12 figure captions use chapter-based numbering ({partial} pts)")
            total_score += partial
        else:
            # Check if old sequential numbering still exists (Figure N without dot)
            seq_pattern = re.compile(r'^Figure\s+\d+\s*[:\-]')
            seq_figs = [t for t in para_texts if seq_pattern.match(t) and not chapter_fig_pattern.match(t)]
            print(f"FAIL: Component 1 -- No chapter-based figure captions found. Sequential captions found: {len(seq_figs)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # ----------------------------------------------------------------
    # Component 2: Table of Figures section exists with entries (0.3 points)
    # ----------------------------------------------------------------
    try:
        tof_entries = []

        # Look for a heading or paragraph containing "Table of Figures"
        tof_start_idx = -1
        for i, p in enumerate(all_paras):
            text = p.text.strip()
            if 'table of figures' in text.lower():
                tof_start_idx = i
                break

        if tof_start_idx >= 0:
            # Collect ToF entries after the heading
            # ToF entries typically contain "Figure X.Y" and may have tab + page number
            tof_fig_pattern = re.compile(r'Figure\s+\d+\.\d+')
            for j in range(tof_start_idx + 1, len(all_paras)):
                text = all_paras[j].text.strip()
                if not text:
                    continue
                # Stop at the next Heading 1 (chapter start)
                style = all_paras[j].style.name if all_paras[j].style else ''
                if style == 'Heading 1' and 'figure' not in text.lower():
                    break
                if tof_fig_pattern.search(text):
                    tof_entries.append(text)

            entry_count = len(tof_entries)
            if entry_count >= 12:
                print(f"PASS: Component 2 -- Table of Figures found with {entry_count} chapter-numbered entries (0.3 pts)")
                total_score += 0.3
            elif entry_count >= 6:
                partial = round(0.3 * entry_count / 12, 2)
                print(f"PARTIAL: Component 2 -- Table of Figures found with {entry_count}/12 entries ({partial} pts)")
                total_score += partial
            elif entry_count >= 1:
                partial = round(0.3 * entry_count / 12, 2)
                print(f"PARTIAL: Component 2 -- Table of Figures found with {entry_count}/12 entries ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 -- Table of Figures heading found but no chapter-numbered entries")
        else:
            print(f"FAIL: Component 2 -- No 'Table of Figures' section found in document")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # ----------------------------------------------------------------
    # Component 3: Correct chapter-figure mapping (0.3 points)
    # Ch1 -> Figure 1.1-1.4 (4 figs), Ch2 -> Figure 2.1-2.3 (3 figs),
    # Ch3 -> Figure 3.1-3.5 (5 figs)
    # ----------------------------------------------------------------
    try:
        # Parse body figure captions and check chapter assignment
        # Walk through paragraphs tracking current chapter
        current_chapter = 0
        chapter_heading_pattern = re.compile(r'Chapter\s+(\d+)')
        figures_by_chapter = {1: [], 2: [], 3: []}
        skip_tof_section = False

        for p in all_paras:
            text = p.text.strip()
            style = p.style.name if p.style else ''

            # Detect Table of Figures section to skip it
            if 'table of figures' in text.lower():
                skip_tof_section = not False  # entering ToF zone
                continue

            # Detect chapter headings
            if style == 'Heading 1':
                ch_match = chapter_heading_pattern.search(text)
                if ch_match:
                    current_chapter = int(ch_match.group(1))
                    skip_tof_section = not True  # leaving ToF zone
                    continue
                elif skip_tof_section:
                    skip_tof_section = not True  # leaving ToF zone

            if skip_tof_section:
                continue

            # Check for figure captions in body
            fig_match = re.match(r'^Figure\s+(\d+)\.(\d+)', text)
            if fig_match and current_chapter > 0:
                ch_num = int(fig_match.group(1))
                fig_num = int(fig_match.group(2))
                if current_chapter in figures_by_chapter:
                    figures_by_chapter[current_chapter].append(f"Figure {ch_num}.{fig_num}")

        # Verify mapping
        correct_chapters = 0
        total_checks = 3
        for ch, expected_figs in CHAPTER_FIGURES.items():
            actual = figures_by_chapter.get(ch, [])
            if len(actual) == len(expected_figs):
                # Check that chapter number matches
                all_correct = all(f.startswith(f"Figure {ch}.") for f in actual)
                if all_correct:
                    correct_chapters += 1
                    print(f"  Chapter {ch}: {len(actual)} figures correctly mapped")
                else:
                    print(f"  Chapter {ch}: {len(actual)} figures but wrong chapter prefix (expected 'Figure {ch}.*')")
            else:
                print(f"  Chapter {ch}: Expected {len(expected_figs)} figures, found {len(actual)}")

        if correct_chapters == 3:
            print(f"PASS: Component 3 -- All 3 chapters have correct figure mapping (0.3 pts)")
            total_score += 0.3
        elif correct_chapters >= 1:
            partial = round(0.3 * correct_chapters / 3, 2)
            print(f"PARTIAL: Component 3 -- {correct_chapters}/3 chapters correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 -- No chapters have correct figure mapping")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

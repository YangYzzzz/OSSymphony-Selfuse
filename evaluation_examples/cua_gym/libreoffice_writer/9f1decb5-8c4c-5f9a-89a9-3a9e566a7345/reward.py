"""
Reward Script: Screenplay Formatting — Courier New, Bold/Centered Names, Indented Dialogue, Italic Stage Directions
Task ID: writer_creative_012
Domain: libreoffice_writer
Scoring:
  Component 1: Entire document uses Courier New 12pt font          — 0.20 pts
  Component 2: Character name paragraphs bold + centered           — 0.30 pts
  Component 3: Dialogue paragraphs indented 1.5in left and right   — 0.30 pts
  Component 4: Stage direction paragraphs italic                   — 0.20 pts
  Total: 1.0
"""

import os
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

WORKDIR = '/home/user'
TASK_ID = 'writer_creative_012'

# Expected values (from task context and golden_env inspection)
EXPECTED_FONT = 'Courier New'
EXPECTED_FONT_SIZE_PT = 12.0
EXPECTED_INDENT_EMU = 1371600        # 1.5 inches in EMU (914400 EMU/inch * 1.5)
INDENT_TOLERANCE_EMU = 45720         # ±0.05 inch tolerance
CHARACTER_NAMES = {'JACK', 'ELENA', 'NARRATOR'}


def is_character_name(text):
    """Return True if paragraph text is a known character name."""
    return text.strip() in CHARACTER_NAMES


def is_stage_direction(text):
    """Return True if paragraph text is a stage direction (enclosed in brackets)."""
    stripped = text.strip()
    return stripped.startswith('[') and stripped.endswith(']')


def is_dialogue(para_index, paragraphs):
    """
    Return True if the paragraph is likely a dialogue line:
    - Not a character name
    - Not a stage direction
    - Not the title (index 0)
    """
    text = paragraphs[para_index].text.strip()
    if para_index == 0:
        return False
    if not text:
        return False
    if is_character_name(text):
        return False
    if is_stage_direction(text):
        return False
    return True


def verify_task(file_path):
    """
    Verify screenplay formatting task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must load correctly
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paragraphs = doc.paragraphs
    if not paragraphs:
        print("CRITICAL: Document has no paragraphs")
        print("REWARD: 0.0")
        return 0.0

    # -----------------------------------------------------------------------
    # Component 1: Entire document uses Courier New 12pt font (0.20 points)
    # Task instruction: "Set the whole doc to Courier New 12pt"
    # Initial state: All Arial 12pt — so font_name change is the key signal
    # -----------------------------------------------------------------------
    try:
        courier_runs = 0
        non_courier_runs = 0
        correct_size_runs = 0
        wrong_size_runs = 0

        for para in paragraphs:
            if not para.text.strip():
                continue
            for run in para.runs:
                if not run.text.strip():
                    continue
                fn = run.font.name
                fs = run.font.size

                if fn == EXPECTED_FONT:
                    courier_runs += 1
                else:
                    non_courier_runs += 1

                if fs is not None:
                    size_pt = fs.pt
                    if abs(size_pt - EXPECTED_FONT_SIZE_PT) < 0.5:
                        correct_size_runs += 1
                    else:
                        wrong_size_runs += 1

        total_runs = courier_runs + non_courier_runs
        if total_runs == 0:
            print("FAIL: Component 1 — No runs with text found")
        elif non_courier_runs == 0:
            print(f"PASS: Component 1 — All {courier_runs} text runs use Courier New 12pt (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — {non_courier_runs}/{total_runs} runs do NOT use Courier New "
                  f"(found non-Courier runs)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: Character name paragraphs are bold AND centered (0.30 points)
    # Character names: JACK, ELENA, NARRATOR (appear 6 times total)
    # Initial state: left-aligned, not bold
    # -----------------------------------------------------------------------
    try:
        char_name_paras_found = 0
        char_name_bold_centered = 0

        for para in paragraphs:
            text = para.text.strip()
            if is_character_name(text):
                char_name_paras_found += 1
                pf = para.paragraph_format
                # Check alignment
                aligned_center = (pf.alignment == WD_PARAGRAPH_ALIGNMENT.CENTER)
                # Check bold — must be bold in at least one run
                all_bold = all(
                    run.font.bold is True
                    for run in para.runs
                    if run.text.strip()
                )
                if aligned_center and all_bold:
                    char_name_bold_centered += 1
                else:
                    reason = []
                    if not aligned_center:
                        reason.append(f"alignment={pf.alignment}")
                    if not all_bold:
                        reason.append("not bold")
                    print(f"FAIL: Component 2 — '{text}' NOT bold+centered: {', '.join(reason)}")

        if char_name_paras_found == 0:
            print("FAIL: Component 2 — No character name paragraphs found")
        elif char_name_bold_centered == char_name_paras_found:
            print(f"PASS: Component 2 — All {char_name_paras_found} character name paragraphs "
                  f"are bold and centered (0.30 pts)")
            total_score += 0.30
        elif char_name_bold_centered > 0:
            partial = round(0.30 * char_name_bold_centered / char_name_paras_found, 4)
            print(f"PARTIAL: Component 2 — {char_name_bold_centered}/{char_name_paras_found} "
                  f"character name paragraphs bold+centered (+{partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — 0/{char_name_paras_found} character name paragraphs "
                  f"are bold and centered")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: Dialogue paragraphs indented ~1.5in left and right (0.30 points)
    # Dialogue paragraphs: the non-title, non-character-name, non-stage-direction lines
    # Initial state: no indentation (left_indent=None)
    # -----------------------------------------------------------------------
    try:
        dialogue_paras_found = 0
        dialogue_indented = 0

        for i, para in enumerate(paragraphs):
            if is_dialogue(i, paragraphs):
                dialogue_paras_found += 1
                pf = para.paragraph_format
                li = pf.left_indent
                ri = pf.right_indent
                # Check both left and right are within tolerance of 1.5in
                left_ok = (li is not None and
                           abs(li - EXPECTED_INDENT_EMU) <= INDENT_TOLERANCE_EMU)
                right_ok = (ri is not None and
                            abs(ri - EXPECTED_INDENT_EMU) <= INDENT_TOLERANCE_EMU)
                if left_ok and right_ok:
                    dialogue_indented += 1
                else:
                    li_in = round(li / 914400, 3) if li else None
                    ri_in = round(ri / 914400, 3) if ri else None
                    print(f"FAIL: Component 3 — Dialogue para {i} "
                          f"left={li_in}in, right={ri_in}in (expected 1.5in each)")

        if dialogue_paras_found == 0:
            print("FAIL: Component 3 — No dialogue paragraphs identified")
        elif dialogue_indented == dialogue_paras_found:
            print(f"PASS: Component 3 — All {dialogue_paras_found} dialogue paragraphs "
                  f"indented 1.5in left and right (0.30 pts)")
            total_score += 0.30
        elif dialogue_indented > 0:
            partial = round(0.30 * dialogue_indented / dialogue_paras_found, 4)
            print(f"PARTIAL: Component 3 — {dialogue_indented}/{dialogue_paras_found} "
                  f"dialogue paragraphs properly indented (+{partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — 0/{dialogue_paras_found} dialogue paragraphs "
                  f"have 1.5in indent")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -----------------------------------------------------------------------
    # Component 4: Stage direction paragraphs are italic (0.20 points)
    # Stage directions: text in brackets like '[Jack enters the room slowly]'
    # Initial state: not italic
    # -----------------------------------------------------------------------
    try:
        stage_paras_found = 0
        stage_italic = 0

        for para in paragraphs:
            text = para.text.strip()
            if is_stage_direction(text):
                stage_paras_found += 1
                # All runs must be italic
                all_italic = all(
                    run.font.italic is True
                    for run in para.runs
                    if run.text.strip()
                )
                if all_italic:
                    stage_italic += 1
                else:
                    non_italic = [r.text for r in para.runs if r.text.strip()
                                  and r.font.italic is not True]
                    print(f"FAIL: Component 4 — Stage direction '{text[:40]}' "
                          f"has non-italic runs: {non_italic}")

        if stage_paras_found == 0:
            print("FAIL: Component 4 — No stage direction paragraphs identified")
        elif stage_italic == stage_paras_found:
            print(f"PASS: Component 4 — All {stage_paras_found} stage direction paragraphs "
                  f"are italic (0.20 pts)")
            total_score += 0.20
        elif stage_italic > 0:
            partial = round(0.20 * stage_italic / stage_paras_found, 4)
            print(f"PARTIAL: Component 4 — {stage_italic}/{stage_paras_found} "
                  f"stage direction paragraphs italic (+{partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — 0/{stage_paras_found} stage direction paragraphs "
                  f"are italic")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Final score
    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in the VM environment
# Both initial and golden states place the file at /home/user/screenplay_scene.docx
file_path = f'{WORKDIR}/screenplay_scene.docx'

if not os.path.exists(file_path):
    # Fallback: try Desktop location (initial setup also places file there)
    alt_path = f'{WORKDIR}/Desktop/screenplay_scene.docx'
    if os.path.exists(alt_path):
        file_path = alt_path
    else:
        print(f"File not found: {file_path}")
        print("REWARD: 0.0")
        exit(0)

verify_task(file_path)

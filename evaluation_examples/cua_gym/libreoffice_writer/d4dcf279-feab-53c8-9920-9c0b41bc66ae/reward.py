"""
Reward Script: Screenplay formatting — character names centered with 24pt spacing,
dialogue with 2.54cm L/R indent, stage directions italic with 5.08cm left indent and single spacing.
Task ID: wrpara_032
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35) — Character names: centered alignment + 24pt space_before
  Component 2 (0.35) — Dialogue lines: 2.54cm left indent + 2.54cm right indent
  Component 3 (0.30) — Stage directions: 5.08cm left indent + italic + single line spacing
"""

import os
from docx import Document
from docx.shared import Pt, Emu, Cm
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

WORKDIR = '/home/user'
TASK_ID = 'wrpara_032'

# Tolerance for EMU comparisons (allow ~5% tolerance)
EMU_TOLERANCE = 0.10  # 10% relative tolerance

def close_enough(actual_emu, expected_emu, rel_tol=EMU_TOLERANCE):
    """Check if actual EMU value is close enough to expected."""
    if actual_emu is None:
        return False
    if expected_emu == 0:
        return actual_emu == 0
    return abs(actual_emu - expected_emu) / abs(expected_emu) <= rel_tol


def classify_paragraphs(doc):
    """
    Classify non-empty paragraphs into character names, dialogue, and stage directions.
    Based on text content patterns in the screenplay.
    - Character names: ALL CAPS single-word lines (ALICE, BOB, CAROL)
    - Stage directions: text in parentheses
    - Dialogue: lines following a character name
    Returns dicts mapping paragraph index to paragraph object.
    """
    character_names = {}
    dialogue_lines = {}
    stage_directions = {}

    known_characters = {'ALICE', 'BOB', 'CAROL'}

    for i, para in enumerate(doc.paragraphs):
        text = para.text.strip()
        if not text:
            continue

        # Character names: known character names in ALL CAPS
        if text in known_characters:
            character_names[i] = para
        # Stage directions: lines that start with '('
        elif text.startswith('(') and not text.startswith('(empty'):
            stage_directions[i] = para
        # Dialogue: non-empty lines that are not the title, scene heading, or empty
        elif text not in ('UNTITLED SCREENPLAY', 'INT. CORPORATE CONFERENCE ROOM - MORNING'):
            dialogue_lines[i] = para

    return character_names, dialogue_lines, stage_directions


def verify_task(file_path):
    """
    Verify screenplay formatting with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    character_names, dialogue_lines, stage_directions = classify_paragraphs(doc)

    print(f"Found {len(character_names)} character name paragraphs: {list(character_names.keys())}")
    print(f"Found {len(dialogue_lines)} dialogue paragraphs: {list(dialogue_lines.keys())}")
    print(f"Found {len(stage_directions)} stage direction paragraphs: {list(stage_directions.keys())}")
    print()

    # Expected EMU values
    EXPECTED_SPACE_BEFORE = Pt(24)  # 304800 EMU (24pt)
    EXPECTED_DIALOGUE_INDENT = Cm(2.54)  # 914400 EMU
    EXPECTED_STAGE_INDENT = Cm(5.08)  # 1828800 EMU

    # Component 1: Character names — centered + 24pt space_before (0.35 points)
    # Task: "character names centered with 24pt spacing before"
    try:
        if len(character_names) == 0:
            print("FAIL: Component 1 — no character name paragraphs found")
        else:
            centered_count = 0
            spacing_count = 0
            total_names = len(character_names)

            for idx, para in character_names.items():
                pf = para.paragraph_format
                # Check centered alignment
                is_centered = (pf.alignment == WD_PARAGRAPH_ALIGNMENT.CENTER)
                # Check space_before ~24pt (304800 EMU)
                has_spacing = close_enough(
                    pf.space_before if pf.space_before is not None else 0,
                    int(EXPECTED_SPACE_BEFORE)
                )

                if is_centered:
                    centered_count += 1
                if has_spacing:
                    spacing_count += 1

                status_c = "OK" if is_centered else "MISSING"
                status_s = "OK" if has_spacing else "MISSING"
                print(f"  P{idx} '{para.text}': centered={status_c}, space_before={pf.space_before} (expect ~{int(EXPECTED_SPACE_BEFORE)}) {status_s}")

            # Both sub-checks must pass for all character names
            center_ratio = centered_count / total_names
            spacing_ratio = spacing_count / total_names

            comp1_score = 0.0
            if center_ratio == 1.0:
                comp1_score += 0.175
            if spacing_ratio == 1.0:
                comp1_score += 0.175

            if comp1_score > 0:
                print(f"PASS: Component 1 — character names: centered={centered_count}/{total_names}, spacing={spacing_count}/{total_names} ({comp1_score} pts)")
                total_score += comp1_score
            else:
                print(f"FAIL: Component 1 — character names: centered={centered_count}/{total_names}, spacing={spacing_count}/{total_names}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Dialogue lines — 2.54cm left + 2.54cm right indent (0.35 points)
    # Task: "dialogue with 2.54cm left and right indent"
    try:
        if len(dialogue_lines) == 0:
            print("FAIL: Component 2 — no dialogue paragraphs found")
        else:
            left_ok_count = 0
            right_ok_count = 0
            total_dialogue = len(dialogue_lines)

            for idx, para in dialogue_lines.items():
                pf = para.paragraph_format
                has_left = close_enough(
                    pf.left_indent if pf.left_indent is not None else 0,
                    int(EXPECTED_DIALOGUE_INDENT)
                )
                has_right = close_enough(
                    pf.right_indent if pf.right_indent is not None else 0,
                    int(EXPECTED_DIALOGUE_INDENT)
                )

                if has_left:
                    left_ok_count += 1
                if has_right:
                    right_ok_count += 1

                status_l = "OK" if has_left else "MISSING"
                status_r = "OK" if has_right else "MISSING"
                print(f"  P{idx} dialogue: left_indent={pf.left_indent} {status_l}, right_indent={pf.right_indent} {status_r}")

            left_ratio = left_ok_count / total_dialogue
            right_ratio = right_ok_count / total_dialogue

            comp2_score = 0.0
            if left_ratio == 1.0:
                comp2_score += 0.175
            if right_ratio == 1.0:
                comp2_score += 0.175

            if comp2_score > 0:
                print(f"PASS: Component 2 — dialogue: left_ok={left_ok_count}/{total_dialogue}, right_ok={right_ok_count}/{total_dialogue} ({comp2_score} pts)")
                total_score += comp2_score
            else:
                print(f"FAIL: Component 2 — dialogue: left_ok={left_ok_count}/{total_dialogue}, right_ok={right_ok_count}/{total_dialogue}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Stage directions — 5.08cm left indent + italic + single line spacing (0.30 points)
    # Task: "stage directions in italics with 5.08cm left indent and single line spacing"
    try:
        if len(stage_directions) == 0:
            print("FAIL: Component 3 — no stage direction paragraphs found")
        else:
            indent_ok_count = 0
            italic_ok_count = 0
            spacing_ok_count = 0
            total_sd = len(stage_directions)

            for idx, para in stage_directions.items():
                pf = para.paragraph_format

                # Check left indent ~5.08cm
                has_indent = close_enough(
                    pf.left_indent if pf.left_indent is not None else 0,
                    int(EXPECTED_STAGE_INDENT)
                )

                # Check italic on all runs with text
                runs_with_text = [r for r in para.runs if r.text.strip()]
                is_italic = len(runs_with_text) > 0 and all(r.italic for r in runs_with_text)

                # Check single line spacing (1.0)
                has_single_spacing = (pf.line_spacing is not None and
                                      abs(float(pf.line_spacing) - 1.0) < 0.05)

                if has_indent:
                    indent_ok_count += 1
                if is_italic:
                    italic_ok_count += 1
                if has_single_spacing:
                    spacing_ok_count += 1

                print(f"  P{idx} stage dir: indent={pf.left_indent} ({'OK' if has_indent else 'MISSING'}), "
                      f"italic={'OK' if is_italic else 'MISSING'}, "
                      f"line_spacing={pf.line_spacing} ({'OK' if has_single_spacing else 'MISSING'})")

            indent_ratio = indent_ok_count / total_sd
            italic_ratio = italic_ok_count / total_sd
            spacing_ratio = spacing_ok_count / total_sd

            comp3_score = 0.0
            if indent_ratio == 1.0:
                comp3_score += 0.10
            if italic_ratio == 1.0:
                comp3_score += 0.10
            if spacing_ratio == 1.0:
                comp3_score += 0.10

            if comp3_score > 0:
                print(f"PASS: Component 3 — stage dirs: indent={indent_ok_count}/{total_sd}, "
                      f"italic={italic_ok_count}/{total_sd}, spacing={spacing_ok_count}/{total_sd} ({comp3_score} pts)")
                total_score += comp3_score
            else:
                print(f"FAIL: Component 3 — stage dirs: indent={indent_ok_count}/{total_sd}, "
                      f"italic={italic_ok_count}/{total_sd}, spacing={spacing_ok_count}/{total_sd}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

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

"""
Reward Script: Line-number CodeBlock paragraphs in Writer document
Task ID: writer_tech_090
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.3): All CodeBlock paragraphs have line-number prefixes
  - Component 2 (0.3): Line numbers are sequential (1,2,3,...) restarting per block
  - Component 3 (0.2): Code content is preserved after the line-number prefix
  - Component 4 (0.2): Non-CodeBlock paragraphs are not modified with line numbers
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_tech_090'


def verify_task(file_path):
    """
    Verify that all CodeBlock-styled paragraphs have sequential line numbers
    prepended as 'N: ' prefix to each line.
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

    # Identify CodeBlock paragraphs
    codeblock_paras = []
    non_codeblock_paras = []
    for p in doc.paragraphs:
        style_name = p.style.name if p.style else 'None'
        if style_name == 'CodeBlock':
            codeblock_paras.append(p)
        else:
            non_codeblock_paras.append(p)

    # Precondition: must have CodeBlock paragraphs
    if len(codeblock_paras) == 0:
        print("FAIL: No CodeBlock paragraphs found in document")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found {len(codeblock_paras)} CodeBlock paragraphs")

    # Component 1: All CodeBlock paragraphs have line-number prefixes on every line (0.3 pts)
    # A line is considered numbered if it matches pattern: digits followed by colon and space
    LINE_NUM_PATTERN = re.compile(r'^\d+:\s')
    try:
        blocks_with_all_numbered = 0
        for idx, para in enumerate(codeblock_paras):
            lines = para.text.split('\n')
            non_empty_lines = [l for l in lines if l.strip()]
            if len(non_empty_lines) == 0:
                continue
            # Check all non-empty lines have number prefix
            all_numbered = all(
                LINE_NUM_PATTERN.match(line)
                for line in lines
                if line.strip() != ''
            )
            if all_numbered:
                blocks_with_all_numbered += 1
                print(f"  CodeBlock {idx}: all non-empty lines are numbered")
            else:
                print(f"  CodeBlock {idx}: NOT all lines are numbered")

        if blocks_with_all_numbered == len(codeblock_paras):
            print(f"PASS: Component 1 — All {len(codeblock_paras)} CodeBlocks have line numbers (0.3 pts)")
            total_score += 0.3
        elif blocks_with_all_numbered > 0:
            partial = 0.3 * (blocks_with_all_numbered / len(codeblock_paras))
            print(f"PARTIAL: Component 1 — {blocks_with_all_numbered}/{len(codeblock_paras)} CodeBlocks numbered ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No CodeBlocks have line numbers")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Line numbers are sequential starting from 1 per block (0.3 pts)
    try:
        blocks_sequential = 0
        for idx, para in enumerate(codeblock_paras):
            lines = para.text.split('\n')
            expected_num = 1
            seq_ok = (len(lines) > 0)  # start assuming ok, break on mismatch
            for line in lines:
                match = re.match(r'^(\d+):\s', line)
                if match:
                    actual_num = int(match.group(1))
                    if actual_num != expected_num:
                        print(f"  CodeBlock {idx}: expected line {expected_num}, got {actual_num}")
                        seq_ok = False
                        break
                    expected_num += 1
                elif line.strip() == '':
                    # Blank line without number — lenient: skip
                    expected_num += 1
                else:
                    # Non-empty line without number prefix
                    seq_ok = False
                    break
            if seq_ok and expected_num > 1:
                blocks_sequential += 1
                print(f"  CodeBlock {idx}: sequential numbering confirmed (1 to {expected_num - 1})")

        if blocks_sequential == len(codeblock_paras):
            print(f"PASS: Component 2 — All CodeBlocks have sequential numbering (0.3 pts)")
            total_score += 0.3
        elif blocks_sequential > 0:
            partial = 0.3 * (blocks_sequential / len(codeblock_paras))
            print(f"PARTIAL: Component 2 — {blocks_sequential}/{len(codeblock_paras)} CodeBlocks sequential ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No CodeBlocks have sequential numbering")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Line-numbered CodeBlocks preserve original code content (0.2 pts)
    # COMPOUND CHECK: lines must have number prefix AND correct code after stripping it
    # This ensures the macro added numbers without corrupting the code.
    # Fails on initial because lines don't have number prefixes.
    try:
        expected_keywords_per_block = [
            ['import socket', 'import time', 'def connect_with_retry'],
            ['class ConfigParser', 'REQUIRED_KEYS', 'def __init__'],
            ['def inspect_packets', 'cap = pcap', 'packet_count'],
        ]
        blocks_content_ok = 0
        for idx, para in enumerate(codeblock_paras):
            if idx >= len(expected_keywords_per_block):
                break
            lines = para.text.split('\n')
            # First, ALL non-empty lines must have number prefix (anchors to task change)
            has_numbers = all(
                LINE_NUM_PATTERN.match(line) or line.strip() == ''
                for line in lines
            )
            if not has_numbers:
                print(f"  CodeBlock {idx}: no line numbers — content check skipped (anchored)")
                continue

            # Strip line number prefixes to get raw content
            stripped_lines = []
            for line in lines:
                m = re.match(r'^\d+:\s?(.*)', line)
                if m:
                    stripped_lines.append(m.group(1))
                else:
                    stripped_lines.append(line)
            full_text = '\n'.join(stripped_lines)

            keywords = expected_keywords_per_block[idx]
            found_all = all(kw in full_text for kw in keywords)
            if found_all:
                blocks_content_ok += 1
                print(f"  CodeBlock {idx}: numbered AND content preserved")
            else:
                missing = [kw for kw in keywords if kw not in full_text]
                print(f"  CodeBlock {idx}: numbered but missing keywords: {missing}")

        check_count = min(len(codeblock_paras), len(expected_keywords_per_block))
        if check_count > 0 and blocks_content_ok == check_count:
            print(f"PASS: Component 3 — Numbered CodeBlocks preserve code content (0.2 pts)")
            total_score += 0.2
        elif blocks_content_ok > 0:
            partial = 0.2 * (blocks_content_ok / check_count)
            print(f"PARTIAL: Component 3 — {blocks_content_ok}/{check_count} numbered CodeBlocks have content ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No numbered CodeBlocks with preserved content")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: CodeBlocks are numbered AND non-CodeBlock paragraphs are NOT numbered (0.2 pts)
    # COMPOUND CHECK: requires that at least one CodeBlock IS numbered (anchors to task change)
    # AND that no non-CodeBlock paragraph was incorrectly numbered.
    # Fails on initial because the anchor condition (CodeBlocks numbered) is false.
    try:
        # Anchor: at least one CodeBlock must have line numbers
        any_codeblock_numbered = any(
            all(LINE_NUM_PATTERN.match(l) for l in [ln for ln in para.text.split('\n') if ln.strip()])
            and len([ln for ln in para.text.split('\n') if ln.strip()]) > 0
            for para in codeblock_paras
        )

        if not any_codeblock_numbered:
            print(f"FAIL: Component 4 — No CodeBlocks are numbered, so selectivity check fails (anchored)")
        else:
            non_code_with_numbers = 0
            total_non_code_checked = 0
            for para in non_codeblock_paras:
                text = para.text.strip()
                if not text:
                    continue
                total_non_code_checked += 1
                if LINE_NUM_PATTERN.match(text):
                    non_code_with_numbers += 1
                    print(f"  Non-CodeBlock para incorrectly numbered: [{text[:60]}]")

            if non_code_with_numbers == 0:
                print(f"PASS: Component 4 — CodeBlocks numbered AND non-CodeBlock paras untouched (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 — {non_code_with_numbers} non-CodeBlock paragraphs incorrectly have line numbers")
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

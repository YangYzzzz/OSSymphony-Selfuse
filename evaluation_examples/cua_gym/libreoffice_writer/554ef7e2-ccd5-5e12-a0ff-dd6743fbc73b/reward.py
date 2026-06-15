"""
Reward Script: Verify endnote settings changes in Writer document
Task ID: writer_bs_018
Domain: libreoffice_writer

Scoring rubric (3 components, sum to 1.0):
  Component 1: Endnote position set to "sectEnd" in all sections (0.4 pts)
  Component 2: Endnote numbering format set to "lowerLetter" in all sections (0.35 pts)
  Component 3: Endnote numbering restarts each section ("eachSect") in all sections (0.25 pts)

Verification approach: Parse the docx XML (word/document.xml) to inspect
<w:endnotePr> inside each <w:sectPr>. This is a direct check of the OOxml
properties that control endnote placement, format, and restart behaviour.
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_bs_018'

W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W_NS}


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ── Load the docx as a ZIP and parse document.xml ──────────────────
    try:
        zf = zipfile.ZipFile(file_path)
        doc_xml = zf.read('word/document.xml')
        root = ET.fromstring(doc_xml)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # ── Locate all <w:sectPr> elements ─────────────────────────────────
    sections = root.findall('.//w:sectPr', NS)
    num_sections = len(sections)
    if num_sections == 0:
        print("FAIL: No sections found in document")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found {num_sections} section(s)")

    # ── Component 1: Endnote position == "sectEnd" (0.4 pts) ──────────
    # In the initial file, there is NO <w:pos> element; default is docEnd.
    # Golden should have <w:pos val="sectEnd"/> in every section.
    try:
        pos_pass_count = 0
        for i, sect in enumerate(sections):
            endnote_pr = sect.find('w:endnotePr', NS)
            if endnote_pr is not None:
                pos_elem = endnote_pr.find('w:pos', NS)
                if pos_elem is not None:
                    val = pos_elem.get(f'{{{W_NS}}}val')
                    if val == 'sectEnd':
                        pos_pass_count += 1
                        continue
            print(f"  Section {i}: endnote pos is NOT 'sectEnd'")

        if pos_pass_count == num_sections:
            print(f"PASS: Component 1 — All {num_sections} sections have endnote pos='sectEnd' (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Only {pos_pass_count}/{num_sections} sections have pos='sectEnd'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ── Component 2: Endnote numFmt == "lowerLetter" (0.35 pts) ───────
    # Initial file has numFmt="lowerRoman". Golden should be "lowerLetter".
    try:
        fmt_pass_count = 0
        for i, sect in enumerate(sections):
            endnote_pr = sect.find('w:endnotePr', NS)
            if endnote_pr is not None:
                fmt_elem = endnote_pr.find('w:numFmt', NS)
                if fmt_elem is not None:
                    val = fmt_elem.get(f'{{{W_NS}}}val')
                    if val == 'lowerLetter':
                        fmt_pass_count += 1
                        continue
            print(f"  Section {i}: endnote numFmt is NOT 'lowerLetter'")

        if fmt_pass_count == num_sections:
            print(f"PASS: Component 2 — All {num_sections} sections have numFmt='lowerLetter' (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — Only {fmt_pass_count}/{num_sections} sections have numFmt='lowerLetter'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ── Component 3: Endnote numRestart == "eachSect" (0.25 pts) ──────
    # Initial file has no numRestart element (continuous). Golden should
    # have numRestart="eachSect" so numbering restarts from 'a' per section.
    try:
        restart_pass_count = 0
        for i, sect in enumerate(sections):
            endnote_pr = sect.find('w:endnotePr', NS)
            if endnote_pr is not None:
                restart_elem = endnote_pr.find('w:numRestart', NS)
                if restart_elem is not None:
                    val = restart_elem.get(f'{{{W_NS}}}val')
                    if val == 'eachSect':
                        restart_pass_count += 1
                        continue
            print(f"  Section {i}: endnote numRestart is NOT 'eachSect'")

        if restart_pass_count == num_sections:
            print(f"PASS: Component 3 — All {num_sections} sections have numRestart='eachSect' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — Only {restart_pass_count}/{num_sections} sections have numRestart='eachSect'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# ── Entry point ────────────────────────────────────────────────────────
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

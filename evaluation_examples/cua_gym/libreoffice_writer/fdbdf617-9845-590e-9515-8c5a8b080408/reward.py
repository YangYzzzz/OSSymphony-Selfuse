"""
Reward Script: Insert cross-reference to 'Chapter 4: Discussion' heading
Task ID: writer_struct_017
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): Hyperlink with text 'see Chapter 4: Discussion' exists in the
                     paragraph ending with 'The implications are explored later ('
  Component 2 (0.3): The hyperlink run uses the 'Hyperlink' character style
  Component 3 (0.2): The hyperlink has an internal anchor reference targeting Chapter 4
"""

import os
from docx import Document
from docx.oxml.ns import qn
import lxml.etree as etree

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_struct_017'
FILE_PATH = os.path.join(WORKDIR, 'phd_thesis.docx')

W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'


def find_implications_paragraph(doc):
    """Find the paragraph that ends with 'The implications are explored later (' """
    for i, para in enumerate(doc.paragraphs):
        if 'The implications are explored later' in para.text:
            return i, para
    return None, None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Locate the target paragraph
    para_idx, target_para = find_implications_paragraph(doc)
    if target_para is None:
        print("CRITICAL: Could not find paragraph with 'The implications are explored later (' — document structure unexpected.")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found target paragraph at index {para_idx}")

    # Component 1: Hyperlink element exists in the target paragraph with correct text (0.5 points)
    # The task requires 'see Chapter 4: Discussion' to appear as a hyperlink after the opening parenthesis.
    # In initial_env this hyperlink does NOT exist — it must be added by the agent.
    try:
        # Find all w:hyperlink children in the paragraph XML
        hyperlink_elements = target_para._element.findall(
            '{%s}hyperlink' % W_NS
        )

        hyperlink_text_found = None
        hyperlink_elem_found = None
        for hl in hyperlink_elements:
            # Collect all text under the hyperlink
            hl_text = ''.join(
                t.text or '' for t in hl.findall('.//{%s}t' % W_NS)
            )
            if hl_text:
                hyperlink_text_found = hl_text
                hyperlink_elem_found = hl
                break

        if hyperlink_elem_found is not None and 'see Chapter 4: Discussion' in hyperlink_text_found:
            print(f"PASS: Component 1 — Hyperlink with text 'see Chapter 4: Discussion' found in target paragraph (0.5 pts)")
            print(f"      Hyperlink text: '{hyperlink_text_found}'")
            total_score += 0.5
        else:
            if hyperlink_elem_found is None:
                print("FAIL: Component 1 — No hyperlink element found in target paragraph")
            else:
                print(f"FAIL: Component 1 — Hyperlink found but text is '{hyperlink_text_found}', expected 'see Chapter 4: Discussion'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The hyperlink run uses 'Hyperlink' character style (0.3 points)
    # In the golden file, the hyperlink run has <w:rStyle w:val="Hyperlink"/>
    # This indicates it is formatted as a proper hyperlink (not plain text).
    try:
        if hyperlink_elem_found is not None:
            # Check for rStyle = "Hyperlink" in any run within the hyperlink
            r_style_found = False
            for run_elem in hyperlink_elem_found.findall('{%s}r' % W_NS):
                rPr = run_elem.find('{%s}rPr' % W_NS)
                if rPr is not None:
                    rStyle = rPr.find('{%s}rStyle' % W_NS)
                    if rStyle is not None:
                        style_val = rStyle.get('{%s}val' % W_NS)
                        if style_val == 'Hyperlink':
                            r_style_found = True
                            break
            if r_style_found:
                print("PASS: Component 2 — Hyperlink run has 'Hyperlink' character style (0.3 pts)")
                total_score += 0.3
            else:
                print("FAIL: Component 2 — Hyperlink run does not have 'Hyperlink' character style")
        else:
            print("FAIL: Component 2 — Cannot check style; no hyperlink element was found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The hyperlink uses an internal anchor pointing to Chapter 4 (0.2 points)
    # The cross-reference should target the 'Chapter 4: Discussion' heading bookmark.
    # In the golden file: <w:hyperlink r:id="rId9" w:anchor="_Chapter4_Discussion">
    # Either the w:anchor attribute OR the relationship target should reference Chapter 4.
    try:
        if hyperlink_elem_found is not None:
            anchor_attr = hyperlink_elem_found.get('{%s}anchor' % W_NS)
            r_id_attr = hyperlink_elem_found.get('{%s}id' % R_NS)

            anchor_valid = False
            # Check w:anchor attribute (internal bookmark anchor)
            if anchor_attr is not None:
                # Anchor should reference Chapter 4
                if 'Chapter4' in anchor_attr or 'chapter4' in anchor_attr.lower() or 'Discussion' in anchor_attr:
                    anchor_valid = True
                    print(f"PASS: Component 3 — Hyperlink has internal anchor '{anchor_attr}' referencing Chapter 4 (0.2 pts)")

            # Also check relationship target (rId) if anchor not found
            if not anchor_valid and r_id_attr is not None:
                try:
                    rel = doc.part.rels.get(r_id_attr)
                    if rel is not None:
                        target_ref = str(rel.target_ref)
                        if 'Chapter4' in target_ref or 'chapter4' in target_ref.lower() or 'Discussion' in target_ref or target_ref.startswith('#'):
                            anchor_valid = True
                            print(f"PASS: Component 3 — Hyperlink relationship '{r_id_attr}' targets '{target_ref}' (Chapter 4) (0.2 pts)")
                except Exception as rel_e:
                    print(f"INFO: Component 3 — Could not resolve relationship {r_id_attr}: {rel_e}")

            # Fallback: if a hyperlink exists at all with some anchor, it's likely an internal cross-reference
            if not anchor_valid and (anchor_attr is not None or r_id_attr is not None):
                # Check if the relationship is an internal hyperlink (#...)
                if anchor_attr is not None:
                    # Any anchor is an internal reference — accept it if hyperlink text was correct
                    # This handles cases where anchor name differs slightly
                    anchor_lower = anchor_attr.lower()
                    if 'chapter' in anchor_lower or 'discussion' in anchor_lower or anchor_lower.startswith('_'):
                        anchor_valid = True
                        print(f"PASS: Component 3 — Hyperlink has internal anchor '{anchor_attr}' (0.2 pts)")

            if anchor_valid:
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — Hyperlink does not have valid Chapter 4 anchor (anchor={anchor_attr}, rId={r_id_attr})")
        else:
            print("FAIL: Component 3 — Cannot check anchor; no hyperlink element was found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

"""
Reward Script: Set alternative text (description) of image on page 1 to 'Company Logo - Acme Corp'
Task ID: writer_obj_015
Domain: libreoffice_writer
Scoring:
  Component 1: Image alt text (description) is non-empty             — 0.4 pts
  Component 2: Image alt text matches exactly 'Company Logo - Acme Corp' — 0.6 pts
  Total: 1.0
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_obj_015'
FILE_PATH = f'{WORKDIR}/Desktop/accessible_doc.docx'

EXPECTED_DESCRIPTION = 'Company Logo - Acme Corp'


def verify_task(file_path):
    """
    Verify that the image on page 1 has its alternative text (description)
    set to 'Company Logo - Acme Corp'.

    Uses the docPr XML element inside drawing elements in the document body,
    which carries the 'descr' attribute for alt text.

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the document — gate: if unreadable, return 0.0
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all docPr elements from the document body
    # docPr carries name, descr (alt text description), and title for images
    doc_pr_elements = []
    try:
        for elem in doc.element.body.iter():
            tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
            if tag == 'docPr':
                doc_pr_elements.append(elem)
    except Exception as e:
        print(f"ERROR: Could not iterate document body elements: {e}")
        print("REWARD: 0.0")
        return 0.0

    if not doc_pr_elements:
        print("FAIL: No image (docPr) elements found in document body")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Use the first docPr element (corresponding to the image on page 1)
    first_doc_pr = doc_pr_elements[0]
    actual_description = first_doc_pr.get('descr', '')
    image_name = first_doc_pr.get('name', '<unknown>')

    print(f"INFO: Found image '{image_name}' with descr={actual_description!r}")

    # Component 1: Image alt text description is non-empty (0.4 points)
    # This FAILS on initial_env (descr='') and PASSES on golden_env (descr='Company Logo - Acme Corp')
    try:
        if actual_description and actual_description.strip():
            print(f"PASS: Component 1 — alt text description is non-empty: {actual_description!r} (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — alt text description is empty (expected non-empty)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Image alt text matches exactly 'Company Logo - Acme Corp' (0.6 points)
    # This FAILS on initial_env (descr='') and PASSES on golden_env (descr='Company Logo - Acme Corp')
    try:
        if actual_description == EXPECTED_DESCRIPTION:
            print(f"PASS: Component 2 — alt text matches exactly '{EXPECTED_DESCRIPTION}' (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 2 — expected '{EXPECTED_DESCRIPTION}', found: {actual_description!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

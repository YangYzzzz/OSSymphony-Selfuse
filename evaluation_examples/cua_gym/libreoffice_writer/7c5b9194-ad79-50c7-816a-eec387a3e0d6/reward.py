"""
FINAL REWARD SCRIPT - SUCCESS
Task: Insert "Grassi, D., et al. (2005). Cocoa reduces blood pressure and insulin resistance. Hypertension, 46(2), 398–405." into my References and use its number at the "<citation>" placeholder in the Discussion’s first paragraph.
Generated: 2025-10-14 12:03:44
Status: success
Model: azure-o3
Total Steps: 3
"""

from docx import Document
import os
import re


def verify_task(file_path: str) -> float:
    """
    Verification logic for the task:
      1.   A new reference (Grassi, D., et al. 2005 …) must be present in the References list.
      2.   This reference must be numbered and its position number must be used to
           replace the “<citation>” placeholder in the first paragraph of the
           Discussion section (i.e., appear as a numeric in-text citation like [4]).

    Progressive scoring (max 1.0):
        • 0.4  – Grassi reference exists in References list
        • 0.3  – Discussion first paragraph contains an in-text citation of the form [N]
        • 0.3  – The citation number N matches the position/index of the Grassi reference
    """

    max_score = 1.0
    score = 0.0

    # ---------- Load document ----------
    if not os.path.exists(file_path):
        print(f"✗ File not found: {file_path}")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Error loading DOCX: {e}")
        return 0.0

    # Gather all paragraph texts
    paragraphs = [p.text.strip() for p in doc.paragraphs]

    # ---------- Locate References section ----------
    try:
        ref_heading_idx = next(i for i, t in enumerate(paragraphs) if t.lower() == "references")
        print(f"✓ 'References' heading found at paragraph {ref_heading_idx}")
    except StopIteration:
        print("✗ 'References' heading not found")
        ref_heading_idx = None

    references = []
    if ref_heading_idx is not None:
        # Collect reference lines until end of doc or until we hit another major heading
        for t in paragraphs[ref_heading_idx + 1 :]:
            if t == "" or t.lower() in {"abstract", "introduction", "discussion", "conclusion"}:
                break
            references.append(t)

    print(f"Detected {len(references)} reference entries")
    for i, ref in enumerate(references, 1):
        print(f"  {i}. {ref}")

    # ---------- Verify Grassi reference ----------
    grassi_idx = None  # 1-based index within References list
    for i, ref in enumerate(references, 1):
        if "grassi, d." in ref.lower():
            grassi_idx = i
            break

    if grassi_idx is not None:
        print(f"✓ Grassi reference found at position {grassi_idx}")
        score += 0.4
    else:
        print("✗ Grassi reference not found")

    # ---------- Locate Discussion section ----------
    try:
        disc_idx = next(i for i, t in enumerate(paragraphs) if t.lower() == "discussion")
        print(f"✓ 'Discussion' heading found at paragraph {disc_idx}")
    except StopIteration:
        print("✗ 'Discussion' heading not found")
        disc_idx = None

    discussion_para = None
    if disc_idx is not None and disc_idx + 1 < len(paragraphs):
        discussion_para = paragraphs[disc_idx + 1]
        print("Discussion first paragraph:", discussion_para)
    else:
        print("✗ Discussion first paragraph not found")

    # ---------- Verify citation in Discussion ----------
    citation_number = None
    if discussion_para:
        m = re.search(r"\[(\d+)\]", discussion_para)
        if m:
            citation_number = int(m.group(1))
            print(f"✓ Found in-text citation [ {citation_number} ] in Discussion paragraph")
            score += 0.3
        else:
            print("✗ Numeric citation not found in Discussion paragraph")

    # ---------- Cross-validate reference number ----------
    if grassi_idx is not None and citation_number is not None:
        if citation_number == grassi_idx:
            print("✓ Citation number matches Grassi reference position")
            score += 0.3
        else:
            print("✗ Citation number does NOT match Grassi reference position")

    final_score = min(score, max_score)
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    path = "/home/user/insert_grassi_d_et_al_2005_cocoa_reduces_blood_pressure_and_insulin_resistance_hypertension_462_3984.docx"
    verify_task(path)

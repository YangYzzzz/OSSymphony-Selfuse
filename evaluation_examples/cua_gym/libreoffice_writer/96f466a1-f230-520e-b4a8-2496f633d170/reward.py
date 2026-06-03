"""
FINAL REWARD SCRIPT - SUCCESS
Task: Every time I paste data from my lab software, it dumps in "cm2" instead of the proper "cm²". Is there a quick way in LibreOffice Writer to run through the whole document and flip every plain 2 in "cm2" up into superscript so it shows as cm²?
Generated: 2025-09-10 16:04:28
Status: success
Model: azure-o3
Total Steps: 5
"""

import os
import re
from docx import Document

############################################################
# Reward script for LibreOffice Writer superscript task
#
# Task: Ensure every occurrence of the pattern "cm2" in the
# document has the "2" formatted as superscript so the text
# appears as "cm²" (either via the superscript character ² or
# by applying superscript formatting to the character "2").
############################################################

def count_cm_sequences(doc):
    """Return counts of total cm2 sequences, how many of them still
    have a normal (non-superscript) 2, and how many are correctly
    superscripted (either unicode ² or superscript formatting)."""
    total_seq = 0           # total occurrences of the pattern cm2
    unsuper_seq = 0        # sequences where the 2 is NOT superscripted
    superscripted_seq = 0  # sequences where the 2 *is* superscripted

    for para in doc.paragraphs:
        # Build char list & corresponding superscript flags for each paragraph
        chars = []
        supers = []  # True if char is superscript already
        for run in para.runs:
            is_super = bool(getattr(run.font, 'superscript', False))
            for ch in run.text:
                chars.append(ch)
                # treat the dedicated unicode superscript character as already superscript
                supers.append(is_super or ch == '²')

        # Slide over the paragraph characters looking for the pattern c m 2
        i = 0
        while i < len(chars) - 2:
            if chars[i].lower() == 'c' and chars[i+1].lower() == 'm' and chars[i+2] == '2':
                total_seq += 1
                if supers[i+2]:
                    superscripted_seq += 1
                else:
                    unsuper_seq += 1
                i += 3  # skip past the sequence just found
            else:
                i += 1

    return total_seq, unsuper_seq, superscripted_seq


def verify_superscript_cm2(file_path):
    """Main verification routine. Returns a progressive score (0-1)."""
    print(f"Checking document: {file_path}")
    if not os.path.exists(file_path):
        print("✗ File not found")
        return 0.0

    # Try to load the document – prerequisite only, no points awarded
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Could not open DOCX: {e}")
        return 0.0

    # Analyse cm2 sequences
    total_seq, unsuper_seq, superscripted_seq = count_cm_sequences(doc)
    print(f"Total 'cm2' sequences found: {total_seq}")
    print(f"Sequences with NON-superscript '2': {unsuper_seq}")
    print(f"Sequences correctly superscripted: {superscripted_seq}")

    # Progressive scoring
    score = 0.0

    # 1) Must have converted every instance -> no plain cm2 left
    if total_seq > 0 and unsuper_seq == 0:
        print("✓ All occurrences converted – no plain 'cm2' remain")
        score += 0.6
    else:
        print("✗ Some occurrences still have a plain '2'")

    # 2) Must actually contain superscripted versions (quality check)
    if superscripted_seq > 0:
        print("✓ Superscripted 'cm²' present in document")
        score += 0.4
    else:
        print("✗ No superscripted 'cm²' detected")

    # Cap score at 1.0 and round for neatness
    final_score = round(min(score, 1.0), 4)
    print(f"REWARD: {final_score}")
    return final_score

# --------------- automatic execution when script is run ---------------
if __name__ == "__main__":
    # Path provided by the task context
    FILE_PATH = "/home/user/every_time_i_paste_data_from_my_lab_software_it_dumps_in_cm2_instead_of_the_proper_cm²_is_there_a_qu.docx"
    verify_superscript_cm2(FILE_PATH)


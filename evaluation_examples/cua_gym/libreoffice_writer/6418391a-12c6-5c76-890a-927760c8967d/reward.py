"""
FINAL REWARD SCRIPT - SUCCESS
Task: Please turn the 3 in "CH3COOH" into a subscript in the caption.
Generated: 2025-10-14 07:09:49
Status: success
Model: azure-o3
Total Steps: 1
"""

from docx import Document
import os

def verify_ch3cooh_subscript(file_path):
    """Verify that within the document caption the string 'CH3COOH' appears
    and ONLY the character '3' is formatted as subscript (other characters are not).

    Scoring (progressive):
        0.7 points – substring located with the '3' properly in subscript
        +0.3 points – no additional characters in that substring are subscript
        1.0 points – perfect completion of the task
    """

    total_score = 0.0
    max_score   = 1.0

    print(f"Loading document: {file_path}")

    # ----------- prerequisite: file must exist and load -------------
    if not os.path.exists(file_path):
        print("✗ File does not exist")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Failed to load document: {e}")
        print("REWARD: 0.0")
        return 0.0

    substring      = "CH3COOH"
    requirement_met = False   # found substring with 3 correctly subscripted
    exclusive_met   = False   # additionally, ONLY 3 is subscript (others normal)

    # ----------- inspect every paragraph & its runs -----------------
    for para_idx, paragraph in enumerate(doc.paragraphs):
        # Build a list where each character is paired with its subscript status
        char_props = []  # list of tuples (char, is_subscript_bool)
        for run in paragraph.runs:
            # run.font.subscript can be True / False / None
            is_sub = bool(run.font.subscript)
            for ch in run.text:
                char_props.append((ch, is_sub))

        # Quick skip if not enough characters
        if len(char_props) < len(substring):
            continue

        # Concatenate characters to locate the substring occurrence
        para_text = ''.join(ch for ch, _ in char_props)
        idx = para_text.upper().find(substring.upper())
        if idx == -1:
            continue

        # Slice out the exact segment covering the substring
        segment = char_props[idx:idx + len(substring)]
        if len(segment) != len(substring):
            continue

        segment_ok   = True  # 3 is subscript, others are not necessarily checked yet
        exclusive_ok = True  # ensure ONLY 3 is subscript

        for i, (ch, is_sub) in enumerate(segment):
            expected_char = substring[i]
            # character match (case-insensitive)
            if ch.upper() != expected_char.upper():
                segment_ok = False
                break
            # verify subscript status
            if expected_char == '3':
                if not is_sub:
                    segment_ok = False
                    break
            else:
                if is_sub:
                    exclusive_ok = False  # some non-3 char also subscripted

        if segment_ok:
            requirement_met = True
            if exclusive_ok:
                exclusive_met = True
            # if perfect, no need to keep searching further
            if exclusive_met:
                break

    # ---------------------- Scoring --------------------------
    if requirement_met:
        print("✓ Found 'CH3COOH' with '3' formatted as subscript.")
        total_score += 0.7
        if exclusive_met:
            print("✓ Only '3' is subscript within the substring.")
            total_score += 0.3
        else:
            print("✗ Additional characters besides '3' are also subscript. Partial credit awarded.")
    else:
        print("✗ Required subscript formatting for '3' in 'CH3COOH' not found.")

    # ensure score capped at 1.0
    final_score = min(total_score, max_score)
    print(f"REWARD: {final_score}")
    return final_score

# -------------------- entry point ---------------------------
if __name__ == "__main__":
    DOC_PATH = "/home/user/please_turn_the_3_in_ch3cooh_into_a_subscript_in_the_caption.docx"
    verify_ch3cooh_subscript(DOC_PATH)


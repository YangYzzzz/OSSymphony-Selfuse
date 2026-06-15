"""
FINAL REWARD SCRIPT - SUCCESS
Task: My draft is clogged with tracked changes—insertions are showing in green (#00A000) underlines, deletions in red (#FF0000) strikethrough. I want to hit one command that accepts every single insertion while rejecting all deletions so the crossed-out text comes back. How do I pull that off in LibreOffice Writer?
Generated: 2025-09-10 18:35:35
Status: success
Model: azure-o3
Total Steps: 11
"""

import os
import zipfile
from lxml import etree as ET

"""
Reward Script: Verify that all insertions have been accepted and all deletions have
been rejected in a LibreOffice/Word DOCX file (i.e. no remaining change-tracking
tags).

Scoring Rules (progressive):
  • 0.5 pts  –  All <w:ins> tags removed   (insertions accepted)
  • 0.5 pts  –  All <w:del>, <w:moveFrom>, <w:moveTo> tags removed (deletions rejected)
  • 0.25 pts –  ≤5 total tags remain in either category (partial credit)
  • 0.0  pts –  >5 tags remain or fatal error

Returns a float 0.0 – 1.0 and prints detailed diagnostics plus
   "REWARD: X.X"  (required by evaluation harness).
"""

def _count_change_tracking_tags(docx_path):
    """Count change-tracking tags across all DOCX XML parts."""
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    counts = {
        'ins': 0,
        'del': 0,
        'moveFrom': 0,
        'moveTo': 0,
    }

    with zipfile.ZipFile(docx_path) as z:
        xml_parts = [n for n in z.namelist() if n.startswith('word/') and n.endswith('.xml')]
        for part in xml_parts:
            try:
                root = ET.fromstring(z.read(part))
            except ET.XMLSyntaxError:
                # Skip non-well-formed or non-XML relationships etc.
                continue
            counts['ins']      += len(root.xpath('.//w:ins',      namespaces=ns))
            counts['del']      += len(root.xpath('.//w:del',      namespaces=ns))
            counts['moveFrom'] += len(root.xpath('.//w:moveFrom', namespaces=ns))
            counts['moveTo']   += len(root.xpath('.//w:moveTo',   namespaces=ns))
    return counts

def _partial_score(tag_total, perfect_value=0, partial_threshold=5):
    """Return 0.5, 0.25, or 0.0 depending on how many tags remain."""
    if tag_total <= perfect_value:
        return 0.5
    elif tag_total <= partial_threshold:
        return 0.25
    return 0.0

def verify_accept_insertions_reject_deletions(file_path: str) -> float:
    print(f"Verifying tracked-changes resolution for: {file_path}\n")

    # Pre-check: file existence & extension
    if not os.path.exists(file_path):
        print("✗ File does not exist.")
        print("REWARD: 0.0")
        return 0.0
    if not file_path.lower().endswith('.docx'):
        print("✗ Unsupported file format. Only .docx is verified.")
        print("REWARD: 0.0")
        return 0.0

    try:
        counts = _count_change_tracking_tags(file_path)
    except Exception as exc:
        print(f"✗ Error while processing DOCX: {exc}")
        print("REWARD: 0.0")
        return 0.0

    # Display diagnostics
    for tag, value in counts.items():
        print(f"Remaining <w:{tag}> tags: {value}")
    print()

    # Compute progressive score
    ins_score  = _partial_score(counts['ins'])
    del_score  = _partial_score(counts['del'] + counts['moveFrom'] + counts['moveTo'])
    total_score = round(min(ins_score + del_score, 1.0), 2)

    # Explanatory output
    if ins_score == 0.5:
        print("✓ All insertions accepted (no <w:ins> tags present).")
    elif ins_score == 0.25:
        print("⚠️  Some insertions remain (≤5 tags). Partial credit awarded.")
    else:
        print("✗ Numerous insertions still pending – no credit.")

    if del_score == 0.5:
        print("✓ All deletions rejected (no deletion/move tags present).")
    elif del_score == 0.25:
        print("⚠️  Some deletions remain (≤5 tags). Partial credit awarded.")
    else:
        print("✗ Numerous deletions still pending – no credit.")

    print(f"\nTotal Score: {total_score}")
    print(f"REWARD: {total_score}")
    return total_score

# =====================================================================================
# MAIN EXECUTION (adjust the default path as necessary for evaluation environment)
# =====================================================================================
if __name__ == "__main__":
    DEFAULT_DOCX = "/home/user/my_draft_is_clogged_with_tracked_changesinsertions_are_showing_in_green_00a000_underlines_deletions_.docx"
    verify_accept_insertions_reject_deletions(DEFAULT_DOCX)


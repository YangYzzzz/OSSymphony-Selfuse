"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’ve finished tweaking a small area and those marching-ants are still showing—how do I quickly deselect everything so I can work on the whole image again?
Generated: 2025-09-01 14:46:33
Status: success
Model: o3
Total Steps: 4
"""

"""Reward script for GIMP deselection task

Task Essence
------------
User had an active selection (marching-ants) and had to *deselect* everything
fast.  In GIMP this is done with Select ▸ None (Ctrl+Shift+A).  When the image
is saved after deselecting, the special *selection channel* that GIMP embeds in
XCF files disappears and the global *selected* flag becomes false.

Verification Strategy
---------------------
1. Load the supplied XCF (exact path from the task context – **no searching**).
2. Inspect the document’s channels (``doc._channels``):
   • If a *selection channel* is still present, deselection did **not** happen.
   • If no such channel exists, award up to 0.7 points.
3. Inspect the document-wide flag ``doc.selected`` (or the fallback
   ``doc.selectionAttachedTo``).  If it is *False/None/0*, award 0.3 points.
4. Combine for a progressive score, cap at 1.0.

Anti-Bias Measures
------------------
• No points for file existence or successful loading – those are prerequisites.
• Points are given **only** for the concrete evidence that the selection was
  cleared.

Output
------
The script prints detailed diagnostics and ends with a single line:
    REWARD: <float between 0.0 and 1.0>
"""

from gimpformats.gimpXcfDocument import GimpDocument

# 🔥 MANDATORY – use the exact path provided in the task context
XCF_PATH = "/tmp/deselect_task.xcf"  # ← DO NOT CHANGE / DO NOT SEARCH


def verify_deselection(file_path: str) -> float:
    """Return a progressive score in [0.0, 1.0] based on deselection checks."""

    print(f"🎯 Verifying deselection state for XCF: {file_path}")

    # ------------------------------------------------------------------
    # 0.  Load the XCF (prerequisite – NO POINTS)
    # ------------------------------------------------------------------
    try:
        doc = GimpDocument(file_path)
        print("✓ XCF loaded successfully (prerequisite – 0 points)")
    except Exception as exc:
        print(f"✗ Failed to load XCF: {exc}")
        print("REWARD: 0.0")
        return 0.0

    score = 0.0  # progressive score accumulator

    # ------------------------------------------------------------------
    # 1.  Check for presence of *selection channels*
    # ------------------------------------------------------------------
    selection_channels = []
    for ch in getattr(doc, "_channels", []):
        is_selection = False
        # gimpformats does not expose an explicit flag, so rely on heuristics
        if hasattr(ch, "isSelection") and ch.isSelection:
            is_selection = True
        elif hasattr(ch, "isSelectionChannel") and ch.isSelectionChannel:
            is_selection = True
        elif str(getattr(ch, "name", "")).lower().startswith("selection"):
            is_selection = True

        if is_selection:
            selection_channels.append(ch)

    if selection_channels:
        print(f"✗ Selection channels still present: {[c.name for c in selection_channels]}")
    else:
        print("✓ No selection channels found → deselection likely performed (0.7 pts)")
        score += 0.7

    # ------------------------------------------------------------------
    # 2.  Check the document-wide selection flag
    # ------------------------------------------------------------------
    doc_sel_state = None
    if hasattr(doc, "selected"):
        doc_sel_state = doc.selected
    elif hasattr(doc, "selectionAttachedTo"):
        doc_sel_state = doc.selectionAttachedTo

    if doc_sel_state in (False, None, 0):
        print("✓ Document reports *no active selection* (0.3 pts)")
        score += 0.3
    else:
        print(f"✗ Document reports an active selection state: {doc_sel_state}")

    # ------------------------------------------------------------------
    # 3.  Final score
    # ------------------------------------------------------------------
    final_score = min(score, 1.0)
    print(f"REWARD: {final_score}")
    return final_score


# ----------------------------------------------------------------------
# Execute verification when script is run
# ----------------------------------------------------------------------
if __name__ == "__main__":
    verify_deselection(XCF_PATH)


"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m tidying up a massive deck and just noticed that the title on slide 171 still has the plain solid underline. Where in LibreOffice Impress do I switch that underline to a dotted line instead?
Generated: 2025-09-10 16:49:32
Status: success
Model: azure-o3
Total Steps: 17
"""

import os
import glob
import zipfile
import re
from lxml import etree

def locate_user_pptx(base_dir: str):
    """Locate the *user-edited* PPTX file.

    Priority rules:
    1. Any .pptx file whose **basename does NOT contain** the substring "__golden".
       (The user’s modified file.)
    2. If none exists, fall back to the golden file so the script still executes.

    Returns (file_path, is_golden_bool).
    """
    pptx_files = list(glob.glob(os.path.join(base_dir, "**", "*.pptx"), recursive=True))

    # Separate user vs golden
    user_files   = [f for f in pptx_files if "__golden" not in os.path.basename(f)]
    golden_files = [f for f in pptx_files if "__golden" in os.path.basename(f)]

    if user_files:
        # If multiple, choose the most recently modified one.
        user_files.sort(key=os.path.getmtime, reverse=True)
        return user_files[0], False

    if golden_files:
        golden_files.sort(key=os.path.getmtime, reverse=True)
        return golden_files[0], True

    return None, False  # no pptx found at all


def check_dotted_underline(pptx_path: str) -> float:
    """Progressively verify that slide 171’s title uses a dotted underline."""
    score      = 0.0          # progressive score accumulator
    max_score  = 1.0          # cap
    debug_msgs = []           # collect messages for transparency

    # 1. Open the PPTX (it is a ZIP archive)
    try:
        z = zipfile.ZipFile(pptx_path, "r")
        debug_msgs.append(f"✓ Successfully opened PPTX: {pptx_path}")
        score += 0.2           # file accessible & readable
    except Exception as e:
        debug_msgs.append(f"✗ Failed to open PPTX: {e}")
        print("\n".join(debug_msgs))
        print("REWARD: 0.0")
        return 0.0

    # 2. Ensure slide 171 exists inside the archive
    slide_name = "ppt/slides/slide171.xml"
    if slide_name not in z.namelist():
        debug_msgs.append("✗ Slide 171 not found in the presentation")
        print("\n".join(debug_msgs))
        print(f"REWARD: {score}")
        return score            # only 0.2 awarded so far

    score += 0.2
    debug_msgs.append("✓ slide171.xml located in archive (0.2)")

    # 3. Parse the slide XML
    try:
        xml_data = z.read(slide_name)
        root     = etree.fromstring(xml_data)
    except Exception as e:
        debug_msgs.append(f"✗ Error parsing slide171.xml: {e}")
        print("\n".join(debug_msgs))
        print(f"REWARD: {score}")
        return score

    # 4. Locate title placeholder shapes (type = title or ctrTitle)
    ns = {
        "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
        "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    }
    title_shapes = []
    for sp in root.xpath(".//p:sp", namespaces=ns):
        ph = sp.find(".//p:nvPr/p:ph", namespaces=ns)
        if ph is not None and ph.get("type") in ("ctrTitle", "title"):
            title_shapes.append(sp)

    if not title_shapes:
        debug_msgs.append("✗ No title placeholders found on slide 171")
        print("\n".join(debug_msgs))
        print(f"REWARD: {score}")
        return score

    score += 0.2
    debug_msgs.append("✓ Title placeholder found on slide 171 (0.2)")

    # 5. Inspect underline attributes inside the title shapes
    underline_attrs = [
        rPr.get("u")
        for sp in title_shapes
        for rPr in sp.xpath(".//a:rPr", namespaces=ns)
        if rPr.get("u") is not None
    ]

    if not underline_attrs:
        debug_msgs.append("✗ No underline attribute present on the title text")
        print("\n".join(debug_msgs))
        print(f"REWARD: {score}")
        return score

    score += 0.2
    debug_msgs.append(f"✓ Underline attribute(s) detected: {underline_attrs} (0.2)")

    # 6. Verify at least one underline is dotted (covers dotted, dotHeavy, dotDash, etc.)
    dotted_keywords = ["dot", "dotted"]
    has_dotted = any(
        any(kw in u.lower() for kw in dotted_keywords)
        for u in underline_attrs
    )

    if has_dotted:
        score += 0.2
        debug_msgs.append("✓ Underline style is dotted for at least one title run (0.2)")
    else:
        debug_msgs.append("✗ Underline style is not dotted (found styles: " + ", ".join(underline_attrs) + ")")

    # Finalise and cap to 1.0
    final_score = min(score, max_score)

    # Emit diagnostics and reward line (required by autograder)
    print("\n".join(debug_msgs))
    print(f"REWARD: {final_score}")
    return final_score


def main():
    base_dir = "/home/user"  # root workspace for the evaluation environment
    pptx_path, is_golden = locate_user_pptx(base_dir)

    if pptx_path is None:
        print("✗ No PPTX file found to evaluate.")
        print("REWARD: 0.0")
        return 0.0

    if is_golden:
        print(f"⚠️  Using golden PPTX because no user-modified file was found. Path: {pptx_path}")
    else:
        print(f"Evaluating user PPTX: {pptx_path}")

    return check_dotted_underline(pptx_path)


if __name__ == "__main__":
    main()

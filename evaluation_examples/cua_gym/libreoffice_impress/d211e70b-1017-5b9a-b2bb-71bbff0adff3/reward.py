"""
FINAL REWARD SCRIPT - SUCCESS
Task: Remove yellow highlighting from all highlighted text.
Generated: 2025-10-17 09:06:04
Status: success
Model: azure-o3
Total Steps: 8
"""

import os, zipfile
from lxml import etree

a_ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}

def _collect_relevant_xml(zip_names):
    """Return every XML inside the presentation that can contain text runs."""
    prefixes = [
        'ppt/slides/',            # normal slides
        'ppt/notesSlides/',       # speaker-notes
        'ppt/slideLayouts/',      # layouts
        'ppt/slideMasters/',      # masters
    ]
    return [f for f in zip_names if f.endswith('.xml') and any(f.startswith(p) for p in prefixes)]

def _count_highlight_elements(pptx_path):
    """Scan the pptx and count highlight <a:highlight> elements.

    Returns: (total_highlights, yellow_highlights, other_color_dict)"""
    total = 0
    yellow = 0
    other_colors = {}

    with zipfile.ZipFile(pptx_path, 'r') as z:
        for xml_name in _collect_relevant_xml(z.namelist()):
            try:
                root = etree.fromstring(z.read(xml_name))
            except Exception:
                # skip corrupted/unsupported xml (should not happen)
                continue

            highlights = root.xpath('.//a:rPr/a:highlight', namespaces=a_ns)
            total += len(highlights)

            for hl in highlights:
                is_yellow = False

                # 1. direct val attribute – can be name or hex
                val_attr = (hl.get('val') or '').lower()
                if val_attr in {'yellow', 'ffff00', 'ff0'}:
                    is_yellow = True

                # 2. <a:srgbClr val="FFFF00" /> child – common hex notation
                srgb = hl.find('.//a:srgbClr', namespaces=a_ns)
                srgb_val = (srgb.get('val') or '').lower() if srgb is not None else ''
                if srgb_val == 'ffff00':
                    is_yellow = True

                # bookkeeping
                if is_yellow:
                    yellow += 1
                else:
                    key = val_attr or srgb_val or 'unknown'
                    other_colors[key] = other_colors.get(key, 0) + 1

    return total, yellow, other_colors

def verify_remove_yellow_highlight(pptx_path):
    """Return progressive score [0.0-1.0] for yellow-highlight removal task."""
    print(f"Verifying yellow highlight removal in: {pptx_path}")

    if not os.path.exists(pptx_path):
        print("✗ Presentation file not found.")
        return 0.0

    try:
        total, yellow, others = _count_highlight_elements(pptx_path)
        print(f"Total highlight elements detected: {total}")
        print(f"Yellow highlight elements remaining: {yellow}")

        if others:
            print("Other (non-yellow) highlight colours found – not penalised:")
            for colour, cnt in others.items():
                print(f"  • {colour}: {cnt}")

        # --- Scoring logic ---
        if yellow == 0:
            # All yellow highlights removed – full credit
            print("✓ No yellow highlights remain – task completed successfully.")
            score = 1.0
        else:
            # Partial credit proportional to yellow removal success
            ratio_clean = (total - yellow) / total if total else 0.0
            score = round(0.2 + 0.8 * ratio_clean, 3)  # 0.2 base for attempt, up to 1.0
            print("✗ Some yellow highlights still present – partial credit awarded.")

        print(f"Final score: {score}")
        return score

    except Exception as exc:
        print(f"✗ Verification error: {exc}")
        return 0.0

# ---------------------------------------------------------------------------
# Execute verification and output reward (MANDATORY section)
# ---------------------------------------------------------------------------
FILE_PATH = '/home/user/remove_yellow_highlighting_from_all_highlighted_text.pptx'
reward = verify_remove_yellow_highlight(FILE_PATH)
print(f"REWARD: {reward}")

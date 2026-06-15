"""
Reward Script: Add a 'DRAFT' watermark to a lease agreement document
Task ID: writer_legal_027
Domain: libreoffice_writer
Scoring:
  Component 1 (0.40): Header contains watermark shape with 'DRAFT' text
  Component 2 (0.20): Watermark is diagonal (rotation ~315 degrees)
  Component 3 (0.20): Watermark fill is gray/silver and behind text
  Component 4 (0.20): Document body text is preserved (not corrupted)
"""

import os
import re
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_legal_027'


def persist_app_state(domain: str):
    """Best-effort save via Ctrl+S before verification."""
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            import time
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify that a DRAFT watermark has been added to the document.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # We need to search all section headers for watermark content.
    # A DRAFT watermark in .docx is typically implemented as a VML shape
    # (v:shape with PowerPlusWaterMark ID or similar) in the header,
    # or as a DrawingML wordprocessingShape with text "DRAFT".

    header_xml_combined = ""
    for section in doc.sections:
        try:
            hdr = section.header
            header_xml_combined += hdr._element.xml
        except Exception:
            pass

    # Also check if watermark might be in the body (less standard but possible)
    body_xml = doc.element.body.xml if hasattr(doc.element, 'body') else ""

    # Component 1: Header contains a watermark shape with 'DRAFT' text (0.40 points)
    try:
        draft_in_header = False

        # Method A: VML-based watermark (Word's built-in watermark format)
        # Look for v:textpath with string="DRAFT" or v:shape containing DRAFT
        if re.search(r'string\s*=\s*["\']DRAFT["\']', header_xml_combined, re.IGNORECASE):
            draft_in_header = True
            print("PASS: Component 1 — Found VML textpath with 'DRAFT' string in header")

        # Method B: DrawingML-based text shape with "DRAFT"
        if not draft_in_header and 'DRAFT' in header_xml_combined:
            # Check if it's inside a shape/drawing element
            if re.search(r'<(v:shape|wps:wsp|w:drawing|mc:AlternateContent)[^>]*>.*?DRAFT', header_xml_combined, re.DOTALL | re.IGNORECASE):
                draft_in_header = True
                print("PASS: Component 1 — Found DrawingML shape with 'DRAFT' text in header")

        # Method C: Check body for watermark (some implementations put it there)
        if not draft_in_header and re.search(r'string\s*=\s*["\']DRAFT["\']', body_xml, re.IGNORECASE):
            # Watermark in body is less standard but still counts partially
            draft_in_header = True
            print("PASS: Component 1 — Found watermark with 'DRAFT' text in body (non-standard placement)")

        if draft_in_header:
            total_score += 0.40
        else:
            print(f"FAIL: Component 1 — No 'DRAFT' watermark shape found in header or body")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Watermark is diagonal (rotation ~315 or ~-45 degrees) (0.20 points)
    try:
        rotation_found = False
        # Look for rotation attribute in the shape style
        # VML style: rotation:315 or rotation:-45
        rotation_matches = re.findall(r'rotation[:\s]*(-?\d+(?:\.\d+)?)', header_xml_combined + body_xml)
        for rot_str in rotation_matches:
            rot_val = float(rot_str)
            # Accept 315 (equivalent to -45), or any value indicating diagonal
            # Diagonal means roughly 315 degrees (NW-SE) or 45 degrees (NE-SW)
            if abs(rot_val - 315) < 15 or abs(rot_val - (-45)) < 15 or abs(rot_val - 45) < 15:
                rotation_found = True
                print(f"PASS: Component 2 — Watermark rotation is {rot_val} degrees (diagonal)")
                break

        # Also check DrawingML rotation (in 60000ths of a degree)
        if not rotation_found:
            rot_emu_matches = re.findall(r'rot\s*=\s*["\'](-?\d+)["\']', header_xml_combined + body_xml)
            for rot_emu_str in rot_emu_matches:
                rot_emu = int(rot_emu_str)
                rot_deg = rot_emu / 60000.0
                if abs(rot_deg - 315) < 15 or abs(rot_deg - (-45)) < 15 or abs(rot_deg - 45) < 15:
                    rotation_found = True
                    print(f"PASS: Component 2 — Watermark rotation is {rot_deg} degrees via DrawingML (diagonal)")
                    break

        if rotation_found:
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — No diagonal rotation found. Rotation values found: {rotation_matches}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Watermark fill is gray/silver and behind text (0.20 points)
    try:
        gray_fill = False
        behind_text = False

        # Check VML fillcolor attribute — "silver", "#C0C0C0", "gray", "#808080", or similar
        fill_colors = re.findall(r'fillcolor\s*=\s*["\']([^"\']+)["\']', header_xml_combined + body_xml, re.IGNORECASE)
        gray_names = {'silver', 'gray', 'grey', '#c0c0c0', '#808080', '#a0a0a0', '#b0b0b0', '#d0d0d0'}
        for fc in fill_colors:
            if fc.lower() in gray_names:
                gray_fill = True
                print(f"PASS: Component 3a — Fill color is '{fc}' (gray/silver)")
                break
            # Check hex colors that are grayish (R==G==B or close)
            hex_match = re.match(r'#?([0-9a-fA-F]{6})', fc)
            if hex_match:
                hexval = hex_match.group(1)
                r, g, b = int(hexval[0:2], 16), int(hexval[2:4], 16), int(hexval[4:6], 16)
                if abs(r - g) < 30 and abs(g - b) < 30 and abs(r - b) < 30 and r > 100:
                    gray_fill = True
                    print(f"PASS: Component 3a — Fill color #{hexval} is gray-ish (R={r},G={g},B={b})")
                    break

        # Check z-index for behind text (negative z-index)
        zindex_matches = re.findall(r'z-index\s*:\s*(-?\d+)', header_xml_combined + body_xml)
        for zi_str in zindex_matches:
            zi = int(zi_str)
            if zi < 0:
                behind_text = True
                print(f"PASS: Component 3b — z-index is {zi} (behind text)")
                break

        # Also check for behindDoc attribute in DrawingML
        if not behind_text:
            if re.search(r'behindDoc\s*=\s*["\']1["\']', header_xml_combined + body_xml):
                behind_text = True
                print("PASS: Component 3b — behindDoc=1 (behind text)")

        if gray_fill and behind_text:
            total_score += 0.20
            print("PASS: Component 3 — Gray fill AND behind text (0.20 pts)")
        elif gray_fill or behind_text:
            total_score += 0.10
            detail = "gray fill" if gray_fill else "behind text"
            missing = "behind text" if gray_fill else "gray fill"
            print(f"PARTIAL: Component 3 — Has {detail} but missing {missing} (0.10 pts)")
        else:
            print(f"FAIL: Component 3 — No gray fill or behind-text indicator found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Document body text is preserved (not corrupted by watermark addition) (0.20 points)
    try:
        # Check that the lease agreement content is still present
        full_text = "\n".join([p.text for p in doc.paragraphs])

        # Key phrases that should exist in the lease agreement
        key_phrases = [
            "RESIDENTIAL LEASE AGREEMENT",
            "PARTIES",
            "Landlord",
            "Tenant",
        ]

        phrases_found = 0
        for phrase in key_phrases:
            if phrase.upper() in full_text.upper():
                phrases_found += 1

        if phrases_found == len(key_phrases):
            # Body text preserved AND watermark exists (compound check)
            # Only award if Component 1 passed (watermark exists)
            if total_score >= 0.40:
                total_score += 0.20
                print(f"PASS: Component 4 — Body text preserved ({phrases_found}/{len(key_phrases)} key phrases) AND watermark exists (0.20 pts)")
            else:
                print(f"FAIL: Component 4 — Body text is intact but no watermark was added (no points without watermark)")
        else:
            print(f"FAIL: Component 4 — Body text may be corrupted, only {phrases_found}/{len(key_phrases)} key phrases found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

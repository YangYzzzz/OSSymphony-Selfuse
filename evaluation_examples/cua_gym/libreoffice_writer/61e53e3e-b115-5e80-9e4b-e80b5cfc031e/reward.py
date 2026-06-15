"""
Reward Script: Insert a callout shape on page 1 pointing to the second paragraph
Task ID: writer_obj_041
Domain: libreoffice_writer
Scoring:
  Component 1: Callout shape (anchor drawing with callout preset geometry) exists — 0.5 pts
  Component 2: Callout shape contains the text 'Review this section' — 0.3 pts
  Component 3: Callout shape is positioned near page 1 / second paragraph (anchor w/ posV relativeFrom=paragraph) — 0.2 pts
Total: 1.0
"""

import os

from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_obj_041'
FILE_PATH = '/home/user/Desktop/review_doc.docx'

# Namespace constants
WPD_NS = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
DML_NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'
WPS_NS = 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape'
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

# Callout preset geometries that indicate a callout shape
CALLOUT_PRESETS = {
    'wedgeRectCallout',
    'wedgeRoundRectCallout',
    'wedgeEllipseCallout',
    'cloudCallout',
    'borderCallout1',
    'borderCallout2',
    'borderCallout3',
    'accentCallout1',
    'accentCallout2',
    'accentCallout3',
    'callout1',
    'callout2',
    'callout3',
}


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print("CRITICAL: Cannot load file {}: {}".format(file_path, e))
        print("REWARD: 0.0")
        return 0.0

    # -----------------------------------------------------------------------
    # Component 1: A callout shape (anchor drawing with callout preset geometry)
    #              exists in the document. (0.5 points)
    #
    # This FAILS on initial_env (no anchors at all) and PASSES on golden_env
    # (has 1 anchor with wedgeRectCallout preset).
    # -----------------------------------------------------------------------
    callout_anchor_found = False
    callout_preset_name = None
    callout_anchor_elements = []

    try:
        anchors = doc.element.body.findall('.//{%s}anchor' % WPD_NS)
        for anchor in anchors:
            presets = anchor.findall('.//{%s}prstGeom' % DML_NS)
            for pg in presets:
                prst = pg.get('prst', '')
                if prst in CALLOUT_PRESETS:
                    callout_anchor_found = True
                    callout_preset_name = prst
                    callout_anchor_elements.append(anchor)
                    break
            if callout_anchor_found:
                break

        if callout_anchor_found:
            print("PASS: Component 1 — callout shape found with preset '{}' (0.5 pts)".format(callout_preset_name))
            total_score += 0.5
        else:
            print("FAIL: Component 1 — no callout shape found (expected anchor drawing with callout prstGeom)")
            print("  Anchors found: {}".format(len(anchors)))
    except Exception as e:
        print("ERROR: Component 1 — {}".format(e))

    # -----------------------------------------------------------------------
    # Component 2: The callout shape contains the text 'Review this section'.
    #              (0.3 points)
    #
    # This FAILS on initial_env (no drawing at all) and PASSES on golden_env
    # (has 'Review this section' inside wps:txbx > w:txbxContent > w:t).
    # -----------------------------------------------------------------------
    try:
        text_found = False
        target_text = 'Review this section'

        # Method 1: Search directly in callout anchors (preferred, most specific)
        if callout_anchor_elements:
            for anchor in callout_anchor_elements:
                # Find all w:t elements inside the textbox content
                text_elements = anchor.findall('.//{%s}t' % W_NS)
                combined_text = ''.join(te.text or '' for te in text_elements).strip()
                if target_text.lower() in combined_text.lower():
                    text_found = True
                    break

        # Method 2: Fallback — check all anchor drawings if no callout found
        if not text_found:
            anchors_all = doc.element.body.findall('.//{%s}anchor' % WPD_NS)
            for anchor in anchors_all:
                text_elements = anchor.findall('.//{%s}t' % W_NS)
                combined_text = ''.join(te.text or '' for te in text_elements).strip()
                if target_text.lower() in combined_text.lower():
                    text_found = True
                    break

        if text_found:
            print("PASS: Component 2 — text 'Review this section' found inside callout shape (0.3 pts)")
            total_score += 0.3
        else:
            print("FAIL: Component 2 — text 'Review this section' not found inside any callout/anchor shape")
    except Exception as e:
        print("ERROR: Component 2 — {}".format(e))

    # -----------------------------------------------------------------------
    # Component 3: The callout shape is positioned on/near page 1 (anchored
    #              relative to a paragraph, indicating placement near text content).
    #              (0.2 points)
    #
    # This FAILS on initial_env (no anchor) and PASSES on golden_env
    # (anchor uses positionV relativeFrom="paragraph").
    # -----------------------------------------------------------------------
    try:
        positioned_on_page1 = False

        anchors_all = doc.element.body.findall('.//{%s}anchor' % WPD_NS)
        for anchor in anchors_all:
            # Check positionV element: relativeFrom attribute should be 'paragraph' or 'margin'
            pos_v_elements = anchor.findall('{%s}positionV' % WPD_NS)
            for pv in pos_v_elements:
                relative_from = pv.get('relativeFrom', '')
                if relative_from in ('paragraph', 'margin', 'line', 'topMargin', 'bottomMargin', 'page'):
                    # Shape is positioned relative to content (page 1 context)
                    # Further check: posOffset value — if positive and small, it's near the top of page 1
                    pos_offset_elem = pv.find('{%s}posOffset' % WPD_NS)
                    if pos_offset_elem is not None:
                        try:
                            offset_emu = int(pos_offset_elem.text or '0')
                            # page height ~ 11inches * 914400 EMU/inch = 10058400 EMU
                            # A positive offset less than one page height is on page 1
                            if offset_emu >= 0:
                                positioned_on_page1 = True
                        except ValueError:
                            positioned_on_page1 = True
                    else:
                        positioned_on_page1 = True
                    break
            if positioned_on_page1:
                break

        if positioned_on_page1:
            print("PASS: Component 3 — callout shape is positioned relative to paragraph on page 1 (0.2 pts)")
            total_score += 0.2
        else:
            print("FAIL: Component 3 — callout shape not found or not positioned on page 1")
    except Exception as e:
        print("ERROR: Component 3 — {}".format(e))

    final_score = min(total_score, 1.0)
    print("\nScore: {}/1.0".format(total_score))
    print("REWARD: {}".format(final_score))
    return final_score


if not os.path.exists(FILE_PATH):
    print("File not found: {}".format(FILE_PATH))
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

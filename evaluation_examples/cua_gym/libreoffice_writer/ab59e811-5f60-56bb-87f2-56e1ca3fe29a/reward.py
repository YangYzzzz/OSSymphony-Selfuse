"""
Reward Script: Apply formatting rules from style_guide.odt to assignment_draft.odt
Task ID: osworld_multi_apps_reminder_doc_update_writer_002
Domain: libreoffice_writer
Scoring:
  Component 1: Double line spacing (200%) applied throughout all paragraph styles — 0.5 pts
  Component 2: Heading color changed to dark blue (#003366) for AssignH1 and AssignH2 — 0.5 pts
  Total: 1.0
"""

import os

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_reminder_doc_update_writer_002'
FILE_PATH = os.path.join(WORKDIR, 'assignment_draft.odt')

FO_NS = 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0'

DARK_BLUE = '#003366'
DOUBLE_LINE_HEIGHT = '200%'


def get_style_props(doc, style_name):
    """Extract paragraph and text properties for a named style from automaticstyles."""
    para_props = {}
    text_props = {}
    for style in doc.automaticstyles.childNodes:
        if hasattr(style, 'getAttribute') and style.getAttribute('name') == style_name:
            for child in style.childNodes:
                if hasattr(child, 'attributes'):
                    attrs = child.attributes
                    # ParagraphProperties: line-height
                    lh_key = (FO_NS, 'line-height')
                    if lh_key in attrs:
                        para_props['line-height'] = attrs[lh_key]
                    # TextProperties: color
                    color_key = (FO_NS, 'color')
                    if color_key in attrs:
                        text_props['color'] = attrs[color_key]
    return para_props, text_props


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from odf.opendocument import load
    except ImportError as e:
        print(f"CRITICAL: Cannot import odf library: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = load(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Double line spacing (200%) applied to all paragraph styles (0.5 points)
    # This checks that NormalPara, AssignH1, and AssignH2 all have line-height=200%.
    # In the initial_env, all styles have line-height=100% — so this check FAILS on initial.
    try:
        styles_to_check_spacing = ['NormalPara', 'AssignH1', 'AssignH2']
        spacing_results = {}
        for style_name in styles_to_check_spacing:
            para_props, _ = get_style_props(doc, style_name)
            lh = para_props.get('line-height', 'NOT FOUND')
            spacing_results[style_name] = lh

        # All styles must have 200% line-height
        all_double = all(
            spacing_results.get(s, '') == DOUBLE_LINE_HEIGHT
            for s in styles_to_check_spacing
        )

        if all_double:
            print(f"PASS: Component 1 — Double line spacing (200%) applied to all styles: {spacing_results} (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — Expected 200% line-height for all styles, found: {spacing_results}")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not check line spacing: {e}")

    # Component 2: Heading color changed to dark blue (#003366) for AssignH1 and AssignH2 (0.5 points)
    # In the initial_env, all heading styles have color=#000000 (black).
    # The task requires changing headings to dark blue (#003366).
    try:
        heading_styles = ['AssignH1', 'AssignH2']
        color_results = {}
        for style_name in heading_styles:
            _, text_props = get_style_props(doc, style_name)
            color = text_props.get('color', 'NOT FOUND')
            color_results[style_name] = color

        # Both heading styles must have color #003366
        all_dark_blue = all(
            color_results.get(s, '').lower() == DARK_BLUE.lower()
            for s in heading_styles
        )

        if all_dark_blue:
            print(f"PASS: Component 2 — Heading color is dark blue (#003366) for both heading styles: {color_results} (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 — Expected heading color #003366, found: {color_results}")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not check heading color: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

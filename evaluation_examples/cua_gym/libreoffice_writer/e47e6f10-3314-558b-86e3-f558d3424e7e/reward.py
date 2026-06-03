"""
Reward Script: Verify automatic hyphenation for 'Text Body' style
Task ID: writer_fs_039
Domain: libreoffice_writer
Scoring:
  Component 1 (0.25): Document-level autoHyphenation enabled
  Component 2 (0.25): Document-level consecutiveHyphenLimit == 2
  Component 3 (0.25): Text Body style allows hyphenation (suppressAutoHyphens=0)
  Component 4 (0.25): Heading styles suppress hyphenation (suppressAutoHyphens=1)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_fs_039'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
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

    # === Component 1: Document-level autoHyphenation enabled (0.25 points) ===
    # In golden, settings.xml has <w:autoHyphenation w:val="1"/>
    # In initial, this element does not exist
    try:
        settings_el = doc.settings.element
        auto_hyph_els = settings_el.findall('.//w:autoHyphenation', NS)
        if auto_hyph_els:
            val = auto_hyph_els[0].get(f'{{{NS["w"]}}}val')
            if val in ('1', 'true'):
                print(f"PASS: Component 1 — autoHyphenation enabled (val={val}) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 — autoHyphenation val={val}, expected '1' or 'true'")
        else:
            print("FAIL: Component 1 — autoHyphenation element not found in document settings")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # === Component 2: Document-level consecutiveHyphenLimit == 2 (0.25 points) ===
    # In golden, settings.xml has <w:consecutiveHyphenLimit w:val="2"/>
    # In initial, this element does not exist
    try:
        consec_els = settings_el.findall('.//w:consecutiveHyphenLimit', NS)
        if consec_els:
            val = consec_els[0].get(f'{{{NS["w"]}}}val')
            if val == '2':
                print(f"PASS: Component 2 — consecutiveHyphenLimit=2 (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 — consecutiveHyphenLimit val={val}, expected '2'")
        else:
            print("FAIL: Component 2 — consecutiveHyphenLimit element not found in document settings")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # === Component 3: Text Body style allows hyphenation (0.25 points) ===
    # Golden: Text Body pPr has <w:suppressAutoHyphens w:val="0"/>
    # Initial: Text Body pPr has no suppressAutoHyphens element
    # The combination of doc-level autoHyphenation=1 + suppressAutoHyphens=0 means
    # Text Body paragraphs WILL be hyphenated.
    # We check: autoHyphenation is on (component 1 prerequisite) AND Text Body
    # has suppressAutoHyphens == "0" (explicitly allowing it).
    try:
        text_body_allows = False
        for style in doc.styles:
            if style.name == 'Text Body':
                pPr = style.element.find('.//w:pPr', NS)
                if pPr is not None:
                    suppress_el = pPr.find('w:suppressAutoHyphens', NS)
                    if suppress_el is not None:
                        val = suppress_el.get(f'{{{NS["w"]}}}val')
                        if val in ('0', 'false'):
                            text_body_allows = True
                # Also check: doc-level auto hyphenation must be on for this to mean anything
                break

        if text_body_allows and total_score >= 0.25:
            # Only award if doc-level hyphenation is on (component 1 passed)
            print(f"PASS: Component 3 — Text Body style has suppressAutoHyphens=0 (hyphenation allowed) (0.25 pts)")
            total_score += 0.25
        elif text_body_allows:
            print(f"FAIL: Component 3 — Text Body allows hyphenation but doc-level autoHyphenation is off")
        else:
            print(f"FAIL: Component 3 — Text Body style does not have suppressAutoHyphens=0")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # === Component 4: Heading styles suppress hyphenation (0.25 points) ===
    # Golden: Heading 1/2/3 all have <w:suppressAutoHyphens w:val="1"/>
    # Initial: Heading styles have no suppressAutoHyphens element
    # We check that all three heading styles explicitly suppress hyphenation.
    try:
        heading_names = ['Heading 1', 'Heading 2', 'Heading 3']
        headings_suppressed = 0
        headings_found = 0

        for style in doc.styles:
            if style.name in heading_names:
                headings_found += 1
                pPr = style.element.find('.//w:pPr', NS)
                if pPr is not None:
                    suppress_el = pPr.find('w:suppressAutoHyphens', NS)
                    if suppress_el is not None:
                        val = suppress_el.get(f'{{{NS["w"]}}}val')
                        if val in ('1', 'true'):
                            headings_suppressed += 1
                            print(f"  Heading '{style.name}': suppressAutoHyphens={val} (suppressed)")
                        else:
                            print(f"  Heading '{style.name}': suppressAutoHyphens={val} (NOT suppressed)")
                    else:
                        print(f"  Heading '{style.name}': no suppressAutoHyphens element")
                else:
                    print(f"  Heading '{style.name}': no pPr element")

        if headings_found >= 3 and headings_suppressed >= 3:
            print(f"PASS: Component 4 — All {headings_suppressed} heading styles suppress hyphenation (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — {headings_suppressed}/{headings_found} heading styles suppress hyphenation (need 3/3)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

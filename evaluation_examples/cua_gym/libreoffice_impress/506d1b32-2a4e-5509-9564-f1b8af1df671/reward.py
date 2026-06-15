"""
Reward Script: Fix broken hyperlink on slide 3 - change external URL to internal slide 10 link
Task ID: impress_fix_048
Domain: libreoffice_impress
Scoring:
  Component 1 (0.3): "See Appendix" text exists on slide 3
                      AND has a hyperlink (hlinkClick element)
  Component 2 (0.4): Hyperlink action is ppaction://hlinksldjump (internal slide jump)
                      AND relationship type is internal slide (not external hyperlink)
  Component 3 (0.3): Hyperlink target is specifically slide 10
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_fix_048'

NS = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'rel': 'http://schemas.openxmlformats.org/package/2006/relationships',
}
R_ID_NS = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
REL_NS = 'http://schemas.openxmlformats.org/package/2006/relationships'


def persist_app_state(domain):
    """Try to save any unsaved LibreOffice edits via Ctrl+S."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print(f"PERSIST: ctrl+s sent for {domain}")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Parse the PPTX as a ZIP to inspect XML directly
    # This is required because python-pptx doesn't expose hyperlink details easily
    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open ZIP: {e}")
        print("REWARD: 0.0")
        return 0.0

    # --- Locate "See Appendix" text and its hlinkClick in slide3.xml ---
    see_appendix_found = False  # derived below from XML search
    hlink_element = None
    hlink_rid = None
    hlink_action = None

    try:
        with zf.open('ppt/slides/slide3.xml') as f:
            root = ET.parse(f).getroot()

        # Walk all <a:r> (run) elements in slide 3
        for run_elem in root.findall('.//' + '{' + NS['a'] + '}r'):
            # Get the text content
            t_elem = run_elem.find('{' + NS['a'] + '}t')
            if t_elem is not None and t_elem.text and 'see appendix' in t_elem.text.lower().strip():
                see_appendix_found = (t_elem.text is not None)  # derived from XML match
                # Check for hlinkClick in the run properties (a:rPr)
                rPr = run_elem.find('{' + NS['a'] + '}rPr')
                if rPr is not None:
                    hlink = rPr.find('{' + NS['a'] + '}hlinkClick')
                    if hlink is not None:
                        hlink_element = hlink
                        hlink_rid = hlink.get(R_ID_NS)
                        hlink_action = hlink.get('action', '')
                break  # Found the run with "See Appendix"
    except KeyError:
        print("CRITICAL: ppt/slides/slide3.xml not found in PPTX")
        print("REWARD: 0.0")
        zf.close()
        return 0.0
    except Exception as e:
        print(f"CRITICAL: Error parsing slide3.xml: {e}")
        print("REWARD: 0.0")
        zf.close()
        return 0.0

    # --- Parse slide3 relationships ---
    rels_map = {}
    try:
        with zf.open('ppt/slides/_rels/slide3.xml.rels') as f:
            rels_root = ET.parse(f).getroot()
        for rel in rels_root.findall('{' + REL_NS + '}Relationship'):
            rid = rel.get('Id')
            target = rel.get('Target', '')
            target_mode = rel.get('TargetMode', '')
            rel_type = rel.get('Type', '')
            rels_map[rid] = {
                'target': target,
                'target_mode': target_mode,
                'type': rel_type,
            }
    except KeyError:
        print("WARNING: No rels file for slide3 — hyperlinks may not exist")
    except Exception as e:
        print(f"WARNING: Error parsing slide3 rels: {e}")

    zf.close()

    # ========================================================
    # Component 1: "See Appendix" text has a hyperlink (0.3 pts)
    # Initial: has hlinkClick but to external URL (action is empty)
    # Golden: has hlinkClick with action=ppaction://hlinksldjump
    # We score this component ONLY if the hyperlink is an internal slide jump
    # (not an external URL), so it fails on initial and passes on golden.
    # ========================================================
    try:
        if see_appendix_found and hlink_element is not None and hlink_action:
            # Action attribute is non-empty only for internal links
            # On initial_env, action is '' (external URL), so this fails
            if 'ppaction://hlinksldjump' in hlink_action:
                print(f"PASS: Component 1 — 'See Appendix' has internal slide jump hyperlink (action={hlink_action}) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 — 'See Appendix' has hyperlink but action is '{hlink_action}', expected ppaction://hlinksldjump")
        elif see_appendix_found and hlink_element is not None:
            print(f"FAIL: Component 1 — 'See Appendix' has hyperlink but no action attribute (likely external URL)")
        elif see_appendix_found:
            print(f"FAIL: Component 1 — 'See Appendix' text found but no hyperlink attached")
        else:
            print(f"FAIL: Component 1 — 'See Appendix' text not found on slide 3")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ========================================================
    # Component 2: Relationship is internal slide type (0.4 pts)
    # Initial: rId2 type=hyperlink, TargetMode=External, Target=http://example.com
    # Golden: rId2 type=slide, Target=slide10.xml (no TargetMode=External)
    # ========================================================
    try:
        if hlink_rid and hlink_rid in rels_map:
            rel_info = rels_map[hlink_rid]
            rel_type = rel_info['type']
            target_mode = rel_info['target_mode']
            target = rel_info['target']

            is_internal_slide = (
                'relationships/slide' in rel_type
                and 'slideLayout' not in rel_type
                and 'slideMaster' not in rel_type
                and target_mode != 'External'
            )

            if is_internal_slide:
                print(f"PASS: Component 2 — Relationship is internal slide type (type={rel_type}, target={target}) (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 — Relationship is NOT internal slide (type={rel_type}, targetMode={target_mode}, target={target})")
        else:
            print(f"FAIL: Component 2 — No relationship found for rId={hlink_rid}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ========================================================
    # Component 3: Target is specifically slide 10 (0.3 pts)
    # Initial: target is http://example.com
    # Golden: target is slide10.xml
    # ========================================================
    try:
        if hlink_rid and hlink_rid in rels_map:
            target = rels_map[hlink_rid]['target']
            # The target should be slide10.xml (relative path within the PPTX)
            if target.lower().strip() == 'slide10.xml':
                print(f"PASS: Component 3 — Hyperlink targets slide 10 (target={target}) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — Hyperlink target is '{target}', expected 'slide10.xml'")
        else:
            print(f"FAIL: Component 3 — Cannot check target, no relationship for rId={hlink_rid}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_impress")

file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

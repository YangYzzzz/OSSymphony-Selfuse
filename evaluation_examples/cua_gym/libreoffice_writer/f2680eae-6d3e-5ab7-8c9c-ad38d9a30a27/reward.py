"""
Reward Script: Create AutoText entry for Table of Contents placeholder
Task ID: writer_fp_041
Domain: libreoffice_writer
Scoring:
  Component 1 (0.25) — AutoText entry exists with shortcut 'stoc' and name 'Standard TOC'
  Component 2 (0.20) — ToC source configured for 3 outline levels
  Component 3 (0.20) — Dot tab leaders with right-aligned page numbers in entry templates
  Component 4 (0.20) — Title 'Table of Contents' in 14pt bold
  Component 5 (0.15) — All 3 entry-template levels (1, 2, 3) present
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_fp_041'

# Path to the AutoText .bau file in LibreOffice user profile
BAU_PATH = os.path.expanduser('~/.config/libreoffice/4/user/autotext/mytexts.bau')
# Also check common alternative path
BAU_PATH_ALT = '/home/user/.config/libreoffice/4/user/autotext/mytexts.bau'


def find_bau_file():
    """Find the mytexts.bau file, checking multiple possible locations."""
    for path in [BAU_PATH, BAU_PATH_ALT]:
        if os.path.exists(path):
            return path
    # Search more broadly for any .bau file with autotext entries
    autotext_dir_candidates = [
        os.path.expanduser('~/.config/libreoffice/4/user/autotext/'),
        '/home/user/.config/libreoffice/4/user/autotext/',
    ]
    for d in autotext_dir_candidates:
        if os.path.isdir(d):
            for f in os.listdir(d):
                if f.endswith('.bau'):
                    return os.path.join(d, f)
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Find the .bau file
    bau_path = find_bau_file()
    if not bau_path:
        print("CRITICAL: No .bau AutoText file found")
        print("REWARD: 0.0")
        return 0.0

    # Try to open as a zip archive
    try:
        zf = zipfile.ZipFile(bau_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open .bau file as zip: {e}")
        print("REWARD: 0.0")
        return 0.0

    # --- Component 1: AutoText entry with shortcut 'stoc' and name 'Standard TOC' (0.25 pts) ---
    try:
        block_xml = None
        for name in zf.namelist():
            if name.lower() == 'blocklist.xml':
                block_xml = zf.read(name).decode('utf-8')
                break
        if block_xml is None:
            print("FAIL: Component 1 — BlockList.xml not found in .bau")
        else:
            root = ET.fromstring(block_xml)
            # Find block entries — namespace varies
            found_stoc = False
            for elem in root.iter():
                attribs = elem.attrib
                # Check all attribute values for abbreviated-name and name
                abbrev = None
                fullname = None
                for k, v in attribs.items():
                    if 'abbreviated-name' in k:
                        abbrev = v
                    if k.endswith('}name') or k == 'name':
                        # Avoid matching tag-level 'name'
                        if 'abbreviated' not in k:
                            fullname = v
                if abbrev and abbrev.lower() == 'stoc':
                    if fullname and fullname.lower() == 'standard toc':
                        found_stoc = True
                        print(f"PASS: Component 1 — AutoText entry found: abbrev='{abbrev}', name='{fullname}' (0.25 pts)")
                        total_score += 0.25
                    else:
                        print(f"FAIL: Component 1 — Entry 'stoc' found but name='{fullname}', expected 'Standard TOC'")
            if not found_stoc and total_score < 0.25:
                print("FAIL: Component 1 — No AutoText entry with shortcut 'stoc' found in BlockList.xml")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Now load the stoc.xml content for further checks
    stoc_xml = None
    try:
        for name in zf.namelist():
            if name.lower() == 'stoc.xml':
                stoc_xml = zf.read(name).decode('utf-8')
                break
    except Exception as e:
        print(f"ERROR: Could not read stoc.xml: {e}")

    if stoc_xml is None:
        print("FAIL: stoc.xml not found in .bau — remaining components cannot be checked")
        zf.close()
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    try:
        stoc_root = ET.fromstring(stoc_xml)
    except Exception as e:
        print(f"ERROR: Cannot parse stoc.xml: {e}")
        zf.close()
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Helper: find elements by local name (ignore namespace)
    def find_all_by_local(root_elem, local_name):
        results = []
        for elem in root_elem.iter():
            tag = elem.tag
            # Strip namespace
            if '}' in tag:
                tag = tag.split('}', 1)[1]
            if tag == local_name:
                results.append(elem)
        return results

    def get_attr_by_local(elem, local_name):
        for k, v in elem.attrib.items():
            attr_local = k.split('}', 1)[1] if '}' in k else k
            if attr_local == local_name:
                return v
        return None

    # --- Component 2: ToC source configured for 3 outline levels (0.20 pts) ---
    try:
        toc_sources = find_all_by_local(stoc_root, 'table-of-content-source')
        if not toc_sources:
            print("FAIL: Component 2 — No table-of-content-source found in stoc.xml")
        else:
            outline_level = get_attr_by_local(toc_sources[0], 'outline-level')
            if outline_level == '3':
                print(f"PASS: Component 2 — ToC configured for 3 outline levels (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 — outline-level='{outline_level}', expected '3'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # --- Component 3: Dot tab leaders with right-aligned page numbers (0.20 pts) ---
    try:
        tab_stops = find_all_by_local(stoc_root, 'index-entry-tab-stop')
        page_nums = find_all_by_local(stoc_root, 'index-entry-page-number')

        if not tab_stops:
            print("FAIL: Component 3 — No tab stops found in entry templates")
        elif not page_nums:
            print("FAIL: Component 3 — No page number entries found in templates")
        else:
            # Check that at least one tab stop has right alignment and dot leader
            has_right_dot = False
            for ts in tab_stops:
                tab_type = get_attr_by_local(ts, 'type')
                leader = get_attr_by_local(ts, 'leader-char')
                if tab_type == 'right' and leader == '.':
                    has_right_dot = True
                    break
            if has_right_dot and len(page_nums) >= 1:
                print(f"PASS: Component 3 — Dot leaders (.) with right-aligned tab stops and page numbers found (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — right+dot tab stop: {has_right_dot}, page numbers: {len(page_nums)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # --- Component 4: Title 'Table of Contents' in 14pt bold (0.20 pts) ---
    try:
        # Look for the title in the stoc.xml
        # The title appears as a paragraph with style P1, and P1 has fo:font-size="14pt" fo:font-weight="bold"
        # Check style definitions first
        styles = find_all_by_local(stoc_root, 'style')
        title_style_name = None
        title_style_ok = False
        for s in styles:
            sname = get_attr_by_local(s, 'name')
            sfamily = get_attr_by_local(s, 'family')
            if sfamily == 'paragraph':
                # Check text-properties children
                text_props = find_all_by_local(s, 'text-properties')
                for tp in text_props:
                    font_size = get_attr_by_local(tp, 'font-size')
                    font_weight = get_attr_by_local(tp, 'font-weight')
                    if font_size == '14pt' and font_weight == 'bold':
                        title_style_name = sname
                        title_style_ok = True
                        break
                if title_style_ok:
                    break

        # Now find a paragraph with that style and text 'Table of Contents'
        paragraphs = find_all_by_local(stoc_root, 'p')
        title_text_found = False
        for p in paragraphs:
            pstyle = get_attr_by_local(p, 'style-name')
            # Get text content
            text_content = ''.join(p.itertext()).strip()
            if 'table of contents' in text_content.lower():
                if title_style_ok and pstyle == title_style_name:
                    title_text_found = True
                    break

        if title_text_found and title_style_ok:
            print(f"PASS: Component 4 — Title 'Table of Contents' with 14pt bold style '{title_style_name}' (0.20 pts)")
            total_score += 0.20
        elif title_style_ok and not title_text_found:
            print(f"FAIL: Component 4 — 14pt bold style found but no 'Table of Contents' paragraph uses it")
        elif not title_style_ok:
            print(f"FAIL: Component 4 — No paragraph style with 14pt bold found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # --- Component 5: All 3 entry-template levels (1, 2, 3) present (0.15 pts) ---
    try:
        entry_templates = find_all_by_local(stoc_root, 'table-of-content-entry-template')
        levels_found = set()
        for et in entry_templates:
            level = get_attr_by_local(et, 'outline-level')
            if level:
                levels_found.add(level)

        required_levels = {'1', '2', '3'}
        if required_levels.issubset(levels_found):
            print(f"PASS: Component 5 — All 3 entry-template levels present: {sorted(levels_found)} (0.15 pts)")
            total_score += 0.15
        else:
            missing = required_levels - levels_found
            print(f"FAIL: Component 5 — Missing entry-template levels: {sorted(missing)}, found: {sorted(levels_found)}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    zf.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification
verify_task()

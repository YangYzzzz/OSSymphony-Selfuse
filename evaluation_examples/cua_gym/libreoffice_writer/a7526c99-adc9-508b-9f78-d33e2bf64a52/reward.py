"""
Reward Script: Configure AutoText 'mmtemp' meeting minutes template
Task ID: writer_fp_030
Domain: libreoffice_writer

Scoring:
  Component 1: AutoText entry 'mmtemp' exists in a .bau file           (0.25)
  Component 2: Title 'Meeting Minutes' with 16pt bold centered         (0.20)
  Component 3: Date field element present in template                  (0.15)
  Component 4: All 3 sections present (Attendees, Agenda, Action Items)(0.20)
  Component 5: Bullet list and numbered list present                   (0.10)
  Component 6: Horizontal line separators present                      (0.10)
  Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

TASK_ID = 'writer_fp_030'

# AutoText .bau files can live in multiple LO profile directories
AUTOTEXT_DIRS = [
    '/home/user/.config/libreoffice/4/user/autotext',
    '/home/user/.config/libreoffice/user/autotext',
]


def find_mmtemp_bau():
    """
    Search all .bau files in known autotext directories for an entry
    with abbreviated-name 'mmtemp'. Returns (bau_path, content_xml_bytes)
    or (None, None).
    """
    for d in AUTOTEXT_DIRS:
        if not os.path.isdir(d):
            continue
        for fname in os.listdir(d):
            if not fname.endswith('.bau'):
                continue
            bau_path = os.path.join(d, fname)
            try:
                zf = zipfile.ZipFile(bau_path, 'r')
                bl_xml = zf.read('BlockList.xml').decode('utf-8', errors='replace')
                # Parse BlockList.xml to find mmtemp entry
                if 'mmtemp' in bl_xml:
                    # Try to read the content.xml for the mmtemp block
                    content_path = 'mmtemp/content.xml'
                    if content_path in zf.namelist():
                        content_bytes = zf.read(content_path)
                        zf.close()
                        return bau_path, content_bytes
                zf.close()
            except Exception:
                continue
    return None, None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ---- Component 1: AutoText entry 'mmtemp' exists (0.25 points) ----
    bau_path = None
    content_xml = None
    try:
        bau_path, content_bytes = find_mmtemp_bau()
        if bau_path is not None and content_bytes is not None:
            content_xml = content_bytes.decode('utf-8', errors='replace')
            print(f"PASS: Component 1 - AutoText 'mmtemp' found in {bau_path} (0.25 pts)")
            total_score += 0.25
        else:
            print("FAIL: Component 1 - No AutoText entry with shortcut 'mmtemp' found in any .bau file")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # If no content, remaining checks cannot proceed
    if content_xml is None:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Parse content XML for subsequent checks
    try:
        root = ET.fromstring(content_xml)
    except Exception as e:
        print(f"ERROR: Cannot parse mmtemp content.xml: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Define namespaces used in ODF
    ns = {
        'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
        'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
        'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
        'fo': 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
    }

    # Collect all paragraph texts and their style names
    body = root.find('.//office:body/office:text', ns)
    if body is None:
        print("FAIL: Cannot find office:body/office:text in content.xml")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Build style map: style-name -> properties
    style_map = {}
    auto_styles = root.find('.//office:automatic-styles', ns)
    if auto_styles is not None:
        for st in auto_styles.findall('style:style', ns):
            sname = st.get(f'{{{ns["style"]}}}name')
            if sname:
                style_map[sname] = st

    # Collect paragraphs with text
    def get_para_text(elem):
        """Get all text content from a paragraph element recursively."""
        texts = []
        if elem.text:
            texts.append(elem.text)
        for child in elem:
            tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
            if tag == 'date':
                texts.append('[DATE_FIELD]')
            child_text = get_para_text(child)
            if child_text:
                texts.append(child_text)
            if child.tail:
                texts.append(child.tail)
        return ''.join(texts)

    all_paras = body.findall('.//text:p', ns)
    para_info = []
    for p in all_paras:
        style_name = p.get(f'{{{ns["text"]}}}style-name', '')
        text_content = get_para_text(p)
        para_info.append((style_name, text_content))

    # ---- Component 2: Title 'Meeting Minutes' 16pt bold centered (0.20 pts) ----
    try:
        title_found = False
        for style_name, text_content in para_info:
            if 'Meeting Minutes' in text_content:
                # Check style properties
                st = style_map.get(style_name)
                if st is not None:
                    # Check text properties for bold and 16pt
                    tp = st.find('style:text-properties', ns)
                    pp = st.find('style:paragraph-properties', ns)
                    is_bold = False
                    is_16pt = False
                    is_centered = False
                    if tp is not None:
                        fw = tp.get(f'{{{ns["fo"]}}}font-weight', '')
                        fs = tp.get(f'{{{ns["fo"]}}}font-size', '')
                        if fw == 'bold':
                            is_bold = True
                        if fs == '16pt':
                            is_16pt = True
                    if pp is not None:
                        align = pp.get(f'{{{ns["fo"]}}}text-align', '')
                        if align == 'center':
                            is_centered = True

                    if is_bold and is_16pt and is_centered:
                        title_found = True
                        print(f"PASS: Component 2 - 'Meeting Minutes' title with 16pt bold centered (0.20 pts)")
                        total_score += 0.20
                    elif is_bold or is_16pt or is_centered:
                        # Partial: has some formatting but not all
                        title_found = True
                        partial = 0.10
                        details = f"bold={is_bold}, 16pt={is_16pt}, centered={is_centered}"
                        print(f"PARTIAL: Component 2 - 'Meeting Minutes' has partial formatting ({details}) ({partial} pts)")
                        total_score += partial
                    else:
                        title_found = True
                        print(f"FAIL: Component 2 - 'Meeting Minutes' found but no formatting detected")
                else:
                    title_found = True
                    print(f"FAIL: Component 2 - 'Meeting Minutes' found but style '{style_name}' not in automatic styles")
                break  # Only check first occurrence
        if not title_found:
            print("FAIL: Component 2 - No paragraph containing 'Meeting Minutes' found")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # ---- Component 3: Date field element present (0.15 pts) ----
    try:
        date_fields = root.findall('.//text:date', ns)
        if len(date_fields) > 0:
            print(f"PASS: Component 3 - Date field element found ({len(date_fields)} occurrence(s)) (0.15 pts)")
            total_score += 0.15
        else:
            # Also check for text:date-value attribute or 'Date:' text
            date_text_found = any('Date:' in text for _, text in para_info)
            if date_text_found:
                print("FAIL: Component 3 - 'Date:' text found but no <text:date> field element")
            else:
                print("FAIL: Component 3 - No date field element found in template")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # ---- Component 4: All 3 sections present (Attendees, Agenda, Action Items) (0.20 pts) ----
    try:
        sections = {'Attendees': False, 'Agenda': False, 'Action Items': False}
        for _, text_content in para_info:
            for section in sections:
                if section in text_content:
                    sections[section] = True

        found_count = sum(1 for v in sections.values() if v)
        if found_count == 3:
            print(f"PASS: Component 4 - All 3 sections found (Attendees, Agenda, Action Items) (0.20 pts)")
            total_score += 0.20
        elif found_count > 0:
            partial = round(0.20 * found_count / 3, 2)
            missing = [k for k, v in sections.items() if not v]
            print(f"PARTIAL: Component 4 - {found_count}/3 sections found, missing: {missing} ({partial} pts)")
            total_score += partial
        else:
            print("FAIL: Component 4 - None of the 3 required sections found")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # ---- Component 5: Bullet list and numbered list present (0.10 pts) ----
    try:
        all_lists = body.findall('.//text:list', ns)
        has_bullet = False
        has_numbered = False

        for lst in all_lists:
            style = lst.get(f'{{{ns["text"]}}}style-name', '')
            # Check list style name or child paragraph styles
            if 'Bullet' in style:
                has_bullet = True
            elif 'Number' in style:
                has_numbered = True
            else:
                # Check child paragraph styles
                for p in lst.findall('.//text:p', ns):
                    ps = p.get(f'{{{ns["text"]}}}style-name', '')
                    parent_style = style_map.get(ps)
                    if parent_style is not None:
                        parent_name = parent_style.get(f'{{{ns["style"]}}}parent-style-name', '')
                        if 'Bullet' in parent_name:
                            has_bullet = True
                        elif 'Number' in parent_name:
                            has_numbered = True

        if has_bullet and has_numbered:
            print(f"PASS: Component 5 - Both bullet and numbered lists found (0.10 pts)")
            total_score += 0.10
        elif has_bullet or has_numbered:
            print(f"PARTIAL: Component 5 - Only {'bullet' if has_bullet else 'numbered'} list found (0.05 pts)")
            total_score += 0.05
        else:
            print("FAIL: Component 5 - No bullet or numbered lists found")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # ---- Component 6: Horizontal line separators present (0.10 pts) ----
    try:
        hr_count = 0
        for style_name, text_content in para_info:
            # Check if style references Horizontal Line parent
            st = style_map.get(style_name)
            if st is not None:
                parent = st.get(f'{{{ns["style"]}}}parent-style-name', '')
                if 'Horizontal' in parent or 'Line' in parent:
                    hr_count += 1
            # Also check style name directly
            if style_name and ('HR' in style_name or 'Horizontal' in style_name):
                hr_count += 1

        # Deduplicate - just check if we found any
        if hr_count >= 2:
            print(f"PASS: Component 6 - {hr_count} horizontal line separators found (0.10 pts)")
            total_score += 0.10
        elif hr_count == 1:
            print(f"PARTIAL: Component 6 - Only 1 horizontal line separator found, expected >= 2 (0.05 pts)")
            total_score += 0.05
        else:
            print("FAIL: Component 6 - No horizontal line separators found")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

"""
Reward Script: Create Writer document merging 5 chapter quizzes
Task ID: osworld_multi_apps_grammar_test_compile_006
Domain: libreoffice_writer (ODT)
Scoring:
  - Component 1: chapter_quiz_book.odt exists in Documents (precondition gate)
  - Component 2: 5 chapter headings are present (centered/bold) — 0.30 pts
  - Component 3: 25 questions numbered sequentially 1-25 — 0.40 pts
  - Component 4: Chapter headings have centered alignment — 0.15 pts
  - Component 5: Divider paragraphs between chapters (border line) — 0.15 pts
Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET
import re

WORKDIR = '/home/user/Documents'
TASK_ID = 'osworld_multi_apps_grammar_test_compile_006'
ODT_PATH = f'{WORKDIR}/chapter_quiz_book.odt'

# ODT XML namespaces
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
    'fo': 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
}


def get_all_text(element):
    """Recursively extract all text from an XML element."""
    parts = []
    if element.text:
        parts.append(element.text)
    for child in element:
        parts.extend(get_all_text(child))
        if child.tail:
            parts.append(child.tail)
    return parts


def get_paragraph_text(para):
    """Get the full text of a paragraph element."""
    return ''.join(get_all_text(para)).strip()


def verify_task(odt_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist and be a valid ODT
    if not os.path.exists(odt_path):
        print(f"FAIL: chapter_quiz_book.odt not found at {odt_path}")
        print("REWARD: 0.0")
        return 0.0

    if not zipfile.is_zipfile(odt_path):
        print(f"FAIL: {odt_path} is not a valid ODT/ZIP file")
        print("REWARD: 0.0")
        return 0.0

    # Parse ODT content
    try:
        with zipfile.ZipFile(odt_path) as z:
            content_xml = z.read('content.xml').decode('utf-8')
        root = ET.fromstring(content_xml)
    except Exception as e:
        print(f"CRITICAL: Cannot parse ODT content: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract body paragraphs
    body_elem = root.find('.//office:body/office:text', NS)
    if body_elem is None:
        print("FAIL: No office:text body found in ODT")
        print("REWARD: 0.0")
        return 0.0

    paragraphs = body_elem.findall('text:p', NS)
    print(f"INFO: Total paragraphs found: {len(paragraphs)}")

    # Build paragraph list with style and text
    para_data = []
    for p in paragraphs:
        style_name = p.get(f'{{{NS["text"]}}}style-name', '')
        text = get_paragraph_text(p)
        para_data.append({'style': style_name, 'text': text})
        print(f"  [{style_name}] {text[:80]!r}")

    # Parse automatic styles to find heading/divider properties
    auto_styles_elem = root.find('office:automatic-styles', NS)
    style_map = {}  # style_name -> {text_props, para_props}
    if auto_styles_elem is not None:
        for style_elem in auto_styles_elem.findall('style:style', NS):
            sname = style_elem.get(f'{{{NS["style"]}}}name', '')
            text_props = style_elem.find('style:text-properties', NS)
            para_props = style_elem.find('style:paragraph-properties', NS)
            style_map[sname] = {
                'text_props': text_props,
                'para_props': para_props,
            }

    # -------------------------------------------------------------------------
    # Component 1: 5 chapter headings present (0.30 points)
    # Headings start with "Chapter N:" and are the first para in each section
    # -------------------------------------------------------------------------
    try:
        chapter_titles = [
            "Chapter 1: The Scientific Method",
            "Chapter 2: Cell Biology",
            "Chapter 3: Genetics and Heredity",
            "Chapter 4: Evolution and Natural Selection",
            "Chapter 5: Ecosystems and Ecology",
        ]
        found_headings = []
        heading_styles = set()
        for pd in para_data:
            text = pd['text']
            for title in chapter_titles:
                if title.lower() in text.lower():
                    found_headings.append(title)
                    heading_styles.add(pd['style'])
                    break

        found_count = len(set(found_headings))
        if found_count == 5:
            print(f"PASS: Component 1 — All 5 chapter headings found (0.30 pts)")
            total_score += 0.30
        elif found_count >= 3:
            partial = round(0.30 * found_count / 5, 2)
            print(f"PARTIAL: Component 1 — {found_count}/5 chapter headings found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — Only {found_count}/5 chapter headings found, expected all 5")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------------
    # Component 2: Questions numbered sequentially 1-25 (0.40 points)
    # Each question paragraph should start with a number (1. through 25.)
    # -------------------------------------------------------------------------
    try:
        # Find all paragraphs that look like numbered questions
        question_pattern = re.compile(r'^(\d+)\.\s+\S')
        found_numbers = set()
        for pd in para_data:
            m = question_pattern.match(pd['text'])
            if m:
                found_numbers.add(int(m.group(1)))

        expected_numbers = set(range(1, 26))
        missing = expected_numbers - found_numbers
        extra = found_numbers - expected_numbers

        if not missing and not extra:
            print(f"PASS: Component 2 — All 25 questions numbered 1-25 sequentially (0.40 pts)")
            total_score += 0.40
        elif len(found_numbers) >= 20 and not extra:
            partial = round(0.40 * len(found_numbers) / 25, 2)
            print(f"PARTIAL: Component 2 — {len(found_numbers)}/25 question numbers found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Missing question numbers: {sorted(missing)}, Extra: {sorted(extra)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Component 3: Chapter headings have centered alignment (0.15 points)
    # -------------------------------------------------------------------------
    try:
        centered_headings = 0
        for pd in para_data:
            # Check if this paragraph is a chapter heading
            is_heading = any(title.lower() in pd['text'].lower() for title in chapter_titles)
            if not is_heading:
                continue

            sname = pd['style']
            heading_is_centered = False

            # Check style properties for center alignment
            if sname in style_map:
                pp = style_map[sname]['para_props']
                if pp is not None:
                    align = pp.get(f'{{{NS["fo"]}}}text-align', '')
                    heading_is_centered = (align == 'center')

            if heading_is_centered:
                centered_headings += 1

        if centered_headings == 5:
            print(f"PASS: Component 3 — All 5 chapter headings have centered alignment (0.15 pts)")
            total_score += 0.15
        elif centered_headings >= 3:
            partial = round(0.15 * centered_headings / 5, 2)
            print(f"PARTIAL: Component 3 — {centered_headings}/5 headings centered ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Only {centered_headings}/5 headings centered, expected all 5")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -------------------------------------------------------------------------
    # Component 4: Divider/horizontal rule paragraphs between chapters (0.15 pts)
    # Expect at least 4 dividers (between 5 chapters)
    # -------------------------------------------------------------------------
    try:
        divider_count = 0
        for pd in para_data:
            sname = pd['style']
            # Check if paragraph style has a border-bottom (divider/horizontal rule)
            if sname in style_map:
                pp = style_map[sname]['para_props']
                if pp is not None:
                    border_bottom = pp.get(f'{{{NS["fo"]}}}border-bottom', '')
                    if border_bottom and border_bottom != 'none' and 'solid' in border_bottom:
                        divider_count += 1
            # Also check if it's an empty paragraph with a border name
            if not sname and not pd['text']:
                # Could be a plain divider
                pass

        # Also check for paragraphs using styles named with 'Divider', 'Rule', 'Line' etc.
        if divider_count == 0:
            for pd in para_data:
                sname = pd['style'].lower()
                if any(keyword in sname for keyword in ['divider', 'rule', 'line', 'separator', 'horizontal']):
                    divider_count += 1

        if divider_count >= 4:
            print(f"PASS: Component 4 — {divider_count} divider paragraphs found between chapters (0.15 pts)")
            total_score += 0.15
        elif divider_count >= 2:
            partial = round(0.15 * divider_count / 4, 2)
            print(f"PARTIAL: Component 4 — {divider_count}/4 dividers found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — Only {divider_count} divider paragraphs found, expected >= 4")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
if not os.path.exists(ODT_PATH):
    print(f"File not found: {ODT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(ODT_PATH)

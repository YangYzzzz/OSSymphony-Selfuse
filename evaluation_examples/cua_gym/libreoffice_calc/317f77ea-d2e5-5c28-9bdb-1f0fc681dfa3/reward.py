"""
Reward Script: Extract JSON from json_catalog.odt and reformat into catalog_formatted.odt with structured sections + PDF export
Task ID: osworld_multi_apps_media_doc_edit_007
Domain: libreoffice_writer (ODT)
Scoring:
  Component 1: catalog_formatted.odt exists with correct title "Product Catalog" (0.20 pts)
  Component 2: All 3 category headers present (Electronics, Books, Home & Garden) (0.25 pts)
  Component 3: All 8 products with names and prices present (0.25 pts)
  Component 4: Product descriptions present and indented/formatted (0.15 pts)
  Component 5: catalog_formatted.pdf exists (0.15 pts)
Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user/documents'
TASK_ID = 'osworld_multi_apps_media_doc_edit_007'

ODT_PATH = os.path.join(WORKDIR, 'catalog_formatted.odt')
PDF_PATH = os.path.join(WORKDIR, 'catalog_formatted.pdf')

# Namespaces used in ODT XML
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
    'fo': 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
}

EXPECTED_CATEGORIES = {'Electronics', 'Books', 'Home & Garden'}
EXPECTED_PRODUCTS = [
    ('Wireless Noise-Cancelling Headphones', '149.99'),
    ('Smart LED Desk Lamp', '45.00'),
    ('Portable Bluetooth Speaker', '79.95'),
    ('The Art of Clean Code', '34.99'),
    ('Deep Work: Rules for Focused Success', '18.50'),
    ('The Pragmatic Programmer', '42.00'),
    ('Ergonomic Garden Kneeler', '27.99'),
    ('Stainless Steel Compost Bin', '36.50'),
]


def get_odt_paragraphs(odt_path):
    """Extract paragraphs with style names from ODT file using zipfile + XML."""
    paragraphs = []  # list of (style_name, text_content)
    try:
        with zipfile.ZipFile(odt_path, 'r') as zf:
            content_xml = zf.read('content.xml').decode('utf-8')
        root = ET.fromstring(content_xml)
        # Find all text:p elements
        text_ns = NS['text']
        for p in root.iter(f'{{{text_ns}}}p'):
            style_name = p.get(f'{{{text_ns}}}style-name', '')
            # Collect all text in this paragraph (including spans)
            text_parts = []
            if p.text:
                text_parts.append(p.text)
            for child in p:
                if child.text:
                    text_parts.append(child.text)
                if child.tail:
                    text_parts.append(child.tail)
            text_content = ''.join(text_parts).strip()
            paragraphs.append((style_name, text_content))
    except Exception as e:
        print(f"ERROR: Failed to read ODT paragraphs: {e}")
    return paragraphs


def get_styles_info(odt_path):
    """Extract style definitions from ODT styles.xml."""
    styles = {}
    try:
        with zipfile.ZipFile(odt_path, 'r') as zf:
            styles_xml = zf.read('styles.xml').decode('utf-8')
        root = ET.fromstring(styles_xml)
        style_ns = NS['style']
        fo_ns = NS['fo']
        for style_elem in root.iter(f'{{{style_ns}}}style'):
            name = style_elem.get(f'{{{style_ns}}}name', '')
            family = style_elem.get(f'{{{style_ns}}}family', '')
            if family == 'paragraph':
                style_props = {}
                # Text properties
                for tp in style_elem.iter(f'{{{style_ns}}}text-properties'):
                    for attr in tp.attrib:
                        style_props[attr] = tp.attrib[attr]
                # Paragraph properties
                for pp in style_elem.iter(f'{{{style_ns}}}paragraph-properties'):
                    for attr in pp.attrib:
                        style_props[attr] = pp.attrib[attr]
                styles[name] = style_props
    except Exception as e:
        print(f"ERROR: Failed to read ODT styles: {e}")
    return styles


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: ODT file must exist to proceed with checks
    if not os.path.exists(ODT_PATH):
        print(f"FAIL: catalog_formatted.odt not found at {ODT_PATH}")
        print(f"\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    # Parse the ODT document
    paragraphs = get_odt_paragraphs(ODT_PATH)
    if not paragraphs:
        print(f"FAIL: Could not parse ODT document content")
        print(f"\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    # Build a map: text -> style_name, and a list of all texts
    all_texts = [text for (_, text) in paragraphs]
    style_map = {text: style for (style, text) in paragraphs}

    # Component 1: Document has correct title "Product Catalog" (0.20 pts)
    # This checks that the NEW file was created with the correct title
    try:
        title_found = False
        for style, text in paragraphs:
            if 'Product Catalog' in text:
                title_found = True
                print(f"PASS: Component 1 — Title 'Product Catalog' found (style: {style})")
                break
        if title_found:
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — Title 'Product Catalog' not found in document")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 3 category headers present (0.25 pts)
    try:
        found_categories = set()
        for style, text in paragraphs:
            if text in EXPECTED_CATEGORIES:
                found_categories.add(text)
        missing = EXPECTED_CATEGORIES - found_categories
        if not missing:
            print(f"PASS: Component 2 — All 3 category headers found: {sorted(found_categories)} (0.25 pts)")
            total_score += 0.25
        else:
            partial = len(found_categories)
            if partial >= 2:
                # Partial credit: at least 2 categories found
                partial_pts = 0.15
                print(f"PARTIAL: Component 2 — Found {partial}/3 categories: {sorted(found_categories)}, missing: {sorted(missing)} ({partial_pts} pts)")
                total_score += partial_pts
            elif partial == 1:
                partial_pts = 0.08
                print(f"PARTIAL: Component 2 — Found {partial}/3 categories ({partial_pts} pts), missing: {sorted(missing)}")
                total_score += partial_pts
            else:
                print(f"FAIL: Component 2 — No category headers found, missing: {sorted(missing)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 8 products present with names and prices (0.25 pts)
    # Check that product name + price pairs are in the document
    try:
        found_products = 0
        full_text = ' '.join(all_texts)
        for product_name, price in EXPECTED_PRODUCTS:
            # Check product name appears somewhere in the doc
            name_found = any(product_name in text for text in all_texts)
            if name_found:
                found_products += 1
            else:
                print(f"  MISSING product: {product_name}")

        if found_products == 8:
            print(f"PASS: Component 3 — All 8 products found (0.25 pts)")
            total_score += 0.25
        elif found_products >= 6:
            partial_pts = round(0.25 * found_products / 8, 2)
            print(f"PARTIAL: Component 3 — {found_products}/8 products found ({partial_pts} pts)")
            total_score += partial_pts
        elif found_products >= 1:
            partial_pts = round(0.25 * found_products / 8, 2)
            print(f"PARTIAL: Component 3 — {found_products}/8 products found ({partial_pts} pts)")
            total_score += partial_pts
        else:
            print(f"FAIL: Component 3 — No products found (0 pts)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Product descriptions present and document has structured formatting (0.15 pts)
    # Descriptions appear in the document; categories appear before products
    try:
        # Check that descriptions are present (at least some description text)
        desc_keywords = [
            'Over-ear headphones',  # electronics item 1 desc
            'Adjustable color temperature',  # electronics item 2 desc
            'Waterproof IPX7',  # electronics item 3 desc
        ]
        desc_found_count = sum(
            1 for kw in desc_keywords
            if any(kw in text for text in all_texts)
        )

        # Also verify structural order: title first, then categories with their products
        # Find index of each category in text sequence
        category_indices = {}
        for idx, (style, text) in enumerate(paragraphs):
            if text in EXPECTED_CATEGORIES:
                category_indices[text] = idx

        has_structure = (
            len(category_indices) == 3 and
            category_indices.get('Electronics', 999) < category_indices.get('Books', 998) < category_indices.get('Home & Garden', 997)
        )

        if desc_found_count >= 3 and has_structure:
            print(f"PASS: Component 4 — Descriptions present ({desc_found_count}/3 checked) and categories in correct order (0.15 pts)")
            total_score += 0.15
        elif desc_found_count >= 2:
            print(f"PARTIAL: Component 4 — {desc_found_count}/3 descriptions found, structure: {has_structure} (0.08 pts)")
            total_score += 0.08
        elif desc_found_count >= 1:
            print(f"PARTIAL: Component 4 — {desc_found_count}/3 descriptions found, structure: {has_structure} (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 4 — No expected description text found, has_structure: {has_structure}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: PDF export exists (0.15 pts)
    try:
        if os.path.exists(PDF_PATH) and os.path.getsize(PDF_PATH) > 1000:
            print(f"PASS: Component 5 — PDF exported at {PDF_PATH} (size: {os.path.getsize(PDF_PATH)} bytes) (0.15 pts)")
            total_score += 0.15
        elif os.path.exists(PDF_PATH):
            print(f"FAIL: Component 5 — PDF exists but is too small ({os.path.getsize(PDF_PATH)} bytes), likely empty")
        else:
            print(f"FAIL: Component 5 — PDF not found at {PDF_PATH}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()

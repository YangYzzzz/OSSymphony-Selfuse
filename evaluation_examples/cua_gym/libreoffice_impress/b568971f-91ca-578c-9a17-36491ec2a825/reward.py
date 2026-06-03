"""
FINAL REWARD SCRIPT - SUCCESS
Task: Change document language for spellchecking to English (UK).
Generated: 2025-10-17 06:59:04
Status: success
Model: azure-o3
Total Steps: 1
"""

import zipfile
import os
import traceback
from lxml import etree

FILE_PATH = '/home/user/change_document_language_for_spellchecking_to_english_uk.pptx'

def extract_lang_attributes_from_xml(xml_bytes):
    """Return all language codes (lang attributes) found in <a:rPr> and <a:pPr> tags."""
    languages = []
    try:
        root = etree.fromstring(xml_bytes)
        a_ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}

        # Run properties (<a:rPr>)
        for rpr in root.xpath('.//a:rPr', namespaces=a_ns):
            lang = rpr.get('lang')
            if lang is not None:
                languages.append(lang)

        # Paragraph properties (<a:pPr>)
        for ppr in root.xpath('.//a:pPr', namespaces=a_ns):
            lang = ppr.get('lang')
            if lang is not None:
                languages.append(lang)
    except Exception as e:
        print(f"Error parsing XML: {e}")
    return languages


def extract_default_language(pptx_zip):
    """Return language codes defined in the default text style of presentation.xml."""
    try:
        pres_xml = pptx_zip.read('ppt/presentation.xml')
        root = etree.fromstring(pres_xml)
        ns = {
            'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
            'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        }
        langs = [rpr.get('lang') for rpr in root.xpath('.//p:defaultTextStyle//a:defRPr', namespaces=ns) if rpr.get('lang')]
        return langs
    except KeyError:
        # presentation.xml not present (extremely unlikely for valid pptx)
        return []
    except Exception as e:
        print(f"Error extracting default language: {e}")
        return []


def verify_language_is_english_uk(file_path):
    """Verify that the document language for spell-checking is English (UK). Returns a progressive score."""
    print(f"Verifying English (UK) language setting in: {file_path}")

    if not os.path.exists(file_path):
        print("✗ File not found")
        return 0.0

    total_lang_attrs = 0  # total language tags encountered
    uk_lang_attrs = 0     # how many of those are English (UK)
    default_uk = False    # is the default text style UK English?

    try:
        with zipfile.ZipFile(file_path, 'r') as pptx_zip:
            # 1. Scan all slide XMLs for explicit lang attributes
            slide_files = [f for f in pptx_zip.namelist() if f.startswith('ppt/slides/slide') and f.endswith('.xml')]
            print(f"Found {len(slide_files)} slide XML files")

            for slide_xml_path in slide_files:
                xml_bytes = pptx_zip.read(slide_xml_path)
                langs = extract_lang_attributes_from_xml(xml_bytes)
                total_lang_attrs += len(langs)
                uk_here = sum(1 for l in langs if l.lower().startswith('en-gb') or l.lower() == 'en-uk')
                uk_lang_attrs += uk_here
                print(f"  {slide_xml_path}: {uk_here}/{len(langs)} English (UK) lang attributes")

            # 2. Check global default language
            default_langs = extract_default_language(pptx_zip)
            default_uk = any(l.lower().startswith('en-gb') or l.lower() == 'en-uk' for l in default_langs)
            if default_langs:
                print(f"Default text style languages: {default_langs}")
            else:
                print("No default text style language entries found")

    except Exception as e:
        print(f"✗ Error processing PPTX: {e}")
        traceback.print_exc()
        return 0.0

    # --- Scoring logic ----------------------------------------------------
    score = 0.0

    if total_lang_attrs == 0:
        # No explicit language tags – rely solely on default language
        if default_uk:
            score = 1.0
            print("✓ Default language is English (UK) – full credit")
        else:
            print("✗ No language tags and default language is not English (UK)")
            score = 0.0
    else:
        proportion_uk = uk_lang_attrs / total_lang_attrs if total_lang_attrs else 0.0
        print(f"Total language tags: {total_lang_attrs}; UK English tags: {uk_lang_attrs}")
        print(f"English (UK) proportion: {proportion_uk:.2%}")

        # Base credit for any evidence of change
        if uk_lang_attrs > 0:
            score += 0.4
        # Additional credit proportional to coverage (capped at 0.6)
        score += 0.6 * proportion_uk
        # Bonus: perfect if all tags (and optionally default) are UK English
        if proportion_uk == 1.0:
            score = 1.0
        else:
            score = min(score, 0.99)  # keep below perfect for partial coverage

    print(f"Calculated score: {score}")
    return score


if __name__ == '__main__':
    reward = verify_language_is_english_uk(FILE_PATH)
    print(f"REWARD: {reward}")

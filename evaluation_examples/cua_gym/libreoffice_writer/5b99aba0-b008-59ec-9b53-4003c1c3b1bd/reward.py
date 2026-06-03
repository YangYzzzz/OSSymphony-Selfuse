"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’ve got a bilingual document open in LibreOffice Writer—most of it is in French, but paragraph 2 is in English. Spell-check won’t leave that second paragraph alone. How do I tag just paragraph 2 as English (USA) without altering the language setting for the rest of the text?
Generated: 2025-09-10 17:03:26
Status: success
Model: azure-o3
Total Steps: 1
"""

import os
import zipfile
import traceback
from lxml import etree

"""
Reward Script: Verify Language Tagging in a Bilingual LibreOffice Writer/Word Document

Task to verify
==============
The user needed to tag ONLY paragraph 2 as English (USA) while keeping the rest of the
bilingual (mostly French) document in its original language. This script checks:
1. Paragraph 2 (index 1) is explicitly tagged with the language code **en-US**.
2. The remaining paragraphs are **not** predominantly tagged as en-US (to ensure the
   global language setting was **not** unintentionally changed).

Scoring (progressive)
---------------------
• 0.6 points – Paragraph 2 correctly tagged en-US.
• 0.4 points – ≥ 75 % of the other paragraphs are **not** en-US (i.e. French or null).
  ‑ 0.2 points if only 50–75 % are non-English.
Total maximum = 1.0.
"""

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

def _run_lang_query(elem):
    """Return a list of language codes (w:lang/@w:val) found in the element."""
    langs = []
    # Paragraph-level language
    langs.extend([ln.get(f"{{{NS['w']}}}val") for ln in elem.xpath('./w:pPr/w:lang', namespaces=NS)])
    # Run-level language(s)
    langs.extend([ln.get(f"{{{NS['w']}}}val") for ln in elem.xpath('.//w:rPr/w:lang', namespaces=NS)])
    # Filter None
    return [l for l in langs if l]

def verify_language_tagging(file_path):
    score = 0.0
    max_score = 1.0

    if not os.path.exists(file_path):
        print(f"✗ File not found: {file_path}")
        return 0.0

    try:
        # Extract document.xml from the DOCX/ODT container
        with zipfile.ZipFile(file_path, 'r') as zf:
            if 'word/document.xml' not in zf.namelist():
                print('✗ word/document.xml not found in archive')
                return 0.0
            xml_bytes = zf.read('word/document.xml')

        root = etree.fromstring(xml_bytes)
        paragraphs = root.xpath('//w:body/w:p', namespaces=NS)
        print(f'Found {len(paragraphs)} paragraphs')
        if len(paragraphs) < 2:
            print('✗ Not enough paragraphs to perform verification')
            return 0.0

        # --- Requirement 1: Paragraph 2 tagged en-US ---
        p2_langs = _run_lang_query(paragraphs[1])
        print(f'Paragraph 2 language codes: {p2_langs}')
        if 'en-US' in p2_langs:
            print('✓ Paragraph 2 correctly tagged as en-US (0.6)')
            score += 0.6
        else:
            print('✗ Paragraph 2 NOT tagged as en-US')

        # --- Requirement 2: Other paragraphs remain non-English ---
        other_langs = []
        for idx, p in enumerate(paragraphs):
            if idx == 1:
                continue  # skip paragraph 2
            lang_codes = _run_lang_query(p)
            other_langs.append(lang_codes[0] if lang_codes else None)

        total_others = len(other_langs)
        non_en_count = sum(1 for l in other_langs if l != 'en-US')
        ratio_non_en = non_en_count / total_others if total_others else 1
        print(f'Other paragraphs not en-US: {non_en_count}/{total_others} (ratio {ratio_non_en:.2f})')

        if ratio_non_en >= 0.75:
            print('✓ Majority of other paragraphs remain non-English (0.4)')
            score += 0.4
        elif ratio_non_en >= 0.5:
            print('✓ Some other paragraphs remain non-English (0.2)')
            score += 0.2
        else:
            print('✗ Too many other paragraphs became en-US')

    except Exception as exc:
        print('✗ Error during verification:', exc)
        traceback.print_exc()
        return 0.0

    final_score = min(score, max_score)
    print(f'Final score: {final_score}')
    return final_score

# ----------------------------------------------------------------------
# MAIN EXECUTION (called by the evaluation harness)
# ----------------------------------------------------------------------
if __name__ == '__main__':
    DOC_PATH = '/home/user/ive_got_a_bilingual_document_open_in_libreoffice_writermost_of_it_is_in_french_but_paragraph_2_is_in.docx'
    reward = verify_language_tagging(DOC_PATH)
    print(f'REWARD: {reward}')


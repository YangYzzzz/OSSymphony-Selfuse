"""
Reward Script: Add Appendix_B_Glossary.odt as last subdocument in master document
Task ID: writer_rm_061
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): Appendix_B_Glossary section exists in the master document
  Component 2 (0.3): The section source links to Appendix_B_Glossary.odt
  Component 3 (0.3): Appendix_B_Glossary is the last section and total sections == 13
"""

import os
import re
import zipfile

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_061'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the ODM file (ZIP archive) and extract content.xml
    # Note: The ODM content.xml has non-standard namespace attributes (xlink:xlink:href)
    # that break standard XML parsers, so we use regex-based parsing.
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            content_xml = z.read('content.xml').decode('utf-8')
    except Exception as e:
        print(f"CRITICAL: Cannot load ODM file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract all section names in order of appearance
    section_names = re.findall(r'text:section\s+text:name="([^"]+)"', content_xml)
    print(f"INFO: Found {len(section_names)} sections: {section_names}")

    # Extract section-source xlink:href values (the first xlink:href in each section-source tag)
    section_sources = re.findall(r'section-source[^>]*?xlink:href="([^"]+)"', content_xml)
    print(f"INFO: Section sources: {section_sources}")

    # Build a mapping of section name -> source href by pairing them
    # Each section has exactly one section-source child, so they align 1:1
    section_to_source = {}
    for i, name in enumerate(section_names):
        if i < len(section_sources):
            section_to_source[name] = section_sources[i]

    # Component 1: Appendix_B_Glossary section exists (0.4 points)
    appendix_b_found = False
    try:
        appendix_b_found = 'Appendix_B_Glossary' in section_names
        if appendix_b_found:
            print(f"PASS: Component 1 — Appendix_B_Glossary section exists (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Appendix_B_Glossary section not found in {section_names}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The section source links to Appendix_B_Glossary.odt (0.3 points)
    try:
        href = section_to_source.get('Appendix_B_Glossary', '')
        if 'Appendix_B_Glossary.odt' in href:
            print(f"PASS: Component 2 — Section source links to Appendix_B_Glossary.odt (href={href}) (0.3 pts)")
            total_score += 0.3
        else:
            if appendix_b_found:
                print(f"FAIL: Component 2 — Section exists but source href='{href}', expected Appendix_B_Glossary.odt")
            else:
                print(f"FAIL: Component 2 — Section not found, cannot check link")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Appendix_B_Glossary is the LAST section and total count is 13 (0.3 points)
    try:
        is_last = len(section_names) > 0 and section_names[-1] == 'Appendix_B_Glossary'
        count_correct = len(section_names) == 13

        if is_last and count_correct:
            print(f"PASS: Component 3 — Appendix_B_Glossary is last section, total=13 (0.3 pts)")
            total_score += 0.3
        elif is_last and not count_correct:
            # It's at the end but count differs — partial credit
            print(f"PARTIAL: Component 3 — Appendix_B_Glossary is last but total sections={len(section_names)}, expected 13 (0.15 pts)")
            total_score += 0.15
        elif not is_last and count_correct:
            print(f"PARTIAL: Component 3 — Total sections=13 but Appendix_B_Glossary is not last (last={section_names[-1] if section_names else 'none'}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — Last section={section_names[-1] if section_names else 'none'}, total={len(section_names)}, expected last=Appendix_B_Glossary, total=13")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook: save any unsaved LibreOffice state before verification
def persist_app_state(domain):
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_writer", "libreoffice_calc", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/Textbook_Master.odm'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

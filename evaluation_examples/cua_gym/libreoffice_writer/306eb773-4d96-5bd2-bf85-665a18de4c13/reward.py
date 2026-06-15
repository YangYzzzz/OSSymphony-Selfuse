"""
Reward Script: Conditional section in Writer document
Task ID: writer_tech_082
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35): Section named 'Advanced Troubleshooting' exists
  Component 2 (0.40): Section has a condition referencing UserLevel and 'admin'
  Component 3 (0.25): Section condition hides when UserLevel != admin (correct polarity)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_tech_082'
TEXT_NS = 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'
OFFICE_NS = 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'


def persist_app_state(domain):
    """Try to save any open LibreOffice document before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print("PERSIST: ctrl+s sent for %s" % domain)
        except Exception as e:
            print("PERSIST_WARN: save hook failed: %s" % e)


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load ODT content.xml
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            content = z.read('content.xml').decode('utf-8')
        root = ET.fromstring(content)
    except Exception as e:
        print("CRITICAL: Cannot load file %s: %s" % (file_path, e))
        print("REWARD: 0.0")
        return 0.0

    # Collect all sections
    sections = list(root.iter('{%s}section' % TEXT_NS))
    section_names = []
    target_section = None
    for sec in sections:
        name = sec.attrib.get('{%s}name' % TEXT_NS, '')
        section_names.append(name)
        if 'advanced' in name.lower() and 'troubleshoot' in name.lower():
            target_section = sec

    # Component 1: A section named 'Advanced Troubleshooting' (or similar) exists (0.35 points)
    try:
        if target_section is not None:
            sec_name = target_section.attrib.get('{%s}name' % TEXT_NS, '')
            print("PASS: Component 1 -- Section '%s' found (0.35 pts)" % sec_name)
            total_score += 0.35
        else:
            print("FAIL: Component 1 -- No section containing 'Advanced Troubleshooting' found. Sections: %s" % section_names)
    except Exception as e:
        print("ERROR: Component 1 -- %s" % e)

    # Component 2: Section has a condition attribute referencing UserLevel and admin (0.40 points)
    try:
        if target_section is not None:
            condition = target_section.attrib.get('{%s}condition' % TEXT_NS, '')
            if condition:
                cond_lower = condition.lower()
                has_userlevel = 'userlevel' in cond_lower
                has_admin = 'admin' in cond_lower
                if has_userlevel and has_admin:
                    print("PASS: Component 2 -- Condition references UserLevel and admin: '%s' (0.40 pts)" % condition)
                    total_score += 0.40
                elif has_userlevel:
                    print("PARTIAL: Component 2 -- Condition references UserLevel but not admin: '%s' (0.20 pts)" % condition)
                    total_score += 0.20
                else:
                    print("FAIL: Component 2 -- Condition does not reference UserLevel: '%s'" % condition)
            else:
                print("FAIL: Component 2 -- Section has no condition attribute")
        else:
            print("FAIL: Component 2 -- No target section found (depends on Component 1)")
    except Exception as e:
        print("ERROR: Component 2 -- %s" % e)

    # Component 3: Condition polarity is correct - hides when UserLevel != admin (0.25 points)
    # The ODF condition for hiding: text:condition="ooow:UserLevel != \"admin\""
    # means "hide this section when UserLevel is not admin" which is correct.
    # Alternatively: text:display="condition" with condition using !=
    # The section should be VISIBLE when UserLevel == admin, HIDDEN otherwise.
    try:
        if target_section is not None:
            condition = target_section.attrib.get('{%s}condition' % TEXT_NS, '')
            if condition:
                # In ODF, the condition attribute specifies WHEN TO HIDE.
                # So "UserLevel != admin" means hide when UserLevel is not admin = correct.
                # "UserLevel == admin" would mean hide when admin = WRONG polarity.
                cond_lower = condition.lower().replace('"', '').replace("'", '')
                # Check for != pattern (correct: hide when not admin)
                has_not_equal = ('!=' in condition or 'ne ' in cond_lower or '<>' in condition)
                # Check for == pattern (wrong: would hide when IS admin)
                has_equal_only = ('==' in condition or '=' in condition.replace('!=', '').replace('<>', '')) and not has_not_equal

                if has_not_equal:
                    print("PASS: Component 3 -- Condition uses != (hides when NOT admin): '%s' (0.25 pts)" % condition)
                    total_score += 0.25
                else:
                    print("FAIL: Component 3 -- Condition polarity may be wrong: '%s'" % condition)
            else:
                print("FAIL: Component 3 -- No condition to check polarity")
        else:
            print("FAIL: Component 3 -- No target section found (depends on Component 1)")
    except Exception as e:
        print("ERROR: Component 3 -- %s" % e)

    final_score = min(total_score, 1.0)
    print("")
    print("Score: %s/1.0" % total_score)
    print("REWARD: %s" % final_score)
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = '%s/%s.odt' % (WORKDIR, TASK_ID)
if not os.path.exists(file_path):
    print("File not found: %s" % file_path)
    print("REWARD: 0.0")
else:
    verify_task(file_path)

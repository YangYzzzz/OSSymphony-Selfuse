"""
Reward Script: Germany Blue Card Guide for Indian Software Engineer
Task ID: osworld_multi_apps_travel_permit_research_010
Domain: libreoffice_writer (ODT file)
Scoring:
  Component 1: File exists with correct name (0.15 pts)
  Component 2: Comprehensive sections/headings present (0.30 pts)
  Component 3: Tables present (salary, timeline, cost) (0.20 pts)
  Component 4: Salary thresholds correctly stated (0.20 pts)
  Component 5: At least 3 official sources cited (0.15 pts)
Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_travel_permit_research_010'
FILE_NAME = 'germany_blue_card_guide_india.odt'
FILE_PATH = os.path.join(WORKDIR, FILE_NAME)


def get_full_text_and_headings(file_path):
    """Parse ODT file and return (full_text_lower, headings_list, table_count)."""
    from odf.opendocument import load
    from odf.text import P, H
    from odf.table import Table

    odt_doc = load(file_path)

    # Collect all paragraph text
    all_text_parts = []
    for para in odt_doc.getElementsByType(P):
        text = ''
        for node in para.childNodes:
            if node.nodeType == node.TEXT_NODE:
                text += node.data
            elif hasattr(node, 'childNodes'):
                for child in node.childNodes:
                    if child.nodeType == child.TEXT_NODE:
                        text += child.data
        if text.strip():
            all_text_parts.append(text.strip())

    # Collect headings
    headings = []
    for h in odt_doc.getElementsByType(H):
        text = ''
        for node in h.childNodes:
            if node.nodeType == node.TEXT_NODE:
                text += node.data
            elif hasattr(node, 'childNodes'):
                for child in node.childNodes:
                    if child.nodeType == child.TEXT_NODE:
                        text += child.data
        if text.strip():
            headings.append(text.strip().lower())

    # Count tables
    tables = odt_doc.getElementsByType(Table)
    table_count = len(tables)

    full_text = ' '.join(all_text_parts).lower()
    return full_text, headings, table_count


def verify_task(file_path):
    """
    Verify that the Germany Blue Card guide ODT document meets all task requirements.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the ODT document
    try:
        full_text, headings, table_count = get_full_text_and_headings(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    headings_combined = ' '.join(headings)

    # Component 1: Required sections/headings present in the document (0.30 pts)
    # Task requires: eligibility, salary threshold, required documents, application process
    # (2 paths), timeline, cost table, language requirements, family reunification, permanent residence
    try:
        required_sections = {
            'eligibility': 'eligib' in headings_combined or 'eligib' in full_text[:500],
            'salary_threshold': 'salary' in headings_combined or 'salary threshold' in full_text,
            'required_documents': 'required document' in headings_combined or 'document' in headings_combined or 'checklist' in headings_combined,
            'application_process': 'application' in headings_combined or 'apply' in headings_combined or 'path' in headings_combined,
            'two_paths': ('path 1' in headings_combined or 'path 2' in headings_combined or
                         'apply from india' in full_text or ('from india' in full_text and 'in germany' in full_text)),
            'timeline': 'timeline' in headings_combined or 'timeline' in full_text,
            'cost_table': 'cost' in headings_combined or 'fee' in headings_combined,
            'language_requirements': 'language' in headings_combined,
            'family_reunification': 'family reunification' in headings_combined or 'family reunification' in full_text,
            'permanent_residence': 'permanent resid' in headings_combined or 'permanent resid' in full_text,
        }

        sections_found = sum(1 for v in required_sections.values() if v)
        sections_total = len(required_sections)

        # Need at least 8 of 10 required sections for full points
        if sections_found >= 9:
            print(f"PASS: Component 1 — All major sections present ({sections_found}/{sections_total}) (0.30 pts)")
            total_score += 0.30
        elif sections_found >= 7:
            partial = 0.20
            print(f"PARTIAL: Component 1 — Most sections present ({sections_found}/{sections_total}) ({partial} pts)")
            total_score += partial
        elif sections_found >= 5:
            partial = 0.10
            print(f"PARTIAL: Component 1 — Some sections present ({sections_found}/{sections_total}) ({partial} pts)")
            total_score += partial
        else:
            missing = [k for k, v in required_sections.items() if not v]
            print(f"FAIL: Component 1 — Only {sections_found}/{sections_total} sections found. Missing: {missing}")

        # Debug info
        for section_name, found in required_sections.items():
            status = 'FOUND' if found else 'MISSING'
            print(f"  Section '{section_name}': {status}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Tables present (salary threshold table, timeline, costs) (0.20 pts)
    try:
        if table_count >= 3:
            print(f"PASS: Component 2 — {table_count} tables found (salary, timeline, cost) (0.20 pts)")
            total_score += 0.20
        elif table_count >= 2:
            print(f"PARTIAL: Component 2 — {table_count} tables found (expected 3) (0.10 pts)")
            total_score += 0.10
        elif table_count == 1:
            print(f"PARTIAL: Component 2 — {table_count} table found (expected 3) (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 2 — No tables found (expected at least 3 for salary, timeline, costs)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Salary thresholds correctly stated (general and shortage occupations) (0.20 pts)
    # Ground truth: 45,300 EUR (general) and 41,041.80 EUR (shortage occupations)
    try:
        has_general_threshold = '45,300' in full_text or '45300' in full_text
        has_shortage_threshold = '41,041' in full_text or '41041' in full_text
        has_shortage_category = 'shortage' in full_text

        if has_general_threshold and has_shortage_threshold and has_shortage_category:
            print(f"PASS: Component 3 — Both salary thresholds present (45,300 general + 41,041.80 shortage) (0.20 pts)")
            total_score += 0.20
        elif (has_general_threshold or has_shortage_threshold) and has_shortage_category:
            print(f"PARTIAL: Component 3 — Partial salary info: general={has_general_threshold}, shortage={has_shortage_threshold} (0.10 pts)")
            total_score += 0.10
        elif has_general_threshold or has_shortage_threshold:
            print(f"PARTIAL: Component 3 — Some salary threshold info present (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 3 — Salary thresholds not found (expected 45,300 and 41,041.80)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: At least 3 official sources cited (make-it-in-germany, BAMF, German Embassy) (0.15 pts)
    try:
        source_checks = {
            'make_it_in_germany': 'make-it-in-germany' in full_text,
            'bamf': 'bamf' in full_text,
            'german_embassy': ('embassy' in full_text or 'diplo.de' in full_text),
        }
        sources_found = sum(1 for v in source_checks.values() if v)

        if sources_found >= 3:
            print(f"PASS: Component 4 — All 3 required official sources cited (make-it-in-germany, BAMF, embassy) (0.15 pts)")
            total_score += 0.15
        elif sources_found == 2:
            print(f"PARTIAL: Component 4 — 2/3 official sources cited (0.08 pts)")
            total_score += 0.08
        elif sources_found == 1:
            print(f"PARTIAL: Component 4 — Only 1/3 official sources cited (0.04 pts)")
            total_score += 0.04
        else:
            print(f"FAIL: Component 4 — No official sources found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Two-path application process described (apply from India vs. in Germany) (0.15 pts)
    try:
        has_path_from_india = ('from india' in full_text and ('embassy' in full_text or 'visa' in full_text))
        has_path_in_germany = 'in germany' in full_text and ('job seeker' in full_text or 'ausländerbehörde' in full_text or 'auslanderbehorde' in full_text or 'immigration office' in full_text)
        has_dual_path = has_path_from_india and has_path_in_germany

        if has_dual_path:
            print(f"PASS: Component 5 — Both application paths described (from India + in Germany) (0.15 pts)")
            total_score += 0.15
        elif has_path_from_india or has_path_in_germany:
            print(f"PARTIAL: Component 5 — Only one application path described (from_india={has_path_from_india}, in_germany={has_path_in_germany}) (0.08 pts)")
            total_score += 0.08
        else:
            print(f"FAIL: Component 5 — Application process paths not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


# Default: test against canonical artifact path in the VM
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

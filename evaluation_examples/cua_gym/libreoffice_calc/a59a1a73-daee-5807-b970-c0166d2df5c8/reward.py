"""
Reward Script: Schengen Visa Application Guide for Chinese Citizens
Task ID: osworld_multi_apps_travel_permit_research_009
Domain: libreoffice_writer (ODT)
Scoring:
  - Component 1 (0.35): ODT file exists at correct Desktop path with correct filename
  - Component 2 (0.35): Document covers all 7 required topic sections
  - Component 3 (0.30): Document cites at least 3 official sources
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_travel_permit_research_009'
TARGET_FILE = '/home/user/Desktop/schengen_visa_china_applicant_guide.odt'


def extract_text_from_odt(file_path):
    """Extract all text content from an ODT file using zipfile + XML parsing."""
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            content_xml = z.read('content.xml').decode('utf-8')
        root = ET.fromstring(content_xml)
        ns = {'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'}

        def get_all_text(element):
            parts = []
            if element.text:
                parts.append(element.text)
            for child in element:
                parts.extend(get_all_text(child))
            if element.tail:
                parts.append(element.tail)
            return parts

        paras = root.findall('.//text:p', ns)
        all_text_parts = []
        for p in paras:
            all_text_parts.extend(get_all_text(p))

        return ' '.join(all_text_parts)
    except Exception as e:
        print(f"ERROR: Failed to extract text from ODT: {e}")
        return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid ODT
    if not os.path.exists(file_path):
        print(f"FAIL: File not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Extract text content for analysis
    full_text = extract_text_from_odt(file_path)
    if full_text is None:
        print("CRITICAL: Cannot parse ODT file — not a valid ODT archive")
        print("REWARD: 0.0")
        return 0.0

    full_text_lower = full_text.lower()

    # Component 1: Correct file path, filename, and ODT format (0.35 points)
    # File must be named exactly 'schengen_visa_china_applicant_guide.odt' on the Desktop
    try:
        correct_filename = os.path.basename(file_path) == 'schengen_visa_china_applicant_guide.odt'
        correct_location = file_path.startswith('/home/user/Desktop/')
        is_odt = file_path.endswith('.odt')
        # Verify it is a valid ODT (ZIP with content.xml)
        with zipfile.ZipFile(file_path, 'r') as z:
            is_valid_odt = 'content.xml' in z.namelist()
        # Check file has substantial content (not empty)
        file_size = os.path.getsize(file_path)
        has_content = file_size > 500  # At least 500 bytes of content

        if correct_filename and correct_location and is_odt and is_valid_odt and has_content:
            print(f"PASS: Component 1 — ODT file at correct Desktop path, size={file_size} bytes (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — correct_filename={correct_filename}, correct_location={correct_location}, "
                  f"is_odt={is_odt}, is_valid_odt={is_valid_odt}, has_content={has_content} (size={file_size})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Document covers all 7 required topic sections (0.35 points)
    # Task requires: which country to apply to, document checklist, biometric appointment,
    # processing timeline, cost breakdown, tips for strong applications, what to do if rejected
    try:
        required_sections = {
            'which_country': (
                any(kw in full_text_lower for kw in [
                    'which schengen country', 'country to apply', 'recommended countries',
                    'main destination country', 'apply at the embassy'
                ])
            ),
            'document_checklist': (
                any(kw in full_text_lower for kw in [
                    'document checklist', 'application documents', 'document requirements',
                    'required documents', 'checklist'
                ])
            ),
            'biometric_appointment': (
                'biometric' in full_text_lower and
                any(kw in full_text_lower for kw in [
                    'appointment', 'fingerprint', 'biometric data'
                ])
            ),
            'processing_timeline': (
                any(kw in full_text_lower for kw in [
                    'processing timeline', 'processing time', 'working days',
                    'calendar days', 'timeline'
                ])
            ),
            'cost_breakdown': (
                any(kw in full_text_lower for kw in [
                    'cost breakdown', 'total cost', 'visa fee', 'eur 80', 'fee'
                ])
            ),
            'tips_strong_application': (
                any(kw in full_text_lower for kw in [
                    'tips for', 'strong application', 'strengthen', 'strong ties',
                    'financial proof', 'cover letter'
                ])
            ),
            'what_to_do_if_rejected': (
                any(kw in full_text_lower for kw in [
                    'if rejected', 'visa is rejected', 'rejection', 'appeal',
                    'reapply', 'refusal'
                ])
            ),
        }

        sections_found = sum(1 for v in required_sections.values() if v)
        sections_total = len(required_sections)

        print(f"Component 2 — Section coverage: {sections_found}/{sections_total}")
        for section_name, found in required_sections.items():
            status = 'PASS' if found else 'FAIL'
            print(f"  {status}: {section_name}")

        # Award full points only when all 7 sections are covered
        if sections_found == sections_total:
            print(f"PASS: Component 2 — All {sections_total} required sections covered (0.35 pts)")
            total_score += 0.35
        elif sections_found >= 5:
            print(f"PARTIAL: Component 2 — {sections_found}/{sections_total} sections covered (0.20 pts)")
            total_score += 0.20
        elif sections_found >= 3:
            print(f"PARTIAL: Component 2 — {sections_found}/{sections_total} sections covered (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 2 — Only {sections_found}/{sections_total} sections covered (0.00 pts)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: At least 3 official sources cited (0.30 points)
    # Task requires at least 3 official sources: individual country embassy sites,
    # eu-delegations.europa.eu, VFS Global
    try:
        sources_found = []

        # Check for VFS Global
        if any(kw in full_text_lower for kw in ['vfs global', 'vfsglobal', 'vfs application']):
            sources_found.append('VFS Global')

        # Check for eu-delegations
        if any(kw in full_text_lower for kw in [
            'eu-delegations', 'eu delegations', 'europa.eu', 'schengen borders code',
            'regulation ec no 810'
        ]):
            sources_found.append('eu-delegations.europa.eu / EU official')

        # Check for embassy sources (individual country)
        embassy_sources = []
        if any(kw in full_text_lower for kw in ['german embassy', 'german consulate', 'deutsche botschaft', 'diplo.de']):
            embassy_sources.append('German Embassy')
        if any(kw in full_text_lower for kw in ['french embassy', 'ambassade de france', 'cn.ambafrance']):
            embassy_sources.append('French Embassy')
        if any(kw in full_text_lower for kw in ['netherlands embassy', 'dutch embassy', 'koninklijke']):
            embassy_sources.append('Netherlands Embassy')
        if embassy_sources:
            sources_found.extend(embassy_sources[:2])  # Count up to 2 distinct embassies

        unique_source_count = len(set(sources_found))
        print(f"Component 3 — Sources found: {list(set(sources_found))}")

        if unique_source_count >= 3:
            print(f"PASS: Component 3 — {unique_source_count} official sources cited (0.30 pts)")
            total_score += 0.30
        elif unique_source_count == 2:
            print(f"PARTIAL: Component 3 — Only {unique_source_count} official sources cited (0.15 pts)")
            total_score += 0.15
        elif unique_source_count == 1:
            print(f"PARTIAL: Component 3 — Only {unique_source_count} official source cited (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 3 — No official sources cited (0.00 pts)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {round(total_score, 4)}/1.0")
    print(f"REWARD: {round(final_score, 4)}")
    return final_score


# Entry point: test against canonical artifact path
if not os.path.exists(TARGET_FILE):
    print(f"File not found: {TARGET_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(TARGET_FILE)

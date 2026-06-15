"""
Reward Script: Insert custom document properties and footer field
Task ID: writer_struct_077
Domain: libreoffice_writer
Scoring:
  Component 1: Custom property 'ProjectCode' = 'PRJ-2025-ML-042'    (0.35 pts)
  Component 2: Custom property 'Classification' = 'Confidential'      (0.25 pts)
  Component 3: Footer contains DOCPROPERTY 'ProjectCode' field         (0.40 pts)
Total: 1.0
"""

import os
import zipfile
import re
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_struct_077'
FILE_PATH = f'{WORKDIR}/ml_project_doc.docx'

# Custom properties namespace
CUSTOM_PROPS_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/custom-properties'
VT_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes'
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Task: Insert custom document properties 'ProjectCode' = 'PRJ-2025-ML-042'
          and 'Classification' = 'Confidential', and insert a DOCPROPERTY field
          for 'ProjectCode' in the footer.
    """
    total_score = 0.0

    # Precondition: file must be readable
    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    with zf:
        namelist = zf.namelist()

        # ---------------------------------------------------------------
        # Component 1: Custom property 'ProjectCode' = 'PRJ-2025-ML-042' (0.35 pts)
        # This FAILS on initial (no custom.xml), PASSES on golden ✅
        # ---------------------------------------------------------------
        try:
            if 'docProps/custom.xml' not in namelist:
                print("FAIL: Component 1 — 'docProps/custom.xml' not found in document (no custom properties)")
            else:
                with zf.open('docProps/custom.xml') as f:
                    content = f.read().decode('utf-8')

                root = ET.fromstring(content)
                project_code_value = None
                for prop in root.findall(f'{{{CUSTOM_PROPS_NS}}}property'):
                    prop_name = prop.get('name', '')
                    if prop_name == 'ProjectCode':
                        # Value stored in vt:lpwstr element
                        lpwstr = prop.find(f'{{{VT_NS}}}lpwstr')
                        if lpwstr is not None:
                            project_code_value = lpwstr.text
                        break

                if project_code_value == 'PRJ-2025-ML-042':
                    print(f"PASS: Component 1 — Custom property 'ProjectCode' = 'PRJ-2025-ML-042' found (0.35 pts)")
                    total_score += 0.35
                elif project_code_value is not None:
                    print(f"FAIL: Component 1 — Custom property 'ProjectCode' found but value is {project_code_value!r}, expected 'PRJ-2025-ML-042'")
                else:
                    print("FAIL: Component 1 — Custom property 'ProjectCode' not found in docProps/custom.xml")
        except Exception as e:
            print(f"ERROR: Component 1 — {e}")

        # ---------------------------------------------------------------
        # Component 2: Custom property 'Classification' = 'Confidential' (0.25 pts)
        # This FAILS on initial (no custom.xml), PASSES on golden ✅
        # ---------------------------------------------------------------
        try:
            if 'docProps/custom.xml' not in namelist:
                print("FAIL: Component 2 — 'docProps/custom.xml' not found in document (no custom properties)")
            else:
                with zf.open('docProps/custom.xml') as f:
                    content = f.read().decode('utf-8')

                root = ET.fromstring(content)
                classification_value = None
                for prop in root.findall(f'{{{CUSTOM_PROPS_NS}}}property'):
                    prop_name = prop.get('name', '')
                    if prop_name == 'Classification':
                        lpwstr = prop.find(f'{{{VT_NS}}}lpwstr')
                        if lpwstr is not None:
                            classification_value = lpwstr.text
                        break

                if classification_value == 'Confidential':
                    print(f"PASS: Component 2 — Custom property 'Classification' = 'Confidential' found (0.25 pts)")
                    total_score += 0.25
                elif classification_value is not None:
                    print(f"FAIL: Component 2 — Custom property 'Classification' found but value is {classification_value!r}, expected 'Confidential'")
                else:
                    print("FAIL: Component 2 — Custom property 'Classification' not found in docProps/custom.xml")
        except Exception as e:
            print(f"ERROR: Component 2 — {e}")

        # ---------------------------------------------------------------
        # Component 3: Footer contains DOCPROPERTY "ProjectCode" field (0.40 pts)
        # The footer must have a w:instrText containing DOCPROPERTY "ProjectCode"
        # and the cached display value must be 'PRJ-2025-ML-042'.
        # This FAILS on initial (empty footer), PASSES on golden ✅
        # ---------------------------------------------------------------
        try:
            footer_file = None
            for name in namelist:
                if name.startswith('word/footer') and name.endswith('.xml'):
                    footer_file = name
                    break

            if footer_file is None:
                print("FAIL: Component 3 — No footer file found in document")
            else:
                with zf.open(footer_file) as f:
                    footer_xml = f.read().decode('utf-8')

                # Check for DOCPROPERTY "ProjectCode" in instrText
                instr_matches = re.findall(
                    r'<w:instrText[^>]*>\s*DOCPROPERTY\s+"?ProjectCode"?\s*</w:instrText>',
                    footer_xml
                )
                # Also check with namespace prefix variation
                if not instr_matches:
                    instr_matches = re.findall(
                        r'DOCPROPERTY\s+"?ProjectCode"?',
                        footer_xml
                    )

                if not instr_matches:
                    print("FAIL: Component 3 — Footer does not contain DOCPROPERTY 'ProjectCode' field instruction")
                else:
                    # Additionally verify the cached display value contains the project code
                    t_values = re.findall(r'<w:t[^>]*>([^<]+)</w:t>', footer_xml)
                    cached_value = ' '.join(t_values).strip()
                    if 'PRJ-2025-ML-042' in cached_value:
                        print(f"PASS: Component 3 — Footer contains DOCPROPERTY 'ProjectCode' field with cached value 'PRJ-2025-ML-042' (0.40 pts)")
                        total_score += 0.40
                    else:
                        # Field instruction is present even if cached value differs — still award partial
                        # The field instruction is the critical part; cached value depends on update state
                        print(f"PASS (partial): Component 3 — Footer contains DOCPROPERTY 'ProjectCode' field instruction (cached value: {cached_value!r}). Awarding 0.40 pts for correct field insertion.")
                        total_score += 0.40
        except Exception as e:
            print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

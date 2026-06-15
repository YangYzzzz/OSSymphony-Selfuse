"""
Reward Script: Client intake form with form controls
Task ID: writer_biz_064
Domain: libreoffice_writer
Scoring:
  Component 1 (0.40): Four text input fields (Company Name, Contact Person, Phone, Email)
  Component 2 (0.35): Dropdown for Industry with 6 specified options
  Component 3 (0.25): Checkbox for Accepts Terms and Conditions
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_biz_064'

# Namespace for Word XML
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


def _parse_form_fields(doc):
    """
    Parse all legacy form fields from the document XML.
    Returns a dict keyed by ffData name with field info.
    """
    body = doc.element.body
    fields = {}

    fld_chars = body.findall('.//w:fldChar', NS)
    for fc in fld_chars:
        fct = fc.get(f'{{{NS["w"]}}}fldCharType', '')
        if fct != 'begin':
            continue
        ffdata = fc.find('w:ffData', NS)
        if ffdata is None:
            continue

        name_el = ffdata.find('w:name', NS)
        name = name_el.get(f'{{{NS["w"]}}}val', '') if name_el is not None else ''

        has_text = ffdata.find('w:textInput', NS) is not None
        has_checkbox = ffdata.find('w:checkBox', NS) is not None
        has_ddl = ffdata.find('w:ddList', NS) is not None

        ctrl_type = 'unknown'
        if has_text:
            ctrl_type = 'text'
        elif has_checkbox:
            ctrl_type = 'checkbox'
        elif has_ddl:
            ctrl_type = 'ddList'

        info = {'name': name, 'type': ctrl_type}

        # Extract dropdown options
        if has_ddl:
            ddl = ffdata.find('w:ddList', NS)
            items = ddl.findall('.//w:listEntry', NS) if ddl is not None else []
            info['options'] = [
                item.get(f'{{{NS["w"]}}}val', '') for item in items
            ]

        fields[name] = info

    return fields


def _get_instrtext_types(doc):
    """
    Get the set of form field instruction types (FORMTEXT, FORMDROPDOWN, FORMCHECKBOX).
    """
    body = doc.element.body
    instrs = body.findall('.//w:instrText', NS)
    return [inst.text.strip() for inst in instrs if inst.text]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse all form fields from document
    try:
        fields = _parse_form_fields(doc)
        instr_types = _get_instrtext_types(doc)
    except Exception as e:
        print(f"CRITICAL: Cannot parse form fields: {e}")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found {len(fields)} form field(s): {list(fields.keys())}")
    print(f"INFO: instrText types: {instr_types}")

    # Component 1: Text input fields for Company Name, Contact Person, Phone, Email (0.4 points, 0.1 each)
    required_text_fields = {
        'CompanyName': ['companyname', 'company_name', 'company name', 'company'],
        'ContactPerson': ['contactperson', 'contact_person', 'contact person', 'contact'],
        'Phone': ['phone', 'telephone', 'tel'],
        'Email': ['email', 'e-mail', 'emailaddress'],
    }
    try:
        for field_label, name_variants in required_text_fields.items():
            found = False
            for fname, finfo in fields.items():
                if finfo['type'] == 'text' and fname.lower().replace(' ', '').replace('_', '') in [
                    v.replace(' ', '').replace('_', '') for v in name_variants
                ]:
                    found = True
                    break
            if not found:
                # Also try substring matching
                for fname, finfo in fields.items():
                    if finfo['type'] == 'text':
                        fname_lower = fname.lower().replace(' ', '').replace('_', '')
                        for variant in name_variants:
                            vn = variant.replace(' ', '').replace('_', '')
                            if vn in fname_lower or fname_lower in vn:
                                found = True
                                break
                    if found:
                        break

            if found:
                print(f"PASS: Component 1 — Text input field for '{field_label}' found (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 1 — Text input field for '{field_label}' NOT found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Dropdown for Industry with 6 specified options (0.35 points)
    try:
        industry_field = None
        for fname, finfo in fields.items():
            if finfo['type'] == 'ddList' and 'industr' in fname.lower():
                industry_field = finfo
                break
        # Fallback: any dropdown field
        if industry_field is None:
            for fname, finfo in fields.items():
                if finfo['type'] == 'ddList':
                    industry_field = finfo
                    break

        if industry_field is None:
            print("FAIL: Component 2 — No dropdown/list form field found for Industry")
        else:
            expected_options = {'technology', 'healthcare', 'finance', 'manufacturing', 'retail', 'other'}
            actual_options = {opt.lower().strip() for opt in industry_field.get('options', [])}
            print(f"INFO: Industry dropdown options: {industry_field.get('options', [])}")

            if expected_options == actual_options:
                print(f"PASS: Component 2 — Industry dropdown with all 6 correct options (0.35 pts)")
                total_score += 0.35
            elif expected_options.issubset(actual_options):
                # Has all required options plus extras
                print(f"PASS: Component 2 — Industry dropdown has all 6 required options (plus extras) (0.35 pts)")
                total_score += 0.35
            elif len(expected_options & actual_options) >= 4:
                # Partial: at least 4 of 6 options correct
                print(f"PARTIAL: Component 2 — Industry dropdown has {len(expected_options & actual_options)}/6 options (0.2 pts)")
                total_score += 0.2
            elif len(actual_options) > 0:
                # Has a dropdown but wrong options
                print(f"PARTIAL: Component 2 — Industry dropdown exists but options mismatch (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 2 — Industry dropdown has no options")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Checkbox for Accepts Terms and Conditions (0.25 points)
    try:
        checkbox_found = False
        for fname, finfo in fields.items():
            if finfo['type'] == 'checkbox':
                # Any checkbox related to terms
                fname_lower = fname.lower().replace(' ', '').replace('_', '')
                if any(kw in fname_lower for kw in ['term', 'accept', 'agree', 'condition']):
                    checkbox_found = True
                    break
        # Fallback: any checkbox at all (task only specifies one)
        if not checkbox_found:
            for fname, finfo in fields.items():
                if finfo['type'] == 'checkbox':
                    checkbox_found = True
                    break

        if checkbox_found:
            print(f"PASS: Component 3 — Checkbox for Terms and Conditions found (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — No checkbox form field found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

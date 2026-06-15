"""
Reward Script: Extract PDF form field data to JSON
Task ID: pdf_pw_029
Domain: pdf
Scoring:
  Component 1 (0.15): survey_data.json exists and is valid JSON array
  Component 2 (0.15): Array has exactly 15 entries
  Component 3 (0.20): Each entry has required keys (field_name, field_type, value)
  Component 4 (0.25): All field_name values match the actual PDF form fields
  Component 5 (0.25): All field_type and value entries are correct
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_029'
JSON_PATH = os.path.join(WORKDIR, 'forms', 'survey_data.json')
PDF_PATH = os.path.join(WORKDIR, 'forms', 'completed_survey.pdf')

# Map PyMuPDF widget type strings to expected JSON type names
WIDGET_TYPE_MAP = {
    'Text': 'text',
    'CheckBox': 'checkbox',
    'RadioButton': 'radio',
    'ComboBox': 'dropdown',
    'ListBox': 'dropdown',
}


def get_pdf_fields(pdf_path):
    """Extract form fields from the PDF using PyMuPDF."""
    import fitz
    doc = fitz.open(pdf_path)
    fields = {}
    for page in doc:
        for w in page.widgets():
            name = w.field_name
            ftype = WIDGET_TYPE_MAP.get(w.field_type_string, w.field_type_string.lower())
            value = w.field_value if w.field_value else ""
            fields[name] = {'field_type': ftype, 'value': value}
    doc.close()
    return fields


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: PDF must exist
    if not os.path.exists(PDF_PATH):
        print(f"CRITICAL: PDF not found at {PDF_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Get ground truth from PDF
    try:
        pdf_fields = get_pdf_fields(PDF_PATH)
        print(f"INFO: Found {len(pdf_fields)} form fields in PDF")
    except Exception as e:
        print(f"CRITICAL: Cannot read PDF form fields: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: survey_data.json exists and is valid JSON array (0.15 pts)
    json_data = None
    try:
        if not os.path.exists(JSON_PATH):
            print(f"FAIL: Component 1 — survey_data.json not found at {JSON_PATH}")
        else:
            with open(JSON_PATH, 'r') as f:
                json_data = json.load(f)
            if isinstance(json_data, list):
                print(f"PASS: Component 1 — survey_data.json exists and is a valid JSON array (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — JSON root is {type(json_data).__name__}, expected list/array")
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 1 — Invalid JSON: {e}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if json_data is None or not isinstance(json_data, list):
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: Array has exactly 15 entries (0.15 pts)
    try:
        count = len(json_data)
        if count == 15:
            print(f"PASS: Component 2 — JSON array has exactly 15 entries (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Expected 15 entries, found {count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Each entry has required keys (0.20 pts)
    required_keys = {'field_name', 'field_type', 'value'}
    try:
        entries_with_keys = 0
        for i, entry in enumerate(json_data):
            if isinstance(entry, dict) and required_keys.issubset(entry.keys()):
                entries_with_keys += 1
            else:
                missing = required_keys - set(entry.keys()) if isinstance(entry, dict) else required_keys
                print(f"  Entry {i}: missing keys {missing}")

        if entries_with_keys == len(json_data) and len(json_data) > 0:
            print(f"PASS: Component 3 — All {entries_with_keys} entries have required keys (0.20 pts)")
            total_score += 0.20
        elif entries_with_keys > 0:
            partial = 0.20 * (entries_with_keys / max(len(json_data), 1))
            print(f"PARTIAL: Component 3 — {entries_with_keys}/{len(json_data)} entries have required keys ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No entries have required keys")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: All field_name values match PDF form fields (0.25 pts)
    try:
        json_names = set()
        for entry in json_data:
            if isinstance(entry, dict) and 'field_name' in entry:
                json_names.add(entry['field_name'])

        pdf_names = set(pdf_fields.keys())
        matching = json_names & pdf_names
        missing_from_json = pdf_names - json_names
        extra_in_json = json_names - pdf_names

        if matching == pdf_names and not extra_in_json:
            print(f"PASS: Component 4 — All {len(matching)} field names match PDF fields (0.25 pts)")
            total_score += 0.25
        elif len(matching) > 0:
            partial = 0.25 * (len(matching) / len(pdf_names))
            print(f"PARTIAL: Component 4 — {len(matching)}/{len(pdf_names)} field names match ({partial:.2f} pts)")
            if missing_from_json:
                print(f"  Missing from JSON: {missing_from_json}")
            if extra_in_json:
                print(f"  Extra in JSON: {extra_in_json}")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No field names match PDF fields")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: All field_type and value entries are correct (0.25 pts)
    try:
        correct_entries = 0
        total_fields = len(pdf_fields)

        for entry in json_data:
            if not isinstance(entry, dict):
                continue
            name = entry.get('field_name', '')
            if name not in pdf_fields:
                continue

            expected = pdf_fields[name]
            etype = entry.get('field_type', '')
            evalue = entry.get('value', '')

            # Normalize type comparison
            type_match = str(etype).lower().strip() == str(expected['field_type']).lower().strip()
            # Normalize value comparison (string comparison, strip whitespace)
            value_match = str(evalue).strip() == str(expected['value']).strip()

            if type_match and value_match:
                correct_entries += 1
            else:
                if not type_match:
                    print(f"  Field '{name}': type mismatch — expected '{expected['field_type']}', got '{etype}'")
                if not value_match:
                    print(f"  Field '{name}': value mismatch — expected '{expected['value']}', got '{evalue}'")

        if correct_entries == total_fields and total_fields > 0:
            print(f"PASS: Component 5 — All {correct_entries} fields have correct type and value (0.25 pts)")
            total_score += 0.25
        elif correct_entries > 0:
            partial = 0.25 * (correct_entries / total_fields)
            print(f"PARTIAL: Component 5 — {correct_entries}/{total_fields} fields correct ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 — No fields have correct type and value")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

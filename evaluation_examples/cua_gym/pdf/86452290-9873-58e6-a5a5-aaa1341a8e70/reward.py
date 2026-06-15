"""
Reward Script: Fill proof of service PDF form fields
Task ID: pdf_legal_058
Domain: pdf
Scoring:
  - Component 1: Filled PDF file exists at expected path (0.1 points)
  - Component 2: ServerName field = 'David Martinez' (0.15 points)
  - Component 3: ServedParty field = 'ABC Corporation' (0.15 points)
  - Component 4: ServedPerson field = 'Jane Doe, Registered Agent' (0.15 points)
  - Component 5: ServiceDate field = '03/25/2024' (0.1 points)
  - Component 6: ServiceTime field = '2:30 PM' (0.1 points)
  - Component 7: ServiceAddress field = '123 Main St, Suite 400, San Francisco, CA 94105' (0.15 points)
  - Component 8: ServiceMethod field = 'Personal Service' (0.1 points)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_058'

# Expected field values from task instruction
EXPECTED_FIELDS = {
    'ServerName': 'David Martinez',
    'ServedParty': 'ABC Corporation',
    'ServedPerson': 'Jane Doe, Registered Agent',
    'ServiceDate': '03/25/2024',
    'ServiceTime': '2:30 PM',
    'ServiceAddress': '123 Main St, Suite 400, San Francisco, CA 94105',
    'ServiceMethod': 'Personal Service',
}

# Scoring weights per field (sum to 0.9; 0.1 for file existence)
FIELD_WEIGHTS = {
    'ServerName': 0.15,
    'ServedParty': 0.15,
    'ServedPerson': 0.15,
    'ServiceDate': 0.10,
    'ServiceTime': 0.10,
    'ServiceAddress': 0.15,
    'ServiceMethod': 0.10,
}


def get_form_fields(pdf_path):
    """Extract all form field name->value mappings from a PDF."""
    doc = pymupdf.open(pdf_path)
    fields = {}
    for page in doc:
        for widget in page.widgets():
            fields[widget.field_name] = widget.field_value
    doc.close()
    return fields


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Filled PDF file exists at the expected output path (0.1 points)
    # The task asks to save as proof_of_service_filled.pdf — this file should NOT exist
    # in the initial env (only the original proof_of_service.pdf exists initially).
    try:
        if os.path.exists(file_path):
            # Additional check: file should be a valid PDF (not empty)
            file_size = os.path.getsize(file_path)
            if file_size > 100:
                print(f"PASS: Component 1 — Filled PDF exists at {file_path} ({file_size} bytes) (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 1 — File exists but too small ({file_size} bytes), likely invalid")
        else:
            print(f"FAIL: Component 1 — Filled PDF not found at {file_path}")
            # No point checking fields if file doesn't exist
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Load form fields from the filled PDF
    try:
        fields = get_form_fields(file_path)
        print(f"INFO: Found {len(fields)} form fields in filled PDF")
    except Exception as e:
        print(f"CRITICAL: Cannot read form fields from {file_path}: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Components 2-8: Verify each form field value
    for field_name, expected_value in EXPECTED_FIELDS.items():
        weight = FIELD_WEIGHTS[field_name]
        comp_num = list(EXPECTED_FIELDS.keys()).index(field_name) + 2
        try:
            actual_value = fields.get(field_name, None)
            if actual_value is not None and str(actual_value).strip() == expected_value:
                print(f"PASS: Component {comp_num} — {field_name} = '{actual_value}' ({weight} pts)")
                total_score += weight
            else:
                print(f"FAIL: Component {comp_num} — {field_name}: expected '{expected_value}', found '{actual_value}'")
        except Exception as e:
            print(f"ERROR: Component {comp_num} — {field_name}: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/legal/forms/proof_of_service_filled.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

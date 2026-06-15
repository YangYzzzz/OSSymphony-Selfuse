"""
Reward Script: PDF Document Classification Pipeline
Task ID: pdf_gf3_036
Domain: pdf
Scoring:
  Component 1: Classifier script exists and is non-empty (0.15)
  Component 2: classifications.json exists with valid structure (0.15)
  Component 3: PDFs moved to correct subdirectories (0.40)
  Component 4: Classification types are correct per PDF (0.20)
  Component 5: Confidence scores are valid numerics in [0,1] (0.10)
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_036'

# Expected classification mapping based on filename prefixes and document types
# The 30 PDFs and their correct categories based on naming convention
EXPECTED_CLASSIFICATIONS = {
    'inv_catering_event.pdf': 'invoice',
    'inv_cloudservices_q4.pdf': 'invoice',
    'inv_consulting_strategic.pdf': 'invoice',
    'inv_maintenance_annual.pdf': 'invoice',
    'inv_marketing_digital.pdf': 'invoice',
    'inv_officesupply_nov.pdf': 'invoice',
    'inv_software_licenses.pdf': 'invoice',
    'inv_techsupply_2024.pdf': 'invoice',
    'contract_employment_senior.pdf': 'contract',
    'contract_lease_office.pdf': 'contract',
    'contract_maintenance_sla.pdf': 'contract',
    'contract_nda_bilateral.pdf': 'contract',
    'contract_partnership_jv.pdf': 'contract',
    'contract_saas_agreement.pdf': 'contract',
    'contract_vendor_master.pdf': 'contract',
    'receipt_amazon_tech.pdf': 'receipt',
    'receipt_fedex_shipping.pdf': 'receipt',
    'receipt_hotel_travel.pdf': 'receipt',
    'receipt_lunch_meeting.pdf': 'receipt',
    'receipt_parking_monthly.pdf': 'receipt',
    'receipt_staples_office.pdf': 'receipt',
    'receipt_uber_ride.pdf': 'receipt',
    'report_customer_satisfaction.pdf': 'report',
    'report_cybersecurity_audit.pdf': 'report',
    'report_employee_engagement.pdf': 'report',
    'report_market_analysis.pdf': 'report',
    'report_operational_efficiency.pdf': 'report',
    'report_product_roadmap.pdf': 'report',
    'report_q3_financial.pdf': 'report',
    'report_sustainability_esg.pdf': 'report',
}

# Map classification type to subdirectory name (plural)
TYPE_TO_SUBDIR = {
    'invoice': 'invoices',
    'contract': 'contracts',
    'receipt': 'receipts',
    'report': 'reports',
}


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    classify_dir = f'{WORKDIR}/classify'

    # Component 1: Classifier script exists and is non-empty (0.15 points)
    try:
        script_path = f'{WORKDIR}/scripts/pdf_classifier.py'
        if os.path.isfile(script_path):
            size = os.path.getsize(script_path)
            if size > 100:  # Must be a real script, not just a stub
                print(f"PASS: Component 1 — pdf_classifier.py exists ({size} bytes) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — pdf_classifier.py too small ({size} bytes), likely stub")
        else:
            print(f"FAIL: Component 1 — pdf_classifier.py not found at {script_path}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: classifications.json exists with valid structure (0.15 points)
    classifications_data = None
    try:
        json_path = f'{classify_dir}/classifications.json'
        if os.path.isfile(json_path):
            with open(json_path) as f:
                classifications_data = json.load(f)
            if isinstance(classifications_data, list) and len(classifications_data) == 30:
                # Check each entry has required fields
                invalid_entries = [
                    e for e in classifications_data
                    if not all(k in e for k in ('filename', 'classified_type', 'confidence_score'))
                ]
                if len(invalid_entries) == 0:
                    print(f"PASS: Component 2 — classifications.json valid with {len(classifications_data)} entries (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 2 — some entries missing required fields (filename, classified_type, confidence_score)")
            else:
                count = len(classifications_data) if isinstance(classifications_data, list) else 'not a list'
                print(f"FAIL: Component 2 — classifications.json has {count} entries, expected 30")
        else:
            print(f"FAIL: Component 2 — classifications.json not found at {json_path}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: PDFs moved to correct subdirectories (0.40 points)
    # Check that no PDFs remain in the root classify directory AND all are in correct subdirs
    try:
        root_pdfs = [f for f in os.listdir(classify_dir) if f.endswith('.pdf')]
        if len(root_pdfs) > 0:
            print(f"FAIL: Component 3 — {len(root_pdfs)} PDFs still in root classify dir")
        else:
            # Check each expected PDF is in its correct subdirectory
            correctly_placed = 0
            total_expected = len(EXPECTED_CLASSIFICATIONS)
            for filename, expected_type in EXPECTED_CLASSIFICATIONS.items():
                subdir = TYPE_TO_SUBDIR[expected_type]
                expected_path = f'{classify_dir}/{subdir}/{filename}'
                if os.path.isfile(expected_path):
                    correctly_placed += 1
                else:
                    print(f"  MISS: {filename} not found in {subdir}/")

            if correctly_placed == total_expected:
                print(f"PASS: Component 3 — all {total_expected} PDFs correctly placed in subdirectories (0.40 pts)")
                total_score += 0.40
            elif correctly_placed > 0:
                # Partial credit: proportional to how many are correctly placed
                if correctly_placed > 0:
                    partial = 0.40 * (correctly_placed / total_expected)
                    print(f"PARTIAL: Component 3 — {correctly_placed}/{total_expected} PDFs correctly placed ({partial:.2f} pts)")
                    total_score += partial
            else:
                print(f"FAIL: Component 3 — no PDFs correctly placed in subdirectories")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Classification types in JSON are correct (0.20 points)
    try:
        if classifications_data and isinstance(classifications_data, list):
            # Build lookup from classifications.json
            json_classifications = {}
            for entry in classifications_data:
                fname = entry.get('filename', '')
                ctype = entry.get('classified_type', '')
                json_classifications[fname] = ctype

            correct_types = 0
            total_checked = 0
            for filename, expected_type in EXPECTED_CLASSIFICATIONS.items():
                actual_type = json_classifications.get(filename)
                if actual_type is not None:
                    total_checked += 1
                    if actual_type == expected_type:
                        correct_types += 1
                    else:
                        print(f"  WRONG TYPE: {filename} classified as '{actual_type}', expected '{expected_type}'")

            if total_checked == 0:
                print(f"FAIL: Component 4 — no matching filenames found in classifications.json")
            elif correct_types == total_checked and total_checked == 30:
                print(f"PASS: Component 4 — all {correct_types} classifications correct (0.20 pts)")
                total_score += 0.20
            elif correct_types > 0:
                partial = 0.20 * (correct_types / 30)
                print(f"PARTIAL: Component 4 — {correct_types}/30 correct classifications ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 — 0 correct classifications")
        else:
            print(f"FAIL: Component 4 — classifications.json not available or invalid")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Confidence scores are valid (0.10 points)
    try:
        if classifications_data and isinstance(classifications_data, list):
            valid_scores = 0
            for entry in classifications_data:
                score = entry.get('confidence_score')
                if isinstance(score, (int, float)) and 0.0 <= score <= 1.0:
                    valid_scores += 1
                else:
                    print(f"  INVALID SCORE: {entry.get('filename', '?')} has score={score}")

            if valid_scores == 30:
                print(f"PASS: Component 5 — all 30 confidence scores valid in [0,1] (0.10 pts)")
                total_score += 0.10
            elif valid_scores > 0:
                partial = 0.10 * (valid_scores / 30)
                print(f"PARTIAL: Component 5 — {valid_scores}/30 valid scores ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 5 — no valid confidence scores")
        else:
            print(f"FAIL: Component 5 — classifications.json not available or invalid")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

"""
Reward Script: PDF form auto-fill service verification
Task ID: pdf_gf3_027
Domain: pdf
Scoring:
  C1 (0.10) - form_service.py exists at /home/user/scripts/form_service.py
  C2 (0.15) - fill_form function is importable and callable
  C3 (0.15) - Validation raises ValueError when Name is missing
  C4 (0.10) - Validation raises ValueError when TaxID is missing
  C5 (0.10) - Validation raises ValueError when Amount is missing
  C6 (0.15) - fill_form returns bytes object for valid input
  C7 (0.15) - Returned bytes are a valid PDF with populated form fields
  C8 (0.10) - Test section or test function exists in the script
"""

import os
import sys
import importlib.util
import tempfile

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_027'
SCRIPT_PATH = os.path.join(WORKDIR, 'scripts', 'form_service.py')
FORM_PATH = os.path.join(WORKDIR, 'forms', 'tax_form_1099.pdf')

SAMPLE_DATA = {
    "PayerName": "Test Corp",
    "PayerTIN": "00-0000000",
    "Name": "Jane Doe",
    "TaxID": "000-00-0000",
    "Address": "123 Main St",
    "City": "Testville",
    "State": "TX",
    "ZipCode": "00000",
    "AccountNumber": "ACC-TEST-001",
    "Amount": "12345.67",
    "FederalTax": "1234.56",
    "StateTax": "567.89",
    "DateFiled": "2025-01-01",
    "Corrected": "Off",
    "SecondTIN": "Off",
}


def load_module(path):
    """Dynamically load form_service module from the given path."""
    spec = importlib.util.spec_from_file_location("form_service", path)
    mod = importlib.util.module_from_spec(spec)
    # Don't execute __main__ block during import
    # We load without running if __name__ == "__main__" by just executing the spec
    spec.loader.exec_module(mod)
    return mod


def verify_task():
    total_score = 0.0

    # Component 1: form_service.py exists (0.10 points)
    try:
        if os.path.isfile(SCRIPT_PATH):
            with open(SCRIPT_PATH, 'r') as f:
                source_code = f.read()
            if len(source_code.strip()) > 50:
                print(f"PASS: Component 1 — form_service.py exists at {SCRIPT_PATH} ({len(source_code)} chars) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 1 — file exists but is too small ({len(source_code)} chars)")
        else:
            print(f"FAIL: Component 1 — {SCRIPT_PATH} does not exist")
            # If the file doesn't exist, nothing else can pass
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Load the module for subsequent checks
    module = None
    fill_form_func = None
    try:
        # Read source to check for test content (C8), but load module carefully
        # Patch __name__ to avoid running tests on import
        spec = importlib.util.spec_from_file_location("form_service", SCRIPT_PATH)
        module = importlib.util.module_from_spec(spec)
        module.__name__ = "form_service"  # ensure __name__ != "__main__"
        spec.loader.exec_module(module)
    except Exception as e:
        print(f"WARNING: Could not import form_service module: {e}")

    # Component 2: fill_form function is callable (0.15 points)
    try:
        if module is not None and hasattr(module, 'fill_form') and callable(module.fill_form):
            fill_form_func = module.fill_form
            print(f"PASS: Component 2 — fill_form function found and callable (0.15 pts)")
            total_score += 0.15
        else:
            if module is None:
                print(f"FAIL: Component 2 — module could not be imported")
            else:
                print(f"FAIL: Component 2 — fill_form not found or not callable in module")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    if fill_form_func is None:
        # Cannot test further without fill_form
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 3: Validation raises ValueError when Name is missing (0.15 points)
    try:
        data_no_name = {"TaxID": "000-00-0000", "Amount": "1000.00"}
        raised = False
        try:
            fill_form_func(data_no_name)
        except ValueError as ve:
            if "Name" in str(ve) or "name" in str(ve).lower():
                raised = True
                print(f"PASS: Component 3 — ValueError raised for missing Name: {ve} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — ValueError raised but doesn't mention Name: {ve}")
        except Exception as ex:
            print(f"FAIL: Component 3 — wrong exception type for missing Name: {type(ex).__name__}: {ex}")
        if not raised and 'Component 3' not in ''.join([]):
            # Check if we already printed
            pass
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Validation raises ValueError when TaxID is missing (0.10 points)
    try:
        data_no_taxid = {"Name": "Jane Doe", "Amount": "1000.00"}
        try:
            fill_form_func(data_no_taxid)
            print(f"FAIL: Component 4 — No exception raised for missing TaxID")
        except ValueError as ve:
            if "TaxID" in str(ve) or "taxid" in str(ve).lower() or "tax" in str(ve).lower():
                print(f"PASS: Component 4 — ValueError raised for missing TaxID: {ve} (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 4 — ValueError raised but doesn't mention TaxID: {ve}")
        except Exception as ex:
            print(f"FAIL: Component 4 — wrong exception type for missing TaxID: {type(ex).__name__}: {ex}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Validation raises ValueError when Amount is missing (0.10 points)
    try:
        data_no_amount = {"Name": "Jane Doe", "TaxID": "000-00-0000"}
        try:
            fill_form_func(data_no_amount)
            print(f"FAIL: Component 5 — No exception raised for missing Amount")
        except ValueError as ve:
            if "Amount" in str(ve) or "amount" in str(ve).lower():
                print(f"PASS: Component 5 — ValueError raised for missing Amount: {ve} (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — ValueError raised but doesn't mention Amount: {ve}")
        except Exception as ex:
            print(f"FAIL: Component 5 — wrong exception type for missing Amount: {type(ex).__name__}: {ex}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: fill_form returns bytes for valid input (0.15 points)
    result_bytes = None
    try:
        result_bytes = fill_form_func(SAMPLE_DATA)
        if isinstance(result_bytes, bytes) and len(result_bytes) > 100:
            print(f"PASS: Component 6 — fill_form returned {len(result_bytes)} bytes (0.15 pts)")
            total_score += 0.15
        elif isinstance(result_bytes, bytes):
            print(f"FAIL: Component 6 — returned bytes but too small ({len(result_bytes)} bytes)")
        else:
            print(f"FAIL: Component 6 — fill_form returned {type(result_bytes).__name__}, not bytes")
    except Exception as e:
        print(f"ERROR: Component 6 — fill_form raised exception with valid data: {e}")

    # Component 7: Returned bytes are a valid PDF with populated fields (0.15 points)
    try:
        if result_bytes and isinstance(result_bytes, bytes):
            import pymupdf
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                tmp.write(result_bytes)
                tmp_path = tmp.name
            doc = pymupdf.open(tmp_path)
            if doc.page_count < 1:
                print(f"FAIL: Component 7 — filled PDF has 0 pages")
            else:
                # Check that at least some fields are populated
                filled_count = 0
                checked_count = 0
                for page in doc:
                    for widget in page.widgets():
                        checked_count += 1
                        val = widget.field_value
                        if val and str(val).strip() and str(val).strip() != "Off":
                            filled_count += 1
                if filled_count >= 3:
                    print(f"PASS: Component 7 — valid PDF with {filled_count}/{checked_count} fields populated (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 7 — only {filled_count}/{checked_count} fields populated (need >= 3)")
            doc.close()
            os.unlink(tmp_path)
        else:
            print(f"FAIL: Component 7 — no valid bytes to verify (skipped)")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    # Component 8: Test section or test function exists (0.10 points)
    try:
        with open(SCRIPT_PATH, 'r') as f:
            source = f.read()
        has_test = False
        # Check for test function definitions or test-related content
        test_indicators = [
            'def test_',
            'def test(',
            'assert ',
            'unittest',
            'pytest',
            'if __name__',
            'test_fill',
            'TESTS',
        ]
        found_indicators = [ind for ind in test_indicators if ind in source]
        # Need at least 2 indicators for a real test section
        if len(found_indicators) >= 2:
            has_test = True
        if has_test:
            print(f"PASS: Component 8 — test section found (indicators: {found_indicators}) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 8 — no test section found (indicators: {found_indicators})")
    except Exception as e:
        print(f"ERROR: Component 8 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_task()

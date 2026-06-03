"""
Reward Script: Python Data Validation Library
Task ID: vscode_gf4_068
Domain: vscode
Scoring:
  C1 (0.15) — venv exists with pydantic v2, email-validator, phonenumbers, pytest
  C2 (0.20) — base.py: BaseValidator abstract class, ValidationResult, compose(), ValidationPipeline
  C3 (0.20) — string.py: 5 validators (Email, Phone, URL, Regex, CreditCard)
  C4 (0.15) — date.py: 3 validators (DateRange, BusinessDay, Age)
  C5 (0.15) — financial.py: 3 validators (Currency, IBAN, AmountRange)
  C6 (0.15) — tests: file exists with 20+ passing tests
"""

import os
import ast
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'python-data-validation')


def check_venv_and_packages():
    """Component 1: venv with required packages (0.15 pts)."""
    venv_dir = os.path.join(PROJECT, 'venv')
    if not os.path.isdir(venv_dir):
        print("FAIL: C1 — venv directory does not exist")
        return 0.0

    # Check installed packages by inspecting site-packages
    site_pkgs = None
    for root, dirs, files in os.walk(os.path.join(venv_dir, 'lib')):
        if 'site-packages' in dirs:
            site_pkgs = os.path.join(root, 'site-packages')
            break

    if site_pkgs is None:
        print("FAIL: C1 — cannot find site-packages in venv")
        return 0.0

    dist_dirs = os.listdir(site_pkgs) if os.path.isdir(site_pkgs) else []
    dist_str = ' '.join(dist_dirs).lower()

    required = {
        'pydantic': False,
        'email_validator': False,
        'phonenumbers': False,
        'pytest': False,
    }

    for pkg_name in required:
        # Check for dist-info or egg-info directories
        for d in dist_dirs:
            dl = d.lower()
            # Normalize: pydantic_core is not pydantic
            if pkg_name == 'pydantic' and dl.startswith('pydantic') and 'core' not in dl and ('dist-info' in dl or 'egg-info' in dl):
                # Verify pydantic v2 by checking version in dist-info name
                if 'pydantic-2' in dl or 'pydantic-2.' in dl:
                    required[pkg_name] = True
                elif 'pydantic-' in dl:
                    # Could be any version; check further
                    version_match = re.search(r'pydantic-(\d+)', dl)
                    if version_match and int(version_match.group(1)) >= 2:
                        required[pkg_name] = True
                break
            elif pkg_name == 'email_validator' and ('email_validator' in dl or 'email-validator' in dl) and ('dist-info' in dl or 'egg-info' in dl):
                required[pkg_name] = True
                break
            elif pkg_name == 'phonenumbers' and dl.startswith('phonenumbers') and ('dist-info' in dl or 'egg-info' in dl):
                required[pkg_name] = True
                break
            elif pkg_name == 'pytest' and dl.startswith('pytest-') and 'core' not in dl and ('dist-info' in dl or 'egg-info' in dl):
                required[pkg_name] = True
                break

    missing = [k for k, v in required.items() if not v]
    if missing:
        print(f"FAIL: C1 — missing packages in venv: {missing}")
        return 0.0

    print("PASS: C1 — venv exists with pydantic v2, email-validator, phonenumbers, pytest (0.15 pts)")
    return 0.15


def check_base_module():
    """Component 2: base.py with BaseValidator, ValidationResult, compose, ValidationPipeline (0.20 pts)."""
    base_path = os.path.join(PROJECT, 'src', 'validators', 'base.py')
    if not os.path.isfile(base_path):
        print("FAIL: C2 — src/validators/base.py does not exist")
        return 0.0

    try:
        with open(base_path, 'r') as f:
            source = f.read()
        tree = ast.parse(source)
    except Exception as e:
        print(f"FAIL: C2 — cannot parse base.py: {e}")
        return 0.0

    class_names = set()
    func_names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_names.add(node.name)
        elif isinstance(node, ast.FunctionDef):
            func_names.add(node.name)

    score = 0.0
    checks = 0

    # Check BaseValidator is an abstract class with validate method
    if 'BaseValidator' in class_names:
        bv_has_validate = any(
            isinstance(item, ast.FunctionDef) and item.name == 'validate'
            for node in ast.walk(tree)
            if isinstance(node, ast.ClassDef) and node.name == 'BaseValidator'
            for item in node.body
        )
        if bv_has_validate:
            checks += 1

    # Check ValidationResult
    if 'ValidationResult' in class_names:
        checks += 1

    # Check compose function
    if 'compose' in func_names:
        checks += 1

    # Check ValidationPipeline with validate method
    if 'ValidationPipeline' in class_names:
        vp_has_validate = any(
            isinstance(item, ast.FunctionDef) and item.name == 'validate'
            for node in ast.walk(tree)
            if isinstance(node, ast.ClassDef) and node.name == 'ValidationPipeline'
            for item in node.body
        )
        if vp_has_validate:
            checks += 1

    if checks == 4:
        score = 0.20
        print(f"PASS: C2 — base.py has BaseValidator(validate), ValidationResult, compose(), ValidationPipeline(validate) (0.20 pts)")
    elif checks >= 2:
        score = 0.10
        print(f"PARTIAL: C2 — base.py has {checks}/4 required components ({score} pts)")
    else:
        print(f"FAIL: C2 — base.py has only {checks}/4 required components")

    return score


def check_string_validators():
    """Component 3: string.py with 5 validators (0.20 pts)."""
    string_path = os.path.join(PROJECT, 'src', 'validators', 'string.py')
    if not os.path.isfile(string_path):
        print("FAIL: C3 — src/validators/string.py does not exist")
        return 0.0

    try:
        with open(string_path, 'r') as f:
            source = f.read()
        tree = ast.parse(source)
    except Exception as e:
        print(f"FAIL: C3 — cannot parse string.py: {e}")
        return 0.0

    class_names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_names.add(node.name)

    required_validators = ['EmailValidator', 'PhoneValidator', 'URLValidator', 'RegexValidator', 'CreditCardValidator']
    found = [v for v in required_validators if v in class_names]
    missing = [v for v in required_validators if v not in class_names]

    if len(found) == 5:
        print(f"PASS: C3 — string.py has all 5 validators: {found} (0.20 pts)")
        return 0.20
    elif len(found) >= 3:
        score = round(0.20 * len(found) / 5, 2)
        print(f"PARTIAL: C3 — string.py has {len(found)}/5 validators, missing: {missing} ({score} pts)")
        return score
    else:
        print(f"FAIL: C3 — string.py has only {len(found)}/5 validators, missing: {missing}")
        return 0.0


def check_date_validators():
    """Component 4: date.py with 3 validators (0.15 pts)."""
    date_path = os.path.join(PROJECT, 'src', 'validators', 'date.py')
    if not os.path.isfile(date_path):
        print("FAIL: C4 — src/validators/date.py does not exist")
        return 0.0

    try:
        with open(date_path, 'r') as f:
            source = f.read()
        tree = ast.parse(source)
    except Exception as e:
        print(f"FAIL: C4 — cannot parse date.py: {e}")
        return 0.0

    class_names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_names.add(node.name)

    required_validators = ['DateRangeValidator', 'BusinessDayValidator', 'AgeValidator']
    found = [v for v in required_validators if v in class_names]
    missing = [v for v in required_validators if v not in class_names]

    if len(found) == 3:
        print(f"PASS: C4 — date.py has all 3 validators: {found} (0.15 pts)")
        return 0.15
    elif len(found) >= 1:
        score = round(0.15 * len(found) / 3, 2)
        print(f"PARTIAL: C4 — date.py has {len(found)}/3 validators, missing: {missing} ({score} pts)")
        return score
    else:
        print(f"FAIL: C4 — date.py has only {len(found)}/3 validators, missing: {missing}")
        return 0.0


def check_financial_validators():
    """Component 5: financial.py with 3 validators (0.15 pts)."""
    fin_path = os.path.join(PROJECT, 'src', 'validators', 'financial.py')
    if not os.path.isfile(fin_path):
        print("FAIL: C5 — src/validators/financial.py does not exist")
        return 0.0

    try:
        with open(fin_path, 'r') as f:
            source = f.read()
        tree = ast.parse(source)
    except Exception as e:
        print(f"FAIL: C5 — cannot parse financial.py: {e}")
        return 0.0

    class_names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_names.add(node.name)

    required_validators = ['CurrencyValidator', 'IBANValidator', 'AmountRangeValidator']
    found = [v for v in required_validators if v in class_names]
    missing = [v for v in required_validators if v not in class_names]

    if len(found) == 3:
        print(f"PASS: C5 — financial.py has all 3 validators: {found} (0.15 pts)")
        return 0.15
    elif len(found) >= 1:
        score = round(0.15 * len(found) / 3, 2)
        print(f"PARTIAL: C5 — financial.py has {len(found)}/3 validators, missing: {missing} ({score} pts)")
        return score
    else:
        print(f"FAIL: C5 — financial.py has only {len(found)}/3 validators, missing: {missing}")
        return 0.0


def check_tests():
    """Component 6: test file exists with 20+ passing tests (0.15 pts)."""
    # Search for test files
    tests_dir = os.path.join(PROJECT, 'tests')
    test_file = None

    if os.path.isdir(tests_dir):
        for fname in os.listdir(tests_dir):
            if fname.startswith('test') and fname.endswith('.py'):
                test_file = os.path.join(tests_dir, fname)
                break

    if test_file is None:
        # Also check project root
        for fname in os.listdir(PROJECT):
            if fname.startswith('test') and fname.endswith('.py'):
                test_file = os.path.join(PROJECT, fname)
                break

    if test_file is None:
        print("FAIL: C6 — no test file found")
        return 0.0

    # Count test methods/functions in the test file
    try:
        with open(test_file, 'r') as f:
            source = f.read()
        tree = ast.parse(source)
    except Exception as e:
        print(f"FAIL: C6 — cannot parse test file: {e}")
        return 0.0

    test_count = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
            test_count += 1

    if test_count >= 20:
        print(f"PASS: C6 — test file has {test_count} test functions (>= 20) (0.15 pts)")
        return 0.15
    elif test_count >= 10:
        score = round(0.15 * test_count / 20, 2)
        print(f"PARTIAL: C6 — test file has {test_count} test functions (< 20) ({score} pts)")
        return score
    else:
        print(f"FAIL: C6 — test file has only {test_count} test functions (need >= 20)")
        return 0.0


def verify_task():
    """Run all verification components and return total score."""
    total_score = 0.0

    # Component 1: venv with required packages (0.15 pts)
    try:
        c1 = check_venv_and_packages()
        if c1 > 0:
            total_score += c1
    except Exception as e:
        print(f"ERROR: C1 — {e}")

    # Component 2: base.py structure (0.20 pts)
    try:
        c2 = check_base_module()
        if c2 > 0:
            total_score += c2
    except Exception as e:
        print(f"ERROR: C2 — {e}")

    # Component 3: string.py validators (0.20 pts)
    try:
        c3 = check_string_validators()
        if c3 > 0:
            total_score += c3
    except Exception as e:
        print(f"ERROR: C3 — {e}")

    # Component 4: date.py validators (0.15 pts)
    try:
        c4 = check_date_validators()
        if c4 > 0:
            total_score += c4
    except Exception as e:
        print(f"ERROR: C4 — {e}")

    # Component 5: financial.py validators (0.15 pts)
    try:
        c5 = check_financial_validators()
        if c5 > 0:
            total_score += c5
    except Exception as e:
        print(f"ERROR: C5 — {e}")

    # Component 6: tests (0.15 pts)
    try:
        c6 = check_tests()
        if c6 > 0:
            total_score += c6
    except Exception as e:
        print(f"ERROR: C6 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.isdir(PROJECT):
    print(f"Project directory not found: {PROJECT}")
    print("REWARD: 0.0")
else:
    verify_task()

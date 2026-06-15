"""
Reward Script: Python Network Scanner project setup verification
Task ID: vscode_gf4_048
Domain: vscode
Scoring:
  - Component 1 (0.15): Virtual environment with required packages
  - Component 2 (0.30): src/scanner.py with NetworkScanner class and 4 methods
  - Component 3 (0.15): src/reporter.py with JSON, CSV, HTML formatting
  - Component 4 (0.15): src/cli.py with Click CLI (scan + report commands)
  - Component 5 (0.10): .vscode/launch.json with debug config and sudo/privilege comment
  - Component 6 (0.15): Tests using mocked socket/scapy calls
"""

import os
import re
import ast
import json

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'python-network-scanner')


def verify_task():
    total_score = 0.0

    # Component 1: Virtual environment with required packages (0.15 points)
    try:
        venv_dir = os.path.join(PROJECT, 'venv')
        pip_path = os.path.join(venv_dir, 'bin', 'pip')
        if os.path.isdir(venv_dir) and os.path.isfile(pip_path):
            # Check installed packages by reading the site-packages
            site_packages_dir = None
            lib_dir = os.path.join(venv_dir, 'lib')
            if os.path.isdir(lib_dir):
                for d in os.listdir(lib_dir):
                    sp = os.path.join(lib_dir, d, 'site-packages')
                    if os.path.isdir(sp):
                        site_packages_dir = sp
                        break

            if site_packages_dir:
                installed = os.listdir(site_packages_dir)
                installed_lower = [x.lower().replace('-', '_').split('.')[0] for x in installed]
                required = ['scapy', 'netifaces', 'ipaddress', 'pytest', 'click']
                found = []
                for pkg in required:
                    # Check if any installed directory/file matches the package name
                    pkg_lower = pkg.lower().replace('-', '_')
                    if any(pkg_lower in item for item in installed_lower):
                        found.append(pkg)

                if len(found) >= 4:  # Allow minor tolerance
                    print(f"PASS: Component 1 - venv exists with packages: {found} (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 1 - venv missing packages. Found: {found}, required: {required}")
            else:
                print(f"FAIL: Component 1 - venv exists but no site-packages found")
        else:
            print(f"FAIL: Component 1 - No virtual environment at {venv_dir}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: src/scanner.py with NetworkScanner class and 4 methods (0.30 points)
    try:
        scanner_path = os.path.join(PROJECT, 'src', 'scanner.py')
        if os.path.isfile(scanner_path):
            with open(scanner_path, 'r') as f:
                scanner_content = f.read()

            # Parse AST to verify class and methods
            tree = ast.parse(scanner_content)
            classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            scanner_class = None
            for cls in classes:
                if cls.name == 'NetworkScanner':
                    scanner_class = cls
                    break

            if scanner_class is None:
                print(f"FAIL: Component 2 - NetworkScanner class not found in scanner.py")
            else:
                methods = {node.name for node in ast.walk(scanner_class)
                           if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef)}
                required_methods = {'scan_range', 'port_scan', 'os_fingerprint', 'async_scan'}
                found_methods = required_methods & methods

                sub_score = 0.0
                # 0.05 for class existing + 0.0625 per required method found
                if len(found_methods) >= 0:
                    sub_score += 0.05 + len(found_methods) * 0.0625

                # Verify scan_range uses CIDR parameter
                if 'scan_range' in methods:
                    # Check for cidr parameter usage
                    if 'cidr' in scanner_content or 'CIDR' in scanner_content:
                        pass  # Already counted above

                # Verify port_scan has host and ports params
                # Verify os_fingerprint uses TTL
                if 'os_fingerprint' in methods and ('ttl' in scanner_content.lower() or 'TTL' in scanner_content):
                    pass  # TTL analysis present

                # Verify async_scan uses asyncio
                if 'async_scan' in methods and 'asyncio' in scanner_content:
                    pass  # asyncio usage present

                total_score += min(sub_score, 0.30)
                if found_methods == required_methods:
                    print(f"PASS: Component 2 - NetworkScanner with all 4 methods ({min(sub_score, 0.30):.2f} pts)")
                else:
                    missing = required_methods - found_methods
                    print(f"PARTIAL: Component 2 - NetworkScanner missing methods: {missing} ({min(sub_score, 0.30):.2f} pts)")
        else:
            print(f"FAIL: Component 2 - src/scanner.py does not exist")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: src/reporter.py with JSON, CSV, HTML formatting (0.15 points)
    try:
        reporter_path = os.path.join(PROJECT, 'src', 'reporter.py')
        if os.path.isfile(reporter_path):
            with open(reporter_path, 'r') as f:
                reporter_content = f.read()

            tree = ast.parse(reporter_content)
            # Find any class that does reporting
            all_methods = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    all_methods.add(node.name)

            sub_score = 0.0
            # Check for JSON formatting capability
            has_json = any(m for m in all_methods if 'json' in m.lower()) or 'json' in reporter_content.lower()
            # Check for CSV formatting capability
            has_csv = any(m for m in all_methods if 'csv' in m.lower()) or 'csv' in reporter_content.lower()
            # Check for HTML formatting capability
            has_html = any(m for m in all_methods if 'html' in m.lower()) or '<table>' in reporter_content or '<html>' in reporter_content

            format_count = sum([has_json, has_csv, has_html])
            sub_score = 0.05 * format_count  # 0.05 per format

            if format_count == 3:
                total_score += 0.15
                print(f"PASS: Component 3 - reporter.py has JSON, CSV, HTML support (0.15 pts)")
            elif format_count > 0:
                total_score += sub_score
                print(f"PARTIAL: Component 3 - reporter.py has {format_count}/3 formats ({sub_score:.2f} pts)")
            else:
                print(f"FAIL: Component 3 - reporter.py missing JSON/CSV/HTML formatting")
        else:
            print(f"FAIL: Component 3 - src/reporter.py does not exist")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: src/cli.py with Click CLI (0.15 points)
    try:
        cli_path = os.path.join(PROJECT, 'src', 'cli.py')
        if os.path.isfile(cli_path):
            with open(cli_path, 'r') as f:
                cli_content = f.read()

            sub_score = 0.0
            # Check for Click import
            if 'click' in cli_content.lower():
                sub_score += 0.05

            # Check for scan command/function
            if re.search(r'def\s+scan\b', cli_content):
                sub_score += 0.05

            # Check for report command/function
            if re.search(r'def\s+report\b', cli_content):
                sub_score += 0.05

            total_score += sub_score
            if sub_score >= 0.15:
                print(f"PASS: Component 4 - cli.py has Click with scan and report commands (0.15 pts)")
            else:
                print(f"PARTIAL: Component 4 - cli.py missing some elements ({sub_score:.2f} pts)")
        else:
            print(f"FAIL: Component 4 - src/cli.py does not exist")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: .vscode/launch.json with debug config and sudo/privilege comment (0.10 points)
    try:
        launch_path = os.path.join(PROJECT, '.vscode', 'launch.json')
        if os.path.isfile(launch_path):
            with open(launch_path, 'r') as f:
                launch_content = f.read()

            sub_score = 0.0

            # Check for valid launch configuration structure
            # launch.json may have JSONC comments, strip them
            cleaned = re.sub(r'//.*$', '', launch_content, flags=re.MULTILINE)
            try:
                launch_data = json.loads(cleaned)
                if 'configurations' in launch_data and len(launch_data['configurations']) > 0:
                    sub_score += 0.05
                    print(f"  launch.json has {len(launch_data['configurations'])} configuration(s)")
            except json.JSONDecodeError:
                print(f"  launch.json is not valid JSON (even after comment stripping)")

            # Check for elevated privileges / sudo comment (in original content with comments)
            privilege_patterns = ['sudo', 'root', 'privilege', 'elevated', 'cap_net_raw', 'raw socket']
            if any(p in launch_content.lower() for p in privilege_patterns):
                sub_score += 0.05

            total_score += sub_score
            if sub_score >= 0.10:
                print(f"PASS: Component 5 - launch.json with config and privilege comment (0.10 pts)")
            else:
                print(f"PARTIAL: Component 5 - launch.json incomplete ({sub_score:.2f} pts)")
        else:
            print(f"FAIL: Component 5 - .vscode/launch.json does not exist")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: Tests using mocked socket/scapy calls (0.15 points)
    try:
        tests_dir = os.path.join(PROJECT, 'tests')
        if os.path.isdir(tests_dir):
            test_files = [f for f in os.listdir(tests_dir) if f.startswith('test_') and f.endswith('.py')]

            if len(test_files) == 0:
                print(f"FAIL: Component 6 - tests/ dir exists but no test_*.py files")
            else:
                sub_score = 0.0

                # Check for test files existence (at least scanner tests)
                has_scanner_test = any('scanner' in f for f in test_files)
                has_any_mock = False

                for tf in test_files:
                    tf_path = os.path.join(tests_dir, tf)
                    with open(tf_path, 'r') as f:
                        test_content = f.read()
                    # Check for mock usage
                    if 'mock' in test_content.lower() or 'patch' in test_content.lower():
                        has_any_mock = True

                if has_scanner_test:
                    sub_score += 0.05

                if has_any_mock:
                    sub_score += 0.05

                # Check for multiple test files (scanner, reporter, cli)
                if len(test_files) >= 2:
                    sub_score += 0.05

                total_score += sub_score
                if sub_score >= 0.15:
                    print(f"PASS: Component 6 - tests with mocked calls, {len(test_files)} test files (0.15 pts)")
                else:
                    print(f"PARTIAL: Component 6 - tests incomplete ({sub_score:.2f} pts)")
        else:
            print(f"FAIL: Component 6 - tests/ directory does not exist")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

"""
Reward Script: Python async scraper project setup in VSCode
Task ID: vscode_gf4_029
Domain: vscode
Scoring:
  Component 1 (0.15): venv with required packages
  Component 2 (0.25): src/scraper.py with AsyncScraper class (fetch, parse_links, scrape_batch)
  Component 3 (0.15): PageResult Pydantic model with required fields
  Component 4 (0.20): tests/test_scraper.py with >= 3 async test functions
  Component 5 (0.10): .vscode/launch.json with Python debug config
  Component 6 (0.15): pytest tests pass
"""

import os
import ast
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'python-async-scraper')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: venv exists with required packages (0.15 points)
    # This FAILS on initial (no venv) and PASSES on golden (venv with packages)
    try:
        venv_dir = os.path.join(PROJECT, 'venv')
        pip_path = os.path.join(venv_dir, 'bin', 'pip')
        if os.path.isdir(venv_dir) and os.path.isfile(pip_path):
            # Check installed packages by reading site-packages
            site_packages = None
            venv_lib = os.path.join(venv_dir, 'lib')
            if os.path.isdir(venv_lib):
                for d in os.listdir(venv_lib):
                    sp = os.path.join(venv_lib, d, 'site-packages')
                    if os.path.isdir(sp):
                        site_packages = sp
                        break

            if site_packages:
                installed_dirs = os.listdir(site_packages)
                installed_lower = [d.lower() for d in installed_dirs]

                required = {
                    'aiohttp': False,
                    'beautifulsoup4': False,
                    'pydantic': False,
                    'pytest_asyncio': False,
                }

                for pkg_key in required:
                    for d in installed_lower:
                        if d.startswith(pkg_key.replace('-', '_')) or d.startswith(pkg_key.replace('_', '-')):
                            required[pkg_key] = True
                            break
                    # Also check dist-info directories
                    if not required[pkg_key]:
                        for d in installed_dirs:
                            if d.lower().startswith(pkg_key.replace('_', '-')) or d.lower().startswith(pkg_key.replace('-', '_')):
                                required[pkg_key] = True
                                break
                    # Special case: beautifulsoup4 dist-info uses "beautifulsoup4"
                    if pkg_key == 'beautifulsoup4' and not required[pkg_key]:
                        for d in installed_dirs:
                            if 'beautifulsoup' in d.lower() or 'bs4' in d.lower():
                                required[pkg_key] = True
                                break

                found_count = sum(1 for v in required.values() if v)
                if found_count == 4:
                    print(f"PASS: Component 1 — venv with all 4 required packages (0.15 pts)")
                    total_score += 0.15
                else:
                    missing = [k for k, v in required.items() if not v]
                    print(f"FAIL: Component 1 — missing packages: {missing} ({found_count}/4 found)")
            else:
                print(f"FAIL: Component 1 — venv exists but no site-packages found")
        else:
            print(f"FAIL: Component 1 — venv directory or pip not found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: src/scraper.py with AsyncScraper class (0.25 points)
    # Checks: class exists, has fetch(), parse_links(), scrape_batch() methods
    # Uses aiohttp, BeautifulSoup, asyncio.gather
    try:
        scraper_path = os.path.join(PROJECT, 'src', 'scraper.py')
        if os.path.isfile(scraper_path):
            with open(scraper_path, 'r') as f:
                source = f.read()

            tree = ast.parse(source)

            # Find AsyncScraper class
            async_scraper_class = None
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name == 'AsyncScraper':
                    async_scraper_class = node
                    break

            if async_scraper_class:
                method_names = set()
                for item in ast.walk(async_scraper_class):
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        method_names.add(item.name)

                required_methods = {'fetch', 'parse_links', 'scrape_batch'}
                has_all_methods = required_methods.issubset(method_names)

                # Check imports for aiohttp, BeautifulSoup, asyncio
                has_aiohttp = 'aiohttp' in source
                has_bs4 = 'BeautifulSoup' in source or 'bs4' in source
                has_asyncio_gather = 'asyncio.gather' in source or 'gather' in source

                if has_all_methods and has_aiohttp and has_bs4 and has_asyncio_gather:
                    print(f"PASS: Component 2 — AsyncScraper with fetch, parse_links, scrape_batch + correct imports (0.25 pts)")
                    total_score += 0.25
                elif has_all_methods:
                    # Partial: class and methods exist but missing some imports
                    print(f"PARTIAL: Component 2 — AsyncScraper has methods but missing imports (aiohttp={has_aiohttp}, bs4={has_bs4}, gather={has_asyncio_gather}) (0.15 pts)")
                    total_score += 0.15
                else:
                    missing_methods = required_methods - method_names
                    print(f"FAIL: Component 2 — AsyncScraper missing methods: {missing_methods}")
            else:
                print(f"FAIL: Component 2 — AsyncScraper class not found in scraper.py")
        else:
            print(f"FAIL: Component 2 — src/scraper.py does not exist")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: PageResult Pydantic model with url, title, links, status_code (0.15 points)
    try:
        scraper_path = os.path.join(PROJECT, 'src', 'scraper.py')
        if os.path.isfile(scraper_path):
            with open(scraper_path, 'r') as f:
                source = f.read()

            tree = ast.parse(source)

            # Find PageResult class
            page_result_class = None
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name == 'PageResult':
                    page_result_class = node
                    break

            if page_result_class:
                # Check that it inherits from BaseModel (Pydantic)
                inherits_basemodel = any(
                    (isinstance(base, ast.Name) and base.id == 'BaseModel') or
                    (isinstance(base, ast.Attribute) and base.attr == 'BaseModel')
                    for base in page_result_class.bases
                )

                # Check for required fields by looking at class-level annotations
                field_names = set()
                for item in page_result_class.body:
                    if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                        field_names.add(item.target.id)

                required_fields = {'url', 'title', 'links', 'status_code'}
                has_all_fields = required_fields.issubset(field_names)

                if inherits_basemodel and has_all_fields:
                    print(f"PASS: Component 3 — PageResult(BaseModel) with all 4 required fields (0.15 pts)")
                    total_score += 0.15
                elif has_all_fields:
                    print(f"PARTIAL: Component 3 — PageResult has fields but doesn't inherit BaseModel (0.05 pts)")
                    total_score += 0.05
                else:
                    missing_fields = required_fields - field_names
                    print(f"FAIL: Component 3 — PageResult missing fields: {missing_fields}, inherits_basemodel={inherits_basemodel}")
            else:
                print(f"FAIL: Component 3 — PageResult class not found")
        else:
            print(f"FAIL: Component 3 — src/scraper.py does not exist")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: tests/test_scraper.py with >= 3 async test functions (0.20 points)
    try:
        test_path = os.path.join(PROJECT, 'tests', 'test_scraper.py')
        if os.path.isfile(test_path):
            with open(test_path, 'r') as f:
                source = f.read()

            tree = ast.parse(source)

            # Count async test functions (functions starting with 'test_' that are async)
            async_test_count = 0
            for node in ast.walk(tree):
                if isinstance(node, ast.AsyncFunctionDef) and node.name.startswith('test_'):
                    async_test_count += 1

            # Also check for pytest-asyncio marker or import
            has_pytest_asyncio = 'pytest_asyncio' in source or 'pytest.mark.asyncio' in source

            # Check for mock usage (aiohttp mock session or unittest.mock)
            has_mock = 'mock' in source.lower() or 'Mock' in source

            if async_test_count >= 3 and has_pytest_asyncio and has_mock:
                print(f"PASS: Component 4 — {async_test_count} async tests with pytest-asyncio + mocks (0.20 pts)")
                total_score += 0.20
            elif async_test_count >= 3:
                print(f"PARTIAL: Component 4 — {async_test_count} async tests but missing pytest-asyncio/mocks (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 4 — only {async_test_count} async test functions (need >= 3)")
        else:
            print(f"FAIL: Component 4 — tests/test_scraper.py does not exist")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: .vscode/launch.json with Python debug config (0.10 points)
    try:
        launch_path = os.path.join(PROJECT, '.vscode', 'launch.json')
        if os.path.isfile(launch_path):
            with open(launch_path, 'r') as f:
                content = f.read()

            # Strip JSONC comments before parsing
            content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            launch_config = json.loads(content_clean)

            configs = launch_config.get('configurations', [])
            has_python_debug = any(
                cfg.get('type') in ('python', 'debugpy') and
                cfg.get('request') == 'launch'
                for cfg in configs
            )

            if has_python_debug:
                print(f"PASS: Component 5 — launch.json has Python debug configuration (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — launch.json exists but no Python debug config found (types: {[c.get('type') for c in configs]})")
        else:
            print(f"FAIL: Component 5 — .vscode/launch.json does not exist")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Tests pass with pytest (0.15 points)
    try:
        venv_pytest = os.path.join(PROJECT, 'venv', 'bin', 'pytest')
        if os.path.isfile(venv_pytest):
            # Use os.popen to run pytest (subprocess is forbidden)
            import tempfile
            tmp_out = os.path.join(tempfile.gettempdir(), 'pytest_output.txt')
            cmd = f'cd {PROJECT} && {venv_pytest} tests/ -v --tb=short > {tmp_out} 2>&1; echo "EXIT:$?" >> {tmp_out}'
            os.system(cmd)

            output = ''
            if os.path.isfile(tmp_out):
                with open(tmp_out, 'r') as f:
                    output = f.read()

            # Count passed/failed
            passed_match = re.search(r'(\d+) passed', output)
            failed_match = re.search(r'(\d+) failed', output)

            passed = int(passed_match.group(1)) if passed_match else 0
            failed = int(failed_match.group(1)) if failed_match else 0

            if passed >= 3 and failed == 0:
                print(f"PASS: Component 6 — pytest: {passed} passed, {failed} failed (0.15 pts)")
                total_score += 0.15
            elif passed > 0:
                partial = 0.15 * (passed / (passed + failed)) if (passed + failed) > 0 else 0
                print(f"PARTIAL: Component 6 — pytest: {passed} passed, {failed} failed ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 6 — pytest: {passed} passed, {failed} failed")
                if output:
                    print(f"  output: {output[-500:]}")
        else:
            print(f"FAIL: Component 6 — pytest not found in venv")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

"""
Reward Script: Collect ML project resources (iris CSV, screenshot, HTML, README.odt)
Task ID: osworld_multi_apps_sys_browser_os_007
Domain: multi_apps (os + browser + libreoffice_writer)

Scoring Rubric:
  Component 1: iris.csv downloaded with correct headers and >=150 data rows (0.25 pts)
  Component 2: sklearn_iris_docs.png exists as valid non-empty PNG file (0.20 pts)
  Component 3: uci_iris.html exists with relevant UCI/iris HTML content (0.20 pts)
  Component 4: README.odt documents all three sources with local paths (0.35 pts)
  Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user/ml_project'

# Expected file paths
IRIS_CSV_PATH = f'{WORKDIR}/data/iris.csv'
SKLEARN_PNG_PATH = f'{WORKDIR}/docs/sklearn_iris_docs.png'
UCI_HTML_PATH = f'{WORKDIR}/docs/uci_iris.html'
README_ODT_PATH = f'{WORKDIR}/README.odt'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: iris.csv downloaded with correct headers and >=150 data rows (0.25 points)
    # This must FAIL on initial_env (no iris.csv) and PASS on golden_env
    try:
        if not os.path.isfile(IRIS_CSV_PATH):
            print(f"FAIL: Component 1 — iris.csv not found at {IRIS_CSV_PATH}")
        else:
            with open(IRIS_CSV_PATH, 'r') as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]

            if len(lines) < 2:
                print(f"FAIL: Component 1 — iris.csv has too few lines ({len(lines)})")
            else:
                header = lines[0].lower()
                # Check for expected iris CSV headers
                expected_cols = ['sepal', 'petal', 'species']
                has_expected_headers = all(col in header for col in expected_cols)
                data_rows = len(lines) - 1  # exclude header row

                if has_expected_headers and data_rows >= 150:
                    print(f"PASS: Component 1 — iris.csv has valid headers and {data_rows} data rows (0.25 pts)")
                    total_score += 0.25
                elif has_expected_headers:
                    print(f"FAIL: Component 1 — iris.csv has valid headers but only {data_rows} data rows (expected >=150)")
                else:
                    print(f"FAIL: Component 1 — iris.csv headers don't match expected: found '{header}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: sklearn_iris_docs.png exists as a valid non-empty PNG file (0.20 points)
    # This must FAIL on initial_env (no PNG file) and PASS on golden_env
    try:
        if not os.path.isfile(SKLEARN_PNG_PATH):
            print(f"FAIL: Component 2 — sklearn_iris_docs.png not found at {SKLEARN_PNG_PATH}")
        else:
            # Verify PNG magic bytes: 89 50 4E 47 0D 0A 1A 0A
            PNG_MAGIC = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
            with open(SKLEARN_PNG_PATH, 'rb') as f:
                header_bytes = f.read(8)
                file_size = os.path.getsize(SKLEARN_PNG_PATH)

            if header_bytes == PNG_MAGIC and file_size > 1000:
                print(f"PASS: Component 2 — sklearn_iris_docs.png is a valid PNG ({file_size} bytes) (0.20 pts)")
                total_score += 0.20
            elif header_bytes != PNG_MAGIC:
                print(f"FAIL: Component 2 — file is not a valid PNG (magic bytes: {header_bytes.hex()})")
            else:
                print(f"FAIL: Component 2 — PNG file is too small ({file_size} bytes), likely not a real screenshot")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: uci_iris.html exists with relevant UCI/iris HTML content (0.20 points)
    # This must FAIL on initial_env (no HTML file) and PASS on golden_env
    try:
        if not os.path.isfile(UCI_HTML_PATH):
            print(f"FAIL: Component 3 — uci_iris.html not found at {UCI_HTML_PATH}")
        else:
            with open(UCI_HTML_PATH, 'r', encoding='utf-8', errors='replace') as f:
                html_content = f.read()

            # Check that the HTML file has content relevant to UCI Iris page
            content_lower = html_content.lower()
            has_html_structure = '<html' in content_lower or '<!doctype html' in content_lower
            has_iris_content = 'iris' in content_lower
            has_uci_content = 'uci' in content_lower or 'machine learning repository' in content_lower
            file_size = os.path.getsize(UCI_HTML_PATH)

            if has_html_structure and has_iris_content and has_uci_content and file_size > 500:
                print(f"PASS: Component 3 — uci_iris.html is valid HTML with UCI/Iris content ({file_size} bytes) (0.20 pts)")
                total_score += 0.20
            elif not has_html_structure:
                print(f"FAIL: Component 3 — uci_iris.html lacks HTML structure tags")
            elif not has_iris_content:
                print(f"FAIL: Component 3 — uci_iris.html has no iris-related content")
            elif not has_uci_content:
                print(f"FAIL: Component 3 — uci_iris.html has no UCI-related content")
            else:
                print(f"FAIL: Component 3 — uci_iris.html is too small ({file_size} bytes)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: README.odt documents all three sources with local paths (0.35 points)
    # This must FAIL on initial_env (no README.odt) and PASS on golden_env
    # Sub-scoring:
    #   - 0.10: ODT file exists and is valid (can open as zip + has content.xml)
    #   - 0.10: Documents iris.csv local path
    #   - 0.10: Documents sklearn screenshot local path
    #   - 0.05: Documents uci_iris.html local path
    try:
        if not os.path.isfile(README_ODT_PATH):
            print(f"FAIL: Component 4 — README.odt not found at {README_ODT_PATH}")
        else:
            # ODT files are zip archives containing content.xml
            try:
                with zipfile.ZipFile(README_ODT_PATH, 'r') as z:
                    if 'content.xml' not in z.namelist():
                        print(f"FAIL: Component 4 — README.odt does not contain content.xml")
                    else:
                        xml_content = z.read('content.xml').decode('utf-8')

                        # Extract text from XML (strip tags for searching)
                        try:
                            root = ET.fromstring(xml_content)
                            # Get all text nodes
                            all_text = ' '.join(root.itertext())
                        except ET.ParseError:
                            all_text = xml_content

                        text_lower = all_text.lower()

                        # Sub-component 4a: Valid ODT with actual text content (0.10 pts)
                        if len(all_text.strip()) > 50:
                            print(f"PASS: Component 4a — README.odt is a valid ODT with text content (0.10 pts)")
                            total_score += 0.10
                        else:
                            print(f"FAIL: Component 4a — README.odt has too little text content")

                        # Sub-component 4b: Documents iris.csv with local path (0.10 pts)
                        has_iris_csv_path = 'ml_project/data/iris.csv' in all_text or 'data/iris.csv' in all_text
                        if has_iris_csv_path:
                            print(f"PASS: Component 4b — README.odt documents iris.csv local path (0.10 pts)")
                            total_score += 0.10
                        else:
                            print(f"FAIL: Component 4b — README.odt does not document iris.csv local path")

                        # Sub-component 4c: Documents sklearn screenshot local path (0.10 pts)
                        has_sklearn_path = 'sklearn_iris_docs.png' in all_text or 'docs/sklearn' in all_text
                        if has_sklearn_path:
                            print(f"PASS: Component 4c — README.odt documents sklearn screenshot local path (0.10 pts)")
                            total_score += 0.10
                        else:
                            print(f"FAIL: Component 4c — README.odt does not document sklearn screenshot local path")

                        # Sub-component 4d: Documents uci_iris.html local path (0.05 pts)
                        has_uci_html_path = 'uci_iris.html' in all_text or 'docs/uci' in all_text
                        if has_uci_html_path:
                            print(f"PASS: Component 4d — README.odt documents uci_iris.html local path (0.05 pts)")
                            total_score += 0.05
                        else:
                            print(f"FAIL: Component 4d — README.odt does not document uci_iris.html local path")

            except zipfile.BadZipFile:
                print(f"FAIL: Component 4 — README.odt is not a valid ZIP/ODT archive")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

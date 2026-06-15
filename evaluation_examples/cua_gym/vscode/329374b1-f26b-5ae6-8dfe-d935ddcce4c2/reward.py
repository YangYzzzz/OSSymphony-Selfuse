"""
Reward Script: Create a multi-module Maven project structure
Task ID: vscode_lang_074
Domain: vscode
Scoring:
  Component 1 (0.30): Parent pom.xml with packaging=pom and modules listing api+service
  Component 2 (0.25): api/pom.xml with parent reference to java-multi
  Component 3 (0.25): service/pom.xml with parent reference and dependency on api
  Component 4 (0.20): Standard Maven directory structure (src/main/java, src/test/java) in both modules
"""

import os
import xml.etree.ElementTree as ET

WORKDIR = '/home/user/projects/java-multi'
TASK_ID = 'vscode_lang_074'

# Maven POM namespace
NS = {'m': 'http://maven.apache.org/POM/4.0.0'}


def parse_pom(path):
    """Parse a pom.xml file and return the root element, or None on failure."""
    try:
        tree = ET.parse(path)
        return tree.getroot()
    except Exception as e:
        print(f"ERROR: Cannot parse {path}: {e}")
        return None


def get_text(element, xpath, ns=NS):
    """Get text content of an element found by xpath, or None."""
    if element is None:
        return None
    found = element.find(xpath, ns)
    if found is not None and found.text is not None:
        return found.text.strip()
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Parent pom.xml with packaging=pom and modules (0.30 points)
    try:
        parent_pom_path = os.path.join(WORKDIR, 'pom.xml')
        if not os.path.exists(parent_pom_path):
            print(f"FAIL: Component 1 — parent pom.xml not found at {parent_pom_path}")
        else:
            root = parse_pom(parent_pom_path)
            if root is None:
                print("FAIL: Component 1 — parent pom.xml could not be parsed")
            else:
                packaging = get_text(root, 'm:packaging')
                modules_elem = root.find('m:modules', NS)

                packaging_ok = (packaging == 'pom')
                modules_ok = False
                module_names = []

                if modules_elem is not None:
                    module_names = [m.text.strip() for m in modules_elem.findall('m:module', NS) if m.text]
                    modules_ok = ('api' in module_names and 'service' in module_names)

                if packaging_ok and modules_ok:
                    print(f"PASS: Component 1 — parent pom.xml has packaging=pom and modules={module_names} (0.30 pts)")
                    total_score += 0.30
                elif packaging_ok:
                    print(f"FAIL: Component 1 — packaging=pom OK but modules missing or incomplete: {module_names}")
                    total_score += 0.10
                elif modules_ok:
                    print(f"FAIL: Component 1 — modules OK but packaging is '{packaging}' instead of 'pom'")
                    total_score += 0.10
                else:
                    print(f"FAIL: Component 1 — packaging='{packaging}', modules={module_names}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: api/pom.xml with parent reference (0.25 points)
    try:
        api_pom_path = os.path.join(WORKDIR, 'api', 'pom.xml')
        if not os.path.exists(api_pom_path):
            print(f"FAIL: Component 2 — api/pom.xml not found")
        else:
            root = parse_pom(api_pom_path)
            if root is None:
                print("FAIL: Component 2 — api/pom.xml could not be parsed")
            else:
                # Check parent reference
                parent_group = get_text(root, 'm:parent/m:groupId')
                parent_artifact = get_text(root, 'm:parent/m:artifactId')
                artifact_id = get_text(root, 'm:artifactId')

                has_parent = (parent_artifact is not None and parent_artifact != '')
                is_api = (artifact_id is not None and 'api' in artifact_id.lower())

                if has_parent and is_api:
                    print(f"PASS: Component 2 — api/pom.xml has parent={parent_group}:{parent_artifact}, artifactId={artifact_id} (0.25 pts)")
                    total_score += 0.25
                elif has_parent:
                    print(f"FAIL: Component 2 — api/pom.xml has parent but artifactId='{artifact_id}' does not indicate api")
                    total_score += 0.10
                else:
                    print(f"FAIL: Component 2 — api/pom.xml missing parent reference")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: service/pom.xml with parent reference and dependency on api (0.25 points)
    try:
        svc_pom_path = os.path.join(WORKDIR, 'service', 'pom.xml')
        if not os.path.exists(svc_pom_path):
            print(f"FAIL: Component 3 — service/pom.xml not found")
        else:
            root = parse_pom(svc_pom_path)
            if root is None:
                print("FAIL: Component 3 — service/pom.xml could not be parsed")
            else:
                # Check parent reference
                parent_artifact = get_text(root, 'm:parent/m:artifactId')
                artifact_id = get_text(root, 'm:artifactId')
                has_parent = (parent_artifact is not None and parent_artifact != '')
                is_service = (artifact_id is not None and 'service' in artifact_id.lower())

                # Check dependency on api
                deps = root.find('m:dependencies', NS)
                api_dep_artifacts = []
                if deps is not None:
                    api_dep_artifacts = [
                        get_text(dep, 'm:artifactId')
                        for dep in deps.findall('m:dependency', NS)
                        if get_text(dep, 'm:artifactId') and 'api' in get_text(dep, 'm:artifactId').lower()
                    ]
                has_api_dep = len(api_dep_artifacts) > 0

                if has_parent and is_service and has_api_dep:
                    print(f"PASS: Component 3 — service/pom.xml has parent={parent_artifact}, artifactId={artifact_id}, depends on api (0.25 pts)")
                    total_score += 0.25
                elif has_parent and is_service:
                    print(f"FAIL: Component 3 — service/pom.xml has parent and correct artifactId but missing api dependency")
                    total_score += 0.10
                elif has_parent:
                    print(f"FAIL: Component 3 — service/pom.xml has parent but artifactId='{artifact_id}', api_dep={has_api_dep}")
                    total_score += 0.05
                else:
                    print(f"FAIL: Component 3 — service/pom.xml missing parent reference")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Standard Maven directory structure in both modules (0.20 points)
    try:
        expected_dirs = [
            os.path.join(WORKDIR, 'api', 'src', 'main', 'java'),
            os.path.join(WORKDIR, 'api', 'src', 'test', 'java'),
            os.path.join(WORKDIR, 'service', 'src', 'main', 'java'),
            os.path.join(WORKDIR, 'service', 'src', 'test', 'java'),
        ]

        dirs_found = 0
        for d in expected_dirs:
            if os.path.isdir(d):
                dirs_found += 1
                print(f"  OK: directory exists: {d}")
            else:
                print(f"  MISSING: directory not found: {d}")

        if dirs_found == len(expected_dirs):
            print(f"PASS: Component 4 — all {len(expected_dirs)} Maven standard dirs present (0.20 pts)")
            total_score += 0.20
        elif dirs_found >= 2:
            partial = round(0.20 * dirs_found / len(expected_dirs), 2)
            print(f"PARTIAL: Component 4 — {dirs_found}/{len(expected_dirs)} dirs present ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — only {dirs_found}/{len(expected_dirs)} dirs present")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.isdir(WORKDIR):
    print(f"Project directory not found: {WORKDIR}")
    print("REWARD: 0.0")
else:
    verify_task()

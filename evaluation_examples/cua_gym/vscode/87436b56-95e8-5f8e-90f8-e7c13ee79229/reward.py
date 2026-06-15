"""
Reward script for vscode_gf4_003: TypeScript project setup verification.

Scoring rubric (5 checks, each worth 0.2):
1. package.json exists and is valid JSON (0.2)
2. package.json has typescript AND ts-node in devDependencies (0.2)
3. tsconfig.json exists, is valid JSON, has outDir='./dist', rootDir='./src', strict=true (0.2)
4. src/index.ts exists and contains a console.log statement (0.2)
5. All JSON files (package.json, tsconfig.json) are syntactically valid (0.2)
   (This is partially redundant with checks 1 and 3 but serves as a combined gate.)

Total: 0.0 - 1.0
"""

import json
import os
import re

WORKDIR = "/home/user"
PROJECT = os.path.join(WORKDIR, "projects", "typescript-app")


def check_package_json_exists_and_valid():
    """Check 1: package.json exists and is valid JSON."""
    path = os.path.join(PROJECT, "package.json")
    if not os.path.isfile(path):
        return 0.0, None
    try:
        with open(path, "r") as f:
            data = json.load(f)
        return 1.0, data
    except (json.JSONDecodeError, IOError):
        return 0.0, None


def check_dev_dependencies(pkg_data):
    """Check 2: devDependencies contain typescript and ts-node."""
    if pkg_data is None:
        return 0.0
    dev_deps = pkg_data.get("devDependencies", {})
    if not isinstance(dev_deps, dict):
        return 0.0
    has_typescript = "typescript" in dev_deps
    has_ts_node = "ts-node" in dev_deps
    if has_typescript and has_ts_node:
        return 1.0
    elif has_typescript or has_ts_node:
        return 0.5
    return 0.0


def check_tsconfig():
    """Check 3: tsconfig.json exists with correct compilerOptions."""
    path = os.path.join(PROJECT, "tsconfig.json")
    if not os.path.isfile(path):
        return 0.0, False
    try:
        with open(path, "r") as f:
            content = f.read()
        # Strip JSONC comments before parsing
        cleaned = re.sub(r"//.*$", "", content, flags=re.MULTILINE)
        cleaned = re.sub(r"/\*.*?\*/", "", cleaned, flags=re.DOTALL)
        data = json.loads(cleaned)
    except (json.JSONDecodeError, IOError):
        return 0.0, False

    compiler_opts = data.get("compilerOptions", {})
    if not isinstance(compiler_opts, dict):
        return 0.0, True  # JSON valid but no compilerOptions

    score = 0.0
    checks = 3
    if compiler_opts.get("outDir") == "./dist":
        score += 1
    if compiler_opts.get("rootDir") == "./src":
        score += 1
    if compiler_opts.get("strict") is True:
        score += 1

    return score / checks, True


def check_index_ts():
    """Check 4: src/index.ts exists and contains console.log."""
    path = os.path.join(PROJECT, "src", "index.ts")
    if not os.path.isfile(path):
        return 0.0
    try:
        with open(path, "r") as f:
            content = f.read()
    except IOError:
        return 0.0
    if "console.log" in content:
        return 1.0
    return 0.0


def check_all_json_valid():
    """Check 5: Both JSON config files are syntactically valid."""
    files = [
        os.path.join(PROJECT, "package.json"),
        os.path.join(PROJECT, "tsconfig.json"),
    ]
    valid_count = 0
    total = 0
    for fpath in files:
        if not os.path.isfile(fpath):
            continue
        total += 1
        try:
            with open(fpath, "r") as f:
                content = f.read()
            cleaned = re.sub(r"//.*$", "", content, flags=re.MULTILINE)
            cleaned = re.sub(r"/\*.*?\*/", "", cleaned, flags=re.DOTALL)
            json.loads(cleaned)
            valid_count += 1
        except (json.JSONDecodeError, IOError):
            pass
    if total == 0:
        return 0.0
    # Both files must exist and be valid for full score
    if total == 2 and valid_count == 2:
        return 1.0
    elif valid_count > 0:
        return 0.5
    return 0.0


def reward() -> float:
    score = 0.0

    # Check 1: package.json exists and valid
    c1, pkg_data = check_package_json_exists_and_valid()
    score += 0.2 * c1

    # Check 2: devDependencies
    c2 = check_dev_dependencies(pkg_data)
    score += 0.2 * c2

    # Check 3: tsconfig.json settings
    c3, _ = check_tsconfig()
    score += 0.2 * c3

    # Check 4: src/index.ts with console.log
    c4 = check_index_ts()
    score += 0.2 * c4

    # Check 5: All JSON valid
    c5 = check_all_json_valid()
    score += 0.2 * c5

    return round(score, 2)


result = reward()
print(f"reward: {result}")

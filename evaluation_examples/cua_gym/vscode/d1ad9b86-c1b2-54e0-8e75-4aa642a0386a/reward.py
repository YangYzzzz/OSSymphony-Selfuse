"""
Reward Script: Rust WebAssembly project setup in VSCode
Task ID: vscode_gf6_057
Domain: vscode
Scoring:
  Component 1: Cargo.toml has cdylib/rlib and wasm-bindgen (0.20)
  Component 2: src/lib.rs has wasm_bindgen, greet(name) -> String, fibonacci(n) -> u32 (0.20)
  Component 3: pkg/ directory with .wasm and .js generated files (0.15)
  Component 4: www/index.html and www/index.js exist and import from pkg (0.15)
  Component 5: .vscode/tasks.json with WASM: Build and WASM: Serve tasks (0.15)
  Component 6: .vscode/settings.json with .wasm file association (0.15)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'rust-wasm')


def verify_task():
    """
    Verify Rust WebAssembly project setup with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Cargo.toml has crate-type=['cdylib', 'rlib'] and wasm-bindgen dependency (0.20 pts)
    try:
        cargo_path = os.path.join(PROJECT, 'Cargo.toml')
        with open(cargo_path, 'r') as f:
            cargo_content = f.read()

        has_cdylib = 'cdylib' in cargo_content
        has_rlib = 'rlib' in cargo_content
        has_wasm_bindgen = 'wasm-bindgen' in cargo_content

        if has_cdylib and has_rlib and has_wasm_bindgen:
            print(f"PASS: Component 1 — Cargo.toml has cdylib, rlib crate-types and wasm-bindgen dep (0.20 pts)")
            total_score += 0.20
        else:
            missing = []
            if not has_cdylib:
                missing.append('cdylib')
            if not has_rlib:
                missing.append('rlib')
            if not has_wasm_bindgen:
                missing.append('wasm-bindgen')
            print(f"FAIL: Component 1 — Cargo.toml missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: src/lib.rs has wasm_bindgen, greet(name: &str) -> String, fibonacci(n: u32) -> u32 (0.20 pts)
    try:
        lib_path = os.path.join(PROJECT, 'src', 'lib.rs')
        with open(lib_path, 'r') as f:
            lib_content = f.read()

        has_wasm_bindgen_import = 'wasm_bindgen' in lib_content
        has_wasm_bindgen_attr = '#[wasm_bindgen]' in lib_content
        # greet must take a name parameter (not be an empty fn greet())
        has_greet_with_param = bool(re.search(r'fn\s+greet\s*\([^)]+\)', lib_content))
        has_greet_returns_string = bool(re.search(r'fn\s+greet\s*\([^)]*\)\s*->\s*String', lib_content))
        has_fibonacci = bool(re.search(r'fn\s+fibonacci\s*\(', lib_content))

        sub_score = 0.0
        if has_wasm_bindgen_import and has_wasm_bindgen_attr:
            sub_score += 0.08
        if has_greet_with_param and has_greet_returns_string:
            sub_score += 0.06
        if has_fibonacci:
            sub_score += 0.06

        details = []
        if not has_wasm_bindgen_import:
            details.append('missing wasm_bindgen import')
        if not has_wasm_bindgen_attr:
            details.append('missing #[wasm_bindgen] attribute')
        if not has_greet_with_param:
            details.append('greet() has no parameter')
        if not has_greet_returns_string:
            details.append('greet() does not return String')
        if not has_fibonacci:
            details.append('no fibonacci function')

        if len(details) == 0:
            print(f"PASS: Component 2 — lib.rs has wasm_bindgen, greet(name)->String, fibonacci (0.20 pts)")
            total_score += 0.20
        elif sub_score > 0:
            print(f"PARTIAL: Component 2 — {', '.join(details)} (earned {sub_score:.2f})")
            total_score += sub_score  # partial credit gated by elif
        else:
            print(f"FAIL: Component 2 — lib.rs missing all wasm_bindgen features")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: pkg/ directory exists with .wasm and .js generated files (0.15 pts)
    try:
        pkg_dir = os.path.join(PROJECT, 'pkg')
        if not os.path.isdir(pkg_dir):
            print(f"FAIL: Component 3 — pkg/ directory does not exist")
        else:
            pkg_files = os.listdir(pkg_dir)
            has_wasm = any(f.endswith('.wasm') for f in pkg_files)
            has_js = any(f.endswith('.js') for f in pkg_files)

            if has_wasm and has_js:
                print(f"PASS: Component 3 — pkg/ has .wasm and .js files (0.15 pts)")
                total_score += 0.15
            else:
                missing = []
                if not has_wasm:
                    missing.append('.wasm')
                if not has_js:
                    missing.append('.js')
                print(f"FAIL: Component 3 — pkg/ missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: www/index.html and www/index.js exist and import from pkg (0.15 pts)
    try:
        www_dir = os.path.join(PROJECT, 'www')
        html_path = os.path.join(www_dir, 'index.html')
        js_path = os.path.join(www_dir, 'index.js')

        has_html = os.path.isfile(html_path)
        has_js_file = os.path.isfile(js_path)

        if not has_html or not has_js_file:
            missing = []
            if not has_html:
                missing.append('www/index.html')
            if not has_js_file:
                missing.append('www/index.js')
            print(f"FAIL: Component 4 — missing files: {', '.join(missing)}")
        else:
            with open(js_path, 'r') as f:
                js_content = f.read()
            # Check that JS imports from pkg
            imports_pkg = 'pkg' in js_content
            calls_greet = 'greet' in js_content
            calls_fibonacci = 'fibonacci' in js_content

            if imports_pkg and calls_greet and calls_fibonacci:
                print(f"PASS: Component 4 — www/index.html and www/index.js exist, JS imports from pkg and calls greet/fibonacci (0.15 pts)")
                total_score += 0.15
            else:
                details = []
                if not imports_pkg:
                    details.append('JS does not import from pkg')
                if not calls_greet:
                    details.append('JS does not reference greet')
                if not calls_fibonacci:
                    details.append('JS does not reference fibonacci')
                print(f"FAIL: Component 4 — {', '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: .vscode/tasks.json has 'WASM: Build' and 'WASM: Serve' tasks (0.15 pts)
    try:
        tasks_path = os.path.join(PROJECT, '.vscode', 'tasks.json')
        if not os.path.isfile(tasks_path):
            print(f"FAIL: Component 5 — .vscode/tasks.json does not exist")
        else:
            with open(tasks_path, 'r') as f:
                content = f.read()
            # Strip comments (JSONC)
            content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            tasks_data = json.loads(content_clean)

            task_labels = [t.get('label', '') for t in tasks_data.get('tasks', [])]
            has_build = 'WASM: Build' in task_labels
            has_serve = 'WASM: Serve' in task_labels

            # Also check that build task runs wasm-pack
            build_task = None
            for t in tasks_data.get('tasks', []):
                if t.get('label') == 'WASM: Build':
                    build_task = t
                    break
            build_runs_wasm_pack = build_task is not None and 'wasm-pack' in str(build_task.get('command', ''))

            if has_build and has_serve and build_runs_wasm_pack:
                print(f"PASS: Component 5 — tasks.json has WASM: Build (wasm-pack) and WASM: Serve tasks (0.15 pts)")
                total_score += 0.15
            else:
                details = []
                if not has_build:
                    details.append('missing WASM: Build task')
                if not has_serve:
                    details.append('missing WASM: Serve task')
                if not build_runs_wasm_pack:
                    details.append('WASM: Build does not run wasm-pack')
                print(f"FAIL: Component 5 — {', '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: .vscode/settings.json maps .wasm to a file association (0.15 pts)
    try:
        settings_path = os.path.join(PROJECT, '.vscode', 'settings.json')
        if not os.path.isfile(settings_path):
            print(f"FAIL: Component 6 — .vscode/settings.json does not exist")
        else:
            with open(settings_path, 'r') as f:
                content = f.read()
            content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            settings = json.loads(content_clean)

            file_assoc = settings.get('files.associations', {})
            wasm_value = next((v for k, v in file_assoc.items() if 'wasm' in k.lower()), None)

            if wasm_value is not None:
                print(f"PASS: Component 6 — settings.json maps .wasm to '{wasm_value}' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 6 — settings.json has no .wasm file association. Associations: {file_assoc}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

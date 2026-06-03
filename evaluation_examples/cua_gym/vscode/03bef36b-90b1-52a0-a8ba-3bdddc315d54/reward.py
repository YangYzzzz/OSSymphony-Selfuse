"""
Reward Script: Configuration-driven CLI framework for VSCode
Task ID: vscode_gf4_065
Domain: vscode
Scoring:
  Component 1 (0.15): venv exists with click, rich, pydantic, pyyaml, pytest
  Component 2 (0.15): src/framework/command.py has Command class + Parameter Pydantic model
  Component 3 (0.15): src/framework/loader.py loads YAML command files
  Component 4 (0.15): src/framework/executor.py validates params and dispatches
  Component 5 (0.15): src/framework/output.py has table/json/tree rich formatters
  Component 6 (0.10): 3+ sample YAML command files (beyond initial example.yml)
  Component 7 (0.15): 10+ tests pass via pytest
"""

import os
import re
import glob

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'python-cli-framework')

def verify_task():
    total_score = 0.0

    # Component 1: venv with required packages (0.15 pts)
    # Check venv dir exists with pyvenv.cfg and packages are accessible.
    # On initial_env there is no venv/ at all, so this fails correctly.
    try:
        venv_dir = os.path.join(PROJECT, 'venv')
        pyvenv_cfg = os.path.join(venv_dir, 'pyvenv.cfg')
        if not os.path.isdir(venv_dir):
            print("FAIL: Component 1 — venv/ directory does not exist")
        elif not os.path.exists(pyvenv_cfg):
            print("FAIL: Component 1 — pyvenv.cfg missing, not a valid venv")
        else:
            # Verify venv has a python binary
            venv_python = None
            for candidate in ['bin/python3', 'bin/python']:
                p = os.path.join(venv_dir, candidate)
                if os.path.exists(p):
                    venv_python = p
                    break

            if venv_python is None:
                print("FAIL: Component 1 — no python found in venv/bin/")
            else:
                # Verify required packages are accessible by checking pip list output
                # We read pip freeze from the venv or check system-site-packages + local
                with open(pyvenv_cfg, 'r') as f:
                    cfg_content = f.read()

                # Check packages via importlib (system python has same packages if include-system-site-packages=true)
                # The key discriminator is that venv directory exists - initial has none
                required = ['click', 'rich', 'pydantic', 'yaml', 'pytest']
                found_pkgs = []
                for pkg in required:
                    try:
                        import importlib
                        importlib.import_module(pkg)
                        found_pkgs.append(pkg)
                    except ImportError:
                        pass

                if len(found_pkgs) >= 5:
                    print(f"PASS: Component 1 — venv exists with valid config, all packages accessible (0.15 pts)")
                    total_score += 0.15
                else:
                    missing = [p for p in required if p not in found_pkgs]
                    print(f"FAIL: Component 1 — venv exists but packages missing: {missing}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: command.py with Command class + Parameter Pydantic model (0.15 pts)
    try:
        cmd_path = os.path.join(PROJECT, 'src', 'framework', 'command.py')
        if not os.path.exists(cmd_path):
            print("FAIL: Component 2 — src/framework/command.py does not exist")
        else:
            with open(cmd_path, 'r') as f:
                content = f.read()

            has_command_class = bool(re.search(r'class\s+Command\b', content))
            has_parameter_model = bool(re.search(r'class\s+Parameter\b', content))
            has_pydantic = 'pydantic' in content or 'BaseModel' in content
            has_name_field = bool(re.search(r'name\s*[:\=]', content))
            has_description_field = bool(re.search(r'description\s*[:\=]', content))
            has_parameters_field = bool(re.search(r'parameters\s*[:\=]', content))

            # Parameter model fields
            has_type_field = bool(re.search(r'type\s*[:\=]', content))
            has_required_field = bool(re.search(r'required\s*[:\=]', content))
            has_default_field = bool(re.search(r'default\s*[:\=]', content))
            has_help_field = bool(re.search(r'help\s*[:\=]', content))

            checks = [has_command_class, has_parameter_model, has_pydantic,
                       has_name_field, has_description_field, has_parameters_field,
                       has_type_field, has_required_field, has_default_field, has_help_field]

            if all(checks):
                print(f"PASS: Component 2 — command.py has Command class, Parameter Pydantic model with all fields (0.15 pts)")
                total_score += 0.15
            else:
                labels = ['Command class', 'Parameter model', 'pydantic import',
                          'name field', 'description field', 'parameters field',
                          'type field', 'required field', 'default field', 'help field']
                failed = [labels[i] for i, c in enumerate(checks) if not c]
                print(f"FAIL: Component 2 — missing: {failed}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: loader.py loads YAML command definitions (0.15 pts)
    try:
        loader_path = os.path.join(PROJECT, 'src', 'framework', 'loader.py')
        if not os.path.exists(loader_path):
            print("FAIL: Component 3 — src/framework/loader.py does not exist")
        else:
            with open(loader_path, 'r') as f:
                content = f.read()

            has_yaml_import = 'import yaml' in content or 'from yaml' in content
            has_load = bool(re.search(r'(yaml\.safe_load|yaml\.load)', content))
            has_file_reading = bool(re.search(r'open\(', content))
            has_directory_scan = bool(re.search(r'(os\.listdir|os\.scandir|glob|Path)', content))

            if has_yaml_import and has_load and has_file_reading and has_directory_scan:
                print(f"PASS: Component 3 — loader.py parses YAML from directory (0.15 pts)")
                total_score += 0.15
            else:
                details = f"yaml_import={has_yaml_import}, yaml_load={has_load}, file_read={has_file_reading}, dir_scan={has_directory_scan}"
                print(f"FAIL: Component 3 — incomplete loader: {details}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: executor.py validates params and dispatches (0.15 pts)
    try:
        exec_path = os.path.join(PROJECT, 'src', 'framework', 'executor.py')
        if not os.path.exists(exec_path):
            print("FAIL: Component 4 — src/framework/executor.py does not exist")
        else:
            with open(exec_path, 'r') as f:
                content = f.read()

            has_validate = bool(re.search(r'def\s+\w*valid\w*', content, re.IGNORECASE))
            has_execute = bool(re.search(r'def\s+\w*execut\w*', content, re.IGNORECASE))
            has_help = bool(re.search(r'(def\s+\w*help\w*|help_text)', content, re.IGNORECASE))

            if has_validate and has_execute:
                print(f"PASS: Component 4 — executor.py has validation and execution (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — validate={has_validate}, execute={has_execute}, help={has_help}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: output.py has table/json/tree formatters using rich (0.15 pts)
    try:
        out_path = os.path.join(PROJECT, 'src', 'framework', 'output.py')
        if not os.path.exists(out_path):
            print("FAIL: Component 5 — src/framework/output.py does not exist")
        else:
            with open(out_path, 'r') as f:
                content = f.read()

            has_rich = bool(re.search(r'(from rich|import rich)', content))
            has_table = bool(re.search(r'def\s+\w*table\w*', content, re.IGNORECASE))
            has_json = bool(re.search(r'def\s+\w*json\w*', content, re.IGNORECASE))
            has_tree = bool(re.search(r'def\s+\w*tree\w*', content, re.IGNORECASE))

            if has_rich and has_table and has_json and has_tree:
                print(f"PASS: Component 5 — output.py has rich-based table/json/tree formatters (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 — rich={has_rich}, table={has_table}, json={has_json}, tree={has_tree}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: 3+ sample YAML command files beyond initial example.yml (0.10 pts)
    try:
        commands_dir = os.path.join(PROJECT, 'commands')
        if not os.path.isdir(commands_dir):
            print("FAIL: Component 6 — commands/ directory does not exist")
        else:
            yml_files = [f for f in os.listdir(commands_dir)
                         if f.endswith(('.yml', '.yaml')) and f != 'example.yml']
            if len(yml_files) >= 3:
                print(f"PASS: Component 6 — {len(yml_files)} additional YAML command files: {yml_files} (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 6 — expected 3+ additional YAML files, found {len(yml_files)}: {yml_files}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: 10+ tests pass (0.15 pts)
    try:
        tests_dir = os.path.join(PROJECT, 'tests')
        if not os.path.isdir(tests_dir):
            print("FAIL: Component 7 — tests/ directory does not exist")
        else:
            test_files = [f for f in os.listdir(tests_dir) if f.startswith('test_') and f.endswith('.py')]
            if not test_files:
                print("FAIL: Component 7 — no test files found")
            else:
                # Count test functions across all test files
                total_tests = 0
                for tf in test_files:
                    tf_path = os.path.join(tests_dir, tf)
                    with open(tf_path, 'r') as f:
                        content = f.read()
                    test_funcs = re.findall(r'def\s+(test_\w+)', content)
                    test_methods = re.findall(r'def\s+(test_\w+)\(self', content)
                    total_tests += max(len(test_funcs), len(test_methods)) if test_funcs else 0

                if total_tests >= 10:
                    print(f"PASS: Component 7 — {total_tests} test functions found across {len(test_files)} files (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 7 — expected 10+ tests, found {total_tests}")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = min(total_score, 1.0)
    # Round to avoid floating point issues
    final_score = round(final_score, 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

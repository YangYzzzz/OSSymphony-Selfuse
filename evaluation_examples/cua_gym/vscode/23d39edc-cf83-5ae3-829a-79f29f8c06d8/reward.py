"""
reward.py – Verification script for vscode_gf4_026.

Checks:
  1. venv/ exists with required packages (0.2 points)
  2. src/model.py exists with ModelTrainer class and 6 methods (0.3 points)
  3. notebooks/training.ipynb is a valid Jupyter notebook with pipeline cells (0.2 points)
  4. .vscode/settings.json references venv Python interpreter (0.15 points)
  5. ModelTrainer actually works (import + basic run) (0.15 points)

Total: 1.0
"""
import json
import os
import ast
import sys

PROJECT = "/home/user/projects/python-ml-project"


def check_venv_and_packages():
    """Check venv exists and has required packages installed. (0.2 points)"""
    score = 0.0
    venv_path = os.path.join(PROJECT, "venv")
    pip_path = os.path.join(venv_path, "bin", "pip")
    python_path = os.path.join(venv_path, "bin", "python")

    if not os.path.isdir(venv_path):
        print("FAIL: venv/ directory does not exist")
        return 0.0

    if not os.path.isfile(python_path):
        print("FAIL: venv/bin/python does not exist")
        return 0.0

    print("PASS: venv/ directory exists with python binary")
    score += 0.05

    # Check installed packages
    required_packages = ["scikit-learn", "pandas", "numpy", "matplotlib", "joblib", "pytest"]
    if os.path.isfile(pip_path):
        import subprocess
        result = subprocess.run(
            [pip_path, "list", "--format=columns"],
            capture_output=True, text=True, timeout=30
        )
        installed = result.stdout.lower()

        found = 0
        for pkg in required_packages:
            # pip list shows sklearn as "scikit-learn"
            check_name = pkg.lower().replace("-", "-")
            if check_name in installed or pkg.replace("-", "_") in installed:
                found += 1
                print(f"PASS: Package '{pkg}' is installed")
            else:
                print(f"FAIL: Package '{pkg}' not found in venv")

        score += 0.15 * (found / len(required_packages))
    else:
        print("FAIL: pip not found in venv")

    return score


def check_model_py():
    """Check src/model.py exists with ModelTrainer class and 6 methods. (0.3 points)"""
    score = 0.0
    model_path = os.path.join(PROJECT, "src", "model.py")

    if not os.path.isfile(model_path):
        print("FAIL: src/model.py does not exist")
        return 0.0

    print("PASS: src/model.py exists")
    score += 0.05

    with open(model_path, "r") as f:
        content = f.read()

    # Parse AST to check class and methods
    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        print(f"FAIL: src/model.py has syntax errors: {e}")
        return score

    # Find ModelTrainer class
    model_trainer_class = None
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == "ModelTrainer":
            model_trainer_class = node
            break

    if model_trainer_class is None:
        print("FAIL: ModelTrainer class not found in src/model.py")
        return score

    print("PASS: ModelTrainer class found")
    score += 0.05

    # Check required methods
    required_methods = ["load_data", "preprocess", "train", "evaluate", "save_model", "load_model"]
    method_names = [
        node.name for node in ast.walk(model_trainer_class)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]

    found_methods = 0
    for method in required_methods:
        if method in method_names:
            print(f"PASS: Method '{method}' found in ModelTrainer")
            found_methods += 1
        else:
            print(f"FAIL: Method '{method}' not found in ModelTrainer")

    score += 0.2 * (found_methods / len(required_methods))

    # Check train method has algorithm parameter with default 'random_forest'
    for node in ast.walk(model_trainer_class):
        if isinstance(node, ast.FunctionDef) and node.name == "train":
            defaults = node.args.defaults
            args = node.args.args
            # Check for algorithm parameter
            arg_names = [a.arg for a in args if a.arg != "self"]
            if "algorithm" in arg_names:
                print("PASS: train() has 'algorithm' parameter")
            else:
                print("FAIL: train() missing 'algorithm' parameter")
            break

    return score


def check_notebook():
    """Check notebooks/training.ipynb exists and is valid. (0.2 points)"""
    score = 0.0
    nb_path = os.path.join(PROJECT, "notebooks", "training.ipynb")

    if not os.path.isfile(nb_path):
        print("FAIL: notebooks/training.ipynb does not exist")
        return 0.0

    print("PASS: notebooks/training.ipynb exists")
    score += 0.05

    try:
        with open(nb_path, "r") as f:
            nb = json.load(f)
    except (json.JSONDecodeError, Exception) as e:
        print(f"FAIL: training.ipynb is not valid JSON: {e}")
        return score

    # Check it's a valid notebook
    if nb.get("nbformat", 0) < 4:
        print("FAIL: Invalid notebook format (nbformat < 4)")
        return score

    cells = nb.get("cells", [])
    if len(cells) < 3:
        print(f"FAIL: Notebook has only {len(cells)} cells, expected at least 3")
        return score

    print(f"PASS: Valid Jupyter notebook with {len(cells)} cells")
    score += 0.05

    # Check for key pipeline steps in code cells
    code_sources = []
    for cell in cells:
        if cell.get("cell_type") == "code":
            src = "".join(cell.get("source", []))
            code_sources.append(src)

    all_code = "\n".join(code_sources)

    pipeline_checks = {
        "data loading": "load_data" in all_code,
        "preprocessing": "preprocess" in all_code,
        "training": "train" in all_code,
        "evaluation": "evaluate" in all_code or "eval" in all_code,
    }

    found_steps = sum(1 for v in pipeline_checks.values() if v)
    for step, found in pipeline_checks.items():
        if found:
            print(f"PASS: Notebook contains {step} step")
        else:
            print(f"FAIL: Notebook missing {step} step")

    score += 0.1 * (found_steps / len(pipeline_checks))

    return score


def check_vscode_settings():
    """Check .vscode/settings.json references venv. (0.15 points)"""
    score = 0.0
    settings_path = os.path.join(PROJECT, ".vscode", "settings.json")

    if not os.path.isfile(settings_path):
        print("FAIL: .vscode/settings.json does not exist")
        return 0.0

    print("PASS: .vscode/settings.json exists")
    score += 0.05

    try:
        with open(settings_path, "r") as f:
            content = f.read()
        # Handle JSONC (comments)
        import re
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        settings = json.loads(content)
    except Exception as e:
        print(f"FAIL: Could not parse .vscode/settings.json: {e}")
        return score

    # Check for venv reference in any setting
    settings_str = json.dumps(settings).lower()
    if "venv" in settings_str:
        print("PASS: Settings reference venv")
        score += 0.05
    else:
        print("FAIL: Settings do not reference venv")

    # Check for Jupyter/Python interpreter config
    jupyter_related = False
    for key in settings:
        key_lower = key.lower()
        if "jupyter" in key_lower or ("python" in key_lower and "interpreter" in key_lower):
            jupyter_related = True
            break
        if "python.defaultinterpreterpath" == key_lower:
            jupyter_related = True
            break

    # Also check common settings keys
    if any(k in settings for k in [
        "python.defaultInterpreterPath",
        "jupyter.notebookFileRoot",
        "python.pythonPath",
        "jupyter.kernels.filter",
    ]):
        jupyter_related = True

    if jupyter_related:
        print("PASS: Settings configure Python/Jupyter interpreter")
        score += 0.05
    else:
        print("FAIL: No Jupyter/Python interpreter configuration found")

    return score


def check_model_works():
    """Try to import and run ModelTrainer. (0.15 points)"""
    score = 0.0
    venv_python = os.path.join(PROJECT, "venv", "bin", "python")

    if not os.path.isfile(venv_python):
        print("FAIL: venv python not available for model test")
        return 0.0

    # Run a test script using the venv python
    test_script = f'''
import sys
sys.path.insert(0, "{PROJECT}/src")
sys.path.insert(0, "{PROJECT}")
try:
    from model import ModelTrainer
    trainer = ModelTrainer()
    data = trainer.load_data("{PROJECT}/data/iris.csv")
    assert data is not None, "load_data returned None"
    print("LOAD_OK")

    trainer.preprocess("species")
    print("PREPROCESS_OK")

    trainer.train(algorithm="random_forest")
    print("TRAIN_OK")

    results = trainer.evaluate()
    assert "accuracy" in results, "evaluate missing accuracy"
    assert "f1" in results, "evaluate missing f1"
    assert results["accuracy"] > 0.5, f"accuracy too low: {{results['accuracy']}}"
    print("EVALUATE_OK")

    trainer.save_model("/tmp/test_model.joblib")
    print("SAVE_OK")

    trainer2 = ModelTrainer()
    trainer2.load_model("/tmp/test_model.joblib")
    print("LOAD_MODEL_OK")
except Exception as e:
    print(f"ERROR: {{e}}")
'''

    import subprocess
    try:
        result = subprocess.run(
            [venv_python, "-c", test_script],
            capture_output=True, text=True, timeout=60,
            cwd=PROJECT,
        )
        output = result.stdout + result.stderr

        checks = {
            "LOAD_OK": 0.025,
            "PREPROCESS_OK": 0.025,
            "TRAIN_OK": 0.025,
            "EVALUATE_OK": 0.025,
            "SAVE_OK": 0.025,
            "LOAD_MODEL_OK": 0.025,
        }

        for check, points in checks.items():
            if check in output:
                print(f"PASS: ModelTrainer {check}")
                score += points
            else:
                print(f"FAIL: ModelTrainer {check}")

    except subprocess.TimeoutExpired:
        print("FAIL: Model test timed out")
    except Exception as e:
        print(f"FAIL: Model test error: {e}")

    return score


def main():
    total_score = 0.0

    print("=" * 60)
    print("Reward Verification for vscode_gf4_026")
    print("=" * 60)

    # Component 1: venv and packages (0.2)
    print("\n--- Component 1: Virtual Environment & Packages (0.2) ---")
    try:
        s = check_venv_and_packages()
        total_score += s
        print(f"Component 1 score: {s:.3f}")
    except Exception as e:
        print(f"ERROR in Component 1: {e}")

    # Component 2: model.py (0.3)
    print("\n--- Component 2: src/model.py (0.3) ---")
    try:
        s = check_model_py()
        total_score += s
        print(f"Component 2 score: {s:.3f}")
    except Exception as e:
        print(f"ERROR in Component 2: {e}")

    # Component 3: notebook (0.2)
    print("\n--- Component 3: notebooks/training.ipynb (0.2) ---")
    try:
        s = check_notebook()
        total_score += s
        print(f"Component 3 score: {s:.3f}")
    except Exception as e:
        print(f"ERROR in Component 3: {e}")

    # Component 4: .vscode/settings.json (0.15)
    print("\n--- Component 4: .vscode/settings.json (0.15) ---")
    try:
        s = check_vscode_settings()
        total_score += s
        print(f"Component 4 score: {s:.3f}")
    except Exception as e:
        print(f"ERROR in Component 4: {e}")

    # Component 5: Model actually works (0.15)
    print("\n--- Component 5: ModelTrainer Functional Test (0.15) ---")
    try:
        s = check_model_works()
        total_score += s
        print(f"Component 5 score: {s:.3f}")
    except Exception as e:
        print(f"ERROR in Component 5: {e}")

    # Clamp to [0.0, 1.0]
    total_score = max(0.0, min(1.0, total_score))

    print("\n" + "=" * 60)
    print(f"REWARD: {total_score:.1f}")


if __name__ == "__main__":
    main()

"""
Initial Setup: Configure a Dev Container with multiple features
Task ID: vscode_rrt_030
Domain: vs_code

Creates a realistic CI tools project directory and opens it in VSCode.
No .devcontainer folder exists yet - that is the task for the agent.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'ci-tools')


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_project():
    # Create the ci-tools project directory structure
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'tests'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, '.github', 'workflows'), exist_ok=True)

    # Create a realistic Dockerfile
    dockerfile_content = """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY tests/ ./tests/

CMD ["python", "-m", "pytest", "tests/"]
"""
    with open(os.path.join(PROJECT_DIR, 'Dockerfile'), 'w') as f:
        f.write(dockerfile_content)

    # Create requirements.txt
    requirements_content = """pytest==7.4.3
requests==2.31.0
pyyaml==6.0.1
click==8.1.7
docker==7.0.0
"""
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write(requirements_content)

    # Create main CI pipeline runner
    main_py = """#!/usr/bin/env python3
\"\"\"CI Tools - Pipeline Runner

A lightweight CI pipeline runner for local development and testing.
Supports Docker-based build steps, GitHub integration, and parallel execution.
\"\"\"

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

import yaml


class PipelineRunner:
    \"\"\"Execute CI pipeline steps defined in pipeline.yaml.\"\"\"

    def __init__(self, config_path: str = "pipeline.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        self.results = []

    def _load_config(self) -> dict:
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def run_step(self, step_name: str, command: str, docker_image: str = None) -> bool:
        print(f"[STEP] Running: {step_name}")
        if docker_image:
            full_cmd = f"docker run --rm {docker_image} {command}"
        else:
            full_cmd = command

        result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
        success = result.returncode == 0
        self.results.append({
            "step": step_name,
            "success": success,
            "output": result.stdout,
            "error": result.stderr
        })
        status = "PASS" if success else "FAIL"
        print(f"  [{status}] {step_name}")
        return success

    def run_pipeline(self) -> bool:
        steps = self.config.get("steps", [])
        all_passed = True
        for step in steps:
            if not self.run_step(step["name"], step["command"], step.get("image")):
                all_passed = False
                if step.get("fail_fast", False):
                    print("[ABORT] fail_fast triggered")
                    break
        return all_passed

    def generate_report(self, output_path: str = "ci-report.json"):
        report = {
            "pipeline": self.config.get("name", "unnamed"),
            "total_steps": len(self.results),
            "passed": sum(1 for r in self.results if r["success"]),
            "failed": sum(1 for r in self.results if not r["success"]),
            "results": self.results
        }
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"Report saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="CI Tools Pipeline Runner")
    parser.add_argument("--config", default="pipeline.yaml", help="Pipeline config file")
    parser.add_argument("--report", default="ci-report.json", help="Output report path")
    parser.add_argument("--step", help="Run a single step by name")
    args = parser.parse_args()

    runner = PipelineRunner(args.config)
    success = runner.run_pipeline()
    runner.generate_report(args.report)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
"""
    with open(os.path.join(PROJECT_DIR, 'src', 'pipeline_runner.py'), 'w') as f:
        f.write(main_py)

    # Create a GitHub Actions workflow
    workflow_content = """name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install flake8
      - run: flake8 src/ tests/

  test:
    needs: lint
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v --tb=short

  docker-build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t ci-tools:test .
      - run: docker run --rm ci-tools:test python -c "print('Container OK')"
"""
    with open(os.path.join(PROJECT_DIR, '.github', 'workflows', 'ci.yml'), 'w') as f:
        f.write(workflow_content)

    # Create pipeline config
    pipeline_yaml = """name: ci-tools-pipeline
steps:
  - name: lint
    command: flake8 src/ tests/
    fail_fast: true
  - name: unit-tests
    command: pytest tests/ -v
  - name: docker-build
    command: docker build -t ci-tools:latest .
    image: null
  - name: integration-test
    command: pytest tests/integration/ -v --timeout=60
"""
    with open(os.path.join(PROJECT_DIR, 'pipeline.yaml'), 'w') as f:
        f.write(pipeline_yaml)

    # Create test files
    test_runner_py = """import pytest
from unittest.mock import patch, MagicMock
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestPipelineRunner:
    def test_load_config(self, tmp_path):
        config_file = tmp_path / "pipeline.yaml"
        config_file.write_text("name: test\\nsteps: []\\n")
        from pipeline_runner import PipelineRunner
        runner = PipelineRunner(str(config_file))
        assert runner.config["name"] == "test"

    def test_run_step_success(self):
        from pipeline_runner import PipelineRunner
        runner = PipelineRunner.__new__(PipelineRunner)
        runner.results = []
        assert runner.run_step("echo test", "echo hello") is True
        assert len(runner.results) == 1
        assert runner.results[0]["success"] is True

    def test_generate_report(self, tmp_path):
        from pipeline_runner import PipelineRunner
        runner = PipelineRunner.__new__(PipelineRunner)
        runner.config = {"name": "test-pipeline"}
        runner.results = [{"step": "test", "success": True, "output": "", "error": ""}]
        report_path = str(tmp_path / "report.json")
        runner.generate_report(report_path)
        with open(report_path) as f:
            report = json.load(f)
        assert report["passed"] == 1
        assert report["failed"] == 0
"""
    with open(os.path.join(PROJECT_DIR, 'tests', 'test_pipeline_runner.py'), 'w') as f:
        f.write(test_runner_py)

    # Create a README
    readme = """# CI Tools

A lightweight CI pipeline runner for local development and testing.

## Features

- Docker-based build steps
- GitHub Actions integration
- Parallel execution support
- JSON report generation

## Quick Start

```bash
pip install -r requirements.txt
python src/pipeline_runner.py --config pipeline.yaml
```

## Development

```bash
pytest tests/ -v
```
"""
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write(readme)

    # Create .gitignore
    gitignore = """__pycache__/
*.pyc
.pytest_cache/
ci-report.json
.env
*.egg-info/
dist/
build/
"""
    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write(gitignore)

    # Ensure NO .devcontainer folder exists (the task is to create it)
    devcontainer_dir = os.path.join(PROJECT_DIR, '.devcontainer')
    if os.path.exists(devcontainer_dir):
        import shutil
        shutil.rmtree(devcontainer_dir)

    print(f'Project created: {PROJECT_DIR}')
    print('Files:')
    for root, dirs, files in os.walk(PROJECT_DIR):
        level = root.replace(PROJECT_DIR, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f'{subindent}{file}')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with ci-tools project')


create_project()

"""
Reward Script: Java Spring Boot project workflow setup in VSCode
Task ID: vscode_wf_056
Domain: vscode (libreoffice_calc domain label, but actually VSCode task)
Scoring:
  1. Java Extension Pack installed (0.15)
  2. Project directory structure created (0.15)
  3. DemoApplication.java with proper annotations (0.15)
  4. HelloController.java with REST endpoint (0.15)
  5. launch.json with Spring Boot debug config (0.15)
  6. tasks.json with Maven build/test/run tasks (0.15)
  7. settings.json with Java runtime and formatting (0.10)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'project')
TASK_ID = 'vscode_wf_056'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Java Extension Pack installed (0.15 points)
    # Check via filesystem: ~/.vscode/extensions/ contains vscjava.vscode-java-pack-*
    # Initial env has NO extensions dir entries; golden env has the pack installed.
    try:
        ext_dir = os.path.join(WORKDIR, '.vscode', 'extensions')
        matching_exts = []
        if os.path.isdir(ext_dir):
            matching_exts = [e for e in os.listdir(ext_dir) if e.lower().startswith('vscjava.vscode-java-pack')]
        if len(matching_exts) > 0:
            print("PASS: Component 1 - Java Extension Pack is installed (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 - vscjava.vscode-java-pack not found in {ext_dir}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Project directory structure (0.15 points)
    # Checks that src/main/java/com/example/demo/, src/main/resources/, src/test/ exist.
    # Initial env has NONE of these; golden env has them all.
    try:
        dirs_to_check = [
            os.path.join(PROJECT, 'src', 'main', 'java', 'com', 'example', 'demo'),
            os.path.join(PROJECT, 'src', 'main', 'resources'),
            os.path.join(PROJECT, 'src', 'test'),
        ]
        dirs_found = sum(1 for d in dirs_to_check if os.path.isdir(d))
        if dirs_found == len(dirs_to_check):
            print(f"PASS: Component 2 - All {len(dirs_to_check)} project directories exist (0.15 pts)")
            total_score += 0.15
        else:
            missing = [d for d in dirs_to_check if not os.path.isdir(d)]
            print(f"FAIL: Component 2 - Missing directories: {missing} ({dirs_found}/{len(dirs_to_check)} found)")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: DemoApplication.java with proper content (0.15 points)
    # Must have @SpringBootApplication annotation and main method with SpringApplication.run
    # Initial env has no such file; golden env has it.
    try:
        demo_path = os.path.join(PROJECT, 'src', 'main', 'java', 'com', 'example', 'demo', 'DemoApplication.java')
        if os.path.isfile(demo_path):
            with open(demo_path, 'r') as f:
                content = f.read()
            has_annotation = '@SpringBootApplication' in content
            has_main = 'public static void main' in content
            has_run = 'SpringApplication.run' in content
            if has_annotation and has_main and has_run:
                print("PASS: Component 3 - DemoApplication.java has @SpringBootApplication, main method, SpringApplication.run (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 - DemoApplication.java missing: annotation={has_annotation}, main={has_main}, run={has_run}")
        else:
            print(f"FAIL: Component 3 - DemoApplication.java not found at {demo_path}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: HelloController.java with REST endpoint (0.15 points)
    # Must have @RestController and @GetMapping annotations
    # Initial env has no such file; golden env has it.
    try:
        controller_path = os.path.join(PROJECT, 'src', 'main', 'java', 'com', 'example', 'demo', 'HelloController.java')
        if os.path.isfile(controller_path):
            with open(controller_path, 'r') as f:
                content = f.read()
            has_rest_controller = '@RestController' in content
            has_get_mapping = '@GetMapping' in content
            if has_rest_controller and has_get_mapping:
                print("PASS: Component 4 - HelloController.java has @RestController and @GetMapping (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 - HelloController.java missing: @RestController={has_rest_controller}, @GetMapping={has_get_mapping}")
        else:
            print(f"FAIL: Component 4 - HelloController.java not found at {controller_path}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: launch.json with Spring Boot debug config (0.15 points)
    # Must have type=java and mainClass referencing DemoApplication
    # Initial env has no .vscode dir; golden env has launch.json.
    try:
        launch_path = os.path.join(PROJECT, '.vscode', 'launch.json')
        if os.path.isfile(launch_path):
            with open(launch_path, 'r') as f:
                raw = f.read()
            # Strip comments for JSONC compatibility
            cleaned = re.sub(r'//.*$', '', raw, flags=re.MULTILINE)
            launch = json.loads(cleaned)
            configs = launch.get('configurations', [])
            matching_configs = [
                cfg for cfg in configs
                if cfg.get('type') == 'java' and 'DemoApplication' in cfg.get('mainClass', '')
            ]
            if len(matching_configs) > 0:
                print("PASS: Component 5 - launch.json has Spring Boot Java debug config (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 - launch.json missing Java debug config for DemoApplication. Configs: {configs}")
        else:
            print(f"FAIL: Component 5 - launch.json not found at {launch_path}")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: tasks.json with Maven tasks (0.15 points)
    # Must have tasks for 'mvn clean install', 'mvn test', 'mvn spring-boot:run'
    # Initial env has no .vscode dir; golden env has tasks.json.
    try:
        tasks_path = os.path.join(PROJECT, '.vscode', 'tasks.json')
        if os.path.isfile(tasks_path):
            with open(tasks_path, 'r') as f:
                raw = f.read()
            cleaned = re.sub(r'//.*$', '', raw, flags=re.MULTILINE)
            tasks_json = json.loads(cleaned)
            tasks = tasks_json.get('tasks', [])
            # Check for the three required Maven commands
            task_commands = []
            for t in tasks:
                cmd = t.get('command', '') or ''
                label = t.get('label', '') or ''
                task_commands.append(cmd.lower())
                task_commands.append(label.lower())
            required = ['mvn clean install', 'mvn test', 'mvn spring-boot:run']
            found = []
            for req in required:
                if any(req in tc for tc in task_commands):
                    found.append(req)
            if len(found) == len(required):
                print(f"PASS: Component 6 - tasks.json has all 3 Maven tasks (0.15 pts)")
                total_score += 0.15
            else:
                missing = [r for r in required if r not in found]
                print(f"FAIL: Component 6 - tasks.json missing Maven tasks: {missing}")
        else:
            print(f"FAIL: Component 6 - tasks.json not found at {tasks_path}")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    # Component 7: settings.json with Java runtime and formatting settings (0.10 points)
    # Must have java.configuration.runtimes and formatting-related settings
    # Initial env has no .vscode dir; golden env has settings.json.
    try:
        settings_path = os.path.join(PROJECT, '.vscode', 'settings.json')
        if os.path.isfile(settings_path):
            with open(settings_path, 'r') as f:
                raw = f.read()
            cleaned = re.sub(r'//.*$', '', raw, flags=re.MULTILINE)
            settings = json.loads(cleaned)
            has_runtimes = 'java.configuration.runtimes' in settings and len(settings['java.configuration.runtimes']) > 0
            # Check for any formatting-related setting
            format_keys = [k for k in settings.keys() if 'format' in k.lower() or 'saveAction' in k or 'formatOnSave' in k.lower()]
            has_formatting = len(format_keys) > 0 or settings.get('editor.formatOnSave') is not None
            if has_runtimes and has_formatting:
                print(f"PASS: Component 7 - settings.json has Java runtimes and formatting config (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 7 - settings.json missing: runtimes={has_runtimes}, formatting={has_formatting}")
        else:
            print(f"FAIL: Component 7 - settings.json not found at {settings_path}")
    except Exception as e:
        print(f"ERROR: Component 7 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

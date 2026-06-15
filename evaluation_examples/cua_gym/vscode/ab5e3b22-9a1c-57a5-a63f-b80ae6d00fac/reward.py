"""
Reward Script: Terraform infrastructure development workflow in VSCode
Task ID: vscode_wf_087
Domain: vscode
Scoring:
  C1: hashicorp.terraform extension installed (0.10)
  C2: main.tf has AWS provider + EC2 instance resource (0.20)
  C3: variables.tf has region, instance_type, ami_id (0.15)
  C4: outputs.tf has instance_id, public_ip outputs (0.15)
  C5: settings.json has terraform formatting/validation (0.15)
  C6: tasks.json has all 5 terraform tasks (0.15)
  C7: tf-apply dependsOn tf-plan (0.05)
  C8: launch.json has terraform debug with verbose logging (0.05)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'project')
VSCODE_DIR = os.path.join(PROJECT, '.vscode')
TASK_ID = 'vscode_wf_087'


def check_extension_installed():
    """Check if hashicorp.terraform extension is installed by scanning extensions directory."""
    try:
        ext_dir = os.path.join(WORKDIR, '.vscode', 'extensions')
        if not os.path.isdir(ext_dir):
            return False
        for entry in os.listdir(ext_dir):
            if entry.lower().startswith('hashicorp.terraform'):
                return True
        return False
    except Exception:
        return False


def load_json_file(path):
    """Load a JSON file, handling JSONC (comments)."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip single-line comments for JSONC compatibility
        cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(cleaned)
    except Exception:
        return None


def verify_task():
    """Verify task completion with progressive scoring."""
    total_score = 0.0

    # Component 1: hashicorp.terraform extension installed (0.10 points)
    try:
        if check_extension_installed():
            print("PASS: Component 1 -- hashicorp.terraform extension is installed (0.10 pts)")
            total_score += 0.10
        else:
            print("FAIL: Component 1 -- hashicorp.terraform extension not found")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: main.tf has AWS provider and EC2 instance resource (0.20 points)
    try:
        main_tf_path = os.path.join(PROJECT, 'main.tf')
        if os.path.isfile(main_tf_path):
            with open(main_tf_path, 'r') as f:
                content = f.read().lower()
            has_provider = 'provider' in content and 'aws' in content
            has_ec2 = 'aws_instance' in content
            if has_provider and has_ec2:
                print("PASS: Component 2 -- main.tf has AWS provider and EC2 instance resource (0.20 pts)")
                total_score += 0.20
            elif has_provider:
                print("PARTIAL: Component 2 -- main.tf has AWS provider but no EC2 resource (0.10 pts)")
                total_score += 0.10
            elif has_ec2:
                print("PARTIAL: Component 2 -- main.tf has EC2 resource but no AWS provider (0.10 pts)")
                total_score += 0.10
            else:
                print("FAIL: Component 2 -- main.tf missing AWS provider and EC2 resource")
        else:
            print("FAIL: Component 2 -- main.tf does not exist")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: variables.tf has region, instance_type, ami_id variables (0.15 points)
    try:
        var_path = os.path.join(PROJECT, 'variables.tf')
        if os.path.isfile(var_path):
            with open(var_path, 'r') as f:
                content = f.read()
            # Parse variable blocks
            var_blocks = re.findall(r'variable\s+"([^"]+)"', content)
            required_vars = {'region', 'instance_type', 'ami_id'}
            found_vars = required_vars.intersection(set(var_blocks))
            if found_vars == required_vars:
                print(f"PASS: Component 3 -- variables.tf has all 3 required variables: {found_vars} (0.15 pts)")
                total_score += 0.15
            elif len(found_vars) > 0:
                pts = round(0.15 * len(found_vars) / 3, 2)
                print(f"PARTIAL: Component 3 -- variables.tf has {found_vars}, missing {required_vars - found_vars} ({pts} pts)")
                total_score += pts
            else:
                print(f"FAIL: Component 3 -- variables.tf has no required variable definitions. Found blocks: {var_blocks}")
        else:
            print("FAIL: Component 3 -- variables.tf does not exist")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: outputs.tf has instance_id and public_ip outputs (0.15 points)
    try:
        out_path = os.path.join(PROJECT, 'outputs.tf')
        if os.path.isfile(out_path):
            with open(out_path, 'r') as f:
                content = f.read()
            output_blocks = re.findall(r'output\s+"([^"]+)"', content)
            required_outputs = {'instance_id', 'public_ip'}
            found_outputs = required_outputs.intersection(set(output_blocks))
            if found_outputs == required_outputs:
                print(f"PASS: Component 4 -- outputs.tf has both required outputs: {found_outputs} (0.15 pts)")
                total_score += 0.15
            elif len(found_outputs) > 0:
                pts = round(0.15 * len(found_outputs) / 2, 2)
                print(f"PARTIAL: Component 4 -- outputs.tf has {found_outputs}, missing {required_outputs - found_outputs} ({pts} pts)")
                total_score += pts
            else:
                print(f"FAIL: Component 4 -- outputs.tf has no required output definitions. Found: {output_blocks}")
        else:
            print("FAIL: Component 4 -- outputs.tf does not exist")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: .vscode/settings.json has terraform formatting/validation (0.15 points)
    try:
        settings_path = os.path.join(VSCODE_DIR, 'settings.json')
        settings = load_json_file(settings_path)
        if settings is not None:
            c5_score = 0.0
            # Check formatOnSave for terraform
            tf_settings = settings.get('[terraform]', {})
            if tf_settings.get('editor.formatOnSave') or settings.get('editor.formatOnSave'):
                c5_score += 0.05
                print("  C5a: formatOnSave enabled for terraform")
            else:
                print("  C5a FAIL: formatOnSave not enabled for terraform")

            # Check terraform formatter
            if tf_settings.get('editor.defaultFormatter') == 'hashicorp.terraform' or \
               settings.get('editor.defaultFormatter') == 'hashicorp.terraform':
                c5_score += 0.05
                print("  C5b: terraform formatter configured")
            else:
                print("  C5b FAIL: terraform formatter not configured")

            # Check validation on save
            if settings.get('terraform.experimentalFeatures.validateOnSave') or \
               settings.get('terraform.languageServer.enable'):
                c5_score += 0.05
                print("  C5c: terraform validation/language server enabled")
            else:
                print("  C5c FAIL: terraform validation not enabled")

            if c5_score > 0:
                print(f"PASS: Component 5 -- settings.json terraform config ({c5_score} pts)")
                total_score += c5_score
            else:
                print("FAIL: Component 5 -- settings.json missing terraform configuration")
        else:
            print("FAIL: Component 5 -- .vscode/settings.json not found or invalid")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: tasks.json has all 5 terraform tasks (0.15 points)
    try:
        tasks_path = os.path.join(VSCODE_DIR, 'tasks.json')
        tasks_data = load_json_file(tasks_path)
        if tasks_data is not None:
            task_labels = [t.get('label', '') for t in tasks_data.get('tasks', [])]
            required_tasks = {'tf-init', 'tf-plan', 'tf-apply', 'tf-destroy', 'tf-fmt'}
            found_tasks = required_tasks.intersection(set(task_labels))
            if found_tasks == required_tasks:
                print(f"PASS: Component 6 -- tasks.json has all 5 required tasks (0.15 pts)")
                total_score += 0.15
            elif len(found_tasks) > 0:
                pts = round(0.15 * len(found_tasks) / 5, 2)
                print(f"PARTIAL: Component 6 -- tasks.json has {found_tasks}, missing {required_tasks - found_tasks} ({pts} pts)")
                total_score += pts
            else:
                print(f"FAIL: Component 6 -- tasks.json has no required task labels. Found: {task_labels}")
        else:
            print("FAIL: Component 6 -- .vscode/tasks.json not found or invalid")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    # Component 7: tf-apply dependsOn tf-plan (0.05 points)
    try:
        tasks_path = os.path.join(VSCODE_DIR, 'tasks.json')
        tasks_data = load_json_file(tasks_path)
        if tasks_data is not None:
            apply_task = None
            for t in tasks_data.get('tasks', []):
                if t.get('label') == 'tf-apply':
                    apply_task = t
                    break
            if apply_task is not None:
                depends = apply_task.get('dependsOn', '')
                # dependsOn can be a string or list
                if isinstance(depends, str):
                    depends_list = [depends]
                elif isinstance(depends, list):
                    depends_list = depends
                else:
                    depends_list = []
                if 'tf-plan' in depends_list:
                    print("PASS: Component 7 -- tf-apply dependsOn tf-plan (0.05 pts)")
                    total_score += 0.05
                else:
                    print(f"FAIL: Component 7 -- tf-apply dependsOn is {depends}, expected tf-plan")
            else:
                print("FAIL: Component 7 -- tf-apply task not found")
        else:
            print("FAIL: Component 7 -- tasks.json not found or invalid")
    except Exception as e:
        print(f"ERROR: Component 7 -- {e}")

    # Component 8: launch.json has terraform debug config with verbose logging (0.05 points)
    try:
        launch_path = os.path.join(VSCODE_DIR, 'launch.json')
        launch_data = load_json_file(launch_path)
        if launch_data is not None:
            configs = launch_data.get('configurations', [])
            debug_config_found = any(
                'terraform' in json.dumps(cfg).lower()
                and ('trace' in json.dumps(cfg).lower() or 'verbose' in json.dumps(cfg).lower()
                     or 'debug' in json.dumps(cfg).lower() or 'tf_log' in json.dumps(cfg).lower())
                for cfg in configs
            )
            if debug_config_found:
                print("PASS: Component 8 -- launch.json has terraform debug with verbose logging (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 8 -- launch.json missing terraform debug config with verbose logging. Configs: {configs}")
        else:
            print("FAIL: Component 8 -- .vscode/launch.json not found or invalid")
    except Exception as e:
        print(f"ERROR: Component 8 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()

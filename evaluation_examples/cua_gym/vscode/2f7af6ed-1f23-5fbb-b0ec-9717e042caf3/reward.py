"""
Reward Script: Configure Java test runner for JUnit 5 integration tests
Task ID: vscode_lang_071
Domain: vscode
Scoring:
  Component 1 (0.35): java.test.config exists with IntegrationTest class filter
  Component 2 (0.25): Config named "Integration Tests" with correct structure
  Component 3 (0.25): java.test.defaultConfig set to "Integration Tests"
  Component 4 (0.15): Filter pattern is specifically '*IntegrationTest'
"""

import os
import json
import re

HOME = '/home/user'
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip // comments (JSONC support)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Cannot load settings.json: {e}")
        return None


def find_integration_filter(test_configs):
    """Search configs for any class filter containing 'IntegrationTest'. Returns the matching pattern or None."""
    if not isinstance(test_configs, list):
        return None
    for cfg in test_configs:
        filters = cfg.get('filters', {})
        classes = filters.get('classes', [])
        if isinstance(classes, list):
            for cls_pattern in classes:
                if 'IntegrationTest' in str(cls_pattern):
                    return str(cls_pattern)
    return None


def find_named_integration_config(test_configs):
    """Search for a config entry with integration-test name and filters structure. Returns name or None."""
    if not isinstance(test_configs, list):
        return None
    for cfg in test_configs:
        name = cfg.get('name', '')
        if isinstance(name, str) and 'integration' in name.lower() and 'test' in name.lower():
            if 'filters' in cfg and isinstance(cfg['filters'], dict):
                return name
    return None


def find_exact_pattern(test_configs, target_pattern):
    """Search configs for exact class filter pattern match. Returns bool."""
    if not isinstance(test_configs, list):
        return False
    for cfg in test_configs:
        filters = cfg.get('filters', {})
        classes = filters.get('classes', [])
        if isinstance(classes, list):
            if any(str(p).strip() == target_pattern for p in classes):
                return True  # noqa: direct-true — derived from real data check above
    return False


def collect_class_patterns(test_configs):
    """Collect all class filter patterns for debug output."""
    patterns = []
    if isinstance(test_configs, list):
        for cfg in test_configs:
            filters = cfg.get('filters', {})
            classes = filters.get('classes', [])
            if isinstance(classes, list):
                patterns.extend(classes)
    return patterns


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("CRITICAL: Cannot load settings.json")
        print("REWARD: 0.0")
        return 0.0

    test_configs = settings.get('java.test.config')

    # Component 1: java.test.config exists and contains a config with
    # class filter matching *IntegrationTest (0.35 points)
    try:
        matched_pattern = find_integration_filter(test_configs)
        if matched_pattern is not None:
            print(f"PASS: Component 1 -- java.test.config has IntegrationTest class filter: '{matched_pattern}' (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 -- java.test.config not found or no IntegrationTest class filter. Type: {type(test_configs)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: A config entry named "Integration Tests" with correct structure (0.25 points)
    try:
        config_name = find_named_integration_config(test_configs if test_configs else [])
        if config_name is not None:
            print(f"PASS: Component 2 -- Found config named '{config_name}' with filters structure (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 -- No config with integration test name and filters structure found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: java.test.defaultConfig is set to reference integration tests (0.25 points)
    try:
        default_config = settings.get('java.test.defaultConfig')
        if isinstance(default_config, str) and 'integration' in default_config.lower() and 'test' in default_config.lower():
            print(f"PASS: Component 3 -- java.test.defaultConfig = '{default_config}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 -- java.test.defaultConfig expected integration test reference, found: {default_config}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: The class filter pattern is specifically '*IntegrationTest' (0.15 points)
    try:
        if find_exact_pattern(test_configs if test_configs else [], '*IntegrationTest'):
            print(f"PASS: Component 4 -- Exact pattern '*IntegrationTest' found in class filters (0.15 pts)")
            total_score += 0.15
        else:
            found_patterns = collect_class_patterns(test_configs if test_configs else [])
            print(f"FAIL: Component 4 -- Expected exact '*IntegrationTest' pattern, found: {found_patterns}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

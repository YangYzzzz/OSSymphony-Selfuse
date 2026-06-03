"""
Reward Script: Set up auto-caption for images with 'Figure' category and sequential numbering
Task ID: writer_tech_077
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): Graphic AutoCaption is enabled
  Component 2 (0.35): Category is set to 'Figure'
  Component 3 (0.15): Numbering is set to Arabic (sequential: value 0) or similar sequential type
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_tech_077'
CONFIG_PATH = os.path.expanduser(
    '~/.config/libreoffice/4/user/registrymodifications.xcu'
)
# Fallback: check common user path directly
ALT_CONFIG_PATH = '/home/user/.config/libreoffice/4/user/registrymodifications.xcu'


def verify_task():
    """
    Verify that LibreOffice Writer AutoCaption is configured for images
    with category 'Figure' and sequential numbering.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Determine config file path
    config_path = None
    for p in [CONFIG_PATH, ALT_CONFIG_PATH]:
        if os.path.exists(p):
            config_path = p
            break

    if config_path is None:
        print(f"CRITICAL: Cannot find registrymodifications.xcu")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read config file: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse relevant settings from the XCU file
    # We look for WriterObject/Graphic entries specifically

    # Component 1: Graphic AutoCaption is enabled (0.5 points)
    # In initial_env this is 'false', in golden_env this should be 'true'
    try:
        # Match the Enable property for Graphic specifically
        enable_pattern = r'<item oor:path="/org\.openoffice\.Office\.Writer/Insert/Caption/WriterObject/Graphic"><prop oor:name="Enable"[^>]*><value>(true|false)</value>'
        enable_match = re.search(enable_pattern, config_content)

        if enable_match:
            enable_value = enable_match.group(1)
            if enable_value == 'true':
                print(f"PASS: Component 1 — Graphic AutoCaption is enabled (0.5 pts)")
                total_score += 0.5
            else:
                print(f"FAIL: Component 1 — Graphic AutoCaption is disabled (Enable={enable_value})")
        else:
            # Try a more flexible pattern
            if 'WriterObject/Graphic' in config_content:
                # Extract all Graphic-related lines
                graphic_lines = [l for l in config_content.split('\n')
                                 if 'WriterObject/Graphic' in l and 'Enable' in l]
                found_enabled = False
                for line in graphic_lines:
                    if '<value>true</value>' in line:
                        found_enabled = True
                        break
                if found_enabled:
                    print(f"PASS: Component 1 — Graphic AutoCaption is enabled (0.5 pts)")
                    total_score += 0.5
                else:
                    print(f"FAIL: Component 1 — Graphic AutoCaption not enabled in config")
            else:
                print(f"FAIL: Component 1 — No WriterObject/Graphic settings found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Category is set to 'Figure' (0.35 points)
    # In initial_env this is 'Illustration', in golden_env it should be 'Figure'
    try:
        category_pattern = r'<item oor:path="/org\.openoffice\.Office\.Writer/Insert/Caption/WriterObject/Graphic/Settings/Category"><value[^>]*>(.*?)</value>'
        category_match = re.search(category_pattern, config_content)

        if category_match:
            category_value = category_match.group(1).strip()
            if category_value == 'Figure':
                print(f"PASS: Component 2 — Category is 'Figure' (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 — Category is '{category_value}', expected 'Figure'")
        else:
            # Flexible fallback
            graphic_cat_lines = [l for l in config_content.split('\n')
                                 if 'WriterObject/Graphic/Settings/Category' in l]
            found_figure = False
            for line in graphic_cat_lines:
                if '>Figure<' in line:
                    found_figure = True
                    break
            if found_figure:
                print(f"PASS: Component 2 — Category is 'Figure' (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 — Category not set to 'Figure'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Numbering uses a sequential type (0.15 points)
    # LibreOffice numbering values: 0=Arabic(1,2,3), 1=Roman upper, 2=Roman lower,
    # 3=Letters upper, 4=Letters lower, 5=None
    # The task says "sequential numbering" — Arabic (0) is the most standard,
    # but any numbered type (0-4) counts as sequential.
    # In initial_env Numbering=4 (letters lower), golden also has Numbering=4.
    # However, the KEY differentiator is that AutoCaption must be ENABLED (Component 1)
    # for any numbering to actually apply. We check that numbering is a sequential type
    # AND that enable is true (compound check).
    try:
        # This component checks: Enable is true AND Numbering is a sequential type
        # This FAILS on initial because Enable=false there
        numbering_pattern = r'<item oor:path="/org\.openoffice\.Office\.Writer/Insert/Caption/WriterObject/Graphic/Settings"><prop oor:name="Numbering"[^>]*><value>(\d+)</value>'
        numbering_match = re.search(numbering_pattern, config_content)

        numbering_value = None
        if numbering_match:
            numbering_value = int(numbering_match.group(1))
        else:
            # Flexible fallback
            for line in config_content.split('\n'):
                if 'WriterObject/Graphic/Settings' in line and 'Numbering' in line:
                    num_match = re.search(r'<value>(\d+)</value>', line)
                    if num_match:
                        numbering_value = int(num_match.group(1))
                        break

        # Compound check: AutoCaption enabled AND numbering is sequential
        if total_score >= 0.5 and numbering_value is not None:
            # Sequential types: 0=Arabic, 1=Roman upper, 2=Roman lower, 3=Letters upper, 4=Letters lower
            if numbering_value in (0, 1, 2, 3, 4):
                numbering_names = {0: 'Arabic', 1: 'Roman Upper', 2: 'Roman Lower',
                                   3: 'Letters Upper', 4: 'Letters Lower'}
                print(f"PASS: Component 3 — Sequential numbering active (type={numbering_names.get(numbering_value, numbering_value)}, "
                      f"AutoCaption enabled) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — Numbering type {numbering_value} is not sequential")
        elif total_score < 0.5:
            print(f"FAIL: Component 3 — AutoCaption not enabled, so numbering is inactive")
        else:
            print(f"FAIL: Component 3 — Could not determine numbering value")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

"""
Reward Script: Change decimal separator in LibreOffice Calc from period to comma
Task ID: osworld_calc_decimal_separator_001
Domain: libreoffice_calc
Scoring:
  Component 1: DecimalSeparator entry present in LibreOffice Calc config (0.5 pts)
  Component 2: DecimalSeparator value is ',' (comma) in the Calc Formula/Syntax path (0.5 pts)
  Total: 1.0
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_calc_decimal_separator_001'
CONFIG_PATH = '/home/user/.config/libreoffice/4/user/registrymodifications.xcu'


def verify_task():
    """
    Verify that the LibreOffice Calc decimal separator setting has been changed
    from the default period (.) to a comma (,).

    The change is stored in the LibreOffice user registry configuration file:
      /home/user/.config/libreoffice/4/user/registrymodifications.xcu

    The relevant XML entry looks like:
      <item oor:path="/org.openoffice.Office.Calc/Formula/Syntax">
        <prop oor:name="DecimalSeparator" oor:op="fuse">
          <value>,</value>
        </prop>
      </item>

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: config file must exist
    if not os.path.exists(CONFIG_PATH):
        print(f"CRITICAL: LibreOffice config file not found: {CONFIG_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read config file {CONFIG_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: DecimalSeparator entry exists in the Calc Formula/Syntax config path (0.5 pts)
    # This entry is ABSENT in initial_env (no customization), PRESENT in golden_env
    try:
        # Look for the path /org.openoffice.Office.Calc/Formula/Syntax
        calc_formula_syntax_present = '/org.openoffice.Office.Calc/Formula/Syntax' in content
        decimal_separator_present = 'DecimalSeparator' in content

        if calc_formula_syntax_present and decimal_separator_present:
            print("PASS: Component 1 — DecimalSeparator entry present in Calc Formula/Syntax config (0.5 pts)")
            total_score += 0.5
        else:
            if not calc_formula_syntax_present:
                print("FAIL: Component 1 — /org.openoffice.Office.Calc/Formula/Syntax path not found in config")
            elif not decimal_separator_present:
                print("FAIL: Component 1 — DecimalSeparator property not found in config")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: DecimalSeparator value is ',' (comma), not '.' or any other value (0.5 pts)
    # Verifies the actual setting value, not just the presence of the entry
    try:
        # Parse the XML around the DecimalSeparator entry
        # The structure is: <prop oor:name="DecimalSeparator" ...><value>,</value></prop>
        # Use regex to find the value within the Calc/Formula/Syntax section
        pattern = r'/org\.openoffice\.Office\.Calc/Formula/Syntax.*?DecimalSeparator.*?<value>(.*?)</value>'
        match = re.search(pattern, content, re.DOTALL)

        if match:
            separator_value = match.group(1).strip()
            if separator_value == ',':
                print(f"PASS: Component 2 — DecimalSeparator value is ',' (comma) as required (0.5 pts)")
                total_score += 0.5
            else:
                print(f"FAIL: Component 2 — DecimalSeparator value is '{separator_value}', expected ','")
        else:
            # Try alternate approach: check if DecimalSeparator with value ',' exists anywhere in Calc section
            alt_pattern = r'DecimalSeparator[^<]*<value>\s*,\s*</value>'
            alt_match = re.search(alt_pattern, content, re.DOTALL)
            if alt_match:
                print("PASS: Component 2 — DecimalSeparator value is ',' (comma) as required (0.5 pts)")
                total_score += 0.5
            else:
                print("FAIL: Component 2 — Could not find DecimalSeparator with value ',' in config")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

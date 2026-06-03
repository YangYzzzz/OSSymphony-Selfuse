"""
Reward Script: Terraform VPC module configuration
Task ID: vscode_ops_044
Domain: vscode
Scoring:
  Component 1 (0.30): main.tf has provider "aws" block and VPC resource with CIDR 10.0.0.0/16
  Component 2 (0.25): main.tf has two subnet resources with CIDRs 10.0.1.0/24 and 10.0.2.0/24
  Component 3 (0.20): outputs.tf has vpc_id and subnet_ids outputs
  Component 4 (0.15): variables.tf has variable definitions for vpc_cidr and subnet CIDRs
  Component 5 (0.10): All three files use valid HCL-like structure (blocks/braces balanced)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_044'
TF_DIR = os.path.join(WORKDIR, 'terraform-infra')


def read_file_safe(path):
    """Read file and return content, or None if not found."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"ERROR: Cannot read {path}: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ----------------------------------------------------------------
    # Component 1: main.tf has provider "aws" and VPC with CIDR 10.0.0.0/16 (0.30 pts)
    # ----------------------------------------------------------------
    try:
        main_tf = read_file_safe(os.path.join(TF_DIR, 'main.tf'))
        if main_tf is None:
            print("FAIL: Component 1 — main.tf not found")
        else:
            has_provider_aws = bool(re.search(r'provider\s+"aws"', main_tf))
            # Check for VPC resource with CIDR 10.0.0.0/16
            # The CIDR could be inline or via variable reference
            has_vpc_resource = bool(re.search(r'resource\s+"aws_vpc"', main_tf))
            # Check that 10.0.0.0/16 appears somewhere (inline or in variables default)
            # We check main.tf for the vpc resource; the CIDR value may be a var reference
            has_cidr_ref = bool(
                re.search(r'10\.0\.0\.0/16', main_tf) or
                re.search(r'cidr_block\s*=\s*var\.', main_tf)
            )

            if has_provider_aws and has_vpc_resource and has_cidr_ref:
                print(f"PASS: Component 1 — provider aws + VPC resource with CIDR ref (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 1 — provider_aws={has_provider_aws}, vpc_resource={has_vpc_resource}, cidr_ref={has_cidr_ref}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ----------------------------------------------------------------
    # Component 2: Two subnet resources with CIDRs 10.0.1.0/24 and 10.0.2.0/24 (0.25 pts)
    # ----------------------------------------------------------------
    try:
        main_tf = read_file_safe(os.path.join(TF_DIR, 'main.tf'))
        if main_tf is None:
            print("FAIL: Component 2 — main.tf not found")
        else:
            # Count aws_subnet resources
            subnet_resources = re.findall(r'resource\s+"aws_subnet"', main_tf)
            has_two_subnets = len(subnet_resources) >= 2

            # Check for subnet CIDR references (inline or via variable)
            # The CIDRs 10.0.1.0/24 and 10.0.2.0/24 may be set via variables
            # We need to check that both CIDRs are referenced somewhere in the project
            has_subnet1_cidr = bool(
                re.search(r'10\.0\.1\.0/24', main_tf) or
                re.search(r'cidr_block\s*=\s*var\..*subnet.*1', main_tf) or
                re.search(r'cidr_block\s*=\s*var\.public_subnet_1_cidr', main_tf)
            )
            has_subnet2_cidr = bool(
                re.search(r'10\.0\.2\.0/24', main_tf) or
                re.search(r'cidr_block\s*=\s*var\..*subnet.*2', main_tf) or
                re.search(r'cidr_block\s*=\s*var\.public_subnet_2_cidr', main_tf)
            )

            if has_two_subnets and has_subnet1_cidr and has_subnet2_cidr:
                print(f"PASS: Component 2 — two subnet resources with CIDR refs (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 — two_subnets={has_two_subnets}, subnet1_cidr={has_subnet1_cidr}, subnet2_cidr={has_subnet2_cidr}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ----------------------------------------------------------------
    # Component 3: outputs.tf has vpc_id and subnet_ids outputs (0.20 pts)
    # ----------------------------------------------------------------
    try:
        outputs_tf = read_file_safe(os.path.join(TF_DIR, 'outputs.tf'))
        if outputs_tf is None:
            print("FAIL: Component 3 — outputs.tf not found")
        else:
            has_vpc_id_output = bool(re.search(r'output\s+"vpc_id"', outputs_tf))
            has_subnet_ids_output = bool(re.search(r'output\s+"subnet_ids"', outputs_tf))

            if has_vpc_id_output and has_subnet_ids_output:
                print(f"PASS: Component 3 — vpc_id and subnet_ids outputs found (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — vpc_id_output={has_vpc_id_output}, subnet_ids_output={has_subnet_ids_output}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ----------------------------------------------------------------
    # Component 4: variables.tf has variable definitions including CIDR defaults (0.15 pts)
    # ----------------------------------------------------------------
    try:
        variables_tf = read_file_safe(os.path.join(TF_DIR, 'variables.tf'))
        if variables_tf is None:
            print("FAIL: Component 4 — variables.tf not found")
        else:
            # Check for variable blocks
            variable_blocks = re.findall(r'variable\s+"([^"]+)"', variables_tf)

            # Must have at least variable defs and the key CIDRs as defaults
            has_vpc_cidr_default = bool(re.search(r'10\.0\.0\.0/16', variables_tf))
            has_subnet1_cidr_default = bool(re.search(r'10\.0\.1\.0/24', variables_tf))
            has_subnet2_cidr_default = bool(re.search(r'10\.0\.2\.0/24', variables_tf))

            if len(variable_blocks) >= 3 and has_vpc_cidr_default and has_subnet1_cidr_default and has_subnet2_cidr_default:
                print(f"PASS: Component 4 — variables.tf has {len(variable_blocks)} variables with correct CIDR defaults (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — var_blocks={len(variable_blocks)}, vpc_cidr={has_vpc_cidr_default}, subnet1={has_subnet1_cidr_default}, subnet2={has_subnet2_cidr_default}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ----------------------------------------------------------------
    # Component 5: Valid HCL structure — braces balanced in all files (0.10 pts)
    # ----------------------------------------------------------------
    try:
        balance_issues = []
        for fname in ['main.tf', 'outputs.tf', 'variables.tf']:
            content = read_file_safe(os.path.join(TF_DIR, fname))
            if content is None:
                balance_issues.append(f"{fname} not found")
                break
            open_braces = content.count('{')
            close_braces = content.count('}')
            if open_braces != close_braces or open_braces == 0:
                balance_issues.append(f"{fname} has unbalanced braces: open={open_braces}, close={close_braces}")

        if len(balance_issues) == 0:
            print(f"PASS: Component 5 — all .tf files have balanced braces (0.10 pts)")
            total_score += 0.10
        else:
            for issue in balance_issues:
                print(f"FAIL: Component 5 — {issue}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.isdir(TF_DIR):
    print(f"Directory not found: {TF_DIR}")
    print("REWARD: 0.0")
else:
    verify_task()

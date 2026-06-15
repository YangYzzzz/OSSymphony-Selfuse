"""
Reward Script: Create a REST Client GraphQL .http file with query and mutation requests
Task ID: vscode_gf3_047
Domain: vscode
Scoring:
  - Component 1 (0.30): GraphQL query request with variable usage
  - Component 2 (0.25): GraphQL mutation request
  - Component 3 (0.15): Both requests use Content-Type application/json
  - Component 4 (0.20): Both requests have JSON body with "query" and "variables" fields
  - Component 5 (0.10): Requests separated by ### separator
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_047'

FILE_PATH = os.path.join(WORKDIR, 'projects', 'api-tests', 'graphql.http')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if not content.strip():
        print("CRITICAL: File is empty")
        print("REWARD: 0.0")
        return 0.0

    # Split content into request blocks by ### separator
    # REST Client uses ### to separate requests
    blocks = re.split(r'^\s*###.*$', content, flags=re.MULTILINE)
    # Filter out empty blocks
    blocks = [b.strip() for b in blocks if b.strip()]

    print(f"INFO: Found {len(blocks)} request block(s) in file")

    # Component 1: GraphQL query request with variable usage (0.30 points)
    # Must contain a POST request with a GraphQL query (not mutation) that uses variables ($)
    try:
        def _find_query_block(blocks_list):
            """Return the index of a block containing a GraphQL query with variables, or -1."""
            for idx, block in enumerate(blocks_list):
                if not re.search(r'^\s*POST\s+', block, re.MULTILINE | re.IGNORECASE):
                    continue
                # Strict: "query" JSON field containing "query " keyword with $ variables
                if re.search(r'"query"\s*:\s*"query\s', block, re.IGNORECASE) and '$' in block:
                    return idx
            # Fallback: more lenient matching
            for idx, block in enumerate(blocks_list):
                if not re.search(r'^\s*POST\s+', block, re.MULTILINE | re.IGNORECASE):
                    continue
                has_query_field = re.search(r'"query"\s*:', block)
                has_query_op = re.search(r'query\s+\w+', block, re.IGNORECASE)
                has_variable = '$' in block or '"variables"' in block
                is_not_mutation_only = not re.search(r'"query"\s*:\s*"mutation\s', block, re.IGNORECASE)
                if has_query_field and has_query_op and has_variable and is_not_mutation_only:
                    return idx
            return -1

        query_idx = _find_query_block(blocks)
        if query_idx >= 0:
            print(f"PASS: Component 1 -- GraphQL query with variables found in block {query_idx} (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 -- No GraphQL query request with variable usage found")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: GraphQL mutation request (0.25 points)
    try:
        def _find_mutation_block(blocks_list):
            """Return index of block containing a GraphQL mutation, or -1."""
            for idx, block in enumerate(blocks_list):
                if not re.search(r'^\s*POST\s+', block, re.MULTILINE | re.IGNORECASE):
                    continue
                if re.search(r'mutation\s+\w+', block, re.IGNORECASE):
                    return idx
            return -1

        mutation_idx = _find_mutation_block(blocks)
        if mutation_idx >= 0:
            print(f"PASS: Component 2 -- GraphQL mutation request found in block {mutation_idx} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 -- No GraphQL mutation request found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Both requests use Content-Type application/json (0.15 points)
    try:
        post_blocks = [b for b in blocks if re.search(r'^\s*POST\s+', b, re.MULTILINE | re.IGNORECASE)]
        if len(post_blocks) >= 2:
            ct_count = 0
            for block in post_blocks:
                if re.search(r'Content-Type\s*:\s*application/json', block, re.IGNORECASE):
                    ct_count += 1
            if ct_count >= 2:
                print(f"PASS: Component 3 -- Both requests have Content-Type application/json (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 -- Only {ct_count} of {len(post_blocks)} POST requests have Content-Type application/json")
        else:
            print(f"FAIL: Component 3 -- Need at least 2 POST requests, found {len(post_blocks)}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Both requests have JSON body with "query" and "variables" fields (0.20 points)
    try:
        post_blocks = [b for b in blocks if re.search(r'^\s*POST\s+', b, re.MULTILINE | re.IGNORECASE)]
        valid_bodies = 0
        for block in post_blocks:
            has_query_field = '"query"' in block
            has_variables_field = '"variables"' in block
            if has_query_field and has_variables_field:
                valid_bodies += 1

        if valid_bodies >= 2:
            print(f"PASS: Component 4 -- Both requests have JSON body with 'query' and 'variables' fields (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 -- Only {valid_bodies} of {len(post_blocks)} POST requests have both 'query' and 'variables' fields")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Requests separated by ### separator (0.10 points)
    try:
        separator_count = len(re.findall(r'^\s*###', content, re.MULTILINE))
        if separator_count >= 1 and len(blocks) >= 2:
            print(f"PASS: Component 5 -- Found {separator_count} ### separator(s) between {len(blocks)} blocks (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 -- Expected ### separators between requests, found {separator_count} separators and {len(blocks)} blocks")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)

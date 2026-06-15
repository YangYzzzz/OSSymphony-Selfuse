"""
Reward Script: GraphQL development workflow setup in ~/project
Task ID: vscode_wf_070
Domain: vscode
Scoring:
  - Component 1: GraphQL extension installed (0.10)
  - Component 2: schema.graphql with User, Post, Query, Mutation types (0.20)
  - Component 3: .graphqlrc.yml pointing to schema.graphql (0.10)
  - Component 4: Resolver files in src/resolvers/ (0.20)
  - Component 5: .vscode/settings.json with GraphQL settings (0.15)
  - Component 6: .vscode/tasks.json with 3 required tasks (0.15)
  - Component 7: codegen.yml configured for TypeScript generation (0.10)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'project')
TASK_ID = 'vscode_wf_070'


def verify_task():
    """
    Verify GraphQL development workflow setup.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: GraphQL extension installed (0.10 points)
    try:
        ext_output = os.popen('code --list-extensions 2>/dev/null').read().strip().lower()
        # Check for graphql.vscode-graphql (case-insensitive)
        if 'graphql.vscode-graphql' in ext_output:
            print(f"PASS: Component 1 — GraphQL extension installed (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — GraphQL extension not found. Extensions: {ext_output}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: schema.graphql with User, Post, Query, Mutation types (0.20 points)
    schema_path = os.path.join(PROJECT, 'schema.graphql')
    try:
        if os.path.isfile(schema_path):
            with open(schema_path, 'r') as f:
                schema_content = f.read()

            # Check for all required type definitions
            has_user_type = bool(re.search(r'type\s+User\s*\{', schema_content))
            has_post_type = bool(re.search(r'type\s+Post\s*\{', schema_content))
            has_query_type = bool(re.search(r'type\s+Query\s*\{', schema_content))
            has_mutation_type = bool(re.search(r'type\s+Mutation\s*\{', schema_content))

            found_count = sum([has_user_type, has_post_type, has_query_type, has_mutation_type])

            if found_count == 4:
                print(f"PASS: Component 2 — schema.graphql has all 4 required types (0.20 pts)")
                total_score += 0.20
            elif found_count > 0:
                partial = round(0.20 * (found_count / 4), 2)
                print(f"PARTIAL: Component 2 — schema.graphql has {found_count}/4 types ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — schema.graphql has no required types")
        else:
            print(f"FAIL: Component 2 — schema.graphql does not exist")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: .graphqlrc.yml pointing to schema.graphql (0.10 points)
    graphqlrc_path = os.path.join(PROJECT, '.graphqlrc.yml')
    try:
        if os.path.isfile(graphqlrc_path):
            with open(graphqlrc_path, 'r') as f:
                rc_content = f.read()

            # Check that it references schema.graphql
            if 'schema.graphql' in rc_content or 'schema: ' in rc_content:
                print(f"PASS: Component 3 — .graphqlrc.yml points to schema (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 — .graphqlrc.yml does not reference schema.graphql")
        else:
            print(f"FAIL: Component 3 — .graphqlrc.yml does not exist")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Resolver files in src/resolvers/ (0.20 points)
    resolvers_dir = os.path.join(PROJECT, 'src', 'resolvers')
    try:
        if os.path.isdir(resolvers_dir):
            resolver_files = os.listdir(resolvers_dir)
            resolver_js_files = [f for f in resolver_files if f.endswith('.js') or f.endswith('.ts')]

            # Check for query and mutation resolver files (any naming convention)
            has_query_resolver = any('query' in f.lower() for f in resolver_js_files)
            has_mutation_resolver = any('mutation' in f.lower() for f in resolver_js_files)

            if has_query_resolver and has_mutation_resolver:
                print(f"PASS: Component 4 — Resolver files found: {resolver_js_files} (0.20 pts)")
                total_score += 0.20
            elif has_query_resolver or has_mutation_resolver:
                print(f"PARTIAL: Component 4 — Only one resolver type found: {resolver_js_files} (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 4 — No query/mutation resolver files in {resolver_files}")
        else:
            print(f"FAIL: Component 4 — src/resolvers/ directory does not exist")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: .vscode/settings.json with GraphQL settings (0.15 points)
    settings_path = os.path.join(PROJECT, '.vscode', 'settings.json')
    try:
        if os.path.isfile(settings_path):
            with open(settings_path, 'r') as f:
                content = f.read()
            # Strip JSONC comments before parsing
            content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            content_clean = re.sub(r'/\*.*?\*/', '', content_clean, flags=re.DOTALL)
            settings = json.loads(content_clean)

            # Check for GraphQL-related settings
            settings_str = json.dumps(settings).lower()
            has_graphql_settings = 'graphql' in settings_str

            if has_graphql_settings:
                print(f"PASS: Component 5 — settings.json has GraphQL settings (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 — settings.json has no GraphQL-related settings")
        else:
            print(f"FAIL: Component 5 — .vscode/settings.json does not exist")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: .vscode/tasks.json with generate-types, start-server, playground tasks (0.15 points)
    tasks_path = os.path.join(PROJECT, '.vscode', 'tasks.json')
    try:
        if os.path.isfile(tasks_path):
            with open(tasks_path, 'r') as f:
                content = f.read()
            content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            content_clean = re.sub(r'/\*.*?\*/', '', content_clean, flags=re.DOTALL)
            # Remove control characters that may break JSON parsing (keep \n \r \t)
            content_clean = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', ' ', content_clean)
            try:
                tasks_config = json.loads(content_clean)
            except json.JSONDecodeError:
                # Fallback: replace all control chars including tabs in string values
                content_clean2 = re.sub(r'[\x00-\x1f\x7f]', ' ', content)
                tasks_config = json.loads(content_clean2)

            tasks = tasks_config.get('tasks', [])
            task_labels = [t.get('label', '').lower() for t in tasks]

            has_generate = any('generate' in l and 'type' in l for l in task_labels)
            has_server = any('start' in l and 'server' in l for l in task_labels)
            has_playground = any('playground' in l for l in task_labels)

            found_tasks = sum([has_generate, has_server, has_playground])

            if found_tasks == 3:
                print(f"PASS: Component 6 — tasks.json has all 3 required tasks (0.15 pts)")
                total_score += 0.15
            elif found_tasks > 0:
                partial = round(0.15 * (found_tasks / 3), 2)
                print(f"PARTIAL: Component 6 — tasks.json has {found_tasks}/3 tasks ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 6 — tasks.json has no required tasks. Labels: {task_labels}")
        else:
            print(f"FAIL: Component 6 — .vscode/tasks.json does not exist")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: codegen.yml configured for TypeScript generation (0.10 points)
    codegen_path = os.path.join(PROJECT, 'codegen.yml')
    # Also check codegen.yaml and codegen.ts as alternatives
    if not os.path.isfile(codegen_path):
        codegen_path = os.path.join(PROJECT, 'codegen.yaml')
    try:
        if os.path.isfile(codegen_path):
            with open(codegen_path, 'r') as f:
                codegen_content = f.read()

            has_typescript = 'typescript' in codegen_content.lower()
            has_schema_ref = 'schema' in codegen_content.lower()

            if has_typescript and has_schema_ref:
                print(f"PASS: Component 7 — codegen.yml configured for TypeScript (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 7 — codegen.yml missing typescript or schema config")
        else:
            print(f"FAIL: Component 7 — codegen.yml does not exist")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()

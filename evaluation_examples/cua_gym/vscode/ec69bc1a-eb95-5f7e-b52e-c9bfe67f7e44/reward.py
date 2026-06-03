"""
Reward Script: Build a GraphQL API with Strawberry in VSCode
Task ID: vscode_gf6_088
Domain: vscode
Scoring:
  1. Packages installed (strawberry-graphql, pytest-asyncio)  - 0.10
  2. src/schema/types.py with Strawberry types                - 0.15
  3. src/schema/query.py with Query type                      - 0.15
  4. src/schema/mutation.py with Mutation type                 - 0.15
  5. src/main.py with FastAPI + GraphQL router                 - 0.15
  6. tests/test_schema.py with >= 3 tests                     - 0.15
  7. .vscode/launch.json with debug config                    - 0.15
"""

import os
import re
import json

WORKDIR = '/home/user/projects/python-graphql'
TASK_ID = 'vscode_gf6_088'
VENV_SITE = os.path.join(WORKDIR, 'venv', 'lib')


def find_site_packages():
    """Find the site-packages directory inside venv."""
    if not os.path.isdir(VENV_SITE):
        return None
    for pydir in os.listdir(VENV_SITE):
        sp = os.path.join(VENV_SITE, pydir, 'site-packages')
        if os.path.isdir(sp):
            return sp
    return None


def check_package_installed(site_packages, package_prefix):
    """Check if a package is installed by looking for its dist-info directory."""
    if not site_packages:
        return False
    try:
        for entry in os.listdir(site_packages):
            if entry.lower().startswith(package_prefix.lower()) and entry.endswith('.dist-info'):
                return True
    except Exception:
        pass
    return False


def verify_task():
    total_score = 0.0

    # =========================================================
    # Component 1: Packages installed (0.10 points)
    # strawberry-graphql and pytest-asyncio must be in venv
    # =========================================================
    try:
        sp = find_site_packages()
        strawberry_installed = check_package_installed(sp, 'strawberry_graphql')
        pytest_asyncio_installed = check_package_installed(sp, 'pytest_asyncio')

        if strawberry_installed and pytest_asyncio_installed:
            print("PASS: Component 1 - Both strawberry-graphql and pytest-asyncio installed (0.10 pts)")
            total_score += 0.10
        elif strawberry_installed:
            print("PARTIAL: Component 1 - Only strawberry-graphql installed (0.05 pts)")
            total_score += 0.05
        elif pytest_asyncio_installed:
            print("PARTIAL: Component 1 - Only pytest-asyncio installed (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 1 - Neither strawberry-graphql nor pytest-asyncio found in {sp}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # =========================================================
    # Component 2: src/schema/types.py (0.15 points)
    # Must define User, Post as @strawberry.type and CreateUserInput as @strawberry.input
    # =========================================================
    try:
        types_path = os.path.join(WORKDIR, 'src', 'schema', 'types.py')
        if os.path.isfile(types_path):
            with open(types_path, 'r') as f:
                types_content = f.read()

            has_strawberry_import = 'import strawberry' in types_content
            has_user_type = bool(re.search(r'@strawberry\.type\s*\n\s*class\s+User', types_content))
            has_post_type = bool(re.search(r'@strawberry\.type\s*\n\s*class\s+Post', types_content))
            has_create_user_input = bool(re.search(r'@strawberry\.input\s*\n\s*class\s+CreateUserInput', types_content))

            sub_score = 0.0
            if has_strawberry_import and has_user_type:
                sub_score += 0.05
            if has_post_type:
                sub_score += 0.05
            if has_create_user_input:
                sub_score += 0.05

            if sub_score >= 0.15:
                print(f"PASS: Component 2 - types.py has User, Post, CreateUserInput ({sub_score} pts)")
            elif sub_score > 0:
                print(f"PARTIAL: Component 2 - types.py partial (import={has_strawberry_import}, User={has_user_type}, Post={has_post_type}, CreateUserInput={has_create_user_input}) ({sub_score} pts)")
            else:
                print(f"FAIL: Component 2 - types.py missing required types (import={has_strawberry_import}, User={has_user_type}, Post={has_post_type}, CreateUserInput={has_create_user_input})")
            total_score += sub_score
        else:
            print(f"FAIL: Component 2 - {types_path} not found")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # =========================================================
    # Component 3: src/schema/query.py (0.15 points)
    # Must define @strawberry.type Query with users() and user() resolvers
    # =========================================================
    try:
        query_path = os.path.join(WORKDIR, 'src', 'schema', 'query.py')
        if os.path.isfile(query_path):
            with open(query_path, 'r') as f:
                query_content = f.read()

            has_query_class = bool(re.search(r'@strawberry\.type\s*\n\s*class\s+Query', query_content))
            has_users_resolver = bool(re.search(r'def\s+users\s*\(', query_content))
            has_user_resolver = bool(re.search(r'def\s+user\s*\(', query_content))

            sub_score = 0.0
            if has_query_class:
                sub_score += 0.05
            if has_users_resolver:
                sub_score += 0.05
            if has_user_resolver:
                sub_score += 0.05

            if sub_score >= 0.15:
                print(f"PASS: Component 3 - query.py has Query with users() and user() ({sub_score} pts)")
            elif sub_score > 0:
                print(f"PARTIAL: Component 3 - query.py partial (Query={has_query_class}, users={has_users_resolver}, user={has_user_resolver}) ({sub_score} pts)")
            else:
                print(f"FAIL: Component 3 - query.py missing required resolvers")
            total_score += sub_score
        else:
            print(f"FAIL: Component 3 - {query_path} not found")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # =========================================================
    # Component 4: src/schema/mutation.py (0.15 points)
    # Must define @strawberry.type Mutation with create_user() resolver
    # =========================================================
    try:
        mutation_path = os.path.join(WORKDIR, 'src', 'schema', 'mutation.py')
        if os.path.isfile(mutation_path):
            with open(mutation_path, 'r') as f:
                mutation_content = f.read()

            has_mutation_class = bool(re.search(r'@strawberry\.type\s*\n\s*class\s+Mutation', mutation_content))
            has_create_user = bool(re.search(r'def\s+create_user\s*\(', mutation_content))
            has_create_user_input_ref = 'CreateUserInput' in mutation_content

            sub_score = 0.0
            if has_mutation_class:
                sub_score += 0.05
            if has_create_user:
                sub_score += 0.05
            if has_create_user_input_ref:
                sub_score += 0.05

            if sub_score >= 0.15:
                print(f"PASS: Component 4 - mutation.py has Mutation with create_user() ({sub_score} pts)")
            elif sub_score > 0:
                print(f"PARTIAL: Component 4 - mutation.py partial (Mutation={has_mutation_class}, create_user={has_create_user}, Input={has_create_user_input_ref}) ({sub_score} pts)")
            else:
                print(f"FAIL: Component 4 - mutation.py missing required definitions")
            total_score += sub_score
        else:
            print(f"FAIL: Component 4 - {mutation_path} not found")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # =========================================================
    # Component 5: src/main.py (0.15 points)
    # Must have FastAPI app with Strawberry GraphQL router at /graphql
    # =========================================================
    try:
        main_path = os.path.join(WORKDIR, 'src', 'main.py')
        if os.path.isfile(main_path):
            with open(main_path, 'r') as f:
                main_content = f.read()

            has_fastapi = bool(re.search(r'from\s+fastapi\s+import|import\s+fastapi', main_content))
            has_strawberry_router = bool(re.search(r'GraphQLRouter', main_content))
            has_graphql_prefix = bool(re.search(r'/graphql', main_content))
            has_app = bool(re.search(r'app\s*=\s*FastAPI', main_content))

            sub_score = 0.0
            if has_fastapi and has_app:
                sub_score += 0.05
            if has_strawberry_router:
                sub_score += 0.05
            if has_graphql_prefix:
                sub_score += 0.05

            if sub_score >= 0.15:
                print(f"PASS: Component 5 - main.py has FastAPI + GraphQL at /graphql ({sub_score} pts)")
            elif sub_score > 0:
                print(f"PARTIAL: Component 5 - main.py partial (FastAPI={has_fastapi}, app={has_app}, Router={has_strawberry_router}, /graphql={has_graphql_prefix}) ({sub_score} pts)")
            else:
                print(f"FAIL: Component 5 - main.py missing required structure")
            total_score += sub_score
        else:
            print(f"FAIL: Component 5 - {main_path} not found")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # =========================================================
    # Component 6: tests/test_schema.py (0.15 points)
    # Must have at least 3 test functions
    # =========================================================
    try:
        test_path = os.path.join(WORKDIR, 'tests', 'test_schema.py')
        if os.path.isfile(test_path):
            with open(test_path, 'r') as f:
                test_content = f.read()

            test_funcs = re.findall(r'def\s+(test_\w+)\s*\(', test_content)
            num_tests = len(test_funcs)
            has_strawberry_ref = 'strawberry' in test_content

            sub_score = 0.0
            if num_tests >= 3 and has_strawberry_ref:
                sub_score = 0.15
                print(f"PASS: Component 6 - test_schema.py has {num_tests} tests with strawberry ({sub_score} pts)")
            elif num_tests >= 1 and has_strawberry_ref:
                sub_score = 0.10
                print(f"PARTIAL: Component 6 - test_schema.py has {num_tests} tests (need >=3) ({sub_score} pts)")
            elif num_tests >= 1:
                sub_score = 0.05
                print(f"PARTIAL: Component 6 - test_schema.py has {num_tests} tests but no strawberry reference ({sub_score} pts)")
            else:
                print(f"FAIL: Component 6 - test_schema.py has no test functions")
            total_score += sub_score
        else:
            print(f"FAIL: Component 6 - {test_path} not found")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    # =========================================================
    # Component 7: .vscode/launch.json (0.15 points)
    # Must have debug configuration for FastAPI/uvicorn
    # =========================================================
    try:
        launch_path = os.path.join(WORKDIR, '.vscode', 'launch.json')
        if os.path.isfile(launch_path):
            with open(launch_path, 'r') as f:
                # Handle JSONC (strip comments)
                content = f.read()
                clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
                launch_data = json.loads(clean)

            configs = launch_data.get('configurations', [])
            has_debug_config = len(configs) > 0

            # Check if any config references uvicorn or fastapi or python
            has_relevant_config = False
            for cfg in configs:
                cfg_str = json.dumps(cfg).lower()
                if 'uvicorn' in cfg_str or 'fastapi' in cfg_str or 'src.main' in cfg_str:
                    has_relevant_config = True
                    break

            sub_score = 0.0
            if has_debug_config and has_relevant_config:
                sub_score = 0.15
                print(f"PASS: Component 7 - launch.json has FastAPI debug config ({sub_score} pts)")
            elif has_debug_config:
                sub_score = 0.10
                print(f"PARTIAL: Component 7 - launch.json has config but not FastAPI-specific ({sub_score} pts)")
            else:
                print(f"FAIL: Component 7 - launch.json has no configurations")
            total_score += sub_score
        else:
            print(f"FAIL: Component 7 - {launch_path} not found")
    except Exception as e:
        print(f"ERROR: Component 7 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

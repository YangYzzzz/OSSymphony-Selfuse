"""
Reward Script: TypeScript GraphQL Server with Apollo, TypeORM, and type-graphql
Task ID: vscode_gf4_032
Domain: vscode
Scoring:
  C1 (0.20): package.json has all required dependencies
  C2 (0.10): tsconfig.json has experimentalDecorators + emitDecoratorMetadata
  C3 (0.20): src/entity/User.ts - TypeORM entity with 4 fields
  C4 (0.25): src/resolver/UserResolver.ts - 2 queries + 2 mutations
  C5 (0.10): src/index.ts - bootstraps Apollo Server + TypeORM
  C6 (0.15): Tests exist with test cases
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'ts-graphql-server')


def verify_task():
    total_score = 0.0

    # ========================================================
    # Component 1: package.json has all required dependencies (0.20 pts)
    # ========================================================
    try:
        pkg_path = os.path.join(PROJECT, 'package.json')
        if not os.path.exists(pkg_path):
            print("FAIL: Component 1 — package.json not found")
        else:
            with open(pkg_path, 'r') as f:
                pkg = json.load(f)

            all_deps = {}
            all_deps.update(pkg.get('dependencies', {}))
            all_deps.update(pkg.get('devDependencies', {}))

            required_runtime = ['apollo-server', 'graphql', 'type-graphql',
                                'reflect-metadata', 'typeorm', 'sqlite3']
            found_runtime = [d for d in required_runtime if d in all_deps]

            # Check for TypeScript types (at least @types/node)
            has_typescript = 'typescript' in all_deps
            has_types = any(k.startswith('@types/') for k in all_deps)

            if len(found_runtime) == len(required_runtime) and has_typescript and has_types:
                print(f"PASS: Component 1 — All {len(required_runtime)} runtime deps + TypeScript + types found (0.20 pts)")
                total_score += 0.20
            elif len(found_runtime) >= 4:
                partial = 0.10
                print(f"PARTIAL: Component 1 — {len(found_runtime)}/{len(required_runtime)} runtime deps found ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 1 — Only {len(found_runtime)}/{len(required_runtime)} runtime deps. Missing: {set(required_runtime) - set(found_runtime)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ========================================================
    # Component 2: tsconfig.json with decorator settings (0.10 pts)
    # ========================================================
    try:
        tsconfig_path = os.path.join(PROJECT, 'tsconfig.json')
        if not os.path.exists(tsconfig_path):
            print("FAIL: Component 2 — tsconfig.json not found")
        else:
            with open(tsconfig_path, 'r') as f:
                content = f.read()
            # Strip JSONC comments before parsing
            cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            cleaned = re.sub(r'/\*.*?\*/', '', cleaned, flags=re.DOTALL)
            tsconfig = json.loads(cleaned)

            compiler_opts = tsconfig.get('compilerOptions', {})
            exp_dec = compiler_opts.get('experimentalDecorators', False)
            emit_meta = compiler_opts.get('emitDecoratorMetadata', False)

            if exp_dec and emit_meta:
                print("PASS: Component 2 — experimentalDecorators=true, emitDecoratorMetadata=true (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 2 — experimentalDecorators={exp_dec}, emitDecoratorMetadata={emit_meta}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ========================================================
    # Component 3: src/entity/User.ts - TypeORM entity with 4 fields (0.20 pts)
    # ========================================================
    try:
        user_entity_path = os.path.join(PROJECT, 'src', 'entity', 'User.ts')
        if not os.path.exists(user_entity_path):
            print("FAIL: Component 3 — src/entity/User.ts not found")
        else:
            with open(user_entity_path, 'r') as f:
                user_content = f.read()

            checks = {
                '@Entity': bool(re.search(r'@Entity\b', user_content)),
                'PrimaryGeneratedColumn_id': bool(re.search(r'@PrimaryGeneratedColumn\b', user_content)) and bool(re.search(r'\bid\b.*:\s*number', user_content)),
                'Column_username_unique': bool(re.search(r'@Column\b', user_content)) and bool(re.search(r'\busername\b.*:\s*string', user_content)),
                'Column_email': bool(re.search(r'\bemail\b.*:\s*string', user_content)),
                'CreateDateColumn_createdAt': bool(re.search(r'@CreateDateColumn\b', user_content)) and bool(re.search(r'\bcreatedAt\b', user_content)),
            }

            passed = sum(1 for v in checks.values() if v)
            total_checks = len(checks)

            if passed == total_checks:
                print(f"PASS: Component 3 — User entity has all {total_checks} required elements (0.20 pts)")
                total_score += 0.20
            elif passed >= 3:
                partial = round(0.20 * passed / total_checks, 2)
                print(f"PARTIAL: Component 3 — {passed}/{total_checks} checks passed ({partial} pts)")
                total_score += partial
            else:
                failed = [k for k, v in checks.items() if not v]
                print(f"FAIL: Component 3 — Only {passed}/{total_checks}. Failed: {failed}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ========================================================
    # Component 4: UserResolver.ts - 2 queries + 2 mutations (0.25 pts)
    # ========================================================
    try:
        resolver_path = os.path.join(PROJECT, 'src', 'resolver', 'UserResolver.ts')
        if not os.path.exists(resolver_path):
            print("FAIL: Component 4 — src/resolver/UserResolver.ts not found")
        else:
            with open(resolver_path, 'r') as f:
                resolver_content = f.read()

            has_resolver_decorator = bool(re.search(r'@Resolver\b', resolver_content))
            # Count @Query decorators
            query_count = len(re.findall(r'@Query\b', resolver_content))
            # Count @Mutation decorators
            mutation_count = len(re.findall(r'@Mutation\b', resolver_content))

            # Check for specific methods
            has_users_query = bool(re.search(r'async\s+users\s*\(', resolver_content))
            has_user_query = bool(re.search(r'async\s+user\s*\(', resolver_content))
            has_create_mutation = bool(re.search(r'async\s+createUser\s*\(', resolver_content))
            has_delete_mutation = bool(re.search(r'async\s+deleteUser\s*\(', resolver_content))

            method_checks = [has_resolver_decorator, has_users_query, has_user_query,
                             has_create_mutation, has_delete_mutation]
            methods_passed = sum(1 for c in method_checks if c)

            if methods_passed == 5 and query_count >= 2 and mutation_count >= 2:
                print(f"PASS: Component 4 — @Resolver with {query_count} queries, {mutation_count} mutations, all 4 methods present (0.25 pts)")
                total_score += 0.25
            elif methods_passed >= 3:
                partial = round(0.25 * methods_passed / 5, 2)
                print(f"PARTIAL: Component 4 — {methods_passed}/5 checks. queries={query_count}, mutations={mutation_count} ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 — {methods_passed}/5 checks. queries={query_count}, mutations={mutation_count}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ========================================================
    # Component 5: src/index.ts bootstraps Apollo + TypeORM (0.10 pts)
    # ========================================================
    try:
        index_path = os.path.join(PROJECT, 'src', 'index.ts')
        if not os.path.exists(index_path):
            print("FAIL: Component 5 — src/index.ts not found")
        else:
            with open(index_path, 'r') as f:
                index_content = f.read()

            has_apollo_import = bool(re.search(r'(apollo-server|@apollo/server)', index_content))
            has_typegraphql = bool(re.search(r'(type-graphql|buildSchema)', index_content))
            has_resolver_import = bool(re.search(r'UserResolver', index_content))
            has_server_listen = bool(re.search(r'(server\.listen|startStandaloneServer)', index_content))

            checks_passed = sum([has_apollo_import, has_typegraphql, has_resolver_import, has_server_listen])

            if checks_passed == 4:
                print(f"PASS: Component 5 — index.ts has Apollo import, type-graphql, UserResolver, server.listen (0.10 pts)")
                total_score += 0.10
            elif checks_passed >= 2:
                partial = round(0.10 * checks_passed / 4, 2)
                print(f"PARTIAL: Component 5 — {checks_passed}/4 bootstrap checks ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 5 — Only {checks_passed}/4 bootstrap checks")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # ========================================================
    # Component 6: Tests exist with test cases (0.15 pts)
    # ========================================================
    try:
        # Search for test files
        test_files = []
        for root, dirs, files in os.walk(os.path.join(PROJECT, 'src')):
            for f in files:
                if f.endswith('.test.ts') or f.endswith('.spec.ts'):
                    test_files.append(os.path.join(root, f))

        # Also check __tests__ directory
        tests_dir = os.path.join(PROJECT, 'src', '__tests__')
        if os.path.isdir(tests_dir):
            for f in os.listdir(tests_dir):
                full_path = os.path.join(tests_dir, f)
                if full_path not in test_files and f.endswith('.ts'):
                    test_files.append(full_path)

        if not test_files:
            print("FAIL: Component 6 — No test files found")
        else:
            # Read test file content and check for actual test cases
            has_test_cases = False
            has_graphql_test = False
            test_content = ""
            for tf in test_files:
                with open(tf, 'r') as fh:
                    test_content += fh.read()

            # Check for test blocks
            test_case_count = len(re.findall(r'\bit\s*\(', test_content))
            has_graphql_test = bool(re.search(r'(executeOperation|graphql|__schema|query|mutation)', test_content, re.IGNORECASE))

            if test_case_count >= 2 and has_graphql_test:
                print(f"PASS: Component 6 — {len(test_files)} test file(s) with {test_case_count} test cases including GraphQL tests (0.15 pts)")
                total_score += 0.15
            elif test_case_count >= 1:
                partial = 0.08
                print(f"PARTIAL: Component 6 — {test_case_count} test case(s), graphql_tests={has_graphql_test} ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 6 — Test files found but no test cases (it blocks)")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

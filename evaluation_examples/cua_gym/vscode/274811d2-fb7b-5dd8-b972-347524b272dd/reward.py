"""
Reward Script: Go Code Review Refactoring
Task ID: vscode_gf6_031
Domain: vscode
Scoring:
  C1 (0.15): Repository interface file exists with ProductRepository interface
  C2 (0.20): Service depends on interface, not concrete *sql.DB
  C3 (0.20): All 4 service methods accept context.Context as first param
  C4 (0.15): Service uses slog instead of log.Printf
  C5 (0.15): FindAll has pagination (page, pageSize params + paginated result struct)
  C6 (0.15): Test file exists with MockProductRepository implementing interface
"""

import os
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'code-review-go')
SERVICE_FILE = os.path.join(PROJECT, 'internal', 'service', 'product_service.go')
REPO_FILE = os.path.join(PROJECT, 'internal', 'repository', 'product_repository.go')
TEST_FILE = os.path.join(PROJECT, 'internal', 'service', 'product_service_test.go')


def read_file(path):
    """Read a file and return its content, or None if not found."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"ERROR: Cannot read {path}: {e}")
        return None


def verify_task():
    total_score = 0.0

    # Read service file (required for most checks)
    service_content = read_file(SERVICE_FILE)
    if service_content is None:
        print(f"CRITICAL: Service file not found at {SERVICE_FILE}")
        print("REWARD: 0.0")
        return 0.0

    # =========================================================================
    # Component 1: Repository interface file exists with ProductRepository (0.15)
    # =========================================================================
    try:
        repo_content = read_file(REPO_FILE)
        if repo_content is not None:
            # Check that it defines a ProductRepository interface with the 4 required methods
            has_interface = 'interface' in repo_content and 'ProductRepository' in repo_content
            has_find_by_id = bool(re.search(r'FindByID\s*\(', repo_content))
            has_find_all = bool(re.search(r'FindAll\s*\(', repo_content))
            has_save = bool(re.search(r'Save\s*\(', repo_content))
            has_delete = bool(re.search(r'Delete\s*\(', repo_content))

            methods_present = sum([has_find_by_id, has_find_all, has_save, has_delete])
            if has_interface and methods_present == 4:
                print(f"PASS: Component 1 — ProductRepository interface with all 4 methods (0.15 pts)")
                total_score += 0.15
            elif has_interface and methods_present > 0:
                partial = 0.15 * (methods_present / 4)
                print(f"PARTIAL: Component 1 — Interface found but only {methods_present}/4 methods ({partial:.3f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 1 — No ProductRepository interface found in repo file")
        else:
            print(f"FAIL: Component 1 — Repository file not found at {REPO_FILE}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # =========================================================================
    # Component 2: Service depends on interface, not concrete *sql.DB (0.20)
    # =========================================================================
    try:
        # The service struct should NOT contain *sql.DB
        has_sql_db = bool(re.search(r'\*sql\.DB', service_content))
        # The service struct should contain a field typed as ProductRepository (or similar interface)
        has_repo_field = bool(re.search(r'repo\s+.*ProductRepository', service_content) or
                             re.search(r'repository\s+.*ProductRepository', service_content) or
                             re.search(r'ProductRepository', service_content))
        # Should NOT import "database/sql"
        imports_sql = bool(re.search(r'"database/sql"', service_content))

        if not has_sql_db and has_repo_field and not imports_sql:
            print(f"PASS: Component 2 — Service depends on interface, not *sql.DB (0.20 pts)")
            total_score += 0.20
        elif not has_sql_db and has_repo_field:
            print(f"PARTIAL: Component 2 — Uses interface but still imports database/sql (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 2 — Service still depends on *sql.DB (has_sql_db={has_sql_db}, has_repo_field={has_repo_field})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # =========================================================================
    # Component 3: All 4 service methods accept context.Context as first param (0.20)
    # =========================================================================
    try:
        # Check that context is imported
        has_context_import = bool(re.search(r'"context"', service_content))

        # Check each method signature for context.Context as first param after receiver
        # Pattern: func (s *ProductService) MethodName(ctx context.Context, ...)
        methods_to_check = ['FindByID', 'FindAll', 'Save', 'Delete']
        methods_with_ctx = 0
        for method in methods_to_check:
            # Match: func (s *ProductService) MethodName(ctx context.Context
            # or: func (s *ProductService) MethodName(c context.Context
            pattern = rf'func\s+\([^)]+\)\s+{method}\s*\(\s*\w+\s+context\.Context'
            if re.search(pattern, service_content):
                methods_with_ctx += 1
            else:
                print(f"  INFO: {method} missing context.Context as first param")

        if has_context_import and methods_with_ctx == 4:
            print(f"PASS: Component 3 — All 4 methods accept context.Context (0.20 pts)")
            total_score += 0.20
        elif methods_with_ctx > 0:
            partial = 0.20 * (methods_with_ctx / 4)
            print(f"PARTIAL: Component 3 — {methods_with_ctx}/4 methods have context.Context ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No methods accept context.Context (import={has_context_import})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # =========================================================================
    # Component 4: Service uses slog instead of log.Printf (0.15)
    # =========================================================================
    try:
        uses_slog = bool(re.search(r'slog\.(Info|Error|Warn|Debug)\s*\(', service_content))
        imports_slog = bool(re.search(r'"log/slog"', service_content))
        uses_log_printf = bool(re.search(r'log\.Printf\s*\(', service_content))
        imports_old_log = bool(re.search(r'"log"', service_content) and
                               not re.search(r'"log/slog"', service_content))
        # Allow "log" import only if it's "log/slog"
        # Check: no standalone "log" import (that isn't log/slog)
        has_standalone_log = any(
            match.group(1) == 'log'
            for match in re.finditer(r'"(log(?:/\w+)?)"', service_content)
        )

        if uses_slog and imports_slog and not uses_log_printf:
            print(f"PASS: Component 4 — Uses slog, no log.Printf (0.15 pts)")
            total_score += 0.15
        elif uses_slog and not uses_log_printf:
            print(f"PARTIAL: Component 4 — Uses slog but import unclear (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 — uses_slog={uses_slog}, uses_log_printf={uses_log_printf}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # =========================================================================
    # Component 5: FindAll has pagination (page, pageSize + paginated result) (0.15)
    # =========================================================================
    try:
        # Check FindAll signature includes page and pageSize params
        findall_pattern = re.search(
            r'func\s+\([^)]+\)\s+FindAll\s*\(([^)]+)\)',
            service_content
        )
        if findall_pattern:
            params = findall_pattern.group(1)
            has_page = bool(re.search(r'page\b', params))
            has_page_size = bool(re.search(r'pageSize\b', params))

            # Check return type includes a paginated result struct (not just a slice)
            # Look for PaginatedResult or similar struct in return
            findall_line_match = re.search(
                r'func\s+\([^)]+\)\s+FindAll\s*\([^)]+\)\s*\(([^)]+)\)',
                service_content
            )
            returns_paginated = False
            if findall_line_match:
                return_types = findall_line_match.group(1)
                # Should return something like *PaginatedResult or *repository.PaginatedResult
                returns_paginated = bool(re.search(r'PaginatedResult', return_types) or
                                        re.search(r'Paginated', return_types))

            # Also check if there's a PaginatedResult struct defined (maybe in repo file)
            repo_content_for_struct = read_file(REPO_FILE)
            has_paginated_struct = False
            if repo_content_for_struct:
                has_paginated_struct = bool(re.search(r'PaginatedResult\s+struct', repo_content_for_struct))
                if has_paginated_struct:
                    has_items = bool(re.search(r'Items\b', repo_content_for_struct))
                    has_total = bool(re.search(r'Total\b', repo_content_for_struct))
                    has_paginated_struct = has_items and has_total

            if has_page and has_page_size and (returns_paginated or has_paginated_struct):
                print(f"PASS: Component 5 — FindAll has pagination with page/pageSize and PaginatedResult (0.15 pts)")
                total_score += 0.15
            elif has_page and has_page_size:
                print(f"PARTIAL: Component 5 — FindAll has page/pageSize but no PaginatedResult struct (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — FindAll missing pagination params (page={has_page}, pageSize={has_page_size})")
        else:
            print(f"FAIL: Component 5 — Could not find FindAll method signature")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # =========================================================================
    # Component 6: Test file with MockProductRepository (0.15)
    # =========================================================================
    try:
        test_content = read_file(TEST_FILE)
        if test_content is not None:
            has_mock = bool(re.search(r'MockProductRepository', test_content))
            has_struct = bool(re.search(r'MockProductRepository\s+struct', test_content) or
                             re.search(r'type\s+MockProductRepository\s+struct', test_content))
            has_test_funcs = bool(re.search(r'func\s+Test\w+\s*\(\s*t\s+\*testing\.T\s*\)', test_content))
            # Check it implements the interface methods
            impl_methods = 0
            for m in ['FindByID', 'FindAll', 'Save', 'Delete']:
                if re.search(rf'func\s+\(\s*\w+\s+\*MockProductRepository\s*\)\s+{m}\s*\(', test_content):
                    impl_methods += 1

            if has_mock and has_struct and has_test_funcs and impl_methods == 4:
                print(f"PASS: Component 6 — Test file with MockProductRepository implementing all 4 methods (0.15 pts)")
                total_score += 0.15
            elif has_mock and has_test_funcs:
                partial = 0.10
                print(f"PARTIAL: Component 6 — Test file with mock but incomplete implementation ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 6 — has_mock={has_mock}, has_struct={has_struct}, has_test_funcs={has_test_funcs}, impl_methods={impl_methods}")
        else:
            print(f"FAIL: Component 6 — Test file not found at {TEST_FILE}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

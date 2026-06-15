"""
Reward Script: SQL-like query language for in-memory data in Go
Task ID: vscode_gf4_086
Domain: vscode
Scoring:
  C1: go.mod with correct module name (0.10)
  C2: lexer.go tokenizes SQL keywords (0.15)
  C3: parser.go has QueryAST struct hierarchy (0.15)
  C4: executor.go has execution logic with filter/sort/join (0.15)
  C5: functions.go has 8 built-in functions (0.15)
  C6: 20+ test functions across test files (0.15)
  C7: go test ./... passes (0.15)
"""

import os
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'go-query-language')
TASK_ID = 'vscode_gf4_086'


def read_file(path):
    """Read file contents, return empty string if not found."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception:
        return ''


def verify_task():
    total_score = 0.0

    # Component 1: go.mod exists with module github.com/user/go-query (0.10 points)
    try:
        gomod_path = os.path.join(PROJECT, 'go.mod')
        gomod = read_file(gomod_path)
        if gomod and 'module github.com/user/go-query' in gomod:
            print(f"PASS: Component 1 — go.mod has module github.com/user/go-query (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — go.mod missing or wrong module. Content: {gomod[:200]}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: lexer.go tokenizes SQL keywords (0.15 points)
    # Must contain token types for SELECT, FROM, WHERE, ORDER, GROUP, LIMIT, JOIN
    try:
        lexer_path = os.path.join(PROJECT, 'pkg', 'parser', 'lexer.go')
        lexer = read_file(lexer_path)
        if not lexer:
            print(f"FAIL: Component 2 — lexer.go not found at {lexer_path}")
        else:
            required_keywords = ['SELECT', 'FROM', 'WHERE', 'ORDER', 'GROUP', 'LIMIT', 'JOIN']
            found = [kw for kw in required_keywords if kw in lexer]
            if len(found) >= 6:
                # Also verify it has a Lexer/tokenizer type and tokenization logic
                has_tokenizer = ('Tokenize' in lexer or 'Lex' in lexer or 'NextToken' in lexer
                                 or 'tokenize' in lexer or 'Token' in lexer)
                if has_tokenizer:
                    print(f"PASS: Component 2 — lexer.go has {len(found)}/7 keywords and tokenizer (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 2 — lexer.go has keywords but no tokenizer logic")
            else:
                print(f"FAIL: Component 2 — lexer.go only has {len(found)}/7 keywords: {found}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: parser.go has QueryAST with SelectStmt, Fields, Source, WhereClause, OrderBy, Limit (0.15 points)
    try:
        parser_path = os.path.join(PROJECT, 'pkg', 'parser', 'parser.go')
        parser_code = read_file(parser_path)
        if not parser_code:
            print(f"FAIL: Component 3 — parser.go not found at {parser_path}")
        else:
            required_types = ['QueryAST', 'SelectStmt', 'Field', 'Source', 'WhereClause', 'OrderBy', 'Limit']
            found = [t for t in required_types if t in parser_code]
            # Also check for parse function
            has_parser = ('Parse' in parser_code or 'parse' in parser_code)
            if len(found) >= 5 and has_parser:
                print(f"PASS: Component 3 — parser.go has {len(found)}/7 AST types and parser (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — parser.go has {len(found)}/7 AST types, parser={has_parser}. Found: {found}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: executor.go has execution logic with filter, sort, project, limit, join (0.15 points)
    try:
        exec_path = os.path.join(PROJECT, 'pkg', 'executor', 'executor.go')
        executor = read_file(exec_path)
        if not executor:
            print(f"FAIL: Component 4 — executor.go not found at {exec_path}")
        else:
            capabilities = {
                'execute': 'Execute' in executor or 'execute' in executor,
                'filter': 'filter' in executor.lower() or 'where' in executor.lower(),
                'sort': 'sort' in executor.lower() or 'order' in executor.lower(),
                'join': 'join' in executor.lower() or 'Join' in executor,
                'limit': 'limit' in executor.lower() or 'Limit' in executor,
            }
            passed = sum(1 for v in capabilities.values() if v)
            if passed >= 4:
                print(f"PASS: Component 4 — executor.go has {passed}/5 capabilities: {capabilities} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — executor.go only has {passed}/5 capabilities: {capabilities}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: functions.go has 8 built-in functions: COUNT, SUM, AVG, MAX, MIN, CONCAT, UPPER, LOWER (0.15 points)
    try:
        func_path = os.path.join(PROJECT, 'pkg', 'executor', 'functions.go')
        functions = read_file(func_path)
        if not functions:
            print(f"FAIL: Component 5 — functions.go not found at {func_path}")
        else:
            required_funcs = ['COUNT', 'SUM', 'AVG', 'MAX', 'MIN', 'CONCAT', 'UPPER', 'LOWER']
            found = [fn for fn in required_funcs if fn in functions]
            if len(found) >= 7:
                print(f"PASS: Component 5 — functions.go has {len(found)}/8 built-in functions (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 — functions.go only has {len(found)}/8 functions: {found}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: 20+ test functions across test files (0.15 points)
    try:
        test_files = [
            os.path.join(PROJECT, 'pkg', 'parser', 'lexer_test.go'),
            os.path.join(PROJECT, 'pkg', 'parser', 'parser_test.go'),
            os.path.join(PROJECT, 'pkg', 'executor', 'executor_test.go'),
        ]
        total_tests = 0
        for tf in test_files:
            content = read_file(tf)
            if content:
                # Count Go test functions: func TestXxx(t *testing.T)
                matches = re.findall(r'func\s+Test\w+', content)
                total_tests += len(matches)

        # Also check for any additional test files
        for root, dirs, files in os.walk(PROJECT):
            for f in files:
                fp = os.path.join(root, f)
                if fp.endswith('_test.go') and fp not in test_files:
                    content = read_file(fp)
                    if content:
                        matches = re.findall(r'func\s+Test\w+', content)
                        total_tests += len(matches)

        if total_tests >= 20:
            print(f"PASS: Component 6 — {total_tests} test functions found (>= 20) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 6 — only {total_tests} test functions found (need >= 20)")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: go test ./... passes (0.15 points)
    try:
        go_binary = '/home/user/go-sdk/go/bin/go'
        if not os.path.exists(go_binary):
            for candidate in ['/usr/local/go/bin/go', '/usr/bin/go', '/snap/bin/go']:
                if os.path.exists(candidate):
                    go_binary = candidate
                    break

        if os.path.exists(go_binary):
            # Use os.popen to run go test (no subprocess import needed)
            cmd = (
                f'cd {PROJECT} && '
                f'PATH={os.path.dirname(go_binary)}:$PATH '
                f'GOPATH={WORKDIR}/go '
                f'HOME={WORKDIR} '
                f'{go_binary} test ./... 2>&1'
            )
            pipe = os.popen(cmd)
            output = pipe.read()
            rc = pipe.close()  # None means success (rc=0)
            if rc is None:
                print(f"PASS: Component 7 — go test ./... passed (0.15 pts)")
                print(f"  output: {output[:300]}")
                total_score += 0.15
            else:
                print(f"FAIL: Component 7 — go test ./... failed (rc={rc})")
                print(f"  output: {output[:300]}")
        else:
            print(f"FAIL: Component 7 — go binary not found")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint
if not os.path.isdir(PROJECT):
    print(f"Project directory not found: {PROJECT}")
    print("REWARD: 0.0")
else:
    verify_task()

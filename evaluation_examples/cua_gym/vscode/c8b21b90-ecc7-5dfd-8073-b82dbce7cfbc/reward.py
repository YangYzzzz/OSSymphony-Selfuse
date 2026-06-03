"""
Reward Script: Implement a simple programming language interpreter
Task ID: vscode_gf4_089
Domain: vscode
Scoring:
  - Component 1: venv with pytest installed (0.10)
  - Component 2: src/lexer.py with required token types and keywords (0.15)
  - Component 3: src/parser.py with 12+ AST node types (0.15)
  - Component 4: src/evaluator.py with Environment, Closure, builtins (0.15)
  - Component 5: src/repl.py with REPL functionality (0.10)
  - Component 6: 20+ test functions in tests/ (0.15)
  - Component 7: pytest passes all tests (0.20)
"""

import os
import re
import ast as python_ast

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'python-interpreter')
SRC = os.path.join(PROJECT, 'src')
VENV = os.path.join(PROJECT, 'venv')


def count_test_functions(test_dir):
    """Count test methods/functions across all test files in the directory."""
    count = 0
    if not os.path.isdir(test_dir):
        return 0
    for fname in os.listdir(test_dir):
        if fname.startswith('test_') and fname.endswith('.py'):
            fpath = os.path.join(test_dir, fname)
            try:
                with open(fpath) as f:
                    content = f.read()
                tree = python_ast.parse(content)
                for node in python_ast.walk(tree):
                    # standalone test functions
                    if isinstance(node, python_ast.FunctionDef) and node.name.startswith('test_'):
                        count += 1
            except Exception:
                pass
    return count


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: venv with pytest installed (0.10 points)
    # Initial env has NO venv, so this only passes on golden
    try:
        pytest_bin = os.path.join(VENV, 'bin', 'pytest')
        if os.path.isdir(VENV) and os.path.isfile(pytest_bin):
            print(f"PASS: Component 1 - venv exists with pytest at {pytest_bin} (0.10 pts)")
            total_score += 0.10
        else:
            venv_exists = os.path.isdir(VENV)
            pytest_exists = os.path.isfile(pytest_bin)
            print(f"FAIL: Component 1 - venv exists: {venv_exists}, pytest binary: {pytest_exists}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: src/lexer.py with required token types and keywords (0.15 points)
    # Initial env has only __init__.py in src/, so lexer.py only exists on golden
    try:
        lexer_path = os.path.join(SRC, 'lexer.py')
        if not os.path.isfile(lexer_path):
            print(f"FAIL: Component 2 - lexer.py not found")
        else:
            with open(lexer_path) as f:
                content = f.read()

            # Check for required token types
            required_tokens = ['INTEGER', 'STRING', 'IDENTIFIER', 'PLUS', 'MINUS',
                               'STAR', 'SLASH', 'EQ', 'LT', 'GT', 'LE', 'GE']
            found_tokens = [t for t in required_tokens if re.search(rf'\b{t}\b', content)]

            # Check for required keywords
            required_keywords = ['let', 'if', 'else', 'while', 'func', 'return', 'print']
            found_keywords = [k for k in required_keywords if f"'{k}'" in content or f'"{k}"' in content]

            # Check for Lexer/tokenize class/method
            has_lexer_class = 'class Lexer' in content
            has_tokenize = 'def tokenize' in content or 'def lex' in content

            token_ratio = len(found_tokens) / len(required_tokens)
            keyword_ratio = len(found_keywords) / len(required_keywords)

            if token_ratio >= 0.8 and keyword_ratio >= 0.8 and has_lexer_class and has_tokenize:
                print(f"PASS: Component 2 - lexer.py has {len(found_tokens)}/{len(required_tokens)} tokens, "
                      f"{len(found_keywords)}/{len(required_keywords)} keywords, Lexer class present (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 - tokens: {len(found_tokens)}/{len(required_tokens)}, "
                      f"keywords: {len(found_keywords)}/{len(required_keywords)}, "
                      f"Lexer class: {has_lexer_class}, tokenize: {has_tokenize}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: src/parser.py with 12+ AST node types via recursive descent (0.15 points)
    # Initial env has no parser.py
    try:
        parser_path = os.path.join(SRC, 'parser.py')
        if not os.path.isfile(parser_path):
            print(f"FAIL: Component 3 - parser.py not found")
        else:
            with open(parser_path) as f:
                content = f.read()

            # Required AST node types from the task spec
            required_nodes = [
                'Program', 'LetStatement', 'IfStatement', 'WhileStatement',
                'FunctionDecl', 'ReturnStatement', 'ExpressionStatement',
                'BinaryOp', 'UnaryOp', 'FuncCall', 'Identifier',
                'IntLiteral', 'StringLiteral'
            ]
            found_nodes = [n for n in required_nodes if re.search(rf'class\s+{n}', content)]

            has_parser_class = 'class Parser' in content
            # Check for recursive descent pattern (parse methods)
            parse_methods = re.findall(r'def\s+parse_\w+', content)

            if len(found_nodes) >= 12 and has_parser_class and len(parse_methods) >= 3:
                print(f"PASS: Component 3 - parser.py has {len(found_nodes)}/{len(required_nodes)} AST nodes, "
                      f"Parser class, {len(parse_methods)} parse methods (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 - AST nodes: {len(found_nodes)}/{len(required_nodes)}, "
                      f"Parser class: {has_parser_class}, parse methods: {len(parse_methods)}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: src/evaluator.py with Environment, Closure, builtins (0.15 points)
    # Initial env has no evaluator.py
    try:
        eval_path = os.path.join(SRC, 'evaluator.py')
        if not os.path.isfile(eval_path):
            print(f"FAIL: Component 4 - evaluator.py not found")
        else:
            with open(eval_path) as f:
                content = f.read()

            has_environment = bool(re.search(r'class\s+Environment', content))
            has_closure = bool(re.search(r'class\s+Closure', content)) or 'closure' in content.lower()
            has_evaluator = bool(re.search(r'class\s+Evaluator', content))

            # Check for builtins: print, len, type
            has_builtin_print = 'print' in content and ('builtin' in content.lower() or '_builtin_print' in content)
            has_builtin_len = 'len' in content and ('builtin' in content.lower() or '_builtin_len' in content)
            has_builtin_type = "'type'" in content or '"type"' in content or '_builtin_type' in content

            # Check for variable scoping (parent chain)
            has_scoping = 'parent' in content

            checks = [has_environment, has_closure, has_evaluator,
                       has_builtin_print, has_builtin_len, has_builtin_type, has_scoping]
            passed = sum(checks)

            if passed >= 5:
                print(f"PASS: Component 4 - evaluator.py: Environment={has_environment}, "
                      f"Closure={has_closure}, Evaluator={has_evaluator}, "
                      f"builtins(print={has_builtin_print}, len={has_builtin_len}, type={has_builtin_type}), "
                      f"scoping={has_scoping} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 - only {passed}/7 checks passed: "
                      f"Environment={has_environment}, Closure={has_closure}, Evaluator={has_evaluator}, "
                      f"builtins(print={has_builtin_print}, len={has_builtin_len}, type={has_builtin_type}), "
                      f"scoping={has_scoping}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: src/repl.py with REPL functionality (0.10 points)
    # Initial env has no repl.py
    try:
        repl_path = os.path.join(SRC, 'repl.py')
        if not os.path.isfile(repl_path):
            print(f"FAIL: Component 5 - repl.py not found")
        else:
            with open(repl_path) as f:
                content = f.read()

            has_repl_func = bool(re.search(r'def\s+repl', content))
            has_input_loop = 'input(' in content
            has_eval_integration = ('Evaluator' in content or 'evaluator' in content or
                                     'eval' in content or 'run_source' in content)

            if has_repl_func and has_input_loop and has_eval_integration:
                print(f"PASS: Component 5 - repl.py has REPL function with input loop and eval integration (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 - repl func: {has_repl_func}, "
                      f"input loop: {has_input_loop}, eval integration: {has_eval_integration}")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: 20+ test functions in tests/ (0.15 points)
    # Initial env has no tests directory
    try:
        tests_dir = os.path.join(PROJECT, 'tests')
        if not os.path.isdir(tests_dir):
            print(f"FAIL: Component 6 - tests/ directory not found")
        else:
            test_count = count_test_functions(tests_dir)
            if test_count >= 20:
                print(f"PASS: Component 6 - found {test_count} test functions (>= 20 required) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 6 - found {test_count} test functions, need >= 20")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    # Component 7: pytest passes all tests (0.20 points)
    # Initial env has no tests and no venv, so this fails on initial
    try:
        pytest_bin = os.path.join(VENV, 'bin', 'pytest')
        tests_dir = os.path.join(PROJECT, 'tests')
        if not os.path.isfile(pytest_bin) or not os.path.isdir(tests_dir):
            print(f"FAIL: Component 7 - prerequisites missing (pytest: {os.path.isfile(pytest_bin)}, "
                  f"tests: {os.path.isdir(tests_dir)})")
        else:
            # Run pytest via os.popen (no subprocess import needed)
            result = os.popen(
                f'cd {PROJECT} && {pytest_bin} tests/ --tb=short 2>&1'
            ).read()

            # Parse pytest output for pass/fail
            passed_match = re.search(r'(\d+)\s+passed', result)
            failed_match = re.search(r'(\d+)\s+failed', result)

            passed_count = int(passed_match.group(1)) if passed_match else 0
            failed_count = int(failed_match.group(1)) if failed_match else 0

            if passed_count >= 20 and failed_count == 0:
                print(f"PASS: Component 7 - pytest: {passed_count} passed, 0 failed (0.20 pts)")
                total_score += 0.20
            elif passed_count > 0 and failed_count == 0:
                # Partial credit: tests pass but fewer than 20
                partial = 0.20 * (passed_count / 20.0)
                partial = min(partial, 0.20)
                print(f"PARTIAL: Component 7 - pytest: {passed_count} passed, {failed_count} failed ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 7 - pytest: {passed_count} passed, {failed_count} failed")
                print(f"  Output tail: {result[-500:]}")
    except Exception as e:
        print(f"ERROR: Component 7 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

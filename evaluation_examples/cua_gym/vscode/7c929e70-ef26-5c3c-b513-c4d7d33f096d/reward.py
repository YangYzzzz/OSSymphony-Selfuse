"""
Reward Script: Go Template Engine Implementation
Task ID: vscode_gf4_057
Domain: vscode
Scoring:
  - C1 (0.10): go.mod exists with correct module path
  - C2 (0.15): pkg/lexer/lexer.go tokenizes template syntax
  - C3 (0.15): pkg/parser/parser.go builds AST with required node types
  - C4 (0.15): pkg/renderer/renderer.go uses reflection for variable lookup
  - C5 (0.10): pkg/engine/engine.go provides caching template engine
  - C6 (0.05): cmd/demo/main.go exists and renders HTML templates
  - C7 (0.10): 20+ test functions across test files
  - C8 (0.20): go test ./... passes (all tests green)
"""

import os

WORKDIR = '/home/user/projects/go-template-engine'
TASK_ID = 'vscode_gf4_057'
GO_BIN = '/home/user/go-sdk/go/bin/go'


def read_file(path):
    """Read file content, return empty string if not found."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception:
        return ''


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: go.mod exists with correct module path (0.10 points)
    try:
        gomod_path = os.path.join(WORKDIR, 'go.mod')
        content = read_file(gomod_path)
        if content and 'module github.com/user/go-template' in content:
            print(f"PASS: Component 1 -- go.mod has module github.com/user/go-template (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 -- go.mod missing or wrong module path. Content: {content[:200]}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: pkg/lexer/lexer.go tokenizes template syntax (0.15 points)
    try:
        lexer_path = os.path.join(WORKDIR, 'pkg', 'lexer', 'lexer.go')
        content = read_file(lexer_path)
        if not content:
            print(f"FAIL: Component 2 -- pkg/lexer/lexer.go not found")
        else:
            checks = {
                'package lexer': 'package declaration',
                'TokenType': 'TokenType definition',
                'Variable': 'Variable token type',
                'IfOpen': 'IfOpen or If token',
                'EachOpen': 'EachOpen or Each token',
            }
            passed = sum(1 for k in checks if k in content)
            if passed >= 4:
                print(f"PASS: Component 2 -- lexer.go has {passed}/5 expected elements (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 -- lexer.go only has {passed}/5 expected elements")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: pkg/parser/parser.go builds AST with required node types (0.15 points)
    try:
        parser_path = os.path.join(WORKDIR, 'pkg', 'parser', 'parser.go')
        content = read_file(parser_path)
        if not content:
            print(f"FAIL: Component 3 -- pkg/parser/parser.go not found")
        else:
            node_types = ['TextNode', 'VariableNode', 'IfNode', 'EachNode']
            found = [nt for nt in node_types if nt in content]
            if len(found) >= 4:
                print(f"PASS: Component 3 -- parser.go has all 4 AST node types: {found} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 -- parser.go has {len(found)}/4 node types: {found}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: pkg/renderer/renderer.go uses reflection for variable lookup (0.15 points)
    try:
        renderer_path = os.path.join(WORKDIR, 'pkg', 'renderer', 'renderer.go')
        content = read_file(renderer_path)
        if not content:
            print(f"FAIL: Component 4 -- pkg/renderer/renderer.go not found")
        else:
            has_reflect = '"reflect"' in content or 'reflect.' in content
            has_render = 'func Render' in content or 'func render' in content
            has_parser_import = 'parser' in content
            if has_reflect and has_render and has_parser_import:
                print(f"PASS: Component 4 -- renderer.go uses reflect and has Render function (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 -- renderer.go: reflect={has_reflect}, render_func={has_render}, parser_import={has_parser_import}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: pkg/engine/engine.go provides caching template engine (0.10 points)
    try:
        engine_path = os.path.join(WORKDIR, 'pkg', 'engine', 'engine.go')
        content = read_file(engine_path)
        if not content:
            print(f"FAIL: Component 5 -- pkg/engine/engine.go not found")
        else:
            has_cache = 'cache' in content.lower()
            has_sync = 'sync' in content
            has_render = 'Render' in content
            if has_cache and has_render:
                print(f"PASS: Component 5 -- engine.go has caching and Render (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 -- engine.go: cache={has_cache}, sync={has_sync}, render={has_render}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: cmd/demo/main.go exists and uses engine (0.05 points)
    try:
        demo_path = os.path.join(WORKDIR, 'cmd', 'demo', 'main.go')
        content = read_file(demo_path)
        if not content:
            print(f"FAIL: Component 6 -- cmd/demo/main.go not found")
        else:
            has_main = 'func main()' in content
            has_html = '<html>' in content.lower() or 'html' in content.lower()
            if has_main and has_html:
                print(f"PASS: Component 6 -- cmd/demo/main.go exists with HTML template rendering (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 6 -- cmd/demo/main.go: main_func={has_main}, html_template={has_html}")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    # Component 7: 20+ test functions across test files (0.10 points)
    try:
        test_count = 0
        test_dirs = [
            os.path.join(WORKDIR, 'pkg', 'lexer'),
            os.path.join(WORKDIR, 'pkg', 'parser'),
            os.path.join(WORKDIR, 'pkg', 'renderer'),
            os.path.join(WORKDIR, 'pkg', 'engine'),
        ]
        for d in test_dirs:
            if not os.path.isdir(d):
                continue
            for fname in os.listdir(d):
                if fname.endswith('_test.go'):
                    fpath = os.path.join(d, fname)
                    content = read_file(fpath)
                    # Count func TestXxx( patterns
                    import re
                    tests = re.findall(r'func\s+Test\w+\s*\(', content)
                    test_count += len(tests)

        if test_count >= 20:
            print(f"PASS: Component 7 -- Found {test_count} test functions (>= 20 required) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 7 -- Found {test_count} test functions, need >= 20")
    except Exception as e:
        print(f"ERROR: Component 7 -- {e}")

    # Component 8: go test ./... passes (0.20 points)
    try:
        # Find go binary
        go_bin = None
        for candidate in [GO_BIN, '/usr/local/go/bin/go', '/snap/bin/go']:
            if os.path.isfile(candidate):
                go_bin = candidate
                break

        if go_bin is None:
            print(f"FAIL: Component 8 -- Go binary not found")
        else:
            go_dir = os.path.dirname(go_bin)
            go_root = os.path.dirname(go_dir)
            cmd = (
                f'export PATH={go_dir}:$PATH && '
                f'export GOROOT={go_root} && '
                f'cd {WORKDIR} && '
                f'{go_bin} test ./... 2>&1'
            )
            pipe = os.popen(cmd)
            output = pipe.read()
            rc = pipe.close()
            # os.popen returns None on success (rc=0)
            if rc is None:
                print(f"PASS: Component 8 -- go test ./... passed (0.20 pts)")
                print(f"  output: {output.strip()[:500]}")
                total_score += 0.20
            else:
                print(f"FAIL: Component 8 -- go test ./... failed (rc={rc})")
                print(f"  output: {output.strip()[:500]}")
    except Exception as e:
        print(f"ERROR: Component 8 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.isdir(WORKDIR):
    print(f"Directory not found: {WORKDIR}")
    print("REWARD: 0.0")
else:
    verify_task()

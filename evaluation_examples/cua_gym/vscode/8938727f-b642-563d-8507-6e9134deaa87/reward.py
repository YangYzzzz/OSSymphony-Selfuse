"""
Reward Script: Rust compile-time dispatch project implementation
Task ID: vscode_gf4_063
Domain: vscode
Scoring:
  C1 (0.15) - Cargo.toml has serde (with derive), serde_json, criterion deps
  C2 (0.30) - src/shapes.rs: Shape trait + Circle, Rectangle, Triangle, Hexagon impls
  C3 (0.20) - src/pipeline.rs: generic Pipeline<S: Shape> with transform, filter, collect
  C4 (0.10) - src/serialization.rs: generic serialize_shapes function
  C5 (0.15) - benches/dispatch_bench.rs: dynamic vs static dispatch benchmarks
  C6 (0.10) - tests/ directory with 10+ tests
"""

import os
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'rust-compile-time-dispatch')


def verify_task():
    total_score = 0.0

    # =========================================================================
    # Component 1: Cargo.toml has serde, serde_json, criterion (0.15 pts)
    # =========================================================================
    try:
        cargo_path = os.path.join(PROJECT, 'Cargo.toml')
        if not os.path.exists(cargo_path):
            print("FAIL: C1 - Cargo.toml not found")
        else:
            with open(cargo_path, 'r') as f:
                cargo_content = f.read()

            # C1a: serde with derive feature (0.05 pts)
            if re.search(r'serde\s*=\s*\{.*features\s*=\s*\[.*"derive".*\]', cargo_content, re.DOTALL):
                print("PASS: C1a - serde with derive feature found (0.05 pts)")
                total_score += 0.05
            else:
                print("FAIL: C1a - serde with derive feature not found")

            # C1b: serde_json dependency (0.05 pts)
            if re.search(r'serde_json\s*=', cargo_content):
                print("PASS: C1b - serde_json dependency found (0.05 pts)")
                total_score += 0.05
            else:
                print("FAIL: C1b - serde_json dependency not found")

            # C1c: criterion as dev-dependency (0.05 pts)
            if re.search(r'\[dev-dependencies\]', cargo_content) and re.search(r'criterion\s*=', cargo_content):
                print("PASS: C1c - criterion dev-dependency found (0.05 pts)")
                total_score += 0.05
            else:
                print("FAIL: C1c - criterion dev-dependency not found")
    except Exception as e:
        print(f"ERROR: C1 - {e}")

    # =========================================================================
    # Component 2: src/shapes.rs with Shape trait and 4 shape impls (0.30 pts)
    # =========================================================================
    try:
        shapes_path = os.path.join(PROJECT, 'src', 'shapes.rs')
        if not os.path.exists(shapes_path):
            print("FAIL: C2 - src/shapes.rs not found")
        else:
            with open(shapes_path, 'r') as f:
                shapes_content = f.read()

            # C2a: Shape trait with area, perimeter, name methods (0.10 pts)
            has_trait = bool(re.search(r'trait\s+Shape', shapes_content))
            has_area = bool(re.search(r'fn\s+area\s*\(', shapes_content))
            has_perimeter = bool(re.search(r'fn\s+perimeter\s*\(', shapes_content))
            has_name = bool(re.search(r'fn\s+name\s*\(', shapes_content))

            if has_trait and has_area and has_perimeter and has_name:
                print("PASS: C2a - Shape trait with area(), perimeter(), name() methods (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: C2a - Shape trait incomplete (trait={has_trait}, area={has_area}, perimeter={has_perimeter}, name={has_name})")

            # C2b: 4 shape implementations (0.12 pts)
            shapes_required = ['Circle', 'Rectangle', 'Triangle', 'Hexagon']
            shapes_found = []
            for shape in shapes_required:
                if re.search(rf'impl\s+Shape\s+for\s+{shape}', shapes_content):
                    shapes_found.append(shape)

            if len(shapes_found) == 4:
                print(f"PASS: C2b - All 4 Shape impls found: {shapes_found} (0.12 pts)")
                total_score += 0.12
            elif len(shapes_found) >= 2:
                print(f"PARTIAL: C2b - {len(shapes_found)}/4 Shape impls found: {shapes_found} (0.06 pts)")
                total_score += 0.06
            else:
                print(f"FAIL: C2b - Only {len(shapes_found)}/4 Shape impls found: {shapes_found}")

            # C2c: Serialize derive on structs (0.08 pts)
            serialize_count = len(re.findall(r'#\[derive\([^\]]*Serialize[^\]]*\)\]', shapes_content))
            if serialize_count >= 4:
                print(f"PASS: C2c - {serialize_count} structs have Serialize derive (0.08 pts)")
                total_score += 0.08
            elif serialize_count >= 2:
                print(f"PARTIAL: C2c - {serialize_count}/4 structs have Serialize derive (0.04 pts)")
                total_score += 0.04
            else:
                print(f"FAIL: C2c - Only {serialize_count}/4 structs have Serialize derive")
    except Exception as e:
        print(f"ERROR: C2 - {e}")

    # =========================================================================
    # Component 3: src/pipeline.rs with generic Pipeline (0.20 pts)
    # =========================================================================
    try:
        pipeline_path = os.path.join(PROJECT, 'src', 'pipeline.rs')
        if not os.path.exists(pipeline_path):
            print("FAIL: C3 - src/pipeline.rs not found")
        else:
            with open(pipeline_path, 'r') as f:
                pipeline_content = f.read()

            # C3a: Pipeline struct with generic Shape bound (0.06 pts)
            if re.search(r'struct\s+Pipeline\s*<\s*S\s*:\s*Shape\s*>', pipeline_content):
                print("PASS: C3a - Pipeline<S: Shape> struct found (0.06 pts)")
                total_score += 0.06
            else:
                print("FAIL: C3a - Pipeline<S: Shape> struct not found")

            # C3b: transform method with generic closure (0.05 pts)
            if re.search(r'fn\s+transform\s*<\s*F\s*:', pipeline_content):
                print("PASS: C3b - transform method with generic F found (0.05 pts)")
                total_score += 0.05
            else:
                print("FAIL: C3b - transform method not found")

            # C3c: filter method with generic predicate (0.05 pts)
            if re.search(r'fn\s+filter\s*<\s*P\s*:', pipeline_content):
                print("PASS: C3c - filter method with generic P found (0.05 pts)")
                total_score += 0.05
            else:
                print("FAIL: C3c - filter method not found")

            # C3d: collect method (0.04 pts)
            if re.search(r'fn\s+collect\s*\(', pipeline_content):
                print("PASS: C3d - collect method found (0.04 pts)")
                total_score += 0.04
            else:
                print("FAIL: C3d - collect method not found")
    except Exception as e:
        print(f"ERROR: C3 - {e}")

    # =========================================================================
    # Component 4: src/serialization.rs with serialize_shapes (0.10 pts)
    # =========================================================================
    try:
        ser_path = os.path.join(PROJECT, 'src', 'serialization.rs')
        if not os.path.exists(ser_path):
            print("FAIL: C4 - src/serialization.rs not found")
        else:
            with open(ser_path, 'r') as f:
                ser_content = f.read()

            # C4a: serialize_shapes with generic bounds (0.07 pts)
            if re.search(r'fn\s+serialize_shapes\s*<\s*S\s*:\s*Shape\s*\+\s*Serialize\s*>', ser_content):
                print("PASS: C4a - serialize_shapes<S: Shape + Serialize> found (0.07 pts)")
                total_score += 0.07
            elif re.search(r'fn\s+serialize_shapes', ser_content):
                print("PARTIAL: C4a - serialize_shapes found but generic signature doesn't match (0.03 pts)")
                total_score += 0.03
            else:
                print("FAIL: C4a - serialize_shapes function not found")

            # C4b: return type is String (0.03 pts)
            if re.search(r'fn\s+serialize_shapes.*->\s*String', ser_content):
                print("PASS: C4b - serialize_shapes returns String (0.03 pts)")
                total_score += 0.03
            else:
                print("FAIL: C4b - serialize_shapes does not appear to return String")
    except Exception as e:
        print(f"ERROR: C4 - {e}")

    # =========================================================================
    # Component 5: benches/dispatch_bench.rs with benchmarks (0.15 pts)
    # =========================================================================
    try:
        bench_path = os.path.join(PROJECT, 'benches', 'dispatch_bench.rs')
        if not os.path.exists(bench_path):
            print("FAIL: C5 - benches/dispatch_bench.rs not found")
        else:
            with open(bench_path, 'r') as f:
                bench_content = f.read()

            # C5a: criterion usage (0.05 pts)
            if re.search(r'use\s+criterion', bench_content):
                print("PASS: C5a - criterion import found (0.05 pts)")
                total_score += 0.05
            else:
                print("FAIL: C5a - criterion import not found")

            # C5b: static dispatch benchmark (0.05 pts)
            if re.search(r'static.?dispatch', bench_content, re.IGNORECASE):
                print("PASS: C5b - static dispatch benchmark found (0.05 pts)")
                total_score += 0.05
            else:
                print("FAIL: C5b - static dispatch benchmark not found")

            # C5c: dynamic dispatch benchmark (0.05 pts)
            if re.search(r'dynamic.?dispatch', bench_content, re.IGNORECASE) or re.search(r'Box\s*<\s*dyn\s+Shape\s*>', bench_content):
                print("PASS: C5c - dynamic dispatch benchmark found (0.05 pts)")
                total_score += 0.05
            else:
                print("FAIL: C5c - dynamic dispatch benchmark not found")
    except Exception as e:
        print(f"ERROR: C5 - {e}")

    # =========================================================================
    # Component 6: tests/ with 10+ tests (0.10 pts)
    # =========================================================================
    try:
        tests_dir = os.path.join(PROJECT, 'tests')
        if not os.path.isdir(tests_dir):
            print("FAIL: C6 - tests/ directory not found")
        else:
            # Count #[test] annotations across all .rs files in tests/
            test_count = 0
            for fname in os.listdir(tests_dir):
                if fname.endswith('.rs'):
                    fpath = os.path.join(tests_dir, fname)
                    with open(fpath, 'r') as f:
                        content = f.read()
                    test_count += len(re.findall(r'#\[test\]', content))

            if test_count >= 10:
                print(f"PASS: C6 - {test_count} tests found (>= 10 required) (0.10 pts)")
                total_score += 0.10
            elif test_count >= 5:
                print(f"PARTIAL: C6 - {test_count} tests found (>= 10 required) (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: C6 - Only {test_count} tests found (>= 10 required)")
    except Exception as e:
        print(f"ERROR: C6 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

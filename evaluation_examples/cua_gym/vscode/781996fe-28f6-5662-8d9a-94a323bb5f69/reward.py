"""
Reward Script: Multi-stage Docker build debug workflow
Task ID: vscode_gf3_032
Domain: vscode
Scoring:
  Component 1 (0.10): Dockerfile exists at the correct path
  Component 2 (0.30): Builder stage — FROM node:18, npm install, TypeScript build
  Component 3 (0.30): Production stage — FROM node:18-alpine, COPY --from=builder, production deps
  Component 4 (0.30): Debug stage — extends builder, includes ts-node-dev for hot-reload
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_032'
DOCKERFILE_PATH = os.path.join(WORKDIR, 'projects', 'node-api', 'Dockerfile')


def parse_stages(content):
    """Parse Dockerfile into stages. Returns list of (stage_name, base_image, stage_content)."""
    stages = []
    # Split on FROM directives
    lines = content.split('\n')
    current_stage_name = None
    current_base = None
    current_lines = []

    for line in lines:
        stripped = line.strip()
        from_match = re.match(r'^FROM\s+(\S+)(\s+AS\s+(\S+))?', stripped, re.IGNORECASE)
        if from_match:
            # Save previous stage if any
            if current_base is not None:
                stages.append((current_stage_name, current_base, '\n'.join(current_lines)))
            current_base = from_match.group(1)
            current_stage_name = from_match.group(3)  # May be None
            current_lines = [stripped]
        else:
            current_lines.append(stripped)

    # Save last stage
    if current_base is not None:
        stages.append((current_stage_name, current_base, '\n'.join(current_lines)))

    return stages


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Dockerfile exists at the correct path (0.1 points)
    try:
        if not os.path.isfile(file_path):
            print(f"FAIL: Component 1 — Dockerfile not found at {file_path}")
            print("REWARD: 0.0")
            return 0.0
        with open(file_path, 'r') as f:
            content = f.read()
        if len(content.strip()) < 20:
            print(f"FAIL: Component 1 — Dockerfile is too small ({len(content)} bytes)")
            print("REWARD: 0.0")
            return 0.0
        print(f"PASS: Component 1 — Dockerfile exists at {file_path} ({len(content)} bytes) (0.1 pts)")
        total_score += 0.1
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse stages
    stages = parse_stages(content)
    stage_names = [s[0].lower() if s[0] else None for s in stages]
    stage_bases = [s[1].lower() for s in stages]
    print(f"INFO: Found {len(stages)} stages: {list(zip(stage_names, stage_bases))}")

    # Component 2: Builder stage (0.3 points)
    # Must have a stage named 'builder' using 'node:18', with npm install and TypeScript build
    try:
        builder_found = False
        for name, base, body in stages:
            if name and name.lower() == 'builder':
                builder_found = True
                sub_score = 0.0
                body_lower = body.lower()

                # Check base image is node:18 (not node:18-alpine or other variant)
                if base.lower() == 'node:18':
                    sub_score += 0.1
                    print(f"  PASS: Builder uses node:18")
                else:
                    print(f"  FAIL: Builder base image is '{base}', expected 'node:18'")

                # Check npm install
                if 'npm install' in body_lower or 'npm ci' in body_lower:
                    sub_score += 0.1
                    print(f"  PASS: Builder runs npm install")
                else:
                    print(f"  FAIL: Builder does not run npm install")

                # Check TypeScript build (npm run build, or tsc, or npx tsc)
                if 'npm run build' in body_lower or 'tsc' in body_lower or 'npx tsc' in body_lower:
                    sub_score += 0.1
                    print(f"  PASS: Builder builds TypeScript")
                else:
                    print(f"  FAIL: Builder does not build TypeScript")

                if sub_score > 0:
                    print(f"PASS: Component 2 — Builder stage ({sub_score} pts)")
                    total_score += sub_score
                else:
                    print(f"FAIL: Component 2 — Builder stage found but no sub-checks passed")
                break

        if not builder_found:
            print(f"FAIL: Component 2 — No stage named 'builder' found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Production stage (0.3 points)
    # Must use node:18-alpine, COPY --from=builder, production-only deps
    try:
        production_found = False
        for name, base, body in stages:
            if name and name.lower() == 'production':
                production_found = True
                sub_score = 0.0
                body_lower = body.lower()

                # Check base image is node:18-alpine
                if 'alpine' in base.lower() and 'node' in base.lower():
                    sub_score += 0.1
                    print(f"  PASS: Production uses alpine node image ({base})")
                else:
                    print(f"  FAIL: Production base image is '{base}', expected node:18-alpine variant")

                # Check COPY --from=builder
                if re.search(r'copy\s+--from=builder', body_lower):
                    sub_score += 0.1
                    print(f"  PASS: Production copies from builder stage")
                else:
                    print(f"  FAIL: Production does not COPY --from=builder")

                # Check production-only dependencies (npm install with --omit=dev or --production or --only=production)
                if re.search(r'npm\s+(install|ci)\s+.*--omit[= ]dev', body_lower) or \
                   re.search(r'npm\s+(install|ci)\s+.*--production', body_lower) or \
                   re.search(r'npm\s+(install|ci)\s+.*--only[= ]prod', body_lower) or \
                   'npm ci --omit=dev' in body_lower or \
                   'npm install --production' in body_lower:
                    sub_score += 0.1
                    print(f"  PASS: Production installs only production dependencies")
                else:
                    print(f"  FAIL: Production does not install production-only dependencies")

                if sub_score > 0:
                    print(f"PASS: Component 3 — Production stage ({sub_score} pts)")
                    total_score += sub_score
                else:
                    print(f"FAIL: Component 3 — Production stage found but no sub-checks passed")
                break

        if not production_found:
            # Also check for unnamed stage with alpine base
            for name, base, body in stages:
                if 'alpine' in base.lower() and re.search(r'copy\s+--from=builder', body.lower()):
                    production_found = True
                    sub_score = 0.0
                    body_lower = body.lower()
                    if 'alpine' in base.lower():
                        sub_score += 0.1
                    if re.search(r'copy\s+--from=builder', body_lower):
                        sub_score += 0.1
                    if re.search(r'npm\s+(install|ci)\s+.*--(omit[= ]dev|production|only[= ]prod)', body_lower):
                        sub_score += 0.1
                    if sub_score > 0:
                        print(f"PASS: Component 3 — Production stage (unnamed) ({sub_score} pts)")
                        total_score += sub_score
                    break
            if not production_found:
                print(f"FAIL: Component 3 — No production stage found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Debug stage (0.3 points)
    # Must extend builder (FROM builder), include ts-node-dev
    try:
        debug_found = False
        for name, base, body in stages:
            if name and name.lower() == 'debug':
                debug_found = True
                sub_score = 0.0
                body_lower = body.lower()

                # Check that it extends builder
                if base.lower() == 'builder':
                    sub_score += 0.15
                    print(f"  PASS: Debug extends builder stage")
                else:
                    print(f"  FAIL: Debug base is '{base}', expected 'builder'")

                # Check ts-node-dev is included (installed or used)
                if 'ts-node-dev' in body_lower:
                    sub_score += 0.15
                    print(f"  PASS: Debug includes ts-node-dev")
                else:
                    print(f"  FAIL: Debug does not include ts-node-dev")

                if sub_score > 0:
                    print(f"PASS: Component 4 — Debug stage ({sub_score} pts)")
                    total_score += sub_score
                else:
                    print(f"FAIL: Component 4 — Debug stage found but no sub-checks passed")
                break

        if not debug_found:
            print(f"FAIL: Component 4 — No stage named 'debug' found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(DOCKERFILE_PATH):
    print(f"File not found: {DOCKERFILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(DOCKERFILE_PATH)

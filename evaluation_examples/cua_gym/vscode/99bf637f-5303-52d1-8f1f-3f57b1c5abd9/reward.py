"""
Reward Script: Create a Dockerfile for a Node.js Express application
Task ID: vscode_gf3_002
Domain: vscode
Scoring:
  - Component 1: FROM node:18-alpine base image (0.20 pts)
  - Component 2: WORKDIR /app (0.15 pts)
  - Component 3: COPY package*.json ./ (0.15 pts)
  - Component 4: RUN npm ci --only=production (0.20 pts)
  - Component 5: COPY . . (source copy) (0.10 pts)
  - Component 6: EXPOSE 3000 (0.10 pts)
  - Component 7: CMD ["node", "server.js"] (0.10 pts)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_002'

def verify_task(file_path):
    """
    Verify Dockerfile creation with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: Dockerfile not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Normalize content for checking: strip each line and work line-by-line
    lines = [line.strip() for line in content.strip().splitlines() if line.strip()]

    # Component 1: FROM node:18-alpine base image (0.20 points)
    try:
        has_from = any(re.match(r'^FROM\s+node:18-alpine\s*$', line, re.IGNORECASE) for line in lines)
        if has_from:
            print(f"PASS: Component 1 — FROM node:18-alpine found (0.20 pts)")
            total_score += 0.20
        else:
            # Check for partial match (right image, wrong tag or vice versa)
            from_lines = [l for l in lines if l.upper().startswith('FROM')]
            print(f"FAIL: Component 1 — Expected 'FROM node:18-alpine', found FROM lines: {from_lines}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: WORKDIR /app (0.15 points)
    try:
        has_workdir = any(re.match(r'^WORKDIR\s+/app\s*$', line, re.IGNORECASE) for line in lines)
        if has_workdir:
            print(f"PASS: Component 2 — WORKDIR /app found (0.15 pts)")
            total_score += 0.15
        else:
            workdir_lines = [l for l in lines if l.upper().startswith('WORKDIR')]
            print(f"FAIL: Component 2 — Expected 'WORKDIR /app', found: {workdir_lines}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: COPY package*.json ./ (0.15 points)
    # Accept variations like "COPY package*.json ./" or "COPY package*.json ."
    try:
        has_pkg_copy = any(
            re.match(r'^COPY\s+package\*\.json\s+\./?$', line, re.IGNORECASE)
            for line in lines
        )
        if has_pkg_copy:
            print(f"PASS: Component 3 — COPY package*.json found (0.15 pts)")
            total_score += 0.15
        else:
            copy_lines = [l for l in lines if l.upper().startswith('COPY')]
            print(f"FAIL: Component 3 — Expected 'COPY package*.json ./', found COPY lines: {copy_lines}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: RUN npm ci --only=production (0.20 points)
    try:
        has_npm_ci = any(
            re.match(r'^RUN\s+npm\s+ci\s+--only=production\s*$', line, re.IGNORECASE)
            for line in lines
        )
        if has_npm_ci:
            print(f"PASS: Component 4 — RUN npm ci --only=production found (0.20 pts)")
            total_score += 0.20
        else:
            run_lines = [l for l in lines if l.upper().startswith('RUN')]
            print(f"FAIL: Component 4 — Expected 'RUN npm ci --only=production', found RUN lines: {run_lines}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: COPY . . (copy source code) (0.10 points)
    try:
        has_copy_all = any(
            re.match(r'^COPY\s+\.\s+\.\s*$', line, re.IGNORECASE)
            for line in lines
        )
        if has_copy_all:
            print(f"PASS: Component 5 — COPY . . found (0.10 pts)")
            total_score += 0.10
        else:
            copy_lines = [l for l in lines if l.upper().startswith('COPY')]
            print(f"FAIL: Component 5 — Expected 'COPY . .', found COPY lines: {copy_lines}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: EXPOSE 3000 (0.10 points)
    try:
        has_expose = any(
            re.match(r'^EXPOSE\s+3000\s*$', line, re.IGNORECASE)
            for line in lines
        )
        if has_expose:
            print(f"PASS: Component 6 — EXPOSE 3000 found (0.10 pts)")
            total_score += 0.10
        else:
            expose_lines = [l for l in lines if l.upper().startswith('EXPOSE')]
            print(f"FAIL: Component 6 — Expected 'EXPOSE 3000', found: {expose_lines}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: CMD ["node", "server.js"] (0.10 points)
    # Accept both JSON form CMD ["node", "server.js"] and shell form CMD node server.js
    try:
        has_cmd = any(
            re.match(r'^CMD\s+\["node",\s*"server\.js"\]\s*$', line) or
            re.match(r'^CMD\s+node\s+server\.js\s*$', line, re.IGNORECASE)
            for line in lines
        )
        if has_cmd:
            print(f"PASS: Component 7 — CMD node server.js found (0.10 pts)")
            total_score += 0.10
        else:
            cmd_lines = [l for l in lines if l.upper().startswith('CMD')]
            print(f"FAIL: Component 7 — Expected CMD [\"node\", \"server.js\"], found: {cmd_lines}")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/projects/myapp/Dockerfile'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)

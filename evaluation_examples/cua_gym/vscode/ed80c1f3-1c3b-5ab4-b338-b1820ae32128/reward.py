"""
Reward Script: VSCode launch.json debug configurations
Task ID: vscode_gf2_020
Domain: vscode
Scoring:
  C1 (0.10) — launch.json exists, valid JSON, version "0.2.0"
  C2 (0.25) — "Debug API" attach config: port 9229, restart true
  C3 (0.25) — "Debug Worker" launch config: program worker/index.js, --inspect
  C4 (0.25) — "Debug All" compound: both configs, stopAll true
  C5 (0.15) — Exactly 2 configurations and 1 compound
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf2_020'
LAUNCH_JSON = os.path.join(WORKDIR, 'projects', 'monorepo', '.vscode', 'launch.json')


def verify_task():
    total_score = 0.0

    # -------------------------------------------------------------------
    # Precondition: file must exist
    # -------------------------------------------------------------------
    if not os.path.exists(LAUNCH_JSON):
        print(f"CRITICAL: launch.json not found at {LAUNCH_JSON}")
        print("REWARD: 0.0")
        return 0.0

    # -------------------------------------------------------------------
    # Precondition: file must be valid JSON
    # -------------------------------------------------------------------
    try:
        with open(LAUNCH_JSON, 'r') as f:
            data = json.load(f)
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: launch.json is not valid JSON: {e}")
        print("REWARD: 0.0")
        return 0.0

    configs = data.get('configurations', [])
    compounds = data.get('compounds', [])

    # Build lookup dicts for configurations by name
    config_by_name = {}
    for c in configs:
        name = c.get('name', '')
        config_by_name[name] = c

    compound_by_name = {}
    for c in compounds:
        name = c.get('name', '')
        compound_by_name[name] = c

    # -------------------------------------------------------------------
    # Component 1: version "0.2.0" present (0.10 pts)
    # This differentiates initial (no file) from golden (file with version).
    # -------------------------------------------------------------------
    try:
        version = data.get('version', '')
        if version == '0.2.0':
            print(f"PASS: C1 — version is '0.2.0' (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: C1 — expected version '0.2.0', found '{version}'")
    except Exception as e:
        print(f"ERROR: C1 — {e}")

    # -------------------------------------------------------------------
    # Component 2: "Debug API" attach config (0.25 pts)
    #   - type: "node", request: "attach", port: 9229, restart: true
    # -------------------------------------------------------------------
    try:
        api_cfg = config_by_name.get('Debug API')
        if api_cfg is None:
            print("FAIL: C2 — 'Debug API' configuration not found")
        else:
            checks = []
            # request must be "attach"
            if api_cfg.get('request') == 'attach':
                checks.append(True)
            else:
                print(f"FAIL: C2a — expected request 'attach', found '{api_cfg.get('request')}'")
                checks.append(False)
            # port must be 9229
            if api_cfg.get('port') == 9229:
                checks.append(True)
            else:
                print(f"FAIL: C2b — expected port 9229, found {api_cfg.get('port')}")
                checks.append(False)
            # restart must be true
            if api_cfg.get('restart') is True:
                checks.append(True)
            else:
                print(f"FAIL: C2c — expected restart true, found {api_cfg.get('restart')}")
                checks.append(False)
            # type must be "node"
            if api_cfg.get('type') == 'node':
                checks.append(True)
            else:
                print(f"FAIL: C2d — expected type 'node', found '{api_cfg.get('type')}'")
                checks.append(False)

            passed = sum(checks)
            pts = 0.25 * (passed / len(checks))
            if passed == len(checks):
                print(f"PASS: C2 — 'Debug API' attach config correct (0.25 pts)")
                total_score += pts
            elif passed > 0:
                print(f"PARTIAL: C2 — {passed}/{len(checks)} sub-checks passed ({pts:.3f} pts)")
                total_score += pts
            else:
                print(f"FAIL: C2 — all sub-checks failed")
    except Exception as e:
        print(f"ERROR: C2 — {e}")

    # -------------------------------------------------------------------
    # Component 3: "Debug Worker" launch config (0.25 pts)
    #   - type: "node", request: "launch", program ends with worker/index.js,
    #     runtimeArgs includes "--inspect"
    # -------------------------------------------------------------------
    try:
        worker_cfg = config_by_name.get('Debug Worker')
        if worker_cfg is None:
            print("FAIL: C3 — 'Debug Worker' configuration not found")
        else:
            checks = []
            # request must be "launch"
            if worker_cfg.get('request') == 'launch':
                checks.append(True)
            else:
                print(f"FAIL: C3a — expected request 'launch', found '{worker_cfg.get('request')}'")
                checks.append(False)
            # program must reference worker/index.js
            program = worker_cfg.get('program', '')
            if 'worker/index.js' in program:
                checks.append(True)
            else:
                print(f"FAIL: C3b — expected program containing 'worker/index.js', found '{program}'")
                checks.append(False)
            # runtimeArgs must include "--inspect"
            runtime_args = worker_cfg.get('runtimeArgs', [])
            if '--inspect' in runtime_args:
                checks.append(True)
            else:
                print(f"FAIL: C3c — expected '--inspect' in runtimeArgs, found {runtime_args}")
                checks.append(False)
            # type must be "node"
            if worker_cfg.get('type') == 'node':
                checks.append(True)
            else:
                print(f"FAIL: C3d — expected type 'node', found '{worker_cfg.get('type')}'")
                checks.append(False)

            passed = sum(checks)
            pts = 0.25 * (passed / len(checks))
            if passed == len(checks):
                print(f"PASS: C3 — 'Debug Worker' launch config correct (0.25 pts)")
                total_score += pts
            elif passed > 0:
                print(f"PARTIAL: C3 — {passed}/{len(checks)} sub-checks passed ({pts:.3f} pts)")
                total_score += pts
            else:
                print(f"FAIL: C3 — all sub-checks failed")
    except Exception as e:
        print(f"ERROR: C3 — {e}")

    # -------------------------------------------------------------------
    # Component 4: "Debug All" compound config (0.25 pts)
    #   - configurations lists both "Debug API" and "Debug Worker"
    #   - stopAll: true
    # -------------------------------------------------------------------
    try:
        compound = compound_by_name.get('Debug All')
        if compound is None:
            print("FAIL: C4 — 'Debug All' compound configuration not found")
        else:
            checks = []
            # Must list both configs
            compound_configs = compound.get('configurations', [])
            if 'Debug API' in compound_configs and 'Debug Worker' in compound_configs:
                checks.append(True)
            else:
                print(f"FAIL: C4a — expected both 'Debug API' and 'Debug Worker' in compound, found {compound_configs}")
                checks.append(False)
            # stopAll must be true
            if compound.get('stopAll') is True:
                checks.append(True)
            else:
                print(f"FAIL: C4b — expected stopAll true, found {compound.get('stopAll')}")
                checks.append(False)

            passed = sum(checks)
            pts = 0.25 * (passed / len(checks))
            if passed == len(checks):
                print(f"PASS: C4 — 'Debug All' compound config correct (0.25 pts)")
                total_score += pts
            elif passed > 0:
                print(f"PARTIAL: C4 — {passed}/{len(checks)} sub-checks passed ({pts:.3f} pts)")
                total_score += pts
            else:
                print(f"FAIL: C4 — all sub-checks failed")
    except Exception as e:
        print(f"ERROR: C4 — {e}")

    # -------------------------------------------------------------------
    # Component 5: Exactly 2 configurations and 1 compound (0.15 pts)
    # -------------------------------------------------------------------
    try:
        checks = []
        if len(configs) == 2:
            checks.append(True)
        else:
            print(f"FAIL: C5a — expected 2 configurations, found {len(configs)}")
            checks.append(False)
        if len(compounds) == 1:
            checks.append(True)
        else:
            print(f"FAIL: C5b — expected 1 compound, found {len(compounds)}")
            checks.append(False)

        passed = sum(checks)
        pts = 0.15 * (passed / len(checks))
        if passed == len(checks):
            print(f"PASS: C5 — exactly 2 configs and 1 compound (0.15 pts)")
            total_score += pts
        elif passed > 0:
            print(f"PARTIAL: C5 — {passed}/{len(checks)} sub-checks passed ({pts:.3f} pts)")
            total_score += pts
        else:
            print(f"FAIL: C5 — all sub-checks failed")
    except Exception as e:
        print(f"ERROR: C5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

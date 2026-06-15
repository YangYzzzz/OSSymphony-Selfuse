"""
Reward Script: Kubernetes-ready Docker image for Node.js application
Task ID: os_gf1_074
Domain: os (Docker)
Scoring:
  Component 1: Dockerfile exists with multi-stage build (0.20)
  Component 2: Non-root USER directive in Dockerfile (0.15)
  Component 3: HEALTHCHECK instruction in Dockerfile (0.15)
  Component 4: LABEL directives with version, maintainer, build-date (0.15)
  Component 5: Image pushed to local registry (nodeapp:latest in catalog) (0.20)
  Component 6: Registry image config has non-root user and labels (0.15)
"""

import os
import re
import json

try:
    from urllib.request import urlopen, Request
    from urllib.error import URLError
except ImportError:
    urlopen = None

WORKDIR = '/home/user'
TASK_ID = 'os_gf1_074'
DOCKERFILE_PATH = '/opt/nodeapp/Dockerfile'

# Registry could be on port 5001 (setup used 5001) or 5000 (task says 5000)
REGISTRY_PORTS = [5001, 5000]


def fetch_json(url, timeout=5):
    """Fetch JSON from a URL using urllib (no subprocess)."""
    try:
        req = Request(url)
        resp = urlopen(req, timeout=timeout)
        return json.loads(resp.read().decode('utf-8'))
    except Exception:
        return None


def find_registry_port():
    """Find which port the registry is listening on."""
    for port in REGISTRY_PORTS:
        data = fetch_json(f'http://localhost:{port}/v2/_catalog')
        if data is not None:
            return port
    return None


def get_image_config_from_registry(port, repo='nodeapp', tag='latest'):
    """
    Retrieve image config (User, Labels, Healthcheck) from registry HTTP API.
    Steps: get index -> get manifest -> get config blob.
    """
    try:
        # Step 1: Get OCI index
        base = f'http://localhost:{port}/v2/{repo}'
        req = Request(f'{base}/manifests/{tag}')
        req.add_header('Accept', 'application/vnd.oci.image.index.v1+json')
        resp = urlopen(req, timeout=10)
        index = json.loads(resp.read().decode('utf-8'))

        # Find amd64 manifest digest (skip attestation manifests)
        manifest_digest = None
        for m in index.get('manifests', []):
            platform = m.get('platform', {})
            annotations = m.get('annotations', {})
            if 'attestation' in annotations.get('vnd.docker.reference.type', ''):
                continue
            if platform.get('architecture') == 'amd64' or platform.get('os') == 'linux':
                manifest_digest = m['digest']
                break
        if not manifest_digest and index.get('manifests'):
            manifest_digest = index['manifests'][0]['digest']

        if not manifest_digest:
            return None

        # Step 2: Get image manifest
        req2 = Request(f'{base}/manifests/{manifest_digest}')
        req2.add_header('Accept', 'application/vnd.oci.image.manifest.v1+json')
        resp2 = urlopen(req2, timeout=10)
        manifest = json.loads(resp2.read().decode('utf-8'))

        config_digest = manifest.get('config', {}).get('digest')
        if not config_digest:
            return None

        # Step 3: Get config blob
        req3 = Request(f'{base}/blobs/{config_digest}')
        resp3 = urlopen(req3, timeout=10)
        config = json.loads(resp3.read().decode('utf-8'))
        return config.get('config', {})

    except Exception as e:
        print(f"  DEBUG: Registry config fetch error: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ------------------------------------------------------------------
    # Precondition: Dockerfile must exist
    # ------------------------------------------------------------------
    if not os.path.isfile(DOCKERFILE_PATH):
        print(f"CRITICAL: Dockerfile not found at {DOCKERFILE_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(DOCKERFILE_PATH, 'r') as f:
            dockerfile_content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read Dockerfile: {e}")
        print("REWARD: 0.0")
        return 0.0

    dockerfile_upper = dockerfile_content.upper()
    dockerfile_lines = dockerfile_content.strip().split('\n')

    # ------------------------------------------------------------------
    # Component 1: Multi-stage build (0.20 points)
    # Dockerfile must have at least 2 FROM instructions (build + production)
    # ------------------------------------------------------------------
    try:
        from_lines = [l for l in dockerfile_lines
                      if re.match(r'^\s*FROM\s+', l, re.IGNORECASE)]
        as_count = sum(1 for l in from_lines if re.search(r'\bAS\b', l, re.IGNORECASE))
        if len(from_lines) >= 2 and as_count >= 1:
            print(f"PASS: Component 1 — Multi-stage build: {len(from_lines)} FROM stages, "
                  f"{as_count} named (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — Expected multi-stage build (>=2 FROM, >=1 AS), "
                  f"found {len(from_lines)} FROM, {as_count} AS")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ------------------------------------------------------------------
    # Component 2: Non-root USER directive (0.15 points)
    # Dockerfile must set USER to a non-root user
    # ------------------------------------------------------------------
    try:
        user_matches = re.findall(r'^\s*USER\s+(\S+)', dockerfile_content, re.MULTILINE | re.IGNORECASE)
        # The last USER directive determines who runs the container
        if user_matches:
            last_user = user_matches[-1]
            if last_user.lower() not in ('root', '0'):
                print(f"PASS: Component 2 — Non-root USER directive: '{last_user}' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 — USER is root: '{last_user}'")
        else:
            print("FAIL: Component 2 — No USER directive found in Dockerfile")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ------------------------------------------------------------------
    # Component 3: HEALTHCHECK instruction checking /health (0.15 points)
    # ------------------------------------------------------------------
    try:
        healthcheck_match = re.search(r'^\s*HEALTHCHECK\b', dockerfile_content, re.MULTILINE | re.IGNORECASE)
        health_endpoint = '/health' in dockerfile_content
        if healthcheck_match and health_endpoint:
            print(f"PASS: Component 3 — HEALTHCHECK with /health endpoint (0.15 pts)")
            total_score += 0.15
        elif healthcheck_match:
            print(f"FAIL: Component 3 — HEALTHCHECK found but /health endpoint not referenced")
        else:
            print(f"FAIL: Component 3 — No HEALTHCHECK instruction found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ------------------------------------------------------------------
    # Component 4: LABEL directives with version, maintainer, build-date (0.15 points)
    # All three required labels must be present
    # ------------------------------------------------------------------
    try:
        label_lines = re.findall(r'^\s*LABEL\s+(.+)', dockerfile_content, re.MULTILINE | re.IGNORECASE)
        all_labels_text = ' '.join(label_lines).lower()

        has_version = 'version' in all_labels_text
        has_maintainer = 'maintainer' in all_labels_text
        has_build_date = 'build-date' in all_labels_text or 'build_date' in all_labels_text

        passed_count = sum([has_version, has_maintainer, has_build_date])
        if passed_count == 3:
            print(f"PASS: Component 4 — All 3 required labels present: version, maintainer, build-date (0.15 pts)")
            total_score += 0.15
        else:
            missing = []
            if not has_version:
                missing.append('version')
            if not has_maintainer:
                missing.append('maintainer')
            if not has_build_date:
                missing.append('build-date')
            print(f"FAIL: Component 4 — Missing labels: {missing} ({passed_count}/3 present)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ------------------------------------------------------------------
    # Component 5: Image pushed to local registry (0.20 points)
    # The registry catalog must contain 'nodeapp' and tag 'latest'
    # ------------------------------------------------------------------
    try:
        port = find_registry_port()
        if port is None:
            print("FAIL: Component 5 — No registry found on ports 5000 or 5001")
        else:
            catalog = fetch_json(f'http://localhost:{port}/v2/_catalog')
            repos = catalog.get('repositories', []) if catalog else []
            if 'nodeapp' in repos:
                tags_data = fetch_json(f'http://localhost:{port}/v2/nodeapp/tags/list')
                tags = tags_data.get('tags', []) if tags_data else []
                if 'latest' in tags:
                    print(f"PASS: Component 5 — nodeapp:latest found in registry on port {port} (0.20 pts)")
                    total_score += 0.20
                else:
                    print(f"FAIL: Component 5 — nodeapp exists but 'latest' tag not found, tags: {tags}")
            else:
                print(f"FAIL: Component 5 — 'nodeapp' not in registry catalog: {repos}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # ------------------------------------------------------------------
    # Component 6: Registry image config has non-root user + labels (0.15 points)
    # Verify the PUSHED image (not just Dockerfile) has correct metadata
    # ------------------------------------------------------------------
    try:
        if port is None:
            port = find_registry_port()
        if port is None:
            print("FAIL: Component 6 — No registry found")
        else:
            config = get_image_config_from_registry(port)
            if config is None:
                print("FAIL: Component 6 — Could not retrieve image config from registry")
            else:
                img_user = config.get('User', '')
                img_labels = config.get('Labels', {}) or {}
                img_healthcheck = config.get('Healthcheck', {}) or {}

                checks_passed = 0
                sub_checks = 3

                # Sub-check 6a: Non-root user in image config
                if img_user and img_user.lower() not in ('root', '0', ''):
                    checks_passed += 1
                    print(f"  6a PASS: Image config User='{img_user}'")
                else:
                    print(f"  6a FAIL: Image config User='{img_user}' (expected non-root)")

                # Sub-check 6b: Labels present in image config
                label_keys_lower = {k.lower(): v for k, v in img_labels.items()}
                has_ver = any('version' in k for k in label_keys_lower)
                has_maint = any('maintainer' in k for k in label_keys_lower)
                if has_ver and has_maint:
                    checks_passed += 1
                    print(f"  6b PASS: Image labels include version and maintainer")
                else:
                    print(f"  6b FAIL: Image labels missing version or maintainer: {list(img_labels.keys())}")

                # Sub-check 6c: Healthcheck in image config
                if img_healthcheck and img_healthcheck.get('Test'):
                    checks_passed += 1
                    print(f"  6c PASS: Image has Healthcheck config")
                else:
                    print(f"  6c FAIL: No Healthcheck in image config")

                if checks_passed == sub_checks:
                    print(f"PASS: Component 6 — All {sub_checks} image config checks passed (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 6 — {checks_passed}/{sub_checks} image config checks passed")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # ------------------------------------------------------------------
    # Final score
    # ------------------------------------------------------------------
    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

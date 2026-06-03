"""
Reward Script: Kubernetes ConfigMap, Secret, and Deployment verification
Task ID: os_gf2_011
Domain: OS (Kubernetes)
Scoring:
  Component 1: ConfigMap 'app-config' exists in 'production' namespace (0.25)
  Component 2: Secret 'db-credentials' exists with correct data (0.25)
  Component 3: Deployment 'api-server' has envFrom configMapRef for app-config (0.25)
  Component 4: Deployment 'api-server' has envFrom secretRef for db-credentials (0.25)
"""

import os
import json
import base64
import tempfile
import ssl

NAMESPACE = 'production'
KUBECONFIG_PATH = '/etc/rancher/k3s/k3s.yaml'


def load_kubeconfig():
    """Parse k3s kubeconfig and return (server, ca_file, cert_file, key_file)."""
    import yaml
    with open(KUBECONFIG_PATH) as f:
        cfg = yaml.safe_load(f)

    server = cfg['clusters'][0]['cluster']['server']
    ca_data = base64.b64decode(cfg['clusters'][0]['cluster']['certificate-authority-data'])
    cert_data = base64.b64decode(cfg['users'][0]['user']['client-certificate-data'])
    key_data = base64.b64decode(cfg['users'][0]['user']['client-key-data'])

    # Write temp files for SSL context
    ca_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pem')
    ca_file.write(ca_data)
    ca_file.close()

    cert_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pem')
    cert_file.write(cert_data)
    cert_file.close()

    key_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pem')
    key_file.write(key_data)
    key_file.close()

    return server, ca_file.name, cert_file.name, key_file.name


def k8s_get(server, ca_path, cert_path, key_path, api_path):
    """Make a GET request to the Kubernetes API and return parsed JSON."""
    import urllib.request
    import urllib.error

    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.load_verify_locations(ca_path)
    ctx.load_cert_chain(cert_path, key_path)

    url = f"{server}{api_path}"
    req = urllib.request.Request(url, method='GET')
    try:
        resp = urllib.request.urlopen(req, context=ctx, timeout=10)
        return json.loads(resp.read().decode()), resp.status
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ''
        return json.loads(body) if body else {}, e.code
    except Exception as e:
        return {"error": str(e)}, 0


def verify_task():
    """
    Verify Kubernetes task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load kubeconfig
    try:
        server, ca_path, cert_path, key_path = load_kubeconfig()
        print(f"INFO: Connected to k8s API at {server}")
    except Exception as e:
        print(f"CRITICAL: Cannot load kubeconfig: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: ConfigMap 'app-config' exists in 'production' (0.25 points)
    try:
        cm_data, cm_status = k8s_get(
            server, ca_path, cert_path, key_path,
            f"/api/v1/namespaces/{NAMESPACE}/configmaps/app-config"
        )
        if cm_status == 200 and cm_data.get('metadata', {}).get('name') == 'app-config':
            # Verify it has data (from the properties file)
            data_keys = cm_data.get('data', {})
            if len(data_keys) > 0:
                print(f"PASS: Component 1 — ConfigMap 'app-config' exists with {len(data_keys)} data key(s) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 — ConfigMap 'app-config' exists but has no data")
        else:
            print(f"FAIL: Component 1 — ConfigMap 'app-config' not found (status: {cm_status})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Secret 'db-credentials' exists with correct fields (0.25 points)
    try:
        secret_data, secret_status = k8s_get(
            server, ca_path, cert_path, key_path,
            f"/api/v1/namespaces/{NAMESPACE}/secrets/db-credentials"
        )
        if secret_status == 200 and secret_data.get('metadata', {}).get('name') == 'db-credentials':
            data = secret_data.get('data', {})
            sub_score = 0.0

            # Check DB_USER field (base64 of 'appuser')
            db_user_b64 = data.get('DB_USER', '')
            try:
                db_user_val = base64.b64decode(db_user_b64).decode()
            except Exception:
                db_user_val = ''
            if db_user_val == 'appuser':
                sub_score += 0.125
                print(f"  PASS: DB_USER = 'appuser'")
            else:
                print(f"  FAIL: DB_USER expected 'appuser', found '{db_user_val}'")

            # Check DB_PASSWORD field (base64 of 's3cr3t')
            db_pass_b64 = data.get('DB_PASSWORD', '')
            try:
                db_pass_val = base64.b64decode(db_pass_b64).decode()
            except Exception:
                db_pass_val = ''
            if db_pass_val == 's3cr3t':
                sub_score += 0.125
                print(f"  PASS: DB_PASSWORD = 's3cr3t'")
            else:
                print(f"  FAIL: DB_PASSWORD expected 's3cr3t', found '{db_pass_val}'")

            if sub_score > 0:
                print(f"PASS: Component 2 — Secret 'db-credentials' ({sub_score} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 2 — Secret 'db-credentials' has wrong data")
        else:
            print(f"FAIL: Component 2 — Secret 'db-credentials' not found (status: {secret_status})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Deployment 'api-server' has envFrom with configMapRef for 'app-config' (0.25 points)
    try:
        dep_data, dep_status = k8s_get(
            server, ca_path, cert_path, key_path,
            f"/apis/apps/v1/namespaces/{NAMESPACE}/deployments/api-server"
        )
        if dep_status == 200:
            containers = dep_data.get('spec', {}).get('template', {}).get('spec', {}).get('containers', [])
            configmap_ref_found = False
            for container in containers:
                env_from = container.get('envFrom', [])
                for ef in env_from:
                    cm_ref = ef.get('configMapRef', {})
                    if cm_ref.get('name') == 'app-config':
                        configmap_ref_found = True
                        break
                if configmap_ref_found:
                    break

            if configmap_ref_found:
                print(f"PASS: Component 3 — Deployment has envFrom configMapRef 'app-config' (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — Deployment lacks envFrom configMapRef for 'app-config'")
        else:
            print(f"FAIL: Component 3 — Deployment 'api-server' not found (status: {dep_status})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Deployment 'api-server' has envFrom with secretRef for 'db-credentials' (0.25 points)
    try:
        # Reuse dep_data from Component 3 if available
        if dep_status == 200:
            containers = dep_data.get('spec', {}).get('template', {}).get('spec', {}).get('containers', [])
            secret_ref_found = False
            for container in containers:
                env_from = container.get('envFrom', [])
                for ef in env_from:
                    s_ref = ef.get('secretRef', {})
                    if s_ref.get('name') == 'db-credentials':
                        secret_ref_found = True
                        break
                if secret_ref_found:
                    break

            if secret_ref_found:
                print(f"PASS: Component 4 — Deployment has envFrom secretRef 'db-credentials' (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 — Deployment lacks envFrom secretRef for 'db-credentials'")
        else:
            print(f"FAIL: Component 4 — Deployment 'api-server' not found (status: {dep_status})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Cleanup temp files
    try:
        os.unlink(ca_path)
        os.unlink(cert_path)
        os.unlink(key_path)
    except Exception:
        pass

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Fix kubeconfig permissions if needed
try:
    os.chmod(KUBECONFIG_PATH, 0o644)
except Exception:
    pass

verify_task()

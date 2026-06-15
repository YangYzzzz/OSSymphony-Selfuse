"""
Initial Setup: Create Kubernetes environment with namespace, deployment, and config file.
Task ID: os_gf2_011
Domain: os (Kubernetes)

Sets up:
- k3s single-node cluster
- 'production' namespace
- 'api-server' deployment in production namespace
- /opt/k8s/app.properties with application config
- Opens a terminal window
"""

import os
import shlex
import subprocess
import time
import textwrap

WORKDIR = '/home/user'
TASK_ID = 'os_gf2_011'


def run(cmd, check=True, timeout=120, **kwargs):
    """Run a shell command with logging."""
    print(f"  RUN: {cmd}")
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True,
        timeout=timeout, **kwargs
    )
    if result.stdout.strip():
        print(f"  OUT: {result.stdout.strip()[:500]}")
    if result.stderr.strip():
        print(f"  ERR: {result.stderr.strip()[:500]}")
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed (rc={result.returncode}): {cmd}\n{result.stderr}")
    return result


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def install_k3s():
    """Install k3s and wait for it to be ready."""
    print("=== Installing k3s ===")

    # Install k3s (non-interactive, no traefik to save resources)
    run("curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC='--disable=traefik' sh -",
        timeout=180)

    # Wait for k3s to be ready
    print("Waiting for k3s to be ready...")
    for i in range(60):
        result = subprocess.run(
            "sudo k3s kubectl get nodes",
            shell=True, capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and "Ready" in result.stdout:
            print(f"  k3s ready after {i+1} attempts")
            break
        time.sleep(2)
    else:
        raise RuntimeError("k3s failed to become ready within 120 seconds")

    # Set up kubectl for the user (non-root access)
    os.makedirs(f"{WORKDIR}/.kube", exist_ok=True)
    run(f"sudo cp /etc/rancher/k3s/k3s.yaml {WORKDIR}/.kube/config")
    run(f"sudo chown user:user {WORKDIR}/.kube/config")
    run(f"chmod 600 {WORKDIR}/.kube/config")

    # Set KUBECONFIG env for this process and all child processes
    os.environ["KUBECONFIG"] = f"{WORKDIR}/.kube/config"

    # Also add to .bashrc so terminal sessions use it
    bashrc = f"{WORKDIR}/.bashrc"
    with open(bashrc, "a") as f:
        f.write(f'\nexport KUBECONFIG={WORKDIR}/.kube/config\n')

    # Verify kubectl works as user
    run("kubectl get nodes")
    print("=== k3s installation complete ===")


def create_namespace():
    """Create the production namespace."""
    print("=== Creating production namespace ===")
    run("kubectl create namespace production --dry-run=client -o yaml | kubectl apply -f -")


def create_deployment():
    """Create the api-server deployment in production namespace."""
    print("=== Creating api-server deployment ===")

    deployment_yaml = textwrap.dedent("""\
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: api-server
      namespace: production
      labels:
        app: api-server
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: api-server
      template:
        metadata:
          labels:
            app: api-server
        spec:
          containers:
          - name: api-server
            image: nginx:alpine
            ports:
            - containerPort: 8080
    """)

    yaml_path = "/tmp/api-server-deployment.yaml"
    with open(yaml_path, 'w') as f:
        f.write(deployment_yaml)

    run(f"kubectl apply -f {yaml_path}")

    # Wait for deployment to be available
    print("Waiting for deployment to be available...")
    for i in range(60):
        result = subprocess.run(
            "kubectl get deployment api-server -n production -o jsonpath='{.status.availableReplicas}'",
            shell=True, capture_output=True, text=True, timeout=10
        )
        if result.stdout.strip("'") == "1":
            print(f"  Deployment ready after {i+1} checks")
            break
        time.sleep(3)
    else:
        # Check status anyway
        run("kubectl get deployment api-server -n production", check=False)
        run("kubectl get pods -n production", check=False)
        print("  Warning: deployment may not be fully ready, continuing...")

    print("=== Deployment created ===")


def create_app_properties():
    """Create /opt/k8s/app.properties with realistic application configuration."""
    print("=== Creating app.properties ===")

    run("sudo mkdir -p /opt/k8s")
    run("sudo chown user:user /opt/k8s")

    properties_content = textwrap.dedent("""\
    # Application Configuration
    app.name=api-server
    app.version=2.4.1
    app.environment=production

    # Server settings
    server.port=8080
    server.host=0.0.0.0
    server.max-threads=200
    server.connection-timeout=30000

    # Database connection pool
    db.pool.min-idle=5
    db.pool.max-active=20
    db.pool.max-wait=10000

    # Logging
    logging.level=INFO
    logging.file=/var/log/api-server/app.log
    logging.max-size=50MB
    logging.max-history=30

    # Cache settings
    cache.enabled=true
    cache.ttl=3600
    cache.max-entries=10000

    # Feature flags
    feature.new-dashboard=true
    feature.beta-api=false
    feature.rate-limiting=true
    """)

    with open("/opt/k8s/app.properties", 'w') as f:
        f.write(properties_content)

    print(f"  Created /opt/k8s/app.properties ({len(properties_content)} bytes)")


def main():
    print(f"=== Initial Setup for {TASK_ID} ===")

    # Step 1: Create the app.properties file
    create_app_properties()

    # Step 2: Install k3s
    install_k3s()

    # Step 3: Create namespace and deployment
    create_namespace()
    create_deployment()

    # Step 4: Verify initial state is clean (no configmap, no secret)
    result = subprocess.run(
        "kubectl get configmap app-config -n production",
        shell=True, capture_output=True, text=True
    )
    assert result.returncode != 0, "ConfigMap app-config should NOT exist in initial state"

    result = subprocess.run(
        "kubectl get secret db-credentials -n production",
        shell=True, capture_output=True, text=True
    )
    assert result.returncode != 0, "Secret db-credentials should NOT exist in initial state"

    print("=== Initial state verified: no configmap or secret exists ===")

    # Step 5: Open terminal for the user
    launch_gui('gnome-terminal', delay_sec=2.0)
    print('GUI_READY: launched terminal with DISPLAY=:0')

    print(f"=== Initial Setup for {TASK_ID} COMPLETE ===")


main()

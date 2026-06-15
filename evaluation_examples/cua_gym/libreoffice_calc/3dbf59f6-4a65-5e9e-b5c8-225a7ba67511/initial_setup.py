"""
Initial Setup: Container security scanning pipeline
Task ID: os_gff_075
Domain: os
"""

import os
import shlex
import subprocess
import time
from pathlib import Path

WORKDIR = '/home/user'
TASK_ID = 'os_gff_075'
SUDO_PASS = 'password'

def sudo_run(cmd_str):
    """Run a command with sudo, piping password via stdin."""
    subprocess.run(
        f"echo '{SUDO_PASS}' | sudo -S {cmd_str}",
        shell=True, check=True,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

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

def create_initial():
    # 1. Create /opt/security directory
    sudo_run('mkdir -p /opt/security')
    sudo_run('chmod 777 /opt/security')

    # 2. Create images.txt with realistic Docker image references
    images = [
        'nginx:1.25.3',
        'python:3.11-slim',
        'node:20-alpine',
        'redis:7.2',
        'postgres:16.1',
        'golang:1.21-bookworm',
        'ubuntu:22.04',
        'alpine:3.19',
    ]
    Path('/opt/security/images.txt').write_text('\n'.join(images) + '\n')
    print('Created /opt/security/images.txt with image references')

    # 3. Ensure NO scan_images.sh exists (the agent must create it)
    script_path = '/opt/security/scan_images.sh'
    if os.path.exists(script_path):
        os.remove(script_path)

    # 4. Create trivy stub if not present
    if not os.path.exists('/usr/local/bin/trivy'):
        trivy_stub = r'''#!/bin/bash
# Trivy stub for CUA-Gym testing
OUTPUT_FILE=""
IMAGE=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        image) shift ;;
        --format) shift 2 ;;
        --output) OUTPUT_FILE="$2"; shift 2 ;;
        --severity) shift 2 ;;
        *) IMAGE="$1"; shift ;;
    esac
done

HAS_CRITICAL=0
case "$IMAGE" in
    *ubuntu*|*python*|*golang*) HAS_CRITICAL=1 ;;
esac

if [ "$HAS_CRITICAL" -eq 1 ]; then
    JSON_OUTPUT='{
  "SchemaVersion": 2,
  "ArtifactName": "'"$IMAGE"'",
  "ArtifactType": "container_image",
  "Results": [
    {
      "Target": "'"$IMAGE"' (debian 12.4)",
      "Class": "os-pkgs",
      "Type": "debian",
      "Vulnerabilities": [
        {"VulnerabilityID": "CVE-2024-1234", "PkgName": "libssl3", "InstalledVersion": "3.0.11-1", "FixedVersion": "3.0.13-1", "Severity": "CRITICAL", "Title": "OpenSSL: Buffer overflow"},
        {"VulnerabilityID": "CVE-2024-5678", "PkgName": "libc6", "InstalledVersion": "2.36-9", "FixedVersion": "2.36-10", "Severity": "HIGH", "Title": "glibc: Use-after-free"},
        {"VulnerabilityID": "CVE-2024-9012", "PkgName": "zlib1g", "InstalledVersion": "1.2.13-1", "FixedVersion": "1.2.13-2", "Severity": "HIGH", "Title": "zlib: buffer overflow"}
      ]
    }
  ]
}'
else
    JSON_OUTPUT='{
  "SchemaVersion": 2,
  "ArtifactName": "'"$IMAGE"'",
  "ArtifactType": "container_image",
  "Results": [
    {
      "Target": "'"$IMAGE"' (alpine 3.19)",
      "Class": "os-pkgs",
      "Type": "alpine",
      "Vulnerabilities": [
        {"VulnerabilityID": "CVE-2024-2345", "PkgName": "busybox", "InstalledVersion": "1.36.1-r6", "FixedVersion": "1.36.1-r7", "Severity": "HIGH", "Title": "busybox: command injection"}
      ]
    }
  ]
}'
fi

if [ -n "$OUTPUT_FILE" ]; then
    echo "$JSON_OUTPUT" > "$OUTPUT_FILE"
else
    echo "$JSON_OUTPUT"
fi
exit 0
'''
        # Write trivy stub via temp file + sudo mv
        tmp_path = '/tmp/trivy_stub.sh'
        Path(tmp_path).write_text(trivy_stub)
        sudo_run(f'cp {tmp_path} /usr/local/bin/trivy')
        sudo_run('chmod 755 /usr/local/bin/trivy')
        os.remove(tmp_path)
        print('Created trivy stub at /usr/local/bin/trivy')

    # 5. Open a terminal for the user to work in
    launch_gui('gnome-terminal', delay_sec=2.0)
    print('GUI_READY: launched terminal with DISPLAY=:0')

create_initial()

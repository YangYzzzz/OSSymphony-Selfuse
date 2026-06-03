"""
Initial Setup: Server hostnames duplicate list for deduplication task
Task ID: osworld_writer_dedup_005
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_dedup_005'
OUTPUT = f'{WORKDIR}/{TASK_ID}.docx'


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
    doc = Document()

    # 40 unique server hostnames in first-occurrence order
    unique_hostnames = [
        'web-server-01.prod',
        'db-server-02.prod',
        'web-server-03.prod',
        'app-server-01.prod',
        'cache-server-01.prod',
        'db-server-01.prod',
        'web-server-02.prod',
        'monitor-01.prod',
        'mail-server-01.prod',
        'ftp-server-01.prod',
        'app-server-02.prod',
        'lb-server-01.prod',
        'proxy-server-01.prod',
        'auth-server-01.prod',
        'storage-node-01.prod',
        'backup-server-01.prod',
        'web-server-04.prod',
        'db-server-03.prod',
        'log-server-01.prod',
        'metrics-server-01.prod',
        'api-gateway-01.prod',
        'scheduler-01.prod',
        'queue-server-01.prod',
        'search-server-01.prod',
        'cdn-node-01.prod',
        'dns-server-01.prod',
        'ntp-server-01.prod',
        'vpn-server-01.prod',
        'firewall-01.prod',
        'bastion-host-01.prod',
        'ci-server-01.prod',
        'registry-server-01.prod',
        'artifact-server-01.prod',
        'report-server-01.prod',
        'etl-server-01.prod',
        'ml-worker-01.prod',
        'staging-web-01.prod',
        'staging-db-01.prod',
        'dev-server-01.prod',
        'test-server-01.prod',
    ]

    # Build the full list with duplicates (2-4 copies per host, scattered)
    # Each hostname will appear 2-4 times in the document
    # We simulate multiple monitoring runs by interleaving duplicate entries
    # Total lines: approximately 120

    # Run 1: all 40 hosts
    # Run 2: first 35 hosts  (simulating slightly different monitoring sweep)
    # Run 3: hosts 5-40      (another sweep with offset)
    # Run 4: hosts 1-10      (targeted sweep of critical servers)

    lines = []

    # Run 1 (full sweep)
    lines.extend(unique_hostnames)

    # Run 2 (35 hosts in shuffled order to simulate unsorted dump)
    run2 = [
        'web-server-01.prod', 'db-server-01.prod', 'app-server-01.prod',
        'cache-server-01.prod', 'web-server-02.prod', 'monitor-01.prod',
        'mail-server-01.prod', 'ftp-server-01.prod', 'app-server-02.prod',
        'lb-server-01.prod', 'proxy-server-01.prod', 'auth-server-01.prod',
        'storage-node-01.prod', 'backup-server-01.prod', 'web-server-03.prod',
        'db-server-02.prod', 'web-server-04.prod', 'db-server-03.prod',
        'log-server-01.prod', 'metrics-server-01.prod', 'api-gateway-01.prod',
        'scheduler-01.prod', 'queue-server-01.prod', 'search-server-01.prod',
        'cdn-node-01.prod', 'dns-server-01.prod', 'ntp-server-01.prod',
        'vpn-server-01.prod', 'firewall-01.prod', 'bastion-host-01.prod',
        'ci-server-01.prod', 'registry-server-01.prod', 'artifact-server-01.prod',
        'report-server-01.prod', 'etl-server-01.prod',
    ]
    lines.extend(run2)

    # Run 3 (partial sweep of second half + some from first half)
    run3 = [
        'ml-worker-01.prod', 'staging-web-01.prod', 'staging-db-01.prod',
        'dev-server-01.prod', 'test-server-01.prod', 'web-server-01.prod',
        'db-server-02.prod', 'app-server-01.prod', 'cache-server-01.prod',
        'api-gateway-01.prod', 'scheduler-01.prod', 'queue-server-01.prod',
        'search-server-01.prod', 'cdn-node-01.prod', 'log-server-01.prod',
        'metrics-server-01.prod', 'monitor-01.prod', 'lb-server-01.prod',
        'backup-server-01.prod', 'bastion-host-01.prod',
    ]
    lines.extend(run3)

    # Run 4 (targeted sweep of critical/web servers)
    run4 = [
        'web-server-01.prod', 'web-server-02.prod', 'web-server-03.prod',
        'web-server-04.prod', 'db-server-01.prod', 'db-server-02.prod',
        'db-server-03.prod', 'app-server-01.prod', 'app-server-02.prod',
        'lb-server-01.prod',
    ]
    lines.extend(run4)

    # Write each hostname as its own paragraph (line)
    for hostname in lines:
        doc.add_paragraph(hostname)

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')
    print(f'Total lines (with duplicates): {len(lines)}')

    # GUI-ready startup
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()

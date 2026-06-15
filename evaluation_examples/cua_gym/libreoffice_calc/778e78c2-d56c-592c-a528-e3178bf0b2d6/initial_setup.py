"""
Initial Setup: Capacity planning automation system - pre-task state
Task ID: os_adm_085
Domain: os (system administration)

Creates 30 days of historical metric CSV files in /var/lib/metrics/
with realistic CPU, memory, and disk usage data showing gradual growth trends.
"""

import os
import shlex
import subprocess
import time
import csv
import random
from datetime import datetime, timedelta

WORKDIR = '/home/user'
TASK_ID = 'os_adm_085'
METRICS_DIR = '/var/lib/metrics'


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


def sudo_run(cmd):
    """Run a command with sudo using password from stdin."""
    proc = subprocess.Popen(
        ['sudo', '-S'] + cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    proc.communicate(input=b'password\n')
    return proc.returncode


def generate_metric_csvs():
    """Generate 30 days of realistic metric CSV files with gradual growth trends."""
    sudo_run(['mkdir', '-p', METRICS_DIR])
    sudo_run(['chmod', '777', METRICS_DIR])

    random.seed(42)  # Reproducible data
    today = datetime(2026, 4, 2)

    # Base values and daily growth rates (simulating gradual resource consumption)
    # CPU: starts ~55%, grows ~0.6%/day => reaches ~73% by day 30
    # Memory: starts ~68%, grows ~0.5%/day => reaches ~83% by day 30
    # Disk: starts ~72%, grows ~0.7%/day => reaches ~93% by day 30 (approaching 95% threshold)
    metrics_config = {
        'cpu': {
            'base': 55.0,
            'daily_growth': 0.6,
            'noise_std': 3.0,
            'headers': ['timestamp', 'cpu_user_pct', 'cpu_system_pct', 'cpu_idle_pct', 'load_avg_1m', 'load_avg_5m', 'load_avg_15m'],
        },
        'mem': {
            'base': 68.0,
            'daily_growth': 0.5,
            'noise_std': 2.5,
            'headers': ['timestamp', 'mem_total_mb', 'mem_used_mb', 'mem_free_mb', 'mem_cached_mb', 'swap_used_mb'],
        },
        'disk': {
            'base': 72.0,
            'daily_growth': 0.7,
            'noise_std': 1.5,
            'headers': ['timestamp', 'disk_total_gb', 'disk_used_gb', 'disk_free_gb', 'inode_used_pct'],
        },
    }

    total_mem_mb = 16384  # 16 GB
    total_disk_gb = 500   # 500 GB

    for day_offset in range(30, 0, -1):
        date = today - timedelta(days=day_offset)
        date_str = date.strftime('%Y-%m-%d')
        day_index = 30 - day_offset  # 0..29

        # --- CPU CSV ---
        cfg = metrics_config['cpu']
        cpu_total = cfg['base'] + cfg['daily_growth'] * day_index + random.gauss(0, cfg['noise_std'])
        cpu_total = max(20, min(99, cpu_total))
        cpu_user = cpu_total * random.uniform(0.65, 0.75)
        cpu_system = cpu_total - cpu_user
        cpu_idle = 100.0 - cpu_total
        load_1 = cpu_total / 25.0 + random.gauss(0, 0.3)
        load_5 = cpu_total / 27.0 + random.gauss(0, 0.2)
        load_15 = cpu_total / 30.0 + random.gauss(0, 0.1)

        cpu_file = os.path.join(METRICS_DIR, f'cpu_{date_str}.csv')
        with open(cpu_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(cfg['headers'])
            # Write 24 hourly samples for the day
            for hour in range(24):
                ts = f'{date_str} {hour:02d}:00:00'
                hour_noise = random.gauss(0, 2.0)
                h_user = round(cpu_user + hour_noise * 0.7, 2)
                h_sys = round(cpu_system + hour_noise * 0.3, 2)
                h_idle = round(100.0 - h_user - h_sys, 2)
                h_l1 = round(load_1 + random.gauss(0, 0.2), 2)
                h_l5 = round(load_5 + random.gauss(0, 0.15), 2)
                h_l15 = round(load_15 + random.gauss(0, 0.1), 2)
                writer.writerow([ts, h_user, h_sys, max(0, h_idle), max(0, h_l1), max(0, h_l5), max(0, h_l15)])

        # --- Memory CSV ---
        cfg = metrics_config['mem']
        mem_pct = cfg['base'] + cfg['daily_growth'] * day_index + random.gauss(0, cfg['noise_std'])
        mem_pct = max(30, min(99, mem_pct))
        mem_used = total_mem_mb * mem_pct / 100.0
        mem_free = total_mem_mb - mem_used
        mem_cached = mem_free * random.uniform(0.3, 0.5)
        swap_used = max(0, (mem_pct - 75) * 50 + random.gauss(0, 30))

        mem_file = os.path.join(METRICS_DIR, f'mem_{date_str}.csv')
        with open(mem_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(cfg['headers'])
            for hour in range(24):
                ts = f'{date_str} {hour:02d}:00:00'
                hour_noise = random.gauss(0, 1.5)
                h_used = round(mem_used + hour_noise * 100, 1)
                h_free = round(total_mem_mb - h_used, 1)
                h_cached = round(mem_cached + random.gauss(0, 50), 1)
                h_swap = round(max(0, swap_used + random.gauss(0, 20)), 1)
                writer.writerow([ts, total_mem_mb, h_used, max(0, h_free), max(0, h_cached), max(0, h_swap)])

        # --- Disk CSV ---
        cfg = metrics_config['disk']
        disk_pct = cfg['base'] + cfg['daily_growth'] * day_index + random.gauss(0, cfg['noise_std'])
        disk_pct = max(30, min(99, disk_pct))
        disk_used = total_disk_gb * disk_pct / 100.0
        disk_free = total_disk_gb - disk_used
        inode_pct = disk_pct * random.uniform(0.4, 0.6)

        disk_file = os.path.join(METRICS_DIR, f'disk_{date_str}.csv')
        with open(disk_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(cfg['headers'])
            for hour in range(24):
                ts = f'{date_str} {hour:02d}:00:00'
                hour_noise = random.gauss(0, 0.5)
                h_used = round(disk_used + hour_noise, 2)
                h_free = round(total_disk_gb - h_used, 2)
                h_inode = round(inode_pct + random.gauss(0, 0.5), 2)
                writer.writerow([ts, total_disk_gb, h_used, max(0, h_free), max(0, h_inode)])

    print(f'Created 30 days of metric CSVs in {METRICS_DIR}')
    # List files
    files = sorted(os.listdir(METRICS_DIR))
    print(f'Total files: {len(files)}')
    print(f'Sample: {files[:3]} ... {files[-3:]}')


def install_dependencies():
    """Ensure required Python packages are available."""
    sudo_run(['apt-get', 'update', '-qq'])
    sudo_run(['apt-get', 'install', '-y', '-qq',
              'python3-numpy', 'python3-scipy', 'python3-jinja2',
              'python3-matplotlib'])
    # Also try pip as fallback
    subprocess.run(['pip3', 'install', 'numpy', 'scipy', 'jinja2', 'matplotlib'],
                   check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print('Dependencies installed/verified')


def setup_environment():
    """Create supporting directories and a README for the task."""
    # Create a workspace readme so the user understands what they have
    readme_content = """# Capacity Planning Task

## Available Resources
- Historical metrics: /var/lib/metrics/
  - cpu_YYYY-MM-DD.csv (30 days)
  - mem_YYYY-MM-DD.csv (30 days)
  - disk_YYYY-MM-DD.csv (30 days)

## Installed Packages
- Python3 with numpy, scipy, jinja2, matplotlib

## Capacity Thresholds
- CPU: 85%
- Memory: 90%
- Disk: 95%

## Task
Create a capacity planning automation system at /usr/local/bin/capacity_planner.py
"""
    with open(os.path.join(WORKDIR, 'capacity_planning_readme.txt'), 'w') as f:
        f.write(readme_content)
    print('Environment setup complete')


def main():
    install_dependencies()
    generate_metric_csvs()
    setup_environment()

    # GUI-ready: open terminal and file manager showing the metrics
    launch_gui('nautilus "/var/lib/metrics"', delay_sec=1.5)
    launch_gui('gnome-terminal', delay_sec=1.5)
    print('GUI_READY: launched nautilus and terminal with DISPLAY=:0')


main()

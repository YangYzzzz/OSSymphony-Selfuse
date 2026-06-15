"""
Initial Setup: Log file archival task - create initial /home/user/logs/ directory with 15 .log files
Task ID: osworld_multi_apps_code_batch_terminal_007
Domain: os / multi_apps (bash scripting + LibreOffice Writer)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_code_batch_terminal_007'
LOGS_DIR = f'{WORKDIR}/logs'


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
    # Create logs directory (no archive subdir)
    os.makedirs(LOGS_DIR, exist_ok=True)

    # Remove any existing archive directory to ensure clean initial state
    archive_dir = os.path.join(LOGS_DIR, 'archive')
    if os.path.exists(archive_dir):
        import shutil
        shutil.rmtree(archive_dir)

    # Remove any existing .gz files in logs dir
    for fname in os.listdir(LOGS_DIR):
        if fname.endswith('.gz'):
            os.remove(os.path.join(LOGS_DIR, fname))

    # Remove any existing writer document for this task
    writer_doc = os.path.join(WORKDIR, f'{TASK_ID}.docx')
    if os.path.exists(writer_doc):
        os.remove(writer_doc)

    # Define 15 log files: 9 older than 7 days, 6 within last 7 days
    # We create files then use 'touch -d' to set modification times
    log_files_old = [
        ('app_server.log',       '-30 days', 'Application server log - old entries\nERROR 2025-12-15 09:00:00 Database connection timeout\nINFO  2025-12-15 08:55:00 Server started on port 8080\nWARN  2025-12-14 23:10:00 Memory usage at 85%\n'),
        ('auth_service.log',     '-25 days', 'Auth service log\nINFO  2025-12-20 14:22:11 User login: alice@corp.com\nINFO  2025-12-20 14:21:05 User login: bob@corp.com\nERROR 2025-12-20 12:00:00 Failed login attempt from 192.168.1.45\n'),
        ('batch_processor.log',  '-21 days', 'Batch processor log\nINFO  2025-12-24 03:00:01 Batch job started: nightly_report\nINFO  2025-12-24 03:15:22 Processed 4823 records\nINFO  2025-12-24 03:15:23 Batch job completed successfully\n'),
        ('cache_service.log',    '-18 days', 'Cache service log\nWARN  2025-12-27 11:30:00 Cache hit rate dropped to 62%\nINFO  2025-12-27 10:00:00 Cache flushed: 15423 keys expired\nINFO  2025-12-26 22:00:00 Cache initialized: 512 MB allocated\n'),
        ('db_backup.log',        '-15 days', 'Database backup log\nINFO  2025-12-30 02:00:05 Backup started: prod_database_v2\nINFO  2025-12-30 02:47:13 Backup size: 8.3 GB\nINFO  2025-12-30 02:47:14 Backup uploaded to s3://corp-backups/2025-12-30/\n'),
        ('email_daemon.log',     '-14 days', 'Email daemon log\nINFO  2025-12-31 09:15:00 Sent 342 emails in queue\nWARN  2025-12-31 08:50:00 SMTP server slow response: 4200ms\nERROR 2025-12-31 07:00:00 Mail delivery failed: user@example.com (mailbox full)\n'),
        ('file_watcher.log',     '-12 days', 'File watcher log\nINFO  2026-01-02 16:00:11 Watched directories: /home/user/uploads, /var/spool/cron\nINFO  2026-01-02 15:45:00 New file detected: report_Q4_2025.xlsx\nINFO  2026-01-02 15:44:58 File moved to /home/user/archive/report_Q4_2025.xlsx\n'),
        ('job_scheduler.log',    '-10 days', 'Job scheduler log\nINFO  2026-01-04 00:00:01 Scheduled jobs: 17 active\nINFO  2026-01-03 23:58:00 Job "cleanup_temp" finished in 2.3s\nWARN  2026-01-03 20:00:00 Job "data_sync" missed schedule: service unavailable\n'),
        ('kernel_monitor.log',   '-8 days',  'Kernel monitor log\nINFO  2026-01-06 12:00:00 Kernel version: 5.15.0-92-generic\nWARN  2026-01-06 11:30:00 High I/O wait detected: 18%\nINFO  2026-01-06 08:00:00 System uptime: 14 days, 3 hours\n'),
    ]

    log_files_new = [
        ('load_balancer.log',    '-5 days',  'Load balancer log\nINFO  2026-01-15 10:00:00 Active backend servers: 4\nINFO  2026-01-15 09:55:00 Request routed to backend-3: 45ms\nINFO  2026-01-15 09:30:00 Health check passed: all backends healthy\n'),
        ('network_scan.log',     '-4 days',  'Network scan log\nINFO  2026-01-16 14:00:00 Scan started: 192.168.1.0/24\nINFO  2026-01-16 14:02:45 Found 23 active hosts\nWARN  2026-01-16 14:02:46 Open port 23 (telnet) on 192.168.1.105\n'),
        ('ops_dashboard.log',    '-3 days',  'Ops dashboard log\nINFO  2026-01-17 08:30:00 Dashboard v2.4.1 started\nINFO  2026-01-17 08:30:15 Loaded 8 metric widgets\nINFO  2026-01-17 07:00:00 Alert: CPU usage > 90% on worker-node-2\n'),
        ('payment_gateway.log',  '-2 days',  'Payment gateway log\nINFO  2026-01-18 12:00:00 Transactions processed: 1842\nINFO  2026-01-18 11:59:59 Transaction TXN-20260118-9921: $249.99 APPROVED\nERROR 2026-01-18 10:22:00 Stripe webhook verification failed\n'),
        ('queue_worker.log',     '-1 day',   'Queue worker log\nINFO  2026-01-19 06:00:00 Worker pool started: 8 threads\nINFO  2026-01-19 05:58:00 Jobs in queue: 127\nINFO  2026-01-19 05:55:00 Processed 95 jobs in last hour\n'),
        ('reporting_engine.log', '-6 hours', 'Reporting engine log\nINFO  2026-01-20 16:30:00 Report generated: quarterly_sales_Q4_2025.pdf\nINFO  2026-01-20 16:29:00 Data rows processed: 78432\nINFO  2026-01-20 14:00:00 Scheduled report: weekly_ops_summary\n'),
    ]

    all_log_files = log_files_old + log_files_new

    for fname, time_offset, content in all_log_files:
        fpath = os.path.join(LOGS_DIR, fname)
        with open(fpath, 'w') as f:
            f.write(content)
        # Set modification time using touch -d
        result = subprocess.run(
            ['touch', '-d', time_offset, fpath],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f'WARNING: Could not set mtime for {fname}: {result.stderr}')

    print(f'Created {len(all_log_files)} log files in {LOGS_DIR}')
    print(f'  - {len(log_files_old)} files older than 7 days')
    print(f'  - {len(log_files_new)} files within last 7 days')

    # Verify timestamps
    result = subprocess.run(
        ['find', LOGS_DIR, '-maxdepth', '1', '-name', '*.log', '-mtime', '+7'],
        capture_output=True, text=True
    )
    old_files = [f for f in result.stdout.strip().split('\n') if f]
    print(f'Files found by find -mtime +7: {len(old_files)}')

    # GUI-ready startup: open a terminal window for the agent to write the script
    launch_gui('gnome-terminal', delay_sec=2.0)
    print('GUI_READY: launched gnome-terminal with DISPLAY=:0')


create_initial()

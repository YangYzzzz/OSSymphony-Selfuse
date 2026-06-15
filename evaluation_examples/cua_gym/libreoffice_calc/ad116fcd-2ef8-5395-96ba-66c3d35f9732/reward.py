"""
Reward Script: PostgreSQL backup script with cron scheduling
Task ID: os_adm_030
Domain: os (system administration)
Scoring:
  Component 1: Script exists and is executable (0.15)
  Component 2: Script contains pg_dumpall with date stamps and compression (0.25)
  Component 3: Script outputs to /backup/postgres/ (0.10)
  Component 4: Compressed backup file exists in /backup/postgres/ (0.20)
  Component 5: Cron entry schedules script at 0 2 * * * (0.30)
"""

import os
import re
import stat
import glob

WORKDIR = '/home/user'
TASK_ID = 'os_adm_030'
SCRIPT_PATH = '/usr/local/bin/pg_backup.sh'
BACKUP_DIR = '/backup/postgres'


def verify_task():
    """
    Verify PostgreSQL backup script deployment and cron scheduling.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ---- Precondition: backup directory exists ----
    if not os.path.isdir(BACKUP_DIR):
        print(f"CRITICAL: Backup directory {BACKUP_DIR} does not exist")
        print("REWARD: 0.0")
        return 0.0

    # ---- Component 1: Script exists and is executable (0.15 points) ----
    try:
        if os.path.isfile(SCRIPT_PATH):
            mode = stat.S_IMODE(os.stat(SCRIPT_PATH).st_mode)
            # Check that owner execute bit is set
            if mode & stat.S_IXUSR:
                print(f"PASS: Component 1 - Script exists at {SCRIPT_PATH} with mode {oct(mode)} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 - Script exists but is not executable (mode: {oct(mode)})")
        else:
            print(f"FAIL: Component 1 - Script does not exist at {SCRIPT_PATH}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # ---- Component 2: Script uses pg_dumpall with date stamps and compression (0.25 points) ----
    try:
        if os.path.isfile(SCRIPT_PATH):
            with open(SCRIPT_PATH, 'r') as f:
                content = f.read()

            has_pg_dump = 'pg_dumpall' in content or 'pg_dump' in content
            has_date = re.search(r'date\s*\+', content) is not None or 'DATE=' in content
            has_gzip = 'gzip' in content or '.gz' in content

            if has_pg_dump and has_date and has_gzip:
                print(f"PASS: Component 2 - Script uses pg_dump with date stamps and compression (0.25 pts)")
                total_score += 0.25
            else:
                missing = []
                if not has_pg_dump:
                    missing.append('pg_dumpall/pg_dump')
                if not has_date:
                    missing.append('date stamp')
                if not has_gzip:
                    missing.append('compression (gzip/.gz)')
                print(f"FAIL: Component 2 - Missing: {', '.join(missing)}")
        else:
            print(f"FAIL: Component 2 - Script does not exist, cannot check content")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # ---- Component 3: Script references /backup/postgres/ output dir (0.10 points) ----
    try:
        if os.path.isfile(SCRIPT_PATH):
            with open(SCRIPT_PATH, 'r') as f:
                content = f.read()

            if '/backup/postgres' in content:
                print(f"PASS: Component 3 - Script references {BACKUP_DIR} (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 - Script does not reference {BACKUP_DIR}")
        else:
            print(f"FAIL: Component 3 - Script does not exist")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # ---- Component 4: Compressed backup file exists in /backup/postgres/ (0.20 points) ----
    try:
        backup_files = glob.glob(os.path.join(BACKUP_DIR, 'pg_all_*.sql.gz'))
        if not backup_files:
            # Also check for any .gz or .sql files as alternative naming
            backup_files = glob.glob(os.path.join(BACKUP_DIR, '*.gz'))

        if backup_files:
            # Verify at least one has non-zero size
            valid_backups = [f for f in backup_files if os.path.getsize(f) > 0]
            if valid_backups:
                sizes = [(os.path.basename(f), os.path.getsize(f)) for f in valid_backups]
                print(f"PASS: Component 4 - Backup file(s) found: {sizes} (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 - Backup files found but all are empty")
        else:
            print(f"FAIL: Component 4 - No backup files found in {BACKUP_DIR}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # ---- Component 5: Cron entry at 0 2 * * * for pg_backup.sh (0.30 points) ----
    try:
        cron_found = False
        cron_pattern = re.compile(r'^\s*0\s+2\s+\*\s+\*\s+\*\s+.*pg_backup\.sh', re.MULTILINE)

        # Check /etc/crontab
        if os.path.isfile('/etc/crontab'):
            with open('/etc/crontab', 'r') as f:
                etc_crontab = f.read()
            if cron_pattern.search(etc_crontab):
                cron_found = True
                print("  Found cron entry in /etc/crontab")

        # Check /etc/cron.d/ files
        if os.path.isdir('/etc/cron.d'):
            for fname in os.listdir('/etc/cron.d'):
                fpath = os.path.join('/etc/cron.d', fname)
                if os.path.isfile(fpath):
                    try:
                        with open(fpath, 'r') as f:
                            content = f.read()
                        if cron_pattern.search(content):
                            cron_found = True
                            print(f"  Found cron entry in {fpath}")
                    except Exception:
                        pass

        # Check root crontab via spool
        root_crontab_path = '/var/spool/cron/crontabs/root'
        if os.path.isfile(root_crontab_path):
            try:
                with open(root_crontab_path, 'r') as f:
                    content = f.read()
                if cron_pattern.search(content):
                    cron_found = True
                    print("  Found cron entry in root crontab spool")
            except PermissionError:
                # Try via subprocess as fallback
                import subprocess
                result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
                if cron_pattern.search(result.stdout):
                    cron_found = True
                    print("  Found cron entry in root crontab (via crontab -l)")

        # Check postgres user crontab spool
        pg_crontab_path = '/var/spool/cron/crontabs/postgres'
        if os.path.isfile(pg_crontab_path):
            try:
                with open(pg_crontab_path, 'r') as f:
                    content = f.read()
                if cron_pattern.search(content):
                    cron_found = True
                    print("  Found cron entry in postgres crontab spool")
            except PermissionError:
                pass

        if cron_found:
            print(f"PASS: Component 5 - Cron entry found: 0 2 * * * pg_backup.sh (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 5 - No cron entry for pg_backup.sh at 0 2 * * *")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    final_score = min(total_score, 1.0)
    # Round to avoid floating point issues
    final_score = round(final_score, 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

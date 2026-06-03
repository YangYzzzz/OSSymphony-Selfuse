"""
Initial Setup: Database migration framework with Flyway for PostgreSQL
Task ID: os_adm_078
Domain: os
"""

import os
import shlex
import subprocess
import time
from pathlib import Path

WORKDIR = '/home/user'
TASK_ID = 'os_adm_078'
SUDO_PASS = 'password'


def run(cmd, **kwargs):
    """Run a command, print output."""
    print(f"  RUN: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, **kwargs)
    if result.stdout.strip():
        print(f"  OUT: {result.stdout.strip()}")
    if result.stderr.strip():
        print(f"  ERR: {result.stderr.strip()}")
    return result


def sudo(cmd):
    """Run command with sudo using password."""
    full = f"echo '{SUDO_PASS}' | sudo -S bash -c {shlex.quote(cmd)}"
    return run(full)


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
    # =========================================================
    # 0. Enable passwordless sudo for the rest of the setup
    # =========================================================
    print("=== Enabling passwordless sudo ===")
    sudo("echo 'user ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/user-nopasswd && chmod 440 /etc/sudoers.d/user-nopasswd")

    # =========================================================
    # 1. Install PostgreSQL
    # =========================================================
    print("=== Installing PostgreSQL ===")
    run("sudo apt-get update -qq")
    run("sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq postgresql postgresql-client")
    run("sudo systemctl start postgresql")
    run("sudo systemctl enable postgresql")
    time.sleep(3)

    # Verify postgresql is running
    result = run("sudo systemctl is-active postgresql")
    if 'active' not in result.stdout:
        print("WARNING: PostgreSQL may not be running, trying to start again...")
        run("sudo pg_ctlcluster 14 main start || sudo pg_ctlcluster 16 main start || sudo pg_ctlcluster 15 main start")
        time.sleep(2)

    # =========================================================
    # 2. Create production_app database and V1 schema
    # =========================================================
    print("=== Creating production_app database ===")
    run("sudo -u postgres createdb production_app 2>/dev/null || true")

    v1_sql = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL,
    full_name VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

INSERT INTO users (username, email, full_name) VALUES
    ('sarah.chen', 'sarah.chen@company.com', 'Sarah Chen'),
    ('marcus.johnson', 'marcus.johnson@company.com', 'Marcus Johnson'),
    ('aisha.patel', 'aisha.patel@company.com', 'Aisha Patel'),
    ('david.kim', 'david.kim@company.com', 'David Kim'),
    ('elena.rodriguez', 'elena.rodriguez@company.com', 'Elena Rodriguez'),
    ('james.wilson', 'james.wilson@company.com', 'James Wilson'),
    ('maria.garcia', 'maria.garcia@company.com', 'Maria Garcia'),
    ('robert.taylor', 'robert.taylor@company.com', 'Robert Taylor')
ON CONFLICT (username) DO NOTHING;
"""
    # Write SQL to temp file and execute
    Path("/tmp/v1_init.sql").write_text(v1_sql)
    run("sudo -u postgres psql -d production_app -f /tmp/v1_init.sql")

    # =========================================================
    # 3. Install Flyway at /opt/flyway/
    # =========================================================
    print("=== Installing Flyway ===")
    run("sudo mkdir -p /opt/flyway /opt/flyway/sql /opt/flyway/conf")
    run("sudo chown -R user:user /opt/flyway")

    # Create a functional Flyway wrapper script
    flyway_script = r'''#!/bin/bash
# Flyway CLI wrapper for PostgreSQL migration management
# Flyway Community Edition 9.22.3 (compatible)

FLYWAY_DIR="/opt/flyway"
CONF_FILE=""
SQL_DIR=""
COMMAND=""

for arg in "$@"; do
    case "$arg" in
        migrate|info|validate|clean|baseline|repair)
            COMMAND="$arg"
            ;;
        -configFiles=*)
            CONF_FILE="${arg#-configFiles=}"
            ;;
        -locations=*)
            SQL_DIR="${arg#-locations=filesystem:}"
            ;;
    esac
done

# Find config
if [ -z "$CONF_FILE" ]; then
    if [ -f "$FLYWAY_DIR/conf/flyway.conf" ]; then
        CONF_FILE="$FLYWAY_DIR/conf/flyway.conf"
    elif [ -f "/opt/migrations/flyway.conf" ]; then
        CONF_FILE="/opt/migrations/flyway.conf"
    fi
fi

# Parse config
DB_URL=""
DB_USER=""
DB_PASSWORD=""
DB_NAME=""
DB_HOST="localhost"
DB_PORT="5432"

if [ -n "$CONF_FILE" ] && [ -f "$CONF_FILE" ]; then
    DB_URL=$(grep "^flyway.url" "$CONF_FILE" | head -1 | cut -d= -f2- | tr -d '[:space:]')
    DB_USER=$(grep "^flyway.user" "$CONF_FILE" | head -1 | cut -d= -f2- | tr -d '[:space:]')
    DB_PASSWORD=$(grep "^flyway.password" "$CONF_FILE" | head -1 | cut -d= -f2- | tr -d '[:space:]')
    DB_NAME=$(echo "$DB_URL" | sed 's|.*://[^/]*/||' | sed 's|[?].*||')
    if [ -z "$SQL_DIR" ]; then
        LOC=$(grep "^flyway.locations" "$CONF_FILE" | head -1 | cut -d= -f2- | tr -d '[:space:]')
        SQL_DIR=$(echo "$LOC" | sed 's|filesystem:||')
    fi
fi

[ -z "$DB_NAME" ] && DB_NAME="production_app"
[ -z "$DB_USER" ] && DB_USER="postgres"
[ -z "$SQL_DIR" ] && SQL_DIR="/opt/migrations/sql"

export PGPASSWORD="$DB_PASSWORD"

# Helper: run psql as correct user
run_psql() {
    if [ "$DB_USER" = "postgres" ]; then
        sudo -u postgres psql "$@" 2>/dev/null
    else
        psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" "$@" 2>/dev/null
    fi
}

# Ensure schema history table
run_psql -d "$DB_NAME" -c "
CREATE TABLE IF NOT EXISTS flyway_schema_history (
    installed_rank INTEGER NOT NULL,
    version VARCHAR(50),
    description VARCHAR(200) NOT NULL,
    type VARCHAR(20) NOT NULL,
    script VARCHAR(1000) NOT NULL,
    checksum INTEGER,
    installed_by VARCHAR(100) NOT NULL,
    installed_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    execution_time INTEGER NOT NULL,
    success BOOLEAN NOT NULL,
    PRIMARY KEY (installed_rank)
);"

case "$COMMAND" in
    info)
        echo "Schema version table \"public\".\"flyway_schema_history\":"
        echo "+-----------+---------+-------------------------+------+---------------------+---------+"
        echo "| Category  | Version | Description             | Type | Installed On        | State   |"
        echo "+-----------+---------+-------------------------+------+---------------------+---------+"

        # Applied migrations
        run_psql -d "$DB_NAME" -t -A -F '|' -c "
            SELECT version, description, type, to_char(installed_on, 'YYYY-MM-DD HH24:MI:SS'), success
            FROM flyway_schema_history
            WHERE version IS NOT NULL
            ORDER BY installed_rank;" | while IFS='|' read -r ver desc mtype inst succ; do
            [ -z "$ver" ] && continue
            if [ "$succ" = "t" ]; then state="Success"; else state="Failed"; fi
            printf "| Versioned | %-7s | %-23s | %-4s | %-19s | %-7s |\n" "$ver" "$desc" "$mtype" "$inst" "$state"
        done

        # Pending migrations
        if [ -d "$SQL_DIR" ]; then
            for sqlfile in $(ls "$SQL_DIR"/V*.sql 2>/dev/null | sort -V); do
                [ -f "$sqlfile" ] || continue
                fname=$(basename "$sqlfile")
                ver=$(echo "$fname" | sed 's/^V//' | sed 's/__.*//')
                desc=$(echo "$fname" | sed 's/^V[0-9]*__//' | sed 's/\.sql$//' | tr '_' ' ')
                applied=$(run_psql -d "$DB_NAME" -t -A -c "
                    SELECT COUNT(*) FROM flyway_schema_history WHERE version='$ver';")
                if [ "$applied" = "0" ] || [ -z "$applied" ]; then
                    printf "| Versioned | %-7s | %-23s | SQL  |                     | Pending |\n" "$ver" "$desc"
                fi
            done
        fi

        echo "+-----------+---------+-------------------------+------+---------------------+---------+"
        ;;

    migrate)
        if [ ! -d "$SQL_DIR" ]; then
            echo "ERROR: Migration directory $SQL_DIR not found"
            exit 1
        fi

        for sqlfile in $(ls "$SQL_DIR"/V*.sql 2>/dev/null | sort -V); do
            [ -f "$sqlfile" ] || continue
            fname=$(basename "$sqlfile")
            ver=$(echo "$fname" | sed 's/^V//' | sed 's/__.*//')
            desc=$(echo "$fname" | sed 's/^V[0-9]*__//' | sed 's/\.sql$//' | tr '_' ' ')

            applied=$(run_psql -d "$DB_NAME" -t -A -c "
                SELECT COUNT(*) FROM flyway_schema_history WHERE version='$ver' AND success=true;")
            if [ "$applied" != "0" ] && [ -n "$applied" ]; then
                continue
            fi

            echo "Migrating schema to version $ver - $desc"
            START_TIME=$(date +%s%N)

            if run_psql -d "$DB_NAME" -f "$sqlfile"; then
                END_TIME=$(date +%s%N)
                ELAPSED=$(( (END_TIME - START_TIME) / 1000000 ))
                max_rank=$(run_psql -d "$DB_NAME" -t -A -c "
                    SELECT COALESCE(MAX(installed_rank),0) FROM flyway_schema_history;")
                next_rank=$((max_rank + 1))
                run_psql -d "$DB_NAME" -c "
                    INSERT INTO flyway_schema_history (installed_rank, version, description, type, script, checksum, installed_by, execution_time, success)
                    VALUES ($next_rank, '$ver', '$desc', 'SQL', '$fname', 0, '$DB_USER', $ELAPSED, true);"
                echo "Successfully applied migration to version $ver"
            else
                END_TIME=$(date +%s%N)
                ELAPSED=$(( (END_TIME - START_TIME) / 1000000 ))
                max_rank=$(run_psql -d "$DB_NAME" -t -A -c "
                    SELECT COALESCE(MAX(installed_rank),0) FROM flyway_schema_history;")
                next_rank=$((max_rank + 1))
                run_psql -d "$DB_NAME" -c "
                    INSERT INTO flyway_schema_history (installed_rank, version, description, type, script, checksum, installed_by, execution_time, success)
                    VALUES ($next_rank, '$ver', '$desc', 'SQL', '$fname', 0, '$DB_USER', $ELAPSED, false);"
                echo "ERROR: Migration to version $ver failed!"
                exit 1
            fi
        done
        echo "Successfully applied all pending migrations"
        ;;

    baseline)
        max_rank=$(run_psql -d "$DB_NAME" -t -A -c "
            SELECT COALESCE(MAX(installed_rank),0) FROM flyway_schema_history;")
        next_rank=$((max_rank + 1))
        run_psql -d "$DB_NAME" -c "
            INSERT INTO flyway_schema_history (installed_rank, version, description, type, script, checksum, installed_by, execution_time, success)
            VALUES ($next_rank, '1', '<< Flyway Baseline >>', 'BASELINE', '<< Flyway Baseline >>', 0, '$DB_USER', 0, true);"
        echo "Successfully baselined schema with version: 1"
        ;;

    *)
        echo "Flyway Community Edition 9.22.3 by Redgate"
        echo ""
        echo "Usage: flyway [options] command"
        echo ""
        echo "Commands:"
        echo "  migrate    Migrates the database"
        echo "  info       Prints the details and status of all migrations"
        echo "  validate   Validates the applied migrations"
        echo "  baseline   Baselines an existing database"
        echo "  repair     Repairs the schema history table"
        echo "  clean      Drops all objects in the configured schemas"
        ;;
esac
'''

    Path("/opt/flyway/flyway").write_text(flyway_script)
    os.chmod("/opt/flyway/flyway", 0o755)
    print("Flyway wrapper installed at /opt/flyway/flyway")

    # PATH setup
    bashrc = Path("/home/user/.bashrc")
    bashrc_content = bashrc.read_text() if bashrc.exists() else ""
    if "/opt/flyway" not in bashrc_content:
        with open(str(bashrc), "a") as f:
            f.write('\nexport PATH="/opt/flyway:$PATH"\n')

    # Symlink for system access
    run("sudo ln -sf /opt/flyway/flyway /usr/local/bin/flyway")

    # =========================================================
    # 4. Create migration SQL files at /opt/migrations/sql/
    # =========================================================
    print("=== Creating migration SQL files ===")
    run("sudo mkdir -p /opt/migrations/sql")
    run("sudo chown -R user:user /opt/migrations")

    # V1 - already applied
    Path("/opt/migrations/sql/V1__Initial_schema.sql").write_text(
        """-- V1: Initial schema - Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL,
    full_name VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);
""")

    # V2 - Pending (agent must run this via migration)
    Path("/opt/migrations/sql/V2__Add_user_preferences.sql").write_text(
        """-- V2: Add user_preferences table
CREATE TABLE user_preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    theme VARCHAR(50) DEFAULT 'light',
    language VARCHAR(10) DEFAULT 'en',
    notifications_enabled BOOLEAN DEFAULT TRUE,
    email_digest VARCHAR(20) DEFAULT 'daily',
    timezone VARCHAR(100) DEFAULT 'UTC',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_user_preferences_user_id ON user_preferences(user_id);
""")

    # V3 - Pending
    Path("/opt/migrations/sql/V3__Add_indexes.sql").write_text(
        """-- V3: Add performance indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_users_is_active ON users(is_active);
""")

    # =========================================================
    # 5. Baseline V1 in Flyway schema_history
    # =========================================================
    print("=== Baselining V1 in Flyway ===")
    run("/opt/flyway/flyway baseline")

    # Verify: V1=Success, V2=Pending, V3=Pending
    print("=== Verifying initial state ===")
    run("/opt/flyway/flyway info")

    # =========================================================
    # 6. Confirm no flyway.conf or safe_migrate.sh exist yet
    # =========================================================
    print("=== Confirming task artifacts do NOT exist ===")
    run("test -f /opt/migrations/flyway.conf && echo 'ERROR: flyway.conf exists!' || echo 'OK: no flyway.conf'")
    run("test -f /usr/local/bin/safe_migrate.sh && echo 'ERROR: safe_migrate.sh exists!' || echo 'OK: no safe_migrate.sh'")

    # =========================================================
    # 7. Open terminal for the user
    # =========================================================
    launch_gui('gnome-terminal', delay_sec=1.5)
    print('GUI_READY: launched terminal with DISPLAY=:0')
    print('Initial setup complete.')


create_initial()

"""
Initial Setup: Configure log analysis workflow in ~/project
Task ID: vscode_wf_093
Domain: vscode (libreoffice_calc label)

Creates ~/project with a realistic app.log file and opens VSCode.
No .vscode config, no extensions, no scripts — the agent must set those up.
"""

import os
import shlex
import subprocess
import time
import random
import datetime

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_093'
PROJECT_DIR = f'{WORKDIR}/project'
LOG_DIR = f'{PROJECT_DIR}/logs'
LOG_FILE = f'{LOG_DIR}/app.log'


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


def generate_log_file():
    """Generate a realistic application log file with thousands of lines."""
    os.makedirs(LOG_DIR, exist_ok=True)

    levels = ['DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL']
    level_weights = [0.15, 0.50, 0.20, 0.12, 0.03]

    modules = [
        'AuthService', 'DatabasePool', 'APIGateway', 'CacheManager',
        'SessionHandler', 'FileUploader', 'NotificationService',
        'PaymentProcessor', 'UserManager', 'SearchIndexer',
        'HealthCheck', 'RateLimiter', 'EmailService', 'TaskScheduler',
        'WebSocketHandler'
    ]

    messages = {
        'DEBUG': [
            'Processing request with params: {user_id=%d, action=query}',
            'Cache lookup for key session_%d returned miss',
            'SQL query executed in %dms: SELECT * FROM users WHERE active=1',
            'Thread pool status: active=%d, idle=%d, queued=0',
            'Received heartbeat from node cluster-%d',
            'Parsing configuration from /etc/app/config.yml',
            'Memory allocation: heap=%dMB, stack=%dMB',
        ],
        'INFO': [
            'User %d logged in successfully from 192.168.1.%d',
            'Request completed: GET /api/v2/users (200) in %dms',
            'Database connection pool initialized with %d connections',
            'Scheduled job "daily-report" started at current timestamp',
            'File uploaded: report_q1_%d.pdf (%.1fMB)',
            'Cache hit ratio: %.1f%% (last 5 minutes)',
            'WebSocket connection established for client session_%d',
            'Email sent to user_%d@company.com: "Weekly Summary"',
            'Payment processed: order #%d amount $%.2f',
            'Service started on port 8080 with %d worker threads',
        ],
        'WARN': [
            'Slow query detected: %dms for SELECT on orders table',
            'Connection pool nearing capacity: %d/%d active',
            'Rate limit approaching for IP 10.0.%d.%d: %d/100 requests',
            'Deprecated API endpoint /api/v1/users called by client_%d',
            'Disk usage at %d%% on /var/log partition',
            'SSL certificate expires in %d days for api.internal.dev',
            'Memory usage high: %d%% of allocated heap',
            'Retry attempt %d/3 for external service call to payments.api.dev',
        ],
        'ERROR': [
            'Failed to connect to database replica db-replica-%d: Connection refused',
            'Unhandled exception in request handler: NullPointerException at line %d',
            'Authentication failed for user admin_%d: invalid credentials',
            'Timeout after %dms waiting for response from search-service',
            'File not found: /data/exports/report_%d.csv',
            'Payment gateway returned error 503 for transaction txn_%d',
            'Failed to parse JSON payload: Unexpected token at position %d',
        ],
        'FATAL': [
            'Out of memory: unable to allocate %dMB for request buffer',
            'Database master node unreachable after %d retries — entering read-only mode',
            'Critical configuration missing: JWT_SECRET not set in environment',
            'Unrecoverable state: data corruption detected in table "sessions"',
        ],
    }

    random.seed(42)
    start_time = datetime.datetime(2025, 3, 1, 0, 0, 0)
    lines = []

    for i in range(3500):
        # Advance time by random interval (1-30 seconds)
        start_time += datetime.timedelta(seconds=random.randint(1, 30))
        timestamp = start_time.strftime('%Y-%m-%d %H:%M:%S.') + f'{random.randint(0, 999):03d}'

        level = random.choices(levels, weights=level_weights, k=1)[0]
        module = random.choice(modules)

        msg_template = random.choice(messages[level])
        # Fill in format placeholders with random values
        try:
            fmt_count = msg_template.count('%')
            fmt_args = []
            for part in msg_template.split('%')[1:]:
                if part.startswith('d'):
                    fmt_args.append(random.randint(1, 9999))
                elif part.startswith('.1f'):
                    fmt_args.append(random.uniform(10, 99))
                elif part.startswith('.2f'):
                    fmt_args.append(random.uniform(10, 500))
                else:
                    fmt_args.append(random.randint(1, 999))
            msg = msg_template % tuple(fmt_args)
        except (TypeError, ValueError):
            msg = msg_template

        line = f'[{timestamp}] [{level}] [{module}] {msg}'
        lines.append(line)

    with open(LOG_FILE, 'w') as f:
        f.write('\n'.join(lines) + '\n')

    print(f'Generated log file with {len(lines)} lines: {LOG_FILE}')


def create_initial():
    # Create project directory structure
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create a basic README so the project looks real
    readme = f'{PROJECT_DIR}/README.md'
    with open(readme, 'w') as f:
        f.write("""# DataFlow Analytics Platform

Internal analytics service for processing and visualizing business metrics.

## Architecture
- **API Gateway**: Express.js REST API on port 8080
- **Database**: PostgreSQL 15 with connection pooling
- **Cache**: Redis 7.x for session and query caching
- **Workers**: Background job processing via task scheduler

## Logs
Application logs are written to `logs/app.log` in the format:
```
[TIMESTAMP] [LEVEL] [MODULE] message
```

Log levels: DEBUG, INFO, WARN, ERROR, FATAL

## Development
```bash
npm install
npm run dev
```
""")

    # Create a simple source file
    src_dir = f'{PROJECT_DIR}/src'
    os.makedirs(src_dir, exist_ok=True)
    with open(f'{src_dir}/server.js', 'w') as f:
        f.write("""const express = require('express');
const logger = require('./utils/logger');
const db = require('./db/connection');

const app = express();
const PORT = process.env.PORT || 8080;

app.use(express.json());

app.get('/health', (req, res) => {
    logger.info('HealthCheck', 'Health check requested');
    res.json({ status: 'ok', uptime: process.uptime() });
});

app.get('/api/v2/users', async (req, res) => {
    try {
        const users = await db.query('SELECT * FROM users WHERE active=1');
        logger.info('APIGateway', `Request completed: GET /api/v2/users (200)`);
        res.json(users);
    } catch (err) {
        logger.error('APIGateway', `Database query failed: ${err.message}`);
        res.status(500).json({ error: 'Internal server error' });
    }
});

app.listen(PORT, () => {
    logger.info('APIGateway', `Service started on port ${PORT} with 4 worker threads`);
});
""")

    # Generate the log file
    generate_log_file()

    # Ensure no .vscode directory exists (agent must create it)
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)

    # Ensure scripts directory doesn't exist
    scripts_dir = f'{PROJECT_DIR}/scripts'
    if os.path.exists(scripts_dir):
        import shutil
        shutil.rmtree(scripts_dir)

    print(f'Project structure created at {PROJECT_DIR}')

    # Open VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

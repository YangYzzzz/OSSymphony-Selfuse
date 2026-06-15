"""
Initial Setup: GitLab CI/CD Pipeline Configuration
Task ID: os_adm_067
Domain: os (DevOps/CI-CD)
Creates a realistic project directory with Dockerfile and app source,
but NO .gitlab-ci.yml — the agent must create that.
"""

import os
import shlex
import subprocess
import time
from pathlib import Path

WORKDIR = '/home/user'
TASK_ID = 'os_adm_067'
PROJECT_DIR = f'{WORKDIR}/webapp-inventory'


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
    # Create project directory structure
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/config', exist_ok=True)

    # --- Dockerfile ---
    Path(f'{PROJECT_DIR}/Dockerfile').write_text("""\
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

EXPOSE 8080

CMD ["python", "src/app.py"]
""")

    # --- requirements.txt ---
    Path(f'{PROJECT_DIR}/requirements.txt').write_text("""\
flask==3.0.2
gunicorn==21.2.0
psycopg2-binary==2.9.9
redis==5.0.1
prometheus-flask-instrumentator==7.0.0
""")

    # --- src/app.py ---
    Path(f'{PROJECT_DIR}/src/app.py').write_text("""\
from flask import Flask, jsonify
from prometheus_flask_instrumentator import Instrumentator
import os

app = Flask(__name__)
Instrumentator().instrument(app).expose(app)

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "version": os.getenv("APP_VERSION", "dev")})

@app.route('/api/inventory')
def list_inventory():
    # Placeholder — connects to PostgreSQL in production
    return jsonify({
        "items": [
            {"sku": "WH-1001", "name": "Industrial Bearing 6205", "qty": 342},
            {"sku": "WH-1002", "name": "Hydraulic Seal Kit HK-40", "qty": 128},
            {"sku": "WH-1003", "name": "Steel Flange DN50 PN16", "qty": 56},
        ]
    })

@app.route('/api/inventory/<sku>')
def get_item(sku):
    return jsonify({"sku": sku, "status": "found"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
""")

    # --- src/__init__.py ---
    Path(f'{PROJECT_DIR}/src/__init__.py').write_text("")

    # --- tests/test_integration.sh ---
    Path(f'{PROJECT_DIR}/tests/test_integration.sh').write_text("""\
#!/bin/bash
# Integration test suite for webapp-inventory
set -e

STAGING_URL="${STAGING_URL:-http://staging.internal:8080}"

echo "Running integration tests against $STAGING_URL ..."

# Health check
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$STAGING_URL/health")
if [ "$HTTP_CODE" -ne 200 ]; then
    echo "FAIL: Health endpoint returned $HTTP_CODE"
    exit 1
fi
echo "PASS: Health endpoint returned 200"

# Inventory list
RESPONSE=$(curl -s "$STAGING_URL/api/inventory")
if echo "$RESPONSE" | grep -q '"items"'; then
    echo "PASS: Inventory list returns items"
else
    echo "FAIL: Inventory list missing items key"
    exit 1
fi

echo "All integration tests passed."
""")
    os.chmod(f'{PROJECT_DIR}/tests/test_integration.sh', 0o755)

    # --- config/staging.env ---
    Path(f'{PROJECT_DIR}/config/staging.env').write_text("""\
APP_VERSION=staging
DATABASE_URL=postgresql://app:secret@db-staging.internal:5432/inventory
REDIS_URL=redis://cache-staging.internal:6379/0
LOG_LEVEL=DEBUG
""")

    # --- config/production.env ---
    Path(f'{PROJECT_DIR}/config/production.env').write_text("""\
APP_VERSION=production
DATABASE_URL=postgresql://app:${DB_PASSWORD}@db-prod.internal:5432/inventory
REDIS_URL=redis://cache-prod.internal:6379/0
LOG_LEVEL=WARNING
""")

    # --- README.md ---
    Path(f'{PROJECT_DIR}/README.md').write_text("""\
# Webapp Inventory Service

Warehouse inventory management microservice. Part of the logistics platform.

## Local Development

```bash
docker build -t webapp-inventory:dev .
docker run -p 8080:8080 webapp-inventory:dev
```

## Deployment

CI/CD pipeline is managed via GitLab CI. See `.gitlab-ci.yml` for the full pipeline.

## Infrastructure

- **Registry**: registry.internal:5000
- **Staging**: Docker Swarm stack `staging-inventory`
- **Production**: Docker Swarm stack `prod-inventory`
- **Security Scanning**: Trivy (installed on GitLab runner)
""")

    # --- .gitignore ---
    Path(f'{PROJECT_DIR}/.gitignore').write_text("""\
__pycache__/
*.pyc
.env
*.egg-info/
dist/
build/
.pytest_cache/
""")

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'Contents: {os.listdir(PROJECT_DIR)}')

    # GUI-ready: open file manager and terminal at project directory
    launch_gui(f'nautilus "{PROJECT_DIR}"', delay_sec=1.5)
    launch_gui('gnome-terminal', delay_sec=1.5)
    print('GUI_READY: launched nautilus and terminal with DISPLAY=:0')


create_initial()

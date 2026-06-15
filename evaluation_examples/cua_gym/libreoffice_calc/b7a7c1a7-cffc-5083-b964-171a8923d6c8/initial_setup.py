"""
Initial Setup: Automate morning data pipeline workspace
Task ID: osworld_multi_apps_workspace_init_010
Domain: multi_apps (OS + Chrome + VSCode + Terminal)

Initial state requirements:
- ~/Data/etl-pipelines exists with realistic ETL project files
- ~/Data/etl-pipelines/.venv exists (virtual environment directory)
- Desktop is idle: no apps open (no Nautilus, terminal, VSCode, Chrome)
"""

import os
from pathlib import Path

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_workspace_init_010'
PROJECT_DIR = f'{WORKDIR}/Data/etl-pipelines'
VENV_DIR = f'{PROJECT_DIR}/.venv'


def create_project_structure():
    """Create realistic ETL pipeline project structure."""
    # Create main project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create a realistic .venv directory structure
    os.makedirs(f'{VENV_DIR}/bin', exist_ok=True)
    os.makedirs(f'{VENV_DIR}/lib/python3.10/site-packages', exist_ok=True)
    os.makedirs(f'{VENV_DIR}/include', exist_ok=True)

    # Create pyvenv.cfg for the virtual environment
    Path(f'{VENV_DIR}/pyvenv.cfg').write_text(
        "home = /usr/bin\n"
        "include-system-site-packages = false\n"
        "version = 3.10.12\n"
        "executable = /usr/bin/python3.10\n"
        "command = /usr/bin/python3.10 -m venv .venv\n"
    )

    # Create an activate script in .venv/bin
    activate_script = f"""# This file must be used with "source bin/activate" *from bash*
# you cannot run it directly

deactivate () {{
    # reset old environment variables
    if [ -n "${{_OLD_VIRTUAL_PATH:-}}" ] ; then
        PATH="${{_OLD_VIRTUAL_PATH:-}}"
        export PATH
        unset _OLD_VIRTUAL_PATH
    fi
    if [ -n "${{_OLD_VIRTUAL_PYTHONHOME:-}}" ] ; then
        PYTHONHOME="${{_OLD_VIRTUAL_PYTHONHOME:-}}"
        export PYTHONHOME
        unset _OLD_VIRTUAL_PYTHONHOME
    fi

    # This should detect bash and zsh, which have a hash command that must
    # be called to get it to forget past commands.  Without forgetting
    # past commands the $PATH changes we made may not be respected
    if [ -n "${{BASH:-}}" -o -n "${{ZSH_VERSION:-}}" ] ; then
        hash -r 2> /dev/null
    fi

    if [ -n "${{_OLD_VIRTUAL_PS1:-}}" ] ; then
        PS1="${{_OLD_VIRTUAL_PS1:-}}"
        export PS1
        unset _OLD_VIRTUAL_PS1
    fi

    unset VIRTUAL_ENV
    unset VIRTUAL_ENV_PROMPT
    if [ ! "${{1:-}}" = "nondestructive" ] ; then
    # Self destruct!
        unset -f deactivate
    fi
}}

# unset irrelevant variables
deactivate nondestructive

VIRTUAL_ENV="{VENV_DIR}"
export VIRTUAL_ENV

_OLD_VIRTUAL_PATH="$PATH"
PATH="$VIRTUAL_ENV/bin:$PATH"
export PATH

# unset PYTHONHOME if set
# this will fail if PYTHONHOME is set to the empty string (which is bad)
# could use unset PYTHONHOME, but it becomes noisy then
if [ -n "${{PYTHONHOME:-}}" ] ; then
    _OLD_VIRTUAL_PYTHONHOME="${{PYTHONHOME:-}}"
    unset PYTHONHOME
fi

if [ -z "${{VIRTUAL_ENV_DISABLE_PROMPT:-}}" ] ; then
    _OLD_VIRTUAL_PS1="${{PS1:-}}"
    PS1="(.venv) ${{PS1:-}}"
    export PS1
    VIRTUAL_ENV_PROMPT="(.venv) "
    export VIRTUAL_ENV_PROMPT
fi

# This should detect bash and zsh, which have a hash command that must
# be called to get it to forget past commands.  Without forgetting
# past commands the $PATH changes we made may not be respected
if [ -n "${{BASH:-}}" -o -n "${{ZSH_VERSION:-}}" ] ; then
    hash -r 2> /dev/null
fi
"""
    Path(f'{VENV_DIR}/bin/activate').write_text(activate_script)
    os.chmod(f'{VENV_DIR}/bin/activate', 0o755)

    # Create a symlink-like python executable placeholder
    Path(f'{VENV_DIR}/bin/python').write_text('#!/bin/sh\nexec /usr/bin/python3 "$@"\n')
    os.chmod(f'{VENV_DIR}/bin/python', 0o755)
    Path(f'{VENV_DIR}/bin/python3').write_text('#!/bin/sh\nexec /usr/bin/python3 "$@"\n')
    os.chmod(f'{VENV_DIR}/bin/python3', 0o755)

    # Create realistic ETL project files
    # Main DAG file
    Path(f'{PROJECT_DIR}/dags').mkdir(exist_ok=True)
    Path(f'{PROJECT_DIR}/dags/__init__.py').write_text('')
    Path(f'{PROJECT_DIR}/dags/daily_etl.py').write_text(
        '"""\nDaily ETL Pipeline DAG\nExtracts data from PostgreSQL, transforms and loads to data warehouse.\n"""\n\n'
        'from datetime import datetime, timedelta\n'
        'from airflow import DAG\n'
        'from airflow.operators.python import PythonOperator\n'
        'from airflow.providers.postgres.hooks.postgres import PostgresHook\n\n'
        "default_args = {\n    'owner': 'data-team',\n    'depends_on_past': False,\n"
        "    'start_date': datetime(2025, 1, 1),\n    'email_on_failure': True,\n"
        "    'email': ['data-alerts@company.com'],\n    'retries': 2,\n"
        "    'retry_delay': timedelta(minutes=5),\n}\n\n"
        "with DAG(\n    'daily_etl_pipeline',\n    default_args=default_args,\n"
        "    description='Daily ETL: PostgreSQL -> Data Warehouse',\n"
        "    schedule_interval='0 6 * * *',\n    catchup=False,\n) as dag:\n\n"
        "    def extract_sales_data(**context):\n"
        "        hook = PostgresHook(postgres_conn_id='prod_postgres')\n"
        "        conn = hook.get_conn()\n"
        "        cursor = conn.cursor()\n"
        "        cursor.execute(\"\"\"\n"
        "            SELECT order_id, customer_id, product_sku, quantity, unit_price,\n"
        "                   order_date, region\n"
        "            FROM sales_transactions\n"
        "            WHERE order_date = CURRENT_DATE - INTERVAL '1 day'\n"
        "        \"\"\")\n"
        "        return cursor.fetchall()\n\n"
        "    extract = PythonOperator(\n"
        "        task_id='extract_sales',\n"
        "        python_callable=extract_sales_data,\n"
        "    )\n"
    )

    # Requirements file
    Path(f'{PROJECT_DIR}/requirements.txt').write_text(
        'apache-airflow==2.8.1\n'
        'apache-airflow-providers-postgres==5.7.1\n'
        'psycopg2-binary==2.9.9\n'
        'pandas==2.1.4\n'
        'sqlalchemy==1.4.51\n'
        'python-dotenv==1.0.0\n'
        'great-expectations==0.18.8\n'
        'pyarrow==14.0.2\n'
    )

    # Config file
    os.makedirs(f'{PROJECT_DIR}/config', exist_ok=True)
    Path(f'{PROJECT_DIR}/config/database.yaml').write_text(
        '# Database connection configuration\n'
        'production:\n'
        '  host: prod-db.internal.company.com\n'
        '  port: 5432\n'
        '  database: analytics_db\n'
        '  username: etl_user\n'
        '  # password loaded from environment variable PROD_DB_PASSWORD\n\n'
        'staging:\n'
        '  host: staging-db.internal.company.com\n'
        '  port: 5432\n'
        '  database: analytics_staging\n'
        '  username: etl_user_staging\n'
    )

    # Scripts directory
    os.makedirs(f'{PROJECT_DIR}/scripts', exist_ok=True)
    Path(f'{PROJECT_DIR}/scripts/run_pipeline.sh').write_text(
        '#!/bin/bash\n'
        '# Run ETL pipeline with virtual environment\n'
        'set -e\n\n'
        'SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"\n'
        'PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"\n\n'
        'echo "Activating virtual environment..."\n'
        'source "$PROJECT_ROOT/.venv/bin/activate"\n\n'
        'echo "Starting Airflow scheduler..."\n'
        'airflow scheduler &\n'
        'SCHEDULER_PID=$!\n\n'
        'echo "Running daily ETL trigger..."\n'
        'airflow dags trigger daily_etl_pipeline\n\n'
        'echo "Pipeline triggered successfully."\n'
    )
    os.chmod(f'{PROJECT_DIR}/scripts/run_pipeline.sh', 0o755)

    # Tests directory
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)
    Path(f'{PROJECT_DIR}/tests/__init__.py').write_text('')
    Path(f'{PROJECT_DIR}/tests/test_transforms.py').write_text(
        '"""Unit tests for ETL transformation functions."""\n\n'
        'import pytest\n'
        'import pandas as pd\n'
        'from datetime import date\n\n\n'
        'def test_sales_aggregation():\n'
        '    """Test that daily sales are correctly aggregated by region."""\n'
        '    sample_data = [\n'
        "        {'order_id': 1001, 'region': 'APAC', 'unit_price': 150.00, 'quantity': 3},\n"
        "        {'order_id': 1002, 'region': 'APAC', 'unit_price': 89.50, 'quantity': 1},\n"
        "        {'order_id': 1003, 'region': 'EMEA', 'unit_price': 320.00, 'quantity': 2},\n"
        '    ]\n'
        '    df = pd.DataFrame(sample_data)\n'
        "    result = df.groupby('region')['unit_price'].sum()\n"
        "    assert result['APAC'] == 239.50\n"
        "    assert result['EMEA'] == 320.00\n\n"
        'def test_null_handling():\n'
        '    """Test that null values in product_sku are handled gracefully."""\n'
        '    df = pd.DataFrame({\n'
        "        'order_id': [101, 102, 103],\n"
        "        'product_sku': ['SKU-A100', None, 'SKU-B200'],\n"
        '    })\n'
        "    cleaned = df.dropna(subset=['product_sku'])\n"
        '    assert len(cleaned) == 2\n'
    )

    # README
    Path(f'{PROJECT_DIR}/README.md').write_text(
        '# ETL Pipeline Project\n\n'
        '## Overview\n'
        'This project contains Apache Airflow DAGs for the daily data pipeline\n'
        'that extracts data from PostgreSQL production databases and loads into\n'
        'the analytics data warehouse.\n\n'
        '## Setup\n'
        '```bash\n'
        'python3 -m venv .venv\n'
        'source .venv/bin/activate\n'
        'pip install -r requirements.txt\n'
        '```\n\n'
        '## Project Structure\n'
        '```\n'
        'etl-pipelines/\n'
        '├── dags/           # Airflow DAG definitions\n'
        '├── config/         # Database and app configuration\n'
        '├── scripts/        # Utility scripts\n'
        '├── tests/          # Unit and integration tests\n'
        '├── requirements.txt\n'
        '└── .venv/          # Python virtual environment\n'
        '```\n\n'
        '## Running the Pipeline\n'
        'Ensure the virtual environment is activated and run:\n'
        '```bash\n'
        './scripts/run_pipeline.sh\n'
        '```\n'
    )

    # .env template
    Path(f'{PROJECT_DIR}/.env.example').write_text(
        '# Copy this file to .env and fill in the values\n'
        'PROD_DB_PASSWORD=your_secure_password_here\n'
        'AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql://airflow:airflow@localhost:5432/airflow\n'
        'AIRFLOW__CORE__FERNET_KEY=your_fernet_key_here\n'
        'AIRFLOW__WEBSERVER__SECRET_KEY=your_secret_key_here\n'
    )

    print(f'Project structure created at: {PROJECT_DIR}')


def create_initial():
    """Create initial state: project directory structure exists, desktop is idle."""
    create_project_structure()

    # Verify .venv exists
    assert os.path.isdir(VENV_DIR), f".venv not found at {VENV_DIR}"
    assert os.path.isdir(PROJECT_DIR), f"Project dir not found at {PROJECT_DIR}"

    print(f'Initial state ready: {PROJECT_DIR} exists with ETL project files')
    print(f'Virtual environment at: {VENV_DIR}')
    print('Desktop is idle — no apps open.')
    print('GUI_READY: Desktop is idle, project directory ready for agent interaction.')


create_initial()

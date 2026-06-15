"""
Initial Setup: Create SQL query optimization workflow environment
Task ID: vscode_gf3_058
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_058'
PROJECT_DIR = f'{WORKDIR}/projects/backend/queries'
OUTPUT = f'{PROJECT_DIR}/slow-query.sql'


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
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Also create some realistic sibling directories/files for context
    os.makedirs(f'{WORKDIR}/projects/backend/models', exist_ok=True)
    os.makedirs(f'{WORKDIR}/projects/backend/migrations', exist_ok=True)
    os.makedirs(f'{WORKDIR}/projects/backend/config', exist_ok=True)

    # Create a realistic database config file for context
    db_config = """{
    "host": "db-prod-replica.internal.acme.io",
    "port": 5432,
    "database": "acme_commerce",
    "user": "readonly_analyst",
    "ssl": true,
    "pool_size": 5
}
"""
    with open(f'{WORKDIR}/projects/backend/config/database.json', 'w') as f:
        f.write(db_config)

    # Create a realistic model file for context
    orders_model = """-- Table: public.orders
-- Description: Customer order records for the ACME Commerce platform
--
-- Columns:
--   id              SERIAL PRIMARY KEY
--   customer_id     INTEGER REFERENCES customers(id)
--   order_date      TIMESTAMP NOT NULL DEFAULT NOW()
--   total_amount    NUMERIC(12,2) NOT NULL
--   shipping_addr   TEXT
--   status          VARCHAR(20) DEFAULT 'pending'
--   created_at      TIMESTAMP DEFAULT NOW()
--   updated_at      TIMESTAMP DEFAULT NOW()
--
-- Related tables: customers, order_items, payments
--
-- Known issues:
--   - Slow queries when filtering by customer status on large result sets
--   - Missing composite indexes on frequently joined columns
"""
    with open(f'{WORKDIR}/projects/backend/models/orders.sql', 'w') as f:
        f.write(orders_model)

    # Create the customers model file
    customers_model = """-- Table: public.customers
-- Description: Customer account information
--
-- Columns:
--   id              SERIAL PRIMARY KEY
--   name            VARCHAR(255) NOT NULL
--   email           VARCHAR(255) UNIQUE NOT NULL
--   status          VARCHAR(20) DEFAULT 'active'
--   tier            VARCHAR(20) DEFAULT 'standard'
--   created_at      TIMESTAMP DEFAULT NOW()
--   updated_at      TIMESTAMP DEFAULT NOW()
--
-- Indexes:
--   idx_customers_email  UNIQUE (email)
--
-- Status values: 'active', 'inactive', 'suspended', 'pending_review'
"""
    with open(f'{WORKDIR}/projects/backend/models/customers.sql', 'w') as f:
        f.write(customers_model)

    # Create the target SQL file - EMPTY (the agent must write the queries)
    # Just a header comment so VSCode recognizes it as SQL
    initial_content = """-- Query Performance Investigation
-- Database: acme_commerce (PostgreSQL 15)
-- Author: Backend Team
-- Date: 2025-11-18
--
-- Issue: Orders endpoint is timing out for filtered customer queries.
-- The production monitoring dashboard shows p99 latency > 3s for
-- GET /api/v2/orders?customer_status=active
--
-- TODO: Use EXPLAIN ANALYZE to identify the bottleneck and add appropriate indexes.
--

"""
    with open(OUTPUT, 'w') as f:
        f.write(initial_content)

    print(f'Initial file created: {OUTPUT}')

    # Open VSCode with the file
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

"""
Initial Setup: Backend PostgreSQL project structure for order total calculation task
Task ID: vscode_gf3_082
Domain: vscode

Creates a realistic backend project structure with existing files but WITHOUT
the task-target files (the SQL procedure, pgTAP test, and VSCode task).
The agent must create those from scratch.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_082'
PROJECT_ROOT = f'{WORKDIR}/projects/backend'


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
    dirs = [
        f'{PROJECT_ROOT}/db/procedures',
        f'{PROJECT_ROOT}/db/tests',
        f'{PROJECT_ROOT}/db/migrations',
        f'{PROJECT_ROOT}/db/seeds',
        f'{PROJECT_ROOT}/src/models',
        f'{PROJECT_ROOT}/src/routes',
        f'{PROJECT_ROOT}/src/middleware',
        f'{PROJECT_ROOT}/config',
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # --- Existing project files to provide realistic context ---

    # README.md
    with open(f'{PROJECT_ROOT}/README.md', 'w') as f:
        f.write("""# E-Commerce Backend Service

A Node.js/Express backend for the ShopWave e-commerce platform.

## Architecture

- `src/` — Application source code (routes, models, middleware)
- `db/` — Database layer (migrations, procedures, seeds, tests)
- `config/` — Environment and service configuration

## Database

PostgreSQL 15 with pgTAP for unit testing stored procedures.

### Running Migrations

```bash
npm run db:migrate
```

### Running Tests

```bash
pg_prove -d shopwave_test db/tests/*.sql
```

## Development

```bash
npm install
npm run dev
```
""")

    # package.json
    with open(f'{PROJECT_ROOT}/package.json', 'w') as f:
        f.write("""{
  "name": "shopwave-backend",
  "version": "2.4.1",
  "description": "ShopWave e-commerce backend service",
  "main": "src/index.js",
  "scripts": {
    "dev": "nodemon src/index.js",
    "start": "node src/index.js",
    "test": "jest --coverage",
    "db:migrate": "node-pg-migrate up",
    "db:seed": "node db/seeds/run.js",
    "db:test": "pg_prove -d shopwave_test db/tests/*.sql"
  },
  "dependencies": {
    "express": "^4.18.2",
    "pg": "^8.11.3",
    "dotenv": "^16.3.1",
    "cors": "^2.8.5",
    "helmet": "^7.1.0"
  },
  "devDependencies": {
    "jest": "^29.7.0",
    "nodemon": "^3.0.2",
    "node-pg-migrate": "^6.2.2"
  }
}
""")

    # config/database.js
    with open(f'{PROJECT_ROOT}/config/database.js', 'w') as f:
        f.write("""const { Pool } = require('pg');
require('dotenv').config();

const pool = new Pool({
  host: process.env.DB_HOST || 'localhost',
  port: parseInt(process.env.DB_PORT) || 5432,
  database: process.env.DB_NAME || 'shopwave',
  user: process.env.DB_USER || 'shopwave_app',
  password: process.env.DB_PASSWORD,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

module.exports = { pool };
""")

    # An existing stored procedure (different from the task target)
    with open(f'{PROJECT_ROOT}/db/procedures/get_customer_lifetime_value.sql', 'w') as f:
        f.write("""-- Calculate the lifetime value of a customer
-- Returns total revenue from all completed orders

CREATE OR REPLACE FUNCTION get_customer_lifetime_value(p_customer_id INTEGER)
RETURNS NUMERIC(12,2)
LANGUAGE plpgsql
AS $$
DECLARE
    total_value NUMERIC(12,2);
BEGIN
    SELECT COALESCE(SUM(total_amount), 0.00)
    INTO total_value
    FROM orders
    WHERE customer_id = p_customer_id
      AND status = 'completed';

    RETURN total_value;
END;
$$;
""")

    # An existing test file (different from the task target)
    with open(f'{PROJECT_ROOT}/db/tests/test_customer_lifetime_value.sql', 'w') as f:
        f.write("""-- pgTAP tests for get_customer_lifetime_value function

BEGIN;
SELECT plan(3);

-- Setup test data
INSERT INTO customers (id, name, email)
VALUES (9001, 'Test Customer', 'test@example.com');

INSERT INTO orders (id, customer_id, total_amount, status)
VALUES
    (8001, 9001, 150.00, 'completed'),
    (8002, 9001, 275.50, 'completed'),
    (8003, 9001, 89.99, 'cancelled');

-- Test 1: Returns correct lifetime value (only completed orders)
SELECT is(
    get_customer_lifetime_value(9001),
    425.50::NUMERIC(12,2),
    'Lifetime value should sum only completed orders'
);

-- Test 2: Returns 0 for customer with no orders
SELECT is(
    get_customer_lifetime_value(99999),
    0.00::NUMERIC(12,2),
    'Should return 0.00 for customer with no orders'
);

-- Test 3: Function exists
SELECT has_function('get_customer_lifetime_value', ARRAY['integer']);

-- Cleanup
DELETE FROM orders WHERE customer_id = 9001;
DELETE FROM customers WHERE id = 9001;

SELECT * FROM finish();
ROLLBACK;
""")

    # Migration file
    with open(f'{PROJECT_ROOT}/db/migrations/001_create_tables.sql', 'w') as f:
        f.write("""-- Initial schema creation for ShopWave

CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS promotions (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    discount_percent NUMERIC(5,2) NOT NULL CHECK (discount_percent BETWEEN 0 AND 100),
    min_order_amount NUMERIC(10,2) DEFAULT 0.00,
    valid_from DATE NOT NULL,
    valid_until DATE NOT NULL,
    active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    promotion_id INTEGER REFERENCES promotions(id),
    subtotal NUMERIC(10,2),
    tax_amount NUMERIC(10,2),
    discount_amount NUMERIC(10,2) DEFAULT 0.00,
    total_amount NUMERIC(10,2),
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS order_line_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
    product_name VARCHAR(200) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10,2) NOT NULL,
    line_total NUMERIC(10,2) NOT NULL
);

CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_line_items_order ON order_line_items(order_id);
""")

    # Seed file
    with open(f'{PROJECT_ROOT}/db/seeds/sample_data.sql', 'w') as f:
        f.write("""-- Sample data for development

INSERT INTO customers (id, name, email) VALUES
    (1, 'Alice Nakamura', 'alice.nakamura@email.com'),
    (2, 'Ben Torres', 'ben.torres@email.com'),
    (3, 'Clara Johansson', 'clara.j@email.com'),
    (4, 'David Kim', 'dkim@email.com'),
    (5, 'Elena Popov', 'elena.popov@email.com');

INSERT INTO promotions (id, code, discount_percent, min_order_amount, valid_from, valid_until) VALUES
    (1, 'SUMMER2025', 15.00, 50.00, '2025-06-01', '2025-08-31'),
    (2, 'WELCOME10', 10.00, 0.00, '2025-01-01', '2025-12-31'),
    (3, 'BIGSPEND20', 20.00, 200.00, '2025-03-01', '2025-12-31');
""")

    # Express route file
    with open(f'{PROJECT_ROOT}/src/routes/orders.js', 'w') as f:
        f.write("""const express = require('express');
const router = express.Router();
const { pool } = require('../../config/database');

// GET /api/orders/:id/total — Calculate order total using stored procedure
router.get('/:id/total', async (req, res) => {
    try {
        const orderId = parseInt(req.params.id);
        const result = await pool.query(
            'SELECT calculate_order_total($1) AS total',
            [orderId]
        );
        if (result.rows.length === 0) {
            return res.status(404).json({ error: 'Order not found' });
        }
        res.json({ order_id: orderId, total: result.rows[0].total });
    } catch (err) {
        console.error('Error calculating order total:', err);
        res.status(500).json({ error: 'Internal server error' });
    }
});

module.exports = router;
""")

    # Model file
    with open(f'{PROJECT_ROOT}/src/models/order.js', 'w') as f:
        f.write("""const { pool } = require('../../config/database');

class Order {
    static async findById(id) {
        const result = await pool.query(
            'SELECT * FROM orders WHERE id = $1',
            [id]
        );
        return result.rows[0] || null;
    }

    static async getLineItems(orderId) {
        const result = await pool.query(
            'SELECT * FROM order_line_items WHERE order_id = $1 ORDER BY id',
            [orderId]
        );
        return result.rows;
    }

    static async calculateTotal(orderId) {
        const result = await pool.query(
            'SELECT calculate_order_total($1) AS total',
            [orderId]
        );
        return result.rows[0]?.total || null;
    }
}

module.exports = Order;
""")

    # .env.example
    with open(f'{PROJECT_ROOT}/.env.example', 'w') as f:
        f.write("""DB_HOST=localhost
DB_PORT=5432
DB_NAME=shopwave
DB_USER=shopwave_app
DB_PASSWORD=your_password_here
PORT=3000
NODE_ENV=development
""")

    print(f'Initial project structure created at: {PROJECT_ROOT}')
    print(f'  db/procedures/ — has existing procedure (get_customer_lifetime_value.sql)')
    print(f'  db/tests/ — has existing test (test_customer_lifetime_value.sql)')
    print(f'  db/procedures/calculate_order_total.sql — DOES NOT EXIST (task target)')
    print(f'  db/tests/test_order_total.sql — DOES NOT EXIST (task target)')
    print(f'  .vscode/tasks.json — DOES NOT EXIST (task target)')

    # GUI-ready: open VSCode on the project
    launch_gui(f'code "{PROJECT_ROOT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

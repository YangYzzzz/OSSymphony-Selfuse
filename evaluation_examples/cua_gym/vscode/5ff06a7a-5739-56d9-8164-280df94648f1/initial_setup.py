"""
Initial Setup: VSCode diff editor with schema.sql in side-by-side mode
Task ID: vscode_rf_028
Domain: vscode
"""

import os
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_rf_028'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'database')


def launch_gui(command, delay_sec=1.0):
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def run(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return result.stdout.strip()


SCHEMA_CURRENT = """-- Database Schema: E-Commerce Platform
-- Version: 3.2.1
-- Last updated: 2025-08-10

CREATE TABLE users (
    user_id         SERIAL PRIMARY KEY,
    username        VARCHAR(50) NOT NULL UNIQUE,
    email           VARCHAR(100) NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login      TIMESTAMP,
    is_active       BOOLEAN DEFAULT TRUE
);

CREATE TABLE products (
    product_id      SERIAL PRIMARY KEY,
    name            VARCHAR(200) NOT NULL,
    description     TEXT,
    price           DECIMAL(10,2) NOT NULL,
    stock_quantity  INTEGER DEFAULT 0,
    category_id     INTEGER,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE categories (
    category_id     SERIAL PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    parent_id       INTEGER REFERENCES categories(category_id)
);

CREATE TABLE orders (
    order_id        SERIAL PRIMARY KEY,
    user_id         INTEGER NOT NULL REFERENCES users(user_id),
    order_date      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status          VARCHAR(20) DEFAULT 'pending',
    total_amount    DECIMAL(12,2),
    shipping_addr   TEXT
);

CREATE TABLE order_items (
    item_id         SERIAL PRIMARY KEY,
    order_id        INTEGER NOT NULL REFERENCES orders(order_id),
    product_id      INTEGER NOT NULL REFERENCES products(product_id),
    quantity        INTEGER NOT NULL,
    unit_price      DECIMAL(10,2) NOT NULL
);

CREATE TABLE payments (
    payment_id      SERIAL PRIMARY KEY,
    order_id        INTEGER NOT NULL REFERENCES orders(order_id),
    amount          DECIMAL(12,2) NOT NULL,
    payment_method  VARCHAR(30),
    payment_date    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status          VARCHAR(20) DEFAULT 'pending'
);

CREATE TABLE shipping (
    shipping_id     SERIAL PRIMARY KEY,
    order_id        INTEGER NOT NULL REFERENCES orders(order_id),
    carrier         VARCHAR(50),
    tracking_number VARCHAR(100),
    shipped_date    TIMESTAMP,
    delivered_date  TIMESTAMP
);

CREATE TABLE legacy_user_profiles (
    profile_id      SERIAL PRIMARY KEY,
    user_id         INTEGER REFERENCES users(user_id),
    bio             TEXT,
    avatar_url      VARCHAR(500),
    phone           VARCHAR(20)
);

CREATE TABLE deprecated_product_tags (
    tag_id          SERIAL PRIMARY KEY,
    product_id      INTEGER REFERENCES products(product_id),
    tag_name        VARCHAR(50)
);

CREATE TABLE old_review_system (
    review_id       SERIAL PRIMARY KEY,
    product_id      INTEGER REFERENCES products(product_id),
    user_id         INTEGER REFERENCES users(user_id),
    rating          INTEGER CHECK (rating BETWEEN 1 AND 5),
    comment         TEXT,
    review_date     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_payments_order ON payments(order_id);

CREATE VIEW active_users AS
SELECT user_id, username, email, last_login
FROM users
WHERE is_active = TRUE;

CREATE VIEW order_summary AS
SELECT o.order_id, u.username, o.order_date, o.status, o.total_amount
FROM orders o
JOIN users u ON o.user_id = u.user_id;
"""

SCHEMA_INCOMING = """-- Database Schema: E-Commerce Platform
-- Version: 4.0.0
-- Last updated: 2025-11-22

CREATE TABLE users (
    user_id         SERIAL PRIMARY KEY,
    username        VARCHAR(80) NOT NULL UNIQUE,
    email           VARCHAR(150) NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,
    display_name    VARCHAR(120),
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login      TIMESTAMP WITH TIME ZONE,
    is_active       BOOLEAN DEFAULT TRUE,
    role            VARCHAR(30) DEFAULT 'customer'
);

CREATE TABLE products (
    product_id      SERIAL PRIMARY KEY,
    sku             VARCHAR(50) NOT NULL UNIQUE,
    name            VARCHAR(200) NOT NULL,
    description     TEXT,
    price           DECIMAL(12,2) NOT NULL,
    cost_price      DECIMAL(12,2),
    stock_quantity  INTEGER DEFAULT 0,
    category_id     INTEGER,
    brand_id        INTEGER,
    weight_kg       DECIMAL(8,3),
    is_available    BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE categories (
    category_id     SERIAL PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    slug            VARCHAR(100) NOT NULL UNIQUE,
    description     TEXT,
    parent_id       INTEGER REFERENCES categories(category_id),
    sort_order      INTEGER DEFAULT 0
);

CREATE TABLE orders (
    order_id        SERIAL PRIMARY KEY,
    user_id         INTEGER NOT NULL REFERENCES users(user_id),
    order_date      TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status          VARCHAR(20) DEFAULT 'pending',
    total_amount    DECIMAL(12,2),
    discount_amount DECIMAL(12,2) DEFAULT 0,
    tax_amount      DECIMAL(12,2) DEFAULT 0,
    shipping_addr   JSONB,
    billing_addr    JSONB,
    notes           TEXT
);

CREATE TABLE order_items (
    item_id         SERIAL PRIMARY KEY,
    order_id        INTEGER NOT NULL REFERENCES orders(order_id),
    product_id      INTEGER NOT NULL REFERENCES products(product_id),
    quantity        INTEGER NOT NULL,
    unit_price      DECIMAL(12,2) NOT NULL,
    discount        DECIMAL(12,2) DEFAULT 0
);

CREATE TABLE payments (
    payment_id      SERIAL PRIMARY KEY,
    order_id        INTEGER NOT NULL REFERENCES orders(order_id),
    amount          DECIMAL(12,2) NOT NULL,
    payment_method  VARCHAR(30),
    payment_date    TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status          VARCHAR(20) DEFAULT 'pending',
    transaction_ref VARCHAR(100),
    gateway         VARCHAR(50)
);

CREATE TABLE shipping (
    shipping_id     SERIAL PRIMARY KEY,
    order_id        INTEGER NOT NULL REFERENCES orders(order_id),
    carrier         VARCHAR(50),
    tracking_number VARCHAR(100),
    shipped_date    TIMESTAMP WITH TIME ZONE,
    estimated_delivery TIMESTAMP WITH TIME ZONE,
    delivered_date  TIMESTAMP WITH TIME ZONE,
    shipping_method VARCHAR(30) DEFAULT 'standard'
);

CREATE TABLE brands (
    brand_id        SERIAL PRIMARY KEY,
    name            VARCHAR(100) NOT NULL UNIQUE,
    logo_url        VARCHAR(500),
    website         VARCHAR(300),
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE product_reviews (
    review_id       SERIAL PRIMARY KEY,
    product_id      INTEGER NOT NULL REFERENCES products(product_id),
    user_id         INTEGER NOT NULL REFERENCES users(user_id),
    rating          SMALLINT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    title           VARCHAR(200),
    body            TEXT,
    is_verified     BOOLEAN DEFAULT FALSE,
    helpful_count   INTEGER DEFAULT 0,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE wishlists (
    wishlist_id     SERIAL PRIMARY KEY,
    user_id         INTEGER NOT NULL REFERENCES users(user_id),
    product_id      INTEGER NOT NULL REFERENCES products(product_id),
    added_at        TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, product_id)
);

CREATE TABLE discount_codes (
    code_id         SERIAL PRIMARY KEY,
    code            VARCHAR(30) NOT NULL UNIQUE,
    discount_type   VARCHAR(10) NOT NULL CHECK (discount_type IN ('percent', 'fixed')),
    discount_value  DECIMAL(10,2) NOT NULL,
    min_order       DECIMAL(10,2) DEFAULT 0,
    max_uses        INTEGER,
    used_count      INTEGER DEFAULT 0,
    valid_from      TIMESTAMP WITH TIME ZONE NOT NULL,
    valid_until     TIMESTAMP WITH TIME ZONE NOT NULL,
    is_active       BOOLEAN DEFAULT TRUE
);

CREATE TABLE inventory_log (
    log_id          SERIAL PRIMARY KEY,
    product_id      INTEGER NOT NULL REFERENCES products(product_id),
    change_qty      INTEGER NOT NULL,
    reason          VARCHAR(50) NOT NULL,
    reference_id    INTEGER,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by      INTEGER REFERENCES users(user_id)
);

CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_brand ON products(brand_id);
CREATE INDEX idx_products_sku ON products(sku);
CREATE INDEX idx_products_available ON products(is_available) WHERE is_available = TRUE;
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_date ON orders(order_date DESC);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);
CREATE INDEX idx_payments_order ON payments(order_id);
CREATE INDEX idx_payments_status ON payments(status);
CREATE INDEX idx_reviews_product ON product_reviews(product_id);
CREATE INDEX idx_reviews_user ON product_reviews(user_id);
CREATE INDEX idx_wishlists_user ON wishlists(user_id);
CREATE INDEX idx_inventory_product ON inventory_log(product_id);
CREATE INDEX idx_discount_codes_active ON discount_codes(is_active) WHERE is_active = TRUE;

CREATE VIEW active_users AS
SELECT user_id, username, display_name, email, last_login, role
FROM users
WHERE is_active = TRUE;

CREATE VIEW order_summary AS
SELECT o.order_id, u.username, o.order_date, o.status,
       o.total_amount, o.discount_amount, o.tax_amount
FROM orders o
JOIN users u ON o.user_id = u.user_id;

CREATE VIEW product_catalog AS
SELECT p.product_id, p.sku, p.name, p.price, p.is_available,
       c.name AS category_name, b.name AS brand_name,
       COALESCE(AVG(r.rating), 0) AS avg_rating,
       COUNT(r.review_id) AS review_count
FROM products p
LEFT JOIN categories c ON p.category_id = c.category_id
LEFT JOIN brands b ON p.brand_id = b.brand_id
LEFT JOIN product_reviews r ON p.product_id = r.product_id
GROUP BY p.product_id, p.sku, p.name, p.price, p.is_available,
         c.name, b.name;
"""


def create_initial():
    os.makedirs(PROJECT_DIR, exist_ok=True)

    schema_path = os.path.join(PROJECT_DIR, 'schema.sql')
    incoming_path = os.path.join(PROJECT_DIR, '.incoming_schema.sql')

    # Write both versions
    with open(schema_path, 'w') as f:
        f.write(SCHEMA_CURRENT)
    with open(incoming_path, 'w') as f:
        f.write(SCHEMA_INCOMING)

    # Init git repo with the current version
    run('git init', cwd=PROJECT_DIR)
    run('git config user.email "dev@company.com"', cwd=PROJECT_DIR)
    run('git config user.name "Developer"', cwd=PROJECT_DIR)
    run('git add schema.sql', cwd=PROJECT_DIR)
    run('git commit -m "v3.2.1 current schema"', cwd=PROJECT_DIR)

    # Create branch with incoming changes
    run('git checkout -b db-migration-v4', cwd=PROJECT_DIR)
    with open(schema_path, 'w') as f:
        f.write(SCHEMA_INCOMING)
    run('git add schema.sql', cwd=PROJECT_DIR)
    run('git commit -m "v4.0.0 database migration"', cwd=PROJECT_DIR)

    # Back to main branch
    run('git checkout master || git checkout main', cwd=PROJECT_DIR)

    print('Project created at: ' + PROJECT_DIR)

    # Launch VSCode with the folder, then open diff
    launch_gui('code "' + PROJECT_DIR + '"', delay_sec=3.0)
    launch_gui('code --diff "' + schema_path + '" "' + incoming_path + '"', delay_sec=2.0)

    print('GUI_READY: VSCode launched with diff editor')


create_initial()

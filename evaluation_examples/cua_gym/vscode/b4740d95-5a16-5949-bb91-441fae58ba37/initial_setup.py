"""
Initial Setup: Accidental commit on wrong branch (git cherry-pick recovery)
Task ID: vscode_git_072
Domain: vs_code
Description:
  Creates a git repository at /home/user/project with a realistic Python
  project. The 'main' branch has an accidental commit 'Add payment validation'
  (changes to payment.py) that should have been on 'feature/payments'.
  The 'feature/payments' branch does NOT yet exist.
  Agent task: move that commit to feature/payments and reset main.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT_DIR = f'{WORKDIR}/project'
TASK_ID = 'vscode_git_072'

def run(cmd, cwd=None, check=True, env=None):
    """Run a shell command, optionally in a given directory."""
    result = subprocess.run(
        shlex.split(cmd),
        cwd=cwd,
        capture_output=True,
        text=True,
        env=env,
        check=check,
    )
    return result

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
    # ── 1. Clean up any prior run ──────────────────────────────────────────
    if os.path.exists(PROJECT_DIR):
        subprocess.run(['rm', '-rf', PROJECT_DIR], check=True)

    os.makedirs(PROJECT_DIR, exist_ok=True)

    # ── 2. Configure git identity (needed for commits) ─────────────────────
    git_env = os.environ.copy()
    git_env['GIT_AUTHOR_NAME'] = 'Dev User'
    git_env['GIT_AUTHOR_EMAIL'] = 'dev@example.com'
    git_env['GIT_COMMITTER_NAME'] = 'Dev User'
    git_env['GIT_COMMITTER_EMAIL'] = 'dev@example.com'

    # ── 3. Initialise repo ─────────────────────────────────────────────────
    run('git init -b main', cwd=PROJECT_DIR, env=git_env)
    run('git config user.name "Dev User"', cwd=PROJECT_DIR, env=git_env)
    run('git config user.email "dev@example.com"', cwd=PROJECT_DIR, env=git_env)

    # ── 4. Create initial project files ───────────────────────────────────
    # README
    readme_content = """# E-Commerce Backend

A Python-based e-commerce backend service.

## Modules

- **app.py** – Flask application entry point
- **orders.py** – Order processing logic
- **products.py** – Product catalogue management
- **users.py** – User account management
- **payment.py** – Payment gateway integration
- **utils.py** – Shared utilities
"""
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write(readme_content)

    # app.py
    app_content = """from flask import Flask, jsonify
from orders import OrderService
from products import ProductService
from users import UserService
from payment import PaymentGateway

app = Flask(__name__)
order_service = OrderService()
product_service = ProductService()
user_service = UserService()
payment_gw = PaymentGateway()


@app.route('/health')
def health():
    return jsonify({'status': 'ok'})


@app.route('/orders', methods=['GET'])
def list_orders():
    return jsonify(order_service.all())


@app.route('/products', methods=['GET'])
def list_products():
    return jsonify(product_service.all())


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
"""
    with open(os.path.join(PROJECT_DIR, 'app.py'), 'w') as f:
        f.write(app_content)

    # orders.py
    orders_content = """from datetime import datetime


class OrderService:
    def __init__(self):
        self._orders = [
            {'id': 'ORD-001', 'customer': 'Alice Nguyen', 'total': 129.99, 'status': 'shipped',
             'created_at': '2025-02-10T09:15:00'},
            {'id': 'ORD-002', 'customer': 'Bob Hartmann', 'total': 49.50, 'status': 'pending',
             'created_at': '2025-02-12T14:30:00'},
            {'id': 'ORD-003', 'customer': 'Clara Osei', 'total': 210.00, 'status': 'delivered',
             'created_at': '2025-02-15T11:00:00'},
        ]

    def all(self):
        return self._orders

    def get(self, order_id):
        return next((o for o in self._orders if o['id'] == order_id), None)

    def create(self, customer, total):
        new_order = {
            'id': f'ORD-{len(self._orders) + 1:03d}',
            'customer': customer,
            'total': total,
            'status': 'pending',
            'created_at': datetime.utcnow().isoformat(),
        }
        self._orders.append(new_order)
        return new_order
"""
    with open(os.path.join(PROJECT_DIR, 'orders.py'), 'w') as f:
        f.write(orders_content)

    # products.py
    products_content = """class ProductService:
    def __init__(self):
        self._products = [
            {'id': 'PRD-101', 'name': 'Wireless Headphones', 'price': 79.99,
             'category': 'Electronics', 'stock': 42},
            {'id': 'PRD-102', 'name': 'Ergonomic Desk Chair', 'price': 349.00,
             'category': 'Furniture', 'stock': 8},
            {'id': 'PRD-103', 'name': 'Stainless Water Bottle', 'price': 24.50,
             'category': 'Lifestyle', 'stock': 120},
            {'id': 'PRD-104', 'name': 'USB-C Hub 7-in-1', 'price': 45.00,
             'category': 'Electronics', 'stock': 55},
        ]

    def all(self):
        return self._products

    def get(self, product_id):
        return next((p for p in self._products if p['id'] == product_id), None)
"""
    with open(os.path.join(PROJECT_DIR, 'products.py'), 'w') as f:
        f.write(products_content)

    # users.py
    users_content = """import hashlib


class UserService:
    def __init__(self):
        self._users = [
            {'id': 1, 'username': 'alice_n', 'email': 'alice@example.com', 'role': 'customer'},
            {'id': 2, 'username': 'bob_h', 'email': 'bob@example.com', 'role': 'customer'},
            {'id': 3, 'username': 'admin_clara', 'email': 'clara@example.com', 'role': 'admin'},
        ]

    def get_by_username(self, username):
        return next((u for u in self._users if u['username'] == username), None)

    def authenticate(self, username, password_hash):
        user = self.get_by_username(username)
        if user is None:
            return False
        expected = hashlib.sha256(f'{username}:secret'.encode()).hexdigest()
        return password_hash == expected
"""
    with open(os.path.join(PROJECT_DIR, 'users.py'), 'w') as f:
        f.write(users_content)

    # payment.py — INITIAL state (basic, no validation logic yet)
    payment_initial_content = """import logging

logger = logging.getLogger(__name__)


class PaymentGateway:
    \"\"\"Handles payment processing for orders.\"\"\"

    SUPPORTED_METHODS = ['credit_card', 'paypal', 'bank_transfer']

    def __init__(self):
        self.transactions = []

    def charge(self, order_id, amount, method):
        \"\"\"Process a payment for an order.\"\"\"
        txn = {
            'order_id': order_id,
            'amount': amount,
            'method': method,
            'status': 'success',
        }
        self.transactions.append(txn)
        logger.info('Charged %s for order %s via %s', amount, order_id, method)
        return txn

    def refund(self, order_id):
        \"\"\"Issue a refund for a previously charged order.\"\"\"
        txn = next((t for t in self.transactions if t['order_id'] == order_id), None)
        if txn is None:
            raise ValueError(f'No transaction found for order {order_id}')
        txn['status'] = 'refunded'
        logger.info('Refunded order %s', order_id)
        return txn
"""
    with open(os.path.join(PROJECT_DIR, 'payment.py'), 'w') as f:
        f.write(payment_initial_content)

    # utils.py
    utils_content = """import re
from datetime import datetime


def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))


def format_currency(amount: float, symbol: str = '$') -> str:
    return f'{symbol}{amount:,.2f}'


def utcnow_iso() -> str:
    return datetime.utcnow().isoformat()


def paginate(items: list, page: int, page_size: int = 20) -> dict:
    start = (page - 1) * page_size
    end = start + page_size
    return {
        'items': items[start:end],
        'page': page,
        'page_size': page_size,
        'total': len(items),
    }
"""
    with open(os.path.join(PROJECT_DIR, 'utils.py'), 'w') as f:
        f.write(utils_content)

    # requirements.txt
    req_content = """Flask==3.0.2
gunicorn==21.2.0
requests==2.31.0
"""
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write(req_content)

    # .gitignore
    gitignore_content = """__pycache__/
*.pyc
.env
venv/
.vscode/
*.log
"""
    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write(gitignore_content)

    # ── 5. Initial commit on main ──────────────────────────────────────────
    run('git add .', cwd=PROJECT_DIR, env=git_env)
    run('git commit -m "Initial project structure"', cwd=PROJECT_DIR, env=git_env)

    # ── 6. Make the ACCIDENTAL commit on main ─────────────────────────────
    # Update payment.py with validation logic — this is the commit that should
    # have gone to feature/payments, not main.
    payment_with_validation = """import logging
import re

logger = logging.getLogger(__name__)

# Regex pattern for basic card number validation (Luhn not enforced here)
CARD_NUMBER_PATTERN = re.compile(r'^\\d{13,19}$')
CVV_PATTERN = re.compile(r'^\\d{3,4}$')
EXPIRY_PATTERN = re.compile(r'^(0[1-9]|1[0-2])/([0-9]{2})$')


class PaymentValidationError(Exception):
    \"\"\"Raised when payment input fails validation.\"\"\"


class PaymentGateway:
    \"\"\"Handles payment processing for orders.\"\"\"

    SUPPORTED_METHODS = ['credit_card', 'paypal', 'bank_transfer']

    def __init__(self):
        self.transactions = []

    def validate_card(self, card_number: str, cvv: str, expiry: str):
        \"\"\"Validate credit card details before charging.\"\"\"
        if not CARD_NUMBER_PATTERN.match(card_number.replace(' ', '')):
            raise PaymentValidationError(
                f'Invalid card number format: must be 13-19 digits.'
            )
        if not CVV_PATTERN.match(cvv):
            raise PaymentValidationError('Invalid CVV: must be 3 or 4 digits.')
        if not EXPIRY_PATTERN.match(expiry):
            raise PaymentValidationError(
                'Invalid expiry date: expected MM/YY format.'
            )

    def charge(self, order_id, amount, method, card_number=None, cvv=None, expiry=None):
        \"\"\"Process a payment for an order.\"\"\"
        if amount <= 0:
            raise PaymentValidationError(f'Charge amount must be positive, got {amount}.')
        if method not in self.SUPPORTED_METHODS:
            raise PaymentValidationError(
                f'Unsupported payment method: {method}. '
                f'Supported: {self.SUPPORTED_METHODS}'
            )
        if method == 'credit_card':
            if not all([card_number, cvv, expiry]):
                raise PaymentValidationError(
                    'credit_card method requires card_number, cvv, and expiry.'
                )
            self.validate_card(card_number, cvv, expiry)

        txn = {
            'order_id': order_id,
            'amount': amount,
            'method': method,
            'status': 'success',
        }
        self.transactions.append(txn)
        logger.info('Charged %s for order %s via %s', amount, order_id, method)
        return txn

    def refund(self, order_id):
        \"\"\"Issue a refund for a previously charged order.\"\"\"
        txn = next((t for t in self.transactions if t['order_id'] == order_id), None)
        if txn is None:
            raise ValueError(f'No transaction found for order {order_id}')
        txn['status'] = 'refunded'
        logger.info('Refunded order %s', order_id)
        return txn
"""
    with open(os.path.join(PROJECT_DIR, 'payment.py'), 'w') as f:
        f.write(payment_with_validation)

    run('git add payment.py', cwd=PROJECT_DIR, env=git_env)
    run('git commit -m "Add payment validation"', cwd=PROJECT_DIR, env=git_env)

    # ── 7. Verify the state ────────────────────────────────────────────────
    result = run('git log --oneline', cwd=PROJECT_DIR, env=git_env)
    print('Git log after setup:')
    print(result.stdout)

    result = run('git branch -a', cwd=PROJECT_DIR, env=git_env)
    print('Branches:')
    print(result.stdout)

    print(f'Initial repo created: {PROJECT_DIR}')
    print('State: main has "Add payment validation" commit; feature/payments does NOT exist')

    # ── 8. GUI-ready startup ───────────────────────────────────────────────
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with project folder on DISPLAY=:0')


create_initial()

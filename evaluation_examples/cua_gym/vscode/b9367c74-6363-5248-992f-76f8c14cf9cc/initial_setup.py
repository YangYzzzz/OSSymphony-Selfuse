"""
Initial Setup: Set up terminal auto-activation for a Python virtual environment
Task ID: vscode_rrt_076
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_076'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'myapp')
VENV_DIR = os.path.join(PROJECT_DIR, '.venv')
VSCODE_DIR = os.path.join(PROJECT_DIR, '.vscode')


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
    # 1. Create project directory structure
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # 2. Create a realistic Python project
    # Main application file
    main_py = os.path.join(PROJECT_DIR, 'main.py')
    with open(main_py, 'w') as f:
        f.write('''\
"""MyApp - Inventory Management System"""

from flask import Flask, jsonify, request
from models import db, Product, Category

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
db.init_app(app)


@app.route('/api/products', methods=['GET'])
def get_products():
    """Return all products with optional category filter."""
    category = request.args.get('category')
    if category:
        products = Product.query.filter_by(category_name=category).all()
    else:
        products = Product.query.all()
    return jsonify([p.to_dict() for p in products])


@app.route('/api/products', methods=['POST'])
def add_product():
    """Add a new product to inventory."""
    data = request.get_json()
    product = Product(
        name=data['name'],
        sku=data['sku'],
        price=data['price'],
        quantity=data.get('quantity', 0),
        category_name=data.get('category', 'Uncategorized'),
    )
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201


@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Return all product categories."""
    categories = Category.query.all()
    return jsonify([c.to_dict() for c in categories])


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
''')

    # Models file
    models_py = os.path.join(PROJECT_DIR, 'models.py')
    with open(models_py, 'w') as f:
        f.write('''\
"""Database models for inventory management."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    products = db.relationship('Product', backref='category', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'product_count': len(self.products),
        }


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=0)
    category_name = db.Column(db.String(100), db.ForeignKey('categories.name'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'sku': self.sku,
            'price': self.price,
            'quantity': self.quantity,
            'category': self.category_name,
            'created_at': self.created_at.isoformat(),
        }
''')

    # Requirements file
    requirements_txt = os.path.join(PROJECT_DIR, 'requirements.txt')
    with open(requirements_txt, 'w') as f:
        f.write('''\
flask==3.0.2
flask-sqlalchemy==3.1.1
gunicorn==21.2.0
python-dotenv==1.0.1
pytest==8.0.2
''')

    # README
    readme = os.path.join(PROJECT_DIR, 'README.md')
    with open(readme, 'w') as f:
        f.write('''\
# MyApp - Inventory Management System

A Flask-based REST API for managing product inventory.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running

```bash
python main.py
```

## API Endpoints

- GET /api/products - List all products
- POST /api/products - Add a new product
- GET /api/categories - List all categories
''')

    # 3. Create virtual environment directory structure manually
    # (python3-venv package may not be installed on the VM)
    os.makedirs(os.path.join(VENV_DIR, 'bin'), exist_ok=True)
    os.makedirs(os.path.join(VENV_DIR, 'lib', 'python3.10', 'site-packages'), exist_ok=True)
    os.makedirs(os.path.join(VENV_DIR, 'include'), exist_ok=True)

    # Create python symlink
    python_bin = os.path.join(VENV_DIR, 'bin', 'python')
    python3_bin = os.path.join(VENV_DIR, 'bin', 'python3')
    if not os.path.exists(python_bin):
        os.symlink('/usr/bin/python3', python_bin)
    if not os.path.exists(python3_bin):
        os.symlink('/usr/bin/python3', python3_bin)

    # Create activate script
    activate_path = os.path.join(VENV_DIR, 'bin', 'activate')
    with open(activate_path, 'w') as f:
        f.write(f'''\
# This file must be used with "source bin/activate" *from bash*
# you cannot run it directly

deactivate () {{
    if [ -n "${{_OLD_VIRTUAL_PATH:-}}" ] ; then
        PATH="${{_OLD_VIRTUAL_PATH:-}}"
        export PATH
        unset _OLD_VIRTUAL_PATH
    fi
    if [ -n "${{_OLD_VIRTUAL_PS1:-}}" ] ; then
        PS1="${{_OLD_VIRTUAL_PS1:-}}"
        export PS1
        unset _OLD_VIRTUAL_PS1
    fi
    unset VIRTUAL_ENV
    unset VIRTUAL_ENV_PROMPT
    if [ ! "${{1:-}}" = "nondestructive" ] ; then
        unset -f deactivate
    fi
}}

deactivate nondestructive

VIRTUAL_ENV="{VENV_DIR}"
export VIRTUAL_ENV

_OLD_VIRTUAL_PATH="$PATH"
PATH="$VIRTUAL_ENV/bin:$PATH"
export PATH

_OLD_VIRTUAL_PS1="${{PS1:-}}"
PS1="(.venv) ${{PS1:-}}"
export PS1
VIRTUAL_ENV_PROMPT="(.venv) "
export VIRTUAL_ENV_PROMPT
''')

    # Create pip stub
    pip_path = os.path.join(VENV_DIR, 'bin', 'pip')
    with open(pip_path, 'w') as f:
        f.write(f'#!/usr/bin/env python3\nimport sys\nprint("pip stub in .venv")\n')
    os.chmod(pip_path, 0o755)

    # Create pyvenv.cfg
    pyvenv_cfg = os.path.join(VENV_DIR, 'pyvenv.cfg')
    with open(pyvenv_cfg, 'w') as f:
        f.write('home = /usr/bin\ninclude-system-site-packages = false\nversion = 3.10.12\n')

    print(f'Virtual environment created at {VENV_DIR}')

    # 4. Ensure .vscode directory exists but has NO python-related settings
    # (No workspace settings file -- the task is to create/configure these)
    os.makedirs(VSCODE_DIR, exist_ok=True)
    # Write a minimal settings.json with no python settings
    settings_path = os.path.join(VSCODE_DIR, 'settings.json')
    initial_settings = {
        "editor.formatOnSave": True,
        "editor.tabSize": 4,
        "files.trimTrailingWhitespace": True
    }
    with open(settings_path, 'w') as f:
        json.dump(initial_settings, f, indent=4)
    print(f'Workspace settings created at {settings_path} (no python settings)')

    # 5. Verify structure
    print(f'Project directory: {PROJECT_DIR}')
    for root, dirs, files in os.walk(PROJECT_DIR):
        # Skip .venv internals for cleaner output
        if '.venv' in root and root != VENV_DIR:
            continue
        level = root.replace(PROJECT_DIR, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
        if '.venv' in root:
            print(f'{indent}  (venv contents omitted)')
            continue
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f'{subindent}{file}')

    # 6. Launch VSCode with the workspace folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

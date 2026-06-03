"""
Initial Setup: Stash only auth.py changes task
Task ID: vscode_git_030
Domain: vs_code

Creates a git repository at /home/user/webapp with three modified Python files:
auth.py, routes.py, and models.py - all tracked with uncommitted changes.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
REPO_DIR = '/home/user/webapp'


def run_cmd(cmd, cwd=None, env=None):
    """Run a shell command and return output."""
    result = subprocess.run(
        shlex.split(cmd) if isinstance(cmd, str) else cmd,
        capture_output=True,
        text=True,
        cwd=cwd,
        env=env,
    )
    if result.returncode != 0:
        print(f'WARN: command failed: {cmd}')
        print(f'  stderr: {result.stderr.strip()}')
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
    # Remove any existing repo to ensure clean state
    if os.path.exists(REPO_DIR):
        run_cmd(f'rm -rf {REPO_DIR}')

    os.makedirs(REPO_DIR, exist_ok=True)

    # Set up git config for the VM user
    git_env = os.environ.copy()
    git_env['GIT_AUTHOR_NAME'] = 'Dev User'
    git_env['GIT_AUTHOR_EMAIL'] = 'dev@example.com'
    git_env['GIT_COMMITTER_NAME'] = 'Dev User'
    git_env['GIT_COMMITTER_EMAIL'] = 'dev@example.com'

    # Initialize git repository
    run_cmd('git init', cwd=REPO_DIR, env=git_env)
    run_cmd('git config user.email "dev@example.com"', cwd=REPO_DIR, env=git_env)
    run_cmd('git config user.name "Dev User"', cwd=REPO_DIR, env=git_env)

    # --- Create original committed versions of the files ---

    auth_py_original = '''\
"""Authentication module for the webapp."""

from flask import request, jsonify
from functools import wraps
import jwt
import datetime

SECRET_KEY = 'production-secret-key-2024'


def generate_token(user_id: int, role: str) -> str:
    """Generate a JWT token for the given user."""
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        'iat': datetime.datetime.utcnow(),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def verify_token(token: str) -> dict:
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError('Token has expired')
    except jwt.InvalidTokenError:
        raise ValueError('Invalid token')


def require_auth(f):
    """Decorator that requires a valid JWT token."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid Authorization header'}), 401
        token = auth_header[7:]
        try:
            payload = verify_token(token)
            request.current_user = payload
        except ValueError as e:
            return jsonify({'error': str(e)}), 401
        return f(*args, **kwargs)
    return decorated


def require_role(role: str):
    """Decorator factory that requires a specific role."""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not hasattr(request, 'current_user'):
                return jsonify({'error': 'Not authenticated'}), 401
            if request.current_user.get('role') != role:
                return jsonify({'error': 'Insufficient permissions'}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator
'''

    routes_py_original = '''\
"""Route definitions for the webapp API."""

from flask import Blueprint, request, jsonify
from .auth import require_auth, require_role
from .models import User, Product, Order

api = Blueprint('api', __name__, url_prefix='/api/v1')


@api.route('/users', methods=['GET'])
@require_auth
@require_role('admin')
def list_users():
    """Return a paginated list of all users."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    users = User.query.paginate(page=page, per_page=per_page)
    return jsonify({
        'users': [u.to_dict() for u in users.items],
        'total': users.total,
        'pages': users.pages,
        'current_page': page,
    })


@api.route('/users/<int:user_id>', methods=['GET'])
@require_auth
def get_user(user_id):
    """Return details for a specific user."""
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())


@api.route('/products', methods=['GET'])
def list_products():
    """Return all available products."""
    category = request.args.get('category')
    if category:
        products = Product.query.filter_by(category=category).all()
    else:
        products = Product.query.filter_by(active=True).all()
    return jsonify({'products': [p.to_dict() for p in products]})


@api.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Return details for a specific product."""
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())


@api.route('/orders', methods=['GET'])
@require_auth
def list_orders():
    """Return orders for the authenticated user."""
    user_id = request.current_user['user_id']
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    return jsonify({'orders': [o.to_dict() for o in orders]})


@api.route('/orders', methods=['POST'])
@require_auth
def create_order():
    """Create a new order for the authenticated user."""
    data = request.get_json()
    if not data or 'items' not in data:
        return jsonify({'error': 'Request body must include items'}), 400
    user_id = request.current_user['user_id']
    order = Order.create_from_items(user_id=user_id, items=data['items'])
    return jsonify(order.to_dict()), 201
'''

    models_py_original = '''\
"""Database models for the webapp."""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """User account model."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    orders = db.relationship('Order', backref='user', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat(),
            'is_active': self.is_active,
        }


class Product(db.Model):
    """Product catalog model."""
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    category = db.Column(db.String(50))
    stock_quantity = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'category': self.category,
            'stock_quantity': self.stock_quantity,
        }


class Order(db.Model):
    """Customer order model."""
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')
    total_amount = db.Column(db.Numeric(10, 2))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    items = db.relationship('OrderItem', backref='order', lazy=True)

    @classmethod
    def create_from_items(cls, user_id: int, items: list) -> 'Order':
        """Create an order and compute total from items."""
        order = cls(user_id=user_id)
        total = 0
        for item_data in items:
            product = Product.query.get(item_data['product_id'])
            if product:
                qty = item_data.get('quantity', 1)
                item = OrderItem(product_id=product.id, quantity=qty, unit_price=product.price)
                order.items.append(item)
                total += float(product.price) * qty
        order.total_amount = total
        db.session.add(order)
        db.session.commit()
        return order

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'status': self.status,
            'total_amount': float(self.total_amount) if self.total_amount else 0,
            'created_at': self.created_at.isoformat(),
        }


class OrderItem(db.Model):
    """Individual line item within an order."""
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'unit_price': float(self.unit_price),
        }
'''

    # Write original files
    with open(os.path.join(REPO_DIR, 'auth.py'), 'w') as f:
        f.write(auth_py_original)
    with open(os.path.join(REPO_DIR, 'routes.py'), 'w') as f:
        f.write(routes_py_original)
    with open(os.path.join(REPO_DIR, 'models.py'), 'w') as f:
        f.write(models_py_original)

    # Create a README for the repo
    readme_content = '''\
# Webapp

A Flask-based web application with authentication, product catalog, and order management.

## Structure

- `auth.py` — JWT authentication and role-based access control
- `routes.py` — REST API route definitions
- `models.py` — SQLAlchemy database models
'''
    with open(os.path.join(REPO_DIR, 'README.md'), 'w') as f:
        f.write(readme_content)

    # Initial commit with all files
    run_cmd('git add .', cwd=REPO_DIR, env=git_env)
    result = run_cmd(
        'git commit -m "Initial commit: add auth, routes, and models modules"',
        cwd=REPO_DIR, env=git_env
    )
    print(f'Initial commit: {result.stdout.strip()}')

    # --- Now make modifications to all three files (experimental/WIP changes) ---

    # Modified auth.py: adds experimental OAuth2 support (experimental, hence should be stashed)
    auth_py_modified = '''\
"""Authentication module for the webapp."""

from flask import request, jsonify
from functools import wraps
import jwt
import datetime
import hashlib
import secrets

SECRET_KEY = 'production-secret-key-2024'
OAUTH2_CLIENT_ID = 'webapp-client-experimental'
OAUTH2_CLIENT_SECRET = secrets.token_hex(32)


def generate_token(user_id: int, role: str) -> str:
    """Generate a JWT token for the given user."""
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        'iat': datetime.datetime.utcnow(),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def generate_oauth2_token(user_id: int, scope: str = 'read') -> dict:
    """Generate an experimental OAuth2 access token."""
    access_token = secrets.token_urlsafe(32)
    refresh_token = secrets.token_urlsafe(32)
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'Bearer',
        'expires_in': 3600,
        'scope': scope,
    }


def verify_token(token: str) -> dict:
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError('Token has expired')
    except jwt.InvalidTokenError:
        raise ValueError('Invalid token')


def require_auth(f):
    """Decorator that requires a valid JWT token."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid Authorization header'}), 401
        token = auth_header[7:]
        try:
            payload = verify_token(token)
            request.current_user = payload
        except ValueError as e:
            return jsonify({'error': str(e)}), 401
        return f(*args, **kwargs)
    return decorated


def require_role(role: str):
    """Decorator factory that requires a specific role."""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not hasattr(request, 'current_user'):
                return jsonify({'error': 'Not authenticated'}), 401
            if request.current_user.get('role') != role:
                return jsonify({'error': 'Insufficient permissions'}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator


def experimental_pkce_verify(code_verifier: str, code_challenge: str) -> bool:
    """Experimental PKCE verification for OAuth2 flow."""
    import base64
    digest = hashlib.sha256(code_verifier.encode()).digest()
    computed_challenge = base64.urlsafe_b64encode(digest).rstrip(b'=').decode()
    return computed_challenge == code_challenge
'''

    # Modified routes.py: adds new search endpoint and pagination improvements
    routes_py_modified = '''\
"""Route definitions for the webapp API."""

from flask import Blueprint, request, jsonify
from .auth import require_auth, require_role
from .models import User, Product, Order

api = Blueprint('api', __name__, url_prefix='/api/v1')

DEFAULT_PAGE_SIZE = 25
MAX_PAGE_SIZE = 100


@api.route('/users', methods=['GET'])
@require_auth
@require_role('admin')
def list_users():
    """Return a paginated list of all users."""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', DEFAULT_PAGE_SIZE, type=int), MAX_PAGE_SIZE)
    users = User.query.paginate(page=page, per_page=per_page)
    return jsonify({
        'users': [u.to_dict() for u in users.items],
        'total': users.total,
        'pages': users.pages,
        'current_page': page,
        'per_page': per_page,
    })


@api.route('/users/<int:user_id>', methods=['GET'])
@require_auth
def get_user(user_id):
    """Return details for a specific user."""
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())


@api.route('/products', methods=['GET'])
def list_products():
    """Return all available products."""
    category = request.args.get('category')
    search = request.args.get('search', '').strip()
    if category:
        products = Product.query.filter_by(category=category)
    else:
        products = Product.query.filter_by(active=True)
    if search:
        products = products.filter(Product.name.ilike(f'%{search}%'))
    return jsonify({'products': [p.to_dict() for p in products.all()]})


@api.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Return details for a specific product."""
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())


@api.route('/orders', methods=['GET'])
@require_auth
def list_orders():
    """Return orders for the authenticated user."""
    user_id = request.current_user['user_id']
    status = request.args.get('status')
    query = Order.query.filter_by(user_id=user_id)
    if status:
        query = query.filter_by(status=status)
    orders = query.order_by(Order.created_at.desc()).all()
    return jsonify({'orders': [o.to_dict() for o in orders]})


@api.route('/orders', methods=['POST'])
@require_auth
def create_order():
    """Create a new order for the authenticated user."""
    data = request.get_json()
    if not data or 'items' not in data:
        return jsonify({'error': 'Request body must include items'}), 400
    user_id = request.current_user['user_id']
    order = Order.create_from_items(user_id=user_id, items=data['items'])
    return jsonify(order.to_dict()), 201
'''

    # Modified models.py: adds full-text search index hints and soft delete support
    models_py_modified = '''\
"""Database models for the webapp."""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

SOFT_DELETE_ENABLED = True


class User(db.Model):
    """User account model."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    deleted_at = db.Column(db.DateTime, nullable=True)

    orders = db.relationship('Order', backref='user', lazy=True)

    @classmethod
    def active_users(cls):
        """Return only non-deleted active users."""
        return cls.query.filter_by(is_active=True, deleted_at=None)

    def soft_delete(self):
        """Soft-delete the user by setting deleted_at timestamp."""
        self.deleted_at = datetime.utcnow()
        self.is_active = False
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat(),
            'is_active': self.is_active,
        }


class Product(db.Model):
    """Product catalog model."""
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    category = db.Column(db.String(50))
    stock_quantity = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tags = db.Column(db.JSON, default=list)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'category': self.category,
            'stock_quantity': self.stock_quantity,
            'tags': self.tags or [],
        }


class Order(db.Model):
    """Customer order model."""
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')
    total_amount = db.Column(db.Numeric(10, 2))
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    items = db.relationship('OrderItem', backref='order', lazy=True)

    @classmethod
    def create_from_items(cls, user_id: int, items: list) -> 'Order':
        """Create an order and compute total from items."""
        order = cls(user_id=user_id)
        total = 0
        for item_data in items:
            product = Product.query.get(item_data['product_id'])
            if product:
                qty = item_data.get('quantity', 1)
                item = OrderItem(product_id=product.id, quantity=qty, unit_price=product.price)
                order.items.append(item)
                total += float(product.price) * qty
        order.total_amount = total
        db.session.add(order)
        db.session.commit()
        return order

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'status': self.status,
            'total_amount': float(self.total_amount) if self.total_amount else 0,
            'created_at': self.created_at.isoformat(),
            'notes': self.notes,
        }


class OrderItem(db.Model):
    """Individual line item within an order."""
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'unit_price': float(self.unit_price),
        }
'''

    # Write modified files (these are the working directory changes)
    with open(os.path.join(REPO_DIR, 'auth.py'), 'w') as f:
        f.write(auth_py_modified)
    with open(os.path.join(REPO_DIR, 'routes.py'), 'w') as f:
        f.write(routes_py_modified)
    with open(os.path.join(REPO_DIR, 'models.py'), 'w') as f:
        f.write(models_py_modified)

    # Verify git status shows all three files as modified
    result = run_cmd('git status --short', cwd=REPO_DIR, env=git_env)
    print(f'Git status after modifications:\n{result.stdout}')

    print(f'Initial repository created at: {REPO_DIR}')

    # GUI-ready startup: open VSCode with the webapp repository
    launch_gui(f'code "{REPO_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

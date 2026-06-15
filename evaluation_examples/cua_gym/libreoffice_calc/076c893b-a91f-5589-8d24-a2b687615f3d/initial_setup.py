"""
Initial Setup: Git reflog recovery operation in VSCode
Task ID: vscode_gf1_080
Domain: vscode (os/git)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf1_080'
PROJECT_DIR = f'{WORKDIR}/projects/accident-prone'

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

def run_git(cmd, cwd=PROJECT_DIR):
    """Run a git command in the project directory."""
    result = subprocess.run(
        cmd, cwd=cwd, shell=True,
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Git command failed: {cmd}")
        print(f"stderr: {result.stderr}")
    return result

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)

def create_initial():
    # Clean up if exists
    if os.path.exists(PROJECT_DIR):
        import shutil
        shutil.rmtree(PROJECT_DIR)

    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Initialize git repo with 'main' as default branch
    run_git('git init -b main')
    run_git('git config user.email "dev@company.com"')
    run_git('git config user.name "Alex Rivera"')

    # ---- Commit 1: Initial project structure ----
    create_file(f'{PROJECT_DIR}/README.md', """# Accident-Prone E-Commerce Platform

A modern e-commerce backend built with Python and FastAPI.

## Setup
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Architecture
- `src/` - Core application code
- `tests/` - Test suite
- `config/` - Configuration files
""")
    create_file(f'{PROJECT_DIR}/requirements.txt', """fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.2
alembic==1.13.0
pytest==7.4.3
httpx==0.25.2
redis==5.0.1
celery==5.3.6
""")
    create_file(f'{PROJECT_DIR}/src/__init__.py', '')
    create_file(f'{PROJECT_DIR}/src/main.py', """from fastapi import FastAPI
from src.routes import products, users, orders

app = FastAPI(title="Accident-Prone E-Commerce", version="0.1.0")

app.include_router(products.router, prefix="/api/products", tags=["products"])
app.include_router(users.router, prefix="/api/users", tags=["users"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "0.1.0"}
""")
    create_file(f'{PROJECT_DIR}/src/routes/__init__.py', '')
    create_file(f'{PROJECT_DIR}/src/routes/products.py', """from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class Product(BaseModel):
    name: str
    price: float
    description: str = ""

products_db = []

@router.get("/")
async def list_products():
    return products_db

@router.post("/")
async def create_product(product: Product):
    products_db.append(product.dict())
    return {"id": len(products_db), **product.dict()}
""")
    create_file(f'{PROJECT_DIR}/src/routes/users.py', """from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

router = APIRouter()

class User(BaseModel):
    username: str
    email: str
    full_name: str = ""

users_db = []

@router.get("/")
async def list_users():
    return users_db

@router.post("/")
async def create_user(user: User):
    users_db.append(user.dict())
    return {"id": len(users_db), **user.dict()}
""")
    create_file(f'{PROJECT_DIR}/config/settings.py', """import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
DEBUG = os.getenv("DEBUG", "true").lower() == "true"
""")
    run_git('git add -A')
    # Set a fixed date for reproducibility (3.5 hours ago approx)
    env_date = 'GIT_AUTHOR_DATE="2026-04-02T18:15:00" GIT_COMMITTER_DATE="2026-04-02T18:15:00"'
    run_git(f'{env_date} git commit -m "Initial project setup with FastAPI structure"')

    # ---- Commit 2: Add database models ----
    create_file(f'{PROJECT_DIR}/src/models/__init__.py', '')
    create_file(f'{PROJECT_DIR}/src/models/base.py', """from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.settings import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
""")
    create_file(f'{PROJECT_DIR}/src/models/product.py', """from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from src.models.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1000), default="")
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
""")
    create_file(f'{PROJECT_DIR}/src/models/user.py', """from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from src.models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), default="")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
""")
    run_git('git add -A')
    env_date = 'GIT_AUTHOR_DATE="2026-04-02T18:30:00" GIT_COMMITTER_DATE="2026-04-02T18:30:00"'
    run_git(f'{env_date} git commit -m "Add SQLAlchemy database models for products and users"')

    # ---- Commit 3: Add payment processing feature (THE IMPORTANT ONE) ----
    create_file(f'{PROJECT_DIR}/src/routes/orders.py', """from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from src.services.payment import PaymentService

router = APIRouter()

class OrderItem(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItem]
    payment_method: str = "credit_card"
    shipping_address: str = ""

class OrderResponse(BaseModel):
    order_id: str
    total: float
    status: str
    payment_status: str

@router.post("/", response_model=OrderResponse)
async def create_order(order: OrderCreate):
    payment_svc = PaymentService()
    total = sum(item.quantity * 29.99 for item in order.items)  # simplified
    payment_result = await payment_svc.process_payment(total, order.payment_method)
    return OrderResponse(
        order_id=payment_result["transaction_id"],
        total=total,
        status="confirmed",
        payment_status=payment_result["status"]
    )

@router.get("/{order_id}")
async def get_order(order_id: str):
    return {"order_id": order_id, "status": "processing"}
""")
    create_file(f'{PROJECT_DIR}/src/services/__init__.py', '')
    create_file(f'{PROJECT_DIR}/src/services/payment.py', """import uuid
import hashlib
from datetime import datetime

class PaymentService:
    SUPPORTED_METHODS = ["credit_card", "debit_card", "paypal", "bank_transfer"]

    async def process_payment(self, amount: float, method: str) -> dict:
        if method not in self.SUPPORTED_METHODS:
            raise ValueError(f"Unsupported payment method: {method}")
        if amount <= 0:
            raise ValueError("Payment amount must be positive")

        transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
        return {
            "transaction_id": transaction_id,
            "amount": amount,
            "method": method,
            "status": "completed",
            "timestamp": datetime.utcnow().isoformat()
        }

    async def refund_payment(self, transaction_id: str, amount: float) -> dict:
        refund_id = f"RFD-{uuid.uuid4().hex[:12].upper()}"
        return {
            "refund_id": refund_id,
            "original_transaction": transaction_id,
            "amount": amount,
            "status": "refunded"
        }

    def validate_card(self, card_number: str) -> bool:
        digits = [int(d) for d in card_number if d.isdigit()]
        checksum = 0
        for i, d in enumerate(reversed(digits)):
            if i % 2 == 1:
                d *= 2
                if d > 9:
                    d -= 9
            checksum += d
        return checksum % 10 == 0
""")
    run_git('git add -A')
    env_date = 'GIT_AUTHOR_DATE="2026-04-02T18:45:00" GIT_COMMITTER_DATE="2026-04-02T18:45:00"'
    run_git(f'{env_date} git commit -m "Add payment processing feature with order management"')

    # ---- Commit 4: Add authentication middleware ----
    create_file(f'{PROJECT_DIR}/src/middleware/__init__.py', '')
    create_file(f'{PROJECT_DIR}/src/middleware/auth.py', """from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from config.settings import SECRET_KEY

security = HTTPBearer()

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def auth_middleware(request: Request, call_next):
    public_paths = ["/health", "/api/users/login", "/api/users/register", "/docs", "/openapi.json"]
    if request.url.path in public_paths:
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing authorization header")

    token = auth_header.split(" ")[1]
    user_data = decode_token(token)
    request.state.user = user_data
    return await call_next(request)
""")
    run_git('git add -A')
    env_date = 'GIT_AUTHOR_DATE="2026-04-02T19:00:00" GIT_COMMITTER_DATE="2026-04-02T19:00:00"'
    run_git(f'{env_date} git commit -m "Add JWT authentication middleware"')

    # ---- Commit 5: Add test suite ----
    create_file(f'{PROJECT_DIR}/tests/__init__.py', '')
    create_file(f'{PROJECT_DIR}/tests/test_products.py', """import pytest
from httpx import AsyncClient
from src.main import app

@pytest.mark.asyncio
async def test_list_products():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/products/")
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_create_product():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/products/", json={
            "name": "Wireless Headphones",
            "price": 79.99,
            "description": "Premium noise-canceling headphones"
        })
        assert response.status_code == 200
        assert response.json()["name"] == "Wireless Headphones"
""")
    create_file(f'{PROJECT_DIR}/tests/test_payment.py', """import pytest
from src.services.payment import PaymentService

@pytest.mark.asyncio
async def test_process_payment():
    svc = PaymentService()
    result = await svc.process_payment(99.99, "credit_card")
    assert result["status"] == "completed"
    assert result["amount"] == 99.99
    assert result["transaction_id"].startswith("TXN-")

@pytest.mark.asyncio
async def test_invalid_payment_method():
    svc = PaymentService()
    with pytest.raises(ValueError, match="Unsupported payment method"):
        await svc.process_payment(50.0, "bitcoin")

@pytest.mark.asyncio
async def test_refund_payment():
    svc = PaymentService()
    result = await svc.refund_payment("TXN-ABC123", 25.00)
    assert result["status"] == "refunded"
    assert result["refund_id"].startswith("RFD-")

def test_validate_card():
    svc = PaymentService()
    assert svc.validate_card("4532015112830366") == True
    assert svc.validate_card("1234567890123456") == False
""")
    run_git('git add -A')
    env_date = 'GIT_AUTHOR_DATE="2026-04-02T19:15:00" GIT_COMMITTER_DATE="2026-04-02T19:15:00"'
    run_git(f'{env_date} git commit -m "Add comprehensive test suite for products and payments"')

    # ---- Commit 6: Add caching layer ----
    create_file(f'{PROJECT_DIR}/src/services/cache.py', """import json
import redis
from config.settings import REDIS_URL

class CacheService:
    def __init__(self):
        self.client = redis.from_url(REDIS_URL, decode_responses=True)
        self.default_ttl = 3600  # 1 hour

    def get(self, key: str):
        value = self.client.get(key)
        if value:
            return json.loads(value)
        return None

    def set(self, key: str, value, ttl: int = None):
        self.client.setex(
            key,
            ttl or self.default_ttl,
            json.dumps(value)
        )

    def delete(self, key: str):
        self.client.delete(key)

    def invalidate_pattern(self, pattern: str):
        keys = self.client.keys(pattern)
        if keys:
            self.client.delete(*keys)
""")
    run_git('git add -A')
    env_date = 'GIT_AUTHOR_DATE="2026-04-02T19:30:00" GIT_COMMITTER_DATE="2026-04-02T19:30:00"'
    run_git(f'{env_date} git commit -m "Add Redis caching layer for product queries"')

    # ---- Commit 7: Add API rate limiting ----
    create_file(f'{PROJECT_DIR}/src/middleware/rate_limit.py', """import time
from collections import defaultdict
from fastapi import Request, HTTPException

class RateLimiter:
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)

    def _clean_old_requests(self, client_ip: str):
        now = time.time()
        cutoff = now - self.window_seconds
        self.requests[client_ip] = [
            ts for ts in self.requests[client_ip] if ts > cutoff
        ]

    def check_rate_limit(self, client_ip: str) -> bool:
        self._clean_old_requests(client_ip)
        if len(self.requests[client_ip]) >= self.max_requests:
            return False
        self.requests[client_ip].append(time.time())
        return True

rate_limiter = RateLimiter()

async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    if not rate_limiter.check_rate_limit(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again later."
        )
    return await call_next(request)
""")
    run_git('git add -A')
    env_date = 'GIT_AUTHOR_DATE="2026-04-02T19:45:00" GIT_COMMITTER_DATE="2026-04-02T19:45:00"'
    run_git(f'{env_date} git commit -m "Add API rate limiting middleware"')

    # Now we have 7 commits on main. Record the current HEAD (commit 7).
    head_before_reset = run_git('git rev-parse HEAD').stdout.strip()
    print(f"HEAD before reset: {head_before_reset}")

    # ---- Simulate the accident: git reset --hard HEAD~5 ----
    # This removes commits 3-7 (payment, auth, tests, cache, rate limit)
    run_git('git reset --hard HEAD~5')

    head_after_reset = run_git('git rev-parse HEAD').stdout.strip()
    print(f"HEAD after reset (back to commit 2): {head_after_reset}")

    # Verify reflog shows the history
    reflog_output = run_git('git reflog').stdout
    print(f"Reflog entries:\n{reflog_output}")

    print(f"Project created at: {PROJECT_DIR}")
    print("Simulated accident: git reset --hard HEAD~5 removed 5 commits")
    print("Developer needs to use git reflog to recover lost work")

    # GUI-ready: Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()

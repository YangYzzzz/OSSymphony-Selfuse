"""
Initial Setup: Git multi-remote project with feature branch for rebase task
Task ID: vscode_gf2_031
Domain: vscode

Creates a realistic API project with:
- Two remotes: 'origin' (fork) and 'upstream' (original repo)
- 'main' branch with shared history
- 'feature/pagination' branch diverged from main (checked out)
- origin/main has commits ahead of the feature branch base
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf2_031'
PROJECT_DIR = f'{WORKDIR}/projects/api'

# Bare repo paths (simulate remotes)
ORIGIN_BARE = f'{WORKDIR}/.git-remotes/origin-api.git'
UPSTREAM_BARE = f'{WORKDIR}/.git-remotes/upstream-api.git'


def run(cmd, cwd=None, env=None):
    """Run a shell command, raising on failure."""
    result = subprocess.run(
        cmd, shell=True, cwd=cwd, env=env,
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"CMD FAILED: {cmd}")
        print(f"STDERR: {result.stderr}")
        raise RuntimeError(f"Command failed: {cmd}\n{result.stderr}")
    return result.stdout.strip()


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


def create_project():
    # Clean up any existing state
    for d in [PROJECT_DIR, ORIGIN_BARE, UPSTREAM_BARE]:
        if os.path.exists(d):
            subprocess.run(f'rm -rf "{d}"', shell=True)

    os.makedirs(os.path.dirname(ORIGIN_BARE), exist_ok=True)
    os.makedirs(PROJECT_DIR, exist_ok=True)

    git_env = os.environ.copy()
    git_env['GIT_AUTHOR_NAME'] = 'Sarah Chen'
    git_env['GIT_AUTHOR_EMAIL'] = 'sarah.chen@example.com'
    git_env['GIT_COMMITTER_NAME'] = 'Sarah Chen'
    git_env['GIT_COMMITTER_EMAIL'] = 'sarah.chen@example.com'

    def git(cmd, cwd=PROJECT_DIR):
        return run(f'git {cmd}', cwd=cwd, env=git_env)

    # ---- Step 1: Create upstream bare repo ----
    run(f'git init --bare "{UPSTREAM_BARE}"', env=git_env)

    # ---- Step 2: Create the working repo ----
    git('init -b main')
    git('config user.name "Sarah Chen"')
    git('config user.email "sarah.chen@example.com"')

    # ---- Step 3: Create initial project files (Commit 1 - project setup) ----
    # README
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write("""# REST API Service

A high-performance REST API for managing product catalog and inventory.

## Tech Stack
- Python 3.11+ / FastAPI
- PostgreSQL 15
- Redis for caching
- Docker for containerization

## Getting Started

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API Documentation
Visit `/docs` for interactive Swagger documentation.
""")

    # requirements.txt
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write("""fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
redis==5.0.1
pydantic==2.5.2
alembic==1.13.0
pytest==7.4.3
httpx==0.25.2
python-dotenv==1.0.0
""")

    # .gitignore
    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write("""__pycache__/
*.pyc
.env
.venv/
*.egg-info/
dist/
build/
.pytest_cache/
.coverage
htmlcov/
""")

    # app directory
    app_dir = os.path.join(PROJECT_DIR, 'app')
    os.makedirs(app_dir, exist_ok=True)

    with open(os.path.join(app_dir, '__init__.py'), 'w') as f:
        f.write('')

    with open(os.path.join(app_dir, 'main.py'), 'w') as f:
        f.write("""from fastapi import FastAPI
from app.routers import products, categories, health

app = FastAPI(
    title="Product Catalog API",
    description="REST API for product catalog management",
    version="1.2.0"
)

app.include_router(health.router, tags=["health"])
app.include_router(products.router, prefix="/api/v1", tags=["products"])
app.include_router(categories.router, prefix="/api/v1", tags=["categories"])


@app.on_event("startup")
async def startup_event():
    print("Starting Product Catalog API v1.2.0")
""")

    with open(os.path.join(app_dir, 'config.py'), 'w') as f:
        f.write("""import os
from pydantic import BaseModel


class Settings(BaseModel):
    database_url: str = os.getenv("DATABASE_URL", "postgresql://localhost:5432/catalog")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    api_key: str = os.getenv("API_KEY", "dev-key-12345")
    items_per_page: int = 20


settings = Settings()
""")

    with open(os.path.join(app_dir, 'database.py'), 'w') as f:
        f.write("""from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
""")

    # Models
    models_dir = os.path.join(app_dir, 'models')
    os.makedirs(models_dir, exist_ok=True)

    with open(os.path.join(models_dir, '__init__.py'), 'w') as f:
        f.write('from app.models.product import Product\nfrom app.models.category import Category\n')

    with open(os.path.join(models_dir, 'product.py'), 'w') as f:
        f.write("""from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1000))
    price = Column(Float, nullable=False)
    sku = Column(String(50), unique=True, nullable=False)
    stock_quantity = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey("categories.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = relationship("Category", back_populates="products")
""")

    with open(os.path.join(models_dir, 'category.py'), 'w') as f:
        f.write("""from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(500))

    products = relationship("Product", back_populates="category")
""")

    # Routers
    routers_dir = os.path.join(app_dir, 'routers')
    os.makedirs(routers_dir, exist_ok=True)

    with open(os.path.join(routers_dir, '__init__.py'), 'w') as f:
        f.write('')

    with open(os.path.join(routers_dir, 'health.py'), 'w') as f:
        f.write("""from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.2.0"}
""")

    with open(os.path.join(routers_dir, 'products.py'), 'w') as f:
        f.write("""from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.product import Product

router = APIRouter()


@router.get("/products")
async def list_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products


@router.get("/products/{product_id}")
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/products")
async def create_product(name: str, price: float, sku: str, db: Session = Depends(get_db)):
    product = Product(name=name, price=price, sku=sku)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product
""")

    with open(os.path.join(routers_dir, 'categories.py'), 'w') as f:
        f.write("""from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.category import Category

router = APIRouter()


@router.get("/categories")
async def list_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories


@router.get("/categories/{category_id}")
async def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category
""")

    # Dockerfile
    with open(os.path.join(PROJECT_DIR, 'Dockerfile'), 'w') as f:
        f.write("""FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
""")

    git('add -A')
    git('commit -m "Initial project setup with FastAPI structure"')

    # ---- Commit 2: Add database migrations ----
    migrations_dir = os.path.join(PROJECT_DIR, 'migrations')
    os.makedirs(os.path.join(migrations_dir, 'versions'), exist_ok=True)

    with open(os.path.join(migrations_dir, 'env.py'), 'w') as f:
        f.write("""from alembic import context
from app.database import Base, engine
from app.models import Product, Category

target_metadata = Base.metadata


def run_migrations_online():
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
""")

    git('add -A')
    git('commit -m "Add Alembic migration configuration"')

    # ---- Commit 3: Add tests ----
    tests_dir = os.path.join(PROJECT_DIR, 'tests')
    os.makedirs(tests_dir, exist_ok=True)

    with open(os.path.join(tests_dir, '__init__.py'), 'w') as f:
        f.write('')

    with open(os.path.join(tests_dir, 'test_health.py'), 'w') as f:
        f.write("""import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_health_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
""")

    with open(os.path.join(tests_dir, 'test_products.py'), 'w') as f:
        f.write("""import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_list_products():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
""")

    git('add -A')
    git('commit -m "Add pytest test suite for health and products endpoints"')

    # ---- Push main to upstream and create origin bare ----
    git(f'remote add upstream "{UPSTREAM_BARE}"')
    git('push upstream main')

    # Create origin bare as a fork of upstream
    run(f'git clone --bare "{UPSTREAM_BARE}" "{ORIGIN_BARE}"', env=git_env)
    # Ensure HEAD points to main in bare repos
    run(f'git -C "{ORIGIN_BARE}" symbolic-ref HEAD refs/heads/main', env=git_env)
    run(f'git -C "{UPSTREAM_BARE}" symbolic-ref HEAD refs/heads/main', env=git_env)
    git(f'remote add origin "{ORIGIN_BARE}"')
    git('push origin main')

    # ---- Step 4: Add commits to origin/main (simulating upstream progress) ----
    # We'll add commits directly to origin bare via a temp clone
    temp_clone = f'{WORKDIR}/.git-remotes/temp-origin-work'
    if os.path.exists(temp_clone):
        subprocess.run(f'rm -rf "{temp_clone}"', shell=True)

    run(f'git clone "{ORIGIN_BARE}" "{temp_clone}"', env=git_env)
    run('git checkout main', cwd=temp_clone, env=git_env)
    run('git config user.name "Marcus Johnson"', cwd=temp_clone, env=git_env)
    run('git config user.email "marcus.j@example.com"', cwd=temp_clone, env=git_env)

    marcus_env = git_env.copy()
    marcus_env['GIT_AUTHOR_NAME'] = 'Marcus Johnson'
    marcus_env['GIT_AUTHOR_EMAIL'] = 'marcus.j@example.com'
    marcus_env['GIT_COMMITTER_NAME'] = 'Marcus Johnson'
    marcus_env['GIT_COMMITTER_EMAIL'] = 'marcus.j@example.com'

    # Add logging middleware on main
    middleware_dir = os.path.join(temp_clone, 'app', 'middleware')
    os.makedirs(middleware_dir, exist_ok=True)

    with open(os.path.join(middleware_dir, '__init__.py'), 'w') as f:
        f.write('')

    with open(os.path.join(middleware_dir, 'logging.py'), 'w') as f:
        f.write("""import time
import logging
from fastapi import Request

logger = logging.getLogger("api.access")


async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(
        f"{request.method} {request.url.path} "
        f"status={response.status_code} duration={duration:.3f}s"
    )
    return response
""")

    run('git add -A', cwd=temp_clone, env=marcus_env)
    run('git commit -m "Add request logging middleware"', cwd=temp_clone, env=marcus_env)

    # Add error handling utilities
    with open(os.path.join(temp_clone, 'app', 'exceptions.py'), 'w') as f:
        f.write("""from fastapi import HTTPException


class NotFoundError(HTTPException):
    def __init__(self, resource: str, resource_id: int):
        super().__init__(
            status_code=404,
            detail=f"{resource} with id {resource_id} not found"
        )


class ConflictError(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=409, detail=message)


class ValidationError(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=422, detail=message)
""")

    run('git add -A', cwd=temp_clone, env=marcus_env)
    run('git commit -m "Add custom exception classes for consistent error handling"', cwd=temp_clone, env=marcus_env)

    # Push these commits to origin bare
    run('git push origin main', cwd=temp_clone, env=marcus_env)

    # Clean up temp clone
    subprocess.run(f'rm -rf "{temp_clone}"', shell=True)

    # ---- Step 5: Create feature/pagination branch (from original main, before the new origin/main commits) ----
    # This creates the divergence: feature/pagination is based on old main, origin/main has moved ahead
    git('checkout -b feature/pagination main')

    # Commit 1 on feature branch: Add pagination utility
    with open(os.path.join(app_dir, 'pagination.py'), 'w') as f:
        f.write("""from dataclasses import dataclass
from typing import TypeVar, Generic, List
from sqlalchemy.orm import Query

T = TypeVar('T')


@dataclass
class PaginatedResponse(Generic[T]):
    items: List[T]
    total: int
    page: int
    per_page: int
    total_pages: int

    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages

    @property
    def has_prev(self) -> bool:
        return self.page > 1


def paginate(query: Query, page: int = 1, per_page: int = 20) -> PaginatedResponse:
    total = query.count()
    total_pages = (total + per_page - 1) // per_page
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
    )
""")

    git('add -A')
    git('commit -m "Add pagination utility with PaginatedResponse dataclass"')

    # Commit 2 on feature branch: Update products router with pagination
    with open(os.path.join(routers_dir, 'products.py'), 'w') as f:
        f.write("""from fastapi import APIRouter, Depends, HTTPException, Query as QueryParam
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.product import Product
from app.pagination import paginate

router = APIRouter()


@router.get("/products")
async def list_products(
    page: int = QueryParam(1, ge=1, description="Page number"),
    per_page: int = QueryParam(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
):
    query = db.query(Product).order_by(Product.created_at.desc())
    result = paginate(query, page=page, per_page=per_page)
    return {
        "items": result.items,
        "total": result.total,
        "page": result.page,
        "per_page": result.per_page,
        "total_pages": result.total_pages,
        "has_next": result.has_next,
        "has_prev": result.has_prev,
    }


@router.get("/products/{product_id}")
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/products")
async def create_product(name: str, price: float, sku: str, db: Session = Depends(get_db)):
    product = Product(name=name, price=price, sku=sku)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product
""")

    git('add -A')
    git('commit -m "Integrate pagination into products list endpoint"')

    # Commit 3 on feature branch: Add pagination tests
    with open(os.path.join(tests_dir, 'test_pagination.py'), 'w') as f:
        f.write("""import pytest
from app.pagination import PaginatedResponse, paginate


def test_paginated_response_has_next():
    resp = PaginatedResponse(items=[], total=50, page=1, per_page=20, total_pages=3)
    assert resp.has_next is True
    assert resp.has_prev is False


def test_paginated_response_last_page():
    resp = PaginatedResponse(items=[], total=50, page=3, per_page=20, total_pages=3)
    assert resp.has_next is False
    assert resp.has_prev is True


def test_paginated_response_single_page():
    resp = PaginatedResponse(items=[], total=5, page=1, per_page=20, total_pages=1)
    assert resp.has_next is False
    assert resp.has_prev is False
""")

    git('add -A')
    git('commit -m "Add unit tests for pagination utility"')

    # ---- Step 6: Fetch from origin to update remote tracking branches ----
    git('fetch origin')
    git('fetch upstream')

    print(f'Project created at: {PROJECT_DIR}')
    print(f'Current branch: feature/pagination')
    print(f'Remotes: origin ({ORIGIN_BARE}), upstream ({UPSTREAM_BARE})')

    # Show branch state
    log_output = run('git log --graph --oneline --all --decorate -15', cwd=PROJECT_DIR, env=git_env)
    print(f'\nBranch topology:\n{log_output}')

    # ---- Step 7: GUI-ready startup ----
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_project()

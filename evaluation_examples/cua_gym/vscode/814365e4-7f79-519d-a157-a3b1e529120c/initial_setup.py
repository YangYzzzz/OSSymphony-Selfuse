"""
Initial Setup: Configure a devcontainer for a Python project
Task ID: vscode_gf3_034
Domain: vscode

Creates a realistic Python API project structure WITHOUT a .devcontainer directory.
The agent's task is to create the devcontainer.json file.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_034'
PROJECT_DIR = f'{WORKDIR}/projects/python-api'

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
    os.makedirs(f'{PROJECT_DIR}/app', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/app/routers', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/app/models', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)

    # requirements.txt
    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write("""fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.2
alembic==1.13.0
pytest==7.4.3
httpx==0.25.2
python-dotenv==1.0.0
psycopg2-binary==2.9.9
""")

    # main.py
    with open(f'{PROJECT_DIR}/app/main.py', 'w') as f:
        f.write('''"""
Python API Service - FastAPI Application
"""

from fastapi import FastAPI
from app.routers import users, products

app = FastAPI(
    title="Inventory Management API",
    description="RESTful API for managing product inventory and user accounts",
    version="1.2.0",
)

app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(products.router, prefix="/api/v1/products", tags=["products"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.2.0"}
''')

    # app/__init__.py
    with open(f'{PROJECT_DIR}/app/__init__.py', 'w') as f:
        f.write('')

    # app/routers/__init__.py
    with open(f'{PROJECT_DIR}/app/routers/__init__.py', 'w') as f:
        f.write('')

    # app/routers/users.py
    with open(f'{PROJECT_DIR}/app/routers/users.py', 'w') as f:
        f.write('''from fastapi import APIRouter, HTTPException
from app.models.user import User, UserCreate

router = APIRouter()

fake_users_db = [
    {"id": 1, "name": "Sarah Chen", "email": "sarah.chen@techcorp.io", "role": "admin"},
    {"id": 2, "name": "Marcus Johnson", "email": "marcus.j@techcorp.io", "role": "editor"},
    {"id": 3, "name": "Priya Patel", "email": "priya.p@techcorp.io", "role": "viewer"},
]


@router.get("/")
async def list_users():
    return fake_users_db


@router.get("/{user_id}")
async def get_user(user_id: int):
    for user in fake_users_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")


@router.post("/")
async def create_user(user: UserCreate):
    new_id = max(u["id"] for u in fake_users_db) + 1
    new_user = {"id": new_id, **user.dict()}
    fake_users_db.append(new_user)
    return new_user
''')

    # app/routers/products.py
    with open(f'{PROJECT_DIR}/app/routers/products.py', 'w') as f:
        f.write('''from fastapi import APIRouter, HTTPException

router = APIRouter()

inventory = [
    {"id": 1, "name": "Wireless Keyboard", "sku": "WK-2024-001", "price": 79.99, "stock": 145},
    {"id": 2, "name": "USB-C Hub 7-in-1", "sku": "UH-2024-003", "price": 54.50, "stock": 230},
    {"id": 3, "name": "Monitor Stand Riser", "sku": "MS-2024-012", "price": 42.00, "stock": 87},
    {"id": 4, "name": "Ergonomic Mouse Pad", "sku": "MP-2024-007", "price": 24.99, "stock": 312},
]


@router.get("/")
async def list_products():
    return inventory


@router.get("/{product_id}")
async def get_product(product_id: int):
    for product in inventory:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")
''')

    # app/models/__init__.py
    with open(f'{PROJECT_DIR}/app/models/__init__.py', 'w') as f:
        f.write('')

    # app/models/user.py
    with open(f'{PROJECT_DIR}/app/models/user.py', 'w') as f:
        f.write('''from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    name: str
    email: str
    role: str = "viewer"


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        from_attributes = True
''')

    # tests/test_health.py
    with open(f'{PROJECT_DIR}/tests/test_health.py', 'w') as f:
        f.write('''import pytest
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
''')

    # tests/__init__.py
    with open(f'{PROJECT_DIR}/tests/__init__.py', 'w') as f:
        f.write('')

    # README.md
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write('''# Inventory Management API

A FastAPI-based REST API for managing product inventory and user accounts.

## Setup

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API Endpoints

- `GET /health` - Health check
- `GET /api/v1/users` - List all users
- `GET /api/v1/users/{id}` - Get user by ID
- `POST /api/v1/users` - Create new user
- `GET /api/v1/products` - List all products
- `GET /api/v1/products/{id}` - Get product by ID

## Testing

```bash
pytest tests/
```
''')

    # .gitignore
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write('''__pycache__/
*.py[cod]
*.egg-info/
.env
.venv/
dist/
build/
*.db
.pytest_cache/
''')

    # pyproject.toml
    with open(f'{PROJECT_DIR}/pyproject.toml', 'w') as f:
        f.write('''[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]

[tool.black]
line-length = 100
target-version = ["py311"]
''')

    print(f'Initial project created at: {PROJECT_DIR}')

    # Verify no .devcontainer exists (the agent must create it)
    devcontainer_dir = f'{PROJECT_DIR}/.devcontainer'
    if os.path.exists(devcontainer_dir):
        import shutil
        shutil.rmtree(devcontainer_dir)
        print('Removed pre-existing .devcontainer directory')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

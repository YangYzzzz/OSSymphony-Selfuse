"""
Initial Setup: Set up code spell checking for ~/project
Task ID: vscode_wf_032
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'project')
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
    # Create project directory structure
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # --- main.py: FastAPI application entry point ---
    main_py = '''\
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import uvicorn
from models import User, Item, SessionLocal, engine, Base
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventory Management API", version="0.3.1")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserCreate(BaseModel):
    username: str
    email: str
    full_name: str


class ItemCreate(BaseModel):
    name: str
    description: str
    price: float
    quantity: int


@app.get("/")
def read_root():
    return {"message": "Welcome to the Inventory Management API"}


@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/items/")
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(
        name=item.name,
        description=item.description,
        price=item.price,
        quantity=item.quantity,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.get("/items/")
def list_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(Item).offset(skip).limit(limit).all()
    return items


@app.get("/items/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.put("/items/{item_id}")
def update_item(item_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.name = item.name
    db_item.description = item.description
    db_item.price = item.price
    db_item.quantity = item.quantity
    db.commit()
    db.refresh(db_item)
    return db_item


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
'''
    with open(os.path.join(PROJECT_DIR, 'main.py'), 'w') as f:
        f.write(main_py)

    # --- models.py: SQLAlchemy models ---
    models_py = '''\
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel, EmailStr
from datetime import datetime

DATABASE_URL = "sqlite:///./inventory.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    full_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str

    class Config:
        from_attributes = True


class ItemResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int

    class Config:
        from_attributes = True
'''
    with open(os.path.join(PROJECT_DIR, 'models.py'), 'w') as f:
        f.write(models_py)

    # --- config.py: Configuration settings ---
    config_py = '''\
import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Inventory Management API"
    debug_mode: bool = False
    database_url: str = "sqlite:///./inventory.db"
    api_version: str = "0.3.1"
    cors_origins: list = ["http://localhost:3000", "http://localhost:8080"]
    max_items_per_page: int = 100
    enable_uvicorn_reload: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
'''
    with open(os.path.join(PROJECT_DIR, 'config.py'), 'w') as f:
        f.write(config_py)

    # --- requirements.txt ---
    requirements = '''\
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.2
pydantic-settings==2.1.0
python-multipart==0.0.6
httpx==0.25.2
pytest==7.4.3
'''
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write(requirements)

    # --- README.md ---
    readme = '''\
# Inventory Management API

A lightweight FastAPI-based REST API for managing inventory items and users.

## Tech Stack

- **FastAPI** - Modern async web framework for Python
- **Pydantic** - Data validation and serialization
- **SQLAlchemy** - SQL toolkit and ORM
- **Uvicorn** - ASGI server for production deployment

## Getting Started

### Prerequisites

- Python 3.10+
- pip or poetry

### Installation

```bash
pip install -r requirements.txt
```

### Running the Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/users/` | Create a new user |
| GET | `/users/{id}` | Get user by ID |
| POST | `/items/` | Create inventory item |
| GET | `/items/` | List all items |
| GET | `/items/{id}` | Get item by ID |
| PUT | `/items/{id}` | Update an item |

## Project Structure

```
project/
  main.py          # Application entry point and routes
  models.py        # SQLAlchemy and Pydantic models
  config.py        # Configuration via pydantic-settings
  requirements.txt # Python dependencies
  tests/
    test_api.py    # API integration tests
```

## Development Notes

This project uses SQLAlchemy with SQLite for local development.
For production, switch to PostgreSQL by updating the `DATABASE_URL`
in your `.env` file or environment variables.
'''
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write(readme)

    # --- tests/test_api.py ---
    tests_dir = os.path.join(PROJECT_DIR, 'tests')
    os.makedirs(tests_dir, exist_ok=True)

    test_api = '''\
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Inventory Management API"}


def test_create_user():
    response = client.post(
        "/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "full_name": "Test User",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"


def test_create_item():
    response = client.post(
        "/items/",
        json={
            "name": "Widget A",
            "description": "A standard widget",
            "price": 19.99,
            "quantity": 150,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Widget A"
    assert data["price"] == 19.99


def test_list_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
'''
    with open(os.path.join(tests_dir, 'test_api.py'), 'w') as f:
        f.write(test_api)

    # --- __init__.py for tests ---
    with open(os.path.join(tests_dir, '__init__.py'), 'w') as f:
        f.write('')

    # Ensure NO .vscode/settings.json exists with cSpell config
    # (don't create .vscode directory at all in initial state)
    if os.path.exists(VSCODE_DIR):
        import shutil
        shutil.rmtree(VSCODE_DIR)

    # Ensure Code Spell Checker extension is NOT installed
    try:
        subprocess.run(
            ["code", "--uninstall-extension", "streetsidesoftware.code-spell-checker"],
            capture_output=True, text=True, timeout=30
        )
    except Exception:
        pass

    print(f'Initial project created: {PROJECT_DIR}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

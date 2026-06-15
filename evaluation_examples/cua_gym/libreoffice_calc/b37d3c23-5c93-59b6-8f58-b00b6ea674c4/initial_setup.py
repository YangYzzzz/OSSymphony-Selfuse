"""
Initial Setup: Configure project-specific dictionary for Code Spell Checker
Task ID: vscode_lp_095
Domain: vscode (Code Spell Checker / cspell.json)
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_095'
PROJECT_DIR = f'{WORKDIR}/workspace'

# --- Helper ---
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
    os.makedirs(f'{PROJECT_DIR}/app', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/app/routers', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/app/models', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)

    # 2. Create realistic Python backend project files

    # main.py - FastAPI application entry point
    with open(f'{PROJECT_DIR}/app/main.py', 'w') as f:
        f.write('''"""
Backend API service built with FastAPI and SQLAlchemy ORM.
Connects to a PostgreSQL database and uses Pydantic for data validation.
Deployed on Kubernetes via Helm charts.
"""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn

from app.models.database import get_db, engine, Base
from app.routers import users, projects, analytics

app = FastAPI(
    title="DevOps Dashboard API",
    description="Backend service for the DevOps monitoring dashboard",
    version="2.4.1",
)

app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(projects.router, prefix="/api/v1/projects", tags=["projects"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])


@app.on_event("startup")
async def startup_event():
    """Initialize database tables and configure Kubernetes health checks."""
    Base.metadata.create_all(bind=engine)


@app.get("/health")
async def health_check():
    """Kubernetes liveness probe endpoint."""
    return {"status": "healthy", "version": "2.4.1"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
''')

    # models/database.py - SQLAlchemy + PostgreSQL
    with open(f'{PROJECT_DIR}/app/models/__init__.py', 'w') as f:
        f.write('')

    with open(f'{PROJECT_DIR}/app/models/database.py', 'w') as f:
        f.write('''"""
Database configuration using SQLAlchemy with PostgreSQL backend.
Connection pooling is handled by SQLAlchemy's built-in pool.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://devops_user:secret@localhost:5432/dashboard_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency for FastAPI route handlers to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
''')

    # models/schemas.py - Pydantic models
    with open(f'{PROJECT_DIR}/app/models/schemas.py', 'w') as f:
        f.write('''"""
Pydantic schemas for request/response validation.
Used by FastAPI for automatic OpenAPI documentation generation.
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    department: str


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserResponse(UserBase):
    id: int
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


class ProjectBase(BaseModel):
    name: str
    repository_url: str
    kubernetes_namespace: str
    deployment_strategy: str = "rolling"


class ProjectCreate(ProjectBase):
    owner_id: int


class DeploymentStatus(BaseModel):
    project_name: str
    kubernetes_cluster: str
    replicas: int
    cpu_utilization: float
    memory_usage_mb: int
    last_deployed: datetime
''')

    # routers/users.py
    with open(f'{PROJECT_DIR}/app/routers/__init__.py', 'w') as f:
        f.write('')

    with open(f'{PROJECT_DIR}/app/routers/users.py', 'w') as f:
        f.write('''"""
User management endpoints.
Handles CRUD operations for users stored in PostgreSQL.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.database import get_db
from app.models.schemas import UserCreate, UserResponse

router = APIRouter()


@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user in the PostgreSQL database."""
    # Implementation would use SQLAlchemy to insert the user
    pass


@router.get("/", response_model=List[UserResponse])
async def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all users with pagination support."""
    pass
''')

    # routers/projects.py
    with open(f'{PROJECT_DIR}/app/routers/projects.py', 'w') as f:
        f.write('''"""
Project management endpoints.
Integrates with Kubernetes API for deployment status.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.models.database import get_db
from app.models.schemas import ProjectCreate, DeploymentStatus

router = APIRouter()


@router.get("/deployments", response_model=List[DeploymentStatus])
async def get_deployment_status():
    """Fetch current Kubernetes deployment status for all projects."""
    pass


@router.post("/deploy/{project_id}")
async def trigger_deployment(project_id: int, db: Session = Depends(get_db)):
    """Trigger a new Kubernetes deployment for the specified project."""
    pass
''')

    # routers/analytics.py
    with open(f'{PROJECT_DIR}/app/routers/analytics.py', 'w') as f:
        f.write('''"""
Analytics endpoints for monitoring and reporting.
Aggregates data from PostgreSQL and Kubernetes metrics.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


class MetricsSummary(BaseModel):
    total_deployments: int
    success_rate: float
    avg_response_time_ms: float
    active_kubernetes_pods: int


@router.get("/summary", response_model=MetricsSummary)
async def get_metrics_summary():
    """Get aggregated metrics from PostgreSQL and Kubernetes cluster."""
    pass
''')

    # tests/test_main.py
    with open(f'{PROJECT_DIR}/tests/__init__.py', 'w') as f:
        f.write('')

    with open(f'{PROJECT_DIR}/tests/test_main.py', 'w') as f:
        f.write('''"""
Test suite for the DevOps Dashboard API.
Uses FastAPI TestClient with SQLAlchemy test fixtures.
"""

import pytest
from fastapi.testclient import TestClient


def test_health_endpoint():
    """Verify the Kubernetes health probe returns correct status."""
    # client = TestClient(app)
    # response = client.get("/health")
    # assert response.status_code == 200
    pass


def test_uvicorn_config():
    """Verify uvicorn server configuration."""
    pass
''')

    # requirements.txt
    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write('''fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
pydantic==2.5.3
pydantic[email]==2.5.3
alembic==1.13.1
python-dotenv==1.0.0
httpx==0.26.0
pytest==7.4.4
''')

    # Dockerfile
    with open(f'{PROJECT_DIR}/Dockerfile', 'w') as f:
        f.write('''FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
''')

    # kubernetes/deployment.yaml
    os.makedirs(f'{PROJECT_DIR}/kubernetes', exist_ok=True)
    with open(f'{PROJECT_DIR}/kubernetes/deployment.yaml', 'w') as f:
        f.write('''apiVersion: apps/v1
kind: Deployment
metadata:
  name: devops-dashboard-api
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: devops-dashboard-api
  template:
    metadata:
      labels:
        app: devops-dashboard-api
    spec:
      containers:
        - name: api
          image: registry.internal/devops-dashboard:2.4.1
          ports:
            - containerPort: 8000
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: db-credentials
                  key: postgresql-url
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 30
          resources:
            requests:
              cpu: "250m"
              memory: "256Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
''')

    # .gitignore
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write('''__pycache__/
*.py[cod]
.env
.venv/
*.egg-info/
dist/
build/
.pytest_cache/
''')

    # 3. Ensure NO cspell.json exists (task requires agent to create it)
    cspell_path = f'{PROJECT_DIR}/cspell.json'
    if os.path.exists(cspell_path):
        os.remove(cspell_path)

    # 4. Install Code Spell Checker extension
    subprocess.run(
        ['code', '--install-extension', 'streetsidesoftware.code-spell-checker'],
        capture_output=True, text=True, timeout=60
    )
    print('Installed Code Spell Checker extension')

    # 5. Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    # Open main.py so the user sees flagged words immediately
    launch_gui(f'code "{PROJECT_DIR}/app/main.py"', delay_sec=2.0)
    print(f'Initial project created at: {PROJECT_DIR}')
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

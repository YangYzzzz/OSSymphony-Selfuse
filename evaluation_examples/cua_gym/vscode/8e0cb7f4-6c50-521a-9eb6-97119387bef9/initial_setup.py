"""
Initial Setup: Multi-root workspace with React frontend, Python backend, and infra code
Task ID: vscode_we_095
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_095'
PROJECTS = f'{WORKDIR}/projects'


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
    # ── Create project directories ──
    os.makedirs(f'{PROJECTS}/frontend/src/components', exist_ok=True)
    os.makedirs(f'{PROJECTS}/frontend/src/hooks', exist_ok=True)
    os.makedirs(f'{PROJECTS}/frontend/public', exist_ok=True)
    os.makedirs(f'{PROJECTS}/backend/app/routers', exist_ok=True)
    os.makedirs(f'{PROJECTS}/backend/app/models', exist_ok=True)
    os.makedirs(f'{PROJECTS}/backend/tests', exist_ok=True)
    os.makedirs(f'{PROJECTS}/infra/terraform/modules', exist_ok=True)
    os.makedirs(f'{PROJECTS}/infra/k8s/base', exist_ok=True)
    os.makedirs(f'{PROJECTS}/infra/k8s/overlays/staging', exist_ok=True)

    # ── Frontend files ──
    with open(f'{PROJECTS}/frontend/package.json', 'w') as f:
        json.dump({
            "name": "saas-platform-frontend",
            "version": "2.1.0",
            "private": True,
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "react-router-dom": "^6.20.1",
                "axios": "^1.6.2",
                "@tanstack/react-query": "^5.12.2",
                "tailwindcss": "^3.3.6"
            },
            "devDependencies": {
                "typescript": "^5.3.2",
                "@types/react": "^18.2.39",
                "eslint": "^8.54.0",
                "prettier": "^3.1.0",
                "vite": "^5.0.4"
            },
            "scripts": {
                "dev": "vite",
                "build": "tsc && vite build",
                "lint": "eslint src --ext .ts,.tsx",
                "format": "prettier --write 'src/**/*.{ts,tsx,css}'"
            }
        }, f, indent=2)

    with open(f'{PROJECTS}/frontend/tsconfig.json', 'w') as f:
        json.dump({
            "compilerOptions": {
                "target": "ES2020",
                "useDefineForClassFields": True,
                "lib": ["ES2020", "DOM", "DOM.Iterable"],
                "module": "ESNext",
                "skipLibCheck": True,
                "moduleResolution": "bundler",
                "allowImportingTsExtensions": True,
                "resolveJsonModule": True,
                "isolatedModules": True,
                "noEmit": True,
                "jsx": "react-jsx",
                "strict": True
            },
            "include": ["src"]
        }, f, indent=2)

    with open(f'{PROJECTS}/frontend/src/App.tsx', 'w') as f:
        f.write('''import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import UserList from './components/UserList';
import SettingsPage from './components/SettingsPage';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <nav className="bg-indigo-600 text-white p-4">
          <h1 className="text-xl font-bold">SaaS Platform</h1>
        </nav>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/users" element={<UserList />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
};

export default App;
''')

    with open(f'{PROJECTS}/frontend/src/components/Dashboard.tsx', 'w') as f:
        f.write('''import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { fetchMetrics } from '../hooks/useMetrics';

interface MetricCard {
  title: string;
  value: number;
  change: number;
}

const Dashboard: React.FC = () => {
  const { data: metrics, isLoading } = useQuery({
    queryKey: ['metrics'],
    queryFn: fetchMetrics,
  });

  if (isLoading) return <div className="p-8">Loading dashboard...</div>;

  return (
    <div className="p-8 grid grid-cols-3 gap-6">
      {metrics?.map((metric: MetricCard) => (
        <div key={metric.title} className="bg-white rounded-lg shadow p-6">
          <h3 className="text-sm text-gray-500">{metric.title}</h3>
          <p className="text-2xl font-bold mt-2">{metric.value.toLocaleString()}</p>
          <span className={metric.change >= 0 ? 'text-green-600' : 'text-red-600'}>
            {metric.change > 0 ? '+' : ''}{metric.change}%
          </span>
        </div>
      ))}
    </div>
  );
};

export default Dashboard;
''')

    with open(f'{PROJECTS}/frontend/src/hooks/useMetrics.ts', 'w') as f:
        f.write('''import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const fetchMetrics = async () => {
  const response = await axios.get(`${API_BASE}/api/v1/metrics`);
  return response.data;
};

export const fetchUserGrowth = async (period: string = '30d') => {
  const response = await axios.get(`${API_BASE}/api/v1/metrics/growth`, {
    params: { period },
  });
  return response.data;
};
''')

    # ── Backend files ──
    with open(f'{PROJECTS}/backend/requirements.txt', 'w') as f:
        f.write('''fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
alembic==1.13.0
pydantic==2.5.2
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
httpx==0.25.2
pytest==7.4.3
pytest-asyncio==0.23.2
black==23.11.0
''')

    with open(f'{PROJECTS}/backend/app/__init__.py', 'w') as f:
        f.write('')

    with open(f'{PROJECTS}/backend/app/main.py', 'w') as f:
        f.write('''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, users, metrics

app = FastAPI(
    title="SaaS Platform API",
    version="2.1.0",
    description="Backend API for the SaaS Platform"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(metrics.router, prefix="/api/v1/metrics", tags=["metrics"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "2.1.0"}
''')

    with open(f'{PROJECTS}/backend/app/routers/__init__.py', 'w') as f:
        f.write('')

    with open(f'{PROJECTS}/backend/app/routers/auth.py', 'w') as f:
        f.write('''from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr

router = APIRouter()


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    # Placeholder authentication logic
    if request.email == "admin@saasplatform.io" and request.password == "admin":
        return TokenResponse(access_token="mock-jwt-token")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials"
    )
''')

    with open(f'{PROJECTS}/backend/app/models/__init__.py', 'w') as f:
        f.write('')

    with open(f'{PROJECTS}/backend/app/models/user.py', 'w') as f:
        f.write('''from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
''')

    with open(f'{PROJECTS}/backend/tests/test_auth.py', 'w') as f:
        f.write('''import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_login_success():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/auth/login", json={
            "email": "admin@saasplatform.io",
            "password": "admin"
        })
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_failure():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/auth/login", json={
            "email": "unknown@example.com",
            "password": "wrong"
        })
    assert response.status_code == 401
''')

    with open(f'{PROJECTS}/backend/pyproject.toml', 'w') as f:
        f.write('''[tool.black]
line-length = 88
target-version = ["py311"]

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
''')

    # ── Infrastructure files ──
    with open(f'{PROJECTS}/infra/terraform/main.tf', 'w') as f:
        f.write('''terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.30"
    }
  }

  backend "s3" {
    bucket = "saas-platform-tfstate"
    key    = "infrastructure/terraform.tfstate"
    region = "us-west-2"
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "saas-platform"
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}

module "networking" {
  source      = "./modules/networking"
  environment = var.environment
  vpc_cidr    = var.vpc_cidr
}

module "database" {
  source       = "./modules/database"
  environment  = var.environment
  vpc_id       = module.networking.vpc_id
  subnet_ids   = module.networking.private_subnet_ids
  instance_class = var.db_instance_class
}
''')

    with open(f'{PROJECTS}/infra/terraform/variables.tf', 'w') as f:
        f.write('''variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-west-2"
}

variable "environment" {
  description = "Deployment environment (staging, production)"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.medium"
}
''')

    with open(f'{PROJECTS}/infra/k8s/base/deployment.yaml', 'w') as f:
        f.write('''apiVersion: apps/v1
kind: Deployment
metadata:
  name: saas-platform-api
  labels:
    app: saas-platform
    component: api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: saas-platform
      component: api
  template:
    metadata:
      labels:
        app: saas-platform
        component: api
    spec:
      containers:
        - name: api
          image: saas-platform/api:latest
          ports:
            - containerPort: 8000
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: saas-platform-secrets
                  key: database-url
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 5
''')

    with open(f'{PROJECTS}/infra/k8s/base/service.yaml', 'w') as f:
        f.write('''apiVersion: v1
kind: Service
metadata:
  name: saas-platform-api
  labels:
    app: saas-platform
spec:
  type: ClusterIP
  ports:
    - port: 80
      targetPort: 8000
      protocol: TCP
  selector:
    app: saas-platform
    component: api
''')

    with open(f'{PROJECTS}/infra/k8s/overlays/staging/kustomization.yaml', 'w') as f:
        f.write('''apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - ../../base
namePrefix: staging-
commonLabels:
  environment: staging
patchesStrategicMerge:
  - replica-patch.yaml
''')

    with open(f'{PROJECTS}/infra/k8s/overlays/staging/replica-patch.yaml', 'w') as f:
        f.write('''apiVersion: apps/v1
kind: Deployment
metadata:
  name: saas-platform-api
spec:
  replicas: 1
''')

    # ── Workspace file (initial state: empty settings, NO .vscode folders) ──
    workspace = {
        "folders": [
            {"path": "frontend"},
            {"path": "backend"},
            {"path": "infra"}
        ],
        "settings": {}
    }
    with open(f'{PROJECTS}/saas-platform.code-workspace', 'w') as f:
        json.dump(workspace, f, indent=4)

    print(f'Initial workspace created at {PROJECTS}/saas-platform.code-workspace')

    # ── Launch VSCode with workspace ──
    launch_gui(f'code "{PROJECTS}/saas-platform.code-workspace"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with workspace')


create_initial()

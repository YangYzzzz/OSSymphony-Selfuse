"""
Initial Setup: Create monorepo structure for fullstack-app CI pipeline task
Task ID: vscode_gf3_083
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_083'
PROJECT_ROOT = f'{WORKDIR}/projects/fullstack-app'


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
    # ============================================================
    # 1. Create monorepo directory structure
    # ============================================================
    dirs = [
        f'{PROJECT_ROOT}/.github',  # .github exists but NO workflows dir
        f'{PROJECT_ROOT}/frontend/src/components',
        f'{PROJECT_ROOT}/frontend/src/pages',
        f'{PROJECT_ROOT}/frontend/src/utils',
        f'{PROJECT_ROOT}/frontend/tests',
        f'{PROJECT_ROOT}/frontend/public',
        f'{PROJECT_ROOT}/backend/app/api',
        f'{PROJECT_ROOT}/backend/app/models',
        f'{PROJECT_ROOT}/backend/app/services',
        f'{PROJECT_ROOT}/backend/tests',
        f'{PROJECT_ROOT}/backend/migrations',
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # ============================================================
    # 2. Frontend files
    # ============================================================

    # package.json
    package_json = {
        "name": "fullstack-app-frontend",
        "version": "1.2.0",
        "private": True,
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "jest --coverage",
            "lint": "eslint src/ --ext .js,.jsx,.ts,.tsx",
            "format:check": "prettier --check \"src/**/*.{js,jsx,ts,tsx,css,json}\""
        },
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.20.1",
            "axios": "^1.6.2",
            "@tanstack/react-query": "^5.12.2"
        },
        "devDependencies": {
            "eslint": "^8.55.0",
            "prettier": "^3.1.0",
            "jest": "^29.7.0",
            "@testing-library/react": "^14.1.2",
            "@testing-library/jest-dom": "^6.1.4",
            "@playwright/test": "^1.40.1",
            "typescript": "^5.3.2"
        }
    }
    with open(f'{PROJECT_ROOT}/frontend/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # .eslintrc.json
    eslintrc = {
        "env": {"browser": True, "es2021": True, "jest": True},
        "extends": ["eslint:recommended", "plugin:react/recommended"],
        "parserOptions": {"ecmaVersion": "latest", "sourceType": "module"},
        "rules": {
            "no-unused-vars": "warn",
            "react/prop-types": "off"
        }
    }
    with open(f'{PROJECT_ROOT}/frontend/.eslintrc.json', 'w') as f:
        json.dump(eslintrc, f, indent=2)

    # .prettierrc
    prettierrc = {
        "semi": True,
        "singleQuote": True,
        "tabWidth": 2,
        "trailingComma": "es5",
        "printWidth": 100
    }
    with open(f'{PROJECT_ROOT}/frontend/.prettierrc', 'w') as f:
        json.dump(prettierrc, f, indent=2)

    # Frontend source files
    with open(f'{PROJECT_ROOT}/frontend/src/App.jsx', 'w') as f:
        f.write("""import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import UserProfile from './pages/UserProfile';
import OrderHistory from './pages/OrderHistory';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/profile" element={<UserProfile />} />
        <Route path="/orders" element={<OrderHistory />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
""")

    with open(f'{PROJECT_ROOT}/frontend/src/pages/Dashboard.jsx', 'w') as f:
        f.write("""import React, { useEffect, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { fetchMetrics } from '../utils/api';
import MetricsCard from '../components/MetricsCard';

export default function Dashboard() {
  const { data: metrics, isLoading } = useQuery({
    queryKey: ['metrics'],
    queryFn: fetchMetrics,
  });

  if (isLoading) return <div className="loading-spinner">Loading...</div>;

  return (
    <div className="dashboard-container">
      <h1>Sales Dashboard</h1>
      <div className="metrics-grid">
        {metrics?.map((m) => (
          <MetricsCard key={m.id} title={m.title} value={m.value} trend={m.trend} />
        ))}
      </div>
    </div>
  );
}
""")

    with open(f'{PROJECT_ROOT}/frontend/src/pages/UserProfile.jsx', 'w') as f:
        f.write("""import React from 'react';

export default function UserProfile() {
  return (
    <div className="profile-page">
      <h1>User Profile</h1>
      <p>Manage your account settings and preferences.</p>
    </div>
  );
}
""")

    with open(f'{PROJECT_ROOT}/frontend/src/pages/OrderHistory.jsx', 'w') as f:
        f.write("""import React from 'react';

export default function OrderHistory() {
  return (
    <div className="orders-page">
      <h1>Order History</h1>
    </div>
  );
}
""")

    with open(f'{PROJECT_ROOT}/frontend/src/components/MetricsCard.jsx', 'w') as f:
        f.write("""import React from 'react';

export default function MetricsCard({ title, value, trend }) {
  const trendColor = trend >= 0 ? 'green' : 'red';
  return (
    <div className="metrics-card">
      <h3>{title}</h3>
      <span className="value">${value.toLocaleString()}</span>
      <span style={{ color: trendColor }}>{trend > 0 ? '+' : ''}{trend}%</span>
    </div>
  );
}
""")

    with open(f'{PROJECT_ROOT}/frontend/src/utils/api.js', 'w') as f:
        f.write("""import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

export async function fetchMetrics() {
  const { data } = await axios.get(`${API_BASE}/metrics`);
  return data;
}

export async function fetchOrders(page = 1) {
  const { data } = await axios.get(`${API_BASE}/orders?page=${page}`);
  return data;
}

export async function updateProfile(profileData) {
  const { data } = await axios.put(`${API_BASE}/profile`, profileData);
  return data;
}
""")

    # Frontend test file
    with open(f'{PROJECT_ROOT}/frontend/tests/Dashboard.test.jsx', 'w') as f:
        f.write("""import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Dashboard from '../src/pages/Dashboard';

const queryClient = new QueryClient({
  defaultOptions: { queries: { retry: false } },
});

function renderWithProviders(ui) {
  return render(
    <QueryClientProvider client={queryClient}>{ui}</QueryClientProvider>
  );
}

test('renders dashboard heading', async () => {
  renderWithProviders(<Dashboard />);
  expect(screen.getByText('Sales Dashboard')).toBeInTheDocument();
});

test('shows loading spinner initially', () => {
  renderWithProviders(<Dashboard />);
  expect(screen.getByText('Loading...')).toBeInTheDocument();
});
""")

    # ============================================================
    # 3. Backend files
    # ============================================================

    # requirements.txt
    with open(f'{PROJECT_ROOT}/backend/requirements.txt', 'w') as f:
        f.write("""fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
alembic==1.13.0
pydantic==2.5.2
python-dotenv==1.0.0
httpx==0.25.2
pytest==7.4.3
pytest-asyncio==0.23.2
flake8==6.1.0
black==23.12.0
""")

    # Backend app files
    with open(f'{PROJECT_ROOT}/backend/app/__init__.py', 'w') as f:
        f.write("")

    with open(f'{PROJECT_ROOT}/backend/app/main.py', 'w') as f:
        f.write("""from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import metrics, orders, users

app = FastAPI(title="Fullstack App API", version="1.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(metrics.router, prefix="/api/metrics", tags=["metrics"])
app.include_router(orders.router, prefix="/api/orders", tags=["orders"])
app.include_router(users.router, prefix="/api/users", tags=["users"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.2.0"}
""")

    with open(f'{PROJECT_ROOT}/backend/app/api/__init__.py', 'w') as f:
        f.write("")

    with open(f'{PROJECT_ROOT}/backend/app/api/metrics.py', 'w') as f:
        f.write("""from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.database import get_db

router = APIRouter()


@router.get("/")
async def get_metrics(db: Session = Depends(get_db)):
    return [
        {"id": 1, "title": "Revenue", "value": 142580, "trend": 12.5},
        {"id": 2, "title": "Orders", "value": 1834, "trend": 8.3},
        {"id": 3, "title": "Customers", "value": 9421, "trend": -2.1},
        {"id": 4, "title": "Avg Order Value", "value": 77.73, "trend": 3.8},
    ]
""")

    with open(f'{PROJECT_ROOT}/backend/app/api/orders.py', 'w') as f:
        f.write("""from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.models.database import get_db

router = APIRouter()


@router.get("/")
async def get_orders(page: int = Query(1, ge=1), db: Session = Depends(get_db)):
    return {"page": page, "total": 156, "orders": []}
""")

    with open(f'{PROJECT_ROOT}/backend/app/api/users.py', 'w') as f:
        f.write("""from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.database import get_db

router = APIRouter()


@router.get("/profile")
async def get_profile(db: Session = Depends(get_db)):
    return {"name": "Sarah Chen", "email": "sarah.chen@example.com", "role": "admin"}
""")

    with open(f'{PROJECT_ROOT}/backend/app/models/__init__.py', 'w') as f:
        f.write("")

    with open(f'{PROJECT_ROOT}/backend/app/models/database.py', 'w') as f:
        f.write("""import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://app:secret@localhost:5432/fullstack_app")

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

    with open(f'{PROJECT_ROOT}/backend/app/models/order.py', 'w') as f:
        f.write("""from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.models.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(255), nullable=False)
    product = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String(50), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
""")

    with open(f'{PROJECT_ROOT}/backend/app/services/__init__.py', 'w') as f:
        f.write("")

    with open(f'{PROJECT_ROOT}/backend/app/services/order_service.py', 'w') as f:
        f.write("""from sqlalchemy.orm import Session
from app.models.order import Order


def get_recent_orders(db: Session, limit: int = 20):
    return db.query(Order).order_by(Order.created_at.desc()).limit(limit).all()


def calculate_revenue(db: Session) -> float:
    from sqlalchemy import func
    result = db.query(func.sum(Order.amount)).filter(Order.status == "completed").scalar()
    return result or 0.0
""")

    # Backend test files
    with open(f'{PROJECT_ROOT}/backend/tests/__init__.py', 'w') as f:
        f.write("")

    with open(f'{PROJECT_ROOT}/backend/tests/test_health.py', 'w') as f:
        f.write("""import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_health_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
""")

    with open(f'{PROJECT_ROOT}/backend/tests/test_metrics.py', 'w') as f:
        f.write("""import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_metrics_returns_list():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/metrics/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "title" in data[0]
    assert "value" in data[0]
""")

    # pyproject.toml for black config
    with open(f'{PROJECT_ROOT}/backend/pyproject.toml', 'w') as f:
        f.write("""[tool.black]
line-length = 100
target-version = ["py311"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
""")

    # ============================================================
    # 4. Root-level files
    # ============================================================

    with open(f'{PROJECT_ROOT}/README.md', 'w') as f:
        f.write("""# Fullstack App

A monorepo containing a React frontend and FastAPI backend for the sales dashboard application.

## Project Structure

```
fullstack-app/
  frontend/     # React 18 + TypeScript SPA
  backend/      # FastAPI + SQLAlchemy REST API
  .github/      # GitHub configuration
```

## Getting Started

### Frontend
```bash
cd frontend && npm install && npm start
```

### Backend
```bash
cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload
```

## Team

- **Sarah Chen** — Tech Lead
- **Marcus Johnson** — Frontend Engineer
- **Priya Patel** — Backend Engineer
- **David Kim** — DevOps
""")

    # .gitignore
    with open(f'{PROJECT_ROOT}/.gitignore', 'w') as f:
        f.write("""node_modules/
__pycache__/
*.pyc
.env
dist/
build/
coverage/
.pytest_cache/
*.egg-info/
""")

    print(f'Monorepo structure created at: {PROJECT_ROOT}')

    # ============================================================
    # 5. GUI-ready startup: open VSCode with the project
    # ============================================================
    launch_gui(f'code "{PROJECT_ROOT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

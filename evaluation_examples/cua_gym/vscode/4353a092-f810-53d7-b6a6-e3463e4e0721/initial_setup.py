"""
Initial Setup: Full-stack workspace configuration for React/TypeScript + FastAPI
Task ID: vscode_wf_035
Domain: vscode

Creates ~/frontend (React/TypeScript project) and ~/backend (FastAPI project).
No workspace file or launch configurations exist yet.
Opens VSCode with the home directory.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_035'

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

def create_frontend():
    """Create ~/frontend with a React TypeScript project structure."""
    frontend = os.path.join(WORKDIR, 'frontend')
    src = os.path.join(frontend, 'src')
    public = os.path.join(frontend, 'public')
    os.makedirs(src, exist_ok=True)
    os.makedirs(public, exist_ok=True)

    # package.json
    package = {
        "name": "inventory-dashboard",
        "version": "1.2.0",
        "private": True,
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-scripts": "5.0.1",
            "typescript": "^5.3.3",
            "axios": "^1.6.5",
            "@types/react": "^18.2.48",
            "@types/react-dom": "^18.2.18"
        },
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test",
            "eject": "react-scripts eject"
        },
        "browserslist": {
            "production": [">0.2%", "not dead", "not op_mini all"],
            "development": ["last 1 chrome version", "last 1 firefox version"]
        }
    }
    with open(os.path.join(frontend, 'package.json'), 'w') as f:
        json.dump(package, f, indent=2)

    # tsconfig.json
    tsconfig = {
        "compilerOptions": {
            "target": "es5",
            "lib": ["dom", "dom.iterable", "esnext"],
            "allowJs": True,
            "skipLibCheck": True,
            "esModuleInterop": True,
            "allowSyntheticDefaultImports": True,
            "strict": True,
            "forceConsistentCasingInFileNames": True,
            "noFallthroughCasesInSwitch": True,
            "module": "esnext",
            "moduleResolution": "node",
            "resolveJsonModule": True,
            "isolatedModules": True,
            "noEmit": True,
            "jsx": "react-jsx"
        },
        "include": ["src"]
    }
    with open(os.path.join(frontend, 'tsconfig.json'), 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # src/index.tsx
    index_tsx = '''import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
'''
    with open(os.path.join(src, 'index.tsx'), 'w') as f:
        f.write(index_tsx)

    # src/App.tsx
    app_tsx = '''import React, { useEffect, useState } from 'react';

interface InventoryItem {
  id: number;
  name: string;
  sku: string;
  quantity: number;
  price: number;
  category: string;
}

const App: React.FC = () => {
  const [items, setItems] = useState<InventoryItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetch('/api/inventory')
      .then(res => res.json())
      .then(data => {
        setItems(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to fetch inventory:', err);
        setLoading(false);
      });
  }, []);

  const totalValue = items.reduce(
    (sum, item) => sum + item.quantity * item.price, 0
  );

  if (loading) {
    return <div className="loading">Loading inventory data...</div>;
  }

  return (
    <div className="app">
      <header>
        <h1>Inventory Dashboard</h1>
        <p>Total Value: ${totalValue.toLocaleString()}</p>
      </header>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>SKU</th>
            <th>Qty</th>
            <th>Price</th>
            <th>Category</th>
          </tr>
        </thead>
        <tbody>
          {items.map(item => (
            <tr key={item.id}>
              <td>{item.name}</td>
              <td>{item.sku}</td>
              <td>{item.quantity}</td>
              <td>${item.price.toFixed(2)}</td>
              <td>{item.category}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default App;
'''
    with open(os.path.join(src, 'App.tsx'), 'w') as f:
        f.write(app_tsx)

    # src/types.ts
    types_ts = '''export interface InventoryItem {
  id: number;
  name: string;
  sku: string;
  quantity: number;
  price: number;
  category: string;
  warehouse: string;
  lastRestocked: string;
}

export interface ApiResponse<T> {
  data: T;
  total: number;
  page: number;
  pageSize: number;
}

export type SortDirection = 'asc' | 'desc';

export interface SortConfig {
  key: keyof InventoryItem;
  direction: SortDirection;
}
'''
    with open(os.path.join(src, 'types.ts'), 'w') as f:
        f.write(types_ts)

    # public/index.html
    index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Inventory Dashboard</title>
</head>
<body>
  <div id="root"></div>
</body>
</html>
'''
    with open(os.path.join(public, 'index.html'), 'w') as f:
        f.write(index_html)

    print(f'Frontend project created at {frontend}')


def create_backend():
    """Create ~/backend with a FastAPI project structure."""
    backend = os.path.join(WORKDIR, 'backend')
    os.makedirs(backend, exist_ok=True)

    # requirements.txt
    requirements = """fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
sqlalchemy==2.0.25
python-dotenv==1.0.0
debugpy==1.8.0
"""
    with open(os.path.join(backend, 'requirements.txt'), 'w') as f:
        f.write(requirements)

    # main.py
    main_py = '''"""
Inventory Management API
FastAPI backend for the inventory dashboard.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Inventory Management API",
    description="Backend API for tracking warehouse inventory",
    version="1.2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class InventoryItem(BaseModel):
    id: int
    name: str
    sku: str
    quantity: int
    price: float
    category: str


# In-memory store for demo purposes
inventory_db: List[InventoryItem] = [
    InventoryItem(id=1, name="Wireless Mouse", sku="WM-1001", quantity=150, price=29.99, category="Electronics"),
    InventoryItem(id=2, name="USB-C Hub", sku="UH-2034", quantity=85, price=49.99, category="Electronics"),
    InventoryItem(id=3, name="Standing Desk Mat", sku="SD-3021", quantity=200, price=34.50, category="Furniture"),
    InventoryItem(id=4, name="Mechanical Keyboard", sku="MK-4055", quantity=62, price=89.99, category="Electronics"),
    InventoryItem(id=5, name="Monitor Arm", sku="MA-5012", quantity=43, price=119.00, category="Furniture"),
    InventoryItem(id=6, name="Webcam HD", sku="WC-6008", quantity=95, price=59.99, category="Electronics"),
    InventoryItem(id=7, name="Desk Organizer", sku="DO-7044", quantity=310, price=18.75, category="Office"),
    InventoryItem(id=8, name="Noise Cancelling Headphones", sku="NC-8019", quantity=28, price=199.99, category="Electronics"),
]


@app.get("/api/inventory", response_model=List[InventoryItem])
def get_inventory(category: Optional[str] = None):
    if category:
        return [item for item in inventory_db if item.category.lower() == category.lower()]
    return inventory_db


@app.get("/api/inventory/{item_id}", response_model=InventoryItem)
def get_item(item_id: int):
    for item in inventory_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")


@app.post("/api/inventory", response_model=InventoryItem)
def create_item(item: InventoryItem):
    inventory_db.append(item)
    return item


@app.get("/health")
def health_check():
    return {"status": "healthy", "items_count": len(inventory_db)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
    with open(os.path.join(backend, 'main.py'), 'w') as f:
        f.write(main_py)

    # models.py
    models_py = '''"""Database models for inventory management."""

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class InventoryRecord(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    sku = Column(String, unique=True, nullable=False)
    quantity = Column(Integer, default=0)
    price = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    warehouse = Column(String, default="main")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
'''
    with open(os.path.join(backend, 'models.py'), 'w') as f:
        f.write(models_py)

    # config.py
    config_py = '''"""Application configuration."""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = "Inventory Management API"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./inventory.db")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    CORS_ORIGINS: list = ["http://localhost:3000"]
    API_VERSION: str = "1.2.0"


settings = Settings()
'''
    with open(os.path.join(backend, 'config.py'), 'w') as f:
        f.write(config_py)

    print(f'Backend project created at {backend}')


def create_initial():
    """Create both projects and open VSCode."""
    create_frontend()
    create_backend()

    # Ensure no workspace file or launch config exists
    workspace_path = os.path.join(WORKDIR, 'fullstack.code-workspace')
    if os.path.exists(workspace_path):
        os.remove(workspace_path)

    # Remove any existing .vscode directories in both projects
    for proj in ['frontend', 'backend']:
        vscode_dir = os.path.join(WORKDIR, proj, '.vscode')
        if os.path.exists(vscode_dir):
            import shutil
            shutil.rmtree(vscode_dir)

    # Launch VSCode with the home directory
    launch_gui(f'code "{WORKDIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

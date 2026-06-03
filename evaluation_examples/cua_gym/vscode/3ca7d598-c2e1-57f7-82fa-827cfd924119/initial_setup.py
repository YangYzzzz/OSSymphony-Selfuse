"""
Initial Setup: Multi-container debugging scenario for microservices
Task ID: vscode_gf2_048
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf2_048'
PROJECT_DIR = f'{WORKDIR}/projects/microservices'


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
    # ── Python backend service ──
    py_dir = os.path.join(PROJECT_DIR, 'python-service')
    os.makedirs(py_dir, exist_ok=True)

    with open(os.path.join(py_dir, 'app.py'), 'w') as f:
        f.write('''\
"""
Order Processing Service — Python / Flask
Handles order creation, validation, and fulfillment tracking.
"""

from flask import Flask, request, jsonify
import logging
from datetime import datetime

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("order-service")

orders_db = {}
next_order_id = 1000


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "order-processing", "timestamp": datetime.utcnow().isoformat()})


@app.route("/orders", methods=["POST"])
def create_order():
    global next_order_id
    data = request.get_json()
    if not data or "items" not in data:
        return jsonify({"error": "Missing items in request body"}), 400

    order_id = f"ORD-{next_order_id}"
    next_order_id += 1

    order = {
        "order_id": order_id,
        "customer_id": data.get("customer_id", "anonymous"),
        "items": data["items"],
        "total": sum(item.get("price", 0) * item.get("quantity", 1) for item in data["items"]),
        "status": "pending",
        "created_at": datetime.utcnow().isoformat(),
    }
    orders_db[order_id] = order
    logger.info(f"Created order {order_id} for customer {order['customer_id']}")
    return jsonify(order), 201


@app.route("/orders/<order_id>", methods=["GET"])
def get_order(order_id):
    order = orders_db.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(order)


@app.route("/orders/<order_id>/fulfill", methods=["POST"])
def fulfill_order(order_id):
    order = orders_db.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    order["status"] = "fulfilled"
    order["fulfilled_at"] = datetime.utcnow().isoformat()
    logger.info(f"Fulfilled order {order_id}")
    return jsonify(order)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
''')

    with open(os.path.join(py_dir, 'requirements.txt'), 'w') as f:
        f.write('''\
flask==3.0.0
debugpy==1.8.1
gunicorn==21.2.0
requests==2.31.0
''')

    with open(os.path.join(py_dir, 'Dockerfile'), 'w') as f:
        f.write('''\
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080 5678
CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "--wait-for-client", "app.py"]
''')

    # ── Node.js middleware service ──
    node_dir = os.path.join(PROJECT_DIR, 'node-service')
    os.makedirs(node_dir, exist_ok=True)

    with open(os.path.join(node_dir, 'server.js'), 'w') as f:
        f.write('''\
/**
 * API Gateway / Middleware Service — Node.js / Express
 * Routes requests between the frontend and backend services,
 * handles authentication tokens and rate limiting.
 */

const express = require("express");
const cors = require("cors");
const axios = require("axios");

const app = express();
const PORT = 4000;
const PYTHON_SERVICE_URL = process.env.PYTHON_SERVICE_URL || "http://python-service:8080";

app.use(cors());
app.use(express.json());

// Simple in-memory rate limiter
const rateLimitMap = new Map();

function rateLimit(req, res, next) {
  const clientIp = req.ip;
  const now = Date.now();
  const windowMs = 60000;
  const maxRequests = 100;

  if (!rateLimitMap.has(clientIp)) {
    rateLimitMap.set(clientIp, []);
  }

  const timestamps = rateLimitMap.get(clientIp).filter((t) => now - t < windowMs);
  if (timestamps.length >= maxRequests) {
    return res.status(429).json({ error: "Too many requests" });
  }

  timestamps.push(now);
  rateLimitMap.set(clientIp, timestamps);
  next();
}

app.use(rateLimit);

app.get("/api/health", async (req, res) => {
  try {
    const backendHealth = await axios.get(`${PYTHON_SERVICE_URL}/health`);
    res.json({
      gateway: "healthy",
      backend: backendHealth.data,
    });
  } catch (err) {
    res.json({ gateway: "healthy", backend: "unreachable" });
  }
});

app.post("/api/orders", async (req, res) => {
  try {
    const response = await axios.post(`${PYTHON_SERVICE_URL}/orders`, req.body);
    res.status(response.status).json(response.data);
  } catch (err) {
    const status = err.response?.status || 500;
    res.status(status).json(err.response?.data || { error: "Internal gateway error" });
  }
});

app.get("/api/orders/:orderId", async (req, res) => {
  try {
    const response = await axios.get(`${PYTHON_SERVICE_URL}/orders/${req.params.orderId}`);
    res.json(response.data);
  } catch (err) {
    const status = err.response?.status || 500;
    res.status(status).json(err.response?.data || { error: "Internal gateway error" });
  }
});

app.listen(PORT, () => {
  console.log(`API Gateway listening on port ${PORT}`);
});
''')

    with open(os.path.join(node_dir, 'package.json'), 'w') as f:
        f.write(json.dumps({
            "name": "api-gateway",
            "version": "1.0.0",
            "description": "API Gateway middleware for microservices architecture",
            "main": "server.js",
            "scripts": {
                "start": "node server.js",
                "debug": "node --inspect=0.0.0.0:9229 server.js",
                "test": "jest --coverage"
            },
            "dependencies": {
                "express": "^4.18.2",
                "cors": "^2.8.5",
                "axios": "^1.6.2"
            },
            "devDependencies": {
                "jest": "^29.7.0"
            }
        }, indent=2))

    with open(os.path.join(node_dir, 'Dockerfile'), 'w') as f:
        f.write('''\
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 4000 9229
CMD ["node", "--inspect=0.0.0.0:9229", "server.js"]
''')

    # ── React frontend ──
    frontend_dir = os.path.join(PROJECT_DIR, 'frontend')
    src_dir = os.path.join(frontend_dir, 'src')
    os.makedirs(src_dir, exist_ok=True)

    with open(os.path.join(frontend_dir, 'package.json'), 'w') as f:
        f.write(json.dumps({
            "name": "microservices-dashboard",
            "version": "0.1.0",
            "private": True,
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "react-scripts": "5.0.1",
                "axios": "^1.6.2"
            },
            "scripts": {
                "start": "react-scripts start",
                "build": "react-scripts build",
                "test": "react-scripts test"
            },
            "browserslist": {
                "production": [">0.2%", "not dead", "not op_mini all"],
                "development": ["last 1 chrome version", "last 1 firefox version"]
            }
        }, indent=2))

    with open(os.path.join(src_dir, 'App.js'), 'w') as f:
        f.write('''\
import React, { useState, useEffect } from "react";
import axios from "axios";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:4000/api";

function OrderDashboard() {
  const [orders, setOrders] = useState([]);
  const [healthStatus, setHealthStatus] = useState(null);
  const [newOrder, setNewOrder] = useState({ customer_id: "", items: [] });

  useEffect(() => {
    checkHealth();
  }, []);

  async function checkHealth() {
    try {
      const response = await axios.get(`${API_BASE}/health`);
      setHealthStatus(response.data);
    } catch (err) {
      setHealthStatus({ gateway: "unreachable", backend: "unknown" });
    }
  }

  async function submitOrder() {
    try {
      const response = await axios.post(`${API_BASE}/orders`, newOrder);
      setOrders([...orders, response.data]);
      setNewOrder({ customer_id: "", items: [] });
    } catch (err) {
      console.error("Failed to create order:", err);
    }
  }

  return (
    <div className="dashboard">
      <h1>Microservices Order Dashboard</h1>
      <section className="health-panel">
        <h2>Service Health</h2>
        {healthStatus ? (
          <pre>{JSON.stringify(healthStatus, null, 2)}</pre>
        ) : (
          <p>Checking services...</p>
        )}
      </section>
      <section className="order-form">
        <h2>Create Order</h2>
        <input
          placeholder="Customer ID"
          value={newOrder.customer_id}
          onChange={(e) => setNewOrder({ ...newOrder, customer_id: e.target.value })}
        />
        <button onClick={submitOrder}>Submit Order</button>
      </section>
      <section className="orders-list">
        <h2>Recent Orders</h2>
        {orders.map((order) => (
          <div key={order.order_id} className="order-card">
            <strong>{order.order_id}</strong> — {order.status} — ${order.total}
          </div>
        ))}
      </section>
    </div>
  );
}

export default function App() {
  return <OrderDashboard />;
}
''')

    with open(os.path.join(src_dir, 'index.js'), 'w') as f:
        f.write('''\
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
''')

    with open(os.path.join(frontend_dir, 'Dockerfile'), 'w') as f:
        f.write('''\
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
''')

    # ── docker-compose.yml at project root ──
    with open(os.path.join(PROJECT_DIR, 'docker-compose.yml'), 'w') as f:
        f.write('''\
version: "3.8"

services:
  python-service:
    build: ./python-service
    ports:
      - "8080:8080"
      - "5678:5678"
    environment:
      - FLASK_ENV=development
    volumes:
      - ./python-service:/app
    networks:
      - microservices-net

  node-service:
    build: ./node-service
    ports:
      - "4000:4000"
      - "9229:9229"
    environment:
      - PYTHON_SERVICE_URL=http://python-service:8080
    depends_on:
      - python-service
    volumes:
      - ./node-service:/app
    networks:
      - microservices-net

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:4000/api
    depends_on:
      - node-service
    volumes:
      - ./frontend:/app
    networks:
      - microservices-net

networks:
  microservices-net:
    driver: bridge
''')

    # ── .vscode directory exists but NO launch.json ──
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    os.makedirs(vscode_dir, exist_ok=True)

    # Only create a basic settings.json (no launch.json!)
    with open(os.path.join(vscode_dir, 'settings.json'), 'w') as f:
        json.dump({
            "editor.tabSize": 2,
            "editor.formatOnSave": True,
            "files.exclude": {
                "**/__pycache__": True,
                "**/node_modules": True
            },
            "python.defaultInterpreterPath": "/usr/bin/python3"
        }, f, indent=4)

    # ── README.md for the project ──
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write('''\
# Microservices Order Platform

A multi-service architecture consisting of:

- **python-service**: Order processing backend (Flask, port 8080, debugpy on 5678)
- **node-service**: API Gateway middleware (Express, port 4000, inspect on 9229)
- **frontend**: React dashboard (port 3000)

## Development

```bash
docker-compose up --build
```

## Debugging

Configure VSCode compound launch configuration to attach to all three
services simultaneously for full-stack debugging.
''')

    print(f'Project structure created at {PROJECT_DIR}')

    # ── GUI-ready: open VSCode with the project folder ──
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

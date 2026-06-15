"""
Initial Setup: Create a project with inconsistently formatted files, no formatting tools configured.
Task ID: vscode_wf_086
Domain: libreoffice_calc (actually VSCode workflow)
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_086'
PROJECT_DIR = os.path.join(WORKDIR, 'project')


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


def create_project_files():
    """Create 30+ files with inconsistent formatting in ~/project."""
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'components'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'utils'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'services'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'models'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'tests'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'config'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'scripts'), exist_ok=True)

    files = {}

    # --- src/index.js (tabs, double quotes, no semicolons) ---
    files['src/index.js'] = '''const express = require("express")
const app = express()
const config = require("./config")
const userRoutes = require("./routes/users")
const productRoutes = require("./routes/products")

app.use(express.json())
app.use("/api/users", userRoutes)
app.use("/api/products", productRoutes)

const PORT = process.env.PORT || 3000
app.listen(PORT, () => {
\tconsole.log("Server running on port " + PORT)
})
'''

    # --- src/app.ts (spaces=4, single quotes, semicolons) ---
    files['src/app.ts'] = """import { Application } from 'express';
import { DatabaseConnection } from './services/database';
import { Logger } from './utils/logger';

export class App {
    private db: DatabaseConnection;
    private logger: Logger;

    constructor() {
        this.db = new DatabaseConnection('postgresql://localhost:5432/mydb');
        this.logger = new Logger('app');
    }

    async initialize(): Promise<void> {
        await this.db.connect();
        this.logger.info('Application initialized successfully');
    }

    async shutdown(): Promise<void> {
        await this.db.disconnect();
        this.logger.info('Application shut down');
    }
}
"""

    # --- src/components/Header.jsx (spaces=2, mixed quotes) ---
    files['src/components/Header.jsx'] = '''import React from "react"
import PropTypes from 'prop-types'

const Header = ({ title, subtitle, showLogo }) => {
  return (
    <header className="main-header">
      <div className='logo-container'>
        {showLogo && <img src="/logo.png" alt="Company Logo" />}
      </div>
      <h1>{title}</h1>
      {subtitle && <p className="subtitle">{subtitle}</p>}
      <nav>
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/about">About</a></li>
          <li><a href='/contact'>Contact</a></li>
        </ul>
      </nav>
    </header>
  )
}

Header.propTypes = {
  title: PropTypes.string.isRequired,
  subtitle: PropTypes.string,
  showLogo: PropTypes.bool
}

export default Header
'''

    # --- src/components/Footer.tsx (tabs, double quotes, semicolons) ---
    files['src/components/Footer.tsx'] = '''import React from "react";

interface FooterProps {
\tcompanyName: string;
\tyear: number;
\tlinks: Array<{ label: string; url: string }>;
}

const Footer: React.FC<FooterProps> = ({ companyName, year, links }) => {
\treturn (
\t\t<footer className="site-footer">
\t\t\t<div className="footer-content">
\t\t\t\t<p>&copy; {year} {companyName}. All rights reserved.</p>
\t\t\t\t<ul className="footer-links">
\t\t\t\t\t{links.map((link, index) => (
\t\t\t\t\t\t<li key={index}>
\t\t\t\t\t\t\t<a href={link.url}>{link.label}</a>
\t\t\t\t\t\t</li>
\t\t\t\t\t))}
\t\t\t\t</ul>
\t\t\t</div>
\t\t</footer>
\t);
};

export default Footer;
'''

    # --- src/components/Sidebar.jsx (spaces=4, no semicolons, single quotes) ---
    files['src/components/Sidebar.jsx'] = """import React, { useState } from 'react'

const Sidebar = ({ items, onSelect, defaultOpen }) => {
    const [isOpen, setIsOpen] = useState(defaultOpen || false)
    const [activeItem, setActiveItem] = useState(null)

    const handleSelect = (item) => {
        setActiveItem(item.id)
        onSelect(item)
    }

    return (
        <aside className={`sidebar ${isOpen ? 'open' : 'closed'}`}>
            <button onClick={() => setIsOpen(!isOpen)}>
                {isOpen ? 'Collapse' : 'Expand'}
            </button>
            <ul>
                {items.map(item => (
                    <li
                        key={item.id}
                        className={activeItem === item.id ? 'active' : ''}
                        onClick={() => handleSelect(item)}
                    >
                        {item.label}
                    </li>
                ))}
            </ul>
        </aside>
    )
}

export default Sidebar
"""

    # --- src/components/Modal.tsx (spaces=2, double quotes, semicolons) ---
    files['src/components/Modal.tsx'] = '''import React, { useEffect, useRef } from "react";

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}

const Modal: React.FC<ModalProps> = ({ isOpen, onClose, title, children }) => {
  const overlayRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    if (isOpen) {
      document.addEventListener("keydown", handleEscape);
    }
    return () => document.removeEventListener("keydown", handleEscape);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" ref={overlayRef} onClick={(e) => {
      if (e.target === overlayRef.current) onClose();
    }}>
      <div className="modal-content">
        <div className="modal-header">
          <h2>{title}</h2>
          <button onClick={onClose}>&times;</button>
        </div>
        <div className="modal-body">{children}</div>
      </div>
    </div>
  );
};

export default Modal;
'''

    # --- src/utils/logger.js (tabs, double quotes) ---
    files['src/utils/logger.js'] = '''const fs = require("fs")
const path = require("path")

class Logger {
\tconstructor(name, logDir) {
\t\tthis.name = name
\t\tthis.logDir = logDir || "./logs"
\t\tif (!fs.existsSync(this.logDir)) {
\t\t\tfs.mkdirSync(this.logDir, { recursive: true })
\t\t}
\t}

\tinfo(message) {
\t\tthis._log("INFO", message)
\t}

\twarn(message) {
\t\tthis._log("WARN", message)
\t}

\terror(message) {
\t\tthis._log("ERROR", message)
\t}

\t_log(level, message) {
\t\tconst timestamp = new Date().toISOString()
\t\tconst logEntry = `[${timestamp}] [${level}] [${this.name}] ${message}`
\t\tconsole.log(logEntry)
\t\tconst logFile = path.join(this.logDir, `${this.name}.log`)
\t\tfs.appendFileSync(logFile, logEntry + "\\n")
\t}
}

module.exports = Logger
'''

    # --- src/utils/validators.ts (spaces=4, single quotes, semicolons) ---
    files['src/utils/validators.ts'] = """export function isValidEmail(email: string): boolean {
    const emailRegex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
    return emailRegex.test(email);
}

export function isValidPhone(phone: string): boolean {
    const phoneRegex = /^\\+?[1-9]\\d{1,14}$/;
    return phoneRegex.test(phone);
}

export function isStrongPassword(password: string): boolean {
    if (password.length < 8) return false;
    const hasUpper = /[A-Z]/.test(password);
    const hasLower = /[a-z]/.test(password);
    const hasDigit = /\\d/.test(password);
    const hasSpecial = /[!@#$%^&*()_+\\-=\\[\\]{}|;':\",.\\/<>?]/.test(password);
    return hasUpper && hasLower && hasDigit && hasSpecial;
}

export function sanitizeInput(input: string): string {
    return input
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#x27;');
}
"""

    # --- src/utils/formatters.js (mixed tabs/spaces, no semicolons) ---
    files['src/utils/formatters.js'] = """const formatCurrency = (amount, currency) => {
  const formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency || 'USD'
  })
  return formatter.format(amount)
}

const formatDate = (date, locale) => {
\tconst d = new Date(date)
\tif (isNaN(d.getTime())) return "Invalid Date"
\treturn d.toLocaleDateString(locale || "en-US", {
\t\tyear: "numeric",
\t\tmonth: "long",
\t\tday: "numeric"
\t})
}

const formatPercentage = (value, decimals) => {
    return (value * 100).toFixed(decimals || 2) + '%'
}

module.exports = { formatCurrency, formatDate, formatPercentage }
"""

    # --- src/utils/helpers.ts (spaces=2, double quotes) ---
    files['src/utils/helpers.ts'] = '''export function debounce<T extends (...args: any[]) => void>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timeoutId: ReturnType<typeof setTimeout>;
  return (...args: Parameters<T>) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

export function throttle<T extends (...args: any[]) => void>(
  fn: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle = false;
  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      fn(...args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}

export function deepClone<T>(obj: T): T {
  return JSON.parse(JSON.stringify(obj));
}
'''

    # --- src/services/database.js (tabs, no semicolons, double quotes) ---
    files['src/services/database.js'] = '''const { Pool } = require("pg")

class DatabaseService {
\tconstructor(connectionString) {
\t\tthis.pool = new Pool({ connectionString })
\t\tthis.connected = false
\t}

\tasync connect() {
\t\ttry {
\t\t\tawait this.pool.connect()
\t\t\tthis.connected = true
\t\t\tconsole.log("Database connected successfully")
\t\t} catch (error) {
\t\t\tconsole.error("Failed to connect:", error.message)
\t\t\tthrow error
\t\t}
\t}

\tasync query(sql, params) {
\t\tif (!this.connected) throw new Error("Not connected")
\t\treturn await this.pool.query(sql, params)
\t}

\tasync disconnect() {
\t\tawait this.pool.end()
\t\tthis.connected = false
\t}
}

module.exports = DatabaseService
'''

    # --- src/services/auth.ts (spaces=4, single quotes, semicolons) ---
    files['src/services/auth.ts'] = """import jwt from 'jsonwebtoken';
import bcrypt from 'bcrypt';

interface TokenPayload {
    userId: string;
    email: string;
    role: string;
}

export class AuthService {
    private secretKey: string;
    private tokenExpiry: string;

    constructor(secretKey: string, tokenExpiry: string = '24h') {
        this.secretKey = secretKey;
        this.tokenExpiry = tokenExpiry;
    }

    async hashPassword(password: string): Promise<string> {
        const saltRounds = 12;
        return await bcrypt.hash(password, saltRounds);
    }

    async verifyPassword(password: string, hash: string): Promise<boolean> {
        return await bcrypt.compare(password, hash);
    }

    generateToken(payload: TokenPayload): string {
        return jwt.sign(payload, this.secretKey, { expiresIn: this.tokenExpiry });
    }

    verifyToken(token: string): TokenPayload | null {
        try {
            return jwt.verify(token, this.secretKey) as TokenPayload;
        } catch {
            return null;
        }
    }
}
"""

    # --- src/services/api.js (spaces=2, mixed quotes, semicolons) ---
    files['src/services/api.js'] = '''const axios = require("axios");

class ApiClient {
  constructor(baseURL, timeout) {
    this.client = axios.create({
      baseURL: baseURL,
      timeout: timeout || 10000,
      headers: {
        'Content-Type': 'application/json',
      }
    });
  }

  async get(endpoint, params) {
    const response = await this.client.get(endpoint, { params });
    return response.data;
  }

  async post(endpoint, data) {
    const response = await this.client.post(endpoint, data);
    return response.data;
  }

  async put(endpoint, data) {
    const response = await this.client.put(endpoint, data);
    return response.data;
  }

  async delete(endpoint) {
    const response = await this.client.delete(endpoint);
    return response.data;
  }

  setAuthToken(token) {
    this.client.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  }
}

module.exports = ApiClient;
'''

    # --- src/services/cache.ts (tabs, double quotes, semicolons) ---
    files['src/services/cache.ts'] = '''interface CacheEntry<T> {
\tvalue: T;
\texpiry: number;
}

export class CacheService<T> {
\tprivate store: Map<string, CacheEntry<T>>;
\tprivate defaultTTL: number;

\tconstructor(defaultTTL: number = 3600) {
\t\tthis.store = new Map();
\t\tthis.defaultTTL = defaultTTL;
\t}

\tset(key: string, value: T, ttl?: number): void {
\t\tconst expiry = Date.now() + (ttl || this.defaultTTL) * 1000;
\t\tthis.store.set(key, { value, expiry });
\t}

\tget(key: string): T | undefined {
\t\tconst entry = this.store.get(key);
\t\tif (!entry) return undefined;
\t\tif (Date.now() > entry.expiry) {
\t\t\tthis.store.delete(key);
\t\t\treturn undefined;
\t\t}
\t\treturn entry.value;
\t}

\tdelete(key: string): boolean {
\t\treturn this.store.delete(key);
\t}

\tclear(): void {
\t\tthis.store.clear();
\t}
}
'''

    # --- src/models/user.ts (spaces=4, single quotes) ---
    files['src/models/user.ts'] = """export interface User {
    id: string;
    email: string;
    firstName: string;
    lastName: string;
    role: 'admin' | 'editor' | 'viewer';
    createdAt: Date;
    updatedAt: Date;
}

export interface CreateUserDTO {
    email: string;
    password: string;
    firstName: string;
    lastName: string;
    role?: 'admin' | 'editor' | 'viewer';
}

export function createUser(dto: CreateUserDTO): Omit<User, 'id'> {
    return {
        email: dto.email,
        firstName: dto.firstName,
        lastName: dto.lastName,
        role: dto.role || 'viewer',
        createdAt: new Date(),
        updatedAt: new Date()
    };
}
"""

    # --- src/models/product.js (tabs, double quotes, no semicolons) ---
    files['src/models/product.js'] = '''class Product {
\tconstructor(data) {
\t\tthis.id = data.id
\t\tthis.name = data.name
\t\tthis.description = data.description
\t\tthis.price = data.price
\t\tthis.category = data.category
\t\tthis.stock = data.stock || 0
\t\tthis.createdAt = data.createdAt || new Date()
\t}

\tapplyDiscount(percentage) {
\t\tif (percentage < 0 || percentage > 100) {
\t\t\tthrow new Error("Invalid discount percentage")
\t\t}
\t\treturn this.price * (1 - percentage / 100)
\t}

\tisInStock() {
\t\treturn this.stock > 0
\t}

\ttoJSON() {
\t\treturn {
\t\t\tid: this.id,
\t\t\tname: this.name,
\t\t\tdescription: this.description,
\t\t\tprice: this.price,
\t\t\tcategory: this.category,
\t\t\tstock: this.stock
\t\t}
\t}
}

module.exports = Product
'''

    # --- src/models/order.ts (spaces=2, double quotes, semicolons) ---
    files['src/models/order.ts'] = '''export interface OrderItem {
  productId: string;
  quantity: number;
  unitPrice: number;
}

export interface Order {
  id: string;
  customerId: string;
  items: OrderItem[];
  status: "pending" | "processing" | "shipped" | "delivered" | "cancelled";
  totalAmount: number;
  createdAt: Date;
}

export function calculateTotal(items: OrderItem[]): number {
  return items.reduce((sum, item) => sum + item.quantity * item.unitPrice, 0);
}

export function canCancel(order: Order): boolean {
  return order.status === "pending" || order.status === "processing";
}
'''

    # --- tests/user.test.js (spaces=2, double quotes, semicolons) ---
    files['tests/user.test.js'] = '''const assert = require("assert");

describe("User Model", () => {
  it("should create a user with default role", () => {
    const user = {
      email: "sarah.chen@example.com",
      firstName: "Sarah",
      lastName: "Chen",
      role: "viewer"
    };
    assert.strictEqual(user.role, "viewer");
  });

  it("should validate email format", () => {
    const validEmail = "marcus.johnson@company.io";
    assert.ok(validEmail.includes("@"));
  });

  it("should reject invalid email", () => {
    const invalidEmail = "not-an-email";
    assert.ok(!invalidEmail.includes("@"));
  });
});
'''

    # --- tests/product.test.js (tabs, single quotes) ---
    files['tests/product.test.js'] = """const assert = require('assert')

describe('Product Model', () => {
\tit('should calculate discount correctly', () => {
\t\tconst price = 99.99
\t\tconst discount = 20
\t\tconst expected = 79.992
\t\tconst result = price * (1 - discount / 100)
\t\tassert.strictEqual(result, expected)
\t})

\tit('should check stock availability', () => {
\t\tconst product = { stock: 5 }
\t\tassert.ok(product.stock > 0)
\t})

\tit('should handle zero stock', () => {
\t\tconst product = { stock: 0 }
\t\tassert.ok(product.stock === 0)
\t})
})
"""

    # --- tests/api.test.ts (spaces=4, single quotes, semicolons) ---
    files['tests/api.test.ts'] = """describe('API Client', () => {
    it('should create client with base URL', () => {
        const baseURL = 'https://api.example.com';
        expect(baseURL).toBeDefined();
    });

    it('should set auth token', () => {
        const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9';
        expect(token.length).toBeGreaterThan(0);
    });

    it('should handle timeout', () => {
        const timeout = 10000;
        expect(timeout).toBe(10000);
    });
});
"""

    # --- tests/validators.test.ts (spaces=2, double quotes) ---
    files['tests/validators.test.ts'] = '''describe("Validators", () => {
  it("should validate correct email", () => {
    const email = "test@example.com";
    expect(email).toMatch(/@/);
  });

  it("should validate phone number", () => {
    const phone = "+14155552671";
    expect(phone).toMatch(/^\\+?[1-9]\\d{1,14}$/);
  });

  it("should check password strength", () => {
    const password = "MyStr0ng!Pass";
    expect(password.length).toBeGreaterThanOrEqual(8);
  });
});
'''

    # --- config/database.json (spaces=2) ---
    files['config/database.json'] = '''{
  "development": {
    "host": "localhost",
    "port": 5432,
    "database": "myapp_dev",
    "username": "dev_user",
    "password": "dev_password_123"
  },
  "production": {
    "host": "db.production.internal",
    "port": 5432,
    "database": "myapp_prod",
    "username": "prod_user",
    "ssl": true
  }
}
'''

    # --- config/redis.json (tabs) ---
    files['config/redis.json'] = '''{
\t"host": "localhost",
\t"port": 6379,
\t"maxRetries": 3,
\t"retryDelay": 1000,
\t"keyPrefix": "myapp:"
}
'''

    # --- scripts/migrate.js (mixed, no semicolons) ---
    files['scripts/migrate.js'] = '''const fs = require("fs")
const path = require("path")

const MIGRATIONS_DIR = path.join(__dirname, "..", "migrations")

async function runMigrations() {
    const files = fs.readdirSync(MIGRATIONS_DIR)
        .filter(f => f.endsWith(".sql"))
        .sort()

    for (const file of files) {
        const sql = fs.readFileSync(path.join(MIGRATIONS_DIR, file), "utf8")
        console.log("Running migration: " + file)
        // Execute SQL here
    }
    console.log("All migrations completed")
}

runMigrations().catch(console.error)
'''

    # --- scripts/seed.js (tabs, double quotes) ---
    files['scripts/seed.js'] = '''const faker = require("faker")

async function seedDatabase() {
\tconst users = []
\tfor (let i = 0; i < 50; i++) {
\t\tusers.push({
\t\t\temail: faker.internet.email(),
\t\t\tfirstName: faker.name.firstName(),
\t\t\tlastName: faker.name.lastName(),
\t\t\trole: ["admin", "editor", "viewer"][Math.floor(Math.random() * 3)]
\t\t})
\t}
\tconsole.log("Seeded " + users.length + " users")
}

seedDatabase().catch(console.error)
'''

    # --- scripts/deploy.sh ---
    files['scripts/deploy.sh'] = '''#!/bin/bash
set -e

echo "Building project..."
npm run build

echo "Running tests..."
npm test

echo "Deploying to production..."
rsync -avz ./dist/ user@production:/var/www/app/

echo "Deployment complete!"
'''

    # --- package.json (spaces=2) ---
    files['package.json'] = '''{
  "name": "myapp-project",
  "version": "1.0.0",
  "description": "A full-stack web application",
  "main": "src/index.js",
  "scripts": {
    "start": "node src/index.js",
    "dev": "nodemon src/index.js",
    "build": "tsc",
    "test": "jest"
  },
  "dependencies": {
    "express": "^4.18.2",
    "pg": "^8.11.3",
    "jsonwebtoken": "^9.0.2",
    "bcrypt": "^5.1.1",
    "axios": "^1.6.2"
  },
  "devDependencies": {
    "typescript": "^5.3.3",
    "jest": "^29.7.0",
    "@types/node": "^20.10.0",
    "nodemon": "^3.0.2"
  }
}
'''

    # --- tsconfig.json (tabs mixed with spaces) ---
    files['tsconfig.json'] = '''{
\t"compilerOptions": {
\t\t"target": "ES2020",
    "module": "commonjs",
\t\t"strict": true,
    "esModuleInterop": true,
\t\t"outDir": "./dist",
    "rootDir": "./src",
\t\t"resolveJsonModule": true
\t},
\t"include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
'''

    # --- README.md ---
    files['README.md'] = '''# MyApp Project

A full-stack web application built with Node.js and TypeScript.

## Getting Started

1. Clone the repository
2. Run `npm install`
3. Configure database in `config/database.json`
4. Run `npm run dev`

## Project Structure

- `src/` - Source code
  - `components/` - React components
  - `utils/` - Utility functions
  - `services/` - Business logic services
  - `models/` - Data models
- `tests/` - Test files
- `config/` - Configuration files
- `scripts/` - Utility scripts
'''

    # --- .gitignore (basic) ---
    files['.gitignore'] = '''node_modules/
dist/
.env
*.log
coverage/
'''

    # --- src/routes/users.js (spaces=4, mixed) ---
    files['src/routes/users.js'] = """const express = require("express")
const router = express.Router()

router.get("/", async (req, res) => {
    try {
        const users = [] // fetch from DB
        res.json({ success: true, data: users })
    } catch (error) {
        res.status(500).json({ success: false, message: error.message })
    }
})

router.post("/", async (req, res) => {
    const { email, firstName, lastName } = req.body
    if (!email || !firstName) {
        return res.status(400).json({ success: false, message: "Missing required fields" })
    }
    res.status(201).json({ success: true, data: { email, firstName, lastName } })
})

module.exports = router
"""
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'routes'), exist_ok=True)

    # --- src/routes/products.js (tabs, double quotes) ---
    files['src/routes/products.js'] = '''const express = require("express")
const router = express.Router()

router.get("/", async (req, res) => {
\ttry {
\t\tconst { category, minPrice, maxPrice } = req.query
\t\tconst products = [] // fetch from DB
\t\tres.json({ success: true, data: products })
\t} catch (error) {
\t\tres.status(500).json({ success: false, message: error.message })
\t}
})

router.get("/:id", async (req, res) => {
\ttry {
\t\tconst product = null // fetch by ID
\t\tif (!product) {
\t\t\treturn res.status(404).json({ success: false, message: "Product not found" })
\t\t}
\t\tres.json({ success: true, data: product })
\t} catch (error) {
\t\tres.status(500).json({ success: false, message: error.message })
\t}
})

module.exports = router
'''

    # --- src/middleware/auth.js (spaces=2, no semicolons) ---
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'middleware'), exist_ok=True)
    files['src/middleware/auth.js'] = """const jwt = require('jsonwebtoken')

const authenticate = (req, res, next) => {
  const authHeader = req.headers.authorization
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ message: 'Authentication required' })
  }

  const token = authHeader.split(' ')[1]
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET)
    req.user = decoded
    next()
  } catch (error) {
    return res.status(401).json({ message: 'Invalid token' })
  }
}

module.exports = authenticate
"""

    # --- src/middleware/errorHandler.js (tabs, double quotes, semicolons) ---
    files['src/middleware/errorHandler.js'] = '''const errorHandler = (err, req, res, next) => {
\tconst statusCode = err.statusCode || 500;
\tconst message = err.message || "Internal Server Error";

\tconsole.error(`[Error] ${statusCode}: ${message}`);

\tres.status(statusCode).json({
\t\tsuccess: false,
\t\terror: {
\t\t\tstatusCode,
\t\t\tmessage,
\t\t\tstack: process.env.NODE_ENV === "development" ? err.stack : undefined
\t\t}
\t});
};

module.exports = errorHandler;
'''

    # --- src/constants.ts (spaces=4, single quotes) ---
    files['src/constants.ts'] = """export const API_VERSION = 'v1';
export const MAX_PAGE_SIZE = 100;
export const DEFAULT_PAGE_SIZE = 20;
export const TOKEN_EXPIRY = '24h';
export const SALT_ROUNDS = 12;

export const HTTP_STATUS = {
    OK: 200,
    CREATED: 201,
    BAD_REQUEST: 400,
    UNAUTHORIZED: 401,
    FORBIDDEN: 403,
    NOT_FOUND: 404,
    INTERNAL_ERROR: 500,
};

export const ROLES = {
    ADMIN: 'admin',
    EDITOR: 'editor',
    VIEWER: 'viewer',
} as const;
"""

    # --- src/types/index.ts (tabs, semicolons) ---
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'types'), exist_ok=True)
    files['src/types/index.ts'] = '''export interface PaginatedResponse<T> {
\tdata: T[];
\ttotal: number;
\tpage: number;
\tpageSize: number;
\thasNext: boolean;
}

export interface ApiError {
\tstatusCode: number;
\tmessage: string;
\tdetails?: Record<string, unknown>;
}

export type SortDirection = "asc" | "desc";

export interface SortOptions {
\tfield: string;
\tdirection: SortDirection;
}
'''

    # Write all files
    for rel_path, content in files.items():
        full_path = os.path.join(PROJECT_DIR, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(content)

    print(f'Created {len(files)} files in {PROJECT_DIR}')


def main():
    create_project_files()
    print(f'Initial project setup complete: {PROJECT_DIR}')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()

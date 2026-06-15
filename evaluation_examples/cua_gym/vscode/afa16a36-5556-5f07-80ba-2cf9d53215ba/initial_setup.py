"""
Initial Setup: Disable ESLint extension for current workspace
Task ID: vscode_we_053
Domain: vscode

Creates ~/projects/legacy-app/ with realistic project files,
installs dbaeumer.vscode-eslint extension globally,
and opens VSCode with the legacy-app folder.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_053'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'legacy-app')
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')


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
    """Create a realistic legacy JavaScript project."""
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # package.json
    package_json = {
        "name": "legacy-app",
        "version": "1.2.7",
        "description": "Legacy customer management application",
        "main": "src/index.js",
        "scripts": {
            "start": "node src/index.js",
            "lint": "eslint src/",
            "test": "jest"
        },
        "dependencies": {
            "express": "^4.18.2",
            "mongoose": "^7.6.3",
            "dotenv": "^16.3.1"
        },
        "devDependencies": {
            "eslint": "^8.52.0",
            "jest": "^29.7.0"
        }
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # .eslintrc.json
    eslintrc = {
        "env": {
            "node": True,
            "es2021": True
        },
        "extends": "eslint:recommended",
        "parserOptions": {
            "ecmaVersion": "latest"
        },
        "rules": {
            "no-unused-vars": "warn",
            "no-console": "off",
            "semi": ["error", "always"],
            "quotes": ["error", "double"]
        }
    }
    with open(os.path.join(PROJECT_DIR, '.eslintrc.json'), 'w') as f:
        json.dump(eslintrc, f, indent=2)

    # src directory
    src_dir = os.path.join(PROJECT_DIR, 'src')
    os.makedirs(src_dir, exist_ok=True)

    # src/index.js
    index_js = '''const express = require("express");
const dotenv = require("dotenv");
const customerRoutes = require("./routes/customers");
const { connectDatabase } = require("./db");

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use("/api/customers", customerRoutes);

app.get("/health", (req, res) => {
  res.json({ status: "ok", uptime: process.uptime() });
});

connectDatabase().then(() => {
  app.listen(PORT, () => {
    console.log(`Legacy App running on port ${PORT}`);
  });
});
'''
    with open(os.path.join(src_dir, 'index.js'), 'w') as f:
        f.write(index_js)

    # src/db.js
    db_js = '''const mongoose = require("mongoose");

const MONGO_URI = process.env.MONGO_URI || "mongodb://localhost:27017/legacy_app";

async function connectDatabase() {
  try {
    await mongoose.connect(MONGO_URI);
    console.log("Connected to MongoDB");
  } catch (error) {
    console.error("Database connection failed:", error.message);
    process.exit(1);
  }
}

module.exports = { connectDatabase };
'''
    with open(os.path.join(src_dir, 'db.js'), 'w') as f:
        f.write(db_js)

    # src/routes directory
    routes_dir = os.path.join(src_dir, 'routes')
    os.makedirs(routes_dir, exist_ok=True)

    # src/routes/customers.js
    customers_js = '''const express = require("express");
const router = express.Router();
const Customer = require("../models/Customer");

router.get("/", async (req, res) => {
  const customers = await Customer.find().sort({ createdAt: -1 });
  res.json(customers);
});

router.post("/", async (req, res) => {
  const { name, email, company, phone } = req.body;
  const customer = new Customer({ name, email, company, phone });
  await customer.save();
  res.status(201).json(customer);
});

router.get("/:id", async (req, res) => {
  const customer = await Customer.findById(req.params.id);
  if (!customer) return res.status(404).json({ error: "Not found" });
  res.json(customer);
});

module.exports = router;
'''
    with open(os.path.join(routes_dir, 'customers.js'), 'w') as f:
        f.write(customers_js)

    # src/models directory
    models_dir = os.path.join(src_dir, 'models')
    os.makedirs(models_dir, exist_ok=True)

    # src/models/Customer.js
    customer_model = '''const mongoose = require("mongoose");

const customerSchema = new mongoose.Schema({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  company: { type: String, default: "" },
  phone: { type: String, default: "" },
  notes: { type: String, default: "" },
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model("Customer", customerSchema);
'''
    with open(os.path.join(models_dir, 'Customer.js'), 'w') as f:
        f.write(customer_model)

    # README.md
    readme = """# Legacy App - Customer Management

Internal customer management system built with Express and MongoDB.

## Setup
```bash
npm install
cp .env.example .env
npm start
```

## Known Issues
- ESLint warnings in several modules need cleanup
- Migration to TypeScript planned for Q3 2026
"""
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write(readme)

    # .env.example
    with open(os.path.join(PROJECT_DIR, '.env.example'), 'w') as f:
        f.write("PORT=3000\nMONGO_URI=mongodb://localhost:27017/legacy_app\n")

    print(f"Project files created at {PROJECT_DIR}")


def install_eslint_extension():
    """Install the ESLint extension globally."""
    result = subprocess.run(
        ["code", "--install-extension", "dbaeumer.vscode-eslint", "--force"],
        capture_output=True, text=True, timeout=120
    )
    print(f"Extension install stdout: {result.stdout.strip()}")
    if result.returncode != 0:
        print(f"Extension install stderr: {result.stderr.strip()}")
    # Verify
    result2 = subprocess.run(
        ["code", "--list-extensions"],
        capture_output=True, text=True
    )
    if "dbaeumer.vscode-eslint" in result2.stdout.lower():
        print("ESLint extension installed successfully")
    else:
        print(f"WARNING: ESLint extension may not be installed. Extensions: {result2.stdout.strip()}")


def ensure_settings():
    """Ensure VSCode user settings exist (merge with existing)."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    # Keep existing settings, just ensure workspace trust is disabled
    settings.setdefault("security.workspace.trust.enabled", False)
    settings.setdefault("security.workspace.trust.startupPrompt", "never")
    settings.setdefault("security.workspace.trust.emptyWindow", False)

    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
    print("User settings ensured")


def main():
    create_project_files()
    install_eslint_extension()
    ensure_settings()

    # Open VSCode with the legacy-app folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: VSCode opened with ~/projects/legacy-app/')


main()

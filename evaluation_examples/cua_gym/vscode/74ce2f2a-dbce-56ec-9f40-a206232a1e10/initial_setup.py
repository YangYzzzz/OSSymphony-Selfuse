"""
Initial Setup: Configure Auto Rename Tag and Auto Close Tag extensions for HTML and JSX files
Task ID: vscode_we_089
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_089'
WORKSPACE = f'{WORKDIR}/workspace'
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


def create_react_project():
    """Create a realistic React project structure."""
    os.makedirs(os.path.join(WORKSPACE, 'src', 'components'), exist_ok=True)
    os.makedirs(os.path.join(WORKSPACE, 'public'), exist_ok=True)

    # package.json
    pkg = {
        "name": "inventory-dashboard",
        "version": "1.2.0",
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
        }
    }
    with open(os.path.join(WORKSPACE, 'package.json'), 'w') as f:
        json.dump(pkg, f, indent=2)

    # public/index.html
    index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Inventory Dashboard</title>
</head>
<body>
    <div id="root"></div>
</body>
</html>
"""
    with open(os.path.join(WORKSPACE, 'public', 'index.html'), 'w') as f:
        f.write(index_html)

    # src/App.jsx
    app_jsx = """import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import ProductTable from './components/ProductTable';
import axios from 'axios';

function App() {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        axios.get('/api/products')
            .then(res => {
                setProducts(res.data);
                setLoading(false);
            })
            .catch(err => {
                console.error('Failed to fetch products:', err);
                setLoading(false);
            });
    }, []);

    return (
        <div className="app-container">
            <Header title="Inventory Dashboard" />
            <main>
                {loading ? (
                    <p className="loading-text">Loading inventory data...</p>
                ) : (
                    <ProductTable products={products} />
                )}
            </main>
            <footer>
                <p>&copy; 2025 Acme Warehouse Solutions</p>
            </footer>
        </div>
    );
}

export default App;
"""
    with open(os.path.join(WORKSPACE, 'src', 'App.jsx'), 'w') as f:
        f.write(app_jsx)

    # src/components/Header.jsx
    header_jsx = """import React from 'react';

function Header({ title }) {
    return (
        <header className="dashboard-header">
            <h1>{title}</h1>
            <nav>
                <ul>
                    <li><a href="/inventory">Inventory</a></li>
                    <li><a href="/orders">Orders</a></li>
                    <li><a href="/reports">Reports</a></li>
                </ul>
            </nav>
        </header>
    );
}

export default Header;
"""
    with open(os.path.join(WORKSPACE, 'src', 'components', 'Header.jsx'), 'w') as f:
        f.write(header_jsx)

    # src/components/ProductTable.jsx
    product_table_jsx = """import React from 'react';

function ProductTable({ products }) {
    return (
        <div className="table-wrapper">
            <table>
                <thead>
                    <tr>
                        <th>SKU</th>
                        <th>Product Name</th>
                        <th>Category</th>
                        <th>Quantity</th>
                        <th>Unit Price</th>
                    </tr>
                </thead>
                <tbody>
                    {products.map(product => (
                        <tr key={product.sku}>
                            <td>{product.sku}</td>
                            <td>{product.name}</td>
                            <td>{product.category}</td>
                            <td>{product.quantity}</td>
                            <td>${product.unitPrice.toFixed(2)}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default ProductTable;
"""
    with open(os.path.join(WORKSPACE, 'src', 'components', 'ProductTable.jsx'), 'w') as f:
        f.write(product_table_jsx)

    # src/index.js
    index_js = """import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);
"""
    with open(os.path.join(WORKSPACE, 'src', 'index.js'), 'w') as f:
        f.write(index_js)

    print(f'React project created at {WORKSPACE}')


def setup_empty_vscode_settings():
    """Ensure VSCode settings.json is empty (no extension settings)."""
    os.makedirs(VSCODE_USER, exist_ok=True)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump({}, f, indent=4)
    print(f'Empty settings.json written to {SETTINGS_PATH}')


def ensure_extensions_not_installed():
    """Uninstall the target extensions if they happen to be installed."""
    for ext_id in ['formulahendry.auto-rename-tag', 'formulahendry.auto-close-tag']:
        subprocess.run(
            ['code', '--uninstall-extension', ext_id],
            capture_output=True, text=True
        )
    print('Ensured target extensions are not installed')


def create_initial():
    create_react_project()
    setup_empty_vscode_settings()
    ensure_extensions_not_installed()

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

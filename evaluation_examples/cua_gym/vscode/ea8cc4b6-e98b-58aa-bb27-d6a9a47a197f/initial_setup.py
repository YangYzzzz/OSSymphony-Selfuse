"""
Initial Setup: Configure VSCode workspace with Prettier + ESLint (conflicting state)
Task ID: vscode_we_084
Domain: vscode

Creates a React TypeScript project with both Prettier and ESLint installed,
but with empty user settings (causing formatting conflicts).
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_084'
PROJECT_DIR = f'{WORKDIR}/{TASK_ID}'
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


def create_project():
    """Create a realistic React TypeScript project."""
    os.makedirs(f'{PROJECT_DIR}/src/components', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/hooks', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/public', exist_ok=True)

    # package.json
    package_json = {
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
        "devDependencies": {
            "eslint": "^8.56.0",
            "@typescript-eslint/eslint-plugin": "^6.19.0",
            "@typescript-eslint/parser": "^6.19.0",
            "eslint-plugin-react": "^7.33.2",
            "eslint-plugin-react-hooks": "^4.6.0",
            "prettier": "^3.2.4",
            "eslint-config-prettier": "^9.1.0"
        },
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test",
            "lint": "eslint src/ --ext .ts,.tsx"
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # tsconfig.json
    tsconfig = {
        "compilerOptions": {
            "target": "es2020",
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
    with open(f'{PROJECT_DIR}/tsconfig.json', 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # .eslintrc.json - ESLint config with formatting rules (causes conflicts)
    eslintrc = {
        "env": {
            "browser": True,
            "es2021": True
        },
        "extends": [
            "eslint:recommended",
            "plugin:react/recommended",
            "plugin:@typescript-eslint/recommended",
            "plugin:react-hooks/recommended"
        ],
        "parser": "@typescript-eslint/parser",
        "parserOptions": {
            "ecmaFeatures": {"jsx": True},
            "ecmaVersion": "latest",
            "sourceType": "module"
        },
        "plugins": ["react", "@typescript-eslint"],
        "rules": {
            "indent": ["error", 4],
            "semi": ["error", "always"],
            "quotes": ["error", "double"],
            "react/react-in-jsx-scope": "off",
            "no-unused-vars": "warn",
            "@typescript-eslint/no-unused-vars": "warn"
        },
        "settings": {
            "react": {"version": "detect"}
        }
    }
    with open(f'{PROJECT_DIR}/.eslintrc.json', 'w') as f:
        json.dump(eslintrc, f, indent=2)

    # .prettierrc - Prettier config (conflicts with ESLint indent/semi/quotes)
    prettierrc = {
        "semi": True,
        "trailingComma": "all",
        "singleQuote": True,
        "printWidth": 100,
        "tabWidth": 2,
        "useTabs": False,
        "bracketSpacing": True,
        "arrowParens": "always"
    }
    with open(f'{PROJECT_DIR}/.prettierrc', 'w') as f:
        json.dump(prettierrc, f, indent=2)

    # src/App.tsx - Main app component (with intentional formatting inconsistencies)
    app_tsx = '''import React, { useState, useEffect } from "react";
import { InventoryTable } from "./components/InventoryTable";
import { useFetchProducts } from "./hooks/useFetchProducts";

interface DashboardStats {
    totalProducts: number;
    lowStockCount: number;
    totalValue: number;
    lastUpdated: string;
}

const App: React.FC = () => {
    const [stats, setStats] = useState<DashboardStats>({
        totalProducts: 0,
        lowStockCount: 0,
        totalValue: 0,
        lastUpdated: new Date().toISOString(),
    });
    const { products, loading, error } = useFetchProducts();

    useEffect(() => {
        if (products.length > 0) {
            const totalValue = products.reduce(
                (sum, p) => sum + p.price * p.quantity,
                0
            );
            const lowStock = products.filter((p) => p.quantity < 10).length;
            setStats({
                totalProducts: products.length,
                lowStockCount: lowStock,
                totalValue,
                lastUpdated: new Date().toISOString(),
            });
        }
    }, [products]);

    if (loading) return <div className="loading-spinner">Loading inventory data...</div>;
    if (error) return <div className="error-banner">Error: {error.message}</div>;

    return (
        <div className="dashboard-container">
            <header>
                <h1>Inventory Management Dashboard</h1>
                <p>Last updated: {new Date(stats.lastUpdated).toLocaleString()}</p>
            </header>
            <div className="stats-grid">
                <div className="stat-card">
                    <span className="stat-label">Total Products</span>
                    <span className="stat-value">{stats.totalProducts}</span>
                </div>
                <div className="stat-card warning">
                    <span className="stat-label">Low Stock Items</span>
                    <span className="stat-value">{stats.lowStockCount}</span>
                </div>
                <div className="stat-card">
                    <span className="stat-label">Total Inventory Value</span>
                    <span className="stat-value">${stats.totalValue.toLocaleString()}</span>
                </div>
            </div>
            <InventoryTable products={products} />
        </div>
    );
};

export default App;
'''
    with open(f'{PROJECT_DIR}/src/App.tsx', 'w') as f:
        f.write(app_tsx)

    # src/components/InventoryTable.tsx
    inventory_table = '''import React from "react";

export interface Product {
    id: string;
    name: string;
    category: string;
    price: number;
    quantity: number;
    supplier: string;
    sku: string;
}

interface InventoryTableProps {
    products: Product[];
}

export const InventoryTable: React.FC<InventoryTableProps> = ({ products }) => {
    const getStockStatus = (quantity: number): string => {
        if (quantity === 0) return "out-of-stock";
        if (quantity < 10) return "low-stock";
        if (quantity < 50) return "medium-stock";
        return "in-stock";
    };

    return (
        <table className="inventory-table">
            <thead>
                <tr>
                    <th>SKU</th>
                    <th>Product Name</th>
                    <th>Category</th>
                    <th>Price</th>
                    <th>Quantity</th>
                    <th>Supplier</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {products.map((product) => (
                    <tr key={product.id} className={getStockStatus(product.quantity)}>
                        <td>{product.sku}</td>
                        <td>{product.name}</td>
                        <td>{product.category}</td>
                        <td>${product.price.toFixed(2)}</td>
                        <td>{product.quantity}</td>
                        <td>{product.supplier}</td>
                        <td>
                            <span className={`badge ${getStockStatus(product.quantity)}`}>
                                {getStockStatus(product.quantity).replace("-", " ")}
                            </span>
                        </td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
};
'''
    with open(f'{PROJECT_DIR}/src/components/InventoryTable.tsx', 'w') as f:
        f.write(inventory_table)

    # src/hooks/useFetchProducts.ts
    hooks_file = '''import { useState, useEffect } from "react";
import { Product } from "../components/InventoryTable";

interface UseFetchProductsReturn {
    products: Product[];
    loading: boolean;
    error: Error | null;
}

const MOCK_PRODUCTS: Product[] = [
    { id: "1", name: "Ergonomic Office Chair", category: "Furniture", price: 349.99, quantity: 24, supplier: "ErgoWorks Inc.", sku: "FRN-2401" },
    { id: "2", name: "Standing Desk Converter", category: "Furniture", price: 229.50, quantity: 8, supplier: "FlexDesk Co.", sku: "FRN-2402" },
    { id: "3", name: "Wireless Keyboard", category: "Electronics", price: 79.99, quantity: 156, supplier: "TechParts Ltd.", sku: "ELC-3301" },
    { id: "4", name: "27-inch 4K Monitor", category: "Electronics", price: 449.00, quantity: 3, supplier: "DisplayPro", sku: "ELC-3302" },
    { id: "5", name: "Noise Cancelling Headset", category: "Electronics", price: 189.95, quantity: 42, supplier: "AudioClear", sku: "ELC-3303" },
    { id: "6", name: "USB-C Docking Station", category: "Accessories", price: 129.99, quantity: 0, supplier: "TechParts Ltd.", sku: "ACC-4401" },
    { id: "7", name: "Webcam HD 1080p", category: "Electronics", price: 69.99, quantity: 67, supplier: "VisionTech", sku: "ELC-3304" },
    { id: "8", name: "Cable Management Kit", category: "Accessories", price: 24.99, quantity: 200, supplier: "OfficePro", sku: "ACC-4402" },
];

export const useFetchProducts = (): UseFetchProductsReturn => {
    const [products, setProducts] = useState<Product[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                // Simulating API call
                await new Promise((resolve) => setTimeout(resolve, 500));
                setProducts(MOCK_PRODUCTS);
            } catch (err) {
                setError(err instanceof Error ? err : new Error("Unknown error"));
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    return { products, loading, error };
};
'''
    with open(f'{PROJECT_DIR}/src/hooks/useFetchProducts.ts', 'w') as f:
        f.write(hooks_file)

    # src/index.tsx
    index_tsx = '''import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

const root = ReactDOM.createRoot(
    document.getElementById("root") as HTMLElement
);

root.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);
'''
    with open(f'{PROJECT_DIR}/src/index.tsx', 'w') as f:
        f.write(index_tsx)

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
    with open(f'{PROJECT_DIR}/public/index.html', 'w') as f:
        f.write(index_html)


def setup_vscode_settings():
    """Set up VSCode with empty user settings (conflict state)."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Empty user settings - this is the initial state with conflicts
    with open(SETTINGS_PATH, 'w') as f:
        json.dump({}, f, indent=4)

    print(f'VSCode settings initialized (empty): {SETTINGS_PATH}')


def install_extensions():
    """Ensure both Prettier and ESLint extensions are installed."""
    extensions = ['esbenp.prettier-vscode', 'dbaeumer.vscode-eslint']
    for ext in extensions:
        result = subprocess.run(
            ['code', '--install-extension', ext, '--force'],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            print(f'Extension installed: {ext}')
        else:
            print(f'Extension install attempt for {ext}: {result.stderr.strip()}')


def main():
    create_project()
    print(f'Project created: {PROJECT_DIR}')

    setup_vscode_settings()
    install_extensions()

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()

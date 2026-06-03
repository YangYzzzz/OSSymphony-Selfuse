"""
Initial Setup: Create monorepo project structure with three packages
Task ID: vscode_wf_047
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT = f'{WORKDIR}/project'

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
    # Create project root
    os.makedirs(PROJECT, exist_ok=True)

    # --- packages/shared ---
    shared_dir = os.path.join(PROJECT, 'packages', 'shared', 'src')
    os.makedirs(shared_dir, exist_ok=True)

    shared_pkg = {
        "name": "@monorepo/shared",
        "version": "1.0.0",
        "description": "Shared utility library for the monorepo",
        "main": "dist/index.js",
        "types": "dist/index.d.ts",
        "scripts": {
            "build": "tsc",
            "dev": "tsc --watch",
            "clean": "rm -rf dist"
        },
        "dependencies": {},
        "devDependencies": {
            "typescript": "^5.3.3"
        }
    }
    with open(os.path.join(PROJECT, 'packages', 'shared', 'package.json'), 'w') as f:
        json.dump(shared_pkg, f, indent=2)

    shared_tsconfig = {
        "compilerOptions": {
            "target": "ES2020",
            "module": "commonjs",
            "lib": ["ES2020"],
            "declaration": True,
            "strict": True,
            "outDir": "./dist",
            "rootDir": "./src",
            "esModuleInterop": True,
            "skipLibCheck": True,
            "forceConsistentCasingInFileNames": True,
            "resolveJsonModule": True
        },
        "include": ["src/**/*"],
        "exclude": ["node_modules", "dist"]
    }
    with open(os.path.join(PROJECT, 'packages', 'shared', 'tsconfig.json'), 'w') as f:
        json.dump(shared_tsconfig, f, indent=2)

    # Create a sample shared utility file
    with open(os.path.join(shared_dir, 'index.ts'), 'w') as f:
        f.write('''export function formatCurrency(amount: number, currency: string = "USD"): string {
    return new Intl.NumberFormat("en-US", {
        style: "currency",
        currency,
    }).format(amount);
}

export function slugify(text: string): string {
    return text
        .toLowerCase()
        .replace(/[^\\w\\s-]/g, "")
        .replace(/[\\s_]+/g, "-")
        .replace(/^-+|-+$/g, "");
}

export interface ApiResponse<T> {
    data: T;
    status: number;
    message: string;
    timestamp: string;
}

export function createResponse<T>(data: T, status: number = 200, message: string = "OK"): ApiResponse<T> {
    return {
        data,
        status,
        message,
        timestamp: new Date().toISOString(),
    };
}
''')

    # --- packages/api ---
    api_dir = os.path.join(PROJECT, 'packages', 'api', 'src')
    os.makedirs(api_dir, exist_ok=True)

    api_pkg = {
        "name": "@monorepo/api",
        "version": "1.0.0",
        "description": "Express API server",
        "main": "dist/server.js",
        "scripts": {
            "build": "tsc",
            "dev": "ts-node src/server.ts",
            "start": "node dist/server.js",
            "clean": "rm -rf dist"
        },
        "dependencies": {
            "express": "^4.18.2",
            "@monorepo/shared": "1.0.0"
        },
        "devDependencies": {
            "typescript": "^5.3.3",
            "@types/express": "^4.17.21",
            "ts-node": "^10.9.2"
        }
    }
    with open(os.path.join(PROJECT, 'packages', 'api', 'package.json'), 'w') as f:
        json.dump(api_pkg, f, indent=2)

    api_tsconfig = {
        "compilerOptions": {
            "target": "ES2020",
            "module": "commonjs",
            "lib": ["ES2020"],
            "strict": True,
            "outDir": "./dist",
            "rootDir": "./src",
            "esModuleInterop": True,
            "skipLibCheck": True,
            "forceConsistentCasingInFileNames": True,
            "resolveJsonModule": True
        },
        "include": ["src/**/*"],
        "exclude": ["node_modules", "dist"]
    }
    with open(os.path.join(PROJECT, 'packages', 'api', 'package.json'), 'r') as f:
        pass  # just verifying it exists
    with open(os.path.join(PROJECT, 'packages', 'api', 'tsconfig.json'), 'w') as f:
        json.dump(api_tsconfig, f, indent=2)

    # Create a sample API server file
    with open(os.path.join(api_dir, 'server.ts'), 'w') as f:
        f.write('''import express from "express";
import { formatCurrency, createResponse } from "@monorepo/shared";

const app = express();
const PORT = process.env.PORT || 3001;

app.use(express.json());

interface Product {
    id: number;
    name: string;
    price: number;
    category: string;
}

const products: Product[] = [
    { id: 1, name: "Wireless Headphones", price: 79.99, category: "Electronics" },
    { id: 2, name: "Ergonomic Keyboard", price: 129.50, category: "Electronics" },
    { id: 3, name: "Standing Desk Mat", price: 45.00, category: "Office" },
    { id: 4, name: "USB-C Hub", price: 34.99, category: "Electronics" },
    { id: 5, name: "Desk Lamp LED", price: 52.75, category: "Office" },
];

app.get("/api/products", (_req, res) => {
    const enriched = products.map((p) => ({
        ...p,
        formattedPrice: formatCurrency(p.price),
    }));
    res.json(createResponse(enriched));
});

app.get("/api/products/:id", (req, res) => {
    const product = products.find((p) => p.id === parseInt(req.params.id));
    if (!product) {
        res.status(404).json(createResponse(null, 404, "Product not found"));
        return;
    }
    res.json(createResponse({ ...product, formattedPrice: formatCurrency(product.price) }));
});

app.listen(PORT, () => {
    console.log(`API server running on port ${PORT}`);
});
''')

    # --- packages/web ---
    web_dir = os.path.join(PROJECT, 'packages', 'web', 'src')
    os.makedirs(web_dir, exist_ok=True)

    web_pkg = {
        "name": "@monorepo/web",
        "version": "1.0.0",
        "description": "React frontend application",
        "scripts": {
            "build": "tsc && vite build",
            "dev": "vite",
            "preview": "vite preview",
            "clean": "rm -rf dist"
        },
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "@monorepo/shared": "1.0.0"
        },
        "devDependencies": {
            "typescript": "^5.3.3",
            "@types/react": "^18.2.48",
            "@types/react-dom": "^18.2.18",
            "vite": "^5.0.12",
            "@vitejs/plugin-react": "^4.2.1"
        }
    }
    with open(os.path.join(PROJECT, 'packages', 'web', 'package.json'), 'w') as f:
        json.dump(web_pkg, f, indent=2)

    web_tsconfig = {
        "compilerOptions": {
            "target": "ES2020",
            "module": "ESNext",
            "lib": ["ES2020", "DOM", "DOM.Iterable"],
            "jsx": "react-jsx",
            "strict": True,
            "moduleResolution": "bundler",
            "outDir": "./dist",
            "rootDir": "./src",
            "esModuleInterop": True,
            "skipLibCheck": True,
            "forceConsistentCasingInFileNames": True,
            "resolveJsonModule": True
        },
        "include": ["src/**/*"],
        "exclude": ["node_modules", "dist"]
    }
    with open(os.path.join(PROJECT, 'packages', 'web', 'tsconfig.json'), 'w') as f:
        json.dump(web_tsconfig, f, indent=2)

    # Create a sample React app file
    with open(os.path.join(web_dir, 'App.tsx'), 'w') as f:
        f.write('''import React, { useEffect, useState } from "react";
import { formatCurrency, ApiResponse } from "@monorepo/shared";

interface Product {
    id: number;
    name: string;
    price: number;
    category: string;
    formattedPrice: string;
}

function App() {
    const [products, setProducts] = useState<Product[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch("/api/products")
            .then((res) => res.json())
            .then((response: ApiResponse<Product[]>) => {
                setProducts(response.data);
                setLoading(false);
            })
            .catch((err) => {
                console.error("Failed to fetch products:", err);
                setLoading(false);
            });
    }, []);

    if (loading) return <div className="loading">Loading products...</div>;

    return (
        <div className="app">
            <h1>Product Catalog</h1>
            <div className="product-grid">
                {products.map((product) => (
                    <div key={product.id} className="product-card">
                        <h3>{product.name}</h3>
                        <p className="category">{product.category}</p>
                        <p className="price">{formatCurrency(product.price)}</p>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default App;
''')

    # Create root package.json for the monorepo
    root_pkg = {
        "name": "monorepo",
        "version": "1.0.0",
        "private": True,
        "description": "Monorepo project with shared utilities, API server, and React frontend",
        "workspaces": [
            "packages/*"
        ],
        "scripts": {
            "dev:api": "cd packages/api && npm run dev",
            "dev:web": "cd packages/web && npm run dev"
        }
    }
    with open(os.path.join(PROJECT, 'package.json'), 'w') as f:
        json.dump(root_pkg, f, indent=2)

    print(f'Initial project structure created at: {PROJECT}')

    # Verify no workspace file, no .vscode/tasks.json, no .vscode/extensions.json exist
    for check_path in [
        os.path.join(PROJECT, 'monorepo.code-workspace'),
        os.path.join(PROJECT, '.vscode', 'tasks.json'),
        os.path.join(PROJECT, '.vscode', 'extensions.json'),
    ]:
        if os.path.exists(check_path):
            os.remove(check_path)
            print(f'Removed pre-existing: {check_path}')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()

"""
Initial Setup: Configure VSCode with a TypeScript project (no watch task)
Task ID: vscode_web_058
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_058'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'ts-app')
VSCODE_DIR = os.path.join(PROJECT_DIR, '.vscode')


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
    # Create project directory structure
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src'), exist_ok=True)
    os.makedirs(VSCODE_DIR, exist_ok=True)

    # --- package.json ---
    package_json = {
        "name": "ts-app",
        "version": "1.0.0",
        "description": "Inventory management system for retail analytics",
        "main": "dist/index.js",
        "scripts": {
            "build": "tsc",
            "start": "node dist/index.js",
            "lint": "eslint src/"
        },
        "dependencies": {
            "express": "^4.18.2",
            "pg": "^8.11.3"
        },
        "devDependencies": {
            "typescript": "^5.3.3",
            "@types/express": "^4.17.21",
            "@types/node": "^20.10.0",
            "@types/pg": "^8.10.9"
        }
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # --- tsconfig.json ---
    tsconfig = {
        "compilerOptions": {
            "target": "ES2020",
            "module": "commonjs",
            "lib": ["ES2020"],
            "outDir": "./dist",
            "rootDir": "./src",
            "strict": True,
            "esModuleInterop": True,
            "skipLibCheck": True,
            "forceConsistentCasingInFileNames": True,
            "resolveJsonModule": True,
            "declaration": True,
            "declarationMap": True,
            "sourceMap": True
        },
        "include": ["src/**/*"],
        "exclude": ["node_modules", "dist"]
    }
    with open(os.path.join(PROJECT_DIR, 'tsconfig.json'), 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # --- src/index.ts ---
    index_ts = '''import express, { Request, Response } from 'express';
import { InventoryService } from './services/inventoryService';
import { DatabaseConfig } from './config/database';

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

const inventoryService = new InventoryService();

app.get('/api/products', async (req: Request, res: Response) => {
    try {
        const products = await inventoryService.getAllProducts();
        res.json({ success: true, data: products });
    } catch (error) {
        res.status(500).json({ success: false, error: 'Failed to fetch products' });
    }
});

app.get('/api/products/:id', async (req: Request, res: Response) => {
    try {
        const product = await inventoryService.getProductById(req.params.id);
        if (!product) {
            return res.status(404).json({ success: false, error: 'Product not found' });
        }
        res.json({ success: true, data: product });
    } catch (error) {
        res.status(500).json({ success: false, error: 'Failed to fetch product' });
    }
});

app.post('/api/products', async (req: Request, res: Response) => {
    try {
        const newProduct = await inventoryService.createProduct(req.body);
        res.status(201).json({ success: true, data: newProduct });
    } catch (error) {
        res.status(500).json({ success: false, error: 'Failed to create product' });
    }
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
'''
    with open(os.path.join(PROJECT_DIR, 'src', 'index.ts'), 'w') as f:
        f.write(index_ts)

    # --- src/models/ ---
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'models'), exist_ok=True)
    product_model = '''export interface Product {
    id: string;
    name: string;
    sku: string;
    category: string;
    price: number;
    quantity: number;
    reorderLevel: number;
    supplier: string;
    lastUpdated: Date;
}

export interface ProductCreateInput {
    name: string;
    sku: string;
    category: string;
    price: number;
    quantity: number;
    reorderLevel?: number;
    supplier: string;
}

export interface InventoryReport {
    totalProducts: number;
    totalValue: number;
    lowStockItems: Product[];
    categoryBreakdown: Record<string, number>;
}
'''
    with open(os.path.join(PROJECT_DIR, 'src', 'models', 'product.ts'), 'w') as f:
        f.write(product_model)

    # --- src/services/ ---
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'services'), exist_ok=True)
    inventory_service = '''import { Product, ProductCreateInput, InventoryReport } from '../models/product';

export class InventoryService {
    private products: Map<string, Product> = new Map();

    async getAllProducts(): Promise<Product[]> {
        return Array.from(this.products.values());
    }

    async getProductById(id: string): Promise<Product | undefined> {
        return this.products.get(id);
    }

    async createProduct(input: ProductCreateInput): Promise<Product> {
        const product: Product = {
            id: this.generateId(),
            ...input,
            reorderLevel: input.reorderLevel ?? 10,
            lastUpdated: new Date(),
        };
        this.products.set(product.id, product);
        return product;
    }

    async updateQuantity(id: string, quantity: number): Promise<Product> {
        const product = this.products.get(id);
        if (!product) {
            throw new Error(`Product ${id} not found`);
        }
        product.quantity = quantity;
        product.lastUpdated = new Date();
        return product;
    }

    async generateReport(): Promise<InventoryReport> {
        const products = Array.from(this.products.values());
        const totalValue = products.reduce((sum, p) => sum + p.price * p.quantity, 0);
        const lowStockItems = products.filter(p => p.quantity <= p.reorderLevel);
        const categoryBreakdown: Record<string, number> = {};
        for (const p of products) {
            categoryBreakdown[p.category] = (categoryBreakdown[p.category] || 0) + 1;
        }
        return {
            totalProducts: products.length,
            totalValue,
            lowStockItems,
            categoryBreakdown,
        };
    }

    private generateId(): string {
        return `PRD-${Date.now()}-${Math.random().toString(36).substring(2, 8)}`;
    }
}
'''
    with open(os.path.join(PROJECT_DIR, 'src', 'services', 'inventoryService.ts'), 'w') as f:
        f.write(inventory_service)

    # --- src/config/ ---
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'config'), exist_ok=True)
    db_config = '''export interface DatabaseConfig {
    host: string;
    port: number;
    database: string;
    username: string;
    password: string;
    ssl: boolean;
}

export const defaultConfig: DatabaseConfig = {
    host: process.env.DB_HOST || 'localhost',
    port: parseInt(process.env.DB_PORT || '5432', 10),
    database: process.env.DB_NAME || 'inventory_db',
    username: process.env.DB_USER || 'admin',
    password: process.env.DB_PASSWORD || '',
    ssl: process.env.DB_SSL === 'true',
};
'''
    with open(os.path.join(PROJECT_DIR, 'src', 'config', 'database.ts'), 'w') as f:
        f.write(db_config)

    # --- VSCode settings (workspace-level) ---
    vscode_settings = {
        "typescript.tsdk": "node_modules/typescript/lib",
        "editor.formatOnSave": True,
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "typescript.preferences.importModuleSpecifier": "relative"
    }
    with open(os.path.join(VSCODE_DIR, 'settings.json'), 'w') as f:
        json.dump(vscode_settings, f, indent=4)

    # NO tasks.json — that's what the agent needs to create
    # Ensure no tasks.json exists
    tasks_path = os.path.join(VSCODE_DIR, 'tasks.json')
    if os.path.exists(tasks_path):
        os.remove(tasks_path)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'tsconfig.json: {os.path.join(PROJECT_DIR, "tsconfig.json")}')
    print(f'No tasks.json exists (agent must create it)')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

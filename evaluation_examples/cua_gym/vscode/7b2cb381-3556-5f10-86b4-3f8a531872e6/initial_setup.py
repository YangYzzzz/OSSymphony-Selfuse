"""
Initial Setup: Configure ESLint extension for auto-fix on save and onType
Task ID: vscode_we_072
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")
WORKSPACE_DIR = os.path.join(HOME, "workspace")


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
    # 1. Ensure VSCode user config directory exists
    os.makedirs(VSCODE_USER, exist_ok=True)

    # 2. Write empty settings.json (no ESLint config yet)
    with open(SETTINGS_PATH, "w") as f:
        json.dump({}, f, indent=4)
    print(f"Settings written: {SETTINGS_PATH}")

    # 3. Create a realistic TypeScript project workspace
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # package.json
    package_json = {
        "name": "inventory-tracker",
        "version": "1.0.0",
        "description": "Product inventory management system",
        "main": "src/index.ts",
        "scripts": {
            "build": "tsc",
            "lint": "eslint src/**/*.ts",
            "start": "node dist/index.js"
        },
        "dependencies": {
            "express": "^4.18.2",
            "pg": "^8.11.3"
        },
        "devDependencies": {
            "typescript": "^5.3.3",
            "@typescript-eslint/eslint-plugin": "^6.18.0",
            "@typescript-eslint/parser": "^6.18.0",
            "eslint": "^8.56.0"
        }
    }
    with open(os.path.join(WORKSPACE_DIR, "package.json"), "w") as f:
        json.dump(package_json, f, indent=2)

    # tsconfig.json
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
            "resolveJsonModule": True
        },
        "include": ["src/**/*"],
        "exclude": ["node_modules", "dist"]
    }
    with open(os.path.join(WORKSPACE_DIR, "tsconfig.json"), "w") as f:
        json.dump(tsconfig, f, indent=2)

    # .eslintrc.json
    eslintrc = {
        "env": {
            "node": True,
            "es2020": True
        },
        "extends": [
            "eslint:recommended"
        ],
        "parser": "@typescript-eslint/parser",
        "parserOptions": {
            "ecmaVersion": 2020,
            "sourceType": "module"
        },
        "plugins": ["@typescript-eslint"],
        "rules": {
            "no-unused-vars": "warn",
            "semi": ["error", "always"],
            "quotes": ["error", "single"]
        }
    }
    with open(os.path.join(WORKSPACE_DIR, ".eslintrc.json"), "w") as f:
        json.dump(eslintrc, f, indent=2)

    # src directory
    src_dir = os.path.join(WORKSPACE_DIR, "src")
    os.makedirs(src_dir, exist_ok=True)

    # src/index.ts
    index_ts = '''import express from 'express';
import { InventoryService } from './services/inventoryService';
import { ProductRouter } from './routes/productRoutes';

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

const inventoryService = new InventoryService();
const productRouter = new ProductRouter(inventoryService);

app.use('/api/products', productRouter.getRouter());

app.get('/health', (_req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.listen(PORT, () => {
    console.log(`Inventory Tracker API running on port ${PORT}`);
});
'''
    with open(os.path.join(src_dir, "index.ts"), "w") as f:
        f.write(index_ts)

    # src/models/product.ts
    models_dir = os.path.join(src_dir, "models")
    os.makedirs(models_dir, exist_ok=True)

    product_ts = '''export interface Product {
    id: string;
    name: string;
    sku: string;
    category: string;
    price: number;
    quantity: number;
    reorderLevel: number;
    supplier: string;
    lastRestocked: Date;
}

export interface ProductCreateInput {
    name: string;
    sku: string;
    category: string;
    price: number;
    quantity: number;
    reorderLevel: number;
    supplier: string;
}

export type ProductUpdateInput = Partial<ProductCreateInput>;
'''
    with open(os.path.join(models_dir, "product.ts"), "w") as f:
        f.write(product_ts)

    # src/services/inventoryService.ts
    services_dir = os.path.join(src_dir, "services")
    os.makedirs(services_dir, exist_ok=True)

    inventory_service_ts = '''import { Product, ProductCreateInput, ProductUpdateInput } from '../models/product';
import { v4 as uuidv4 } from 'uuid';

export class InventoryService {
    private products: Map<string, Product> = new Map();

    addProduct(input: ProductCreateInput): Product {
        const product: Product = {
            ...input,
            id: uuidv4(),
            lastRestocked: new Date()
        };
        this.products.set(product.id, product);
        return product;
    }

    getProduct(id: string): Product | undefined {
        return this.products.get(id);
    }

    getAllProducts(): Product[] {
        return Array.from(this.products.values());
    }

    updateProduct(id: string, updates: ProductUpdateInput): Product | undefined {
        const existing = this.products.get(id);
        if (!existing) return undefined;

        const updated: Product = { ...existing, ...updates };
        this.products.set(id, updated);
        return updated;
    }

    getLowStockProducts(): Product[] {
        return this.getAllProducts().filter(
            p => p.quantity <= p.reorderLevel
        );
    }

    getProductsByCategory(category: string): Product[] {
        return this.getAllProducts().filter(
            p => p.category === category
        );
    }
}
'''
    with open(os.path.join(services_dir, "inventoryService.ts"), "w") as f:
        f.write(inventory_service_ts)

    # src/routes/productRoutes.ts
    routes_dir = os.path.join(src_dir, "routes")
    os.makedirs(routes_dir, exist_ok=True)

    product_routes_ts = '''import { Router, Request, Response } from 'express';
import { InventoryService } from '../services/inventoryService';

export class ProductRouter {
    private router: Router;
    private service: InventoryService;

    constructor(service: InventoryService) {
        this.router = Router();
        this.service = service;
        this.setupRoutes();
    }

    private setupRoutes(): void {
        this.router.get('/', this.getAllProducts.bind(this));
        this.router.get('/low-stock', this.getLowStock.bind(this));
        this.router.get('/:id', this.getProduct.bind(this));
        this.router.post('/', this.createProduct.bind(this));
        this.router.put('/:id', this.updateProduct.bind(this));
    }

    getRouter(): Router {
        return this.router;
    }

    private getAllProducts(_req: Request, res: Response): void {
        const products = this.service.getAllProducts();
        res.json(products);
    }

    private getLowStock(_req: Request, res: Response): void {
        const products = this.service.getLowStockProducts();
        res.json(products);
    }

    private getProduct(req: Request, res: Response): void {
        const product = this.service.getProduct(req.params.id);
        if (!product) {
            res.status(404).json({ error: 'Product not found' });
            return;
        }
        res.json(product);
    }

    private createProduct(req: Request, res: Response): void {
        const product = this.service.addProduct(req.body);
        res.status(201).json(product);
    }

    private updateProduct(req: Request, res: Response): void {
        const product = this.service.updateProduct(req.params.id, req.body);
        if (!product) {
            res.status(404).json({ error: 'Product not found' });
            return;
        }
        res.json(product);
    }
}
'''
    with open(os.path.join(routes_dir, "productRoutes.ts"), "w") as f:
        f.write(product_routes_ts)

    print(f"TypeScript project created: {WORKSPACE_DIR}")

    # 4. Launch VSCode with the workspace
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


create_initial()

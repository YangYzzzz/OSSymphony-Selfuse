"""
Initial Setup: Configure workspace-level settings to enable strict null checks in TypeScript
Task ID: vscode_lp_028
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_028'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'strict-ts')
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


def create_initial():
    # 1. Create project directory structure
    os.makedirs(os.path.join(PROJECT_DIR, 'src'), exist_ok=True)

    # 2. Create tsconfig.json with strict: false and NO strictNullChecks
    tsconfig = {
        "compilerOptions": {
            "target": "ES2020",
            "module": "commonjs",
            "lib": ["ES2020"],
            "outDir": "./dist",
            "rootDir": "./src",
            "strict": False,
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
    print(f'Created tsconfig.json')

    # 3. Create package.json
    package = {
        "name": "strict-ts",
        "version": "1.0.0",
        "description": "Inventory management system for Meridian Electronics",
        "main": "dist/index.js",
        "scripts": {
            "build": "tsc",
            "start": "node dist/index.js",
            "dev": "ts-node src/index.ts"
        },
        "dependencies": {
            "typescript": "^5.3.3"
        }
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package, f, indent=2)
    print(f'Created package.json')

    # 4. Create TypeScript source files with potential null issues
    index_ts = '''import { InventoryService } from './services/inventory';
import { Product, WarehouseLocation } from './models/product';

const service = new InventoryService();

function displayProductInfo(productId: string) {
    const product = service.findProduct(productId);
    // Potential null issue: product could be undefined
    console.log(`Product: ${product.name}, Price: $${product.price.toFixed(2)}`);
    console.log(`Location: ${product.warehouse.building}-${product.warehouse.aisle}`);
}

function getDiscountedPrice(productId: string, discountPercent: number) {
    const product = service.findProduct(productId);
    // Potential null issue: product could be undefined
    const basePrice = product.price;
    return basePrice * (1 - discountPercent / 100);
}

function printWarehouseReport() {
    const locations = service.getWarehouseLocations();
    for (const loc of locations) {
        const manager = loc.assignedManager;
        // Potential null issue: manager could be null
        console.log(`${loc.building}-${loc.aisle}: managed by ${manager.name}`);
    }
}

displayProductInfo('SKU-4821');
const discounted = getDiscountedPrice('SKU-4821', 15);
console.log(`Discounted price: $${discounted.toFixed(2)}`);
printWarehouseReport();
'''
    with open(os.path.join(PROJECT_DIR, 'src', 'index.ts'), 'w') as f:
        f.write(index_ts)

    # Create models directory
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'models'), exist_ok=True)

    product_model = '''export interface WarehouseManager {
    name: string;
    employeeId: string;
    email: string;
}

export interface WarehouseLocation {
    building: string;
    aisle: string;
    shelf: number;
    assignedManager: WarehouseManager | null;
}

export interface Product {
    id: string;
    name: string;
    price: number;
    category: string;
    warehouse: WarehouseLocation;
    lastRestocked: Date | null;
    discontinuedAt: Date | null;
}
'''
    with open(os.path.join(PROJECT_DIR, 'src', 'models', 'product.ts'), 'w') as f:
        f.write(product_model)

    # Create services directory
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'services'), exist_ok=True)

    inventory_service = '''import { Product, WarehouseLocation } from '../models/product';

export class InventoryService {
    private products: Map<string, Product> = new Map();

    findProduct(id: string): Product | undefined {
        return this.products.get(id);
    }

    getWarehouseLocations(): WarehouseLocation[] {
        const locations: WarehouseLocation[] = [];
        for (const product of this.products.values()) {
            if (!locations.find(l => l.building === product.warehouse.building
                && l.aisle === product.warehouse.aisle)) {
                locations.push(product.warehouse);
            }
        }
        return locations;
    }

    addProduct(product: Product): void {
        this.products.set(product.id, product);
    }

    getProductsByCategory(category: string): Product[] {
        const results: Product[] = [];
        for (const product of this.products.values()) {
            if (product.category === category) {
                results.push(product);
            }
        }
        return results;
    }

    getRecentlyRestocked(daysAgo: number): Product[] {
        const cutoff = new Date();
        cutoff.setDate(cutoff.getDate() - daysAgo);
        const results: Product[] = [];
        for (const product of this.products.values()) {
            // Potential null issue: lastRestocked could be null
            if (product.lastRestocked > cutoff) {
                results.push(product);
            }
        }
        return results;
    }

    getDiscontinuedProducts(): Product[] {
        const results: Product[] = [];
        for (const product of this.products.values()) {
            if (product.discontinuedAt !== null) {
                results.push(product);
            }
        }
        return results;
    }
}
'''
    with open(os.path.join(PROJECT_DIR, 'src', 'services', 'inventory.ts'), 'w') as f:
        f.write(inventory_service)

    # Create utils
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'utils'), exist_ok=True)

    formatter_util = '''export function formatCurrency(amount: number | null): string {
    // Potential null issue: amount could be null
    return `$${amount.toFixed(2)}`;
}

export function formatDate(date: Date | null): string {
    // Potential null issue: date could be null
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

export function truncateString(str: string | null, maxLength: number): string {
    // Potential null issue: str could be null
    if (str.length <= maxLength) {
        return str;
    }
    return str.substring(0, maxLength - 3) + '...';
}
'''
    with open(os.path.join(PROJECT_DIR, 'src', 'utils', 'formatter.ts'), 'w') as f:
        f.write(formatter_util)

    print(f'Created TypeScript source files')

    # 5. Ensure user settings do NOT have TypeScript overrides
    os.makedirs(VSCODE_USER, exist_ok=True)
    user_settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                user_settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            user_settings = {}

    # Remove any TypeScript-related settings if present
    ts_keys_to_remove = [k for k in user_settings if k.startswith('typescript.')]
    for k in ts_keys_to_remove:
        del user_settings[k]

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(user_settings, f, indent=4)
    print(f'User settings cleaned of TypeScript overrides')

    # 6. Ensure NO .vscode/settings.json in the workspace
    vscode_ws_dir = os.path.join(PROJECT_DIR, '.vscode')
    vscode_ws_settings = os.path.join(vscode_ws_dir, 'settings.json')
    if os.path.exists(vscode_ws_settings):
        os.remove(vscode_ws_settings)
        print('Removed existing .vscode/settings.json')

    # 7. Launch VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

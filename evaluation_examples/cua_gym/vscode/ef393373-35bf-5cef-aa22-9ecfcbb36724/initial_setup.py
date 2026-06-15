"""
Initial Setup: Create a TypeScript api-server project for VSCode tasks.json task
Task ID: vscode_gf2_024
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf2_024'
PROJECT_DIR = f'{WORKDIR}/projects/api-server'

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
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)

    # DO NOT create .vscode/tasks.json - that's the task for the agent

    # package.json
    package_json = {
        "name": "api-server",
        "version": "1.0.0",
        "description": "RESTful API server for inventory management",
        "main": "dist/index.js",
        "scripts": {
            "build": "tsc",
            "start": "node dist/index.js",
            "dev": "ts-node src/index.ts"
        },
        "dependencies": {
            "express": "^4.18.2",
            "cors": "^2.8.5",
            "dotenv": "^16.3.1"
        },
        "devDependencies": {
            "typescript": "^5.3.3",
            "@types/express": "^4.17.21",
            "@types/cors": "^2.8.17",
            "@types/node": "^20.10.0",
            "ts-node": "^10.9.2"
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
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
            "resolveJsonModule": True,
            "declaration": True,
            "declarationMap": True,
            "sourceMap": True
        },
        "include": ["src/**/*"],
        "exclude": ["node_modules", "dist", "tests"]
    }
    with open(f'{PROJECT_DIR}/tsconfig.json', 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # src/index.ts - main entry point
    with open(f'{PROJECT_DIR}/src/index.ts', 'w') as f:
        f.write('''import express from 'express';
import cors from 'cors';
import { productRouter } from './routes/products';
import { orderRouter } from './routes/orders';

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

app.use('/api/products', productRouter);
app.use('/api/orders', orderRouter);

app.get('/health', (_req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.listen(PORT, () => {
  console.log(`API server running on port ${PORT}`);
});

export default app;
''')

    # src/routes/products.ts
    os.makedirs(f'{PROJECT_DIR}/src/routes', exist_ok=True)
    with open(f'{PROJECT_DIR}/src/routes/products.ts', 'w') as f:
        f.write('''import { Router, Request, Response } from 'express';

export const productRouter = Router();

interface Product {
  id: number;
  name: string;
  price: number;
  category: string;
  inStock: boolean;
}

const products: Product[] = [
  { id: 1, name: 'Wireless Keyboard', price: 59.99, category: 'Electronics', inStock: true },
  { id: 2, name: 'Ergonomic Mouse', price: 34.50, category: 'Electronics', inStock: true },
  { id: 3, name: 'USB-C Hub', price: 42.00, category: 'Accessories', inStock: false },
  { id: 4, name: 'Monitor Stand', price: 89.95, category: 'Furniture', inStock: true },
];

productRouter.get('/', (_req: Request, res: Response) => {
  res.json(products);
});

productRouter.get('/:id', (req: Request, res: Response) => {
  const product = products.find(p => p.id === parseInt(req.params.id));
  if (!product) {
    return res.status(404).json({ error: 'Product not found' });
  }
  res.json(product);
});
''')

    # src/routes/orders.ts
    with open(f'{PROJECT_DIR}/src/routes/orders.ts', 'w') as f:
        f.write('''import { Router, Request, Response } from 'express';

export const orderRouter = Router();

interface OrderItem {
  productId: number;
  quantity: number;
}

interface Order {
  id: number;
  customerName: string;
  items: OrderItem[];
  total: number;
  createdAt: string;
}

const orders: Order[] = [
  {
    id: 101,
    customerName: 'Sarah Chen',
    items: [{ productId: 1, quantity: 2 }, { productId: 3, quantity: 1 }],
    total: 161.98,
    createdAt: '2025-11-15T10:30:00Z',
  },
  {
    id: 102,
    customerName: 'Marcus Rivera',
    items: [{ productId: 4, quantity: 1 }],
    total: 89.95,
    createdAt: '2025-11-16T14:20:00Z',
  },
];

orderRouter.get('/', (_req: Request, res: Response) => {
  res.json(orders);
});

orderRouter.post('/', (req: Request, res: Response) => {
  const { customerName, items, total } = req.body;
  const newOrder: Order = {
    id: orders.length + 100 + 1,
    customerName,
    items,
    total,
    createdAt: new Date().toISOString(),
  };
  orders.push(newOrder);
  res.status(201).json(newOrder);
});
''')

    # src/models/types.ts
    os.makedirs(f'{PROJECT_DIR}/src/models', exist_ok=True)
    with open(f'{PROJECT_DIR}/src/models/types.ts', 'w') as f:
        f.write('''export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  timestamp: string;
}

export interface PaginationParams {
  page: number;
  limit: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}

export interface InventoryItem {
  sku: string;
  name: string;
  quantity: number;
  reorderPoint: number;
  warehouseLocation: string;
  lastUpdated: string;
}
''')

    # .gitignore
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write('''node_modules/
dist/
*.js.map
.env
.env.local
coverage/
''')

    # README.md
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write('''# API Server

RESTful API server for inventory management built with Express and TypeScript.

## Getting Started

```bash
npm install
npm run build
npm start
```

## Development

```bash
npm run dev
```

## API Endpoints

- `GET /health` - Health check
- `GET /api/products` - List all products
- `GET /api/products/:id` - Get product by ID
- `GET /api/orders` - List all orders
- `POST /api/orders` - Create a new order
''')

    print(f'Project created at: {PROJECT_DIR}')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()

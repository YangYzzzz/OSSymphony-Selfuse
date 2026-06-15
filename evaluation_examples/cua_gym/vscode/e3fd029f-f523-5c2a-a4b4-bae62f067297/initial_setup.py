"""
Initial Setup: Webpack TypeScript project with broken source map configuration
Task ID: vscode_fix_071
Domain: vs_code

Creates a realistic webpack-bundled TypeScript project where:
- webpack.config.js has devtool set to 'eval' (no proper source maps)
- .vscode/launch.json has incorrect sourceMapPathOverrides
- Breakpoints will show as unverified during debugging
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_fix_071'
PROJECT_DIR = os.path.join(WORKDIR, 'webpack-ts-project')


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
    # Create directory structure
    os.makedirs(os.path.join(PROJECT_DIR, 'src'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'dist'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, '.vscode'), exist_ok=True)

    # --- package.json ---
    package_json = {
        "name": "inventory-dashboard",
        "version": "2.1.0",
        "description": "Warehouse inventory tracking dashboard",
        "main": "dist/bundle.js",
        "scripts": {
            "build": "webpack --mode development",
            "build:prod": "webpack --mode production",
            "start": "webpack serve --mode development",
            "debug": "webpack --mode development && node dist/bundle.js"
        },
        "dependencies": {
            "chart.js": "^4.4.1",
            "date-fns": "^3.2.0"
        },
        "devDependencies": {
            "typescript": "^5.3.3",
            "webpack": "^5.90.1",
            "webpack-cli": "^5.1.4",
            "webpack-dev-server": "^4.15.2",
            "ts-loader": "^9.5.1",
            "html-webpack-plugin": "^5.6.0"
        }
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # --- tsconfig.json ---
    tsconfig = {
        "compilerOptions": {
            "target": "ES2020",
            "module": "ES2020",
            "lib": ["ES2020", "DOM"],
            "outDir": "./dist",
            "rootDir": "./src",
            "strict": True,
            "esModuleInterop": True,
            "sourceMap": True,
            "declaration": True,
            "moduleResolution": "node",
            "resolveJsonModule": True,
            "skipLibCheck": True,
            "forceConsistentCasingInFileNames": True
        },
        "include": ["src/**/*"],
        "exclude": ["node_modules", "dist"]
    }
    with open(os.path.join(PROJECT_DIR, 'tsconfig.json'), 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # --- webpack.config.js (BROKEN: devtool is 'eval') ---
    webpack_config = """const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  entry: './src/index.ts',
  devtool: 'eval',
  module: {
    rules: [
      {
        test: /\\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
    ],
  },
  resolve: {
    extensions: ['.tsx', '.ts', '.js'],
  },
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist'),
    clean: true,
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './src/index.html',
    }),
  ],
  devServer: {
    static: './dist',
    port: 3000,
    hot: true,
  },
};
"""
    with open(os.path.join(PROJECT_DIR, 'webpack.config.js'), 'w') as f:
        f.write(webpack_config)

    # --- .vscode/launch.json (BROKEN: incorrect sourceMapPathOverrides) ---
    launch_json = {
        "version": "0.2.0",
        "configurations": [
            {
                "type": "node",
                "request": "launch",
                "name": "Debug Webpack Bundle",
                "program": "${workspaceFolder}/dist/bundle.js",
                "preLaunchTask": "npm: build",
                "outFiles": ["${workspaceFolder}/dist/**/*.js"],
                "sourceMaps": True,
                "sourceMapPathOverrides": {
                    "webpack:///./~/*": "${workspaceFolder}/node_modules/*",
                    "webpack:///./*": "${workspaceFolder}/src/*"
                },
                "console": "integratedTerminal",
                "skipFiles": ["<node_internals>/**"]
            },
            {
                "type": "node",
                "request": "launch",
                "name": "Run Tests",
                "program": "${workspaceFolder}/node_modules/.bin/jest",
                "args": ["--runInBand"],
                "console": "integratedTerminal"
            }
        ]
    }
    with open(os.path.join(PROJECT_DIR, '.vscode', 'launch.json'), 'w') as f:
        json.dump(launch_json, f, indent=2)

    # --- .vscode/tasks.json ---
    tasks_json = {
        "version": "2.0.0",
        "tasks": [
            {
                "type": "npm",
                "script": "build",
                "group": {
                    "kind": "build",
                    "isDefault": True
                },
                "problemMatcher": ["$tsc-watch"],
                "label": "npm: build"
            }
        ]
    }
    with open(os.path.join(PROJECT_DIR, '.vscode', 'tasks.json'), 'w') as f:
        json.dump(tasks_json, f, indent=2)

    # --- src/index.ts ---
    index_ts = '''import { InventoryTracker } from './services/inventoryTracker';
import { ReportGenerator } from './services/reportGenerator';
import { WarehouseLocation } from './models/warehouse';
import { formatDate, calculateDaysBetween } from './utils/dateHelpers';

const WAREHOUSE_LOCATIONS: WarehouseLocation[] = [
  { id: 'WH-001', name: 'Portland Main', capacity: 50000, region: 'Pacific Northwest' },
  { id: 'WH-002', name: 'Austin Distribution', capacity: 35000, region: 'South Central' },
  { id: 'WH-003', name: 'Chicago Hub', capacity: 75000, region: 'Midwest' },
  { id: 'WH-004', name: 'Atlanta Fulfillment', capacity: 42000, region: 'Southeast' },
];

async function initializeDashboard(): Promise<void> {
  console.log(`[${formatDate(new Date())}] Initializing Inventory Dashboard v2.1.0`);

  const tracker = new InventoryTracker(WAREHOUSE_LOCATIONS);
  await tracker.loadCurrentStock();

  const lowStockItems = tracker.getLowStockAlerts(100);
  if (lowStockItems.length > 0) {
    console.warn(`WARNING: ${lowStockItems.length} items below reorder threshold`);
    lowStockItems.forEach(item => {
      console.warn(`  - ${item.sku}: ${item.quantity} units at ${item.location}`);
    });
  }

  const reportGen = new ReportGenerator(tracker);
  const weeklyReport = await reportGen.generateWeeklyReport();
  console.log(`Weekly report generated: ${weeklyReport.totalItems} items across ${weeklyReport.warehouseCount} warehouses`);

  const lastRestock = new Date('2025-12-15');
  const daysSinceRestock = calculateDaysBetween(lastRestock, new Date());
  console.log(`Days since last major restock: ${daysSinceRestock}`);
}

initializeDashboard().catch(err => {
  console.error('Dashboard initialization failed:', err.message);
  process.exit(1);
});
'''
    with open(os.path.join(PROJECT_DIR, 'src', 'index.ts'), 'w') as f:
        f.write(index_ts)

    # --- src/models/warehouse.ts ---
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'models'), exist_ok=True)
    warehouse_ts = '''export interface WarehouseLocation {
  id: string;
  name: string;
  capacity: number;
  region: string;
}

export interface StockItem {
  sku: string;
  name: string;
  quantity: number;
  location: string;
  reorderPoint: number;
  unitCost: number;
  lastUpdated: Date;
}

export interface StockMovement {
  id: string;
  sku: string;
  fromWarehouse: string;
  toWarehouse: string;
  quantity: number;
  timestamp: Date;
  reason: 'restock' | 'transfer' | 'return' | 'damaged';
}

export interface WeeklyReport {
  generatedAt: Date;
  totalItems: number;
  totalValue: number;
  warehouseCount: number;
  lowStockAlerts: StockItem[];
  recentMovements: StockMovement[];
}
'''
    with open(os.path.join(PROJECT_DIR, 'src', 'models', 'warehouse.ts'), 'w') as f:
        f.write(warehouse_ts)

    # --- src/services/inventoryTracker.ts ---
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'services'), exist_ok=True)
    inventory_tracker_ts = '''import { WarehouseLocation, StockItem } from '../models/warehouse';

export class InventoryTracker {
  private warehouses: WarehouseLocation[];
  private stock: StockItem[] = [];

  constructor(warehouses: WarehouseLocation[]) {
    this.warehouses = warehouses;
  }

  async loadCurrentStock(): Promise<void> {
    // Simulated stock data for dashboard demo
    this.stock = [
      { sku: 'ELC-4521', name: 'Circuit Board Assembly Kit', quantity: 2340, location: 'WH-001', reorderPoint: 500, unitCost: 45.99, lastUpdated: new Date('2026-01-08') },
      { sku: 'MEC-1187', name: 'Precision Bearing Set', quantity: 89, location: 'WH-002', reorderPoint: 200, unitCost: 12.50, lastUpdated: new Date('2026-01-05') },
      { sku: 'OPT-3302', name: 'Fiber Optic Cable 50m', quantity: 1560, location: 'WH-003', reorderPoint: 300, unitCost: 78.00, lastUpdated: new Date('2026-01-10') },
      { sku: 'HYD-7744', name: 'Hydraulic Valve Assembly', quantity: 45, location: 'WH-001', reorderPoint: 100, unitCost: 234.00, lastUpdated: new Date('2026-01-03') },
      { sku: 'ELC-9981', name: 'LED Panel 60x60', quantity: 3200, location: 'WH-004', reorderPoint: 400, unitCost: 32.75, lastUpdated: new Date('2026-01-09') },
      { sku: 'MEC-5563', name: 'Stainless Steel Fastener Pack', quantity: 12800, location: 'WH-003', reorderPoint: 2000, unitCost: 5.25, lastUpdated: new Date('2026-01-11') },
      { sku: 'PLM-2240', name: 'PVC Pipe Connector Set', quantity: 67, location: 'WH-002', reorderPoint: 150, unitCost: 8.99, lastUpdated: new Date('2026-01-02') },
      { sku: 'ELC-6670', name: 'Voltage Regulator Module', quantity: 890, location: 'WH-004', reorderPoint: 250, unitCost: 19.50, lastUpdated: new Date('2026-01-07') },
    ];
    console.log(`Loaded ${this.stock.length} stock items from ${this.warehouses.length} warehouses`);
  }

  getLowStockAlerts(threshold?: number): StockItem[] {
    return this.stock.filter(item => {
      const effectiveThreshold = threshold ?? item.reorderPoint;
      return item.quantity < effectiveThreshold;
    });
  }

  getStockByWarehouse(warehouseId: string): StockItem[] {
    return this.stock.filter(item => item.location === warehouseId);
  }

  getTotalInventoryValue(): number {
    return this.stock.reduce((sum, item) => sum + (item.quantity * item.unitCost), 0);
  }
}
'''
    with open(os.path.join(PROJECT_DIR, 'src', 'services', 'inventoryTracker.ts'), 'w') as f:
        f.write(inventory_tracker_ts)

    # --- src/services/reportGenerator.ts ---
    report_generator_ts = '''import { InventoryTracker } from './inventoryTracker';
import { WeeklyReport, StockMovement } from '../models/warehouse';

export class ReportGenerator {
  private tracker: InventoryTracker;

  constructor(tracker: InventoryTracker) {
    this.tracker = tracker;
  }

  async generateWeeklyReport(): Promise<WeeklyReport> {
    const lowStock = this.tracker.getLowStockAlerts();
    const totalValue = this.tracker.getTotalInventoryValue();

    const recentMovements: StockMovement[] = [
      { id: 'MOV-001', sku: 'ELC-4521', fromWarehouse: 'WH-003', toWarehouse: 'WH-001', quantity: 500, timestamp: new Date('2026-01-09'), reason: 'transfer' },
      { id: 'MOV-002', sku: 'MEC-1187', fromWarehouse: 'WH-001', toWarehouse: 'WH-002', quantity: 300, timestamp: new Date('2026-01-08'), reason: 'restock' },
      { id: 'MOV-003', sku: 'HYD-7744', fromWarehouse: 'WH-004', toWarehouse: 'WH-001', quantity: 50, timestamp: new Date('2026-01-07'), reason: 'return' },
    ];

    return {
      generatedAt: new Date(),
      totalItems: 8,
      totalValue: totalValue,
      warehouseCount: 4,
      lowStockAlerts: lowStock,
      recentMovements: recentMovements,
    };
  }
}
'''
    with open(os.path.join(PROJECT_DIR, 'src', 'services', 'reportGenerator.ts'), 'w') as f:
        f.write(report_generator_ts)

    # --- src/utils/dateHelpers.ts ---
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'utils'), exist_ok=True)
    date_helpers_ts = '''export function formatDate(date: Date): string {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  return `${year}-${month}-${day} ${hours}:${minutes}`;
}

export function calculateDaysBetween(start: Date, end: Date): number {
  const msPerDay = 1000 * 60 * 60 * 24;
  const diffMs = Math.abs(end.getTime() - start.getTime());
  return Math.floor(diffMs / msPerDay);
}

export function isBusinessDay(date: Date): boolean {
  const day = date.getDay();
  return day !== 0 && day !== 6;
}

export function getNextBusinessDay(date: Date): Date {
  const next = new Date(date);
  do {
    next.setDate(next.getDate() + 1);
  } while (!isBusinessDay(next));
  return next;
}
'''
    with open(os.path.join(PROJECT_DIR, 'src', 'utils', 'dateHelpers.ts'), 'w') as f:
        f.write(date_helpers_ts)

    # --- src/index.html ---
    index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Inventory Dashboard</title>
  <style>
    body { font-family: 'Segoe UI', Tahoma, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
    .header { background: #1a73e8; color: white; padding: 16px 24px; border-radius: 8px; margin-bottom: 20px; }
    .card { background: white; border-radius: 8px; padding: 16px; margin-bottom: 16px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .alert { border-left: 4px solid #ea4335; }
    table { width: 100%; border-collapse: collapse; }
    th, td { text-align: left; padding: 8px 12px; border-bottom: 1px solid #e0e0e0; }
    th { background: #f8f9fa; font-weight: 600; }
  </style>
</head>
<body>
  <div class="header">
    <h1>Warehouse Inventory Dashboard</h1>
    <p>Real-time stock tracking across all locations</p>
  </div>
  <div id="app">Loading dashboard...</div>
</body>
</html>
'''
    with open(os.path.join(PROJECT_DIR, 'src', 'index.html'), 'w') as f:
        f.write(index_html)

    # --- README.md ---
    readme = '''# Inventory Dashboard

Warehouse inventory tracking dashboard built with TypeScript and webpack.

## Development

```bash
npm install
npm run build
npm start
```

## Debugging

Use the "Debug Webpack Bundle" launch configuration in VSCode.
Note: Source maps must be properly configured in webpack for breakpoints to work.

## Project Structure

```
src/
  index.ts          - Entry point
  models/           - TypeScript interfaces
  services/         - Business logic
  utils/            - Helper functions
```
'''
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write(readme)

    print(f'Project created: {PROJECT_DIR}')

    # GUI-ready: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_project()

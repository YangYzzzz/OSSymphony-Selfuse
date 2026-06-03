"""
Initial Setup: Set up TypeScript project with long relative imports (no path aliases)
Task ID: vscode_lp_039
Domain: vs_code
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_039'
PROJECT_DIR = f'{WORKDIR}/{TASK_ID}'


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
    dirs = [
        f'{PROJECT_DIR}/src/components',
        f'{PROJECT_DIR}/src/utils',
        f'{PROJECT_DIR}/src/services',
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # --- tsconfig.json (basic config, NO path aliases, NO baseUrl) ---
    tsconfig = {
        "compilerOptions": {
            "target": "ES2020",
            "module": "commonjs",
            "lib": ["ES2020", "DOM"],
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
    with open(f'{PROJECT_DIR}/tsconfig.json', 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # --- package.json ---
    package = {
        "name": "inventory-management-api",
        "version": "2.1.0",
        "description": "Backend API for warehouse inventory management system",
        "main": "dist/index.js",
        "scripts": {
            "build": "tsc",
            "start": "node dist/index.js",
            "dev": "ts-node src/index.ts"
        },
        "dependencies": {
            "express": "^4.18.2",
            "pg": "^8.11.3",
            "redis": "^4.6.10"
        },
        "devDependencies": {
            "typescript": "^5.3.3",
            "@types/express": "^4.17.21",
            "@types/node": "^20.10.0",
            "ts-node": "^10.9.2"
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package, f, indent=2)

    # --- src/utils/logger.ts ---
    with open(f'{PROJECT_DIR}/src/utils/logger.ts', 'w') as f:
        f.write('''import * as fs from 'fs';

export enum LogLevel {
  DEBUG = 'DEBUG',
  INFO = 'INFO',
  WARN = 'WARN',
  ERROR = 'ERROR',
}

export class Logger {
  private context: string;
  private level: LogLevel;

  constructor(context: string, level: LogLevel = LogLevel.INFO) {
    this.context = context;
    this.level = level;
  }

  info(message: string, data?: Record<string, unknown>): void {
    console.log(`[${new Date().toISOString()}] [${this.context}] INFO: ${message}`, data || '');
  }

  error(message: string, error?: Error): void {
    console.error(`[${new Date().toISOString()}] [${this.context}] ERROR: ${message}`, error?.stack || '');
  }

  warn(message: string): void {
    console.warn(`[${new Date().toISOString()}] [${this.context}] WARN: ${message}`);
  }

  debug(message: string, data?: Record<string, unknown>): void {
    if (this.level === LogLevel.DEBUG) {
      console.debug(`[${new Date().toISOString()}] [${this.context}] DEBUG: ${message}`, data || '');
    }
  }
}
''')

    # --- src/utils/validators.ts ---
    with open(f'{PROJECT_DIR}/src/utils/validators.ts', 'w') as f:
        f.write('''export function isValidSKU(sku: string): boolean {
  const skuPattern = /^[A-Z]{2,4}-\\d{4,8}$/;
  return skuPattern.test(sku);
}

export function isPositiveInteger(value: number): boolean {
  return Number.isInteger(value) && value > 0;
}

export function isValidEmail(email: string): boolean {
  const emailPattern = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
  return emailPattern.test(email);
}

export function sanitizeString(input: string): string {
  return input.replace(/[<>"'&]/g, '').trim();
}

export function isValidDateRange(start: Date, end: Date): boolean {
  return start < end;
}
''')

    # --- src/services/database.ts ---
    with open(f'{PROJECT_DIR}/src/services/database.ts', 'w') as f:
        f.write('''import { Logger } from '../../utils/logger';

const logger = new Logger('DatabaseService');

export interface ConnectionConfig {
  host: string;
  port: number;
  database: string;
  user: string;
  password: string;
  maxConnections: number;
}

export class DatabaseService {
  private config: ConnectionConfig;
  private isConnected: boolean = false;

  constructor(config: ConnectionConfig) {
    this.config = config;
  }

  async connect(): Promise<void> {
    try {
      logger.info(`Connecting to ${this.config.host}:${this.config.port}/${this.config.database}`);
      // Simulated connection logic
      this.isConnected = true;
      logger.info('Database connection established successfully');
    } catch (error) {
      logger.error('Failed to connect to database', error as Error);
      throw error;
    }
  }

  async disconnect(): Promise<void> {
    if (this.isConnected) {
      this.isConnected = false;
      logger.info('Database connection closed');
    }
  }

  async query<T>(sql: string, params?: unknown[]): Promise<T[]> {
    if (!this.isConnected) {
      throw new Error('Database not connected');
    }
    logger.debug('Executing query', { sql, params });
    return [] as T[];
  }
}
''')

    # --- src/services/cacheService.ts ---
    with open(f'{PROJECT_DIR}/src/services/cacheService.ts', 'w') as f:
        f.write('''import { Logger } from '../../utils/logger';

const logger = new Logger('CacheService');

export class CacheService {
  private store: Map<string, { value: unknown; expiresAt: number }> = new Map();
  private defaultTTL: number;

  constructor(defaultTTL: number = 3600) {
    this.defaultTTL = defaultTTL;
  }

  set(key: string, value: unknown, ttl?: number): void {
    const expiresAt = Date.now() + (ttl || this.defaultTTL) * 1000;
    this.store.set(key, { value, expiresAt });
    logger.debug(`Cache set: ${key}`, { ttl: ttl || this.defaultTTL });
  }

  get<T>(key: string): T | null {
    const entry = this.store.get(key);
    if (!entry) return null;
    if (Date.now() > entry.expiresAt) {
      this.store.delete(key);
      return null;
    }
    return entry.value as T;
  }

  invalidate(pattern: string): number {
    let count = 0;
    const regex = new RegExp(pattern);
    for (const key of this.store.keys()) {
      if (regex.test(key)) {
        this.store.delete(key);
        count++;
      }
    }
    logger.info(`Invalidated ${count} cache entries matching: ${pattern}`);
    return count;
  }

  clear(): void {
    const size = this.store.size;
    this.store.clear();
    logger.info(`Cache cleared: ${size} entries removed`);
  }
}
''')

    # --- src/components/InventoryItem.ts ---
    with open(f'{PROJECT_DIR}/src/components/InventoryItem.ts', 'w') as f:
        f.write('''import { isValidSKU, isPositiveInteger } from '../../utils/validators';
import { Logger } from '../../utils/logger';
import { DatabaseService } from '../../services/database';

const logger = new Logger('InventoryItem');

export interface InventoryRecord {
  id: number;
  sku: string;
  name: string;
  quantity: number;
  warehouseLocation: string;
  lastRestocked: Date;
  unitPrice: number;
  supplier: string;
}

export class InventoryItem {
  private record: InventoryRecord;
  private db: DatabaseService;

  constructor(record: InventoryRecord, db: DatabaseService) {
    if (!isValidSKU(record.sku)) {
      throw new Error(`Invalid SKU format: ${record.sku}`);
    }
    if (!isPositiveInteger(record.quantity)) {
      logger.warn(`Non-positive quantity for ${record.sku}: ${record.quantity}`);
    }
    this.record = record;
    this.db = db;
  }

  get sku(): string {
    return this.record.sku;
  }

  get totalValue(): number {
    return this.record.quantity * this.record.unitPrice;
  }

  async updateQuantity(delta: number): Promise<void> {
    const newQty = this.record.quantity + delta;
    if (newQty < 0) {
      throw new Error(`Insufficient stock for ${this.record.sku}: have ${this.record.quantity}, need ${-delta}`);
    }
    this.record.quantity = newQty;
    logger.info(`Updated ${this.record.sku} quantity: ${newQty}`);
  }

  needsRestock(threshold: number = 10): boolean {
    return this.record.quantity < threshold;
  }

  toJSON(): InventoryRecord {
    return { ...this.record };
  }
}
''')

    # --- src/components/WarehouseReport.ts ---
    with open(f'{PROJECT_DIR}/src/components/WarehouseReport.ts', 'w') as f:
        f.write('''import { InventoryItem, InventoryRecord } from './InventoryItem';
import { Logger } from '../../utils/logger';
import { CacheService } from '../../services/cacheService';

const logger = new Logger('WarehouseReport');

export interface ReportSummary {
  totalItems: number;
  totalValue: number;
  lowStockItems: string[];
  topSuppliers: { name: string; itemCount: number }[];
  generatedAt: Date;
}

export class WarehouseReport {
  private items: InventoryItem[];
  private cache: CacheService;

  constructor(items: InventoryItem[], cache: CacheService) {
    this.items = items;
    this.cache = cache;
  }

  generateSummary(lowStockThreshold: number = 10): ReportSummary {
    const cached = this.cache.get<ReportSummary>('warehouse-summary');
    if (cached) {
      logger.info('Returning cached warehouse summary');
      return cached;
    }

    const summary: ReportSummary = {
      totalItems: this.items.length,
      totalValue: this.items.reduce((sum, item) => sum + item.totalValue, 0),
      lowStockItems: this.items
        .filter(item => item.needsRestock(lowStockThreshold))
        .map(item => item.sku),
      topSuppliers: [],
      generatedAt: new Date(),
    };

    this.cache.set('warehouse-summary', summary, 300);
    logger.info('Generated new warehouse summary', {
      totalItems: summary.totalItems,
      totalValue: summary.totalValue,
    });
    return summary;
  }
}
''')

    # --- src/index.ts (main entry point with long relative imports) ---
    with open(f'{PROJECT_DIR}/src/index.ts', 'w') as f:
        f.write('''import { Logger, LogLevel } from './utils/logger';
import { DatabaseService } from './services/database';
import { CacheService } from './services/cacheService';
import { InventoryItem } from './components/InventoryItem';
import { WarehouseReport } from './components/WarehouseReport';
import { isValidSKU } from './utils/validators';

const logger = new Logger('Main', LogLevel.INFO);

async function main(): Promise<void> {
  logger.info('Starting Inventory Management API');

  const db = new DatabaseService({
    host: 'localhost',
    port: 5432,
    database: 'inventory_db',
    user: 'admin',
    password: process.env.DB_PASSWORD || 'dev_password',
    maxConnections: 20,
  });

  await db.connect();

  const cache = new CacheService(600);

  logger.info('All services initialized successfully');
  logger.info('API server ready on port 3000');
}

main().catch((error) => {
  logger.error('Application startup failed', error);
  process.exit(1);
});
''')

    print(f'Initial project created: {PROJECT_DIR}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

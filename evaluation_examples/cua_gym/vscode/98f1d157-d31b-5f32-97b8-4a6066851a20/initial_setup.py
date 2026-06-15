"""
Initial Setup: Configure a TypeScript project for Error Lens extension testing
Task ID: vscode_gf2_037
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf2_037'
PROJECT_DIR = f'{WORKDIR}/projects/ts-app'
VSCODE_USER = os.path.expanduser('~/.config/Code/User')
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
    # --- Create project directory structure ---
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/models', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/utils', exist_ok=True)

    # --- package.json ---
    package_json = {
        "name": "ts-app",
        "version": "1.0.0",
        "description": "Customer analytics dashboard application",
        "main": "dist/index.js",
        "scripts": {
            "build": "tsc",
            "start": "node dist/index.js",
            "dev": "ts-node src/index.ts"
        },
        "dependencies": {
            "express": "^4.18.2",
            "pg": "^8.11.3"
        },
        "devDependencies": {
            "typescript": "^5.3.3",
            "@types/express": "^4.17.21",
            "@types/node": "^20.10.6",
            "ts-node": "^10.9.2"
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
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
    with open(f'{PROJECT_DIR}/tsconfig.json', 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # --- src/index.ts (has intentional type errors) ---
    index_ts = '''\
import { CustomerRecord, AnalyticsReport } from "./models/customer";
import { calculateMetrics, formatCurrency } from "./utils/helpers";

// Application entry point for customer analytics dashboard
const PORT: number = 3000;

interface ServerConfig {
    port: number;
    host: string;
    debug: boolean;
    maxConnections: number;
}

// Type error: 'debug' should be boolean, not string
const config: ServerConfig = {
    port: PORT,
    host: "localhost",
    debug: "yes",
    maxConnections: 100,
};

function processCustomerData(customers: CustomerRecord[]): AnalyticsReport {
    const totalRevenue = customers.reduce((sum, c) => sum + c.totalSpent, 0);
    const avgOrderValue = totalRevenue / customers.length;

    // Type error: returning number where string is expected
    const reportTitle: string = 42;

    return {
        title: reportTitle,
        generatedAt: new Date(),
        totalCustomers: customers.length,
        totalRevenue: totalRevenue,
        averageOrderValue: avgOrderValue,
    };
}

// Type error: passing wrong argument type
const sampleCustomers: CustomerRecord[] = [
    { id: 1, name: "Elena Rodriguez", email: "elena@acme.com", totalSpent: 15420.50, joinDate: "2023-04-12" },
    { id: 2, name: "James Park", email: "james@globex.net", totalSpent: 8930.00, joinDate: "2024-01-08" },
    { id: 3, name: "Aisha Patel", email: "aisha@initech.io", totalSpent: 22100.75, joinDate: "2022-11-30" },
];

const report = processCustomerData(sampleCustomers);
console.log(`Report: ${report.title} - ${formatCurrency(report.totalRevenue)}`);

// Type error: accessing non-existent property
console.log(`Summary: ${report.summaryText}`);
'''
    with open(f'{PROJECT_DIR}/src/index.ts', 'w') as f:
        f.write(index_ts)

    # --- src/models/customer.ts ---
    customer_ts = '''\
export interface CustomerRecord {
    id: number;
    name: string;
    email: string;
    totalSpent: number;
    joinDate: string;
}

export interface AnalyticsReport {
    title: string;
    generatedAt: Date;
    totalCustomers: number;
    totalRevenue: number;
    averageOrderValue: number;
}

export interface OrderItem {
    productId: number;
    productName: string;
    quantity: number;
    unitPrice: number;
    discount: number;
}

export interface Order {
    orderId: string;
    customerId: number;
    items: OrderItem[];
    status: "pending" | "shipped" | "delivered" | "cancelled";
    createdAt: Date;
}

export function createCustomer(
    name: string,
    email: string,
): CustomerRecord {
    return {
        id: Math.floor(Math.random() * 10000),
        name,
        email,
        totalSpent: 0,
        joinDate: new Date().toISOString().split("T")[0],
    };
}
'''
    with open(f'{PROJECT_DIR}/src/models/customer.ts', 'w') as f:
        f.write(customer_ts)

    # --- src/utils/helpers.ts ---
    helpers_ts = '''\
export function formatCurrency(amount: number): string {
    return new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
    }).format(amount);
}

export function calculateMetrics(values: number[]): {
    mean: number;
    median: number;
    stdDev: number;
} {
    const n = values.length;
    if (n === 0) {
        return { mean: 0, median: 0, stdDev: 0 };
    }

    const mean = values.reduce((s, v) => s + v, 0) / n;
    const sorted = [...values].sort((a, b) => a - b);
    const median =
        n % 2 === 0
            ? (sorted[n / 2 - 1] + sorted[n / 2]) / 2
            : sorted[Math.floor(n / 2)];
    const variance = values.reduce((s, v) => s + (v - mean) ** 2, 0) / n;
    const stdDev = Math.sqrt(variance);

    return { mean, median, stdDev };
}

export function validateEmail(email: string): boolean {
    const pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$/;
    return pattern.test(email);
}

export function generateReportId(): string {
    const timestamp = Date.now().toString(36);
    const random = Math.random().toString(36).substring(2, 8);
    return `RPT-${timestamp}-${random}`.toUpperCase();
}
'''
    with open(f'{PROJECT_DIR}/src/utils/helpers.ts', 'w') as f:
        f.write(helpers_ts)

    # --- Ensure VSCode settings exist but do NOT contain errorLens config ---
    os.makedirs(VSCODE_USER, exist_ok=True)
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}
    # Remove any errorLens settings if they exist
    keys_to_remove = [k for k in settings if k.startswith('errorLens.')]
    for k in keys_to_remove:
        del settings[k]
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    # --- Ensure Error Lens extension is NOT installed ---
    subprocess.run(['code', '--uninstall-extension', 'usernamehw.errorlens'],
                   capture_output=True, text=True)
    print(f'Project created at: {PROJECT_DIR}')
    print(f'Settings cleaned at: {SETTINGS_PATH}')

    # --- Launch VSCode with the project ---
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

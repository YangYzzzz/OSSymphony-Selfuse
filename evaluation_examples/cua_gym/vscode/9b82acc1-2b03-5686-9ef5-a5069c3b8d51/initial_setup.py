"""
Initial Setup: Create a TypeScript pricing file with duplicated calculation blocks and magic numbers
Task ID: vscode_web_045
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_045'
PROJECT_DIR = f'{WORKDIR}/projects/webapp'
SRC_DIR = f'{PROJECT_DIR}/src/utils'
OUTPUT = f'{SRC_DIR}/pricing.ts'


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
    os.makedirs(SRC_DIR, exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/components', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/models', exist_ok=True)

    # Create package.json
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        f.write("""{
  "name": "webapp",
  "version": "1.0.0",
  "description": "E-commerce pricing module",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "test": "jest"
  },
  "dependencies": {
    "typescript": "^5.3.0"
  }
}
""")

    # Create tsconfig.json
    with open(f'{PROJECT_DIR}/tsconfig.json', 'w') as f:
        f.write("""{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "strict": true,
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*"]
}
""")

    # Create the pricing.ts file with duplicated code and magic number
    # Line numbers are carefully counted (1-indexed)
    content = '''// pricing.ts - E-commerce pricing utilities
// Handles cart calculations, discounts, and tax computation

export interface CartItem {
  name: string;
  price: number;
  quantity: number;
  discountPercent: number;
}

const SHIPPING_THRESHOLD = 100;
const taxRate = 0.0875;
const LOYALTY_DISCOUNT = 0.05;

export function getShippingCost(subtotal: number): number {
  if (subtotal >= SHIPPING_THRESHOLD) {
    return 0;
  }
  return 12.99;
}

export function applyLoyaltyDiscount(total: number, isMember: boolean): number {
  if (isMember) {
    return total * (1 - LOYALTY_DISCOUNT);
  }
  return total;
}

export function calculateOrderTotal(items: CartItem[]): number {
  let subtotal = 0;
  for (const item of items) {
    const basePrice = item.price * item.quantity;
    const discountAmount = basePrice * (item.discountPercent / 100);
    const itemTotal = basePrice - discountAmount;
    subtotal += itemTotal;
  }
  const shipping = getShippingCost(subtotal);
  const tax = subtotal * taxRate;
  return subtotal + tax + shipping;
}

export function calculateRefundAmount(items: CartItem[]): number {
  let subtotal = 0;
  for (const item of items) {
    const basePrice = item.price * item.quantity;
    const discountAmount = basePrice * (item.discountPercent / 100);
    const itemTotal = basePrice - discountAmount;
    subtotal += itemTotal;
  }
  const tax = subtotal * taxRate;
  return subtotal + tax;
}

export function previewCartSubtotal(items: CartItem[]): number {
  let subtotal = 0;
  for (const item of items) {
    const basePrice = item.price * item.quantity;
    const discountAmount = basePrice * (item.discountPercent / 100);
    const itemTotal = basePrice - discountAmount;
    subtotal += itemTotal;
  }
  return subtotal;
}

export function formatCurrency(amount: number): string {
  return `$${amount.toFixed(2)}`;
}

export function generateInvoiceSummary(
  items: CartItem[],
  isMember: boolean
): string {
  const orderTotal = calculateOrderTotal(items);
  const finalTotal = applyLoyaltyDiscount(orderTotal, isMember);
  const savings = orderTotal - finalTotal;
  return [
    `Items: ${items.length}`,
    `Order Total: ${formatCurrency(orderTotal)}`,
    `Loyalty Savings: ${formatCurrency(savings)}`,
    `Final Total: ${formatCurrency(finalTotal)}`,
  ].join("\\n");
}
'''

    with open(OUTPUT, 'w') as f:
        f.write(content)

    print(f'Initial file created: {OUTPUT}')

    # Create a simple additional file for realistic project structure
    with open(f'{PROJECT_DIR}/src/models/cart.ts', 'w') as f:
        f.write('''// cart.ts - Cart data model

export interface Cart {
  id: string;
  userId: string;
  items: CartItem[];
  createdAt: Date;
  updatedAt: Date;
}

export interface CartItem {
  productId: string;
  name: string;
  price: number;
  quantity: number;
  discountPercent: number;
}

export function createEmptyCart(userId: string): Cart {
  return {
    id: crypto.randomUUID(),
    userId,
    items: [],
    createdAt: new Date(),
    updatedAt: new Date(),
  };
}
''')

    with open(f'{PROJECT_DIR}/src/components/CartView.ts', 'w') as f:
        f.write('''// CartView.ts - Cart display component

import { formatCurrency, calculateOrderTotal } from "../utils/pricing";
import type { CartItem } from "../utils/pricing";

export function renderCartView(items: CartItem[]): string {
  const total = calculateOrderTotal(items);
  const lines = items.map(
    (item) =>
      `${item.name} x${item.quantity} @ ${formatCurrency(item.price)}`
  );
  lines.push(`Total: ${formatCurrency(total)}`);
  return lines.join("\\n");
}
''')

    # GUI-ready startup: open VSCode with the project and the specific file
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

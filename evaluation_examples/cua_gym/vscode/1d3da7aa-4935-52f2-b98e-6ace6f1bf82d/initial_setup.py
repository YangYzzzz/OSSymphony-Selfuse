"""
Initial Setup: Configure VSCode with a TypeScript project, inlay hints disabled
Task ID: vscode_web_066
Domain: vs_code
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_066'
PROJECT_DIR = f'{WORKDIR}/projects/react-ts-app'
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
    """Create a realistic React TypeScript project structure."""
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'components'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'services'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'types'), exist_ok=True)

    # tsconfig.json
    tsconfig = {
        "compilerOptions": {
            "target": "ES2020",
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
            "jsx": "react-jsx",
            "outDir": "./dist"
        },
        "include": ["src"]
    }
    with open(os.path.join(PROJECT_DIR, 'tsconfig.json'), 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # package.json
    package = {
        "name": "react-ts-app",
        "version": "1.2.0",
        "private": True,
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "typescript": "^5.3.3",
            "axios": "^1.6.5"
        },
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test"
        }
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package, f, indent=2)

    # src/types/models.ts
    models_ts = '''export interface User {
  id: number;
  name: string;
  email: string;
  role: "admin" | "editor" | "viewer";
  lastLogin: Date;
}

export interface Product {
  sku: string;
  title: string;
  price: number;
  category: string;
  inStock: boolean;
  rating: number;
}

export interface OrderItem {
  product: Product;
  quantity: number;
  discount: number;
}

export interface Order {
  orderId: string;
  customer: User;
  items: OrderItem[];
  createdAt: Date;
  status: "pending" | "shipped" | "delivered" | "cancelled";
}
'''
    with open(os.path.join(PROJECT_DIR, 'src', 'types', 'models.ts'), 'w') as f:
        f.write(models_ts)

    # src/services/api.ts - functions without explicit return types
    api_ts = '''import { User, Product, Order } from "../types/models";

const API_BASE = "https://api.example.com/v2";

export function fetchUser(userId: number, includeProfile: boolean) {
  const url = `${API_BASE}/users/${userId}`;
  const params = includeProfile ? "?include=profile" : "";
  return fetch(url + params).then(res => res.json()) as Promise<User>;
}

export function searchProducts(query: string, maxResults: number, sortBy: string) {
  const params = new URLSearchParams({
    q: query,
    limit: String(maxResults),
    sort: sortBy,
  });
  return fetch(`${API_BASE}/products?${params}`).then(res => res.json()) as Promise<Product[]>;
}

export function calculateOrderTotal(items: { price: number; quantity: number; discount: number }[]) {
  const subtotal = items.reduce((sum, item) => {
    const itemTotal = item.price * item.quantity * (1 - item.discount / 100);
    return sum + itemTotal;
  }, 0);
  const tax = subtotal * 0.085;
  return { subtotal, tax, total: subtotal + tax };
}

export function formatCurrency(amount: number, locale: string, currencyCode: string) {
  return new Intl.NumberFormat(locale, {
    style: "currency",
    currency: currencyCode,
  }).format(amount);
}

export async function submitOrder(customerId: number, items: { sku: string; qty: number }[], shippingMethod: string) {
  const response = await fetch(`${API_BASE}/orders`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ customerId, items, shippingMethod }),
  });
  return response.json() as Promise<Order>;
}
'''
    with open(os.path.join(PROJECT_DIR, 'src', 'services', 'api.ts'), 'w') as f:
        f.write(api_ts)

    # src/components/UserCard.tsx
    usercard_tsx = '''import React from "react";
import { User } from "../types/models";
import { fetchUser, formatCurrency } from "../services/api";

interface UserCardProps {
  userId: number;
  showBalance: boolean;
}

function formatDate(date: Date) {
  return date.toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

function getRoleBadgeColor(role: string) {
  const colorMap: Record<string, string> = {
    admin: "#e74c3c",
    editor: "#3498db",
    viewer: "#95a5a6",
  };
  return colorMap[role] || "#bdc3c7";
}

const UserCard: React.FC<UserCardProps> = ({ userId, showBalance }) => {
  const [user, setUser] = React.useState<User | null>(null);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    fetchUser(userId, true).then((data) => {
      setUser(data);
      setLoading(false);
    });
  }, [userId]);

  if (loading) return <div className="skeleton-card" />;
  if (!user) return <div>User not found</div>;

  const badgeColor = getRoleBadgeColor(user.role);
  const loginDate = formatDate(user.lastLogin);

  return (
    <div className="user-card">
      <h3>{user.name}</h3>
      <p className="email">{user.email}</p>
      <span className="badge" style={{ backgroundColor: badgeColor }}>
        {user.role}
      </span>
      <p className="last-login">Last login: {loginDate}</p>
      {showBalance && (
        <p className="balance">
          Balance: {formatCurrency(1250.75, "en-US", "USD")}
        </p>
      )}
    </div>
  );
};

export default UserCard;
'''
    with open(os.path.join(PROJECT_DIR, 'src', 'components', 'UserCard.tsx'), 'w') as f:
        f.write(usercard_tsx)

    # src/App.tsx
    app_tsx = '''import React from "react";
import UserCard from "./components/UserCard";
import { searchProducts, calculateOrderTotal } from "./services/api";

function App() {
  const [products, setProducts] = React.useState<any[]>([]);

  React.useEffect(() => {
    searchProducts("electronics", 20, "price_asc").then(setProducts);
  }, []);

  const sampleItems = [
    { price: 29.99, quantity: 2, discount: 10 },
    { price: 149.50, quantity: 1, discount: 0 },
    { price: 9.99, quantity: 5, discount: 15 },
  ];

  const orderSummary = calculateOrderTotal(sampleItems);

  return (
    <div className="app">
      <header>
        <h1>Dashboard</h1>
      </header>
      <main>
        <section>
          <h2>User Profile</h2>
          <UserCard userId={42} showBalance={true} />
        </section>
        <section>
          <h2>Order Summary</h2>
          <p>Subtotal: ${orderSummary.subtotal.toFixed(2)}</p>
          <p>Tax: ${orderSummary.tax.toFixed(2)}</p>
          <p>Total: ${orderSummary.total.toFixed(2)}</p>
        </section>
        <section>
          <h2>Products ({products.length})</h2>
          <ul>
            {products.map((p, i) => (
              <li key={i}>{p.title} - ${p.price}</li>
            ))}
          </ul>
        </section>
      </main>
    </div>
  );
}

export default App;
'''
    with open(os.path.join(PROJECT_DIR, 'src', 'App.tsx'), 'w') as f:
        f.write(app_tsx)

    print(f'Project created at: {PROJECT_DIR}')


def setup_vscode_settings():
    """Set up VSCode settings with TypeScript inlay hints DISABLED."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings or start fresh
    try:
        with open(SETTINGS_PATH, 'r') as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    # Explicitly disable TypeScript inlay hints
    settings.update({
        "editor.fontSize": 14,
        "editor.tabSize": 2,
        "editor.minimap.enabled": True,
        "workbench.colorTheme": "Default Dark Modern",
        "typescript.inlayHints.parameterNames.enabled": "none",
        "typescript.inlayHints.functionLikeReturnTypes.enabled": False,
        "typescript.inlayHints.variableTypes.enabled": False,
        "typescript.inlayHints.propertyDeclarationTypes.enabled": False,
        "typescript.inlayHints.parameterTypes.enabled": False,
        "typescript.inlayHints.enumMemberValues.enabled": False,
    })

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f'VSCode settings written to: {SETTINGS_PATH}')


def main():
    create_project()
    setup_vscode_settings()

    # Launch VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()

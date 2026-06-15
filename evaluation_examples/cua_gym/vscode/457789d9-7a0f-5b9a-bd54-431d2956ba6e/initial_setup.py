"""
Initial Setup: Create a webapp project with basic Playwright config (no accessibility testing)
Task ID: vscode_gf3_071
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_071'
PROJECT_DIR = f'{WORKDIR}/projects/webapp'


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
    os.makedirs(f'{PROJECT_DIR}/src/components', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/pages', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests/e2e', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/public', exist_ok=True)

    # package.json - basic webapp with Playwright (NO @axe-core/playwright)
    package_json = {
        "name": "webapp",
        "version": "1.0.0",
        "description": "Customer portal web application",
        "scripts": {
            "dev": "vite",
            "build": "tsc && vite build",
            "preview": "vite preview",
            "test": "vitest",
            "test:e2e": "playwright test"
        },
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.20.0"
        },
        "devDependencies": {
            "@playwright/test": "^1.40.0",
            "@types/react": "^18.2.37",
            "@types/react-dom": "^18.2.15",
            "typescript": "^5.2.2",
            "vite": "^5.0.0",
            "@vitejs/plugin-react": "^4.2.0",
            "vitest": "^1.0.0"
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # tsconfig.json
    tsconfig = {
        "compilerOptions": {
            "target": "ES2020",
            "useDefineForClassFields": True,
            "lib": ["ES2020", "DOM", "DOM.Iterable"],
            "module": "ESNext",
            "skipLibCheck": True,
            "moduleResolution": "bundler",
            "allowImportingTsExtensions": True,
            "resolveJsonModule": True,
            "isolatedModules": True,
            "noEmit": True,
            "jsx": "react-jsx",
            "strict": True,
            "noUnusedLocals": True,
            "noUnusedParameters": True,
            "noFallthroughCasesInSwitch": True
        },
        "include": ["src"],
        "references": [{"path": "./tsconfig.node.json"}]
    }
    with open(f'{PROJECT_DIR}/tsconfig.json', 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # playwright.config.ts - basic config WITHOUT accessibility project
    playwright_config = '''import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
  },
});
'''
    with open(f'{PROJECT_DIR}/playwright.config.ts', 'w') as f:
        f.write(playwright_config)

    # Existing e2e test
    e2e_test = '''import { test, expect } from '@playwright/test';

test.describe('Homepage', () => {
  test('should display the welcome message', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('h1')).toContainText('Welcome');
  });

  test('should navigate to login page', async ({ page }) => {
    await page.goto('/');
    await page.click('a[href="/login"]');
    await expect(page).toHaveURL(/.*login/);
  });

  test('should show featured products', async ({ page }) => {
    await page.goto('/');
    const products = page.locator('.product-card');
    await expect(products).toHaveCount(6);
  });
});
'''
    with open(f'{PROJECT_DIR}/tests/e2e/homepage.spec.ts', 'w') as f:
        f.write(e2e_test)

    # src/App.tsx
    app_tsx = '''import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import ProductPage from './pages/ProductPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/products/:id" element={<ProductPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
'''
    with open(f'{PROJECT_DIR}/src/App.tsx', 'w') as f:
        f.write(app_tsx)

    # src/pages/HomePage.tsx
    homepage_tsx = '''import React from 'react';
import ProductCard from '../components/ProductCard';

const featuredProducts = [
  { id: 1, name: 'Wireless Headphones', price: 79.99, rating: 4.5 },
  { id: 2, name: 'Mechanical Keyboard', price: 129.99, rating: 4.8 },
  { id: 3, name: 'USB-C Hub', price: 49.99, rating: 4.2 },
  { id: 4, name: 'Monitor Stand', price: 89.99, rating: 4.6 },
  { id: 5, name: 'Webcam HD', price: 59.99, rating: 4.3 },
  { id: 6, name: 'Desk Lamp', price: 34.99, rating: 4.7 },
];

export default function HomePage() {
  return (
    <main>
      <h1>Welcome to TechStore</h1>
      <p>Find the best tech accessories for your workspace.</p>
      <section className="featured-products">
        <h2>Featured Products</h2>
        <div className="product-grid">
          {featuredProducts.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </section>
    </main>
  );
}
'''
    with open(f'{PROJECT_DIR}/src/pages/HomePage.tsx', 'w') as f:
        f.write(homepage_tsx)

    # src/pages/LoginPage.tsx
    login_tsx = '''import React, { useState } from 'react';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Login attempt:', email);
  };

  return (
    <main>
      <h1>Sign In</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Sign In</button>
      </form>
    </main>
  );
}
'''
    with open(f'{PROJECT_DIR}/src/pages/LoginPage.tsx', 'w') as f:
        f.write(login_tsx)

    # src/pages/ProductPage.tsx
    product_tsx = '''import React from 'react';
import { useParams } from 'react-router-dom';

export default function ProductPage() {
  const { id } = useParams<{ id: string }>();

  return (
    <main>
      <h1>Product Details</h1>
      <p>Viewing product #{id}</p>
    </main>
  );
}
'''
    with open(f'{PROJECT_DIR}/src/pages/ProductPage.tsx', 'w') as f:
        f.write(product_tsx)

    # src/components/ProductCard.tsx
    product_card = '''import React from 'react';

interface Product {
  id: number;
  name: string;
  price: number;
  rating: number;
}

interface ProductCardProps {
  product: Product;
}

export default function ProductCard({ product }: ProductCardProps) {
  return (
    <div className="product-card">
      <h3>{product.name}</h3>
      <p className="price">${product.price.toFixed(2)}</p>
      <p className="rating">Rating: {product.rating}/5</p>
      <a href={`/products/${product.id}`}>View Details</a>
    </div>
  );
}
'''
    with open(f'{PROJECT_DIR}/src/components/ProductCard.tsx', 'w') as f:
        f.write(product_card)

    # index.html
    index_html = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>TechStore - Workspace Accessories</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
'''
    with open(f'{PROJECT_DIR}/index.html', 'w') as f:
        f.write(index_html)

    # src/main.tsx
    main_tsx = '''import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
'''
    with open(f'{PROJECT_DIR}/src/main.tsx', 'w') as f:
        f.write(main_tsx)

    # vite.config.ts
    vite_config = '''import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
});
'''
    with open(f'{PROJECT_DIR}/vite.config.ts', 'w') as f:
        f.write(vite_config)

    print(f'Initial project created: {PROJECT_DIR}')

    # Open VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

"""
Initial Setup: Next.js project with API routes and SSR pages, no debug configuration
Task ID: vscode_web_044
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_044'
PROJECT_DIR = f'{WORKDIR}/projects/next-app'


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
        f'{PROJECT_DIR}/pages/api',
        f'{PROJECT_DIR}/styles',
        f'{PROJECT_DIR}/components',
        f'{PROJECT_DIR}/public',
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # package.json — standard Next.js project, NO debug script
    package_json = {
        "name": "next-app",
        "version": "1.0.0",
        "private": True,
        "scripts": {
            "dev": "next dev",
            "build": "next build",
            "start": "next start",
            "lint": "next lint"
        },
        "dependencies": {
            "next": "14.1.0",
            "react": "18.2.0",
            "react-dom": "18.2.0"
        },
        "devDependencies": {
            "eslint": "8.56.0",
            "eslint-config-next": "14.1.0"
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # next.config.js
    with open(f'{PROJECT_DIR}/next.config.js', 'w') as f:
        f.write("""/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
};

module.exports = nextConfig;
""")

    # pages/index.js — home page
    with open(f'{PROJECT_DIR}/pages/index.js', 'w') as f:
        f.write("""import Head from 'next/head';
import styles from '../styles/Home.module.css';

export default function Home() {
  return (
    <div className={styles.container}>
      <Head>
        <title>Acme Dashboard</title>
        <meta name="description" content="Acme Corp internal dashboard" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>
          Welcome to <a href="/products">Acme Dashboard</a>
        </h1>

        <p className={styles.description}>
          Internal product management and analytics platform
        </p>

        <div className={styles.grid}>
          <a href="/products" className={styles.card}>
            <h2>Products &rarr;</h2>
            <p>Browse and manage the product catalog with real-time inventory data.</p>
          </a>

          <a href="/api/hello" className={styles.card}>
            <h2>API Status &rarr;</h2>
            <p>Check the health and status of backend API endpoints.</p>
          </a>
        </div>
      </main>
    </div>
  );
}
""")

    # pages/api/hello.js — API route
    with open(f'{PROJECT_DIR}/pages/api/hello.js', 'w') as f:
        f.write("""// API route: /api/hello
// Returns a JSON greeting with server timestamp

export default function handler(req, res) {
  const { name } = req.query;
  const greeting = name ? `Hello, ${name}!` : 'Hello, World!';

  res.status(200).json({
    message: greeting,
    timestamp: new Date().toISOString(),
    server: 'next-app-api',
    version: '1.0.0',
  });
}
""")

    # pages/api/products.js — another API route
    with open(f'{PROJECT_DIR}/pages/api/products.js', 'w') as f:
        f.write("""// API route: /api/products
// Returns product catalog data

const products = [
  { id: 1, name: 'Wireless Keyboard', price: 79.99, stock: 142 },
  { id: 2, name: 'Ergonomic Mouse', price: 54.50, stock: 87 },
  { id: 3, name: 'USB-C Hub', price: 42.00, stock: 203 },
  { id: 4, name: '27-inch Monitor', price: 349.99, stock: 31 },
  { id: 5, name: 'Webcam HD Pro', price: 119.00, stock: 65 },
];

export default function handler(req, res) {
  if (req.method === 'GET') {
    const { category, minPrice } = req.query;
    let filtered = [...products];

    if (minPrice) {
      filtered = filtered.filter(p => p.price >= parseFloat(minPrice));
    }

    res.status(200).json({
      products: filtered,
      total: filtered.length,
      fetchedAt: new Date().toISOString(),
    });
  } else {
    res.setHeader('Allow', ['GET']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
""")

    # pages/products.js — page with getServerSideProps
    with open(f'{PROJECT_DIR}/pages/products.js', 'w') as f:
        f.write("""import styles from '../styles/Home.module.css';

export async function getServerSideProps(context) {
  // In production, this would fetch from an external API or database
  const products = [
    { id: 1, name: 'Wireless Keyboard', price: 79.99, stock: 142, category: 'Peripherals' },
    { id: 2, name: 'Ergonomic Mouse', price: 54.50, stock: 87, category: 'Peripherals' },
    { id: 3, name: 'USB-C Hub', price: 42.00, stock: 203, category: 'Accessories' },
    { id: 4, name: '27-inch Monitor', price: 349.99, stock: 31, category: 'Displays' },
    { id: 5, name: 'Webcam HD Pro', price: 119.00, stock: 65, category: 'Peripherals' },
    { id: 6, name: 'Standing Desk', price: 599.00, stock: 18, category: 'Furniture' },
    { id: 7, name: 'Noise-Cancelling Headphones', price: 249.99, stock: 54, category: 'Audio' },
    { id: 8, name: 'Laptop Stand', price: 38.50, stock: 176, category: 'Accessories' },
  ];

  const totalValue = products.reduce((sum, p) => sum + p.price * p.stock, 0);

  return {
    props: {
      products,
      totalValue: totalValue.toFixed(2),
      lastUpdated: new Date().toISOString(),
    },
  };
}

export default function Products({ products, totalValue, lastUpdated }) {
  return (
    <div className={styles.container}>
      <main className={styles.main}>
        <h1 className={styles.title}>Product Catalog</h1>
        <p>Total inventory value: ${totalValue}</p>
        <p>Last updated: {lastUpdated}</p>

        <table style={{ borderCollapse: 'collapse', width: '100%', marginTop: '2rem' }}>
          <thead>
            <tr>
              <th style={{ border: '1px solid #ddd', padding: '8px' }}>Name</th>
              <th style={{ border: '1px solid #ddd', padding: '8px' }}>Category</th>
              <th style={{ border: '1px solid #ddd', padding: '8px' }}>Price</th>
              <th style={{ border: '1px solid #ddd', padding: '8px' }}>Stock</th>
            </tr>
          </thead>
          <tbody>
            {products.map((product) => (
              <tr key={product.id}>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{product.name}</td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{product.category}</td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>${product.price.toFixed(2)}</td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{product.stock}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </main>
    </div>
  );
}
""")

    # styles/Home.module.css
    with open(f'{PROJECT_DIR}/styles/Home.module.css', 'w') as f:
        f.write(""".container {
  padding: 0 2rem;
}

.main {
  min-height: 100vh;
  padding: 4rem 0;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.title {
  margin: 0;
  line-height: 1.15;
  font-size: 3rem;
  text-align: center;
}

.title a {
  color: #0070f3;
  text-decoration: none;
}

.description {
  text-align: center;
  margin: 1rem 0;
  line-height: 1.5;
  font-size: 1.2rem;
}

.grid {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  max-width: 800px;
  margin-top: 2rem;
}

.card {
  margin: 1rem;
  padding: 1.5rem;
  text-align: left;
  color: inherit;
  text-decoration: none;
  border: 1px solid #eaeaea;
  border-radius: 10px;
  transition: color 0.15s ease, border-color 0.15s ease;
  max-width: 300px;
}

.card:hover {
  color: #0070f3;
  border-color: #0070f3;
}

.card h2 {
  margin: 0 0 1rem 0;
  font-size: 1.3rem;
}

.card p {
  margin: 0;
  font-size: 1.1rem;
  line-height: 1.5;
}
""")

    # styles/globals.css
    with open(f'{PROJECT_DIR}/styles/globals.css', 'w') as f:
        f.write("""html,
body {
  padding: 0;
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen,
    Ubuntu, Cantarell, Fira Sans, Droid Sans, Helvetica Neue, sans-serif;
}

a {
  color: inherit;
  text-decoration: none;
}

* {
  box-sizing: border-box;
}
""")

    # pages/_app.js
    with open(f'{PROJECT_DIR}/pages/_app.js', 'w') as f:
        f.write("""import '../styles/globals.css';

function MyApp({ Component, pageProps }) {
  return <Component {...pageProps} />;
}

export default MyApp;
""")

    # components/Layout.js — reusable layout component
    with open(f'{PROJECT_DIR}/components/Layout.js', 'w') as f:
        f.write("""import Head from 'next/head';

export default function Layout({ children, title = 'Acme Dashboard' }) {
  return (
    <>
      <Head>
        <title>{title}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>
      <nav style={{ padding: '1rem 2rem', borderBottom: '1px solid #eaeaea' }}>
        <a href="/" style={{ fontWeight: 'bold', fontSize: '1.2rem' }}>Acme Dashboard</a>
        <a href="/products" style={{ marginLeft: '2rem' }}>Products</a>
      </nav>
      <main>{children}</main>
    </>
  );
}
""")

    # .gitignore
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write("""# dependencies
/node_modules
/.pnp
.pnp.js

# testing
/coverage

# next.js
/.next/
/out/

# production
/build

# misc
.DS_Store
*.pem

# debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# local env files
.env*.local

# vercel
.vercel

# typescript
*.tsbuildinfo
next-env.d.ts
""")

    # README.md
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write("""# Acme Dashboard (Next.js)

Internal product management and analytics dashboard for Acme Corp.

## Getting Started

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the dashboard.

## Project Structure

- `pages/` - Next.js pages and API routes
- `pages/api/` - Backend API endpoints
- `components/` - Reusable React components
- `styles/` - CSS modules and global styles
- `public/` - Static assets

## API Routes

- `GET /api/hello?name=<name>` - Health check / greeting
- `GET /api/products` - Product catalog data
""")

    # NOTE: No .vscode directory, no launch.json — that's the task
    print(f'Initial project created at: {PROJECT_DIR}')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

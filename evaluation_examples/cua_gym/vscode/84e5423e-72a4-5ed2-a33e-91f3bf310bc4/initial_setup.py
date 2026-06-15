"""
Initial Setup: Configure VSCode to exclude directories from search and file watching
Task ID: vscode_web_040
Domain: vscode

Creates a realistic Next.js project structure and opens VSCode with no
exclusion settings configured. node_modules, .next, and dist are present
and will appear in search and file watching.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_040'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'next-app')
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


def create_project_structure():
    """Create a realistic Next.js project directory tree."""
    # Main project files
    dirs = [
        os.path.join(PROJECT_DIR, 'src', 'pages'),
        os.path.join(PROJECT_DIR, 'src', 'components'),
        os.path.join(PROJECT_DIR, 'src', 'styles'),
        os.path.join(PROJECT_DIR, 'public', 'images'),
        # These are the directories that should be excluded from search/watching
        os.path.join(PROJECT_DIR, 'node_modules', 'react'),
        os.path.join(PROJECT_DIR, 'node_modules', 'next', 'dist'),
        os.path.join(PROJECT_DIR, 'node_modules', '@types', 'react'),
        os.path.join(PROJECT_DIR, '.next', 'static', 'chunks'),
        os.path.join(PROJECT_DIR, '.next', 'cache'),
        os.path.join(PROJECT_DIR, 'dist', 'static'),
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # package.json
    write_file(os.path.join(PROJECT_DIR, 'package.json'), json.dumps({
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
            "@types/react": "18.2.48",
            "typescript": "5.3.3"
        }
    }, indent=2))

    # next.config.js
    write_file(os.path.join(PROJECT_DIR, 'next.config.js'), """\
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: ['cdn.example.com'],
  },
};

module.exports = nextConfig;
""")

    # tsconfig.json
    write_file(os.path.join(PROJECT_DIR, 'tsconfig.json'), json.dumps({
        "compilerOptions": {
            "target": "es5",
            "lib": ["dom", "dom.iterable", "esnext"],
            "allowJs": True,
            "skipLibCheck": True,
            "strict": True,
            "noEmit": True,
            "esModuleInterop": True,
            "module": "esnext",
            "moduleResolution": "bundler",
            "resolveJsonModule": True,
            "isolatedModules": True,
            "jsx": "preserve",
            "incremental": True,
            "paths": {"@/*": ["./src/*"]}
        },
        "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx"],
        "exclude": ["node_modules"]
    }, indent=2))

    # src/pages/index.tsx
    write_file(os.path.join(PROJECT_DIR, 'src', 'pages', 'index.tsx'), """\
import Head from 'next/head';
import { ProductCard } from '../components/ProductCard';
import styles from '../styles/Home.module.css';

interface Product {
  id: number;
  name: string;
  price: number;
  category: string;
}

const products: Product[] = [
  { id: 1, name: 'Wireless Headphones', price: 79.99, category: 'Electronics' },
  { id: 2, name: 'Organic Coffee Beans', price: 24.50, category: 'Food' },
  { id: 3, name: 'Yoga Mat Premium', price: 45.00, category: 'Fitness' },
  { id: 4, name: 'LED Desk Lamp', price: 34.99, category: 'Home' },
];

export default function Home() {
  return (
    <div className={styles.container}>
      <Head>
        <title>NextShop - Your Marketplace</title>
        <meta name="description" content="Browse our curated product selection" />
      </Head>
      <main className={styles.main}>
        <h1 className={styles.title}>Welcome to NextShop</h1>
        <div className={styles.grid}>
          {products.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </main>
    </div>
  );
}
""")

    # src/pages/about.tsx
    write_file(os.path.join(PROJECT_DIR, 'src', 'pages', 'about.tsx'), """\
import Head from 'next/head';
import styles from '../styles/Home.module.css';

export default function About() {
  return (
    <div className={styles.container}>
      <Head>
        <title>About - NextShop</title>
      </Head>
      <main className={styles.main}>
        <h1>About NextShop</h1>
        <p>NextShop was founded in 2024 by a team of passionate developers
        who wanted to create the best online shopping experience.</p>
        <p>Our mission is to connect buyers with high-quality products
        from trusted sellers around the world.</p>
      </main>
    </div>
  );
}
""")

    # src/components/ProductCard.tsx
    write_file(os.path.join(PROJECT_DIR, 'src', 'components', 'ProductCard.tsx'), """\
import styles from '../styles/ProductCard.module.css';

interface ProductCardProps {
  product: {
    id: number;
    name: string;
    price: number;
    category: string;
  };
}

export function ProductCard({ product }: ProductCardProps) {
  return (
    <div className={styles.card}>
      <h3>{product.name}</h3>
      <span className={styles.category}>{product.category}</span>
      <p className={styles.price}>${product.price.toFixed(2)}</p>
      <button className={styles.addToCart}>Add to Cart</button>
    </div>
  );
}
""")

    # src/styles/Home.module.css
    write_file(os.path.join(PROJECT_DIR, 'src', 'styles', 'Home.module.css'), """\
.container {
  min-height: 100vh;
  padding: 0 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.main {
  padding: 4rem 0;
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.title {
  margin: 0;
  line-height: 1.15;
  font-size: 3rem;
  text-align: center;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  max-width: 1000px;
  margin-top: 2rem;
}
""")

    # src/styles/ProductCard.module.css
    write_file(os.path.join(PROJECT_DIR, 'src', 'styles', 'ProductCard.module.css'), """\
.card {
  padding: 1.5rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  transition: box-shadow 0.2s ease;
}

.card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.category {
  display: inline-block;
  background: #f0f0f0;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.85rem;
  color: #666;
}

.price {
  font-size: 1.25rem;
  font-weight: 700;
  color: #2d8cf0;
}

.addToCart {
  width: 100%;
  padding: 0.5rem;
  background: #2d8cf0;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
""")

    # node_modules files (enough to show up in search)
    write_file(os.path.join(PROJECT_DIR, 'node_modules', 'react', 'index.js'),
               'module.exports = require("./cjs/react.production.min.js");\n')
    write_file(os.path.join(PROJECT_DIR, 'node_modules', 'react', 'package.json'),
               json.dumps({"name": "react", "version": "18.2.0", "main": "index.js"}, indent=2))
    write_file(os.path.join(PROJECT_DIR, 'node_modules', 'next', 'dist', 'server.js'),
               '// Next.js server runtime\nconst http = require("http");\n')
    write_file(os.path.join(PROJECT_DIR, 'node_modules', '@types', 'react', 'index.d.ts'),
               'declare module "react" {\n  export function useState<T>(init: T): [T, (v: T) => void];\n}\n')

    # .next build output files
    write_file(os.path.join(PROJECT_DIR, '.next', 'static', 'chunks', 'main.js'),
               '// Compiled Next.js chunk\n(self.__next_f=self.__next_f||[]).push([0]);\n')
    write_file(os.path.join(PROJECT_DIR, '.next', 'cache', 'webpack.cache'),
               'WEBPACK_CACHE_BINARY_PLACEHOLDER\n')
    write_file(os.path.join(PROJECT_DIR, '.next', 'BUILD_ID'), 'a1b2c3d4e5f6\n')

    # dist output files
    write_file(os.path.join(PROJECT_DIR, 'dist', 'static', 'bundle.js'),
               '// Production bundle output\nvar app=function(){console.log("NextShop")};\n')
    write_file(os.path.join(PROJECT_DIR, 'dist', 'index.html'),
               '<!DOCTYPE html><html><head><title>NextShop</title></head><body><div id="root"></div><script src="static/bundle.js"></script></body></html>\n')

    # .gitignore
    write_file(os.path.join(PROJECT_DIR, '.gitignore'), """\
node_modules/
.next/
dist/
.env.local
""")

    # README.md
    write_file(os.path.join(PROJECT_DIR, 'README.md'), """\
# NextShop

A modern e-commerce storefront built with Next.js 14, React 18, and TypeScript.

## Getting Started

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

## Project Structure

- `src/pages/` - Next.js pages and API routes
- `src/components/` - Reusable React components
- `src/styles/` - CSS Modules
- `public/` - Static assets
""")


def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)


def setup_vscode_settings():
    """Ensure VSCode settings exist but WITHOUT any exclusion settings for the target dirs."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings or start fresh
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Ensure NO search.exclude, files.watcherExclude have the target patterns
    # Remove them if they exist (clean state)
    for key in ['search.exclude', 'files.watcherExclude']:
        if key in settings:
            for pattern in ['**/node_modules', '**/node_modules/**',
                            '**/.next', '**/.next/**',
                            '**/dist', '**/dist/**',
                            'node_modules', '.next', 'dist']:
                settings[key].pop(pattern, None)
            # Remove the key entirely if empty
            if not settings[key]:
                del settings[key]

    # Also ensure files.exclude doesn't have these (should remain visible)
    if 'files.exclude' in settings:
        for pattern in ['**/node_modules', '**/.next', '**/dist',
                        'node_modules', '.next', 'dist']:
            settings['files.exclude'].pop(pattern, None)

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'VSCode settings configured (no exclusions): {SETTINGS_PATH}')


def main():
    create_project_structure()
    print(f'Project structure created: {PROJECT_DIR}')

    setup_vscode_settings()

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()

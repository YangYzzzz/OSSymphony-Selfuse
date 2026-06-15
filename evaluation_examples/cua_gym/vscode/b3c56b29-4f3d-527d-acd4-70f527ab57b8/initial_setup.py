"""
Initial Setup: Configure a Chrome debugging launch configuration for a React app
Task ID: vscode_web_022
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_022'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'react-app')


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
    src_dir = os.path.join(PROJECT_DIR, 'src')
    components_dir = os.path.join(src_dir, 'components')
    public_dir = os.path.join(PROJECT_DIR, 'public')
    os.makedirs(src_dir, exist_ok=True)
    os.makedirs(components_dir, exist_ok=True)
    os.makedirs(public_dir, exist_ok=True)

    # Ensure NO .vscode/launch.json exists (critical: task asks to create it)
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    if os.path.exists(os.path.join(vscode_dir, 'launch.json')):
        os.remove(os.path.join(vscode_dir, 'launch.json'))

    # package.json
    package_json = {
        "name": "react-app",
        "private": True,
        "version": "1.0.0",
        "type": "module",
        "scripts": {
            "dev": "vite",
            "build": "tsc && vite build",
            "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
            "preview": "vite preview"
        },
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0"
        },
        "devDependencies": {
            "@types/react": "^18.2.43",
            "@types/react-dom": "^18.2.17",
            "@typescript-eslint/eslint-plugin": "^6.14.0",
            "@typescript-eslint/parser": "^6.14.0",
            "@vitejs/plugin-react": "^4.2.1",
            "eslint": "^8.55.0",
            "eslint-plugin-react-hooks": "^4.6.0",
            "eslint-plugin-react-refresh": "^0.4.5",
            "typescript": "^5.2.2",
            "vite": "^5.0.8"
        }
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # vite.config.ts
    vite_config = '''import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    open: false,
  },
})
'''
    with open(os.path.join(PROJECT_DIR, 'vite.config.ts'), 'w') as f:
        f.write(vite_config)

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
            "noFallthroughCasesInSwitch": True,
            "sourceMap": True
        },
        "include": ["src"],
        "references": [{"path": "./tsconfig.node.json"}]
    }
    with open(os.path.join(PROJECT_DIR, 'tsconfig.json'), 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # tsconfig.node.json
    tsconfig_node = {
        "compilerOptions": {
            "composite": True,
            "skipLibCheck": True,
            "module": "ESNext",
            "moduleResolution": "bundler",
            "allowSyntheticDefaultImports": True
        },
        "include": ["vite.config.ts"]
    }
    with open(os.path.join(PROJECT_DIR, 'tsconfig.node.json'), 'w') as f:
        json.dump(tsconfig_node, f, indent=2)

    # index.html
    index_html = '''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Inventory Dashboard</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
'''
    with open(os.path.join(PROJECT_DIR, 'index.html'), 'w') as f:
        f.write(index_html)

    # src/main.tsx
    main_tsx = '''import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
'''
    with open(os.path.join(src_dir, 'main.tsx'), 'w') as f:
        f.write(main_tsx)

    # src/App.tsx
    app_tsx = '''import { useState, useEffect } from 'react'
import { ProductTable } from './components/ProductTable'
import { SearchBar } from './components/SearchBar'
import './App.css'

interface Product {
  id: number
  name: string
  category: string
  price: number
  stock: number
  lastUpdated: string
}

const INITIAL_PRODUCTS: Product[] = [
  { id: 1, name: "Wireless Mouse", category: "Electronics", price: 29.99, stock: 150, lastUpdated: "2025-11-10" },
  { id: 2, name: "USB-C Hub", category: "Electronics", price: 49.95, stock: 85, lastUpdated: "2025-11-12" },
  { id: 3, name: "Standing Desk Mat", category: "Office", price: 34.50, stock: 200, lastUpdated: "2025-11-08" },
  { id: 4, name: "Mechanical Keyboard", category: "Electronics", price: 89.99, stock: 62, lastUpdated: "2025-11-15" },
  { id: 5, name: "Monitor Light Bar", category: "Lighting", price: 45.00, stock: 110, lastUpdated: "2025-11-14" },
  { id: 6, name: "Ergonomic Chair Cushion", category: "Office", price: 27.50, stock: 340, lastUpdated: "2025-11-09" },
  { id: 7, name: "Webcam HD 1080p", category: "Electronics", price: 59.99, stock: 95, lastUpdated: "2025-11-13" },
  { id: 8, name: "Desk Organizer Set", category: "Office", price: 22.00, stock: 175, lastUpdated: "2025-11-11" },
]

function App() {
  const [products, setProducts] = useState<Product[]>(INITIAL_PRODUCTS)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('All')

  const filteredProducts = products.filter(product => {
    const matchesSearch = product.name.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesCategory = selectedCategory === 'All' || product.category === selectedCategory
    return matchesSearch && matchesCategory
  })

  const categories = ['All', ...new Set(products.map(p => p.category))]

  const totalValue = filteredProducts.reduce((sum, p) => sum + p.price * p.stock, 0)

  return (
    <div className="app-container">
      <header>
        <h1>Inventory Dashboard</h1>
        <p className="summary">
          Showing {filteredProducts.length} of {products.length} products |
          Total inventory value: ${totalValue.toLocaleString('en-US', { minimumFractionDigits: 2 })}
        </p>
      </header>
      <SearchBar
        searchTerm={searchTerm}
        onSearchChange={setSearchTerm}
        categories={categories}
        selectedCategory={selectedCategory}
        onCategoryChange={setSelectedCategory}
      />
      <ProductTable products={filteredProducts} />
    </div>
  )
}

export default App
'''
    with open(os.path.join(src_dir, 'App.tsx'), 'w') as f:
        f.write(app_tsx)

    # src/App.css
    app_css = '''.app-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
}

header {
  margin-bottom: 2rem;
}

header h1 {
  color: #1a1a2e;
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
}

.summary {
  color: #666;
  font-size: 0.95rem;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

th, td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid #e0e0e0;
}

th {
  background-color: #f5f5f5;
  font-weight: 600;
  color: #333;
}

tr:hover {
  background-color: #fafafa;
}
'''
    with open(os.path.join(src_dir, 'App.css'), 'w') as f:
        f.write(app_css)

    # src/index.css
    index_css = ''':root {
  font-family: Inter, system-ui, Avenir, Helvetica, Arial, sans-serif;
  line-height: 1.5;
  font-weight: 400;
  color: #213547;
  background-color: #ffffff;
}

body {
  margin: 0;
  min-width: 320px;
  min-height: 100vh;
}
'''
    with open(os.path.join(src_dir, 'index.css'), 'w') as f:
        f.write(index_css)

    # src/components/ProductTable.tsx
    product_table = '''interface Product {
  id: number
  name: string
  category: string
  price: number
  stock: number
  lastUpdated: string
}

interface ProductTableProps {
  products: Product[]
}

export function ProductTable({ products }: ProductTableProps) {
  if (products.length === 0) {
    return <p style={{ textAlign: 'center', color: '#999' }}>No products found.</p>
  }

  return (
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Category</th>
          <th>Price</th>
          <th>Stock</th>
          <th>Last Updated</th>
        </tr>
      </thead>
      <tbody>
        {products.map(product => (
          <tr key={product.id}>
            <td>{product.name}</td>
            <td>{product.category}</td>
            <td>${product.price.toFixed(2)}</td>
            <td>{product.stock}</td>
            <td>{product.lastUpdated}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
'''
    with open(os.path.join(components_dir, 'ProductTable.tsx'), 'w') as f:
        f.write(product_table)

    # src/components/SearchBar.tsx
    search_bar = '''interface SearchBarProps {
  searchTerm: string
  onSearchChange: (value: string) => void
  categories: string[]
  selectedCategory: string
  onCategoryChange: (value: string) => void
}

export function SearchBar({
  searchTerm,
  onSearchChange,
  categories,
  selectedCategory,
  onCategoryChange,
}: SearchBarProps) {
  return (
    <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem' }}>
      <input
        type="text"
        placeholder="Search products..."
        value={searchTerm}
        onChange={(e) => onSearchChange(e.target.value)}
        style={{
          padding: '0.5rem 1rem',
          border: '1px solid #ccc',
          borderRadius: '4px',
          fontSize: '0.95rem',
          flex: 1,
        }}
      />
      <select
        value={selectedCategory}
        onChange={(e) => onCategoryChange(e.target.value)}
        style={{
          padding: '0.5rem 1rem',
          border: '1px solid #ccc',
          borderRadius: '4px',
          fontSize: '0.95rem',
        }}
      >
        {categories.map(cat => (
          <option key={cat} value={cat}>{cat}</option>
        ))}
      </select>
    </div>
  )
}
'''
    with open(os.path.join(components_dir, 'SearchBar.tsx'), 'w') as f:
        f.write(search_bar)

    # src/vite-env.d.ts
    vite_env_dts = '/// <reference types="vite/client" />\n'
    with open(os.path.join(src_dir, 'vite-env.d.ts'), 'w') as f:
        f.write(vite_env_dts)

    # public/vite.svg
    vite_svg = '''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" class="iconify iconify--logos" width="31.88" height="32" preserveAspectRatio="xMidYMid meet" viewBox="0 0 256 257"><defs><linearGradient id="IconifyId1813088fe1fbc01fb466" x1="-.828%" x2="57.636%" y1="7.652%" y2="78.411%"><stop offset="0%" stop-color="#41D1FF"></stop><stop offset="100%" stop-color="#BD34FE"></stop></linearGradient></defs><path fill="url(#IconifyId1813088fe1fbc01fb466)" d="M255.153 37.938L134.897 252.976c-2.483 4.44-8.862 4.466-11.382.048L.875 37.958c-2.746-4.814 1.371-10.646 6.827-9.67l120.385 21.517a6.537 6.537 0 0 0 2.322-.004l117.867-21.483c5.438-.991 9.574 4.796 6.877 9.62Z"></path></svg>
'''
    with open(os.path.join(public_dir, 'vite.svg'), 'w') as f:
        f.write(vite_svg)

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'Files: package.json, vite.config.ts, tsconfig.json, src/App.tsx, src/main.tsx, etc.')
    print(f'No .vscode/launch.json exists (task requires creating it)')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

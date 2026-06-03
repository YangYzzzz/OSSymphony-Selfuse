"""
Initial Setup: Create a React project workspace without .vscode/extensions.json
Task ID: vscode_web_038
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_038'
PROJECT_DIR = f'{WORKDIR}/projects/react-app'


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
    os.makedirs(f'{PROJECT_DIR}/src/hooks', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/utils', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/public', exist_ok=True)
    # Explicitly do NOT create .vscode directory

    # package.json
    package_json = {
        "name": "react-app",
        "version": "1.2.0",
        "private": True,
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-scripts": "5.0.1",
            "tailwindcss": "^3.3.5",
            "autoprefixer": "^10.4.16",
            "postcss": "^8.4.31"
        },
        "devDependencies": {
            "eslint": "^8.53.0",
            "prettier": "^3.1.0",
            "@testing-library/react": "^14.1.2",
            "@testing-library/jest-dom": "^6.1.4"
        },
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test",
            "eject": "react-scripts eject",
            "lint": "eslint src/",
            "format": "prettier --write \"src/**/*.{js,jsx,css}\""
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # src/App.js
    with open(f'{PROJECT_DIR}/src/App.js', 'w') as f:
        f.write("""import React from 'react';
import Header from './components/Header';
import ProductList from './components/ProductList';
import useCart from './hooks/useCart';
import './App.css';

function App() {
  const { cartItems, addToCart, removeFromCart, total } = useCart();

  return (
    <div className="min-h-screen bg-gray-50">
      <Header cartCount={cartItems.length} total={total} />
      <main className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">
          Featured Products
        </h1>
        <ProductList onAddToCart={addToCart} />
      </main>
    </div>
  );
}

export default App;
""")

    # src/App.css
    with open(f'{PROJECT_DIR}/src/App.css', 'w') as f:
        f.write("""@tailwind base;
@tailwind components;
@tailwind utilities;

.product-card {
  @apply bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition-shadow;
}

.btn-primary {
  @apply bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700;
}
""")

    # src/index.js
    with open(f'{PROJECT_DIR}/src/index.js', 'w') as f:
        f.write("""import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
""")

    # src/components/Header.js
    with open(f'{PROJECT_DIR}/src/components/Header.js', 'w') as f:
        f.write("""import React from 'react';

const Header = ({ cartCount, total }) => {
  return (
    <header className="bg-white shadow-sm border-b">
      <div className="container mx-auto px-4 py-3 flex justify-between items-center">
        <div className="flex items-center space-x-2">
          <span className="text-2xl font-bold text-blue-600">ShopWave</span>
        </div>
        <nav className="hidden md:flex space-x-6">
          <a href="/products" className="text-gray-600 hover:text-gray-900">Products</a>
          <a href="/deals" className="text-gray-600 hover:text-gray-900">Deals</a>
          <a href="/about" className="text-gray-600 hover:text-gray-900">About</a>
        </nav>
        <div className="flex items-center space-x-4">
          <span className="text-sm text-gray-500">
            Cart ({cartCount}) - ${total.toFixed(2)}
          </span>
        </div>
      </div>
    </header>
  );
};

export default Header;
""")

    # src/components/ProductList.js
    with open(f'{PROJECT_DIR}/src/components/ProductList.js', 'w') as f:
        f.write("""import React, { useState, useEffect } from 'react';
import { formatPrice } from '../utils/formatters';

const PRODUCTS = [
  { id: 1, name: 'Wireless Bluetooth Headphones', price: 79.99, category: 'Electronics', rating: 4.5 },
  { id: 2, name: 'Organic Cotton T-Shirt', price: 34.50, category: 'Clothing', rating: 4.2 },
  { id: 3, name: 'Stainless Steel Water Bottle', price: 24.99, category: 'Accessories', rating: 4.8 },
  { id: 4, name: 'USB-C Charging Cable 6ft', price: 12.99, category: 'Electronics', rating: 4.0 },
  { id: 5, name: 'Bamboo Cutting Board Set', price: 42.00, category: 'Kitchen', rating: 4.6 },
  { id: 6, name: 'Running Shoes Pro', price: 129.99, category: 'Sports', rating: 4.7 },
];

const ProductList = ({ onAddToCart }) => {
  const [filter, setFilter] = useState('All');

  const categories = ['All', ...new Set(PRODUCTS.map(p => p.category))];
  const filtered = filter === 'All' ? PRODUCTS : PRODUCTS.filter(p => p.category === filter);

  return (
    <div>
      <div className="flex space-x-2 mb-6">
        {categories.map(cat => (
          <button
            key={cat}
            onClick={() => setFilter(cat)}
            className={`px-3 py-1 rounded-full text-sm ${
              filter === cat ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'
            }`}
          >
            {cat}
          </button>
        ))}
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filtered.map(product => (
          <div key={product.id} className="product-card">
            <h3 className="font-semibold text-lg">{product.name}</h3>
            <p className="text-gray-500 text-sm">{product.category}</p>
            <div className="flex justify-between items-center mt-4">
              <span className="text-xl font-bold">{formatPrice(product.price)}</span>
              <button onClick={() => onAddToCart(product)} className="btn-primary">
                Add to Cart
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProductList;
""")

    # src/hooks/useCart.js
    with open(f'{PROJECT_DIR}/src/hooks/useCart.js', 'w') as f:
        f.write("""import { useState, useCallback, useMemo } from 'react';

const useCart = () => {
  const [cartItems, setCartItems] = useState([]);

  const addToCart = useCallback((product) => {
    setCartItems(prev => {
      const existing = prev.find(item => item.id === product.id);
      if (existing) {
        return prev.map(item =>
          item.id === product.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
      }
      return [...prev, { ...product, quantity: 1 }];
    });
  }, []);

  const removeFromCart = useCallback((productId) => {
    setCartItems(prev => prev.filter(item => item.id !== productId));
  }, []);

  const total = useMemo(
    () => cartItems.reduce((sum, item) => sum + item.price * item.quantity, 0),
    [cartItems]
  );

  return { cartItems, addToCart, removeFromCart, total };
};

export default useCart;
""")

    # src/utils/formatters.js
    with open(f'{PROJECT_DIR}/src/utils/formatters.js', 'w') as f:
        f.write("""export const formatPrice = (price) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(price);
};

export const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
};

export const truncateText = (text, maxLength = 100) => {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength) + '...';
};
""")

    # public/index.html
    with open(f'{PROJECT_DIR}/public/index.html', 'w') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>ShopWave - React App</title>
</head>
<body>
  <div id="root"></div>
</body>
</html>
""")

    # tailwind.config.js
    with open(f'{PROJECT_DIR}/tailwind.config.js', 'w') as f:
        f.write("""/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#eff6ff',
          500: '#3b82f6',
          700: '#1d4ed8',
        }
      }
    },
  },
  plugins: [],
}
""")

    # .eslintrc.json
    with open(f'{PROJECT_DIR}/.eslintrc.json', 'w') as f:
        json.dump({
            "env": {
                "browser": True,
                "es2021": True,
                "jest": True
            },
            "extends": [
                "eslint:recommended",
                "plugin:react/recommended"
            ],
            "parserOptions": {
                "ecmaFeatures": {"jsx": True},
                "ecmaVersion": "latest",
                "sourceType": "module"
            },
            "rules": {
                "react/react-in-jsx-scope": "off",
                "no-unused-vars": "warn"
            }
        }, f, indent=2)

    # .prettierrc
    with open(f'{PROJECT_DIR}/.prettierrc', 'w') as f:
        json.dump({
            "semi": True,
            "trailingComma": "es5",
            "singleQuote": True,
            "printWidth": 100,
            "tabWidth": 2
        }, f, indent=2)

    # README.md
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write("""# ShopWave React App

A modern e-commerce storefront built with React and Tailwind CSS.

## Getting Started

```bash
npm install
npm start
```

## Team Notes

- Please ensure consistent code formatting before committing
- Use ESLint for code quality checks
- Tailwind CSS is used for styling
""")

    print(f'Initial project created: {PROJECT_DIR}')
    print('Verified: No .vscode/extensions.json exists')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

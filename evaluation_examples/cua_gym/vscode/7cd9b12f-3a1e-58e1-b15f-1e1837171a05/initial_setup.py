"""
Initial Setup: React TypeScript project with missing useState import
Task ID: vscode_lp_015
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_015'
PROJECT_DIR = f'{WORKDIR}/workspace'

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
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/node_modules/react', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/node_modules/@types/react', exist_ok=True)

    # --- package.json ---
    package_json = {
        "name": "inventory-dashboard",
        "version": "1.0.0",
        "description": "Product inventory tracking dashboard",
        "main": "src/App.tsx",
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test"
        },
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-scripts": "5.0.1",
            "typescript": "^5.0.0",
            "@types/react": "^18.2.0",
            "@types/react-dom": "^18.2.0"
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # --- tsconfig.json ---
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
            "noEmit": True,
            "jsx": "react-jsx"
        },
        "include": ["src"]
    }
    with open(f'{PROJECT_DIR}/tsconfig.json', 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # --- src/App.tsx --- (NO import for useState - this is what the task requires the agent to add)
    app_tsx_content = '''import React from "react";

interface Product {
  id: number;
  name: string;
  quantity: number;
  price: number;
}

const initialProducts: Product[] = [
  { id: 1, name: "Wireless Keyboard", quantity: 45, price: 59.99 },
  { id: 2, name: "USB-C Hub", quantity: 23, price: 34.99 },
  { id: 3, name: "Monitor Stand", quantity: 18, price: 79.99 },
  { id: 4, name: "Webcam HD Pro", quantity: 56, price: 89.99 },
  { id: 5, name: "Ergonomic Mouse", quantity: 31, price: 44.99 },
];

const App: React.FC = () => {
  const [products, setProducts] = useState<Product[]>(initialProducts);
  const [searchTerm, setSearchTerm] = useState<string>("");

  const filteredProducts = products.filter((product) =>
    product.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const totalValue = filteredProducts.reduce(
    (sum, product) => sum + product.quantity * product.price,
    0
  );

  return (
    <div style={{ padding: "24px", fontFamily: "Arial, sans-serif" }}>
      <h1>Inventory Dashboard</h1>
      <input
        type="text"
        placeholder="Search products..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        style={{ padding: "8px", width: "300px", marginBottom: "16px" }}
      />
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th style={{ textAlign: "left", padding: "8px", borderBottom: "2px solid #ddd" }}>Product</th>
            <th style={{ textAlign: "right", padding: "8px", borderBottom: "2px solid #ddd" }}>Qty</th>
            <th style={{ textAlign: "right", padding: "8px", borderBottom: "2px solid #ddd" }}>Price</th>
            <th style={{ textAlign: "right", padding: "8px", borderBottom: "2px solid #ddd" }}>Total</th>
          </tr>
        </thead>
        <tbody>
          {filteredProducts.map((product) => (
            <tr key={product.id}>
              <td style={{ padding: "8px", borderBottom: "1px solid #eee" }}>{product.name}</td>
              <td style={{ textAlign: "right", padding: "8px", borderBottom: "1px solid #eee" }}>{product.quantity}</td>
              <td style={{ textAlign: "right", padding: "8px", borderBottom: "1px solid #eee" }}>${product.price.toFixed(2)}</td>
              <td style={{ textAlign: "right", padding: "8px", borderBottom: "1px solid #eee" }}>
                ${(product.quantity * product.price).toFixed(2)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <p style={{ marginTop: "16px", fontWeight: "bold" }}>
        Total Inventory Value: ${totalValue.toFixed(2)}
      </p>
    </div>
  );
};

export default App;
'''
    with open(f'{PROJECT_DIR}/src/App.tsx', 'w') as f:
        f.write(app_tsx_content)

    # --- src/index.tsx ---
    index_tsx_content = '''import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
'''
    with open(f'{PROJECT_DIR}/src/index.tsx', 'w') as f:
        f.write(index_tsx_content)

    # --- Minimal react type stubs so TypeScript recognizes the module ---
    react_index = '''export function useState<T>(initialState: T | (() => T)): [T, (value: T) => void];
export type FC<P = {}> = (props: P) => JSX.Element | null;
export default React;
declare namespace React {}
declare namespace JSX {
  interface Element {}
  interface IntrinsicElements {
    [elemName: string]: any;
  }
}
'''
    with open(f'{PROJECT_DIR}/node_modules/react/index.d.ts', 'w') as f:
        f.write(react_index)

    react_package = {
        "name": "react",
        "version": "18.2.0",
        "main": "index.js",
        "types": "index.d.ts"
    }
    with open(f'{PROJECT_DIR}/node_modules/react/package.json', 'w') as f:
        json.dump(react_package, f, indent=2)

    with open(f'{PROJECT_DIR}/node_modules/react/index.js', 'w') as f:
        f.write('module.exports = {};\n')

    # @types/react
    types_react_index = '''import * as React from "react";
export = React;
export as namespace React;
declare namespace React {
  function useState<T>(initialState: T | (() => T)): [T, (value: T) => void];
  type FC<P = {}> = (props: P) => JSX.Element | null;
}
declare global {
  namespace JSX {
    interface Element {}
    interface IntrinsicElements {
      [elemName: string]: any;
    }
  }
}
'''
    with open(f'{PROJECT_DIR}/node_modules/@types/react/index.d.ts', 'w') as f:
        f.write(types_react_index)

    types_react_package = {
        "name": "@types/react",
        "version": "18.2.0",
        "main": "",
        "types": "index.d.ts"
    }
    with open(f'{PROJECT_DIR}/node_modules/@types/react/package.json', 'w') as f:
        json.dump(types_react_package, f, indent=2)

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'App.tsx location: {PROJECT_DIR}/src/App.tsx')

    # GUI-ready: open VSCode with the project folder and the problematic file
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    launch_gui(f'code "{PROJECT_DIR}/src/App.tsx"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()

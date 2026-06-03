"""
Initial Setup: Create a React TypeScript project folder with no .vscode directory
Task ID: vscode_we_059
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'react-ts')

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
    # Create project directory structure (no .vscode/)
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'components'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'hooks'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'public'), exist_ok=True)

    # Ensure .vscode does NOT exist
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)

    # package.json
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        f.write("""{
  "name": "react-ts-dashboard",
  "version": "1.2.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.1",
    "typescript": "^5.3.2",
    "tailwindcss": "^3.4.0",
    "@types/react": "^18.2.42",
    "@types/react-dom": "^18.2.17"
  },
  "devDependencies": {
    "eslint": "^8.55.0",
    "prettier": "^3.1.1",
    "@typescript-eslint/eslint-plugin": "^6.14.0",
    "@typescript-eslint/parser": "^6.14.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "lint": "eslint src/ --ext .ts,.tsx"
  }
}
""")

    # tsconfig.json
    with open(os.path.join(PROJECT_DIR, 'tsconfig.json'), 'w') as f:
        f.write("""{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noFallthroughCasesInSwitch": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "baseUrl": "src"
  },
  "include": ["src"]
}
""")

    # tailwind.config.js
    with open(os.path.join(PROJECT_DIR, 'tailwind.config.js'), 'w') as f:
        f.write("""/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3B82F6',
        secondary: '#10B981',
      },
    },
  },
  plugins: [],
}
""")

    # .eslintrc.json
    with open(os.path.join(PROJECT_DIR, '.eslintrc.json'), 'w') as f:
        f.write("""{
  "env": {
    "browser": true,
    "es2021": true
  },
  "extends": [
    "eslint:recommended",
    "plugin:react/recommended",
    "plugin:@typescript-eslint/recommended"
  ],
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "ecmaFeatures": {
      "jsx": true
    },
    "ecmaVersion": "latest",
    "sourceType": "module"
  },
  "plugins": ["react", "@typescript-eslint"],
  "rules": {
    "react/react-in-jsx-scope": "off"
  }
}
""")

    # .prettierrc
    with open(os.path.join(PROJECT_DIR, '.prettierrc'), 'w') as f:
        f.write("""{
  "semi": true,
  "trailingComma": "all",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2
}
""")

    # src/App.tsx
    with open(os.path.join(PROJECT_DIR, 'src', 'App.tsx'), 'w') as f:
        f.write("""import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import Sidebar from './components/Sidebar';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <div className="flex h-screen bg-gray-100">
        <Sidebar />
        <main className="flex-1 overflow-y-auto p-6">
          <Routes>
            <Route path="/" element={<Dashboard />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
};

export default App;
""")

    # src/index.tsx
    with open(os.path.join(PROJECT_DIR, 'src', 'index.tsx'), 'w') as f:
        f.write("""import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement,
);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
""")

    # src/components/Dashboard.tsx
    with open(os.path.join(PROJECT_DIR, 'src', 'components', 'Dashboard.tsx'), 'w') as f:
        f.write("""import React, { useState, useEffect } from 'react';
import { useMetrics } from '../hooks/useMetrics';

interface MetricCard {
  title: string;
  value: string;
  change: number;
}

const Dashboard: React.FC = () => {
  const { metrics, loading } = useMetrics();

  if (loading) {
    return <div className="text-center py-10">Loading dashboard...</div>;
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Dashboard Overview</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {metrics.map((metric: MetricCard, index: number) => (
          <div key={index} className="bg-white rounded-lg shadow p-6">
            <h3 className="text-sm font-medium text-gray-500">{metric.title}</h3>
            <p className="text-3xl font-bold text-primary mt-2">{metric.value}</p>
            <span className={`text-sm ${metric.change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
              {metric.change >= 0 ? '+' : ''}{metric.change}%
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
""")

    # src/components/Sidebar.tsx
    with open(os.path.join(PROJECT_DIR, 'src', 'components', 'Sidebar.tsx'), 'w') as f:
        f.write("""import React from 'react';

const Sidebar: React.FC = () => {
  const menuItems = ['Dashboard', 'Analytics', 'Users', 'Settings'];

  return (
    <aside className="w-64 bg-white shadow-md">
      <div className="p-4 border-b">
        <h2 className="text-xl font-bold text-primary">ReactTS App</h2>
      </div>
      <nav className="mt-4">
        {menuItems.map((item) => (
          <a
            key={item}
            href="#"
            className="block px-4 py-3 text-gray-700 hover:bg-gray-100 hover:text-primary transition-colors"
          >
            {item}
          </a>
        ))}
      </nav>
    </aside>
  );
};

export default Sidebar;
""")

    # src/hooks/useMetrics.ts
    with open(os.path.join(PROJECT_DIR, 'src', 'hooks', 'useMetrics.ts'), 'w') as f:
        f.write("""import { useState, useEffect } from 'react';

interface MetricCard {
  title: string;
  value: string;
  change: number;
}

export const useMetrics = () => {
  const [metrics, setMetrics] = useState<MetricCard[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMetrics = async () => {
      // Simulated data fetch
      await new Promise((resolve) => setTimeout(resolve, 500));
      setMetrics([
        { title: 'Total Revenue', value: '$48,250', change: 12.5 },
        { title: 'Active Users', value: '2,340', change: -3.2 },
        { title: 'Conversion Rate', value: '3.8%', change: 0.7 },
      ]);
      setLoading(false);
    };
    fetchMetrics();
  }, []);

  return { metrics, loading };
};
""")

    # public/index.html
    with open(os.path.join(PROJECT_DIR, 'public', 'index.html'), 'w') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>React TS Dashboard</title>
</head>
<body>
  <div id="root"></div>
</body>
</html>
""")

    # src/index.css
    with open(os.path.join(PROJECT_DIR, 'src', 'index.css'), 'w') as f:
        f.write("""@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
}
""")

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'.vscode/ does NOT exist: {not os.path.exists(vscode_dir)}')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()

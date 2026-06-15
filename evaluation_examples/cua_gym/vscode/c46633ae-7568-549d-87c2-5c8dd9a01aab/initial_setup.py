"""
Initial Setup: Set up Playwright e2e testing workflow in ~/project
Task ID: vscode_wf_066
Domain: vscode

Creates a web application project with @playwright/test installed via npm.
No Playwright config, test files, or VSCode debug/task configurations exist yet.
Opens VSCode with ~/project.
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'project')
SRC_DIR = os.path.join(PROJECT, 'src')
VSCODE_DIR = os.path.join(PROJECT, '.vscode')


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
    # Create project structure
    os.makedirs(SRC_DIR, exist_ok=True)
    os.makedirs(os.path.join(SRC_DIR, 'components'), exist_ok=True)
    os.makedirs(os.path.join(SRC_DIR, 'pages'), exist_ok=True)
    os.makedirs(os.path.join(SRC_DIR, 'styles'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT, 'public'), exist_ok=True)

    # package.json with @playwright/test already installed
    package_json = {
        "name": "acme-dashboard",
        "version": "1.2.0",
        "description": "ACME Corp internal dashboard application",
        "main": "src/index.js",
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test",
            "lint": "eslint src/"
        },
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.20.0",
            "react-scripts": "5.0.1",
            "axios": "^1.6.2"
        },
        "devDependencies": {
            "@playwright/test": "^1.40.0",
            "@types/react": "^18.2.42",
            "eslint": "^8.54.0",
            "typescript": "^5.3.2"
        }
    }
    with open(os.path.join(PROJECT, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # tsconfig.json
    tsconfig = {
        "compilerOptions": {
            "target": "es2020",
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
    with open(os.path.join(PROJECT, 'tsconfig.json'), 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # src/index.tsx
    with open(os.path.join(SRC_DIR, 'index.tsx'), 'w') as f:
        f.write("""import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles/global.css';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
""")

    # src/App.tsx
    with open(os.path.join(SRC_DIR, 'App.tsx'), 'w') as f:
        f.write("""import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import HomePage from './pages/HomePage';
import DashboardPage from './pages/DashboardPage';
import ContactPage from './pages/ContactPage';

function App() {
  return (
    <Router>
      <nav className="main-nav">
        <Link to="/">Home</Link>
        <Link to="/dashboard">Dashboard</Link>
        <Link to="/contact">Contact</Link>
      </nav>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/contact" element={<ContactPage />} />
      </Routes>
    </Router>
  );
}

export default App;
""")

    # src/pages/HomePage.tsx
    with open(os.path.join(SRC_DIR, 'pages', 'HomePage.tsx'), 'w') as f:
        f.write("""import React from 'react';

export default function HomePage() {
  return (
    <main>
      <h1>Welcome to ACME Dashboard</h1>
      <p>Manage your projects and track performance metrics.</p>
      <section className="features">
        <div className="feature-card">
          <h2>Analytics</h2>
          <p>Real-time insights into your business performance.</p>
        </div>
        <div className="feature-card">
          <h2>Team Management</h2>
          <p>Organize and collaborate with your team members.</p>
        </div>
      </section>
    </main>
  );
}
""")

    # src/pages/DashboardPage.tsx
    with open(os.path.join(SRC_DIR, 'pages', 'DashboardPage.tsx'), 'w') as f:
        f.write("""import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface MetricData {
  label: string;
  value: number;
  trend: 'up' | 'down' | 'stable';
}

export default function DashboardPage() {
  const [metrics, setMetrics] = useState<MetricData[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('/api/metrics')
      .then(res => {
        setMetrics(res.data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading">Loading dashboard...</div>;

  return (
    <main>
      <h1>Dashboard</h1>
      <div className="metrics-grid">
        {metrics.map((m, i) => (
          <div key={i} className="metric-card">
            <span className="metric-label">{m.label}</span>
            <span className="metric-value">{m.value}</span>
            <span className={`trend trend-${m.trend}`}>{m.trend}</span>
          </div>
        ))}
      </div>
    </main>
  );
}
""")

    # src/pages/ContactPage.tsx
    with open(os.path.join(SRC_DIR, 'pages', 'ContactPage.tsx'), 'w') as f:
        f.write("""import React, { useState } from 'react';

export default function ContactPage() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: '',
  });
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Submit logic here
    setSubmitted(true);
  };

  if (submitted) {
    return (
      <main>
        <h1>Thank You!</h1>
        <p>Your message has been sent successfully.</p>
      </main>
    );
  }

  return (
    <main>
      <h1>Contact Us</h1>
      <form onSubmit={handleSubmit} data-testid="contact-form">
        <label htmlFor="name">Name</label>
        <input
          id="name"
          type="text"
          value={formData.name}
          onChange={e => setFormData({...formData, name: e.target.value})}
          required
        />
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          value={formData.email}
          onChange={e => setFormData({...formData, email: e.target.value})}
          required
        />
        <label htmlFor="message">Message</label>
        <textarea
          id="message"
          value={formData.message}
          onChange={e => setFormData({...formData, message: e.target.value})}
          required
        />
        <button type="submit">Send Message</button>
      </form>
    </main>
  );
}
""")

    # src/components/Header.tsx
    with open(os.path.join(SRC_DIR, 'components', 'Header.tsx'), 'w') as f:
        f.write("""import React from 'react';
import { Link } from 'react-router-dom';

interface HeaderProps {
  username?: string;
}

export default function Header({ username }: HeaderProps) {
  return (
    <header className="app-header">
      <div className="logo">ACME Dashboard</div>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/dashboard">Dashboard</Link>
        <Link to="/contact">Contact</Link>
      </nav>
      {username && <span className="user-greeting">Hello, {username}</span>}
    </header>
  );
}
""")

    # src/styles/global.css
    with open(os.path.join(SRC_DIR, 'styles', 'global.css'), 'w') as f:
        f.write("""* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f5f5f5;
  color: #333;
}

.main-nav {
  background-color: #1a1a2e;
  padding: 1rem 2rem;
  display: flex;
  gap: 1.5rem;
}

.main-nav a {
  color: #e0e0e0;
  text-decoration: none;
  font-weight: 500;
}

main {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1.5rem;
}

h1 {
  margin-bottom: 1rem;
  color: #1a1a2e;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.feature-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

form {
  max-width: 600px;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

input, textarea {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}

button[type="submit"] {
  background-color: #1a1a2e;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  margin-top: 0.5rem;
}
""")

    # public/index.html
    with open(os.path.join(PROJECT, 'public', 'index.html'), 'w') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>ACME Dashboard</title>
</head>
<body>
  <div id="root"></div>
</body>
</html>
""")

    # .gitignore
    with open(os.path.join(PROJECT, '.gitignore'), 'w') as f:
        f.write("""node_modules/
dist/
build/
.env
*.log
test-results/
playwright-report/
""")

    # README.md
    with open(os.path.join(PROJECT, 'README.md'), 'w') as f:
        f.write("""# ACME Dashboard

Internal dashboard application for ACME Corp.

## Getting Started

```bash
npm install
npm start
```

The app runs on http://localhost:3000 by default.

## Available Scripts

- `npm start` - Runs the development server
- `npm run build` - Builds the production bundle
- `npm test` - Runs the unit test suite
- `npm run lint` - Lints the source code
""")

    # Create a minimal .vscode/settings.json (no Playwright-related configs)
    os.makedirs(VSCODE_DIR, exist_ok=True)
    vscode_settings = {
        "editor.formatOnSave": True,
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "typescript.tsdk": "node_modules/typescript/lib"
    }
    with open(os.path.join(VSCODE_DIR, 'settings.json'), 'w') as f:
        json.dump(vscode_settings, f, indent=2)

    # Install @playwright/test npm package (simulate node_modules presence)
    os.makedirs(os.path.join(PROJECT, 'node_modules', '@playwright', 'test'), exist_ok=True)
    playwright_pkg = {
        "name": "@playwright/test",
        "version": "1.40.0",
        "description": "A high-level API to automate web browsers",
        "main": "index.js"
    }
    with open(os.path.join(PROJECT, 'node_modules', '@playwright', 'test', 'package.json'), 'w') as f:
        json.dump(playwright_pkg, f, indent=2)

    print(f'Initial project created: {PROJECT}')

    # Launch VSCode with the project
    launch_gui(f'code "{PROJECT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

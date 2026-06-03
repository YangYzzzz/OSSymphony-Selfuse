"""
Initial Setup: Configure pre-commit hook with Husky and lint-staged
Task ID: vscode_web_084
Domain: vscode

Creates a realistic Node.js webapp project with ESLint and Prettier configured,
but WITHOUT husky or lint-staged installed. Opens VSCode with the project.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_084'
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
    os.makedirs(f'{PROJECT_DIR}/src/utils', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/public', exist_ok=True)

    # package.json - has eslint and prettier but NOT husky/lint-staged
    package_json = {
        "name": "webapp",
        "version": "1.2.0",
        "description": "Internal dashboard for sales analytics",
        "main": "src/index.js",
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test",
            "lint": "eslint src/",
            "format": "prettier --write \"src/**/*.{js,jsx,ts,tsx,css,json}\""
        },
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-scripts": "5.0.1",
            "axios": "^1.6.2",
            "chart.js": "^4.4.1",
            "react-chartjs-2": "^5.2.0",
            "react-router-dom": "^6.21.1"
        },
        "devDependencies": {
            "eslint": "^8.56.0",
            "eslint-config-react-app": "^7.0.1",
            "eslint-plugin-react": "^7.33.2",
            "eslint-plugin-react-hooks": "^4.6.0",
            "prettier": "^3.2.4",
            "@types/react": "^18.2.48"
        },
        "browserslist": {
            "production": [">0.2%", "not dead", "not op_mini all"],
            "development": ["last 1 chrome version", "last 1 firefox version"]
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # .eslintrc.json
    eslintrc = {
        "env": {
            "browser": True,
            "es2021": True,
            "node": True
        },
        "extends": [
            "eslint:recommended",
            "plugin:react/recommended",
            "plugin:react-hooks/recommended"
        ],
        "parserOptions": {
            "ecmaFeatures": {"jsx": True},
            "ecmaVersion": "latest",
            "sourceType": "module"
        },
        "plugins": ["react", "react-hooks"],
        "rules": {
            "no-unused-vars": "warn",
            "no-console": "warn",
            "react/prop-types": "off",
            "semi": ["error", "always"],
            "quotes": ["error", "single"]
        },
        "settings": {
            "react": {"version": "detect"}
        }
    }
    with open(f'{PROJECT_DIR}/.eslintrc.json', 'w') as f:
        json.dump(eslintrc, f, indent=2)

    # .prettierrc
    prettierrc = {
        "semi": True,
        "trailingComma": "es5",
        "singleQuote": True,
        "printWidth": 80,
        "tabWidth": 2,
        "useTabs": False,
        "bracketSpacing": True,
        "jsxSingleQuote": False,
        "arrowParens": "always"
    }
    with open(f'{PROJECT_DIR}/.prettierrc', 'w') as f:
        json.dump(prettierrc, f, indent=2)

    # .prettierignore
    with open(f'{PROJECT_DIR}/.prettierignore', 'w') as f:
        f.write("node_modules\nbuild\ncoverage\n")

    # .gitignore
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write("""node_modules/
build/
coverage/
.env
.env.local
.DS_Store
*.log
""")

    # src/index.js
    with open(f'{PROJECT_DIR}/src/index.js', 'w') as f:
        f.write("""import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
""")

    # src/App.js
    with open(f'{PROJECT_DIR}/src/App.js', 'w') as f:
        f.write("""import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import SalesReport from './components/SalesReport';
import Header from './components/Header';

function App() {
  return (
    <BrowserRouter>
      <Header />
      <div className="app-container">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/sales" element={<SalesReport />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
""")

    # src/components/Dashboard.jsx
    with open(f'{PROJECT_DIR}/src/components/Dashboard.jsx', 'w') as f:
        f.write("""import React, { useState, useEffect } from 'react';
import { fetchSalesData } from '../utils/api';
import SalesChart from './SalesChart';

const Dashboard = () => {
  const [salesData, setSalesData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        setIsLoading(true);
        const data = await fetchSalesData();
        setSalesData(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };
    loadData();
  }, []);

  if (isLoading) return <div className="loading">Loading dashboard...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  const totalRevenue = salesData.reduce((sum, item) => sum + item.revenue, 0);
  const avgDealSize = totalRevenue / salesData.length;

  return (
    <div className="dashboard">
      <h1>Sales Analytics Dashboard</h1>
      <div className="metrics-grid">
        <div className="metric-card">
          <h3>Total Revenue</h3>
          <p className="metric-value">${totalRevenue.toLocaleString()}</p>
        </div>
        <div className="metric-card">
          <h3>Average Deal Size</h3>
          <p className="metric-value">${avgDealSize.toFixed(2)}</p>
        </div>
        <div className="metric-card">
          <h3>Total Deals</h3>
          <p className="metric-value">{salesData.length}</p>
        </div>
      </div>
      <SalesChart data={salesData} />
    </div>
  );
};

export default Dashboard;
""")

    # src/components/SalesReport.jsx
    with open(f'{PROJECT_DIR}/src/components/SalesReport.jsx', 'w') as f:
        f.write("""import React, { useState, useEffect } from 'react';
import { fetchSalesData } from '../utils/api';
import { formatCurrency, formatDate } from '../utils/formatters';

const SalesReport = () => {
  const [sales, setSales] = useState([]);
  const [sortField, setSortField] = useState('date');
  const [sortOrder, setSortOrder] = useState('desc');

  useEffect(() => {
    fetchSalesData().then(setSales);
  }, []);

  const sortedSales = [...sales].sort((a, b) => {
    const modifier = sortOrder === 'asc' ? 1 : -1;
    if (sortField === 'revenue') return (a.revenue - b.revenue) * modifier;
    return a[sortField].localeCompare(b[sortField]) * modifier;
  });

  const handleSort = (field) => {
    if (field === sortField) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortOrder('asc');
    }
  };

  return (
    <div className="sales-report">
      <h1>Sales Report</h1>
      <table>
        <thead>
          <tr>
            <th onClick={() => handleSort('date')}>Date</th>
            <th onClick={() => handleSort('client')}>Client</th>
            <th onClick={() => handleSort('product')}>Product</th>
            <th onClick={() => handleSort('revenue')}>Revenue</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {sortedSales.map((sale, idx) => (
            <tr key={idx}>
              <td>{formatDate(sale.date)}</td>
              <td>{sale.client}</td>
              <td>{sale.product}</td>
              <td>{formatCurrency(sale.revenue)}</td>
              <td className={`status-${sale.status}`}>{sale.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default SalesReport;
""")

    # src/components/Header.jsx
    with open(f'{PROJECT_DIR}/src/components/Header.jsx', 'w') as f:
        f.write("""import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <header className="app-header">
      <div className="logo">
        <h2>SalesViz</h2>
      </div>
      <nav>
        <Link to="/">Dashboard</Link>
        <Link to="/sales">Sales Report</Link>
      </nav>
    </header>
  );
};

export default Header;
""")

    # src/components/SalesChart.jsx
    with open(f'{PROJECT_DIR}/src/components/SalesChart.jsx', 'w') as f:
        f.write("""import React from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const SalesChart = ({ data }) => {
  const chartData = {
    labels: data.map((item) => item.month),
    datasets: [
      {
        label: 'Monthly Revenue',
        data: data.map((item) => item.revenue),
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      title: { display: true, text: 'Monthly Sales Revenue' },
    },
  };

  return (
    <div className="chart-container">
      <Bar data={chartData} options={options} />
    </div>
  );
};

export default SalesChart;
""")

    # src/utils/api.js
    with open(f'{PROJECT_DIR}/src/utils/api.js', 'w') as f:
        f.write("""import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'https://api.example.com';

export const fetchSalesData = async () => {
  try {
    const response = await axios.get(`${API_BASE}/sales`);
    return response.data;
  } catch (error) {
    console.error('Failed to fetch sales data:', error);
    throw error;
  }
};

export const fetchClientList = async () => {
  try {
    const response = await axios.get(`${API_BASE}/clients`);
    return response.data;
  } catch (error) {
    console.error('Failed to fetch client list:', error);
    throw error;
  }
};
""")

    # src/utils/formatters.js
    with open(f'{PROJECT_DIR}/src/utils/formatters.js', 'w') as f:
        f.write("""export const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(amount);
};

export const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};

export const formatPercentage = (value) => {
  return `${(value * 100).toFixed(1)}%`;
};
""")

    # src/index.css
    with open(f'{PROJECT_DIR}/src/index.css', 'w') as f:
        f.write("""body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background-color: #f5f7fa;
  color: #333;
}

.app-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.app-header {
  background: #1a237e;
  color: white;
  padding: 12px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.app-header nav a {
  color: white;
  margin-left: 20px;
  text-decoration: none;
}

.dashboard h1 {
  margin-bottom: 24px;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 32px;
}

.metric-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.metric-value {
  font-size: 28px;
  font-weight: bold;
  color: #1a237e;
}

.sales-report table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

.sales-report th,
.sales-report td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.sales-report th {
  background: #f0f0f0;
  cursor: pointer;
}

.status-closed {
  color: #2e7d32;
}
.status-pending {
  color: #f57c00;
}
""")

    # public/index.html
    with open(f'{PROJECT_DIR}/public/index.html', 'w') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>SalesViz - Sales Analytics Dashboard</title>
</head>
<body>
  <div id="root"></div>
</body>
</html>
""")

    # Initialize git repo
    subprocess.run(['git', 'init'], cwd=PROJECT_DIR, capture_output=True)
    subprocess.run(['git', 'config', 'user.email', 'dev@salesviz.com'], cwd=PROJECT_DIR, capture_output=True)
    subprocess.run(['git', 'config', 'user.name', 'Dev Team'], cwd=PROJECT_DIR, capture_output=True)
    subprocess.run(['git', 'add', '.'], cwd=PROJECT_DIR, capture_output=True)
    subprocess.run(['git', 'commit', '-m', 'Initial commit: React dashboard with ESLint and Prettier'], cwd=PROJECT_DIR, capture_output=True)

    # Create a fake node_modules with just enough for the task to work
    # (husky and lint-staged need npm, so we ensure npm is functional)
    # We don't run npm install for the full project - just make sure git is initialized

    print(f'Initial project created: {PROJECT_DIR}')

    # Launch VSCode with the project directory
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

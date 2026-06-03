"""
Initial Setup: Configure multi-root workspace with folder-specific settings
Task ID: vscode_lp_077
Domain: vscode

Creates a multi-root workspace with two project folders (Python api and JavaScript frontend).
Both folders have realistic code files but NO folder-specific .vscode/settings.json.
VSCode is launched with the workspace open.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_077'

# Project paths
API_DIR = os.path.join(WORKDIR, 'projects', 'api')
FRONTEND_DIR = os.path.join(WORKDIR, 'projects', 'frontend')
WORKSPACE_FILE = os.path.join(WORKDIR, 'projects', 'projects.code-workspace')


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


def create_python_project():
    """Create a realistic Python API project."""
    os.makedirs(API_DIR, exist_ok=True)

    # Main application file
    with open(os.path.join(API_DIR, 'app.py'), 'w') as f:
        f.write('''\
from flask import Flask, jsonify, request
from datetime import datetime
from models import db, Employee, Department

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///company.db"
db.init_app(app)


@app.route("/api/employees", methods=["GET"])
def get_employees():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    employees = Employee.query.paginate(page=page, per_page=per_page)
    return jsonify({
        "employees": [emp.to_dict() for emp in employees.items],
        "total": employees.total,
        "pages": employees.pages,
        "current_page": page
    })


@app.route("/api/employees/<int:employee_id>", methods=["GET"])
def get_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    return jsonify(employee.to_dict())


@app.route("/api/departments", methods=["GET"])
def get_departments():
    departments = Department.query.all()
    return jsonify([dept.to_dict() for dept in departments])


@app.route("/api/employees", methods=["POST"])
def create_employee():
    data = request.get_json()
    employee = Employee(
        name=data["name"],
        email=data["email"],
        department_id=data["department_id"],
        salary=data.get("salary", 0),
        hire_date=datetime.strptime(data["hire_date"], "%Y-%m-%d").date()
    )
    db.session.add(employee)
    db.session.commit()
    return jsonify(employee.to_dict()), 201


if __name__ == "__main__":
    app.run(debug=True, port=8080)
''')

    # Models file
    with open(os.path.join(API_DIR, 'models.py'), 'w') as f:
        f.write('''\
from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()


class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    budget = db.Column(db.Float, default=0.0)
    manager_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=True)
    employees = db.relationship("Employee", backref="department", lazy=True,
                                foreign_keys="Employee.department_id")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "budget": self.budget,
            "employee_count": len(self.employees)
        }


class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))
    salary = db.Column(db.Float, default=0.0)
    hire_date = db.Column(db.Date, default=date.today)
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "department": self.department.name if self.department else None,
            "salary": self.salary,
            "hire_date": self.hire_date.isoformat(),
            "is_active": self.is_active
        }
''')

    # Config file
    with open(os.path.join(API_DIR, 'config.py'), 'w') as f:
        f.write('''\
import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-prod")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///company.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    ITEMS_PER_PAGE = 20


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    DEBUG = False


config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
''')

    # Requirements file
    with open(os.path.join(API_DIR, 'requirements.txt'), 'w') as f:
        f.write('''\
flask==3.0.2
flask-sqlalchemy==3.1.1
gunicorn==21.2.0
black==24.2.0
pytest==8.0.2
''')

    print(f'Python project created at {API_DIR}')


def create_javascript_project():
    """Create a realistic JavaScript frontend project."""
    os.makedirs(FRONTEND_DIR, exist_ok=True)
    os.makedirs(os.path.join(FRONTEND_DIR, 'src'), exist_ok=True)
    os.makedirs(os.path.join(FRONTEND_DIR, 'src', 'components'), exist_ok=True)

    # Package.json
    with open(os.path.join(FRONTEND_DIR, 'package.json'), 'w') as f:
        json.dump({
            "name": "company-dashboard",
            "version": "2.1.0",
            "private": True,
            "scripts": {
                "dev": "vite",
                "build": "vite build",
                "preview": "vite preview",
                "lint": "eslint src/",
                "format": "prettier --write src/"
            },
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "react-router-dom": "^6.22.0",
                "axios": "^1.6.7"
            },
            "devDependencies": {
                "vite": "^5.1.0",
                "@vitejs/plugin-react": "^4.2.1",
                "eslint": "^8.56.0",
                "prettier": "^3.2.5"
            }
        }, f, indent=2)

    # Main App component
    with open(os.path.join(FRONTEND_DIR, 'src', 'App.jsx'), 'w') as f:
        f.write('''\
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './components/Dashboard';
import EmployeeList from './components/EmployeeList';

function App() {
  return (
    <BrowserRouter>
      <div className="app-container">
        <Navbar />
        <main className="content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/employees" element={<EmployeeList />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
''')

    # Dashboard component
    with open(os.path.join(FRONTEND_DIR, 'src', 'components', 'Dashboard.jsx'), 'w') as f:
        f.write('''\
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Dashboard() {
  const [stats, setStats] = useState({
    totalEmployees: 0,
    departments: 0,
    avgSalary: 0,
    recentHires: []
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchStats() {
      try {
        const [empRes, deptRes] = await Promise.all([
          axios.get('/api/employees?per_page=100'),
          axios.get('/api/departments')
        ]);
        const employees = empRes.data.employees;
        const totalSalary = employees.reduce((sum, emp) => sum + emp.salary, 0);
        setStats({
          totalEmployees: empRes.data.total,
          departments: deptRes.data.length,
          avgSalary: employees.length > 0 ? totalSalary / employees.length : 0,
          recentHires: employees.slice(0, 5)
        });
      } catch (error) {
        console.error('Failed to fetch dashboard stats:', error);
      } finally {
        setLoading(false);
      }
    }
    fetchStats();
  }, []);

  if (loading) {
    return <div className="loading-spinner">Loading dashboard...</div>;
  }

  return (
    <div className="dashboard">
      <h1>Company Dashboard</h1>
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Employees</h3>
          <p className="stat-value">{stats.totalEmployees}</p>
        </div>
        <div className="stat-card">
          <h3>Departments</h3>
          <p className="stat-value">{stats.departments}</p>
        </div>
        <div className="stat-card">
          <h3>Average Salary</h3>
          <p className="stat-value">${stats.avgSalary.toLocaleString()}</p>
        </div>
      </div>
      <h2>Recent Hires</h2>
      <ul className="recent-hires">
        {stats.recentHires.map(emp => (
          <li key={emp.id}>{emp.name} - {emp.department}</li>
        ))}
      </ul>
    </div>
  );
}

export default Dashboard;
''')

    # Navbar component
    with open(os.path.join(FRONTEND_DIR, 'src', 'components', 'Navbar.jsx'), 'w') as f:
        f.write('''\
import React from 'react';
import { Link, useLocation } from 'react-router-dom';

function Navbar() {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Dashboard' },
    { path: '/employees', label: 'Employees' },
  ];

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <h2>CompanyHub</h2>
      </div>
      <ul className="nav-links">
        {navItems.map(item => (
          <li key={item.path}>
            <Link
              to={item.path}
              className={location.pathname === item.path ? 'active' : ''}
            >
              {item.label}
            </Link>
          </li>
        ))}
      </ul>
    </nav>
  );
}

export default Navbar;
''')

    # EmployeeList component
    with open(os.path.join(FRONTEND_DIR, 'src', 'components', 'EmployeeList.jsx'), 'w') as f:
        f.write('''\
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function EmployeeList() {
  const [employees, setEmployees] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    async function fetchEmployees() {
      try {
        const response = await axios.get(`/api/employees?page=${page}&per_page=20`);
        setEmployees(response.data.employees);
        setTotalPages(response.data.pages);
      } catch (error) {
        console.error('Failed to fetch employees:', error);
      }
    }
    fetchEmployees();
  }, [page]);

  const filteredEmployees = employees.filter(emp =>
    emp.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="employee-list">
      <h1>Employees</h1>
      <input
        type="text"
        placeholder="Search employees..."
        value={searchQuery}
        onChange={e => setSearchQuery(e.target.value)}
        className="search-input"
      />
      <table className="employee-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Department</th>
            <th>Salary</th>
            <th>Hire Date</th>
          </tr>
        </thead>
        <tbody>
          {filteredEmployees.map(emp => (
            <tr key={emp.id}>
              <td>{emp.name}</td>
              <td>{emp.email}</td>
              <td>{emp.department}</td>
              <td>${emp.salary.toLocaleString()}</td>
              <td>{new Date(emp.hire_date).toLocaleDateString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="pagination">
        <button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1}>
          Previous
        </button>
        <span>Page {page} of {totalPages}</span>
        <button onClick={() => setPage(p => Math.min(totalPages, p + 1))} disabled={page === totalPages}>
          Next
        </button>
      </div>
    </div>
  );
}

export default EmployeeList;
''')

    print(f'JavaScript project created at {FRONTEND_DIR}')


def create_workspace():
    """Create a multi-root workspace file."""
    workspace = {
        "folders": [
            {"path": os.path.join(WORKDIR, 'projects', 'api')},
            {"path": os.path.join(WORKDIR, 'projects', 'frontend')}
        ]
    }
    os.makedirs(os.path.dirname(WORKSPACE_FILE), exist_ok=True)
    with open(WORKSPACE_FILE, 'w') as f:
        json.dump(workspace, f, indent=4)
    print(f'Workspace file created: {WORKSPACE_FILE}')


def main():
    # Ensure no leftover .vscode dirs from previous runs
    import shutil
    for d in [os.path.join(API_DIR, '.vscode'), os.path.join(FRONTEND_DIR, '.vscode')]:
        if os.path.exists(d):
            shutil.rmtree(d)

    create_python_project()
    create_javascript_project()
    create_workspace()

    # Launch VSCode with the workspace
    launch_gui(f'code "{WORKSPACE_FILE}"', delay_sec=3.0)
    print('GUI_READY: VSCode launched with multi-root workspace')


main()

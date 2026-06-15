"""
Initial Setup: Create VSCode workspace with webapp project for Lighthouse CI auditing task.
Task ID: vscode_web_068
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_068'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'webapp')
VSCODE_DIR = os.path.join(PROJECT_DIR, '.vscode')
DIST_DIR = os.path.join(PROJECT_DIR, 'dist')


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
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(VSCODE_DIR, exist_ok=True)
    os.makedirs(DIST_DIR, exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'components'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'styles'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'utils'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'public'), exist_ok=True)

    # --- package.json ---
    package_json = {
        "name": "webapp",
        "version": "2.1.0",
        "description": "Healthcare appointment scheduling platform",
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
            "react-router-dom": "^6.20.1",
            "axios": "^1.6.2",
            "@mui/material": "^5.15.0",
            "@emotion/react": "^11.11.0",
            "@emotion/styled": "^11.11.0"
        },
        "devDependencies": {
            "react-scripts": "5.0.1",
            "eslint": "^8.56.0",
            "@lhci/cli": "^0.13.0"
        }
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # --- lighthouserc.js (Lighthouse CI config) ---
    lhci_config = """module.exports = {
  ci: {
    collect: {
      staticDistDir: './dist',
      numberOfRuns: 1,
    },
    assert: {
      preset: 'lighthouse:recommended',
      assertions: {
        'categories:performance': ['warn', { minScore: 0.8 }],
        'categories:accessibility': ['error', { minScore: 0.9 }],
        'categories:seo': ['warn', { minScore: 0.7 }],
      },
    },
    upload: {
      target: 'temporary-public-storage',
    },
  },
};
"""
    with open(os.path.join(PROJECT_DIR, 'lighthouserc.js'), 'w') as f:
        f.write(lhci_config)

    # --- .vscode/settings.json (workspace settings, NO tasks) ---
    vscode_settings = {
        "editor.tabSize": 2,
        "editor.formatOnSave": True,
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "files.exclude": {
            "node_modules": True,
            ".git": True
        }
    }
    with open(os.path.join(VSCODE_DIR, 'settings.json'), 'w') as f:
        json.dump(vscode_settings, f, indent=4)

    # --- src/index.js ---
    index_js = """import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles/global.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
"""
    with open(os.path.join(PROJECT_DIR, 'src', 'index.js'), 'w') as f:
        f.write(index_js)

    # --- src/App.js ---
    app_js = """import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import AppointmentList from './components/AppointmentList';
import PatientProfile from './components/PatientProfile';

function App() {
  return (
    <BrowserRouter>
      <div className="app-container">
        <header>
          <h1>MediSchedule Pro</h1>
          <nav>
            <a href="/">Dashboard</a>
            <a href="/appointments">Appointments</a>
            <a href="/patients">Patients</a>
          </nav>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/appointments" element={<AppointmentList />} />
            <Route path="/patients/:id" element={<PatientProfile />} />
          </Routes>
        </main>
        <footer>
          <p>&copy; 2025 MediSchedule Pro. All rights reserved.</p>
        </footer>
      </div>
    </BrowserRouter>
  );
}

export default App;
"""
    with open(os.path.join(PROJECT_DIR, 'src', 'App.js'), 'w') as f:
        f.write(app_js)

    # --- src/components/Dashboard.js ---
    dashboard_js = """import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Dashboard() {
  const [stats, setStats] = useState({
    todayAppointments: 0,
    pendingReviews: 0,
    totalPatients: 0,
  });

  useEffect(() => {
    axios.get('/api/dashboard/stats')
      .then(res => setStats(res.data))
      .catch(err => console.error('Failed to load stats:', err));
  }, []);

  return (
    <section className="dashboard">
      <h2>Today's Overview</h2>
      <div className="stats-grid">
        <div className="stat-card">
          <span className="stat-value">{stats.todayAppointments}</span>
          <span className="stat-label">Appointments Today</span>
        </div>
        <div className="stat-card">
          <span className="stat-value">{stats.pendingReviews}</span>
          <span className="stat-label">Pending Reviews</span>
        </div>
        <div className="stat-card">
          <span className="stat-value">{stats.totalPatients}</span>
          <span className="stat-label">Total Patients</span>
        </div>
      </div>
    </section>
  );
}

export default Dashboard;
"""
    with open(os.path.join(PROJECT_DIR, 'src', 'components', 'Dashboard.js'), 'w') as f:
        f.write(dashboard_js)

    # --- src/components/AppointmentList.js ---
    appointment_js = """import React, { useState, useEffect } from 'react';
import axios from 'axios';

function AppointmentList() {
  const [appointments, setAppointments] = useState([]);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    axios.get('/api/appointments', { params: { status: filter } })
      .then(res => setAppointments(res.data))
      .catch(err => console.error('Failed to load appointments:', err));
  }, [filter]);

  return (
    <section className="appointments">
      <h2>Appointments</h2>
      <div className="filter-bar">
        <button onClick={() => setFilter('all')}>All</button>
        <button onClick={() => setFilter('upcoming')}>Upcoming</button>
        <button onClick={() => setFilter('completed')}>Completed</button>
      </div>
      <table className="appointment-table">
        <thead>
          <tr>
            <th>Patient</th>
            <th>Date</th>
            <th>Time</th>
            <th>Doctor</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {appointments.map(appt => (
            <tr key={appt.id}>
              <td>{appt.patientName}</td>
              <td>{appt.date}</td>
              <td>{appt.time}</td>
              <td>{appt.doctor}</td>
              <td className={`status-${appt.status}`}>{appt.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}

export default AppointmentList;
"""
    with open(os.path.join(PROJECT_DIR, 'src', 'components', 'AppointmentList.js'), 'w') as f:
        f.write(appointment_js)

    # --- src/components/PatientProfile.js ---
    patient_js = """import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

function PatientProfile() {
  const { id } = useParams();
  const [patient, setPatient] = useState(null);

  useEffect(() => {
    axios.get(`/api/patients/${id}`)
      .then(res => setPatient(res.data))
      .catch(err => console.error('Failed to load patient:', err));
  }, [id]);

  if (!patient) return <p>Loading patient profile...</p>;

  return (
    <section className="patient-profile">
      <h2>{patient.name}</h2>
      <div className="patient-info">
        <p><strong>DOB:</strong> {patient.dateOfBirth}</p>
        <p><strong>Phone:</strong> {patient.phone}</p>
        <p><strong>Email:</strong> {patient.email}</p>
        <p><strong>Insurance:</strong> {patient.insuranceProvider}</p>
      </div>
      <h3>Medical History</h3>
      <ul>
        {patient.history.map((entry, idx) => (
          <li key={idx}>{entry.date} - {entry.description}</li>
        ))}
      </ul>
    </section>
  );
}

export default PatientProfile;
"""
    with open(os.path.join(PROJECT_DIR, 'src', 'components', 'PatientProfile.js'), 'w') as f:
        f.write(patient_js)

    # --- src/styles/global.css ---
    global_css = """* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f5f7fa;
  color: #2d3748;
}

.app-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background: #2563eb;
  color: white;
  border-radius: 8px;
  margin-bottom: 24px;
}

header nav a {
  color: white;
  text-decoration: none;
  margin-left: 16px;
  font-weight: 500;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-top: 16px;
}

.stat-card {
  background: white;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  text-align: center;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #2563eb;
  display: block;
}

.stat-label {
  color: #718096;
  font-size: 0.875rem;
  margin-top: 4px;
}

.appointment-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 16px;
}

.appointment-table th,
.appointment-table td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}

.appointment-table th {
  background: #f7fafc;
  font-weight: 600;
}

footer {
  margin-top: 48px;
  padding: 16px;
  text-align: center;
  color: #a0aec0;
  font-size: 0.875rem;
}
"""
    with open(os.path.join(PROJECT_DIR, 'src', 'styles', 'global.css'), 'w') as f:
        f.write(global_css)

    # --- src/utils/api.js ---
    api_js = """import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:3001/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;
"""
    with open(os.path.join(PROJECT_DIR, 'src', 'utils', 'api.js'), 'w') as f:
        f.write(api_js)

    # --- public/index.html ---
    index_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="description" content="MediSchedule Pro - Healthcare appointment scheduling platform" />
  <title>MediSchedule Pro</title>
</head>
<body>
  <noscript>You need to enable JavaScript to run this app.</noscript>
  <div id="root"></div>
</body>
</html>
"""
    with open(os.path.join(PROJECT_DIR, 'public', 'index.html'), 'w') as f:
        f.write(index_html)

    # --- dist/ (production build output) ---
    dist_index = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <meta name="description" content="MediSchedule Pro - Healthcare appointment scheduling platform"/>
  <title>MediSchedule Pro</title>
  <link rel="stylesheet" href="/static/css/main.a1b2c3d4.css"/>
</head>
<body>
  <noscript>You need to enable JavaScript to run this app.</noscript>
  <div id="root"></div>
  <script src="/static/js/main.e5f6a7b8.js"></script>
</body>
</html>
"""
    with open(os.path.join(DIST_DIR, 'index.html'), 'w') as f:
        f.write(dist_index)

    # Create minimal static assets in dist
    os.makedirs(os.path.join(DIST_DIR, 'static', 'css'), exist_ok=True)
    os.makedirs(os.path.join(DIST_DIR, 'static', 'js'), exist_ok=True)

    with open(os.path.join(DIST_DIR, 'static', 'css', 'main.a1b2c3d4.css'), 'w') as f:
        f.write('body{font-family:Segoe UI,sans-serif;margin:0}')

    with open(os.path.join(DIST_DIR, 'static', 'js', 'main.e5f6a7b8.js'), 'w') as f:
        f.write('!function(){console.log("MediSchedule Pro v2.1.0")}();')

    # --- .gitignore ---
    gitignore = """node_modules/
.env
.env.local
build/
coverage/
.lighthouseci/
"""
    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write(gitignore)

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'dist/ build directory exists: {os.path.isdir(DIST_DIR)}')

    # --- GUI-ready: Open VSCode with the project folder ---
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

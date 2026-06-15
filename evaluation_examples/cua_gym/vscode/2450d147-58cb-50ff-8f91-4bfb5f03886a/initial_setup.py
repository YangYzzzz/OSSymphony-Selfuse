"""
Initial Setup: Multi-root workspace with frontend and backend folders
Task ID: vscode_we_019
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_019'
PROJECTS_DIR = os.path.join(WORKDIR, 'projects')
FRONTEND_DIR = os.path.join(PROJECTS_DIR, 'frontend')
BACKEND_DIR = os.path.join(PROJECTS_DIR, 'backend')
WORKSPACE_FILE = os.path.join(PROJECTS_DIR, 'myproject.code-workspace')


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
    # Create project directories
    os.makedirs(FRONTEND_DIR, exist_ok=True)
    os.makedirs(BACKEND_DIR, exist_ok=True)

    # Create frontend source files (React-style project)
    os.makedirs(os.path.join(FRONTEND_DIR, 'src', 'components'), exist_ok=True)

    with open(os.path.join(FRONTEND_DIR, 'package.json'), 'w') as f:
        json.dump({
            "name": "dashboard-frontend",
            "version": "1.2.0",
            "description": "Analytics dashboard frontend",
            "main": "src/index.js",
            "scripts": {
                "start": "react-scripts start",
                "build": "react-scripts build",
                "test": "react-scripts test"
            },
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "axios": "^1.6.2"
            }
        }, f, indent=2)

    with open(os.path.join(FRONTEND_DIR, 'src', 'index.js'), 'w') as f:
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

    with open(os.path.join(FRONTEND_DIR, 'src', 'App.js'), 'w') as f:
        f.write("""import React, { useState, useEffect } from 'react';
import Dashboard from './components/Dashboard';

function App() {
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    fetch('/api/metrics')
      .then(res => res.json())
      .then(data => setMetrics(data))
      .catch(err => console.error('Failed to load metrics:', err));
  }, []);

  return (
    <div className="app-container">
      <header>
        <h1>Analytics Dashboard</h1>
      </header>
      <main>
        {metrics ? <Dashboard data={metrics} /> : <p>Loading...</p>}
      </main>
    </div>
  );
}

export default App;
""")

    with open(os.path.join(FRONTEND_DIR, 'src', 'components', 'Dashboard.js'), 'w') as f:
        f.write("""import React from 'react';

function Dashboard({ data }) {
  return (
    <div className="dashboard">
      <div className="metric-card">
        <h3>Total Revenue</h3>
        <p className="value">${data.totalRevenue.toLocaleString()}</p>
      </div>
      <div className="metric-card">
        <h3>Active Users</h3>
        <p className="value">{data.activeUsers.toLocaleString()}</p>
      </div>
      <div className="metric-card">
        <h3>Conversion Rate</h3>
        <p className="value">{data.conversionRate}%</p>
      </div>
    </div>
  );
}

export default Dashboard;
""")

    # Create backend source files (Python Flask-style project)
    os.makedirs(os.path.join(BACKEND_DIR, 'app', 'routes'), exist_ok=True)
    os.makedirs(os.path.join(BACKEND_DIR, 'app', 'models'), exist_ok=True)

    with open(os.path.join(BACKEND_DIR, 'requirements.txt'), 'w') as f:
        f.write("""flask==3.0.0
flask-cors==4.0.0
sqlalchemy==2.0.23
python-dotenv==1.0.0
gunicorn==21.2.0
marshmallow==3.20.1
""")

    with open(os.path.join(BACKEND_DIR, 'app', '__init__.py'), 'w') as f:
        f.write("""from flask import Flask
from flask_cors import CORS

def create_app(config_name='development'):
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///analytics.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from app.routes.metrics import metrics_bp
    app.register_blueprint(metrics_bp, url_prefix='/api')

    return app
""")

    with open(os.path.join(BACKEND_DIR, 'app', 'models', '__init__.py'), 'w') as f:
        f.write("")

    with open(os.path.join(BACKEND_DIR, 'app', 'models', 'metric.py'), 'w') as f:
        f.write("""from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class DailyMetric(Base):
    __tablename__ = 'daily_metrics'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    total_revenue = Column(Float, nullable=False)
    active_users = Column(Integer, nullable=False)
    conversion_rate = Column(Float, nullable=False)
    region = Column(String(50), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'totalRevenue': self.total_revenue,
            'activeUsers': self.active_users,
            'conversionRate': self.conversion_rate,
            'region': self.region,
        }
""")

    with open(os.path.join(BACKEND_DIR, 'app', 'routes', '__init__.py'), 'w') as f:
        f.write("")

    with open(os.path.join(BACKEND_DIR, 'app', 'routes', 'metrics.py'), 'w') as f:
        f.write("""from flask import Blueprint, jsonify

metrics_bp = Blueprint('metrics', __name__)


@metrics_bp.route('/metrics', methods=['GET'])
def get_metrics():
    summary = {
        'totalRevenue': 1247850.00,
        'activeUsers': 34521,
        'conversionRate': 3.72,
    }
    return jsonify(summary)


@metrics_bp.route('/metrics/daily', methods=['GET'])
def get_daily_metrics():
    # Placeholder for daily breakdown
    return jsonify({'data': [], 'count': 0})
""")

    with open(os.path.join(BACKEND_DIR, 'run.py'), 'w') as f:
        f.write("""from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
""")

    # Create the workspace file (NO .vscode/settings.json in either folder)
    workspace = {
        "folders": [
            {"path": "frontend"},
            {"path": "backend"}
        ],
        "settings": {}
    }
    with open(WORKSPACE_FILE, 'w') as f:
        json.dump(workspace, f, indent=4)

    print(f'Workspace file created: {WORKSPACE_FILE}')
    print(f'Frontend directory: {FRONTEND_DIR}')
    print(f'Backend directory: {BACKEND_DIR}')

    # Launch VSCode with the workspace
    launch_gui(f'code "{WORKSPACE_FILE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with workspace DISPLAY=:0')


create_initial()

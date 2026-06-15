"""
Initial Setup: Storybook development workflow in ~/project
Task ID: vscode_wf_075
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_075'
PROJECT_DIR = os.path.join(WORKDIR, 'project')

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
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'components'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'styles'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'public'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, '.vscode'), exist_ok=True)

    # package.json with @storybook/react in devDependencies
    package_json = {
        "name": "react-component-library",
        "version": "1.2.0",
        "description": "Internal UI component library for Meridian Analytics dashboard",
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
            "react-scripts": "5.0.1",
            "prop-types": "^15.8.1",
            "classnames": "^2.3.2"
        },
        "devDependencies": {
            "@storybook/react": "^7.6.7",
            "@storybook/addon-essentials": "^7.6.7",
            "@storybook/addon-interactions": "^7.6.7",
            "@storybook/testing-library": "^0.2.2",
            "eslint": "^8.56.0",
            "eslint-plugin-react": "^7.33.2",
            "prettier": "^3.2.2"
        },
        "browserslist": {
            "production": [">0.2%", "not dead", "not op_mini all"],
            "development": ["last 1 chrome version", "last 1 firefox version", "last 1 safari version"]
        }
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # src/index.js
    with open(os.path.join(PROJECT_DIR, 'src', 'index.js'), 'w') as f:
        f.write("""import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles/global.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
""")

    # src/App.js
    with open(os.path.join(PROJECT_DIR, 'src', 'App.js'), 'w') as f:
        f.write("""import React from 'react';
import Button from './components/Button';

function App() {
  return (
    <div className="app-container">
      <header>
        <h1>Meridian Analytics</h1>
        <p>Component Library Demo</p>
      </header>
      <main>
        <section className="button-showcase">
          <h2>Buttons</h2>
          <Button>Default Action</Button>
          <Button variant="primary">Submit Report</Button>
          <Button disabled>Archived</Button>
        </section>
      </main>
    </div>
  );
}

export default App;
""")

    # src/components/Button.jsx - the existing component
    with open(os.path.join(PROJECT_DIR, 'src', 'components', 'Button.jsx'), 'w') as f:
        f.write("""import React from 'react';
import PropTypes from 'prop-types';
import classnames from 'classnames';

const Button = ({
  children,
  variant = 'default',
  size = 'medium',
  disabled = false,
  loading = false,
  onClick,
  type = 'button',
  className,
  ...rest
}) => {
  const buttonClasses = classnames(
    'btn',
    `btn--${variant}`,
    `btn--${size}`,
    {
      'btn--disabled': disabled,
      'btn--loading': loading,
    },
    className
  );

  return (
    <button
      type={type}
      className={buttonClasses}
      disabled={disabled || loading}
      onClick={onClick}
      {...rest}
    >
      {loading && <span className="btn__spinner" aria-hidden="true" />}
      <span className={loading ? 'btn__text--hidden' : 'btn__text'}>
        {children}
      </span>
    </button>
  );
};

Button.propTypes = {
  children: PropTypes.node.isRequired,
  variant: PropTypes.oneOf(['default', 'primary', 'secondary', 'danger']),
  size: PropTypes.oneOf(['small', 'medium', 'large']),
  disabled: PropTypes.bool,
  loading: PropTypes.bool,
  onClick: PropTypes.func,
  type: PropTypes.oneOf(['button', 'submit', 'reset']),
  className: PropTypes.string,
};

export default Button;
""")

    # src/components/Button.css
    with open(os.path.join(PROJECT_DIR, 'src', 'components', 'Button.css'), 'w') as f:
        f.write(""".btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 16px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  background-color: #ffffff;
  color: #374151;
}

.btn--primary {
  background-color: #2563eb;
  border-color: #2563eb;
  color: #ffffff;
}

.btn--primary:hover {
  background-color: #1d4ed8;
}

.btn--secondary {
  background-color: #6b7280;
  border-color: #6b7280;
  color: #ffffff;
}

.btn--danger {
  background-color: #dc2626;
  border-color: #dc2626;
  color: #ffffff;
}

.btn--small { padding: 4px 10px; font-size: 12px; }
.btn--medium { padding: 8px 16px; font-size: 14px; }
.btn--large { padding: 12px 24px; font-size: 16px; }

.btn--disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn--loading {
  position: relative;
  cursor: wait;
}

.btn__spinner {
  width: 16px;
  height: 16px;
  border: 2px solid currentColor;
  border-right-color: transparent;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
  position: absolute;
}

.btn__text--hidden {
  visibility: hidden;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
""")

    # src/styles/global.css
    with open(os.path.join(PROJECT_DIR, 'src', 'styles', 'global.css'), 'w') as f:
        f.write("""* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
  color: #1f2937;
  background-color: #f9fafb;
}

.app-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}

header {
  margin-bottom: 32px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e5e7eb;
}

h1 { font-size: 28px; color: #111827; }
h2 { font-size: 20px; color: #374151; margin-bottom: 16px; }

.button-showcase {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  align-items: center;
}
""")

    # public/index.html
    with open(os.path.join(PROJECT_DIR, 'public', 'index.html'), 'w') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Meridian Analytics - Component Library</title>
</head>
<body>
  <div id="root"></div>
</body>
</html>
""")

    # .eslintrc.json
    with open(os.path.join(PROJECT_DIR, '.eslintrc.json'), 'w') as f:
        json.dump({
            "env": {"browser": True, "es2021": True, "jest": True},
            "extends": ["eslint:recommended", "plugin:react/recommended"],
            "parserOptions": {"ecmaFeatures": {"jsx": True}, "ecmaVersion": "latest", "sourceType": "module"},
            "plugins": ["react"],
            "rules": {"react/react-in-jsx-scope": "off", "react/prop-types": "warn"},
            "settings": {"react": {"version": "detect"}}
        }, f, indent=2)

    # .prettierrc
    with open(os.path.join(PROJECT_DIR, '.prettierrc'), 'w') as f:
        json.dump({
            "semi": True,
            "trailingComma": "es5",
            "singleQuote": True,
            "printWidth": 100,
            "tabWidth": 2
        }, f, indent=2)

    # .gitignore
    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write("""node_modules/
build/
.env
.env.local
coverage/
*.log
.DS_Store
storybook-static/
""")

    # Empty .vscode/settings.json for project-level settings
    with open(os.path.join(PROJECT_DIR, '.vscode', 'settings.json'), 'w') as f:
        json.dump({
            "editor.formatOnSave": True,
            "editor.defaultFormatter": "esbenp.prettier-vscode",
            "editor.tabSize": 2,
            "emmet.includeLanguages": {
                "javascript": "javascriptreact"
            }
        }, f, indent=2)

    # NO .storybook directory
    # NO stories files
    # NO storybook tasks in tasks.json
    # NO storybook debug config in launch.json

    print(f'Initial project created at: {PROJECT_DIR}')

    # Launch VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()

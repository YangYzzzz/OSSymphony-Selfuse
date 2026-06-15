"""
Initial Setup: Move components/ folder from project root into src/ directory
Task ID: vscode_file_063
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_file_063'
PROJECT_DIR = f'{WORKDIR}/react-project'


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
    # Clean up any previous state
    import shutil
    if os.path.exists(PROJECT_DIR):
        shutil.rmtree(PROJECT_DIR)

    # Create directory structure
    os.makedirs(f'{PROJECT_DIR}/components', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)

    # --- components/Button.jsx ---
    with open(f'{PROJECT_DIR}/components/Button.jsx', 'w') as f:
        f.write("""import React from 'react';
import PropTypes from 'prop-types';

const Button = ({ label, onClick, variant = 'primary', disabled = false }) => {
  const baseStyles = {
    padding: '8px 16px',
    borderRadius: '4px',
    border: 'none',
    cursor: disabled ? 'not-allowed' : 'pointer',
    fontSize: '14px',
    fontWeight: '500',
    opacity: disabled ? 0.6 : 1,
  };

  const variantStyles = {
    primary: { backgroundColor: '#007bff', color: '#ffffff' },
    secondary: { backgroundColor: '#6c757d', color: '#ffffff' },
    danger: { backgroundColor: '#dc3545', color: '#ffffff' },
  };

  return (
    <button
      style={{ ...baseStyles, ...(variantStyles[variant] || variantStyles.primary) }}
      onClick={onClick}
      disabled={disabled}
    >
      {label}
    </button>
  );
};

Button.propTypes = {
  label: PropTypes.string.isRequired,
  onClick: PropTypes.func,
  variant: PropTypes.oneOf(['primary', 'secondary', 'danger']),
  disabled: PropTypes.bool,
};

export default Button;
""")

    # --- components/Modal.jsx ---
    with open(f'{PROJECT_DIR}/components/Modal.jsx', 'w') as f:
        f.write("""import React, { useEffect } from 'react';
import PropTypes from 'prop-types';

const Modal = ({ isOpen, onClose, title, children }) => {
  useEffect(() => {
    const handleEsc = (event) => {
      if (event.key === 'Escape') {
        onClose();
      }
    };
    if (isOpen) {
      document.addEventListener('keydown', handleEsc);
    }
    return () => {
      document.removeEventListener('keydown', handleEsc);
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const overlayStyle = {
    position: 'fixed',
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 1000,
  };

  const modalStyle = {
    backgroundColor: '#ffffff',
    borderRadius: '8px',
    padding: '24px',
    maxWidth: '500px',
    width: '90%',
    boxShadow: '0 4px 20px rgba(0, 0, 0, 0.15)',
  };

  return (
    <div style={overlayStyle} onClick={onClose}>
      <div style={modalStyle} onClick={(e) => e.stopPropagation()}>
        <h2 style={{ marginTop: 0 }}>{title}</h2>
        <div>{children}</div>
        <button onClick={onClose} style={{ marginTop: '16px' }}>
          Close
        </button>
      </div>
    </div>
  );
};

Modal.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  title: PropTypes.string,
  children: PropTypes.node,
};

export default Modal;
""")

    # --- components/Header.jsx ---
    with open(f'{PROJECT_DIR}/components/Header.jsx', 'w') as f:
        f.write("""import React, { useState } from 'react';
import PropTypes from 'prop-types';

const Header = ({ title, navLinks = [], onMenuToggle }) => {
  const [menuOpen, setMenuOpen] = useState(false);

  const headerStyle = {
    backgroundColor: '#282c34',
    color: '#ffffff',
    padding: '0 24px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    height: '60px',
    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.2)',
  };

  const navStyle = {
    display: 'flex',
    gap: '20px',
    listStyle: 'none',
    margin: 0,
    padding: 0,
  };

  const linkStyle = {
    color: '#abb2bf',
    textDecoration: 'none',
    fontSize: '14px',
    transition: 'color 0.2s',
  };

  const handleMenuToggle = () => {
    setMenuOpen(!menuOpen);
    if (onMenuToggle) {
      onMenuToggle(!menuOpen);
    }
  };

  return (
    <header style={headerStyle}>
      <h1 style={{ margin: 0, fontSize: '20px' }}>{title}</h1>
      <nav>
        <ul style={navStyle}>
          {navLinks.map((link, index) => (
            <li key={index}>
              <a href={link.href} style={linkStyle}>
                {link.label}
              </a>
            </li>
          ))}
        </ul>
      </nav>
      <button onClick={handleMenuToggle} style={{ background: 'none', border: 'none', color: '#ffffff', cursor: 'pointer' }}>
        {menuOpen ? 'Close' : 'Menu'}
      </button>
    </header>
  );
};

Header.propTypes = {
  title: PropTypes.string.isRequired,
  navLinks: PropTypes.arrayOf(
    PropTypes.shape({
      href: PropTypes.string,
      label: PropTypes.string,
    })
  ),
  onMenuToggle: PropTypes.func,
};

export default Header;
""")

    # --- src/App.js ---
    with open(f'{PROJECT_DIR}/src/App.js', 'w') as f:
        f.write("""import React, { useState } from 'react';
import Button from '../components/Button';
import Modal from '../components/Modal';
import Header from '../components/Header';
import './App.css';

const NAV_LINKS = [
  { href: '#home', label: 'Home' },
  { href: '#about', label: 'About' },
  { href: '#contact', label: 'Contact' },
];

function App() {
  const [modalOpen, setModalOpen] = useState(false);

  return (
    <div className="App">
      <Header
        title="My React App"
        navLinks={NAV_LINKS}
      />
      <main style={{ padding: '40px 24px' }}>
        <h2>Welcome to My React App</h2>
        <p>This is a simple React application demonstrating component composition.</p>
        <div style={{ display: 'flex', gap: '12px', marginTop: '20px' }}>
          <Button
            label="Open Modal"
            onClick={() => setModalOpen(true)}
            variant="primary"
          />
          <Button
            label="Secondary Action"
            variant="secondary"
          />
          <Button
            label="Disabled"
            disabled={true}
          />
        </div>
      </main>
      <Modal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        title="Example Modal"
      >
        <p>This modal was opened by clicking the button above.</p>
        <p>Press Escape or click outside to close.</p>
      </Modal>
    </div>
  );
}

export default App;
""")

    # --- src/index.js ---
    with open(f'{PROJECT_DIR}/src/index.js', 'w') as f:
        f.write("""import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
""")

    # --- package.json ---
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        f.write("""{
  "name": "react-project",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "@testing-library/jest-dom": "^5.17.0",
    "@testing-library/react": "^13.4.0",
    "@testing-library/user-event": "^13.5.0",
    "prop-types": "^15.8.1",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "web-vitals": "^2.1.4"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
""")

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'  components/Button.jsx')
    print(f'  components/Modal.jsx')
    print(f'  components/Header.jsx')
    print(f'  src/App.js')
    print(f'  src/index.js')
    print(f'  package.json')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with react-project folder, DISPLAY=:0')


create_initial()

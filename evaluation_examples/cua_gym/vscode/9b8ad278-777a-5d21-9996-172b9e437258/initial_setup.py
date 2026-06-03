"""
Initial Setup: VSCode breadcrumbs navigation task
Task ID: vscode_edit_067
Domain: vs_code

Creates the project directory structure for breadcrumb navigation:
  ~/Desktop/project/
    src/
      components/
        Button.js
        Header.js
        Footer.js
        NavBar.js
      pages/
        HomePage.js
        AboutPage.js
        ContactPage.js
        DashboardPage.js
      utils/
        formatters/
          dateFormatter.js   <-- target file (opened in editor)
          numberFormatter.js
          stringFormatter.js
        validators/
          emailValidator.js
          formValidator.js
        helpers.js
        constants.js
      index.js
    public/
      index.html
      favicon.ico
    package.json
    README.md
    .gitignore

Opens VSCode with the project folder and the target file active.
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_067'
DESKTOP = f'{WORKDIR}/Desktop'
PROJECT_DIR = f'{DESKTOP}/project'
TARGET_FILE = f'{PROJECT_DIR}/src/utils/formatters/dateFormatter.js'


def create_dir(path):
    os.makedirs(path, exist_ok=True)


def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env['DISPLAY'] = ':0'
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_initial():
    # --- Create directory structure ---
    create_dir(f'{PROJECT_DIR}/src/components')
    create_dir(f'{PROJECT_DIR}/src/pages')
    create_dir(f'{PROJECT_DIR}/src/utils/formatters')
    create_dir(f'{PROJECT_DIR}/src/utils/validators')
    create_dir(f'{PROJECT_DIR}/public')

    # --- src/components ---
    write_file(f'{PROJECT_DIR}/src/components/Button.js', """\
import React from 'react';

const Button = ({ label, onClick, variant = 'primary', disabled = false }) => {
  return (
    <button
      className={`btn btn-${variant}`}
      onClick={onClick}
      disabled={disabled}
    >
      {label}
    </button>
  );
};

export default Button;
""")

    write_file(f'{PROJECT_DIR}/src/components/Header.js', """\
import React from 'react';
import NavBar from './NavBar';

const Header = ({ title, user }) => {
  return (
    <header className="app-header">
      <h1 className="header-title">{title}</h1>
      <NavBar user={user} />
    </header>
  );
};

export default Header;
""")

    write_file(f'{PROJECT_DIR}/src/components/Footer.js', """\
import React from 'react';

const Footer = () => {
  const currentYear = new Date().getFullYear();
  return (
    <footer className="app-footer">
      <p>&copy; {currentYear} Acme Corp. All rights reserved.</p>
    </footer>
  );
};

export default Footer;
""")

    write_file(f'{PROJECT_DIR}/src/components/NavBar.js', """\
import React, { useState } from 'react';

const NavBar = ({ user }) => {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <nav className="navbar">
      <ul className={`nav-links ${menuOpen ? 'open' : ''}`}>
        <li><a href="/">Home</a></li>
        <li><a href="/about">About</a></li>
        <li><a href="/contact">Contact</a></li>
        {user && <li><a href="/dashboard">Dashboard</a></li>}
      </ul>
      <button className="menu-toggle" onClick={() => setMenuOpen(!menuOpen)}>
        &#9776;
      </button>
    </nav>
  );
};

export default NavBar;
""")

    # --- src/pages ---
    write_file(f'{PROJECT_DIR}/src/pages/HomePage.js', """\
import React from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';

const HomePage = () => {
  return (
    <div className="page home-page">
      <Header title="Welcome to Acme" />
      <main>
        <section className="hero">
          <h2>Innovative Solutions for Your Business</h2>
          <p>We deliver cutting-edge software solutions tailored to your needs.</p>
        </section>
        <section className="features">
          <h3>Our Services</h3>
          <ul>
            <li>Web Development</li>
            <li>Mobile Applications</li>
            <li>Cloud Infrastructure</li>
            <li>Data Analytics</li>
          </ul>
        </section>
      </main>
      <Footer />
    </div>
  );
};

export default HomePage;
""")

    write_file(f'{PROJECT_DIR}/src/pages/AboutPage.js', """\
import React from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';

const AboutPage = () => {
  return (
    <div className="page about-page">
      <Header title="About Us" />
      <main>
        <section className="about-content">
          <h2>Our Story</h2>
          <p>Founded in 2015, Acme Corp has been at the forefront of digital innovation.</p>
          <p>Our team of 50+ engineers is dedicated to crafting exceptional software.</p>
        </section>
      </main>
      <Footer />
    </div>
  );
};

export default AboutPage;
""")

    write_file(f'{PROJECT_DIR}/src/pages/ContactPage.js', """\
import React, { useState } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import Button from '../components/Button';

const ContactPage = () => {
  const [formData, setFormData] = useState({ name: '', email: '', message: '' });

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Form submitted:', formData);
  };

  return (
    <div className="page contact-page">
      <Header title="Contact Us" />
      <main>
        <form onSubmit={handleSubmit}>
          <input type="text" placeholder="Your Name" value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })} />
          <input type="email" placeholder="Your Email" value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })} />
          <textarea placeholder="Your Message" value={formData.message}
            onChange={(e) => setFormData({ ...formData, message: e.target.value })} />
          <Button label="Send Message" onClick={handleSubmit} />
        </form>
      </main>
      <Footer />
    </div>
  );
};

export default ContactPage;
""")

    write_file(f'{PROJECT_DIR}/src/pages/DashboardPage.js', """\
import React, { useEffect, useState } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { formatDate } from '../utils/formatters/dateFormatter';

const DashboardPage = ({ user }) => {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    // Simulate fetching dashboard data
    setStats({
      totalOrders: 142,
      pendingOrders: 8,
      revenue: 28450.75,
      lastUpdated: new Date()
    });
  }, []);

  return (
    <div className="page dashboard-page">
      <Header title="Dashboard" user={user} />
      <main>
        {stats && (
          <div className="stats-grid">
            <div className="stat-card">
              <h3>Total Orders</h3>
              <p>{stats.totalOrders}</p>
            </div>
            <div className="stat-card">
              <h3>Pending Orders</h3>
              <p>{stats.pendingOrders}</p>
            </div>
            <div className="stat-card">
              <h3>Revenue</h3>
              <p>${stats.revenue.toFixed(2)}</p>
            </div>
            <div className="stat-card">
              <h3>Last Updated</h3>
              <p>{formatDate(stats.lastUpdated)}</p>
            </div>
          </div>
        )}
      </main>
      <Footer />
    </div>
  );
};

export default DashboardPage;
""")

    # --- src/utils/formatters ---
    write_file(TARGET_FILE, """\
/**
 * dateFormatter.js
 * Utility functions for formatting date and time values throughout the application.
 */

/**
 * Formats a Date object or date string into a human-readable string.
 * @param {Date|string} date - The date to format.
 * @param {string} locale - The locale string (default: 'en-US').
 * @returns {string} Formatted date string, e.g. "March 15, 2025"
 */
export function formatDate(date, locale = 'en-US') {
  const d = date instanceof Date ? date : new Date(date);
  return d.toLocaleDateString(locale, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

/**
 * Formats a Date object into a short date string.
 * @param {Date|string} date - The date to format.
 * @returns {string} Short date string, e.g. "03/15/2025"
 */
export function formatShortDate(date) {
  const d = date instanceof Date ? date : new Date(date);
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  const year = d.getFullYear();
  return `${month}/${day}/${year}`;
}

/**
 * Formats a Date object into an ISO 8601 date string.
 * @param {Date|string} date - The date to format.
 * @returns {string} ISO date string, e.g. "2025-03-15"
 */
export function formatISODate(date) {
  const d = date instanceof Date ? date : new Date(date);
  return d.toISOString().split('T')[0];
}

/**
 * Formats a Date object into a time string.
 * @param {Date|string} date - The date to format.
 * @param {boolean} includeSeconds - Whether to include seconds (default: false).
 * @returns {string} Time string, e.g. "2:30 PM" or "2:30:45 PM"
 */
export function formatTime(date, includeSeconds = false) {
  const d = date instanceof Date ? date : new Date(date);
  const options = {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true,
  };
  if (includeSeconds) {
    options.second = '2-digit';
  }
  return d.toLocaleTimeString('en-US', options);
}

/**
 * Returns a relative time string based on the difference from now.
 * @param {Date|string} date - The date to compare with now.
 * @returns {string} Relative time, e.g. "2 days ago", "just now"
 */
export function formatRelativeTime(date) {
  const d = date instanceof Date ? date : new Date(date);
  const now = new Date();
  const diffMs = now - d;
  const diffSecs = Math.floor(diffMs / 1000);
  const diffMins = Math.floor(diffSecs / 60);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);

  if (diffSecs < 60) return 'just now';
  if (diffMins < 60) return `${diffMins} minute${diffMins !== 1 ? 's' : ''} ago`;
  if (diffHours < 24) return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`;
  if (diffDays < 7) return `${diffDays} day${diffDays !== 1 ? 's' : ''} ago`;
  return formatDate(d);
}

export default {
  formatDate,
  formatShortDate,
  formatISODate,
  formatTime,
  formatRelativeTime,
};
""")

    write_file(f'{PROJECT_DIR}/src/utils/formatters/numberFormatter.js', """\
/**
 * numberFormatter.js
 * Utility functions for formatting numeric values throughout the application.
 */

/**
 * Formats a number as currency.
 * @param {number} value - The number to format.
 * @param {string} currency - The currency code (default: 'USD').
 * @returns {string} Formatted currency string, e.g. "$1,234.56"
 */
export function formatCurrency(value, currency = 'USD') {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
    minimumFractionDigits: 2,
  }).format(value);
}

/**
 * Formats a number with thousands separators.
 * @param {number} value - The number to format.
 * @param {number} decimals - Number of decimal places (default: 0).
 * @returns {string} Formatted number string, e.g. "1,234,567"
 */
export function formatNumber(value, decimals = 0) {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value);
}

/**
 * Formats a number as a percentage.
 * @param {number} value - The decimal value (0.0 to 1.0).
 * @param {number} decimals - Number of decimal places (default: 1).
 * @returns {string} Percentage string, e.g. "85.3%"
 */
export function formatPercent(value, decimals = 1) {
  return `${(value * 100).toFixed(decimals)}%`;
}

export default { formatCurrency, formatNumber, formatPercent };
""")

    write_file(f'{PROJECT_DIR}/src/utils/formatters/stringFormatter.js', """\
/**
 * stringFormatter.js
 * Utility functions for formatting and transforming string values.
 */

/**
 * Converts a string to title case.
 * @param {string} str - The string to convert.
 * @returns {string} Title-cased string.
 */
export function toTitleCase(str) {
  return str
    .toLowerCase()
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}

/**
 * Truncates a string to a maximum length and appends an ellipsis.
 * @param {string} str - The string to truncate.
 * @param {number} maxLength - Maximum length before truncation.
 * @returns {string} Truncated string.
 */
export function truncate(str, maxLength = 100) {
  if (str.length <= maxLength) return str;
  return str.slice(0, maxLength - 3) + '...';
}

/**
 * Converts camelCase to a human-readable label.
 * @param {string} str - The camelCase string.
 * @returns {string} Human-readable string, e.g. "camelCase" -> "Camel Case"
 */
export function camelToLabel(str) {
  return str.replace(/([A-Z])/g, ' $1').replace(/^./, s => s.toUpperCase());
}

export default { toTitleCase, truncate, camelToLabel };
""")

    # --- src/utils/validators ---
    write_file(f'{PROJECT_DIR}/src/utils/validators/emailValidator.js', """\
/**
 * emailValidator.js
 * Utility functions for validating email addresses.
 */

const EMAIL_REGEX = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$/;

/**
 * Validates whether a string is a properly formatted email address.
 * @param {string} email - The email address to validate.
 * @returns {boolean} True if valid, false otherwise.
 */
export function isValidEmail(email) {
  if (!email || typeof email !== 'string') return false;
  return EMAIL_REGEX.test(email.trim());
}

/**
 * Returns a validation result object for an email address.
 * @param {string} email - The email address to validate.
 * @returns {{ valid: boolean, error: string|null }}
 */
export function validateEmail(email) {
  if (!email) return { valid: false, error: 'Email is required' };
  if (!isValidEmail(email)) return { valid: false, error: 'Invalid email format' };
  return { valid: true, error: null };
}

export default { isValidEmail, validateEmail };
""")

    write_file(f'{PROJECT_DIR}/src/utils/validators/formValidator.js', """\
/**
 * formValidator.js
 * General form validation utility functions.
 */

import { isValidEmail } from './emailValidator';

/**
 * Validates that a value is not empty.
 * @param {any} value - The value to check.
 * @returns {{ valid: boolean, error: string|null }}
 */
export function validateRequired(value) {
  const isEmpty = value === null || value === undefined ||
    (typeof value === 'string' && value.trim() === '');
  return isEmpty
    ? { valid: false, error: 'This field is required' }
    : { valid: true, error: null };
}

/**
 * Validates minimum string length.
 * @param {string} value - The string to check.
 * @param {number} min - Minimum allowed length.
 * @returns {{ valid: boolean, error: string|null }}
 */
export function validateMinLength(value, min) {
  if (!value || value.length < min) {
    return { valid: false, error: `Must be at least ${min} characters` };
  }
  return { valid: true, error: null };
}

export default { validateRequired, validateMinLength, isValidEmail };
""")

    write_file(f'{PROJECT_DIR}/src/utils/helpers.js', """\
/**
 * helpers.js
 * General utility helper functions used throughout the application.
 */

/**
 * Deep clones a plain JavaScript object.
 * @param {object} obj - The object to clone.
 * @returns {object} A deep copy of the object.
 */
export function deepClone(obj) {
  return JSON.parse(JSON.stringify(obj));
}

/**
 * Debounces a function call.
 * @param {Function} fn - The function to debounce.
 * @param {number} delay - Delay in milliseconds.
 * @returns {Function} Debounced function.
 */
export function debounce(fn, delay = 300) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}

/**
 * Groups an array of objects by a key.
 * @param {Array} items - Array of objects.
 * @param {string} key - Key to group by.
 * @returns {object} Grouped object.
 */
export function groupBy(items, key) {
  return items.reduce((acc, item) => {
    const group = item[key];
    if (!acc[group]) acc[group] = [];
    acc[group].push(item);
    return acc;
  }, {});
}

export default { deepClone, debounce, groupBy };
""")

    write_file(f'{PROJECT_DIR}/src/utils/constants.js', """\
/**
 * constants.js
 * Application-wide constants.
 */

export const APP_NAME = 'Acme App';
export const APP_VERSION = '2.4.1';
export const API_BASE_URL = 'https://api.acmecorp.example.com/v2';

export const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  NO_CONTENT: 204,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  INTERNAL_SERVER_ERROR: 500,
};

export const ROLES = {
  ADMIN: 'admin',
  EDITOR: 'editor',
  VIEWER: 'viewer',
};

export const DATE_FORMATS = {
  SHORT: 'MM/DD/YYYY',
  LONG: 'MMMM D, YYYY',
  ISO: 'YYYY-MM-DD',
  TIME: 'h:mm A',
};

export default {
  APP_NAME,
  APP_VERSION,
  API_BASE_URL,
  HTTP_STATUS,
  ROLES,
  DATE_FORMATS,
};
""")

    # --- src/index.js ---
    write_file(f'{PROJECT_DIR}/src/index.js', """\
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import AboutPage from './pages/AboutPage';
import ContactPage from './pages/ContactPage';
import DashboardPage from './pages/DashboardPage';
import './styles.css';

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/contact" element={<ContactPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
      </Routes>
    </Router>
  </React.StrictMode>
);
""")

    # --- public/index.html ---
    write_file(f'{PROJECT_DIR}/public/index.html', """\
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="description" content="Acme Corp Application" />
    <title>Acme App</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
""")

    # --- package.json ---
    write_file(f'{PROJECT_DIR}/package.json', json.dumps({
        "name": "acme-app",
        "version": "2.4.1",
        "description": "Acme Corp React Application",
        "private": True,
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.20.0"
        },
        "devDependencies": {
            "react-scripts": "5.0.1",
            "@testing-library/react": "^14.0.0",
            "@testing-library/jest-dom": "^6.1.0",
            "eslint": "^8.55.0"
        },
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test",
            "lint": "eslint src/"
        },
        "eslintConfig": {
            "extends": ["react-app", "react-app/jest"]
        },
        "browserslist": {
            "production": [">0.2%", "not dead", "not op_mini all"],
            "development": ["last 1 chrome version", "last 1 firefox version", "last 1 safari version"]
        }
    }, indent=2))

    # --- README.md ---
    write_file(f'{PROJECT_DIR}/README.md', """\
# Acme App

A production-grade React web application for Acme Corp.

## Project Structure

```
project/
  src/
    components/    React UI components (Button, Header, Footer, NavBar)
    pages/         Page-level components (Home, About, Contact, Dashboard)
    utils/
      formatters/  Date, number, and string formatting utilities
      validators/  Input validation utilities
      helpers.js   General helper functions
      constants.js Application-wide constants
    index.js       Application entry point
  public/
    index.html     HTML template
  package.json     Project dependencies
```

## Getting Started

```bash
npm install
npm start
```

## Available Scripts

- `npm start` - Start the development server at http://localhost:3000
- `npm run build` - Build for production
- `npm test` - Run tests
- `npm run lint` - Lint source files
""")

    # --- .gitignore ---
    write_file(f'{PROJECT_DIR}/.gitignore', """\
# Dependencies
node_modules/
/.pnp
.pnp.js

# Production build
/build

# Testing
/coverage

# Environment files
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Editor directories and files
.vscode/settings.json
.idea/
*.swp
*.swo
*~
""")

    # --- Enable breadcrumbs in VSCode settings ---
    vscode_user_dir = f'{WORKDIR}/.config/Code/User'
    settings_path = f'{vscode_user_dir}/settings.json'
    os.makedirs(vscode_user_dir, exist_ok=True)

    # Load existing settings if present
    try:
        with open(settings_path, 'r') as f:
            import re
            content = f.read()
            # Strip JS-style comments (JSONC)
            content_no_comments = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            settings = json.loads(content_no_comments)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    # Ensure breadcrumbs are visible and enabled
    settings['breadcrumbs.enabled'] = True
    settings['breadcrumbs.filePath'] = 'on'
    settings['breadcrumbs.symbolPath'] = 'on'

    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'Project structure created at: {PROJECT_DIR}')
    print(f'Target file: {TARGET_FILE}')
    print(f'VSCode settings updated: breadcrumbs enabled')

    # GUI-ready startup: open VSCode with the project folder
    # Open the workspace folder, then open the specific target file
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    # Open the specific target file so it's active with breadcrumbs visible
    launch_gui(f'code "{TARGET_FILE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with project folder and dateFormatter.js active (DISPLAY=:0)')


create_initial()

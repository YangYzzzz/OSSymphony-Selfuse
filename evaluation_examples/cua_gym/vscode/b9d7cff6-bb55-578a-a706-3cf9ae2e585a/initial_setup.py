"""
Initial Setup: Create a VSCode workspace with helpers.js and files that import it.
Task ID: vscode_rrt_047
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_047'
PROJECT_DIR = f'{WORKDIR}/projects'


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
    # Create directory structure
    os.makedirs(f'{PROJECT_DIR}/lib', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)

    # --- lib/helpers.js ---
    with open(f'{PROJECT_DIR}/lib/helpers.js', 'w') as f:
        f.write("""/**
 * String utility functions for text processing.
 * Used across the application for formatting and validation.
 */

/**
 * Capitalize the first letter of each word in a string.
 * @param {string} str - The input string.
 * @returns {string} The title-cased string.
 */
function titleCase(str) {
    return str
        .toLowerCase()
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}

/**
 * Truncate a string to a maximum length, appending an ellipsis if needed.
 * @param {string} str - The input string.
 * @param {number} maxLen - Maximum allowed length.
 * @returns {string} The truncated string.
 */
function truncate(str, maxLen = 50) {
    if (str.length <= maxLen) return str;
    return str.slice(0, maxLen - 3) + '...';
}

/**
 * Remove all non-alphanumeric characters from a string.
 * @param {string} str - The input string.
 * @returns {string} The sanitized string.
 */
function sanitize(str) {
    return str.replace(/[^a-zA-Z0-9]/g, '');
}

/**
 * Check if a string is a valid email address.
 * @param {string} email - The email string to validate.
 * @returns {boolean} True if valid email format.
 */
function isValidEmail(email) {
    const re = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
    return re.test(email);
}

/**
 * Convert a camelCase string to kebab-case.
 * @param {string} str - The camelCase input.
 * @returns {string} The kebab-case output.
 */
function camelToKebab(str) {
    return str.replace(/([a-z])([A-Z])/g, '$1-$2').toLowerCase();
}

module.exports = {
    titleCase,
    truncate,
    sanitize,
    isValidEmail,
    camelToKebab,
};
""")

    # --- src/app.js ---
    with open(f'{PROJECT_DIR}/src/app.js', 'w') as f:
        f.write("""const express = require('express');
const { titleCase, truncate, isValidEmail } = require('../lib/helpers');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get('/api/users/:id', (req, res) => {
    const userName = titleCase(req.params.id.replace(/-/g, ' '));
    res.json({
        name: userName,
        displayName: truncate(userName, 20),
    });
});

app.post('/api/contact', (req, res) => {
    const { email, message } = req.body;
    if (!isValidEmail(email)) {
        return res.status(400).json({ error: 'Invalid email address' });
    }
    const safeMessage = truncate(message, 500);
    res.json({ status: 'received', preview: safeMessage });
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});

module.exports = app;
""")

    # --- src/formatter.js ---
    with open(f'{PROJECT_DIR}/src/formatter.js', 'w') as f:
        f.write("""const { titleCase, camelToKebab, sanitize } = require('../lib/helpers');

/**
 * Format a user profile object for display.
 * @param {Object} profile - Raw profile data.
 * @returns {Object} Formatted profile.
 */
function formatProfile(profile) {
    return {
        displayName: titleCase(profile.name || ''),
        slug: camelToKebab(sanitize(profile.name || '')),
        bio: profile.bio ? profile.bio.trim() : '',
        joinedAt: new Date(profile.createdAt).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
        }),
    };
}

/**
 * Format a list of tags for URL-safe usage.
 * @param {string[]} tags - Array of tag strings.
 * @returns {string[]} Sanitized and formatted tags.
 */
function formatTags(tags) {
    return tags.map(tag => camelToKebab(sanitize(tag)));
}

/**
 * Generate a page title from a section name.
 * @param {string} section - The section identifier.
 * @returns {string} Human-readable page title.
 */
function pageTitle(section) {
    return titleCase(section.replace(/[-_]/g, ' '));
}

module.exports = {
    formatProfile,
    formatTags,
    pageTitle,
};
""")

    # --- tests/helpers.test.js ---
    with open(f'{PROJECT_DIR}/tests/helpers.test.js', 'w') as f:
        f.write("""const {
    titleCase,
    truncate,
    sanitize,
    isValidEmail,
    camelToKebab,
} = require('../lib/helpers');

describe('String Utility Functions', () => {
    describe('titleCase', () => {
        test('capitalizes first letter of each word', () => {
            expect(titleCase('hello world')).toBe('Hello World');
        });
        test('handles single word', () => {
            expect(titleCase('javascript')).toBe('Javascript');
        });
        test('handles empty string', () => {
            expect(titleCase('')).toBe('');
        });
    });

    describe('truncate', () => {
        test('truncates long strings with ellipsis', () => {
            const long = 'a'.repeat(60);
            expect(truncate(long, 50).length).toBe(50);
            expect(truncate(long, 50).endsWith('...')).toBe(true);
        });
        test('returns short strings unchanged', () => {
            expect(truncate('short', 50)).toBe('short');
        });
    });

    describe('sanitize', () => {
        test('removes special characters', () => {
            expect(sanitize('hello@world!')).toBe('helloworld');
        });
        test('keeps alphanumeric characters', () => {
            expect(sanitize('abc123')).toBe('abc123');
        });
    });

    describe('isValidEmail', () => {
        test('accepts valid emails', () => {
            expect(isValidEmail('user@example.com')).toBe(true);
        });
        test('rejects invalid emails', () => {
            expect(isValidEmail('notanemail')).toBe(false);
        });
    });

    describe('camelToKebab', () => {
        test('converts camelCase to kebab-case', () => {
            expect(camelToKebab('myVariableName')).toBe('my-variable-name');
        });
        test('handles single word', () => {
            expect(camelToKebab('hello')).toBe('hello');
        });
    });
});
""")

    # --- package.json ---
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        f.write("""{
    "name": "text-processing-api",
    "version": "1.2.0",
    "description": "REST API with string processing utilities",
    "main": "src/app.js",
    "scripts": {
        "start": "node src/app.js",
        "test": "jest"
    },
    "dependencies": {
        "express": "^4.18.2"
    },
    "devDependencies": {
        "jest": "^29.7.0"
    }
}
""")

    print(f'Initial workspace created: {PROJECT_DIR}')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

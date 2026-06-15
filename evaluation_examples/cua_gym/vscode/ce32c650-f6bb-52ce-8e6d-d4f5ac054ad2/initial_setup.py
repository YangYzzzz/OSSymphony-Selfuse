"""
Initial Setup: Create Chrome extension project with manifest and dist files.
Task ID: vscode_td_072
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_072'
PROJECT_DIR = f'{WORKDIR}/projects/chrome-extension'


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
    os.makedirs(f'{PROJECT_DIR}/dist', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/icons', exist_ok=True)

    # manifest.json - Chrome Extension Manifest V3
    manifest = {
        "manifest_version": 3,
        "name": "Tab Organizer Pro",
        "version": "1.2.0",
        "description": "Automatically organize browser tabs by domain and category",
        "permissions": ["tabs", "storage", "activeTab"],
        "action": {
            "default_popup": "popup.html",
            "default_icon": {
                "16": "icons/icon16.png",
                "48": "icons/icon48.png",
                "128": "icons/icon128.png"
            }
        },
        "background": {
            "service_worker": "background.js"
        },
        "content_scripts": [
            {
                "matches": ["<all_urls>"],
                "js": ["content.js"],
                "css": ["content.css"]
            }
        ],
        "icons": {
            "16": "icons/icon16.png",
            "48": "icons/icon48.png",
            "128": "icons/icon128.png"
        }
    }
    with open(f'{PROJECT_DIR}/manifest.json', 'w') as f:
        json.dump(manifest, f, indent=2)

    # package.json
    package = {
        "name": "tab-organizer-pro",
        "version": "1.2.0",
        "description": "Chrome extension to organize browser tabs",
        "scripts": {
            "build": "webpack --config webpack.config.js",
            "watch": "webpack --watch --config webpack.config.js",
            "lint": "eslint src/",
            "test": "jest"
        },
        "devDependencies": {
            "webpack": "^5.89.0",
            "webpack-cli": "^5.1.4",
            "eslint": "^8.56.0",
            "jest": "^29.7.0",
            "copy-webpack-plugin": "^12.0.2"
        },
        "dependencies": {
            "webextension-polyfill": "^0.10.0"
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package, f, indent=2)

    # dist/ - Built extension files
    # dist/background.js
    with open(f'{PROJECT_DIR}/dist/background.js', 'w') as f:
        f.write("""// Tab Organizer Pro - Background Service Worker
chrome.runtime.onInstalled.addListener(() => {
  console.log('Tab Organizer Pro installed');
  chrome.storage.local.set({ categories: {}, settings: { autoSort: true } });
});

chrome.tabs.onCreated.addListener(async (tab) => {
  const { settings } = await chrome.storage.local.get('settings');
  if (settings.autoSort) {
    await organizeTab(tab);
  }
});

async function organizeTab(tab) {
  if (!tab.url) return;
  try {
    const url = new URL(tab.url);
    const domain = url.hostname;
    const { categories } = await chrome.storage.local.get('categories');
    const category = getCategoryForDomain(domain, categories);
    if (category) {
      const group = await findOrCreateGroup(category);
      await chrome.tabs.group({ tabIds: [tab.id], groupId: group.id });
    }
  } catch (err) {
    console.error('Failed to organize tab:', err);
  }
}

function getCategoryForDomain(domain, categories) {
  for (const [cat, domains] of Object.entries(categories)) {
    if (domains.includes(domain)) return cat;
  }
  return null;
}

async function findOrCreateGroup(name) {
  const groups = await chrome.tabGroups.query({ title: name });
  if (groups.length > 0) return groups[0];
  const tab = await chrome.tabs.create({ active: false });
  const groupId = await chrome.tabs.group({ tabIds: [tab.id] });
  await chrome.tabGroups.update(groupId, { title: name });
  return { id: groupId };
}
""")

    # dist/content.js
    with open(f'{PROJECT_DIR}/dist/content.js', 'w') as f:
        f.write("""// Tab Organizer Pro - Content Script
(function() {
  'use strict';

  const observer = new MutationObserver((mutations) => {
    for (const mutation of mutations) {
      if (mutation.type === 'childList') {
        trackPageChanges();
      }
    }
  });

  function trackPageChanges() {
    const title = document.title;
    const url = window.location.href;
    chrome.runtime.sendMessage({
      type: 'PAGE_UPDATED',
      data: { title, url, timestamp: Date.now() }
    });
  }

  observer.observe(document.body, { childList: true, subtree: true });
  console.log('Tab Organizer Pro content script loaded');
})();
""")

    # dist/content.css
    with open(f'{PROJECT_DIR}/dist/content.css', 'w') as f:
        f.write("""/* Tab Organizer Pro - Content Styles */
.tab-organizer-overlay {
  position: fixed;
  top: 10px;
  right: 10px;
  z-index: 999999;
  background: rgba(30, 30, 30, 0.95);
  color: #e0e0e0;
  padding: 12px 16px;
  border-radius: 8px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  font-size: 13px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  transition: opacity 0.3s ease;
}
""")

    # dist/popup.html
    with open(f'{PROJECT_DIR}/dist/popup.html', 'w') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Tab Organizer Pro</title>
  <link rel="stylesheet" href="popup.css">
</head>
<body>
  <div class="container">
    <h1>Tab Organizer Pro</h1>
    <div class="stats">
      <span id="tab-count">0 tabs</span>
      <span id="group-count">0 groups</span>
    </div>
    <button id="sort-btn" class="primary-btn">Sort All Tabs</button>
    <button id="settings-btn" class="secondary-btn">Settings</button>
  </div>
  <script src="popup.js"></script>
</body>
</html>
""")

    # dist/popup.js
    with open(f'{PROJECT_DIR}/dist/popup.js', 'w') as f:
        f.write("""// Tab Organizer Pro - Popup Script
document.addEventListener('DOMContentLoaded', async () => {
  const tabs = await chrome.tabs.query({});
  const groups = await chrome.tabGroups.query({});

  document.getElementById('tab-count').textContent = `${tabs.length} tabs`;
  document.getElementById('group-count').textContent = `${groups.length} groups`;

  document.getElementById('sort-btn').addEventListener('click', async () => {
    chrome.runtime.sendMessage({ type: 'SORT_ALL' });
    window.close();
  });

  document.getElementById('settings-btn').addEventListener('click', () => {
    chrome.runtime.openOptionsPage();
  });
});
""")

    # dist/popup.css
    with open(f'{PROJECT_DIR}/dist/popup.css', 'w') as f:
        f.write("""body {
  width: 280px;
  margin: 0;
  padding: 16px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: #1e1e1e;
  color: #e0e0e0;
}
.container { text-align: center; }
h1 { font-size: 16px; margin-bottom: 12px; color: #4fc3f7; }
.stats { display: flex; justify-content: space-around; margin-bottom: 16px; font-size: 13px; color: #aaa; }
.primary-btn, .secondary-btn {
  display: block; width: 100%; padding: 10px; margin-bottom: 8px;
  border: none; border-radius: 6px; cursor: pointer; font-size: 14px;
}
.primary-btn { background: #4fc3f7; color: #1e1e1e; font-weight: 600; }
.secondary-btn { background: #333; color: #e0e0e0; }
""")

    # src/ - Source files (pre-build)
    with open(f'{PROJECT_DIR}/src/background.ts', 'w') as f:
        f.write("""// Tab Organizer Pro - Background Service Worker (TypeScript Source)
import { TabOrganizer } from './organizer';
import { StorageManager } from './storage';

const organizer = new TabOrganizer();
const storage = new StorageManager();

chrome.runtime.onInstalled.addListener(async () => {
  console.log('Tab Organizer Pro installed');
  await storage.initDefaults();
});

chrome.tabs.onCreated.addListener(async (tab: chrome.tabs.Tab) => {
  const settings = await storage.getSettings();
  if (settings.autoSort) {
    await organizer.organizeTab(tab);
  }
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'SORT_ALL') {
    organizer.sortAllTabs().then(() => sendResponse({ success: true }));
    return true;
  }
});
""")

    with open(f'{PROJECT_DIR}/src/organizer.ts', 'w') as f:
        f.write("""// Tab organization logic
export class TabOrganizer {
  async organizeTab(tab: chrome.tabs.Tab): Promise<void> {
    if (!tab.url) return;
    try {
      const url = new URL(tab.url);
      const category = this.categorize(url.hostname);
      if (category) {
        await this.addToGroup(tab.id!, category);
      }
    } catch (err) {
      console.error('Organize failed:', err);
    }
  }

  async sortAllTabs(): Promise<void> {
    const tabs = await chrome.tabs.query({ currentWindow: true });
    for (const tab of tabs) {
      await this.organizeTab(tab);
    }
  }

  private categorize(hostname: string): string | null {
    const categories: Record<string, string[]> = {
      'Development': ['github.com', 'stackoverflow.com', 'developer.mozilla.org'],
      'Social': ['twitter.com', 'reddit.com', 'linkedin.com'],
      'Email': ['mail.google.com', 'outlook.live.com'],
      'Docs': ['docs.google.com', 'notion.so', 'confluence.atlassian.net'],
    };
    for (const [cat, domains] of Object.entries(categories)) {
      if (domains.some(d => hostname.includes(d))) return cat;
    }
    return null;
  }

  private async addToGroup(tabId: number, groupName: string): Promise<void> {
    const groups = await chrome.tabGroups.query({ title: groupName });
    if (groups.length > 0) {
      await chrome.tabs.group({ tabIds: [tabId], groupId: groups[0].id });
    } else {
      const groupId = await chrome.tabs.group({ tabIds: [tabId] });
      await chrome.tabGroups.update(groupId, { title: groupName });
    }
  }
}
""")

    with open(f'{PROJECT_DIR}/src/storage.ts', 'w') as f:
        f.write("""// Storage management
export interface Settings {
  autoSort: boolean;
  showNotifications: boolean;
  groupColors: Record<string, string>;
}

export class StorageManager {
  private readonly DEFAULTS: Settings = {
    autoSort: true,
    showNotifications: false,
    groupColors: {
      Development: 'blue',
      Social: 'purple',
      Email: 'red',
      Docs: 'green',
    },
  };

  async initDefaults(): Promise<void> {
    const existing = await chrome.storage.local.get('settings');
    if (!existing.settings) {
      await chrome.storage.local.set({
        settings: this.DEFAULTS,
        categories: {},
      });
    }
  }

  async getSettings(): Promise<Settings> {
    const { settings } = await chrome.storage.local.get('settings');
    return settings || this.DEFAULTS;
  }

  async updateSettings(updates: Partial<Settings>): Promise<void> {
    const current = await this.getSettings();
    await chrome.storage.local.set({
      settings: { ...current, ...updates },
    });
  }
}
""")

    # webpack.config.js
    with open(f'{PROJECT_DIR}/webpack.config.js', 'w') as f:
        f.write("""const path = require('path');
const CopyPlugin = require('copy-webpack-plugin');

module.exports = {
  entry: {
    background: './src/background.ts',
    content: './src/content.ts',
    popup: './src/popup.ts',
  },
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].js',
  },
  resolve: {
    extensions: ['.ts', '.js'],
  },
  module: {
    rules: [
      {
        test: /\\.ts$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
    ],
  },
  plugins: [
    new CopyPlugin({
      patterns: [
        { from: 'manifest.json', to: '.' },
        { from: 'src/popup.html', to: '.' },
        { from: 'src/popup.css', to: '.' },
        { from: 'icons', to: 'icons' },
      ],
    }),
  ],
};
""")

    # tsconfig.json
    with open(f'{PROJECT_DIR}/tsconfig.json', 'w') as f:
        json.dump({
            "compilerOptions": {
                "target": "ES2020",
                "module": "ESNext",
                "moduleResolution": "node",
                "strict": True,
                "esModuleInterop": True,
                "outDir": "./dist",
                "rootDir": "./src",
                "types": ["chrome"]
            },
            "include": ["src/**/*.ts"],
            "exclude": ["node_modules", "dist"]
        }, f, indent=2)

    # .gitignore
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write("""node_modules/
dist/
*.zip
.DS_Store
""")

    # README.md
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write("""# Tab Organizer Pro

A Chrome extension that automatically organizes your browser tabs by domain and category.

## Features
- Auto-sort tabs into groups by domain category
- Customizable category definitions
- One-click manual sort
- Persistent settings via Chrome storage API

## Development

```bash
npm install
npm run build
npm run watch  # for development
```

## Loading in Chrome
1. Open chrome://extensions
2. Enable Developer Mode
3. Click "Load unpacked" and select the `dist/` directory
""")

    # Ensure NO .vscode/launch.json exists (this is what the task asks to create)
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    launch_json = f'{vscode_dir}/launch.json'
    if os.path.exists(launch_json):
        os.remove(launch_json)

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'Files: manifest.json, package.json, dist/*, src/*, webpack.config.js, tsconfig.json')
    print(f'No .vscode/launch.json exists (task requires creating it)')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

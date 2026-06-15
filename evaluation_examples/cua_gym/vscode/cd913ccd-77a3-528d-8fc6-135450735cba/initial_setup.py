"""
Initial Setup: React Native mobile development workflow in VSCode
Task ID: vscode_wf_090
Domain: vscode

Creates ~/project as a React Native/Expo project scaffold.
Node.js is installed. No React Native extension, no debug configs,
no .vscode folder, no .eslintrc.json.
VSCode is opened with ~/project.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_090'
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


def install_node():
    """Install Node.js and npm if not present."""
    node_check = subprocess.run(["which", "node"], capture_output=True)
    npm_check = subprocess.run(["which", "npm"], capture_output=True)
    if node_check.returncode == 0 and npm_check.returncode == 0:
        print("Node.js and npm already installed")
        return
    print("Installing Node.js and npm...")
    subprocess.run(
        ["bash", "-c",
         "echo 'password' | sudo -S apt-get update -qq && "
         "echo 'password' | sudo -S DEBIAN_FRONTEND=noninteractive apt-get install -y nodejs npm"],
        check=True,
        timeout=180,
    )
    # Verify
    r = subprocess.run(["node", "--version"], capture_output=True, text=True)
    print(f"Node.js version: {r.stdout.strip()}")
    r = subprocess.run(["npm", "--version"], capture_output=True, text=True)
    print(f"npm version: {r.stdout.strip()}")
    print("Node.js installed successfully")


def create_project():
    """Create a React Native/Expo project structure."""
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # package.json — Expo-based React Native project
    package_json = {
        "name": "mobile-expense-tracker",
        "version": "1.0.0",
        "main": "node_modules/expo/AppEntry.js",
        "scripts": {
            "start": "expo start",
            "android": "expo start --android",
            "ios": "expo start --ios",
            "web": "expo start --web"
        },
        "dependencies": {
            "expo": "~49.0.15",
            "expo-status-bar": "~1.6.0",
            "react": "18.2.0",
            "react-native": "0.72.6",
            "@react-navigation/native": "^6.1.9",
            "@react-navigation/stack": "^6.3.20",
            "react-native-screens": "~3.22.0",
            "react-native-safe-area-context": "4.6.3"
        },
        "devDependencies": {
            "@babel/core": "^7.20.0",
            "eslint": "^8.50.0",
            "jest": "^29.7.0",
            "react-test-renderer": "18.2.0"
        },
        "private": True
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # app.json — Expo configuration
    app_json = {
        "expo": {
            "name": "Mobile Expense Tracker",
            "slug": "mobile-expense-tracker",
            "version": "1.0.0",
            "orientation": "portrait",
            "icon": "./assets/icon.png",
            "userInterfaceStyle": "light",
            "splash": {
                "image": "./assets/splash.png",
                "resizeMode": "contain",
                "backgroundColor": "#ffffff"
            },
            "assetBundlePatterns": ["**/*"],
            "ios": {
                "supportsTablet": True,
                "bundleIdentifier": "com.example.expensetracker"
            },
            "android": {
                "adaptiveIcon": {
                    "foregroundImage": "./assets/adaptive-icon.png",
                    "backgroundColor": "#ffffff"
                },
                "package": "com.example.expensetracker"
            },
            "web": {
                "favicon": "./assets/favicon.png"
            }
        }
    }
    with open(os.path.join(PROJECT_DIR, 'app.json'), 'w') as f:
        json.dump(app_json, f, indent=2)

    # babel.config.js
    with open(os.path.join(PROJECT_DIR, 'babel.config.js'), 'w') as f:
        f.write("""module.exports = function(api) {
  api.cache(true);
  return {
    presets: ['babel-preset-expo'],
  };
};
""")

    # App.js — main component
    with open(os.path.join(PROJECT_DIR, 'App.js'), 'w') as f:
        f.write("""import React, { useState } from 'react';
import { StyleSheet, Text, View, FlatList, TextInput, TouchableOpacity } from 'react-native';
import { StatusBar } from 'expo-status-bar';

const CATEGORIES = ['Food', 'Transport', 'Entertainment', 'Bills', 'Shopping', 'Health'];

export default function App() {
  const [expenses, setExpenses] = useState([
    { id: '1', description: 'Grocery shopping', amount: 52.30, category: 'Food', date: '2025-03-15' },
    { id: '2', description: 'Uber ride', amount: 18.50, category: 'Transport', date: '2025-03-14' },
    { id: '3', description: 'Movie tickets', amount: 25.00, category: 'Entertainment', date: '2025-03-13' },
  ]);
  const [description, setDescription] = useState('');
  const [amount, setAmount] = useState('');

  const addExpense = () => {
    if (!description || !amount) return;
    const newExpense = {
      id: Date.now().toString(),
      description,
      amount: parseFloat(amount),
      category: CATEGORIES[0],
      date: new Date().toISOString().split('T')[0],
    };
    setExpenses([newExpense, ...expenses]);
    setDescription('');
    setAmount('');
  };

  const totalExpenses = expenses.reduce((sum, e) => sum + e.amount, 0);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Expense Tracker</Text>
      <Text style={styles.total}>Total: ${totalExpenses.toFixed(2)}</Text>
      <View style={styles.inputRow}>
        <TextInput
          style={styles.input}
          placeholder="Description"
          value={description}
          onChangeText={setDescription}
        />
        <TextInput
          style={styles.inputSmall}
          placeholder="Amount"
          keyboardType="numeric"
          value={amount}
          onChangeText={setAmount}
        />
        <TouchableOpacity style={styles.addBtn} onPress={addExpense}>
          <Text style={styles.addBtnText}>+</Text>
        </TouchableOpacity>
      </View>
      <FlatList
        data={expenses}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <View style={styles.expenseItem}>
            <View>
              <Text style={styles.expenseDesc}>{item.description}</Text>
              <Text style={styles.expenseMeta}>{item.category} - {item.date}</Text>
            </View>
            <Text style={styles.expenseAmount}>${item.amount.toFixed(2)}</Text>
          </View>
        )}
      />
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5', paddingTop: 60, paddingHorizontal: 20 },
  title: { fontSize: 28, fontWeight: 'bold', color: '#333', marginBottom: 8 },
  total: { fontSize: 20, color: '#666', marginBottom: 20 },
  inputRow: { flexDirection: 'row', marginBottom: 20 },
  input: { flex: 2, backgroundColor: '#fff', borderRadius: 8, padding: 12, marginRight: 8, fontSize: 16 },
  inputSmall: { flex: 1, backgroundColor: '#fff', borderRadius: 8, padding: 12, marginRight: 8, fontSize: 16 },
  addBtn: { backgroundColor: '#4CAF50', borderRadius: 8, width: 48, justifyContent: 'center', alignItems: 'center' },
  addBtnText: { color: '#fff', fontSize: 24, fontWeight: 'bold' },
  expenseItem: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', backgroundColor: '#fff', padding: 16, borderRadius: 8, marginBottom: 8 },
  expenseDesc: { fontSize: 16, fontWeight: '600', color: '#333' },
  expenseMeta: { fontSize: 13, color: '#999', marginTop: 4 },
  expenseAmount: { fontSize: 18, fontWeight: 'bold', color: '#e53935' },
});
""")

    # Create assets directory with placeholder files
    assets_dir = os.path.join(PROJECT_DIR, 'assets')
    os.makedirs(assets_dir, exist_ok=True)
    # Create minimal placeholder files
    for fname in ['icon.png', 'splash.png', 'adaptive-icon.png', 'favicon.png']:
        fpath = os.path.join(assets_dir, fname)
        if not os.path.exists(fpath):
            # Create a tiny 1x1 PNG placeholder
            import struct, zlib
            def make_minimal_png():
                header = b'\x89PNG\r\n\x1a\n'
                ihdr_data = struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0)
                ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data) & 0xffffffff
                ihdr = struct.pack('>I', 13) + b'IHDR' + ihdr_data + struct.pack('>I', ihdr_crc)
                raw = zlib.compress(b'\x00\x00\x00\x00')
                idat_crc = zlib.crc32(b'IDAT' + raw) & 0xffffffff
                idat = struct.pack('>I', len(raw)) + b'IDAT' + raw + struct.pack('>I', idat_crc)
                iend_crc = zlib.crc32(b'IEND') & 0xffffffff
                iend = struct.pack('>I', 0) + b'IEND' + struct.pack('>I', iend_crc)
                return header + ihdr + idat + iend
            with open(fpath, 'wb') as pf:
                pf.write(make_minimal_png())

    # Create src directory with some components
    src_dir = os.path.join(PROJECT_DIR, 'src')
    screens_dir = os.path.join(src_dir, 'screens')
    components_dir = os.path.join(src_dir, 'components')
    os.makedirs(screens_dir, exist_ok=True)
    os.makedirs(components_dir, exist_ok=True)

    with open(os.path.join(screens_dir, 'HomeScreen.js'), 'w') as f:
        f.write("""import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

export default function HomeScreen({ navigation }) {
  return (
    <View style={styles.container}>
      <Text style={styles.header}>Dashboard</Text>
      <Text style={styles.subtitle}>Welcome to Expense Tracker</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  header: { fontSize: 24, fontWeight: 'bold' },
  subtitle: { fontSize: 16, color: '#888', marginTop: 8 },
});
""")

    with open(os.path.join(components_dir, 'ExpenseCard.js'), 'w') as f:
        f.write("""import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

export default function ExpenseCard({ description, amount, category, date }) {
  return (
    <View style={styles.card}>
      <View style={styles.row}>
        <Text style={styles.description}>{description}</Text>
        <Text style={styles.amount}>${amount.toFixed(2)}</Text>
      </View>
      <Text style={styles.meta}>{category} | {date}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  card: { backgroundColor: '#fff', borderRadius: 12, padding: 16, marginBottom: 12, elevation: 2 },
  row: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  description: { fontSize: 16, fontWeight: '600' },
  amount: { fontSize: 16, fontWeight: 'bold', color: '#e53935' },
  meta: { fontSize: 12, color: '#aaa', marginTop: 6 },
});
""")

    # .gitignore
    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write("""node_modules/
.expo/
dist/
npm-debug.*
*.jks
*.p8
*.p12
*.key
*.mobileprovision
*.orig.*
web-build/
.DS_Store
""")

    print(f"Project created at {PROJECT_DIR}")


def create_initial():
    # Install Node.js
    install_node()

    # Create project structure
    create_project()

    # Ensure no .vscode folder exists (clean initial state)
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)

    # Ensure no .eslintrc.json exists
    eslintrc = os.path.join(PROJECT_DIR, '.eslintrc.json')
    if os.path.exists(eslintrc):
        os.remove(eslintrc)

    # Ensure React Native Tools extension is NOT installed
    subprocess.run(
        ["code", "--uninstall-extension", "msjsdiag.vscode-react-native"],
        capture_output=True,
    )
    print("Ensured React Native Tools extension is not installed")

    # Launch VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with ~/project and DISPLAY=:0')


create_initial()

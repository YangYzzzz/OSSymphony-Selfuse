"""
Initial Setup: Create a webapp project with Node.js backend and React frontend, no launch.json
Task ID: vscode_td_056
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_056'
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
    os.makedirs(f'{PROJECT_DIR}/server', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/client/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/client/public', exist_ok=True)

    # Ensure NO .vscode/launch.json exists
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    launch_json_path = f'{vscode_dir}/launch.json'
    if os.path.exists(launch_json_path):
        os.remove(launch_json_path)

    # Create package.json for the root project
    root_package = {
        "name": "webapp",
        "version": "1.0.0",
        "description": "Full-stack web application with Node.js backend and React frontend",
        "private": True,
        "scripts": {
            "start:server": "node server/index.js",
            "start:client": "cd client && npm start",
            "start": "concurrently \"npm run start:server\" \"npm run start:client\""
        },
        "dependencies": {
            "express": "^4.18.2",
            "cors": "^2.8.5",
            "concurrently": "^8.2.0"
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(root_package, f, indent=2)

    # Create server/index.js - Node.js Express backend
    server_code = '''const express = require('express');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

// In-memory data store
let tasks = [
    { id: 1, title: 'Set up project structure', completed: true, assignee: 'Sarah Chen' },
    { id: 2, title: 'Implement REST API endpoints', completed: false, assignee: 'Marcus Johnson' },
    { id: 3, title: 'Design database schema', completed: true, assignee: 'Emily Rodriguez' },
    { id: 4, title: 'Write unit tests for API', completed: false, assignee: 'David Park' },
    { id: 5, title: 'Configure CI/CD pipeline', completed: false, assignee: 'Sarah Chen' },
];

// GET /api/tasks - Retrieve all tasks
app.get('/api/tasks', (req, res) => {
    res.json(tasks);
});

// GET /api/tasks/:id - Retrieve a single task
app.get('/api/tasks/:id', (req, res) => {
    const task = tasks.find(t => t.id === parseInt(req.params.id));
    if (!task) return res.status(404).json({ error: 'Task not found' });
    res.json(task);
});

// POST /api/tasks - Create a new task
app.post('/api/tasks', (req, res) => {
    const { title, assignee } = req.body;
    if (!title) return res.status(400).json({ error: 'Title is required' });

    const newTask = {
        id: tasks.length > 0 ? Math.max(...tasks.map(t => t.id)) + 1 : 1,
        title,
        completed: false,
        assignee: assignee || 'Unassigned',
    };
    tasks.push(newTask);
    res.status(201).json(newTask);
});

// PUT /api/tasks/:id - Update a task
app.put('/api/tasks/:id', (req, res) => {
    const task = tasks.find(t => t.id === parseInt(req.params.id));
    if (!task) return res.status(404).json({ error: 'Task not found' });

    const { title, completed, assignee } = req.body;
    if (title !== undefined) task.title = title;
    if (completed !== undefined) task.completed = completed;
    if (assignee !== undefined) task.assignee = assignee;
    res.json(task);
});

// DELETE /api/tasks/:id - Delete a task
app.delete('/api/tasks/:id', (req, res) => {
    const index = tasks.findIndex(t => t.id === parseInt(req.params.id));
    if (index === -1) return res.status(404).json({ error: 'Task not found' });

    tasks.splice(index, 1);
    res.status(204).send();
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
'''
    with open(f'{PROJECT_DIR}/server/index.js', 'w') as f:
        f.write(server_code)

    # Create client/package.json
    client_package = {
        "name": "webapp-client",
        "version": "0.1.0",
        "private": True,
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-scripts": "5.0.1",
            "axios": "^1.6.0"
        },
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test"
        },
        "proxy": "http://localhost:5000",
        "browserslist": {
            "production": [">0.2%", "not dead", "not op_mini all"],
            "development": ["last 1 chrome version", "last 1 firefox version"]
        }
    }
    with open(f'{PROJECT_DIR}/client/package.json', 'w') as f:
        json.dump(client_package, f, indent=2)

    # Create client/src/App.js - React frontend
    app_js = '''import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
    const [tasks, setTasks] = useState([]);
    const [newTaskTitle, setNewTaskTitle] = useState('');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchTasks();
    }, []);

    const fetchTasks = async () => {
        try {
            const response = await axios.get('/api/tasks');
            setTasks(response.data);
        } catch (error) {
            console.error('Error fetching tasks:', error);
        } finally {
            setLoading(false);
        }
    };

    const addTask = async (e) => {
        e.preventDefault();
        if (!newTaskTitle.trim()) return;

        try {
            const response = await axios.post('/api/tasks', {
                title: newTaskTitle,
            });
            setTasks([...tasks, response.data]);
            setNewTaskTitle('');
        } catch (error) {
            console.error('Error adding task:', error);
        }
    };

    const toggleTask = async (id) => {
        const task = tasks.find(t => t.id === id);
        try {
            await axios.put(`/api/tasks/${id}`, {
                completed: !task.completed,
            });
            setTasks(tasks.map(t =>
                t.id === id ? { ...t, completed: !t.completed } : t
            ));
        } catch (error) {
            console.error('Error updating task:', error);
        }
    };

    const deleteTask = async (id) => {
        try {
            await axios.delete(`/api/tasks/${id}`);
            setTasks(tasks.filter(t => t.id !== id));
        } catch (error) {
            console.error('Error deleting task:', error);
        }
    };

    if (loading) return <div className="loading">Loading tasks...</div>;

    return (
        <div className="App">
            <h1>Task Manager</h1>
            <form onSubmit={addTask}>
                <input
                    type="text"
                    value={newTaskTitle}
                    onChange={(e) => setNewTaskTitle(e.target.value)}
                    placeholder="Enter a new task..."
                />
                <button type="submit">Add Task</button>
            </form>
            <ul className="task-list">
                {tasks.map(task => (
                    <li key={task.id} className={task.completed ? 'completed' : ''}>
                        <input
                            type="checkbox"
                            checked={task.completed}
                            onChange={() => toggleTask(task.id)}
                        />
                        <span className="task-title">{task.title}</span>
                        <span className="task-assignee">({task.assignee})</span>
                        <button onClick={() => deleteTask(task.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default App;
'''
    with open(f'{PROJECT_DIR}/client/src/App.js', 'w') as f:
        f.write(app_js)

    # Create client/src/index.js
    index_js = '''import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);
'''
    with open(f'{PROJECT_DIR}/client/src/index.js', 'w') as f:
        f.write(index_js)

    # Create client/public/index.html
    index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Task Manager - WebApp</title>
</head>
<body>
    <div id="root"></div>
</body>
</html>
'''
    with open(f'{PROJECT_DIR}/client/public/index.html', 'w') as f:
        f.write(index_html)

    # Create a README.md for the project
    readme = '''# WebApp - Task Manager

A full-stack task management application built with Node.js and React.

## Project Structure

```
webapp/
  server/
    index.js          # Express API server (port 5000)
  client/
    src/
      App.js          # React frontend application
      index.js        # React entry point
    public/
      index.html      # HTML template
    package.json      # Client dependencies
  package.json        # Root project config
```

## Getting Started

### Backend
```bash
npm install
npm run start:server
```

### Frontend
```bash
cd client
npm install
npm start
```

The frontend runs on port 3000 and proxies API requests to port 5000.
'''
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme)

    print(f'Project created at: {PROJECT_DIR}')
    print(f'  server/index.js - Express backend')
    print(f'  client/src/App.js - React frontend')
    print(f'  No .vscode/launch.json (task requires agent to create it)')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()

"""
Initial Setup: GraphQL development workflow in ~/project
Task ID: vscode_wf_070
Domain: vscode

Creates a Node.js project with graphql/apollo-server/codegen deps in package.json.
No schema, no config, no resolvers - those are the task for the agent to create.
Opens VSCode with ~/project.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_070'
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
    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create package.json with graphql dependencies
    package_json = {
        "name": "graphql-project",
        "version": "1.0.0",
        "description": "GraphQL API server for user and post management",
        "main": "src/index.js",
        "scripts": {
            "start": "node src/index.js",
            "dev": "nodemon src/index.js"
        },
        "dependencies": {
            "graphql": "^16.8.1",
            "apollo-server": "^3.13.0",
            "@apollo/server": "^4.10.0",
            "graphql-tag": "^2.12.6"
        },
        "devDependencies": {
            "@graphql-codegen/cli": "^5.0.0",
            "@graphql-codegen/typescript": "^4.0.1",
            "@graphql-codegen/typescript-resolvers": "^4.0.1",
            "nodemon": "^3.0.2",
            "typescript": "^5.3.3"
        },
        "keywords": ["graphql", "apollo", "api"],
        "author": "Dev Team",
        "license": "MIT"
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # Create src directory with a basic index.js entry point
    src_dir = os.path.join(PROJECT_DIR, 'src')
    os.makedirs(src_dir, exist_ok=True)

    index_js = """const { ApolloServer } = require('apollo-server');

// TODO: Import schema and resolvers
// const typeDefs = require('./schema');
// const resolvers = require('./resolvers');

const server = new ApolloServer({
  // typeDefs,
  // resolvers,
});

server.listen({ port: 4000 }).then(({ url }) => {
  console.log(`Server ready at ${url}`);
});
"""
    with open(os.path.join(src_dir, 'index.js'), 'w') as f:
        f.write(index_js)

    # Create a basic .gitignore
    gitignore = """node_modules/
dist/
.env
*.log
generated/
"""
    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write(gitignore)

    # Create a basic tsconfig.json
    tsconfig = {
        "compilerOptions": {
            "target": "ES2020",
            "module": "commonjs",
            "lib": ["ES2020"],
            "outDir": "./dist",
            "rootDir": "./src",
            "strict": True,
            "esModuleInterop": True,
            "skipLibCheck": True,
            "forceConsistentCasingInFileNames": True,
            "resolveJsonModule": True
        },
        "include": ["src/**/*"],
        "exclude": ["node_modules", "dist"]
    }
    with open(os.path.join(PROJECT_DIR, 'tsconfig.json'), 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # Create a README.md
    readme = """# GraphQL Project

A GraphQL API server for user and post management.

## Getting Started

1. Install dependencies: `npm install`
2. Start the server: `npm start`

## Development

This project uses Apollo Server with GraphQL.
"""
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write(readme)

    # Create .vscode directory (empty settings to start)
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    os.makedirs(vscode_dir, exist_ok=True)

    print(f'Initial project created: {PROJECT_DIR}')

    # Open VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with ~/project with DISPLAY=:0')


create_initial()

"""
Initial Setup: Set up file associations for a VSCode project workspace
Task ID: vscode_code_072
Domain: vs_code

Creates the initial state where a workspace exists but has no file associations
configured yet. The agent must set up the .njk, .graphql, and Dockerfile.* associations.
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_072'
WORKSPACE_DIR = f'{WORKDIR}/{TASK_ID}'
VSCODE_DIR = f'{WORKSPACE_DIR}/.vscode'
SETTINGS_PATH = f'{VSCODE_DIR}/settings.json'


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
    # Create workspace directory structure
    os.makedirs(VSCODE_DIR, exist_ok=True)

    # Create realistic project files to make it look like a real project
    # index.njk - Nunjucks template file
    nunjucks_content = """{%- extends "base.njk" -%}

{%- block title -%}Home | My Project{%- endblock -%}

{%- block content -%}
<main class="container">
  <section class="hero">
    <h1>{{ page.title }}</h1>
    <p>{{ page.description }}</p>
  </section>

  {%- for item in collections.posts | reverse | limit(3) -%}
  <article class="post-card">
    <h2><a href="{{ item.url }}">{{ item.data.title }}</a></h2>
    <time datetime="{{ item.date | dateIso }}">{{ item.date | dateReadable }}</time>
    <p>{{ item.data.excerpt }}</p>
  </article>
  {%- endfor -%}
</main>
{%- endblock -%}
"""
    with open(f'{WORKSPACE_DIR}/index.njk', 'w') as f:
        f.write(nunjucks_content)

    # base.njk layout template
    base_njk_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}My Project{% endblock %}</title>
  <link rel="stylesheet" href="/css/main.css">
</head>
<body>
  <header>
    <nav>
      <a href="/">Home</a>
      <a href="/about">About</a>
      <a href="/blog">Blog</a>
    </nav>
  </header>

  {% block content %}{% endblock %}

  <footer>
    <p>&copy; {{ site.year }} My Project. All rights reserved.</p>
  </footer>
  <script src="/js/main.js"></script>
</body>
</html>
"""
    with open(f'{WORKSPACE_DIR}/base.njk', 'w') as f:
        f.write(base_njk_content)

    # schema.graphql - GraphQL schema file
    graphql_content = """# GraphQL Schema for the API
# Version: 1.0.0

type Query {
  user(id: ID!): User
  users(limit: Int, offset: Int): [User!]!
  post(id: ID!): Post
  posts(authorId: ID, limit: Int): [Post!]!
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User
  deleteUser(id: ID!): Boolean!
  createPost(input: CreatePostInput!): Post!
  publishPost(id: ID!): Post
}

type User {
  id: ID!
  username: String!
  email: String!
  displayName: String
  bio: String
  createdAt: String!
  posts: [Post!]!
}

type Post {
  id: ID!
  title: String!
  content: String!
  excerpt: String
  published: Boolean!
  author: User!
  tags: [String!]
  createdAt: String!
  updatedAt: String!
}

input CreateUserInput {
  username: String!
  email: String!
  displayName: String
  password: String!
}

input UpdateUserInput {
  displayName: String
  bio: String
  email: String
}

input CreatePostInput {
  title: String!
  content: String!
  excerpt: String
  tags: [String!]
  authorId: ID!
}
"""
    with open(f'{WORKSPACE_DIR}/schema.graphql', 'w') as f:
        f.write(graphql_content)

    # queries.gql - GraphQL query file
    gql_content = """# Common GraphQL queries used by the frontend

query GetUser($id: ID!) {
  user(id: $id) {
    id
    username
    email
    displayName
    bio
    posts {
      id
      title
      excerpt
      published
      createdAt
    }
  }
}

query GetPosts($limit: Int = 10, $offset: Int = 0) {
  posts(limit: $limit) {
    id
    title
    excerpt
    published
    author {
      username
      displayName
    }
    tags
    createdAt
  }
}

mutation CreatePost($input: CreatePostInput!) {
  createPost(input: $input) {
    id
    title
    content
    published
    createdAt
  }
}

mutation PublishPost($id: ID!) {
  publishPost(id: $id) {
    id
    title
    published
    updatedAt
  }
}
"""
    with open(f'{WORKSPACE_DIR}/queries.gql', 'w') as f:
        f.write(gql_content)

    # Dockerfile.dev - development Dockerfile
    dockerfile_dev_content = """FROM node:18-alpine AS base

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Development stage
FROM base AS development

RUN npm ci
COPY . .

ENV NODE_ENV=development
ENV PORT=3000

EXPOSE 3000

CMD ["npm", "run", "dev"]
"""
    with open(f'{WORKSPACE_DIR}/Dockerfile.dev', 'w') as f:
        f.write(dockerfile_dev_content)

    # Dockerfile.prod - production Dockerfile
    dockerfile_prod_content = """FROM node:18-alpine AS base

WORKDIR /app

# Install production dependencies
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Build stage
FROM base AS builder
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM base AS production

COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules

ENV NODE_ENV=production
ENV PORT=8080

EXPOSE 8080

USER node

CMD ["node", "dist/server.js"]
"""
    with open(f'{WORKSPACE_DIR}/Dockerfile.prod', 'w') as f:
        f.write(dockerfile_prod_content)

    # package.json for project context
    package_json = {
        "name": "my-project",
        "version": "1.0.0",
        "description": "A web application with GraphQL API",
        "main": "src/index.js",
        "scripts": {
            "dev": "nodemon src/index.js",
            "start": "node src/index.js",
            "build": "webpack --mode production",
            "test": "jest"
        },
        "dependencies": {
            "express": "^4.18.2",
            "graphql": "^16.8.1",
            "express-graphql": "^0.12.0",
            "nunjucks": "^3.2.4"
        },
        "devDependencies": {
            "nodemon": "^3.0.2",
            "jest": "^29.7.0",
            "webpack": "^5.89.0"
        }
    }
    with open(f'{WORKSPACE_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # Create initial .vscode/settings.json with empty settings (no file associations)
    initial_settings = {}
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(initial_settings, f, indent=4)

    print(f'Workspace created: {WORKSPACE_DIR}')
    print(f'Initial settings (empty): {SETTINGS_PATH}')

    # GUI-ready startup: open VSCode with the workspace
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with workspace folder')


create_initial()

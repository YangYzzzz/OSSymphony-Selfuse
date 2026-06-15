"""
Initial Setup: Create a React project with UserCard component used across 6 files
Task ID: vscode_web_031
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_031'
PROJECT_DIR = f'{WORKDIR}/projects/react-app'

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

def create_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)

def create_initial():
    # --- package.json ---
    create_file(f'{PROJECT_DIR}/package.json', '''{
  "name": "react-app",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "typescript": "^5.3.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test"
  }
}
''')

    # --- tsconfig.json ---
    create_file(f'{PROJECT_DIR}/tsconfig.json', '''{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noFallthroughCasesInSwitch": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "baseUrl": "src"
  },
  "include": ["src"]
}
''')

    # --- src/types/index.ts ---
    create_file(f'{PROJECT_DIR}/src/types/index.ts', '''export interface UserProfile {
  id: string;
  name: string;
  email: string;
  avatarUrl: string;
  role: 'admin' | 'editor' | 'viewer';
  joinedAt: Date;
  department: string;
}

export interface TeamMember extends UserProfile {
  teamId: string;
  isLead: boolean;
}

export interface Notification {
  id: string;
  message: string;
  read: boolean;
  createdAt: Date;
}
''')

    # --- src/components/UserCard.tsx (the main component to be renamed) ---
    create_file(f'{PROJECT_DIR}/src/components/UserCard.tsx', '''import React from 'react';
import { UserProfile } from '../types';

interface UserCardProps {
  user: UserProfile;
  onSelect?: (userId: string) => void;
  showDetails?: boolean;
}

const UserCard: React.FC<UserCardProps> = ({ user, onSelect, showDetails = false }) => {
  const handleClick = () => {
    if (onSelect) {
      onSelect(user.id);
    }
  };

  return (
    <div className="user-card" onClick={handleClick}>
      <img src={user.avatarUrl} alt={`${user.name} avatar`} className="user-card__avatar" />
      <div className="user-card__info">
        <h3 className="user-card__name">{user.name}</h3>
        <span className="user-card__role">{user.role}</span>
        {showDetails && (
          <div className="user-card__details">
            <p>{user.email}</p>
            <p>{user.department}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default UserCard;
''')

    # --- src/components/UserCardList.tsx (file 1: imports UserCard) ---
    create_file(f'{PROJECT_DIR}/src/components/UserCardList.tsx', '''import React from 'react';
import UserCard from './UserCard';
import { UserProfile } from '../types';

interface UserCardListProps {
  users: UserProfile[];
  onUserSelect: (userId: string) => void;
}

const UserCardList: React.FC<UserCardListProps> = ({ users, onUserSelect }) => {
  if (users.length === 0) {
    return <p className="empty-state">No team members found.</p>;
  }

  return (
    <div className="user-card-list">
      {users.map((user) => (
        <UserCard key={user.id} user={user} onSelect={onUserSelect} showDetails />
      ))}
    </div>
  );
};

export default UserCardList;
''')

    # --- src/pages/Dashboard.tsx (file 2: imports UserCard) ---
    create_file(f'{PROJECT_DIR}/src/pages/Dashboard.tsx', '''import React, { useState, useEffect } from 'react';
import UserCard from '../components/UserCard';
import { UserProfile } from '../types';

const mockFeaturedUsers: UserProfile[] = [
  {
    id: 'usr-001',
    name: 'Sarah Chen',
    email: 'sarah.chen@company.com',
    avatarUrl: '/avatars/sarah.png',
    role: 'admin',
    joinedAt: new Date('2023-01-15'),
    department: 'Engineering',
  },
  {
    id: 'usr-002',
    name: 'Marcus Johnson',
    email: 'marcus.j@company.com',
    avatarUrl: '/avatars/marcus.png',
    role: 'editor',
    joinedAt: new Date('2023-06-01'),
    department: 'Marketing',
  },
];

const Dashboard: React.FC = () => {
  const [selectedUserId, setSelectedUserId] = useState<string | null>(null);

  return (
    <div className="dashboard">
      <h1>Team Dashboard</h1>
      <section className="dashboard__featured">
        <h2>Featured Team Members</h2>
        <div className="dashboard__cards">
          {mockFeaturedUsers.map((user) => (
            <UserCard
              key={user.id}
              user={user}
              onSelect={setSelectedUserId}
              showDetails
            />
          ))}
        </div>
      </section>
      {selectedUserId && (
        <p className="dashboard__selection">Selected user: {selectedUserId}</p>
      )}
    </div>
  );
};

export default Dashboard;
''')

    # --- src/pages/TeamPage.tsx (file 3: imports UserCard) ---
    create_file(f'{PROJECT_DIR}/src/pages/TeamPage.tsx', '''import React, { useState } from 'react';
import UserCard from '../components/UserCard';
import { UserProfile } from '../types';

const allTeamMembers: UserProfile[] = [
  {
    id: 'usr-010',
    name: 'Amara Okafor',
    email: 'amara.o@company.com',
    avatarUrl: '/avatars/amara.png',
    role: 'editor',
    joinedAt: new Date('2024-02-10'),
    department: 'Design',
  },
  {
    id: 'usr-011',
    name: 'Liam Brennan',
    email: 'liam.b@company.com',
    avatarUrl: '/avatars/liam.png',
    role: 'viewer',
    joinedAt: new Date('2024-05-20'),
    department: 'Sales',
  },
  {
    id: 'usr-012',
    name: 'Priya Sharma',
    email: 'priya.s@company.com',
    avatarUrl: '/avatars/priya.png',
    role: 'admin',
    joinedAt: new Date('2022-11-03'),
    department: 'Engineering',
  },
];

const TeamPage: React.FC = () => {
  const [filter, setFilter] = useState<string>('all');

  const filteredMembers = filter === 'all'
    ? allTeamMembers
    : allTeamMembers.filter((m) => m.department.toLowerCase() === filter);

  return (
    <div className="team-page">
      <h1>Our Team</h1>
      <div className="team-page__filters">
        <button onClick={() => setFilter('all')}>All</button>
        <button onClick={() => setFilter('engineering')}>Engineering</button>
        <button onClick={() => setFilter('design')}>Design</button>
        <button onClick={() => setFilter('sales')}>Sales</button>
      </div>
      <div className="team-page__grid">
        {filteredMembers.map((member) => (
          <UserCard key={member.id} user={member} showDetails />
        ))}
      </div>
    </div>
  );
};

export default TeamPage;
''')

    # --- src/pages/SearchResults.tsx (file 4: imports UserCard) ---
    create_file(f'{PROJECT_DIR}/src/pages/SearchResults.tsx', '''import React from 'react';
import UserCard from '../components/UserCard';
import { UserProfile } from '../types';

interface SearchResultsProps {
  query: string;
  results: UserProfile[];
  onSelect: (userId: string) => void;
}

const SearchResults: React.FC<SearchResultsProps> = ({ query, results, onSelect }) => {
  if (results.length === 0) {
    return (
      <div className="search-results search-results--empty">
        <p>No results found for &quot;{query}&quot;</p>
      </div>
    );
  }

  return (
    <div className="search-results">
      <h2>Search Results for &quot;{query}&quot; ({results.length} found)</h2>
      <div className="search-results__grid">
        {results.map((user) => (
          <UserCard key={user.id} user={user} onSelect={onSelect} />
        ))}
      </div>
    </div>
  );
};

export default SearchResults;
''')

    # --- src/pages/AdminPanel.tsx (file 5: imports UserCard) ---
    create_file(f'{PROJECT_DIR}/src/pages/AdminPanel.tsx', '''import React, { useState } from 'react';
import UserCard from '../components/UserCard';
import { UserProfile } from '../types';

const adminUsers: UserProfile[] = [
  {
    id: 'usr-100',
    name: 'Elena Rodriguez',
    email: 'elena.r@company.com',
    avatarUrl: '/avatars/elena.png',
    role: 'admin',
    joinedAt: new Date('2021-08-15'),
    department: 'Operations',
  },
  {
    id: 'usr-101',
    name: 'David Kim',
    email: 'david.k@company.com',
    avatarUrl: '/avatars/david.png',
    role: 'admin',
    joinedAt: new Date('2022-03-22'),
    department: 'Engineering',
  },
];

const AdminPanel: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'users' | 'settings'>('users');

  return (
    <div className="admin-panel">
      <h1>Admin Panel</h1>
      <nav className="admin-panel__tabs">
        <button
          className={activeTab === 'users' ? 'active' : ''}
          onClick={() => setActiveTab('users')}
        >
          Users
        </button>
        <button
          className={activeTab === 'settings' ? 'active' : ''}
          onClick={() => setActiveTab('settings')}
        >
          Settings
        </button>
      </nav>
      {activeTab === 'users' && (
        <div className="admin-panel__user-list">
          <h2>System Administrators</h2>
          {adminUsers.map((admin) => (
            <UserCard key={admin.id} user={admin} showDetails />
          ))}
        </div>
      )}
      {activeTab === 'settings' && (
        <div className="admin-panel__settings">
          <h2>System Settings</h2>
          <p>Configure application-wide settings here.</p>
        </div>
      )}
    </div>
  );
};

export default AdminPanel;
''')

    # --- src/App.tsx (file 6: imports UserCard) ---
    create_file(f'{PROJECT_DIR}/src/App.tsx', '''import React, { useState } from 'react';
import UserCard from './components/UserCard';
import Dashboard from './pages/Dashboard';
import TeamPage from './pages/TeamPage';
import { UserProfile } from './types';

const currentUser: UserProfile = {
  id: 'usr-self',
  name: 'Alex Rivera',
  email: 'alex.r@company.com',
  avatarUrl: '/avatars/alex.png',
  role: 'admin',
  joinedAt: new Date('2021-01-10'),
  department: 'Engineering',
};

type Page = 'dashboard' | 'team' | 'admin';

const App: React.FC = () => {
  const [currentPage, setCurrentPage] = useState<Page>('dashboard');

  return (
    <div className="app">
      <header className="app__header">
        <h1>TeamHub</h1>
        <nav className="app__nav">
          <button onClick={() => setCurrentPage('dashboard')}>Dashboard</button>
          <button onClick={() => setCurrentPage('team')}>Team</button>
          <button onClick={() => setCurrentPage('admin')}>Admin</button>
        </nav>
        <div className="app__current-user">
          <UserCard user={currentUser} />
        </div>
      </header>
      <main className="app__content">
        {currentPage === 'dashboard' && <Dashboard />}
        {currentPage === 'team' && <TeamPage />}
      </main>
    </div>
  );
};

export default App;
''')

    # --- src/index.tsx ---
    create_file(f'{PROJECT_DIR}/src/index.tsx', '''import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
''')

    print(f'Initial project created at: {PROJECT_DIR}')

    # Open VSCode with the project and the UserCard file
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    launch_gui(f'code "{PROJECT_DIR}/src/components/UserCard.tsx"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()

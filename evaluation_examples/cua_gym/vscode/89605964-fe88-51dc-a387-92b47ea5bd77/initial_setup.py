"""
Initial Setup: VSCode Find and Replace - className="btn" to className="btn btn-primary"
Task ID: vscode_web_014
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_014'
PROJECT_DIR = f'{WORKDIR}/projects/react-app'
SRC_DIR = f'{PROJECT_DIR}/src'


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


def create_project():
    """Create a realistic React project with .jsx files containing className='btn'."""

    # Create directory structure
    dirs = [
        f'{SRC_DIR}/components',
        f'{SRC_DIR}/components/common',
        f'{SRC_DIR}/pages',
        f'{SRC_DIR}/layouts',
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # Create package.json for realism
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        f.write('''{
  "name": "react-app",
  "version": "1.2.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test"
  }
}
''')

    # File 1: src/App.jsx — 2 occurrences
    with open(f'{SRC_DIR}/App.jsx', 'w') as f:
        f.write('''import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './layouts/Header';
import HomePage from './pages/HomePage';
import AboutPage from './pages/AboutPage';

function App() {
  return (
    <BrowserRouter>
      <Header />
      <main className="app-container">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/about" element={<AboutPage />} />
        </Routes>
      </main>
      <footer className="app-footer">
        <button className="btn" onClick={() => window.scrollTo(0, 0)}>
          Back to Top
        </button>
        <button className="btn" onClick={() => window.history.back()}>
          Go Back
        </button>
      </footer>
    </BrowserRouter>
  );
}

export default App;
''')

    # File 2: src/components/LoginForm.jsx — 2 occurrences
    with open(f'{SRC_DIR}/components/LoginForm.jsx', 'w') as f:
        f.write('''import React, { useState } from 'react';

function LoginForm({ onSubmit }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      await onSubmit({ email, password });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form className="login-form" onSubmit={handleSubmit}>
      <h2>Sign In</h2>
      <div className="form-group">
        <label htmlFor="email">Email Address</label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="you@example.com"
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </div>
      <button className="btn" type="submit" disabled={isLoading}>
        {isLoading ? 'Signing in...' : 'Sign In'}
      </button>
      <button className="btn" type="button" onClick={() => window.location.href = '/forgot'}>
        Forgot Password?
      </button>
    </form>
  );
}

export default LoginForm;
''')

    # File 3: src/components/ProductCard.jsx — 2 occurrences
    with open(f'{SRC_DIR}/components/ProductCard.jsx', 'w') as f:
        f.write('''import React from 'react';

function ProductCard({ product, onAddToCart, onViewDetails }) {
  const { name, price, imageUrl, inStock, rating } = product;

  return (
    <div className="product-card">
      <img src={imageUrl} alt={name} className="product-image" />
      <div className="product-info">
        <h3 className="product-title">{name}</h3>
        <div className="product-rating">
          {'★'.repeat(Math.round(rating))}{'☆'.repeat(5 - Math.round(rating))}
        </div>
        <p className="product-price">${price.toFixed(2)}</p>
        {inStock ? (
          <span className="in-stock">In Stock</span>
        ) : (
          <span className="out-of-stock">Out of Stock</span>
        )}
      </div>
      <div className="product-actions">
        <button className="btn" onClick={() => onAddToCart(product)} disabled={!inStock}>
          Add to Cart
        </button>
        <button className="btn" onClick={() => onViewDetails(product.id)}>
          View Details
        </button>
      </div>
    </div>
  );
}

export default ProductCard;
''')

    # File 4: src/components/common/Modal.jsx — 2 occurrences
    with open(f'{SRC_DIR}/components/common/Modal.jsx', 'w') as f:
        f.write('''import React, { useEffect, useRef } from 'react';

function Modal({ isOpen, title, children, onConfirm, onCancel }) {
  const modalRef = useRef(null);

  useEffect(() => {
    if (isOpen) {
      modalRef.current?.focus();
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onCancel}>
      <div
        className="modal-content"
        ref={modalRef}
        tabIndex={-1}
        onClick={(e) => e.stopPropagation()}
      >
        <h2 className="modal-title">{title}</h2>
        <div className="modal-body">{children}</div>
        <div className="modal-footer">
          <button className="btn" onClick={onConfirm}>
            Confirm
          </button>
          <button className="btn" onClick={onCancel}>
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}

export default Modal;
''')

    # File 5: src/pages/HomePage.jsx — 1 occurrence
    with open(f'{SRC_DIR}/pages/HomePage.jsx', 'w') as f:
        f.write('''import React from 'react';
import ProductCard from '../components/ProductCard';

const featuredProducts = [
  { id: 1, name: 'Wireless Headphones', price: 79.99, imageUrl: '/img/headphones.jpg', inStock: true, rating: 4.5 },
  { id: 2, name: 'Mechanical Keyboard', price: 129.99, imageUrl: '/img/keyboard.jpg', inStock: true, rating: 4.8 },
  { id: 3, name: 'USB-C Hub', price: 45.00, imageUrl: '/img/hub.jpg', inStock: false, rating: 4.2 },
];

function HomePage() {
  const handleAddToCart = (product) => {
    console.log(`Added ${product.name} to cart`);
  };

  return (
    <div className="home-page">
      <section className="hero-section">
        <h1>Welcome to TechStore</h1>
        <p>Discover the latest in consumer electronics and accessories.</p>
        <button className="btn" onClick={() => document.getElementById('products').scrollIntoView()}>
          Shop Now
        </button>
      </section>
      <section id="products" className="products-section">
        <h2>Featured Products</h2>
        <div className="product-grid">
          {featuredProducts.map((product) => (
            <ProductCard
              key={product.id}
              product={product}
              onAddToCart={handleAddToCart}
              onViewDetails={(id) => console.log(`View product ${id}`)}
            />
          ))}
        </div>
      </section>
    </div>
  );
}

export default HomePage;
''')

    # File 6: src/pages/AboutPage.jsx — 1 occurrence
    with open(f'{SRC_DIR}/pages/AboutPage.jsx', 'w') as f:
        f.write('''import React from 'react';

function AboutPage() {
  return (
    <div className="about-page">
      <h1>About TechStore</h1>
      <p>
        TechStore was founded in 2019 with a mission to make quality electronics
        accessible to everyone. We carefully curate our selection to ensure every
        product meets our high standards for performance and reliability.
      </p>
      <h2>Our Team</h2>
      <div className="team-grid">
        <div className="team-member">
          <h3>Sarah Chen</h3>
          <p>CEO & Founder</p>
        </div>
        <div className="team-member">
          <h3>Marcus Johnson</h3>
          <p>Head of Engineering</p>
        </div>
        <div className="team-member">
          <h3>Priya Patel</h3>
          <p>Design Lead</p>
        </div>
      </div>
      <button className="btn" onClick={() => window.location.href = '/contact'}>
        Contact Us
      </button>
    </div>
  );
}

export default AboutPage;
''')

    # File 7: src/layouts/Header.jsx — 2 occurrences
    with open(f'{SRC_DIR}/layouts/Header.jsx', 'w') as f:
        f.write('''import React, { useState } from 'react';

function Header() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className="app-header">
      <div className="header-brand">
        <a href="/">TechStore</a>
      </div>
      <nav className={`header-nav ${menuOpen ? 'open' : ''}`}>
        <a href="/">Home</a>
        <a href="/products">Products</a>
        <a href="/about">About</a>
      </nav>
      <div className="header-actions">
        <button className="btn" onClick={() => window.location.href = '/cart'}>
          Cart (0)
        </button>
        <button className="btn" onClick={() => setMenuOpen(!menuOpen)}>
          {menuOpen ? 'Close' : 'Menu'}
        </button>
      </div>
    </header>
  );
}

export default Header;
''')

    print(f'Project created at {PROJECT_DIR}')

    # Count occurrences for verification
    total = 0
    for root, dirs, files in os.walk(SRC_DIR):
        for fname in files:
            if fname.endswith('.jsx'):
                fpath = os.path.join(root, fname)
                with open(fpath, 'r') as f:
                    content = f.read()
                count = content.count('className="btn"')
                if count > 0:
                    total += count
                    print(f'  {fpath}: {count} occurrence(s)')
    print(f'Total className="btn" occurrences: {total}')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_project()

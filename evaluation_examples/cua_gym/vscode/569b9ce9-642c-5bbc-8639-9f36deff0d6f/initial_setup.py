"""
Initial Setup: Cypress component testing configuration for a Vue 3 project
Task ID: vscode_gf3_064
Domain: vscode

Creates a realistic Vue 3 project structure WITHOUT Cypress config or test files.
Opens the project in VSCode.
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_064'
PROJECT_DIR = f'{WORKDIR}/projects/vue-app'


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
    dirs = [
        f'{PROJECT_DIR}/src/components',
        f'{PROJECT_DIR}/src/assets',
        f'{PROJECT_DIR}/src/views',
        f'{PROJECT_DIR}/src/router',
        f'{PROJECT_DIR}/src/store',
        f'{PROJECT_DIR}/public',
        f'{PROJECT_DIR}/tests/unit',
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # --- package.json ---
    package_json = {
        "name": "vue-app",
        "version": "1.2.0",
        "private": True,
        "description": "Artisan Marketplace - Vue 3 E-Commerce Application",
        "scripts": {
            "serve": "vue-cli-service serve",
            "build": "vue-cli-service build",
            "lint": "vue-cli-service lint",
            "test:unit": "vue-cli-service test:unit"
        },
        "dependencies": {
            "vue": "^3.3.4",
            "vue-router": "^4.2.4",
            "pinia": "^2.1.6",
            "axios": "^1.5.0"
        },
        "devDependencies": {
            "@vue/cli-plugin-babel": "~5.0.8",
            "@vue/cli-plugin-typescript": "~5.0.8",
            "@vue/cli-plugin-router": "~5.0.8",
            "@vue/cli-service": "~5.0.8",
            "typescript": "~5.1.6",
            "webpack": "^5.88.0",
            "vue-loader": "^17.2.2",
            "@types/node": "^20.4.5"
        },
        "browserslist": [
            "> 1%",
            "last 2 versions",
            "not dead",
            "not ie 11"
        ]
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # --- tsconfig.json ---
    tsconfig = {
        "compilerOptions": {
            "target": "esnext",
            "module": "esnext",
            "strict": True,
            "jsx": "preserve",
            "moduleResolution": "node",
            "skipLibCheck": True,
            "esModuleInterop": True,
            "allowSyntheticDefaultImports": True,
            "forceConsistentCasingInFileNames": True,
            "useDefineForClassFields": True,
            "sourceMap": True,
            "baseUrl": ".",
            "paths": {
                "@/*": ["src/*"]
            },
            "lib": ["esnext", "dom", "dom.iterable"]
        },
        "include": [
            "src/**/*.ts",
            "src/**/*.tsx",
            "src/**/*.vue",
            "tests/**/*.ts"
        ],
        "exclude": ["node_modules"]
    }
    with open(f'{PROJECT_DIR}/tsconfig.json', 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # --- webpack.config.js ---
    webpack_config = """const { VueLoaderPlugin } = require('vue-loader');
const path = require('path');

module.exports = {
  mode: 'development',
  entry: './src/main.ts',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js',
  },
  resolve: {
    extensions: ['.ts', '.tsx', '.js', '.vue', '.json'],
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  module: {
    rules: [
      {
        test: /\\.vue$/,
        loader: 'vue-loader',
      },
      {
        test: /\\.tsx?$/,
        loader: 'ts-loader',
        options: { appendTsSuffix: [/\\.vue$/] },
        exclude: /node_modules/,
      },
      {
        test: /\\.css$/,
        use: ['style-loader', 'css-loader'],
      },
      {
        test: /\\.(png|jpe?g|gif|svg)$/i,
        type: 'asset/resource',
      },
    ],
  },
  plugins: [new VueLoaderPlugin()],
};
"""
    with open(f'{PROJECT_DIR}/webpack.config.js', 'w') as f:
        f.write(webpack_config)

    # --- src/main.ts ---
    main_ts = """import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);
app.mount('#app');
"""
    with open(f'{PROJECT_DIR}/src/main.ts', 'w') as f:
        f.write(main_ts)

    # --- src/App.vue ---
    app_vue = """<template>
  <div id="app">
    <nav class="main-nav">
      <router-link to="/">Home</router-link>
      <router-link to="/products">Products</router-link>
      <router-link to="/cart">Cart ({{ cartCount }})</router-link>
    </nav>
    <router-view />
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue';
import { useCartStore } from './store/cart';

export default defineComponent({
  name: 'App',
  setup() {
    const cartStore = useCartStore();
    const cartCount = computed(() => cartStore.itemCount);
    return { cartCount };
  },
});
</script>

<style>
#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #2c3e50;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}
.main-nav {
  display: flex;
  gap: 24px;
  padding: 16px 0;
  border-bottom: 2px solid #e0e0e0;
  margin-bottom: 32px;
}
.main-nav a {
  text-decoration: none;
  color: #42b983;
  font-weight: 600;
}
</style>
"""
    with open(f'{PROJECT_DIR}/src/App.vue', 'w') as f:
        f.write(app_vue)

    # --- src/components/ProductCard.vue ---
    product_card = """<template>
  <div class="product-card" :data-product-id="product.id">
    <div class="product-image">
      <img :src="product.imageUrl" :alt="product.name" />
      <span v-if="product.onSale" class="sale-badge">Sale</span>
    </div>
    <div class="product-info">
      <h3 class="product-name">{{ product.name }}</h3>
      <p class="product-description">{{ product.description }}</p>
      <div class="product-pricing">
        <span class="product-price">{{ formattedPrice }}</span>
        <span v-if="product.originalPrice" class="original-price">
          {{ formatCurrency(product.originalPrice) }}
        </span>
      </div>
      <div class="product-rating">
        <span v-for="star in 5" :key="star" class="star" :class="{ filled: star <= product.rating }">
          &#9733;
        </span>
        <span class="review-count">({{ product.reviewCount }} reviews)</span>
      </div>
      <button
        class="add-to-cart-btn"
        :disabled="!product.inStock"
        @click="handleAddToCart"
      >
        {{ product.inStock ? 'Add to Cart' : 'Out of Stock' }}
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, PropType } from 'vue';

export interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  originalPrice?: number;
  imageUrl: string;
  onSale: boolean;
  inStock: boolean;
  rating: number;
  reviewCount: number;
  category: string;
}

export default defineComponent({
  name: 'ProductCard',
  props: {
    product: {
      type: Object as PropType<Product>,
      required: true,
    },
  },
  emits: ['add-to-cart'],
  setup(props, { emit }) {
    const formatCurrency = (amount: number): string => {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
      }).format(amount);
    };

    const formattedPrice = computed(() => formatCurrency(props.product.price));

    const handleAddToCart = () => {
      emit('add-to-cart', {
        productId: props.product.id,
        name: props.product.name,
        price: props.product.price,
        quantity: 1,
      });
    };

    return {
      formattedPrice,
      formatCurrency,
      handleAddToCart,
    };
  },
});
</script>

<style scoped>
.product-card {
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  overflow: hidden;
  transition: box-shadow 0.2s ease;
  background: #ffffff;
  max-width: 320px;
}
.product-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}
.product-image {
  position: relative;
  height: 200px;
  background: #f5f5f5;
}
.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.sale-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  background: #e74c3c;
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
}
.product-info {
  padding: 16px;
}
.product-name {
  margin: 0 0 8px;
  font-size: 1.1rem;
  color: #2c3e50;
}
.product-description {
  color: #7f8c8d;
  font-size: 0.875rem;
  margin: 0 0 12px;
  line-height: 1.4;
}
.product-pricing {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}
.product-price {
  font-size: 1.25rem;
  font-weight: 700;
  color: #27ae60;
}
.original-price {
  text-decoration: line-through;
  color: #bdc3c7;
  font-size: 0.9rem;
}
.product-rating {
  margin-bottom: 12px;
}
.star {
  color: #ddd;
  font-size: 1rem;
}
.star.filled {
  color: #f39c12;
}
.review-count {
  color: #95a5a6;
  font-size: 0.8rem;
  margin-left: 4px;
}
.add-to-cart-btn {
  width: 100%;
  padding: 10px 16px;
  background: #42b983;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
.add-to-cart-btn:hover:not(:disabled) {
  background: #38a373;
}
.add-to-cart-btn:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}
</style>
"""
    with open(f'{PROJECT_DIR}/src/components/ProductCard.vue', 'w') as f:
        f.write(product_card)

    # --- src/components/SearchBar.vue ---
    search_bar = """<template>
  <div class="search-bar">
    <input
      type="text"
      v-model="query"
      placeholder="Search products..."
      @input="$emit('search', query)"
    />
    <select v-model="selectedCategory" @change="$emit('filter-category', selectedCategory)">
      <option value="">All Categories</option>
      <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
    </select>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, PropType } from 'vue';

export default defineComponent({
  name: 'SearchBar',
  props: {
    categories: {
      type: Array as PropType<string[]>,
      default: () => [],
    },
  },
  emits: ['search', 'filter-category'],
  setup() {
    const query = ref('');
    const selectedCategory = ref('');
    return { query, selectedCategory };
  },
});
</script>

<style scoped>
.search-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}
.search-bar input {
  flex: 1;
  padding: 10px 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 0.95rem;
}
.search-bar select {
  padding: 10px 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
}
</style>
"""
    with open(f'{PROJECT_DIR}/src/components/SearchBar.vue', 'w') as f:
        f.write(search_bar)

    # --- src/router/index.ts ---
    router = """import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomeView.vue'),
  },
  {
    path: '/products',
    name: 'Products',
    component: () => import('../views/ProductsView.vue'),
  },
  {
    path: '/products/:id',
    name: 'ProductDetail',
    component: () => import('../views/ProductDetailView.vue'),
  },
  {
    path: '/cart',
    name: 'Cart',
    component: () => import('../views/CartView.vue'),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
"""
    with open(f'{PROJECT_DIR}/src/router/index.ts', 'w') as f:
        f.write(router)

    # --- src/store/cart.ts ---
    store = """import { defineStore } from 'pinia';

interface CartItem {
  productId: number;
  name: string;
  price: number;
  quantity: number;
}

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [] as CartItem[],
  }),
  getters: {
    itemCount: (state) => state.items.reduce((sum, item) => sum + item.quantity, 0),
    totalPrice: (state) =>
      state.items.reduce((sum, item) => sum + item.price * item.quantity, 0),
  },
  actions: {
    addItem(item: CartItem) {
      const existing = this.items.find((i) => i.productId === item.productId);
      if (existing) {
        existing.quantity += item.quantity;
      } else {
        this.items.push({ ...item });
      }
    },
    removeItem(productId: number) {
      this.items = this.items.filter((i) => i.productId !== productId);
    },
    clearCart() {
      this.items = [];
    },
  },
});
"""
    with open(f'{PROJECT_DIR}/src/store/cart.ts', 'w') as f:
        f.write(store)

    # --- src/views/HomeView.vue ---
    home_view = """<template>
  <div class="home">
    <h1>Welcome to Artisan Marketplace</h1>
    <p class="tagline">Discover handcrafted goods from independent makers worldwide.</p>
    <router-link to="/products" class="browse-btn">Browse Products</router-link>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'HomeView',
});
</script>

<style scoped>
.home {
  text-align: center;
  padding: 80px 20px;
}
.home h1 {
  font-size: 2.5rem;
  color: #2c3e50;
}
.tagline {
  color: #7f8c8d;
  font-size: 1.2rem;
  margin: 16px 0 32px;
}
.browse-btn {
  display: inline-block;
  padding: 12px 32px;
  background: #42b983;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
}
</style>
"""
    with open(f'{PROJECT_DIR}/src/views/HomeView.vue', 'w') as f:
        f.write(home_view)

    # --- src/views/ProductsView.vue (stub) ---
    products_view = """<template>
  <div class="products-page">
    <h2>Our Products</h2>
    <SearchBar :categories="categories" @search="onSearch" @filter-category="onFilter" />
    <div class="product-grid">
      <ProductCard
        v-for="product in filteredProducts"
        :key="product.id"
        :product="product"
        @add-to-cart="addToCart"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import ProductCard from '../components/ProductCard.vue';
import SearchBar from '../components/SearchBar.vue';
import { useCartStore } from '../store/cart';

export default defineComponent({
  name: 'ProductsView',
  components: { ProductCard, SearchBar },
  setup() {
    const cartStore = useCartStore();
    const searchQuery = ref('');
    const selectedCategory = ref('');

    const products = ref([
      {
        id: 1,
        name: 'Ceramic Pour-Over Set',
        description: 'Handmade ceramic dripper and carafe with matte glaze finish.',
        price: 78.50,
        imageUrl: '/images/pour-over.jpg',
        onSale: false,
        inStock: true,
        rating: 5,
        reviewCount: 142,
        category: 'Kitchen',
      },
      {
        id: 2,
        name: 'Walnut Cutting Board',
        description: 'End-grain walnut board with juice groove, 18x12 inches.',
        price: 124.00,
        originalPrice: 155.00,
        imageUrl: '/images/cutting-board.jpg',
        onSale: true,
        inStock: true,
        rating: 4,
        reviewCount: 89,
        category: 'Kitchen',
      },
      {
        id: 3,
        name: 'Indigo Linen Throw',
        description: 'Plant-dyed linen blanket, 60x80 inches, natural indigo.',
        price: 195.00,
        imageUrl: '/images/linen-throw.jpg',
        onSale: false,
        inStock: true,
        rating: 5,
        reviewCount: 67,
        category: 'Home Decor',
      },
      {
        id: 4,
        name: 'Brass Desk Lamp',
        description: 'Adjustable arm lamp with aged brass finish and linen shade.',
        price: 245.00,
        imageUrl: '/images/desk-lamp.jpg',
        onSale: false,
        inStock: false,
        rating: 4,
        reviewCount: 53,
        category: 'Lighting',
      },
    ]);

    const categories = computed(() =>
      [...new Set(products.value.map((p) => p.category))].sort()
    );

    const filteredProducts = computed(() => {
      return products.value.filter((p) => {
        const matchesSearch = p.name.toLowerCase().includes(searchQuery.value.toLowerCase());
        const matchesCategory = !selectedCategory.value || p.category === selectedCategory.value;
        return matchesSearch && matchesCategory;
      });
    });

    const onSearch = (q: string) => { searchQuery.value = q; };
    const onFilter = (cat: string) => { selectedCategory.value = cat; };
    const addToCart = (item: any) => { cartStore.addItem(item); };

    return { products, filteredProducts, categories, onSearch, onFilter, addToCart };
  },
});
</script>

<style scoped>
.products-page h2 {
  margin-bottom: 24px;
}
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}
</style>
"""
    with open(f'{PROJECT_DIR}/src/views/ProductsView.vue', 'w') as f:
        f.write(products_view)

    # --- stub views ---
    for view_name, view_content in [
        ('ProductDetailView.vue', '<template><div><h2>Product Detail</h2></div></template>\n<script lang="ts">\nimport { defineComponent } from \'vue\';\nexport default defineComponent({ name: \'ProductDetailView\' });\n</script>\n'),
        ('CartView.vue', '<template><div><h2>Shopping Cart</h2><p>Your cart is empty.</p></div></template>\n<script lang="ts">\nimport { defineComponent } from \'vue\';\nexport default defineComponent({ name: \'CartView\' });\n</script>\n'),
    ]:
        with open(f'{PROJECT_DIR}/src/views/{view_name}', 'w') as f:
            f.write(view_content)

    # --- .gitignore ---
    gitignore = """node_modules/
dist/
.DS_Store
*.log
.env
.env.local
coverage/
"""
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write(gitignore)

    # --- vue.config.js ---
    vue_config = """const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    port: 8080,
    open: false,
  },
});
"""
    with open(f'{PROJECT_DIR}/vue.config.js', 'w') as f:
        f.write(vue_config)

    # --- tests/unit/cart.spec.ts ---
    cart_test = """import { setActivePinia, createPinia } from 'pinia';
import { useCartStore } from '@/store/cart';

describe('Cart Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('adds items to cart', () => {
    const cart = useCartStore();
    cart.addItem({ productId: 1, name: 'Test Product', price: 29.99, quantity: 1 });
    expect(cart.itemCount).toBe(1);
    expect(cart.totalPrice).toBeCloseTo(29.99);
  });

  it('increments quantity for duplicate items', () => {
    const cart = useCartStore();
    cart.addItem({ productId: 1, name: 'Test Product', price: 29.99, quantity: 1 });
    cart.addItem({ productId: 1, name: 'Test Product', price: 29.99, quantity: 2 });
    expect(cart.itemCount).toBe(3);
  });

  it('removes items from cart', () => {
    const cart = useCartStore();
    cart.addItem({ productId: 1, name: 'Widget', price: 10.00, quantity: 1 });
    cart.removeItem(1);
    expect(cart.itemCount).toBe(0);
  });
});
"""
    with open(f'{PROJECT_DIR}/tests/unit/cart.spec.ts', 'w') as f:
        f.write(cart_test)

    print(f'Initial project structure created at: {PROJECT_DIR}')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

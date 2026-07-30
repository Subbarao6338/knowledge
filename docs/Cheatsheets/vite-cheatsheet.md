---
layout: default
title: "Vite Cheatsheet"
---

# Vite Cheatsheet

Vite is a modern frontend build tool that is extremely fast. It consists of two major parts: a dev server that serves source files over native ES modules, and a Rollup build command that bundles your code for production.

---

## 1. Quick Start Commands

```bash
# Create a new Vite project interactively
npm create vite@latest my-awesome-app

# Install dependencies and launch the fast development server
npm install
npm run dev

# Build the application for production (creates a optimized /dist folder)
npm run build

# Preview the locally built production application
npm run preview
```

---

## 2. Basic Configuration (`vite.config.js` or `vite.config.ts`)

```javascript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  // 1. Plugins integration
  plugins: [react()],

  // 2. Local development server options
  server: {
    port: 3000,
    open: true, // Auto open browser on server startup
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  },

  // 3. Import path aliases
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },

  // 4. Production build configurations
  build: {
    outDir: 'dist',
    sourcemap: true,
    minify: 'esbuild', // standard ultra-fast minifier
    rollupOptions: {
      output: {
        // Manual chunk splitting
        manualChunks(id) {
          if (id.includes('node_modules')) {
            return 'vendor';
          }
        }
      }
    }
  }
});
```

---

## 3. Environment Variables & Modes

Vite uses `dotenv` to load environment variables from `.env` files. Variables must be prefixed with `VITE_` to be exposed to your client-side code.

```text
# .env.development
VITE_API_BASE_URL=http://localhost:3000/api
VITE_APP_TITLE=My App (Dev)

# .env.production
VITE_API_BASE_URL=https://api.myapp.com
VITE_APP_TITLE=My App
```

### Accessing Environment Variables in Client Code
```javascript
// Accessing variable
const apiEndpoint = import.meta.env.VITE_API_BASE_URL;

// Built-in utility booleans
const isDev = import.meta.env.DEV;     // true/false
const isProd = import.meta.env.PROD;   // true/false
const mode = import.meta.env.MODE;     // 'development' or 'production'
```

---

## 4. Static Asset Handling

### Direct URL Imports
```javascript
import imgUrl from './assets/logo.png';
// imgUrl resolves to '/src/assets/logo.png' in dev, or '/assets/logo-hash.png' in prod

document.getElementById('logo').src = imgUrl;
```

### Raw String Imports
```javascript
import rawSvgText from './assets/icon.svg?raw';
// Imports the file contents as a raw string
```

### Single-File Assembly (Inlining limits)
Assets smaller than `4KB` (by default) will be inlined as base64 data URIs automatically to avoid additional network requests.

---

## 5. CSS & CSS Modules

Vite supports pre-processors out of the box (just run `npm install -D sass` to use `.scss` files).

### CSS Modules
Any CSS file ending in `.module.css` is treated as a CSS module.

```css
/* button.module.css */
.customButton {
  background: var(--primary);
  color: white;
  padding: 8px 16px;
}
```

```javascript
import styles from './button.module.css';

export function Button() {
  return <button className={styles.customButton}>Click Me</button>;
}
```

---

## 6. Build & Optimization Best Practices

1. **Lazy Loading Components**: Use dynamic imports to let Rollup split chunks automatically:
   ```javascript
   const LazyComponent = () => import('./HeavyComponent.jsx');
   ```
2. **Keep Public Clean**: The `public/` directory contains files that are copied directly to the root of the build output without any processing. Use it only for assets like `favicon.ico` or `robots.txt`.
3. **Analyze Chunks size**: Install `rollup-plugin-visualizer` to get an interactive chart of your production bundles to keep sizes small.

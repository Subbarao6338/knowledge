---
layout: default
title: "Web Performance Optimization Cheatsheet"
---

# Web Performance Optimization Cheatsheet

Optimizing frontend assets, critical rendering path, and server behaviors to build fast web applications.

---

## 1. Core Web Vitals (CWV) Reference

Core Web Vitals are key metrics used by search engines and developers to grade real-world page speed.

| Metric | Full Name | Description | Target / Good |
| :--- | :--- | :--- | :--- |
| **LCP** | Largest Contentful Paint | Measures *loading* performance (how fast the main page content renders). | **≤ 2.5s** |
| **INP** | Interaction to Next Paint | Measures *responsiveness* (how fast page UI updates after user click/keypress). | **≤ 200ms** |
| **CLS** | Cumulative Layout Shift | Measures *visual stability* (prevents text jumping around due to loading images/fonts). | **≤ 0.1** |

---

## 2. Resource Hints & Document Optimizations

Instruct browsers how to prioritize network tasks early on.

```html
<!-- 1. DNS Prefetch: Resolve DNS early for external API domains -->
<link rel="dns-prefetch" href="https://api.example.com">

<!-- 2. Preconnect: Resolve DNS, TCP Handshake, and TLS negotiation -->
<link rel="preconnect" href="https://fonts.googleapis.com" crossorigin>

<!-- 3. Preload: Download critical assets (like fonts/LCP images) as a priority -->
<link rel="preload" href="/fonts/inter-bold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/images/hero-banner.webp" as="image">

<!-- 4. Prefetch: Download low-priority assets needed for subsequent page navigations -->
<link rel="prefetch" href="/pages/dashboard-bundle.js">
```

---

## 3. Optimizing the Critical Rendering Path (CRP)

The Critical Rendering Path represents the sequential steps the browser takes to convert HTML, CSS, and JS into visible screen pixels.

### Non-blocking Scripts
By default, scripts block HTML parsing. Use modern non-blocking attributes:
```html
<!-- async: Executes as soon as downloaded, blocking parsing momentarily -->
<script async src="analytics.js"></script>

<!-- defer: Downloads in parallel, executes strictly after HTML parsing completes (Recommended) -->
<script defer src="main-bundle.js"></script>
```

### Critical CSS Pattern
To avoid "Flash of Unstyled Content" (FOUC) and speed up LCP:
1. Inline your most critical CSS needed for styling above-the-fold content inside a `<style>` block in the HTML `<head>`.
2. Load remaining non-critical styles asynchronously:
```html
<link rel="stylesheet" href="deferred-styles.css" media="print" onload="this.media='all'">
```

---

## 4. Modern Cache Control Headers

Set caching parameters on your CDN or Origin Web Server to avoid redundant trips to the server.

```http
# 1. Immutable Long-Term Cache (for versioned/hashed static assets like JS, CSS, images)
Cache-Control: public, max-age=31536000, immutable

# 2. Revalidate Every Time (good for dynamic index.html files)
Cache-Control: public, max-age=0, must-revalidate

# 3. No Caching allowed (sensitive account pages)
Cache-Control: no-store, max-age=0
```

---

## 5. Webpack & Bundle Size Optimization Best Practices

Keep bundle sizes small to satisfy low-powered mobile devices over slow cellular networks.

### Code Splitting (Dynamic Imports)
Split large modules out of the initial loading bundle:
```javascript
// Before (Blocks initial bundle load):
// import { renderBigChart } from './charts';

// After (Downloads charts bundle only when user clicks):
button.addEventListener('click', async () => {
  const { renderBigChart } = await import('./charts');
  renderBigChart();
});
```

### Tree Shaking Requirements
Ensure your bundler can remove unused dead code lines:
- Use ES Modules (`import` and `export`) exclusively, avoiding CommonJS (`require` and `module.exports`).
- Configure `"sideEffects": false` inside `package.json` to allow clean pruning of unused dependencies.

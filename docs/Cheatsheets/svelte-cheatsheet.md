---
layout: default
title: "Svelte & SvelteKit Cheatsheet"
---

# Svelte & SvelteKit Cheatsheet

A modern master reference for Svelte and SvelteKit, covering reactive declarations, component properties, stores, lifecycle hooks, and SvelteKit routing conventions.

---

## 1. Svelte Component Syntax

Svelte components are declared in single `.svelte` files which bundle markup, styling, and script logic.

```html
<!-- Counter.svelte -->
<script>
  let count = 0; // standard reactive state variable

  function increment() {
    count += 1;
  }
</script>

<div class="counter">
  <h2>The count is {count}</h2>
  <button on:click={increment}>Increment</button>
</div>

<style>
  .counter {
    padding: 1rem;
    border: 1px solid #ccc;
    border-radius: 8px;
  }
</style>
```

---

## 2. Reactivity with `$:`

The `$:` prefix creates a **reactive declaration** or **reactive statement**. It runs whenever any dependent variable changes.

```html
<script>
  let count = 1;

  // Reactive declaration (re-calculated on count changes)
  $: doubled = count * 2;

  // Reactive statement / block
  $: if (count >= 10) {
    alert("Count is high!");
    count = 0; // reset
  }
</script>

<p>Count: {count} | Doubled: {doubled}</p>
```

---

## 3. Properties (Props)

To accept data from a parent component, use the `export` keyword.

```html
<!-- Child.svelte -->
<script>
  export let title = "Default Title"; // Default value if none provided
  export let itemLimit;
</script>

<div>
  <h3>{title}</h3>
  <p>Limit: {itemLimit}</p>
</div>
```

---

## 4. Control Flow (Blocks)

### If / Else
```html
{#if count > 10}
  <p>Count is greater than 10</p>
{:else if count === 10}
  <p>Count is exactly 10</p>
{:else}
  <p>Count is less than 10</p>
{/if}
```

### Each Loops
```html
<script>
  let items = [
    { id: '1', name: 'Item A' },
    { id: '2', name: 'Item B' }
  ];
</script>

<ul>
  {#each items as item (item.id)}
    <li>{item.name}</li>
  {/each}
</ul>
```

### Await Blocks (Async Promises)
```html
{#await fetchUserData()}
  <p>Loading user data...</p>
{:then data}
  <p>User name: {data.name}</p>
{:catch error}
  <p style="color: red">Error: {error.message}</p>
{/await}
```

---

## 5. Svelte Stores

Stores are used to share reactive state between unrelated components.

```javascript
// store.js
import { writable } from 'svelte/store';

export const userProfile = writable({
  name: 'Anonymous',
  loggedIn: false
});
```

### Using Stores in Components
Use the `$` prefix to automatically subscribe to and unsubscribe from stores.

```html
<!-- ProfileCard.svelte -->
<script>
  import { userProfile } from './store.js';

  function login() {
    userProfile.set({ name: 'Jules', loggedIn: true });
  }
</script>

<p>Welcome, {$userProfile.name}!</p>
<button on:click={login}>Log In</button>
```

---

## 6. SvelteKit File-System Routing

SvelteKit is the official framework for building full-stack apps with Svelte.

```text
src/routes/
├── +layout.svelte        # App-wide visual layout wrapper
├── +page.svelte          # Root home route (/)
├── +error.svelte         # Fallback error page
├── about/
│   └── +page.svelte      # Sub-page (/about)
└── blog/
    ├── +page.server.js   # Server loader to fetch blog lists from DB
    ├── +page.svelte      # Blog list page (/blog)
    └── [slug]/
        ├── +page.server.js # Dynamic segment server loader
        └── +page.svelte    # Blog detail page (/blog/my-first-post)
```

### SvelteKit Server Loader Example
```javascript
// src/routes/blog/+page.server.js
export async function load() {
  const posts = await fetchFromDatabase();
  return {
    posts
  };
}
```

```html
<!-- src/routes/blog/+page.svelte -->
<script>
  export let data; // Loaded data is automatically passed to the page as 'data'
</script>

<h1>Blog Feed</h1>
<ul>
  {#each data.posts as post}
    <li><a href="/blog/{post.slug}">{post.title}</a></li>
  {/each}
</ul>
```

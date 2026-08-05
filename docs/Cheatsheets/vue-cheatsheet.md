---
layout: default
title: "VueJS Cheatsheet"
---

# VueJS Cheatsheet

## 1. Vue 3 Composition API vs Options API

### Composition API (Modern & Scalable)
```vue
<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue'

// Primitive reactive state
const count = ref(0)

// Complex object reactive state
const user = reactive({
  name: 'Alex',
  role: 'Developer'
})

// Computed property
const doubledCount = computed(() => count.value * 2)

// Watcher
watch(count, (newValue, oldValue) => {
  console.log(`count changed from ${oldValue} to ${newValue}`)
})

// Lifecycle hook
onMounted(() => {
  console.log('Component mounted via Composition API!')
})

function increment() {
  count.value++
}
</script>

<template>
  <div>
    <p>Doubled Count: {{ doubledCount }}</p>
    <button @click="increment">Add</button>
  </div>
</template>
```

### Options API (Classic)
```vue
<script>
export default {
  data() {
    return {
      count: 0,
      user: {
        name: 'Alex',
        role: 'Developer'
      }
    }
  },
  computed: {
    doubledCount() {
      return this.count * 2
    }
  },
  watch: {
    count(newValue, oldValue) {
      console.log(`count changed from ${oldValue} to ${newValue}`)
    }
  },
  mounted() {
    console.log('Component mounted via Options API!')
  },
  methods: {
    increment() {
      this.count++
    }
  }
}
</script>
```

---

## 2. Core Directives Reference

| Directive | Purpose | Syntax Example |
| :--- | :--- | :--- |
| `v-bind` | Dynamic attribute binding | `:src="imageUrl"` or `:class="{ active: isActive }"` |
| `v-on` | Event listener binding | `@click="doSomething"` or `@submit.prevent="save"` |
| `v-model` | Two-way data binding | `<input v-model="searchText" />` |
| `v-if` / `v-else-if` / `v-else` | Conditional rendering (DOM manipulation) | `<p v-if="loading">Loading...</p>` |
| `v-show` | Toggle visibility (CSS `display: none`) | `<div v-show="isVisible">Sidebar</div>` |
| `v-for` | List rendering | `<li v-for="(item, idx) in list" :key="item.id">` |
| `v-slot` | Named or scoped slots templates | `<template #header><h1>Title</h1></template>` |
| `v-once` | Render element/component once and cache | `<span v-once>This will never change: {{ msg }}</span>` |
| `v-pre` | Skip compilation for this element | `{% raw %}<span v-pre>{{ this will not be compiled }}</span>{% endraw %}` |

---

## 3. Component Communication (Props & Emits)

### Child Component (`MyButton.vue`)
```vue
<script setup>
// Define props (inputs)
const props = defineProps({
  label: {
    type: String,
    required: true
  },
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'danger'].includes(value)
  }
})

// Define emits (outputs)
const emit = defineEmits(['customClick', 'update:modelValue'])

function handleClick() {
  emit('customClick', { timestamp: Date.now() })
}
</script>

<template>
  <button :class="['btn', variant]" @click="handleClick">
    {{ label }}
  </button>
</template>
```

### Parent Component (`App.vue`)
```vue
<script setup>
import MyButton from './MyButton.vue'

function handleChildClick(payload) {
  console.log('Child button clicked at:', payload.timestamp)
}
</script>

<template>
  <main>
    <MyButton
      label="Proceed to Payment"
      variant="primary"
      @customClick="handleChildClick"
    />
  </main>
</template>
```

---

## 4. Global State Management (Pinia)

Pinia is the modern, official state management library replacing Vuex.

### Defining a Store (`stores/counter.js`)
```javascript
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// Setup Store Pattern (Composition style)
export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  const doubled = computed(() => count.value * 2)

  function increment() {
    count.value++
  }

  function decrement() {
    count.value--
  }

  return { count, doubled, increment, decrement }
})
```

### Using a Store in a Component
```vue
<script setup>
import { useCounterStore } from '@/stores/counter'
import { storeToRefs } from 'pinia'

const store = useCounterStore()

// Destructure reactive properties cleanly using storeToRefs
const { count, doubled } = storeToRefs(store)
// Methods can be extracted directly without storeToRefs
const { increment, decrement } = store
</script>

<template>
  <div>
    <p>Pinia Count: {{ count }} (Doubled: {{ doubled }})</p>
    <button @click="decrement">-</button>
    <button @click="increment">+</button>
  </div>
</template>
```

---

## 5. Client-Side Routing (Vue Router)

### Router Setup (`router/index.js`)
```javascript
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/user/:id',
    name: 'user-profile',
    // Lazy loaded route
    component: () => import('../views/UserProfile.vue'),
    props: true, // Route params will be passed as props to the component
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// Navigation Guards (Auth check example)
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token')
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'login' })
  } else {
    next()
  }
})

export default router
```

---

## 6. Vue 3 Advanced Features & Optimization

### Template Refs
To access direct DOM elements:
```vue
<script setup>
import { ref, onMounted } from 'vue'

const inputElement = ref(null)

onMounted(() => {
  inputElement.value.focus()
})
</script>

<template>
  <input ref="inputElement" placeholder="Type here..." />
</template>
```

### Teleport (Render outside component tree)
Perfect for modals, popups, and dropdown overlays:
```vue
<template>
  <button @click="isOpen = true">Open Modal</button>

  <Teleport to="body">
    <div v-if="isOpen" class="modal-overlay">
      <div class="modal-content">
        <p>I am rendered directly inside the body element!</p>
        <button @click="isOpen = false">Close</button>
      </div>
    </div>
  </Teleport>
</template>
```

### Suspense (Async Dependencies Handling)
```vue
<template>
  <Suspense>
    <!-- Component containing async setup() -->
    <template #default>
      <AsyncDashboard />
    </template>

    <!-- Loading fallback spinner -->
    <template #fallback>
      <div class="spinner">Loading dashboard analytics...</div>
    </template>
  </Suspense>
</template>
```

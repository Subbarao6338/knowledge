---
layout: default
title: "CSS Cheatsheet"
---

# CSS Cheatsheet

## Flexbox Layout

```css
.container {
  display: flex;
  flex-direction: row;       /* row, row-reverse, column, column-reverse */
  flex-wrap: wrap;           /* nowrap, wrap, wrap-reverse */
  justify-content: center;   /* flex-start, flex-end, center, space-between, space-around, space-evenly */
  align-items: center;       /* flex-start, flex-end, center, baseline, stretch */
  align-content: stretch;    /* flex-start, flex-end, center, space-between, space-around, stretch */
}

.item {
  flex-grow: 1;              /* relative growth ratio */
  flex-shrink: 1;            /* relative shrinkage ratio */
  flex-basis: auto;          /* initial dimensions before distribution */
  align-self: auto;          /* overrides parent align-items setting for this item */
}
```

## Grid Layout

```css
.grid-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);  /* 3 columns of equal fraction width */
  grid-template-rows: auto 100px;
  grid-column-gap: 10px;
  grid-row-gap: 15px;
  gap: 15px 10px;                         /* row gap, column gap shorthand */
}

.grid-item {
  grid-column: 1 / 3;                     /* spans from column track 1 to 3 */
  grid-row: span 2;                       /* spans across two rows */
}
```

## CSS Custom Properties (Variables)

```css
:root {
  --primary-color: #3b82f6;
  --secondary-color: #10b981;
  --font-stack: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.card {
  background-color: white;
  color: var(--primary-color);
  font-family: var(--font-stack);
}
```

---

## 1. Advanced Selectors & Combinators

Modern CSS selectors allow precise targeting with zero Javascript.

```css
/* 1. Attribute Selectors */
a[href^="https://"] { color: green; }  /* Starts with https */
a[href$=".pdf"] { color: red; }        /* Ends with .pdf */
img[src*="avatar"] { border-radius: 50%; } /* Contains "avatar" */

/* 2. Pseudo-Classes */
li:nth-child(2n+1) { background: #eee; } /* Odd items list */
li:not(:first-child) { border-top: 1px solid #ccc; } /* Skip first */

/* 3. Logical Pseudo-Classes (:is, :where, :has) */
/* :is() groups selectors to simplify declarations */
:is(h1, h2, h3):hover { color: var(--primary-color); }

/* :where() is identical but has zero selector specificity weight */
:where(section, article) p { line-height: 1.6; }

/* :has() is the legendary parent selector (matches container based on contents) */
.card:has(img) { padding: 0; } /* Remove padding of card ONLY if card contains img */
.form-group:has(input:invalid) label { color: red; } /* Style label if input is invalid */

/* 4. Pseudo-Elements */
p::first-line { font-weight: bold; }
blockquote::before { content: "“"; font-size: 2em; }
```

---

## 2. Advanced Sizing & Math Functions

```css
.box {
  /* calc() performs basic dynamic calculations */
  width: calc(100% - 40px);

  /* clamp(min, preferred, max) creates fully responsive fluid text/padding bounds */
  font-size: clamp(1rem, 2.5vw + 0.5rem, 3rem);

  /* min() and max() select the lowest/highest value respectively */
  padding: min(5%, 20px);
  max-width: max(50vw, 400px);

  /* Logical dimensions for multi-language or vertical text alignments */
  margin-block-start: 1.5rem;  /* Top margin (logical) */
  padding-inline-end: 1rem;    /* Right padding (logical) */
}
```

---

## 3. Transitions & Core Animations

```css
/* 1. Transition shorthand (property duration timing-function delay) */
.btn {
  background-color: var(--primary-color);
  transition: background-color 0.3s cubic-bezier(0.4, 0, 0.2, 1), transform 0.1s ease;
}

.btn:hover {
  background-color: var(--secondary-color);
  transform: translateY(-2px);
}

/* 2. Keyframes Keyed Animations */
@keyframes slideAndFade {
  0% {
    transform: translateX(-50px);
    opacity: 0;
  }
  50% {
    transform: translateX(10px);
    opacity: 0.8;
  }
  100% {
    transform: translateX(0);
    opacity: 1;
  }
}

.toast-notification {
  /* animation name, duration, timing-function, delay, fill-mode */
  animation: slideAndFade 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
```

---

## 4. Responsive Queries (Media & Container)

### Viewport Media Queries (Based on browser width)
```css
@media (max-width: 768px) {
  .sidebar {
    display: none; /* Hide sidebar on mobile views */
  }
  .grid-container {
    grid-template-columns: 1fr; /* Switch grid to single column */
  }
}
```

### Container Queries (Based on parent component width - modern!)
Enables elements to style themselves dynamically depending on how much width their *parent container* has.
```css
/* Declare parent element as a container context */
.card-wrapper {
  container-type: inline-size;
  container-name: card-container;
}

/* Style child component based on parent wrapper width, NOT whole browser */
@container card-container (max-width: 400px) {
  .card {
    display: flex;
    flex-direction: column; /* Stack details vertically in narrow wrapper */
  }
  .card-avatar {
    width: 60px;
    height: 60px;
  }
}
```

---

## 5. Visual Filters & Blend Modes

```css
.card-overlay {
  /* Backdrop-filter applies blur or color-shifts behind transparency */
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px) saturate(180%);

  /* Drop shadow with transparency handling */
  filter: drop-shadow(0 4px 10px rgba(0, 0, 0, 0.15));
}

.text-blend-overlay {
  /* Mix-blend-mode blends element contents with parent background */
  mix-blend-mode: difference;
  color: white;
}
```

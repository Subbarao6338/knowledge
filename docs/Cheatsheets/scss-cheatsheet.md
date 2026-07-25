---
layout: default
title: "SCSS Cheatsheet"
---

# SCSS Cheatsheet

Sassy CSS (SCSS) is a preprocessor scripting language that compiles down to clean, standardized browser-runnable CSS.

---

## 1. Nesting & Reference Selectors

```scss
.navbar {
  background-color: #333;
  padding: 1rem;

  ul {
    list-style: none;
    margin: 0;

    li {
      display: inline-block;
      margin-right: 15px;
    }
  }

  // Parent Selector Reference (&)
  a {
    color: white;
    text-decoration: none;

    &:hover {
      color: #3b82f6;
    }
  }
}
```

## 2. Variables & Mixins (Reusability)

```scss
// Variables
$primary-color: #3b82f6;
$border-radius: 8px;

// Mixins with defaults
@mixin flex-center($direction: row) {
  display: flex;
  flex-direction: $direction;
  justify-content: center;
  align-items: center;
}

.card {
  border-radius: $border-radius;
  @include flex-center(column);
  background-color: lighten($primary-color, 30%); // Color adjustment functions
}
```

## 3. Extends & Placeholder Selectors

```scss
// Placeholders are not compiled to output unless extended
%button-base {
  padding: 10px 20px;
  border: none;
  font-weight: bold;
  cursor: pointer;
}

.btn-success {
  @extend %button-base;
  background-color: green;
  color: white;
}

.btn-danger {
  @extend %button-base;
  background-color: red;
  color: white;
}
```

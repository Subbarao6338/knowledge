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

---

## 4. Modern Sass Module System (@use & @forward)

Modern Sass discourages `@import` because of namespace collisions. Use `@use` to load members (variables, mixins, functions) with namespaces, and `@forward` to group files.

### Loading Modules with `@use`
```scss
// _variables.scss
$brand-color: #6366f1;
$font-stack: "Inter", sans-serif;

// _mixins.scss
@mixin text-truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

// main.scss
@use "variables";
@use "mixins" as mx; // Aliasing

.page-title {
  color: variables.$brand-color;
  font-family: variables.$font-stack;
  @include mx.text-truncate;
}
```

---

## 5. Sass Maps & Control Flow (@each, @for, @if)

Manage complex systems like responsive grids or color utilities using maps, loops, and conditional structures.

### Iterating over Maps with `@each`
```scss
// Map definition
$theme-colors: (
  "primary": #3b82f6,
  "success": #10b981,
  "warning": #f59e0b,
  "danger": #ef4444
);

// Dynamic utility class generator
@each $name, $color in $theme-colors {
  .bg-tint-#{$name} {
    background-color: scale-color($color, $lightness: 80%);
    border: 1px solid $color;
    color: darken($color, 15%);
  }
}
```

### Grids with `@for` loops
```scss
// Compile 12-column grid layout
@for $i from 1 through 12 {
  .col-#{$i} {
    width: (100% / 12) * $i;
  }
}
```

---

## 6. Functions & Advanced Media Mixins

Create specialized math calculations or write viewport break-point managers to keep code incredibly clean.

```scss
// Custom grid gap calculator function
@function calc-rem-spacing($pixels) {
  @return ($pixels / 16) * 1rem;
}

// Breakpoints Map
$breakpoints: (
  "sm": 640px,
  "md": 768px,
  "lg": 1024px,
  "xl": 1280px
);

// Responsive Viewport Mixin
@mixin respond-to($size) {
  $width: map-get($breakpoints, $size);
  @if $width {
    @media (min-width: $width) {
      @content;
    }
  } @else {
    @error "No breakpoint found for #{$size}!";
  }
}

// Practical usage
.container {
  padding: calc-rem-spacing(16);

  @include respond-to("md") {
    padding: calc-rem-spacing(32);
    display: flex;
  }
}
```

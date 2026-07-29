---
layout: default
title: "Bootstrap Cheatsheet"
---

# Bootstrap Cheatsheet

## Grid System Basics

```html
<!-- Container, Row, Columns -->
<div class="container text-center">
  <div class="row">
    <div class="col-sm-12 col-md-6 col-lg-4">
      Column Content
    </div>
    <div class="col-sm-12 col-md-6 col-lg-4">
      Column Content
    </div>
    <div class="col-sm-12 col-md-12 col-lg-4">
      Column Content
    </div>
  </div>
</div>
```

## Responsive Utilities & Breakpoints

```text
- Extra small: None (< 576px)
- Small: sm (>= 576px)
- Medium: md (>= 768px)
- Large: lg (>= 992px)
- Extra Large: xl (>= 1200px)
- Extra Extra Large: xxl (>= 1400px)
```

## Essential Helper Classes

```html
<!-- Display Properties -->
<div class="d-none d-md-block">Visible only on medium screen width and up</div>

<!-- Spacing (m = margin, p = padding, t = top, b = bottom, s = start, e = end, x = horiz, y = vert) -->
<div class="mt-4 pb-2 px-3">Margin top, padding bottom, padding horizontal</div>

<!-- Flexbox Shorthands -->
<div class="d-flex justify-content-between align-items-center">
  <span>Left</span>
  <span>Right</span>
</div>

<!-- Text Formatting -->
<p class="text-primary fw-bold text-center text-uppercase">Styled Text Element</p>
```

---

## Buttons & Interactive Components

```html
<!-- Buttons Colors and Sizes -->
<button type="button" class="btn btn-primary btn-lg">Large Primary</button>
<button type="button" class="btn btn-outline-secondary">Outline Secondary</button>
<button type="button" class="btn btn-danger btn-sm" disabled>Disabled Small Red</button>

<!-- Button Group -->
<div class="btn-group" role="group" aria-label="Basic example">
  <button type="button" class="btn btn-primary">Left</button>
  <button type="button" class="btn btn-primary">Middle</button>
  <button type="button" class="btn btn-primary">Right</button>
</div>
```

---

## Cards Layout

Cards provide a flexible and extensible content container with multiple variants.

```html
<div class="card" style="width: 18rem;">
  <img src="https://via.placeholder.com/150" class="card-img-top" alt="Card Header Image">
  <div class="card-body">
    <h5 class="card-title">Card Header Title</h5>
    <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card content.</p>
    <a href="#" class="btn btn-primary">Go somewhere</a>
  </div>
</div>
```

---

## Responsive Navigation Bar (Navbar)

```html
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">Navbar Logo</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="#">Home</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">Features</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">Pricing</a>
        </li>
      </ul>
      <form class="d-flex">
        <input class="form-control me-2" type="search" placeholder="Search..." aria-label="Search">
        <button class="btn btn-outline-success" type="submit">Search</button>
      </form>
    </div>
  </div>
</nav>
```

---

## Form Controls & Floating Labels

```html
<!-- Text Inputs and Selects -->
<div class="mb-3">
  <label for="exampleInputEmail1" class="form-label">Email address</label>
  <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp">
  <div id="emailHelp" class="form-text">We'll never share your email with anyone else.</div>
</div>

<!-- Floating Labels -->
<div class="form-floating mb-3">
  <input type="password" class="form-control" id="floatingPassword" placeholder="Password">
  <label for="floatingPassword">Password</label>
</div>
```

---

## Interactive Modals

Modals are positioned over active content on screen using trigger buttons.

```html
<!-- Trigger Button -->
<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
  Launch demo modal
</button>

<!-- Modal Container -->
<div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel">Modal Title</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        This is the main inner body content of your modal component.
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary">Save changes</button>
      </div>
    </div>
  </div>
</div>
```

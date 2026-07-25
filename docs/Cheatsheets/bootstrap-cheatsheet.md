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

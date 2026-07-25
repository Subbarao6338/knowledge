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

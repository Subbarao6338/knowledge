# CSS Grid & Flexbox Cheatsheet

A modern master reference comparing CSS Grid and CSS Flexbox layouts with advanced axis guides, utility tables, responsive patterns, and layout recipes.

---

## 1. Grid vs. Flexbox: Key Differences

| Feature | CSS Flexbox | CSS Grid |
| :--- | :--- | :--- |
| **Dimension** | One-Dimensional (Row **or** Column) | Two-Dimensional (Rows **and** Columns) |
| **Pillar Concept** | Content-driven layout. Items find their own size. | Container-driven layout. Space is divided first. |
| **Best Used For** | UI Component lists, navigations, dynamic alignments. | Full page architectures, complex forms, dashboard layouts. |
| **Nesting** | Flex items can also be flex containers. | Grid items can be grid containers, or house flex containers. |

---

## 2. Flexbox Reference

### Flex Container Properties

```css
.flex-container {
  display: flex;                  /* or inline-flex */

  /* Axis Orientation */
  flex-direction: row;            /* row | row-reverse | column | column-reverse */

  /* Flex Wrap behavior */
  flex-wrap: nowrap;              /* nowrap | wrap | wrap-reverse */

  /* Combined Shorthand */
  flex-flow: row wrap;

  /* Main-Axis Alignment */
  justify-content: flex-start;    /* flex-start | flex-end | center | space-between | space-around | space-evenly */

  /* Cross-Axis Alignment */
  align-items: stretch;           /* stretch | flex-start | flex-end | center | baseline */

  /* Alignment of wrapped rows (multi-line) */
  align-content: stretch;         /* stretch | flex-start | flex-end | center | space-between | space-around */

  /* Spacing between items */
  gap: 10px 20px;                 /* row-gap column-gap */
}
```

### Flex Item Properties

```css
.flex-item {
  /* Growth factor when there's leftover space */
  flex-grow: 1;                   /* default 0 (does not grow) */

  /* Shrink factor when container is too small */
  flex-shrink: 1;                 /* default 1 (can shrink) */

  /* Base size of item before grow/shrink math */
  flex-basis: auto;               /* auto | <length> */

  /* Shorthand (Highly Recommended) */
  flex: 1 1 auto;                 /* flex-grow flex-shrink flex-basis */

  /* Override align-items for a single element */
  align-self: auto;               /* auto | flex-start | flex-end | center | baseline | stretch */

  /* Visual arrangement order */
  order: 1;                       /* default 0 */
}
```

---

## 3. CSS Grid Reference

### Grid Container Properties

```css
.grid-container {
  display: grid;                  /* or inline-grid */

  /* Track Definitions */
  grid-template-columns: 200px 1fr 2fr;  /* absolute, fractional units */
  grid-template-rows: auto 1fr;

  /* Track Gaps */
  gap: 16px;                      /* grid-gap / row-gap & column-gap */

  /* Grid Template Areas (Visual naming) */
  grid-template-areas:
    "header header header"
    "sidebar main main"
    "footer footer footer";

  /* Aligning items inside cells */
  justify-items: stretch;         /* stretch | start | end | center */
  align-items: stretch;           /* stretch | start | end | center */

  /* Aligning tracks in the container */
  justify-content: stretch;       /* stretch | start | end | center | space-between | space-around | space-evenly */
  align-content: stretch;         /* stretch | start | end | center | space-between | space-around | space-evenly */
}
```

### Grid Item Properties

```css
.grid-item {
  /* Line-Based Placement */
  grid-column-start: 1;
  grid-column-end: 3;             /* spans column lines 1 to 3 */
  grid-row-start: span 2;         /* starts automatically, spans 2 rows */

  /* Line-Based Shorthands */
  grid-column: 1 / 3;             /* start / end */
  grid-row: 1 / span 2;           /* start / end */

  /* Named-Area Placement */
  grid-area: header;              /* Matches string defined in grid-template-areas */

  /* Align individual item inside its cell */
  justify-self: center;           /* stretch | start | end | center */
  align-self: center;              /* stretch | start | end | center */
}
```

---

## 4. Advanced Responsive Layout Tricks

### Auto-Fit & Auto-Fill (No Media Queries!)
Automatically create responsive column tracks that wrap perfectly without any `@media` definitions.

```css
.responsive-grid {
  display: grid;
  /* Min width of items is 250px, max is the available fractional space */
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
}
```
- **`auto-fit`:** Stretches filled columns to fill remaining empty space.
- **`auto-fill`:** Keeps the columns sized, leaving empty track space at the end of the container.

---

## 5. Modern Layout Recipes

### Recipe 1: Perfect Absolute Centering
The ultimate short way to center anything.

```css
.center-anyways {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* OR even shorter with Grid */
.center-anyways-grid {
  display: grid;
  place-content: center;
}
```

### Recipe 2: Sticky Footer (Flexbox)
Guarantees the footer remains pushed to the bottom of the viewport even on empty pages.

```css
.body-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.content {
  flex-grow: 1; /* Pushes footer down */
}

.footer {
  flex-shrink: 0;
}
```

### Recipe 3: Holy Grail Dashboard Layout (Grid)
```css
.dashboard {
  display: grid;
  grid-template-rows: 60px 1fr 40px;
  grid-template-columns: 240px 1fr;
  grid-template-areas:
    "header header"
    "sidebar main"
    "footer footer";
  height: 100vh;
}

header  { grid-area: header; }
sidebar { grid-area: sidebar; }
main    { grid-area: main; }
footer  { grid-area: footer; }
```

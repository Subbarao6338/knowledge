---
layout: default
title: "Tailwind CSS Cheatsheet"
---

# Tailwind CSS Cheatsheet

Tailwind CSS is a utility-first CSS framework designed for rapid UI development. Rather than pre-designed components, it provides low-level utility classes to build completely custom designs.

---

## 1. Quick Config (`tailwind.config.js`)

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          light: '#3fbaeb',
          DEFAULT: '#0fa9e6',
          dark: '#0c87b8',
        },
      },
      spacing: {
        '128': '32rem',
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
  ],
}
```

---

## 2. Layout & Spacing

### Box Alignment
- **Container:** `container` (centers and clamps to max-width based on screen sizes)
- **Display:** `block`, `inline-block`, `inline`, `flex`, `inline-flex`, `grid`, `hidden`
- **Overflow:** `overflow-auto`, `overflow-hidden`, `overflow-scroll`, `overflow-x-hidden`

### Spacing (Margin & Padding)
- **Padding:** `p-{size}` (all sides), `py-{size}` (top/bottom), `px-{size}` (left/right)
- **Margin:** `m-{size}` (all sides), `my-{size}` (top/bottom), `mx-{size}` (left/right), `mx-auto` (center block elements)
- **Sizes:** `0`, `0.5`, `1` (4px), `2` (8px), `3` (12px), `4` (16px), `8` (32px), `12` (48px), `16` (64px), `20`, `24`, `32`, `40`, `48`, `56`, `64`, `72`, `80`, `96`

---

## 3. Flexbox & Grid

### Flexbox Layout
- **Container:** `flex`
- **Direction:** `flex-row`, `flex-row-reverse`, `flex-col`, `flex-col-reverse`
- **Wrap:** `flex-wrap`, `flex-nowrap`
- **Grow/Shrink:** `flex-1`, `flex-auto`, `flex-initial`, `flex-none`, `grow`, `shrink`
- **Justify Content:** `justify-start`, `justify-end`, `justify-center`, `justify-between`, `justify-around`, `justify-evenly`
- **Align Items:** `items-start`, `items-end`, `items-center`, `items-baseline`, `items-stretch`

### Grid Layout
- **Container:** `grid`
- **Columns:** `grid-cols-1`, `grid-cols-2`, `grid-cols-3`, `grid-cols-4`, `grid-cols-12`
- **Column Span:** `col-span-1`, `col-span-2`, `col-span-12`, `col-start-1`, `col-end-auto`
- **Gap:** `gap-{size}`, `gap-x-{size}`, `gap-y-{size}`

---

## 4. Typography

### Font Styles
- **Size:** `text-xs`, `text-sm`, `text-base`, `text-lg`, `text-xl`, `text-2xl`, `text-3xl`, `text-4xl`, `text-5xl`, `text-6xl`
- **Weight:** `font-thin`, `font-light`, `font-normal`, `font-medium`, `font-semibold`, `font-bold`, `font-extrabold`
- **Color:** `text-black`, `text-white`, `text-gray-500`, `text-blue-600`, `text-red-500`
- **Alignment:** `text-left`, `text-center`, `text-right`, `text-justify`
- **Leading (Line Height):** `leading-none`, `leading-tight`, `leading-snug`, `leading-normal`, `leading-relaxed`, `leading-loose`
- **Tracking (Letter Spacing):** `tracking-tighter`, `tracking-tight`, `tracking-normal`, `tracking-wide`, `tracking-wider`, `tracking-widest`

---

## 5. Visuals & Decor

### Backgrounds
- **Color:** `bg-transparent`, `bg-black`, `bg-white`, `bg-slate-100`, `bg-emerald-500`
- **Opacity:** `bg-opacity-50`, `bg-opacity-75`
- **Gradients:** `bg-gradient-to-r`, `bg-gradient-to-t`, `from-indigo-500`, `via-purple-500`, `to-pink-500`

### Borders & Effects
- **Radius:** `rounded-none`, `rounded-sm`, `rounded`, `rounded-md`, `rounded-lg`, `rounded-xl`, `rounded-2xl`, `rounded-full`
- **Width:** `border-0`, `border`, `border-2`, `border-4`, `border-8`
- **Style:** `border-solid`, `border-dashed`, `border-dotted`, `border-double`
- **Color:** `border-gray-300`, `border-blue-500`
- **Shadow:** `shadow-sm`, `shadow`, `shadow-md`, `shadow-lg`, `shadow-xl`, `shadow-2xl`, `shadow-inner`, `shadow-none`

---

## 6. Responsive & States

Tailwind uses screen size prefixes to build highly responsive user interfaces.

### Breakpoints
- `sm`: `min-width: 640px` (mobile landscape)
- `md`: `min-width: 768px` (tablets)
- `lg`: `min-width: 1024px` (laptops)
- `xl`: `min-width: 1280px` (desktops)
- `2xl`: `min-width: 1536px` (large screens)

```html
<!-- Example of responsive widths and colors -->
<div class="w-full md:w-1/2 lg:w-1/3 bg-blue-500 md:bg-green-500 lg:bg-red-500">
  Responsive Box
</div>
```

### Hover, Focus, & Active States
```html
<button class="bg-blue-500 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-300 active:bg-blue-800">
  Click Me
</button>
```

---

## 7. Common Gotchas

1. **Dynamic Class Names:** Tailwind scans your raw source code for complete class names. If you construct classes dynamically using string interpolation, Tailwind will not find them and won't generate the styles.
   ```javascript
   // BAD:
   const color = 'red';
   const className = `text-${color}-500`; // Will not be compiled!

   // GOOD:
   const className = color === 'red' ? 'text-red-500' : 'text-blue-500';
   ```
2. **Purging CSS (Optimizing):** Ensure your `content` configuration covers all folders with UI components to avoid missing classes in production builds.
3. **Specifying Component Style Hierarchies:** Use utility classes directly rather than trying to write heavy custom CSS files using `@apply` on massive classes unless absolutely necessary. Keep CSS clean!

---

## 8. Arbitrary Values & JIT Customization

With Tailwind's Just-In-Time (JIT) engine, you can write inline arbitrary properties directly without configuring them in your theme:

```html
<!-- Arbitrary Width/Height/Padding -->
<div class="w-[347px] h-[calc(100vh-80px)] p-[1.8rem]">
  Arbitrary dimensions
</div>

<!-- Arbitrary Colors and Gradients -->
<span class="text-[#3b82f6] bg-[rgb(243,244,246)]">
  Custom Color Box
</span>

<!-- Arbitrary Grid Tracks -->
<div class="grid grid-cols-[200px_1fr_100px]">
  Custom grid track mapping
</div>
```

---

## 9. Group & Peer Modifiers (Complex Interactivity)

Tailwind allows you to style elements based on the state of their parent (`group`) or siblings (`peer`).

### Group States (Hover/Focus Parent)
```html
<div class="group border p-4 hover:bg-slate-50">
  <h3 class="text-slate-900 group-hover:text-blue-600">Parent Title</h3>
  <p class="text-slate-500 group-hover:text-slate-700">This description changes color when the entire card is hovered.</p>
</div>
```

### Peer States (Form Validation/Sibling Focus)
```html
<form class="space-y-4">
  <input type="email" class="peer border rounded p-2 invalid:border-red-500" placeholder="Enter email..." />
  <p class="hidden peer-invalid:block text-red-500 text-sm">
    Please enter a valid email address.
  </p>
</form>
```

---

## 10. Transitions & Keyframe Animations

Smooth out changes and add custom keyframe animations cleanly with utilities:

- **Transition Properties:** `transition`, `transition-colors`, `transition-all`, `transition-none`
- **Duration:** `duration-75` (75ms), `duration-150`, `duration-300`, `duration-500`, `duration-1000`
- **Timing Functions:** `ease-linear`, `ease-in`, `ease-out`, `ease-in-out`
- **Delay:** `delay-75`, `delay-150`, `delay-300`, `delay-500`

### Built-in Core Animations
- `animate-none`: Disable animation.
- `animate-spin`: Smooth 360-degree rotation (useful for spinner icons).
- `animate-ping`: Repeating outward expanding circle.
- `animate-pulse`: Gently fading in and out (useful for skeleton loading placeholders).
- `animate-bounce`: Repeating vertical hop.

```html
<!-- Spinning loading icon -->
<svg class="animate-spin h-5 w-5 mr-3 ..." viewBox="0 0 24 24"></svg>
```

---

## 11. Dark Mode Configuration

To support manual theme toggling via JS, ensure your tailwind configuration is set to `'class'` instead of the default `'media'`:

```javascript
// tailwind.config.js
module.exports = {
  darkMode: 'class', // Enables manual toggle by adding class="dark" to <html>
  // ...
}
```

Then prefix any dark mode utility styles with `dark:`:
```html
<div class="bg-white text-slate-900 dark:bg-slate-900 dark:text-white">
  Automatic Dark Theme Container
</div>
```

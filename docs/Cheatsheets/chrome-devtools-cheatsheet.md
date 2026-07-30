---
layout: default
title: "Chrome DevTools Cheatsheet"
---

# Chrome DevTools Cheatsheet

A highly detailed master guide covering Chrome Developer Tools, essential keyboard shortcuts, console API tricks, styling, and diagnostic workflows.

---

## 1. Quick Keyboard Shortcuts

Unlocking swift workflows via key binds.

| Command | Mac OS | Windows / Linux |
| :--- | :--- | :--- |
| **Open DevTools** | `Cmd + Opt + I` | `F12` or `Ctrl + Shift + I` |
| **Open Command Menu** | `Cmd + Shift + P` | `Ctrl + Shift + P` |
| **Switch Console Tab** | `Esc` (toggles drawer) | `Esc` |
| **Toggle Device Mode** | `Cmd + Shift + M` | `Ctrl + Shift + M` |
| **Search across files** | `Cmd + Opt + F` | `Ctrl + Shift + F` |
| **Inspect element hover**| `Cmd + Shift + C` | `Ctrl + Shift + C` |

*Command Menu Tip:* Press `Cmd + Shift + P` and type "screenshot" to capture specific DOM node screenshots, full-size screenshots, or standard viewport images effortlessly.

---

## 2. Advanced Console API Utilities

The Console panel has built-in utility commands that run natively outside standard JavaScript engines.

```javascript
// 1. $0, $1, $2, $3, $4 Reference
// Reference currently or recently active elements in the Elements panel tree.
$0.style.backgroundColor = "yellow"; // Highlight the currently selected DOM node!

// 2. Query Selectors
$(selector)     // Short for document.querySelector()
$$(selector)    // Short for Array.from(document.querySelectorAll())

// 3. Monitor Events
monitorEvents(window, ["resize", "scroll"]); // Track and print matching event objects to console
unmonitorEvents(window);                     // Disable event logging

// 4. Trace performance and stack counts
console.time("Heavy Loop");
for (let i = 0; i < 1000000; i++) {}
console.timeEnd("Heavy Loop"); // Heavy Loop: X.XX ms

// 5. Structure data outputs beautifully in tables
const users = [
  { id: 1, name: "Jules", role: "Admin" },
  { id: 2, name: "Subbarao", role: "Architect" }
];
console.table(users); // Renders a beautiful visual table directly in the logs panel!

// 6. Monitor Function Calls
monitor(myFunctionName);   // Print a log warning each time 'myFunctionName' gets invoked
unmonitor(myFunctionName); // Stop tracking
```

---

## 3. Styling & Elements panel hacks

Inspect layout issues, force element pseudo-states, and modify modern layouts instantly.

### Forcing Pseudo-states
- To debug `:hover`, `:active`, `:focus`, or `:visited` styles:
  1. Inspect the target node in the **Elements** panel.
  2. Right-click the element line and select **Force State** -> choose `:hover` (or click the `:hov` option tab in the Style Sidebar).

### Modern Flexbox & Grid Badges
- Elements featuring `display: flex` or `display: grid` will have interactive badges next to them in the inspector.
- Clicking the badge toggles on-screen visual overlay grids showing exact margins, lanes, gaps, and line numbers.

---

## 4. Network Panel Diagnostic Tricks

Identify slow requests, mock payloads, and optimize network overheads.

### Throttling Connection Speeds
- In the **Network** panel, locate the throttling dropdown (defaults to "No throttling").
- Toggle connection profiles to **Fast 3G**, **Slow 3G**, or **Offline** to test offline sync databases and slow loading progress bars.

### Payload Mocking & Local Overrides
- You can override any remote API payload locally without modifying backend servers:
  1. Go to the **Sources** tab -> select the **Overrides** sidebar option -> click **+ Select folder for overrides** (allow permission).
  2. In the **Network** panel, right-click the target request -> click **Override content**.
  3. Edit response bodies directly inside DevTools and save. All future requests to that URL will load your edited local mock!

---

## 5. Performance & Memory Leak Profiling

Track page rendering stutter, high CPU load, and JavaScript heap allocation leaks.

### Spotting "Jank" with Performance Profiles
1. Go to the **Performance** tab and click the **Record** button (or `Cmd + E`).
2. Interact with slow scrolling elements or animations for 5-10 seconds -> click **Stop**.
3. In the flame chart, analyze red bars next to "Frames" indicating long tasks exceeding **50ms** (blocking main thread).
4. Click on a long task to see the exact call stack and script lines causing layout thrashing.

### Locating Memory Leaks
1. Go to the **Memory** panel -> select **Heap snapshot** -> click **Take snapshot**.
2. Perform on-screen actions (e.g. opening and closing interactive modals multiple times).
3. Take a second snapshot. Select **Comparison** view from the perspectives dropdown.
4. Filter by objects remaining active that should have been garbage collected (e.g. detached DOM nodes, uncleared Event Listeners, or un-terminated WebSocket connections).

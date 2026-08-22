---
layout: default
title: "PWA & WebAssembly Cheatsheet"
---

# Progressive Web Apps (PWA) & WebAssembly (Wasm) Cheatsheet

Progressive Web Apps (PWAs) combine native app capabilities with web reach. WebAssembly (Wasm) provides a binary instruction format for near-native code execution speed in web browsers.

---

## 1. PWA & Service Worker Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Register
    Register --> Installing
    Installing --> Installed
    Installed --> Activating
    Activating --> Active
    Active --> FetchIntercept: Intercept Network Requests
    Active --> PushNotify: Receive Push Messages
```

---

## 2. WebAssembly (Wasm) Execution Flow

```mermaid
graph TD
    Code[Rust / C++ / Go Source] --> Compiler[Wasm Compiler target = wasm32]
    Compiler --> WasmFile[.wasm Binary File]
    WasmFile --> JS[Web Browser JS Engine]
    JS --> Instantiation[WebAssembly.instantiateStreaming]
    Instantiation --> Execution[Near-Native Execution Speed]
```

---

## Key Snippets

### Registering Service Worker
```javascript
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js').then(reg => {
      console.log('ServiceWorker registered:', reg.scope);
    });
  });
}
```

### Instantiating WebAssembly
```javascript
WebAssembly.instantiateStreaming(fetch('module.wasm'), {})
  .then(results => {
    const { add } = results.instance.exports;
    console.log('Wasm result:', add(10, 20));
  });
```

---

## Related Cheatsheets

- [Master Index](../Cheatsheets.html)
- [Web Performance Optimization Cheatsheet](web-performance-optimization-cheatsheet.md)
- [Rust Cheatsheet](rust-cheatsheet.md)
- [JavaScript Cheatsheet](javascript-cheatsheet.md)

---
layout: default
title: "Deno Cheatsheet"
---

# Deno Cheatsheet

An exhaustive developer's reference for **Deno**, the modern, secure runtime for JavaScript, TypeScript, and WebAssembly.

---

## 1. Security & Sandbox Permissions

Unlike Node, Deno runs code in a secure sandbox by default. You must explicitly allow capabilities with command-line flags.

| Flag | Capability | Example |
| :--- | :--- | :--- |
| `--allow-net` | Network access | `deno run --allow-net app.ts` |
| `--allow-read` | Read files | `deno run --allow-read=/tmp app.ts` |
| `--allow-write` | Write files | `deno run --allow-write=/tmp app.ts` |
| `--allow-env` | Environment access | `deno run --allow-env=PORT app.ts` |
| `--allow-run` | Run subprocesses | `deno run --allow-run app.ts` |
| `--allow-all` / `-A` | Disable all security | `deno run -A app.ts` |

---

## 2. CLI Tooling

Deno has built-in code management tools out of the box, eliminating extra dev-dependencies.

```bash
# General runtime
deno run app.ts                        # compile & run a TS/JS file
deno run --watch app.ts                # auto-restarts on change
deno compile --output app-bin app.ts   # build standalone single executable

# Code styling & linting
deno fmt                               # formats files in place
deno fmt --check                       # verify formatting styles
deno lint                              # run static analysis linter

# Dependencies & JSR
deno add @std/http                     # add standard package from JSR/npm
deno install                           # fetch and cache dependencies
deno cache deps.ts                     # pre-compile and lock dependencies
```

---

## 3. Core Standard Library & Web Standards

Deno utilizes modern Web APIs (like standard `fetch`, `Request`, `Response`, `WebSockets`, `ReadableStream`) natively, avoiding non-standard interfaces.

### Fast Native HTTP Server (`Deno.serve`)
```typescript
import { serve } from "jsr:@std/http/server";

Deno.serve({ port: 8080 }, (req: Request) => {
  const url = new URL(req.url);

  if (url.pathname === "/") {
    return new Response("Hello from Deno Secure Runtime!");
  }
  if (url.pathname === "/json") {
    return Response.json({ success: true, timestamp: Date.now() });
  }

  return new Response("Not Found", { status: 404 });
});
```

### Advanced File Operations
```typescript
// 1. Reading file content
const text = await Deno.readTextFile("input.txt");

// 2. Writing file content
await Deno.writeTextFile("output.txt", "Data generated safely.");

// 3. Inspecting file metadata
const info = await Deno.stat("output.txt");
console.log(`File size: ${info.size} bytes. Modified: ${info.mtime}`);
```

---

## 4. Deno KV (Built-in Key-Value Database)

Deno includes **Deno KV**, a zero-config, transactional key-value database built into the runtime. It supports ACID properties and distributed scaling.

```typescript
// Open connection to KV database (works locally and on Deno Deploy)
const kv = await Deno.openKv();

// 1. Setting and writing values
await kv.set(["users", "jules"], { name: "Jules", role: "Admin" });

// 2. Retrieving value by namespace array key
const response = await kv.get(["users", "jules"]);
console.log("User Profile:", response.value); // { name: "Jules", role: "Admin" }

// 3. Deleting values
await kv.delete(["users", "jules"]);

// 4. Batch transaction updates
const r1 = await kv.atomic()
  .check({ key: ["users", "jules"], versionstamp: null })
  .set(["users", "jules"], { name: "Jules", updated: true })
  .commit();
```

---

## 5. Deno Task Runner & Configuration

Store scripts, security settings, and runtime configurations inside a single `deno.json` or `deno.jsonc` file.

```jsonc
{
  "tasks": {
    "start": "deno run --allow-net --allow-read main.ts",
    "dev": "deno run --allow-net --allow-read --watch main.ts",
    "test": "deno test --allow-read --allow-env"
  },
  "imports": {
    "@std/http": "jsr:@std/http@^1.0.0",
    "lodash": "npm:lodash@^4.17.21"
  },
  "fmt": {
    "useTabs": false,
    "lineWidth": 100,
    "singleQuote": true
  }
}
```

Execute Deno Tasks:
```bash
deno task dev
```

---

## 6. JSR (Javascript Registry)

Deno is deeply integrated with JSR, the modern package registry focused on TypeScript, standard auto-documentation, and ES module layouts.

```typescript
// Importing direct from JSR
import { assert } from "jsr:@std/assert";
import { parse } from "jsr:@std/toml";

const parsed = parse(`
[database]
server = "192.168.1.1"
ports = [ 8001, 8001, 8002 ]
`);

assert(parsed.database.ports.length === 3);
```

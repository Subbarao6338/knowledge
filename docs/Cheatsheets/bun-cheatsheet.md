---
layout: default
title: "Bun Cheatsheet"
---

# Bun Cheatsheet

A highly-detailed reference for **Bun**, the fast, all-in-one JavaScript/TypeScript runtime, bundler, package manager, and test runner.

---

## 1. CLI Commands

Bun provides a single unified CLI replacing `node`, `npm`, `npx`, and `jest`/`vitest`.

```bash
# Running scripts & files
bun run index.ts                     # run a TS/JS file natively
bun run dev                          # execute scripts defined in package.json
bun x package-name                   # run a package from bin (replaces npx)

# Managing packages
bun install                          # install all dependencies
bun add package-name                 # add dependency (replaces npm install)
bun add -d package-name              # add devDependency
bun remove package-name              # remove dependency
bun update                           # update packages
```

---

## 2. Fast Package Manager

Bun installs dependencies up to 25x faster than npm/yarn by using a global cache, hardlinks, and optimized system calls.

```bash
# Bun uses a binary lockfile (bun.lockb) for super fast parses
bun install --frozen-lockfile        # production install (enforces lockfile)
bun pm bin                           # locate the active node_modules/.bin directory
bun pm cache                         # show the cache folder path
bun pm cache rm                      # clear the local/global package cache
```

---

## 3. High-Performance Core APIs

Bun provides blazing fast replacements for standard file, network, and security operations.

### Fast HTTP Server (`Bun.serve`)
```typescript
Bun.serve({
  port: 3000,
  fetch(req) {
    const url = new URL(req.url);
    if (url.pathname === "/") {
      return new Response("Welcome to Bun!");
    }
    if (url.pathname === "/api") {
      return Response.json({ status: "ok", version: Bun.version });
    }
    return new Response("Not Found", { status: 404 });
  },
  error(error) {
    return new Response(`Error occurred: ${error.message}`, { status: 500 });
  },
});
console.log("Server running on http://localhost:3000");
```

### High-Speed File I/O (`Bun.file`)
```typescript
// 1. Reading files efficiently
const file = Bun.file("data.json");
const exists = await file.exists();
const text = await file.text();
const json = await file.json(); // Direct parse

// 2. Writing files efficiently
const data = { name: "Bun", speed: "blazing" };
await Bun.write("output.json", JSON.stringify(data, null, 2));

// 3. Streaming and binary content
const binaryStream = file.stream();
const arrayBuffer = await file.arrayBuffer();
```

### Cryptography & Password Hashing
```typescript
// Fast hashing out of the box
const password = "mysecretpassword";
const hashed = await Bun.password.hash(password);

// Verify hashed password
const isMatch = await Bun.password.verify(password, hashed);
console.log(`Password match: ${isMatch}`);
```

---

## 4. Built-in SQLite Database

Bun comes natively bundled with a highly optimized SQLite driver (`bun:sqlite`), bypassing slow system-level bindings.

```typescript
import { Database } from "bun:sqlite";

// Create an in-memory database or load a file
const db = new Database(":memory:"); // or new Database("mydb.sqlite");

// Create table and execute queries
db.run("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)");

// Prepare statement and execute batch operations
const insertUser = db.prepare("INSERT INTO users (name, email) VALUES ($name, $email)");
insertUser.run({ $name: "Jules", $email: "jules@example.com" });

// Retrieve results
const users = db.query("SELECT * FROM users").all();
const singleUser = db.query("SELECT * FROM users WHERE id = ?1").get(1);

console.log("Database entries:", users);
db.close();
```

---

## 5. Bun Shell (`$`)

Bun Shell allows you to run shell commands inside JavaScript/TypeScript cross-platform (Mac, Linux, Windows) with complete escape safety.

```typescript
import { $ } from "bun";

// 1. Basic command execution
await $`echo "Hello World"`;

// 2. Redirect stdout into variables
const files = await $`ls -la`.text();
console.log("Files present:", files);

// 3. Multi-line script execution
const branch = "main";
await $`
  git checkout ${branch}
  git pull origin ${branch}
`;

// 4. Input redirection from variables
const inputData = "Data to process\nMore lines";
const processed = await $`grep "Data"`.map(inputData).text();
```

---

## 6. Native Bundler (`Bun.build`)

Bun features an incredibly fast JavaScript/TypeScript compiler and bundler.

```typescript
// build.ts
await Bun.build({
  entrypoints: ["./index.ts"],
  outdir: "./dist",
  target: "browser",       // "browser" | "bun" | "node"
  minify: true,
  sourcemap: "external",   // "inline" | "external" | "none"
  naming: "[name].[ext]",
});
```

Execute build via CLI:
```bash
bun build ./index.ts --outdir ./dist --minify
```

---

## 7. Bun Test

Bun includes a fully Jest-compatible fast test runner built-in, supporting TS, JSX, mock interfaces, and snapshots.

```typescript
// math.test.ts
import { expect, test, describe, beforeAll, mock } from "bun:test";

describe("Math Suite", () => {
  beforeAll(() => {
    console.log("Setting up suite...");
  });

  test("addition works", () => {
    expect(1 + 1).toBe(2);
  });

  test("object matching", () => {
    expect({ a: 1, b: 2 }).toEqual({ a: 1, b: 2 });
  });

  test("mocking functions", () => {
    const double = mock((x: number) => x * 2);
    expect(double(2)).toBe(4);
    expect(double).toHaveBeenCalledTimes(1);
  });
});
```

Run tests from the CLI:
```bash
bun test                             # run all tests (*.test.ts, *.spec.ts)
bun test --watch                     # run tests in watcher mode
bun test --coverage                  # run and generate code coverage report
```

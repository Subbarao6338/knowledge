---
layout: default
title: "NodeJS Cheatsheet"
---

# NodeJS Cheatsheet

## CommonJS vs ES Modules Imports

```javascript
// CommonJS (Legacy standard)
const fs = require('fs');
const path = require('path');

// ES Modules (Modern standard - needs "type": "module" in package.json)
import fsPromises from 'fs/promises';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';
```

## Basic File System APIs

```javascript
import fs from 'fs/promises';

// Write File
async function writeLog(message) {
  try {
    await fs.writeFile('app_output.log', `${message}\n`, { flag: 'a' });
  } catch (err) {
    console.error("FS Error:", err);
  }
}

// Read File
async function readConfig() {
  const raw = await fs.readFile('config.json', 'utf-8');
  return JSON.parse(raw);
}
```

## Creating HTTP/Express Server

```javascript
import express from 'express';

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json()); // Body Parser Middleware

// GET handler
app.get('/api/v1/health', (req, res) => {
  res.status(200).json({ status: "UP", timestamp: new Date() });
});

// POST handler
app.post('/api/v1/echo', (req, res) => {
  const body = req.body;
  res.status(201).json({ message: "Payload processed successfully", payload: body });
});

app.listen(PORT, () => {
  console.log(`Server listening live on http://localhost:${PORT}`);
});
```

---

## 1. Events Module & EventEmitter

The Node.js core is built on an asynchronous event-driven architecture, orchestrated by the `events` module.

```javascript
import { EventEmitter } from 'events';

class OrderProcessor extends EventEmitter {
  placeOrder(orderId, amount) {
    console.log(`Placing order: ${orderId}`);
    // Process order logic...

    // Emit custom event
    this.emit('orderPlaced', { id: orderId, total: amount });
  }
}

const processor = new OrderProcessor();

// Listen to events
processor.on('orderPlaced', (data) => {
  console.log(`[Notification Service] Order ${data.id} placed for $${data.total}`);
});

processor.once('orderPlaced', (data) => {
  console.log(`[Inventory Service] Executing one-time supply lock check for order ${data.id}`);
});

// Place order triggers both event listeners
processor.placeOrder('ORD-90234', 150.50);
```

---

## 2. Buffers and Streams API

Buffers and Streams allow Node.js to read, write, and process binary files or large network datasets efficiently without loading the entire content into system memory.

### Working with Buffers (Binary memory allocation)
```javascript
// Allocate buffer of 16 bytes
const buf1 = Buffer.alloc(16);

// Write string to buffer
buf1.write("Hello binary!");

// Convert buffer back to string or hex
console.log(buf1.toString('utf-8'));
console.log(buf1.toString('hex'));

// Create buffer from string or array
const bufFromStr = Buffer.from("NodeJS is fast");
```

### High-Performance Streams (Read/Write chunks sequentially)
```javascript
import { createReadStream, createWriteStream } from 'fs';
import { Transform } from 'stream';

// 1. Create a readable stream from a large file
const readableStream = createReadStream('large_source_file.csv', { encoding: 'utf8', highWaterMark: 64 * 1024 });

// 2. Create a writable stream to destination
const writableStream = createWriteStream('uppercase_output.csv');

// 3. Create a Transform Stream to modify data on-the-fly
const uppercaseTransformer = new Transform({
  transform(chunk, encoding, callback) {
    const transformedData = chunk.toString().toUpperCase();
    this.push(transformedData);
    callback();
  }
});

// 4. Pipe streams together with error handling
readableStream
  .pipe(uppercaseTransformer)
  .pipe(writableStream)
  .on('finish', () => {
    console.log('File processing completed seamlessly.');
  })
  .on('error', (err) => {
    console.error('An error occurred during file streaming:', err);
  });
```

---

## 3. Child Processes (`exec`, `spawn`, `fork`)

Scale or offload commands to separate sub-processes to execute system bash scripts or background code.

```javascript
import { exec, spawn, fork } from 'child_process';

// 1. exec(): Runs command in a shell, buffers whole output (good for small output)
exec('ls -la', (err, stdout, stderr) => {
  if (err) {
    console.error(`Exec Error: ${err}`);
    return;
  }
  console.log(`Files list:\n${stdout}`);
});

// 2. spawn(): Spawns command, stream outputs directly (good for huge outputs/servers)
const pyProcess = spawn('python', ['-c', 'print("Spawned process runs python code!")']);

pyProcess.stdout.on('data', (data) => {
  console.log(`Python process output: ${data.toString()}`);
});

// 3. fork(): Special spawn version with full inter-process IPC communication channels
const worker = fork('./scripts/worker_script.js');

worker.send({ task: 'start_heavy_computation', data: 50000 });

worker.on('message', (result) => {
  console.log('Received computation result from child process:', result);
  worker.kill(); // Stop process
});
```

---

## 4. Multithreading via Worker Threads

Worker threads permit executing parallel JavaScript calculations in actual system threads, bypassing single-thread limits.

### Main File (`main.js`)
```javascript
import { Worker } from 'worker_threads';

function runWorkerTask(numberToCalculate) {
  return new Promise((resolve, reject) => {
    const worker = new Worker('./worker.js', {
      workerData: { number: numberToCalculate }
    });

    worker.on('message', resolve);
    worker.on('error', reject);
    worker.on('exit', (code) => {
      if (code !== 0) reject(new Error(`Worker stopped with exit code ${code}`));
    });
  });
}

const result = await runWorkerTask(40);
console.log('Fibonacci (40) calculated via Worker Thread:', result);
```

### Worker File (`worker.js`)
```javascript
import { parentPort, workerData } from 'worker_threads';

function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

const result = fibonacci(workerData.number);

// Pass calculation result back to parent
parentPort.postMessage(result);
```

---

## 5. System Clustering (Scaling Servers)

Run multiple server instances on the exact same port by automatically spreading requests across CPUs.

```javascript
import cluster from 'cluster';
import http from 'http';
import { availableParallelism } from 'os';

if (cluster.isPrimary) {
  const cpuCount = availableParallelism();
  console.log(`Primary cluster process is running. Forking ${cpuCount} workers...`);

  // Fork process for each core
  for (let i = 0; i < cpuCount; i++) {
    cluster.fork();
  }

  cluster.on('exit', (worker, code, signal) => {
    console.log(`Worker process ${worker.process.pid} died. Spinning up replacement...`);
    cluster.fork();
  });
} else {
  // Workers share the same TCP port
  http.createServer((req, res) => {
    res.writeHead(200);
    res.end(`Served from cluster worker process ${process.pid}\n`);
  }).listen(8000);

  console.log(`Worker process ${process.pid} started serving requests.`);
}
```

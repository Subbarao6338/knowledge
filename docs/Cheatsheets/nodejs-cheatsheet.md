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

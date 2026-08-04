---
layout: default
title: "Javascript Cheatsheet"
---

# Javascript Cheatsheet

## ES6+ Core Grammar & Syntax

```javascript
// Variable bindings
const immutableValue = 42;
let reassignableValue = "Hello";

// Arrow Functions
const add = (a, b) => a + b;
const blockFunction = (x) => {
    const double = x * 2;
    return double + 1;
};

// Template Literals
const user = "Rao";
console.log(`Hello, ${user}! The math answer is ${1 + 1}`);
```

## Array & Object Operations

```javascript
const items = [1, 2, 3, 4, 5];

// Map, Filter, Reduce
const doubled = items.map(n => n * 2);
const evens = items.filter(n => n % 2 === 0);
const sum = items.reduce((acc, curr) => acc + curr, 0);

// Destructuring & Spread Operators
const person = { name: "Rao", role: "Developer", age: 30 };
const { name, ...restOfAttributes } = person;
const extendedPerson = { ...person, country: "USA" };

const listA = [1, 2];
const combinedList = [...listA, 3, 4];
```

## Async Control Flow (Promises, Async/Await)

```javascript
// Promise API
const fetchData = (url) => {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            if (url) resolve({ status: "success", data: [1, 2, 3] });
            else reject(new Error("No URL provided"));
        }, 1000);
    });
};

// Async/Await Pattern
async function run() {
    try {
        const response = await fetchData("https://api.com/items");
        console.log("Response:", response.data);
    } catch (err) {
        console.error("Fetch Error:", err.message);
    } finally {
        console.log("Finished running query pipeline.");
    }
}
```

---

## 1. Closures and Lexical Scoping

A closure is the combination of a function bundled together with references to its surrounding state (the lexical environment).

```javascript
function createCounter(initialValue = 0) {
  let count = initialValue; // Private variable encapsulated in closure

  return {
    increment() {
      count++;
      return count;
    },
    decrement() {
      count--;
      return count;
    },
    getValue() {
      return count;
    }
  };
}

const counter = createCounter(10);
console.log(counter.increment()); // 11
console.log(counter.increment()); // 12
console.log(counter.getValue());   // 12
// count is inaccessible directly from outside: console.log(counter.count) => undefined
```

---

## 2. Prototypes & Inheritance Chain

In JavaScript, objects have a private property pointing to another object called its prototype.

```javascript
// 1. Prototypal Inheritance (Classic constructor pattern)
function Animal(name) {
  this.name = name;
}

Animal.prototype.speak = function() {
  return `${this.name} makes a noise.`;
};

function Dog(name, breed) {
  Animal.call(this, name); // Call parent constructor with "this" context
  this.breed = breed;
}

// Inherit Animal prototypes
Dog.prototype = Object.create(Animal.prototype);
// Reset constructor pointer to Dog
Dog.prototype.constructor = Dog;

// Override parent method
Dog.prototype.speak = function() {
  return `${this.name} barks!`;
};

const fido = new Dog("Fido", "Golden Retriever");
console.log(fido.speak()); // "Fido barks!"
```

---

## 3. The JS Event Loop & Concurrency Model

JavaScript is a single-threaded non-blocking runtime. It utilizes a concurrency engine involving:
- **Call Stack:** Where function execution frames are stacked and run.
- **Microtask Queue:** Processes Promises (`then`, `catch`, `finally`, `await`) and `queueMicrotask` directly after current stack clears, *before* anything else.
- **Macrotask (Callback) Queue:** Processes `setTimeout`, `setInterval`, `setImmediate`, network API requests, DOM clicks.

```javascript
console.log("1. Start of script"); // Call Stack executes directly

setTimeout(() => {
  console.log("5. Macrotask timeout finished"); // Enqueued in Macrotask queue
}, 0);

Promise.resolve().then(() => {
  console.log("3. Microtask promise callback"); // Enqueued in Microtask queue
});

queueMicrotask(() => {
  console.log("4. Explicit microtask callback"); // Enqueued in Microtask queue
});

console.log("2. End of script"); // Call Stack completes

// Output order:
// 1. Start of script
// 2. End of script
// 3. Microtask promise callback
// 4. Explicit microtask callback
// 5. Macrotask timeout finished
```

---

## 4. Meta-Programming with Proxy and Reflect

`Proxy` intercepts object target operations, and `Reflect` executes standard object default behaviors.

```javascript
const targetObject = {
  id: 'USER-100',
  username: 'jules',
  age: 25
};

const securityProxy = new Proxy(targetObject, {
  // Intercept reads
  get(target, prop, receiver) {
    console.log(`[Proxy Log] Reading attribute property: ${prop}`);
    if (prop === 'id') {
      return "ACCESS_DENIED"; // Guard specific fields
    }
    return Reflect.get(target, prop, receiver);
  },

  // Intercept writes
  set(target, prop, value, receiver) {
    console.log(`[Proxy Log] Writing attribute property ${prop} = ${value}`);
    if (prop === 'age' && (typeof value !== 'number' || value <= 0)) {
      throw new TypeError("Age must be a positive number!");
    }
    return Reflect.set(target, prop, value, receiver);
  }
});

console.log(securityProxy.username); // Logs access, returns "jules"
console.log(securityProxy.id);       // Returns "ACCESS_DENIED"
securityProxy.age = 30;              // Logs mutation
// securityProxy.age = "not-a-number"; // Throws TypeError
```

---

## 5. Modern Class Grammar & Modules

```javascript
export class EnterpriseUser {
  // Private field (starts with #) - inaccessible from outside
  #hashedPassword;

  static activeInstances = 0; // Static class property

  constructor(username, rawPassword) {
    this.username = username;
    this.#hashedPassword = this.#hash(rawPassword);
    EnterpriseUser.activeInstances++;
  }

  // Getter
  get profile() {
    return `Username: ${this.username}`;
  }

  // Setter
  set password(newPassword) {
    this.#hashedPassword = this.#hash(newPassword);
  }

  // Private method
  #hash(pwd) {
    return `###${pwd}###`; // Simple mock hash representation
  }

  // Static method
  static printTotalInstances() {
    return `Total users logged into memory: ${EnterpriseUser.activeInstances}`;
  }
}
```

---

## 7. Custom Iterators & Generators Protocol

Objects can customize their iteration behavior (like supporting `for...of` loops) by implementing the `Symbol.iterator` property.

```javascript
const collection = {
  items: ["Alpha", "Beta", "Gamma"],
  [Symbol.iterator]() {
    let index = 0;
    return {
      next: () => {
        if (index < this.items.length) {
          return { value: this.items[index++], done: false };
        } else {
          return { value: undefined, done: true };
        }
      }
    };
  }
};

for (const name of collection) {
  console.log(name); // Prints Alpha, Beta, Gamma
}
```

---

## 6. Advanced Fetch Requests with Cancelation (AbortController)

Cancel pending HTTP fetch requests to optimize network resources when components unmount or user searches again.

```javascript
async function fetchWithTimeout(url, duration = 5000) {
  // 1. Instantiate controller
  const controller = new AbortController();
  const { signal } = controller;

  // 2. Set timeout callback to trigger abort
  const timeoutId = setTimeout(() => {
    controller.abort();
    console.warn("Request timed out - aborting fetch request!");
  }, duration);

  try {
    const response = await fetch(url, { signal });
    const data = await response.json();
    return data;
  } catch (error) {
    if (error.name === 'AbortError') {
      return { status: "aborted", reason: "Network operation timed out." };
    }
    throw error;
  } finally {
    clearTimeout(timeoutId); // Clean up timer
  }
}
```

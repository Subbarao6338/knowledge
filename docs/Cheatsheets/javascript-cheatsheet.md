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

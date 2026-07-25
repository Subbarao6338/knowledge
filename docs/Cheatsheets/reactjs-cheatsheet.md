# ReactJS Cheatsheet

## 1. Functional Components & JSX

```jsx
import React, { useState, useEffect } from 'react';

export function CounterComponent({ initialCount = 0 }) {
  const [count, setCount] = useState(initialCount);

  // Effect Trigger Hook
  useEffect(() => {
    document.title = `Count: ${count}`;
    return () => {
      // Clean up phase on unmount
      document.title = "React App";
    };
  }, [count]); // Fires every time 'count' changes

  return (
    <div className="p-4 border rounded shadow">
      <h2 className="text-xl">Counter: {count}</h2>
      <button
        onClick={() => setCount(prev => prev + 1)}
        className="px-4 py-2 mt-2 bg-blue-500 text-white rounded"
      >
        Increment
      </button>
    </div>
  );
}
```

## 2. Advanced State Management (useReducer)

```jsx
import React, { useReducer } from 'react';

const initialState = { count: 0 };

function reducer(state, action) {
  switch (action.type) {
    case 'increment':
      return { count: state.count + 1 };
    case 'decrement':
      return { count: state.count - 1 };
    case 'reset':
      return { count: 0 };
    default:
      throw new Error();
  }
}

export function ReducerCounter() {
  const [state, dispatch] = useReducer(reducer, initialState);

  return (
    <>
      <h3>Reducer Count: {state.count}</h3>
      <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
    </>
  );
}
```

## 3. Custom Hooks Patterns

```jsx
import { useState, useEffect } from 'react';

export function useFetch(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;
    async function load() {
      setLoading(true);
      const res = await fetch(url);
      const json = await res.json();
      if (active) {
        setData(json);
        setLoading(false);
      }
    }
    load();
    return () => { active = false; };
  }, [url]);

  return { data, loading };
}
```

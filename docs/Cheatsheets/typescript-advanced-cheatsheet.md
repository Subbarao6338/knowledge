# Advanced TypeScript Cheatsheet

A deep-dive reference guide for advanced TypeScript concepts, type manipulation, and strict compiler-level optimizations.

---

## 1. Advanced Type Manipulation

### Conditional Types
Conditional types select one of two possible types based on a relation expressed as a type-assignment test.

```typescript
// Syntax: T extends U ? X : Y
type IsString<T> = T extends string ? true : false;

type A = IsString<string>; // true
type B = IsString<number>; // false

// Extract element type of an array (using 'infer')
type ElementType<T> = T extends (infer U)[] ? U : T;

type C = ElementType<string[]>; // string
type D = ElementType<number>;   // number
```

### Distributive Conditional Types
When conditional types act on a generic type, they become distributive when given a union type.

```typescript
type ToArray<Type> = Type extends any ? Type[] : never;
type StrArrOrNumArr = ToArray<string | number>; // string[] | number[]

// To prevent distribution, wrap the extends clauses in square brackets
type ToArrayNonDist<Type> = [Type] extends [any] ? Type[] : never;
type StrOrNumArr = ToArrayNonDist<string | number>; // (string | number)[]
```

---

## 2. Mapped Types & Key Remapping

Mapped types allow you to create new types based on another type's keys.

```typescript
type ReadonlyMapped<T> = {
  readonly [P in keyof T]: T[P];
};

type OptionalMapped<T> = {
  [P in keyof T]?: T[P];
};

// Key Remapping (TypeScript 4.1+) using 'as'
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

interface User {
  name: string;
  age: number;
}

type UserGetters = Getters<User>;
// Result:
// {
//   getName: () => string;
//   getAge: () => number;
// }
```

### Filter Keys with Key Remapping
```typescript
// Filter out keys that are not of a specific type
type FilterTypeKeys<T, ValueType> = {
  [K in keyof T as T[K] extends ValueType ? K : never]: T[K];
};

interface Profile {
  id: number;
  name: string;
  isActive: boolean;
  avatarUrl: string;
}

type StringProperties = FilterTypeKeys<Profile, string>;
// Result: { name: string; avatarUrl: string; }
```

---

## 3. Template Literal Types

Template literal types build on string literal types, and have the ability to expand into many strings via unions.

```typescript
type Direction = "left" | "right" | "up" | "down";
type Speed = "slow" | "fast";

type Movement = `${Direction}-${Speed}`;
// Result: "left-slow" | "left-fast" | "right-slow" | "right-fast" | ...

// Capitalize, Uncapitalize, Uppercase, Lowercase utilities
type UpperDirection = Uppercase<Direction>; // "LEFT" | "RIGHT" | "UP" | "DOWN"
```

---

## 4. Built-in Utility Types (Deep Dive)

TypeScript provides several global utility types to facilitate common type transformations.

| Utility Type | Syntax | Description |
| :--- | :--- | :--- |
| **Partial\<T\>** | `Partial<T>` | Makes all properties of `T` optional. |
| **Required\<T\>** | `Required<T>` | Makes all properties of `T` required. |
| **Readonly\<T\>** | `Readonly<T>` | Makes all properties of `T` readonly. |
| **Record\<K, T\>** | `Record<K, T>` | Constructs an object type with keys `K` and value type `T`. |
| **Pick\<T, K\>** | `Pick<T, K>` | Selects a subset of properties `K` from `T`. |
| **Omit\<T, K\>** | `Omit<T, K>` | Removes a subset of properties `K` from `T`. |
| **Exclude\<T, U\>** | `Exclude<T, U>` | Excludes types from `T` that are assignable to `U`. |
| **Extract\<T, U\>** | `Extract<T, U>` | Extracts types from `T` that are assignable to `U`. |
| **NonNullable\<T\>** | `NonNullable<T>` | Excludes `null` and `undefined` from `T`. |
| **Parameters\<T\>** | `Parameters<T>` | Extracts a tuple of the parameter types of a function `T`. |
| **ReturnType\<T\>** | `ReturnType<T>` | Extracts the return type of a function `T`. |

```typescript
// Custom implementation of ReturnType
type MyReturnType<T extends (...args: any) => any> = T extends (...args: any) => infer R ? R : any;
```

---

## 5. Type Guards & Type Assertions

### Custom Type Guards
A user-defined type guard is a function whose return type is a type predicate.

```typescript
interface Cat {
  meow: () => void;
}
interface Dog {
  bark: () => void;
}

function isCat(animal: Cat | Dog): animal is Cat {
  return (animal as Cat).meow !== undefined;
}

const pet: Cat | Dog = getPet();
if (isCat(pet)) {
  pet.meow(); // safe!
} else {
  pet.bark(); // compiler knows it's a Dog!
}
```

### Assertion Signatures
Assert functions verify condition inputs and throw errors if false, refining types for consecutive scopes.

```typescript
function assertIsString(val: any): asserts val is string {
  if (typeof val !== "string") {
    throw new Error("Value must be a string!");
  }
}

const input: any = "Hello World";
assertIsString(input);
console.log(input.toUpperCase()); // compiler treats 'input' as string here!
```

---

## 6. Advanced Generics & Constraints

### Recursive Types (e.g. JSON Type)
```typescript
type JSONValue =
  | string
  | number
  | boolean
  | null
  | { [key: string]: JSONValue }
  | JSONValue[];
```

### Generic Type Constraints with Defaults
```typescript
interface Lengthwise {
  length: number;
}

// T must satisfy length constraint, defaults to array of any
function logLength<T extends Lengthwise = any[]>(arg: T): void {
  console.log(arg.length);
}
```

---

## 7. Decorators (Stage 3 Standard)

Modern decorators (standardized in ECMAScript/TS 5.0+) provide a clean syntax for class and method meta-programming.

```typescript
function loggedMethod<This, Args extends any[], Return>(
  target: (this: This, ...args: Args) => Return,
  context: ClassMethodDecoratorContext<This, (this: This, ...args: Args) => Return>
) {
  const methodName = String(context.name);
  return function (this: This, ...args: Args): Return {
    console.log(`LOG: Entering method ${methodName}.`);
    const result = target.call(this, ...args);
    console.log(`LOG: Exiting method ${methodName}.`);
    return result;
  };
}

class Calculator {
  @loggedMethod
  add(a: number, b: number): number {
    return a + b;
  }
}
```

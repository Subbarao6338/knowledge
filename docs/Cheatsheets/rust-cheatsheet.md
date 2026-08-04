---
layout: default
title: "Rust Language Cheatsheet"
---

# Rust Cheatsheet

A developer reference for the Rust programming language, covering memory safety rules (ownership, borrowing, lifetimes), structures, pattern matching, error handling, traits, generics, and Cargo tools.

---

## 1. Syntax & Variable Declarations

```rust
fn main() {
    // Variables are immutable by default
    let x = 5;

    // Mutable variable
    let mut y = 10;
    y += 5;

    // Constants (always require explicit types)
    const MAX_LIMIT: u32 = 100_000;

    println!("y: {}, limit: {}", y, MAX_LIMIT);
}
```

---

## 2. Ownership & Borrowing System

Rust manages memory safety through compile-time ownership semantics instead of a garbage collector.

### Rules of Ownership
1. Each value in Rust has an owner.
2. There can only be one owner at a time.
3. When the owner goes out of scope, the value is automatically dropped (RAII).

```rust
fn ownership_demo() {
    let s1 = String::from("hello"); // s1 owns the heap allocation
    let s2 = s1; // Ownership is MOVED to s2. s1 is now invalid!

    // println!("{}", s1); // Compile Error! value used here after move

    let s3 = s2.clone(); // Deep clone, both s2 and s3 are valid
}
```

### Borrowing Rules
- You can have any number of immutable references (`&T`) to a resource.
- Or, you can have exactly **one** mutable reference (`&mut T`) to a resource at any time.
- You cannot have both at the same time in the same scope.

```rust
fn borrowing_demo() {
    let mut s = String::from("hello");

    let r1 = &s; // Immutable borrow
    let r2 = &s; // Immutable borrow
    println!("{} and {}", r1, r2); // Works fine

    // let r3 = &mut s; // Compile Error! Cannot borrow as mutable because it is already borrowed as immutable

    let r4 = &mut s; // This is allowed because previous borrows (r1, r2) are no longer used here
    r4.push_str(", world");
}
```

---

## 3. Structs and Enums

### Structures
```rust
struct User {
    username: String,
    email: String,
    active: bool,
}

// Method implementation
impl User {
    fn greet(&self) -> String {
        format!("Hello, I am {}!", self.username)
    }
}
```

### Enums and Pattern Matching
```rust
enum IpAddrKind {
    V4(u8, u8, u8, u8),
    V6(String),
}

fn route(ip: IpAddrKind) {
    match ip {
        IpAddrKind::V4(a, b, c, d) => println!("IPv4: {}.{}.{}.{}", a, b, c, d),
        IpAddrKind::V6(addr) => println!("IPv6: {}", addr),
    }
}
```

---

## 4. Error Handling

Rust does not use traditional exceptions. Instead, it uses type-safe enums.

```rust
// 1. Recoverable errors with Result<T, E>
fn divide(a: f64, b: f64) -> Result<f64, String> {
    if b == 0.0 {
        Err(String::from("Cannot divide by zero"))
    } else {
        Ok(a / b)
    }
}

// 2. Unrecoverable errors with panic!
fn fatal_error() {
    panic!("A critical internal error has occurred!");
}
```

### Propagating Errors (`?` operator)
```rust
use std::fs::File;
use std::io::{self, Read};

fn read_username_from_file() -> Result<String, io::Error> {
    let mut username = String::new();
    File::open("username.txt")?.read_to_string(&mut username)?;
    Ok(username)
}
```

---

## 5. Traits and Generics

Traits represent interfaces or shared behaviors that types can implement.

```rust
trait Summary {
    fn summarize(&self) -> String;
}

struct Article {
    title: String,
    author: String,
}

impl Summary for Article {
    fn summarize(&self) -> String {
        format!("{} by {}", self.title, self.author)
    }
}
```

---

## 6. Cargo Commands

```bash
cargo new my_app          # Create a new binary project
cargo build               # Compile project
cargo build --release     # Compile with full release optimizations
cargo run                 # Compile and run immediately
cargo test                # Execute all tests
cargo check               # Quickly analyze code for syntax errors without full compilation
cargo fmt                 # Auto-format codebase
cargo clippy              # Advanced linter for Rust best practices
```


---

## Best Practices & Production Standards

1. **Enforce Clippy rules**: Run `cargo clippy` frequently to verify memory-safety constraints and structural code quality.
2. **Utilize Pattern Matching**: Leverage exhaustive `match` syntax over Option and Result types instead of calling risky `.unwrap()` methods.
3. **Minimize Lifetime over-complications**: Design modular struct hierarchies to prevent excessively complex lifetime annotations.

---

## Common Mistakes & Antipatterns

1. **Overusing `.clone()`**: Cloning variables excessively to bypass borrow checker rules, causing high CPU/memory overhead.
2. **Using Unsafe blocks inappropriately**: Bypassing the compiler's strict type-safety guarantees with unsafe pointers.
3. **Thread Lifetime issues**: Trying to send non-`Send` or non-`Sync` references across concurrent threads.

---

## Troubleshooting & Debugging Guide

1. **Resolving Borrow Checker Conflicts**: Carefully analyze compiler errors; split mutable borrows into isolated scopes, or use interior mutability (`RefCell`, `Mutex`).
2. **Resolving Thread Boundaries**: Wrap shared structures inside `Arc` (atomic references) and lock them using thread-safe synchronization primitives.

---

## Core Interview Questions & Answers

1. **Q: Explain Rust's Ownership, Borrowing, and Lifetimes core rules.**
   - **A**: Each value has a single owner. When the owner goes out of scope, the value is dropped. You can have either one mutable borrow OR any number of immutable borrows at any time, but never both. Lifetimes are compile-time annotations ensuring references remain valid as long as they are referenced.
2. **Q: Describe the difference between `Rc` and `Arc` smart pointers.**
   - **A**: `Rc` is a reference-counted pointer for single-threaded heap allocations (cheap, not thread-safe). `Arc` is an atomic reference-counted pointer with synchronized reference increments (thread-safe, suitable for concurrent execution).

---

## Technical Architecture Diagram

```mermaid
graph LR
    Owner[Owner Var Scope] --> Borrow[Borrow: Immutable/Mutable]
    Borrow --> Release[End of Scope: Memory Reclaimed Instantly]
```

---

## Related Cheatsheets & References

- [C++ Cheatsheet](cpp-cheatsheet.md)
- [Go Cheatsheet](go-cheatsheet.md)
- [Master Directory Index](../Cheatsheets.html)
- [Knowledge Hub Portal](../Knowledge%2021cb6c26d9ba808da8d4f72eb2193ca2.html)

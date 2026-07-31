---
layout: default
title: "Swift & SwiftUI Cheatsheet"
---

# Swift & SwiftUI Cheatsheet

A highly detailed, production-ready reference guide for Apple's Swift programming language and declarative SwiftUI framework.

---

## 1. Swift Language Basics

### Variables, Constants, & Basic Types
```swift
let greeting = "Hello, World!" // Constant (immutable)
var mutableCount = 42          // Variable (mutable)

// Explicit Type Annotation
let pi: Double = 3.14159
let name: String = "Jules"
let isDeveloper: Bool = true
```

### Optionals & Unwrapping
Optionals represent a variable that can hold either a value or `nil`.
```swift
var middleName: String? = nil
middleName = "Alexander"

// 1. Optional Binding (if let / guard let)
if let actualName = middleName {
    print("Middle Name: \(actualName)")
}

func greetUser(name: String?) {
    guard let unwrappedName = name else {
        print("No name provided.")
        return
    }
    print("Welcome, \(unwrappedName)!")
}

// 2. Nil-Coalescing Operator
let displayName = middleName ?? "No Middle Name"

// 3. Optional Chaining
let count = middleName?.count
```

---

## 2. Control Flow & Patterns

### Switch & Pattern Matching
```swift
enum StatusCode {
    case success
    case clientError(Int)
    case serverError(Int)
}

let code = StatusCode.clientError(404)

switch code {
case .success:
    print("Request Succeeded")
case .clientError(let errorCode) where errorCode == 404:
    print("Not Found Error")
case .clientError(let errorCode):
    print("Client Error: \(errorCode)")
case .serverError(let errorCode):
    print("Server Error: \(errorCode)")
}
```

---

## 3. Object-Oriented & Value Types

In Swift, structs are **value types** (copied on assignment) and classes are **reference types** (shared instances).

```swift
// Struct (Value Type)
struct Point {
    var x: Double
    var y: Double

    // Mutating function is required to modify properties within structs
    mutating func moveBy(dx: Double, dy: Double) {
        x += dx
        y += dy
    }
}

// Class (Reference Type)
class User {
    var username: String

    init(username: String) {
        self.username = username
    }

    deinit {
        print("User \(username) is being deallocated.")
    }
}
```

---

## 4. Protocols & Extensions

Protocols define a blueprint of methods or properties. Extensions let you add functionality to existing types.

```swift
protocol Describable {
    var description: String { get }
    func describe()
}

extension Point: Describable {
    var description: String {
        return "Point at (\(x), \(y))"
    }

    func describe() {
        print(description)
    }
}
```

---

## 5. SwiftUI Foundations

SwiftUI is Apple's modern declarative UI framework.

```swift
import SwiftUI

struct CounterView: View {
    // State manages local mutable source of truth
    @State private var count = 0

    var body: some View {
        VStack(spacing: 20) {
            Text("Tap Count: \(count)")
                .font(.headline)
                .foregroundColor(.blue)

            Button(action: {
                count += 1
            }) {
                Text("Increment")
                    .padding()
                    .background(Color.emerald)
                    .foregroundColor(.white)
                    .cornerRadius(8)
            }
        }
        .padding()
    }
}
```

### Property Wrappers in SwiftUI
* `@State`: Used for simple local private properties owned by the current view.
* `@Binding`: Creates a two-way read-write link to a `@State` property owned by a parent view.
* `@StateObject`: Instantiates an observable object reference type (`ObservableObject`) inside a view (view owns the lifecycle).
* `@ObservedObject`: Refers to an observable object passed from outside.
* `@EnvironmentObject`: Shared data available to all child views in a hierarchy.

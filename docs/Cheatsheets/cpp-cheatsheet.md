---
layout: default
title: "C++ Cheatsheet"
---

# C++ Cheatsheet

Modern C++ (C++11, C++14, C++17, C++20, and C++23) is a highly efficient, general-purpose programming language. It offers low-level memory manipulation alongside high-level abstractions like classes, templates, and the Standard Template Library (STL).

---

## 1. Core Language & Modern Syntax

### Variables, Auto, and Initialization
```cpp
#include <iostream>
#include <vector>

int main() {
    // Uniform Initialization (braced initialization)
    int x{5};
    std::string s{"Hello C++"};
    std::vector<int> vec{1, 2, 3, 4, 5};

    // Auto Type Inference (compiler deduces type)
    auto d = 5.5;          // double
    auto flag = true;      // bool

    // Constexpr: evaluated at compile-time
    constexpr int max_limit = 100 * 2;

    // Range-based for loops
    for (const auto& item : vec) {
        std::cout << item << " ";
    }
    std::cout << "\n";
}
```

### Lambda Expressions
Lambdas provide inline, anonymous function definitions.
```cpp
// Syntax: [capture](parameters) -> return_type { body }
auto add = [](int a, int b) -> int { return a + b; };
std::cout << "Sum: " << add(10, 20) << "\n";

// Capture clauses:
// [=]  capture all local variables by value
// [&]  capture all local variables by reference
// [x, &y] capture x by value, y by reference
int multiplier = 3;
auto multiply = [multiplier](int val) { return val * multiplier; };
```

---

## 2. Object-Oriented Programming (OOP)

```cpp
#include <iostream>
#include <string>
#include <utility>

// Base class
class Animal {
protected:
    std::string name;
public:
    // Constructor with member initializer list
    explicit Animal(std::string  n) : name(std::move(n)) {}

    // Virtual destructor is critical for base classes with virtual functions!
    virtual ~Animal() = default;

    // Pure virtual function (makes class Abstract)
    virtual void make_sound() const = 0;

    // Getter
    std::string get_name() const { return name; }
};

// Derived class
class Dog : public Animal {
public:
    explicit Dog(const std::string& n) : Animal(n) {}

    // override keyword prevents typos & mismatching signatures
    void make_sound() const override {
        std::cout << name << " says: Woof!\n";
    }
};
```

---

## 3. Memory Management & Smart Pointers

Avoid raw `new` and `delete` in modern C++. Use Smart Pointers from `<memory>` to automate resource cleanup.

```cpp
#include <memory>
#include <iostream>

class Resource {
public:
    Resource() { std::cout << "Resource acquired\n"; }
    ~Resource() { std::cout << "Resource destroyed\n"; }
    void do_work() { std::cout << "Working...\n"; }
};

void smart_pointer_demo() {
    // 1. std::unique_ptr (Sole ownership, cannot be copied, only moved)
    std::unique_ptr<Resource> ptr1 = std::make_unique<Resource>();
    ptr1->do_work();

    // std::unique_ptr<Resource> ptr2 = ptr1; // ERROR: Copying is disabled
    std::unique_ptr<Resource> ptr2 = std::move(ptr1); // OK: Ownership transferred

    // 2. std::shared_ptr (Reference counted ownership)
    std::shared_ptr<Resource> sptr1 = std::make_shared<Resource>();
    {
        std::shared_ptr<Resource> sptr2 = sptr1; // Count = 2
        std::cout << "Use count: " << sptr1.use_count() << "\n";
    } // sptr2 goes out of scope, Count = 1
    std::cout << "Use count: " << sptr1.use_count() << "\n";

    // 3. std::weak_ptr (Prevents reference cycles with std::shared_ptr)
    std::weak_ptr<Resource> wptr = sptr1;
    if (auto shared = wptr.lock()) { // Safely convert to shared_ptr before use
        shared->do_work();
    }
} // sptr1 out of scope, Resource destroyed automatically
```

---

## 4. Templates & Generic Programming

Templates allow you to write functions and classes that work with any data type.

```cpp
#include <iostream>

// Function Template
template <typename T>
T find_max(T a, T b) {
    return (a > b) ? a : b;
}

// Class Template
template <typename T, int Size>
class StaticArray {
private:
    T data[Size];
public:
    void set(int index, T value) {
        if (index >= 0 && index < Size) {
            data[index] = value;
        }
    }
    T get(int index) const {
        return data[index];
    }
};

int main() {
    std::cout << find_max<int>(10, 20) << "\n";       // 20
    std::cout << find_max<double>(10.5, 3.2) << "\n"; // 10.5

    StaticArray<std::string, 5> arr;
    arr.set(0, "C++ Templates");
    std::cout << arr.get(0) << "\n";
}
```

---

## 5. Standard Template Library (STL)

### Common Containers
- **`std::vector`**: Dynamic contiguous array (prefer by default).
- **`std::list`**: Doubly-linked list.
- **`std::map`**: Red-black tree key-value store (sorted, $O(\log N)$).
- **`std::unordered_map`**: Hash-table key-value store (unsorted, $O(1)$ average).

```cpp
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <iostream>

void stl_demo() {
    // Vector
    std::vector<int> nums{4, 1, 3, 5, 2};
    nums.push_back(6);

    // Sorting algorithm from <algorithm>
    std::sort(nums.begin(), nums.end()); // 1, 2, 3, 4, 5, 6

    // Unordered Map
    std::unordered_map<std::string, int> age_map;
    age_map["Alice"] = 30;
    age_map["Bob"] = 25;

    // Iterating map
    for (const auto& [name, age] : age_map) { // Structured binding (C++17)
        std::cout << name << ": " << age << "\n";
    }
}
```

---

## 6. Modern C++ Features by Standard

### C++11
- `auto`, `nullptr`, `constexpr`, Lambdas, `std::unique_ptr`/`std::shared_ptr`, Range-based loops, Rvalue references (`&&`) and Move semantics.

### C++14
- Generic lambdas, Return type deduction for normal functions, Binary literals (`0b1010`), Digit separators (`1'000'000`).

### C++17
- Structured bindings (`auto [x, y]`), `std::filesystem`, Fold expressions, Inline variables, Nested namespaces (`namespace A::B`).

### C++20
- **Concepts**: Constraints on template parameters.
- **Ranges**: Functional pipelines (`views::filter`, `views::transform`).
- **Coroutines**: Asynchronous and lazy execution.
- **Modules**: Modern alternative to headers (`import std;`).

---

## 7. Common Gotchas & Best Practices

1. **Avoid `using namespace std;` in Header Files:** This causes namespace pollution and unexpected function resolution collisions.
2. **Pass Large Objects by Const Reference:** Prefer `void print_vector(const std::vector<int>& vec)` over passing by value to avoid expensive copies.
3. **Remember the Rule of 5:** If you define a custom Destructor, Copy Constructor, Copy Assignment, Move Constructor, or Move Assignment, you likely need to define all five.
4. **Use `override` for Virtual Overrides:** It forces the compiler to verify that the base method exists with matching parameters.

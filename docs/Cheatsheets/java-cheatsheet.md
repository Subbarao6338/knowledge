---
layout: default
title: "Java Cheatsheet"
---

# Java Cheatsheet

Java is a class-based, object-oriented, concurrent, secure, and general-purpose programming language. It follows the "Write Once, Run Anywhere" (WORA) principle via the Java Virtual Machine (JVM).

---

## 1. Core Syntax & Primitive Types

Java has 8 primitive types: `byte`, `short`, `int`, `long`, `float`, `double`, `boolean`, and `char`. All other types are reference types.

```java
public class CoreDemo {
    public static void main(String[] args) {
        // Uniform Primitive declaration
        int count = 10;
        double price = 29.99;
        boolean isActive = true;
        char grade = 'A';

        // Local Variable Type Inference (Java 10+)
        var message = "Hello from Java!";
        var list = new java.util.ArrayList<Integer>();

        // Constants (final variables)
        final double PI = 3.14159;

        // String operations
        String str = "Coded";
        String combined = str + " in Java"; // Concatenation
        int len = combined.length();
    }
}
```

---

## 2. Object-Oriented Programming (OOP)

```java
// Abstract Class representing a Base Entity
abstract class Vehicle {
    private final String brand;

    // Constructor
    protected Vehicle(String brand) {
        this.brand = brand;
    }

    // Concrete Method
    public String getBrand() {
        return brand;
    }

    // Abstract Method to override
    public abstract void startEngine();
}

// Interface for Capabilities
interface Electric {
    void chargeBattery();
}

// Derived Class implementing Interface
class Tesla extends Vehicle implements Electric {
    private int batteryLevel;

    public Tesla(String brand, int initialCharge) {
        super(brand);
        this.batteryLevel = initialCharge;
    }

    @Override
    public void startEngine() {
        System.out.println("Tesla starting silently...");
    }

    @Override
    public void chargeBattery() {
        this.batteryLevel = 100;
        System.out.println("Battery fully charged to 100%!");
    }
}
```

---

## 3. Java Collections Framework

All common data structures are standard inside the `java.util` package.

```java
import java.util.*;

public class CollectionsDemo {
    public static void main(String[] args) {
        // 1. List (Ordered, duplicates allowed)
        List<String> names = new ArrayList<>();
        names.add("Alice");
        names.add("Bob");
        names.add("Alice"); // Duplicate is OK

        // 2. Set (Unordered, unique items)
        Set<Integer> uniqueNums = new HashSet<>();
        uniqueNums.add(10);
        uniqueNums.add(20);
        uniqueNums.add(10); // Ignored automatically

        // 3. Map (Key-Value associations)
        Map<String, Integer> scoreMap = new HashMap<>();
        scoreMap.put("Alice", 95);
        scoreMap.put("Bob", 88);

        // Accessing map entries elegantly (Java 8+)
        scoreMap.forEach((name, score) -> {
            System.out.println(name + " scored: " + score);
        });
    }
}
```

---

## 4. Functional Programming & Streams (Java 8+)

The Java Streams API allows functional-style transformations over collections.

```java
import java.util.List;
import java.util.stream.Collectors;

public class StreamsDemo {
    public static void main(String[] args) {
        List<String> fruits = List.of("Apple", "Banana", "Apricot", "Blueberry", "Cherry");

        // Filter and transform lists fluently
        List<String> aFruits = fruits.stream()
                .filter(fruit -> fruit.startsWith("A")) // Select "Apple", "Apricot"
                .map(String::toUpperCase)              // Transform to "APPLE", "APRICOT"
                .collect(Collectors.toList());         // terminal operation

        System.out.println(aFruits); // [APPLE, APRICOT]
    }
}
```

---

## 5. Multi-Threading & Concurrency

### Basic Thread Creation
```java
class MyRunnable implements Runnable {
    @Override
    public void run() {
        System.out.println("Running inside: " + Thread.currentThread().getName());
    }
}

public class ThreadDemo {
    public static void main(String[] args) {
        Thread thread = new Thread(new MyRunnable());
        thread.start();
    }
}
```

### Modern Thread Pools (Executors Framework)
```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class ExecutorDemo {
    public static void main(String[] args) {
        // Create pool of 4 virtual or OS worker threads
        ExecutorService executor = Executors.newFixedThreadPool(4);

        for (int i = 0; i < 10; i++) {
            final int taskId = i;
            executor.submit(() -> {
                System.out.println("Executing task " + taskId + " on " + Thread.currentThread().getName());
            });
        }

        executor.shutdown(); // Gracefully stops accepting new tasks
    }
}
```

---

## 6. Generics

Generics ensure compile-time type safety for parameterized classes and methods.

```java
// Parameterized generic class
public class Box<T> {
    private T item;

    public void set(T item) {
        this.item = item;
    }

    public T get() {
        return item;
    }

    // Generic method
    public static <E> void printArray(E[] elements) {
        for (E element : elements) {
            System.out.print(element + " ");
        }
        System.out.println();
    }
}
```

---

## 7. Common Gotchas & Best Practices

1. **Avoid `NullPointerException` (NPE):** Use Java 8's `Optional<T>` wrapper or annotations like `@NonNull` to handle potentially absent values safely.
2. **Always override `equals()` and `hashCode()` together:** In collections like `HashSet` and `HashMap`, failing to do so will cause objects with matching fields to be treated as unique keys, resulting in duplicates.
3. **Use `StringBuilder` inside Loops:** String concatenation (`str += s`) in loops creates a brand-new `String` object on every iteration. Use `StringBuilder` to modify a single mutable buffer.
4. **Prefer `try-with-resources`:** For streams, database connections, and files, use the try-with-resources syntax to automatically close them:
   ```java
   try (var reader = new java.io.BufferedReader(new java.io.FileReader("file.txt"))) {
       System.out.println(reader.readLine());
   } catch (java.io.IOException e) {
       e.printStackTrace();
   }
   ```
5. **Understand the difference between `==` and `.equals()`:** `==` tests for reference equality (memory addresses), whereas `.equals()` tests for logical value equivalence.

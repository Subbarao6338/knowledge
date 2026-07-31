---
layout: default
title: "Kotlin & Android Cheatsheet"
---

# Kotlin & Android Cheatsheet

A highly detailed, production-ready reference guide for JetBrains Kotlin language and modern Android app development.

---

## 1. Kotlin Language Basics

### Variables & Type Safety
```kotlin
val immutableName: String = "Jules" // Read-only variable
var mutableScore: Int = 100         // Mutable variable

// Null Safety features
var nullableText: String? = null
// nullableText = "Hello"

// Safe call (?.) and Elvis Operator (?:)
val length: Int = nullableText?.length ?: 0

// Safe Cast
val number: Int? = nullableText as? Int
```

### Control Flow
```kotlin
// When expression (replaces switch)
val grade = when (mutableScore) {
    in 90..100 -> "A"
    in 80..89 -> "B"
    else -> "F"
}

// Smart Casts
fun printLength(obj: Any) {
    if (obj is String) {
        // Kotlin automatically casts obj to String within this block
        println(obj.length)
    }
}
```

---

## 2. Advanced Functions & Extensions

### Extension Functions
Add new methods to existing classes without inheriting from them.
```kotlin
fun String.isValidEmail(): Boolean {
    return this.contains("@") && this.contains(".")
}

val email = "user@example.com"
val isValid = email.isValidEmail() // returns true
```

### Scope Functions
Kotlin provides `let`, `run`, `with`, `apply`, and `also` to execute blocks of code within the context of an object.
```kotlin
val person = Person("Rao").apply {
    age = 30
    city = "New York"
}

person.let {
    println("Name: ${it.name}, Age: ${it.age}")
}
```

---

## 3. Concurrency with Coroutines

Coroutines are light-weight cooperative threads for executing asynchronous task flows.

```kotlin
import kotlinx.coroutines.*

fun main() = runBlocking {
    launch {
        delay(1000L)
        println("World!")
    }
    print("Hello, ")
}

// Suspending functions
suspend fun fetchUserData(): String = withContext(Dispatchers.IO) {
    // Network or Database simulation operation
    delay(2000L)
    "User Data"
}
```

---

## 4. Modern Android Development (Jetpack Compose)

Jetpack Compose is Android's modern declarative UI toolkit.

```kotlin
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun MainScreen() {
    var counter by remember { mutableStateOf(0) }

    Surface(
        modifier = Modifier.fillMaxSize(),
        color = MaterialTheme.colorScheme.background
    ) {
        Column(
            modifier = Modifier
                .padding(16.dp)
                .fillMaxWidth(),
            verticalArrangement = Arrangement.Center
        ) {
            Text(
                text = "Button tapped: $counter times",
                style = MaterialTheme.typography.headlineMedium
            )

            Spacer(modifier = Modifier.height(16.dp))

            Button(onClick = { counter++ }) {
                Text(text = "Tap Me")
            }
        }
    }
}
```

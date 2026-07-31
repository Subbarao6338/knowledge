---
layout: default
title: "Spring Boot Cheatsheet"
---

# Spring Boot Cheatsheet

A highly detailed, production-ready reference guide for Spring Boot backend applications and Spring Framework internals.

---

## 1. Project Initialization & Architecture

### Dependency Injection & Core Annotations
* `@SpringBootApplication`: Marks the main class, enabling auto-configuration and component scanning.
* `@Component`: Generic stereotype annotation for Spring-managed beans.
* `@Service`: Annotates service-layer beans containing business logic.
* `@Repository`: Annotates database DAO beans with automatic SQL exception translation.
* `@Autowired`: Injects a dependency (constructor injection is preferred).

```java
@Service
public class UserService {
    private final UserRepository userRepository;

    // Constructor Injection (Recommended)
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
}
```

---

## 2. REST Controller API Endpoints

```java
import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpStatus;

import java.util.List;

@RestController
@RequestMapping("/api/v1/users")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping
    public List<User> getAllUsers() {
        return userService.findAll();
    }

    @PostMapping
    public ResponseEntity<User> createUser(@RequestBody User user) {
        User savedUser = userService.save(user);
        return new ResponseEntity<>(savedUser, HttpStatus.CREATED);
    }

    @GetMapping("/{id}")
    public ResponseEntity<User> getUserById(@PathVariable Long id) {
        return userService.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }
}
```

---

## 3. Database Access with Spring Data JPA

### Repository Interfaces
```java
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    // Dynamic Query Method Derivation
    Optional<User> findByEmail(String email);

    // Custom JPQL queries
    @Query("SELECT u FROM User u WHERE u.status = 'ACTIVE'")
    List<User> findAllActiveUsers();
}
```

### Entity Mapping
```java
import jakarta.persistence.*;

@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String email;

    @Column(name = "full_name")
    private String fullName;

    // Getters, Setters, Constructors
}
```

---

## 4. Configuration & Application Properties

Spring Boot loads configuration properties from `src/main/resources/application.properties` or `application.yml`.

### YAML Configuration Example (`application.yml`)
```yaml
server:
  port: 8080
  servlet:
    context-path: /app

spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/notion_vault
    username: dev_user
    password: dev_secure_password
  jpa:
    hibernate:
      ddl-auto: update
    show-sql: true
```

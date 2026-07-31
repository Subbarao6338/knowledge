---
layout: default
title: "C# & .NET Cheatsheet"
---

# C# & .NET Cheatsheet

A highly detailed, production-ready reference guide for C# programming and Microsoft .NET backend framework.

---

## 1. C# Basic & Modern Language Features

### Variables, Pattern Matching, & Records
```csharp
// Implicit typing
var age = 30;

// Modern Pattern Matching (C# 9+)
string DescribeObject(object obj) => obj switch
{
    int i when i > 100 => "Large Integer",
    int i => "Regular Integer",
    string s => $"String of length {s.Length}",
    null => "Null reference",
    _ => "Unknown type"
};

// Records (immutable reference types with value semantics)
public record Person(string FirstName, string LastName);
```

---

## 2. LINQ (Language Integrated Query)

LINQ provides a declarative syntax for querying and manipulating data collections.

```csharp
using System.Linq;
using System.Collections.Generic;

var scores = new List<int> { 97, 92, 81, 60, 55, 90 };

// 1. Query Syntax
var highScoresQuery = from score in scores
                      where score > 80
                      orderby score descending
                      select score;

// 2. Method Syntax (Most common in production)
var highScoresMethod = scores
    .Where(score => score > 80)
    .OrderByDescending(score => score)
    .ToList();
```

---

## 3. Asynchronous Programming (async / await)

Asynchronous programming in C# is built around the Task-based Asynchronous Pattern (TAP).

```csharp
using System;
using System.Net.Http;
using System.Threading.Tasks;

public class ApiService
{
    private readonly HttpClient _httpClient = new HttpClient();

    public async Task<string> FetchDataFromEndpointAsync(string url)
    {
        try
        {
            // Non-blocking wait
            string data = await _httpClient.GetStringAsync(url);
            return data;
        }
        catch (HttpRequestException e)
        {
            Console.WriteLine($"Request failed: {e.Message}");
            throw;
        }
    }
}
```

---

## 4. ASP.NET Core Minimal APIs

Modern, lightweight way to build REST APIs in .NET 6/7/8.

```csharp
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.Hosting;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", () => "Welcome to .NET Core Portal API!");

app.MapGet("/api/users/{id}", (int id) => new { Id = id, Name = $"User {id}" });

app.Run();
```

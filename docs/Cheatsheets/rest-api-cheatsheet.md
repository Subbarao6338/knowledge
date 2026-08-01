---
layout: default
title: "REST API Design Cheatsheet"
---

# REST API Design Cheatsheet

A highly detailed, production-ready reference guide for designing elegant, robust, and industry-standard REST APIs.

---

## 1. HTTP Methods & Resource Semantics

REST APIs use standard HTTP verbs as commands to perform actions on database resources.

| HTTP Method | CRUD Action | URI / Path | Request Body | Success Status | Idempotent |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **GET** | Read | `/users` | None | 200 OK | Yes |
| **GET** | Read | `/users/{id}` | None | 200 OK | Yes |
| **POST** | Create | `/users` | Entity representation | 201 Created | No |
| **PUT** | Update (Replace) | `/users/{id}` | Full entity representation | 200 OK / 204 No Content | Yes |
| **PATCH** | Update (Partial) | `/users/{id}` | Partial entity properties | 200 OK | No |
| **DELETE** | Delete | `/users/{id}` | None | 200 OK / 204 No Content | Yes |

---

## 2. Standard HTTP Response Status Codes

Using accurate status codes helps client applications handle API responses appropriately.

### 2xx: Success
* `200 OK`: Request succeeded.
* `201 Created`: Resource was created successfully (usually returned with `Location` header).
* `204 No Content`: Request succeeded but there is no body in response (common for DELETE/PUT).

### 3xx: Redirection
* `304 Not Modified`: Client's cached copy of resource is still up-to-date (used with ETags).

### 4xx: Client Errors
* `400 Bad Request`: General client error (malformed JSON payload, validation error).
* `401 Unauthorized`: Authentication is required or has failed.
* `403 Forbidden`: Client is authenticated but lacks permission for requested resource.
* `404 Not Found`: Requested resource does not exist.
* `405 Method Not Allowed`: HTTP verb is not supported for requested URL endpoint.
* `429 Too Many Requests`: Client has exceeded rate limit thresholds.

### 5xx: Server Errors
* `500 Internal Server Error`: An unexpected error occurred on the server-side.
* `502 Bad Gateway`: Server acting as gateway received an invalid upstream response.
* `503 Service Unavailable`: Server is temporarily down for maintenance or overloaded.

---

## 3. Designing Elegant Endpoints

Endpoints should focus on **nouns** representing resources, not verbs describing actions.

* **❌ Bad (Verbs):**
  * `POST /createUser`
  * `GET /getAllUsers`
  * `POST /deleteUser?id=12`
* **✅ Good (Nouns & Hierarchical Paths):**
  * `POST /users` (Creates a user)
  * `GET /users` (Retrieves list of users)
  * `GET /users/12` (Retrieves user with ID 12)
  * `DELETE /users/12` (Deletes user 12)
  * `GET /users/12/orders` (Retrieves orders belonging to user 12)

---

## 4. Query Parameters: Filtering, Sorting, & Pagination

Use query parameters for non-resource modifiers like searching, page offsets, or sort order.

* **Filtering:** `GET /products?category=apparel&status=available`
* **Sorting:** `GET /products?sort=-price,created_at` (prefix `-` signifies descending order)
* **Pagination:** `GET /products?page=2&limit=50` (offset-based) or `GET /products?starting_after=prod_9281` (cursor-based)

---

## 5. Standard Error Payload Format

API errors should return a structured, standardized error payload containing a machine-readable code and a human-readable message.

```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "The provided request payload did not pass validation.",
    "details": [
      {
        "field": "email",
        "issue": "Must be a valid email address."
      }
    ]
  }
}
```

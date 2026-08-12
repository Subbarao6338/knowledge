---
layout: default
title: "Web Security Cheatsheet"
---

# Web Security Cheatsheet

Web Security is the practice of protecting web-facing assets, applications, servers, and data from unauthorized access, manipulation, disruption, or malware.

---

## 1. OWASP Top 10 Critical Web Vulnerabilities

The Open Web Application Security Project (OWASP) lists the most critical security risks facing web applications.

### 1. SQL Injection (SQLi)
- **Concept:** Attackers inject malicious SQL statements into input fields, manipulating backend databases to extract, modify, or delete sensitive data.
- **Prevention:** Always use parameterized queries (Prepared Statements) or Object-Relational Mappers (ORMs). Never concatenate input strings directly into SQL queries.

### 2. Cross-Site Scripting (XSS)
- **Concept:** Attackers inject malicious client-side scripts (usually JavaScript) into web pages viewed by other users.
  - *Stored XSS:* Malicious payload is stored in the database and served to users.
  - *Reflected XSS:* Payload is reflected off the web server in response queries.
  - *DOM-based XSS:* Payload is executed due to unsafe DOM manipulation.
- **Prevention:** Sanitize and html-escape user outputs; implement a strict **Content Security Policy (CSP)**.

### 3. Cross-Site Request Forgery (CSRF)
- **Concept:** Forces an authenticated user's browser to send a forged HTTP request to a vulnerable web application where the user is already authenticated.
- **Prevention:** Generate and validate anti-CSRF tokens for mutating requests; use `SameSite=Lax` or `SameSite=Strict` cookie flags.

---

## 2. Browser Security Mechanisms

Browsers implement strict policy boundaries to secure client-side execution environments.

### Content Security Policy (CSP)
An HTTP response header that declares approved resource loading origins. Minimizes XSS vulnerabilities by restricting script, image, stylesheet, and plugin sources.

```http
Content-Security-Policy: default-src 'self'; script-src 'self' https://trustedscripts.com; img-src 'self' data:;
```

### Cross-Origin Resource Sharing (CORS)
An HTTP header protocol that permits servers to specify which third-party origins can bypass the browser's default **Same-Origin Policy (SOP)** to fetch server resources.

```http
Access-Control-Allow-Origin: https://mytrustedapp.com
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
```

---

## 3. Token-Based Authentication & Cryptography

### JSON Web Tokens (JWT)
JWTs are compact, URL-safe means of representing claims to be transferred between two parties.
- **Structure:** `Header.Payload.Signature`
- **Security Rule:** Signature verification is absolutely mandatory. Always use secure, modern signing algorithms (e.g., RS256, EdDSA) instead of insecure HS255 or `none`.
- **Storage:** Avoid storing JWT access tokens in `localStorage` due to XSS vulnerability. Secure them in a `HttpOnly`, `Secure`, and `SameSite` cookie.

---

## 4. Session Management & Header Hardening

Securing sessions and using secure HTTP response headers is critical for mitigating attacks such as CSRF, Session Hijacking, Clickjacking, and MIME sniffing.

### Secure Cookie Attributes

To protect sessions against physical theft, client-side scripts, or unauthorized state transmissions, secure all session/state cookies with these vital attributes.

| Attribute | Recommended Value | Security Purpose |
| :--- | :--- | :--- |
| **HttpOnly** | `True` | Prevents client-side scripts (JavaScript) from accessing the cookie via `document.cookie`, mitigating Session Hijacking via XSS. |
| **Secure** | `True` | Restricts the cookie to encrypted (HTTPS) requests only, preventing interception over unencrypted Wi-Fi or networks. |
| **SameSite** | `Strict` or `Lax` | Controls whether cookies are sent with cross-site requests. `Strict` blocks the cookie on all cross-site navigations; `Lax` allows it on top-level safe navigations (e.g., links). Prevents CSRF. |
| **Domain** | Omit, or set to exact host | Specifies which hosts can receive the cookie. Omit to default to the exact domain (no subdomains), minimizing exposure. |
| **Path** | Specific resource path (e.g., `/api`) | Limits cookie transmission to matching sub-paths of the site. Defaults to `/`. |
| **Max-Age / Expires**| Set reasonable session expiry | Enforces cookie cleanup. Prefer `Max-Age` (in seconds) over `Expires` (absolute timestamp). |

### Production HTTP Response Header Checklist

Hardening server-side response headers is one of the easiest and most effective ways to defend an application against multiple attack vectors.

#### 1. Content Security Policy (CSP)
Declares approved resource loading sources. Restricts script execution to mitigate XSS.
```http
Content-Security-Policy: default-src 'self'; object-src 'none'; frame-ancestors 'none';
```

#### 2. HTTP Strict Transport Security (HSTS)
Forces browsers to connect via HTTPS only, protecting against SSL stripping.
```http
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
```

#### 3. X-Frame-Options
Mitigates Clickjacking by preventing the page from being rendered inside an `<iframe>` on external websites.
```http
X-Frame-Options: DENY
```

#### 4. X-Content-Type-Options
Mitigates MIME Sniffing by forcing the browser to adhere strictly to the declared content type.
```http
X-Content-Type-Options: nosniff
```

#### 5. Referrer-Policy
Controls how much referrer information is passed along with requests when navigating away.
```http
Referrer-Policy: strict-origin-when-cross-origin
```

#### 6. Permissions-Policy
Controls which browser APIs and features (e.g., camera, microphone, geolocation, payment APIs) can be accessed by the page.
```http
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

---

## Best Practices & Production Standards

1. **HTTPS Everywhere:** Force TLS 1.3 across all domains. Implement HTTP Strict Transport Security (HSTS) headers to block unencrypted connections.
2. **Secure Cookie Configuration:** Enforce flags: `HttpOnly` (blocks JS access), `Secure` (requires HTTPS), and `SameSite=Lax` (blocks CSRF cross-origin state transmission).
3. **Defense in Depth:** Never rely on a single layer of security. Enforce authentication, rate limiting, logging, web application firewalls (WAF), and perimeter network segmentation.
4. **Input Sanitization & Output Encoding:** Treat all client-supplied data as hostile. Validate schemas, enforce strict types, and encode outputs based on context (HTML, JS, URL, or CSS context).

---

## Common Mistakes & Antipatterns

1. **Hardcoding Private Secrets:** Committing API keys, database credentials, or private cryptographic keys into Git repositories.
2. **Failing to Verify Signatures:** Accepting JWTs without validating their signatures on backend routes, or allowing the `alg: "none"` header vulnerability.
3. **Permissive CORS Wildcard (`*`):** Configuring `Access-Control-Allow-Origin: *` alongside active credentials, exposing endpoint resources to third-party scripts.

---

## Troubleshooting & Debugging Guide

1. **Debugging SSL Handshake Failures:** Check server cipher suites using OpenSSL commands. Verify certificates are valid, not expired, and chain root CA correctly.
2. **Tracking Content Blocked by CSP:** Monitor browser console reports. Implement `Content-Security-Policy-Report-Only` headers to send violations to a collection endpoint without blocking active users.

---

## Core Interview Questions & Answers

1. **Q: What is the difference between Symmetric and Asymmetric Encryption?**
   - **A**: Symmetric encryption uses a single shared secret key to both encrypt and decrypt data (fast, good for large file content). Asymmetric encryption uses a public key to encrypt and a separate private key to decrypt (secure key exchange, signatures, slower).
2. **Q: Explain how OAuth 2.0 Authorization Code Flow with PKCE works.**
   - **A**: PKCE (Proof Key for Code Exchange) protects public clients from authorization code interception. The client generates a random secret (`Code Verifier`) and hashes it (`Code Challenge`). During the initial login redirect, the challenge is sent. When exchanging the auth code for a token, the client passes the raw verifier, proving identity without relying on a pre-shared client secret.

---

## Technical Architecture Diagram

```mermaid
sequenceDiagram
    participant User as Browser / User
    participant App as Client Frontend
    participant Auth as OAuth / Auth Server
    participant API as Resource Backend Server

    User->>App: Clicks Login
    App->>Auth: Redirect to Login (with PKCE Challenge)
    User->>Auth: Enters Credentials & MFA
    Auth-->>App: Redirect back with Auth Code
    App->>Auth: Exchange Auth Code + Code Verifier
    Auth->>Auth: Validate Verifier matches Challenge
    Auth-->>App: Return JWT Access & Refresh Token
    App->>API: HTTP API Request (Authorization: Bearer <Token>)
    API->>API: Validate Token Signature & Expiry
    API-->>App: Return Protected Resources JSON
```

---

## Related Cheatsheets & References

- [Master Index](../Cheatsheets.html)
- [System Design Cheatsheet](system-design-cheatsheet.md)
- [Microservices Cheatsheet](microservices-cheatsheet.md)

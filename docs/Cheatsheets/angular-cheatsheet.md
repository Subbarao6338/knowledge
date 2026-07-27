---
layout: default
title: "Angular Cheatsheet"
---

# Angular Cheatsheet (Angular 17+)

## 1. Standalone Components Architecture

Modern Angular defaults to **Standalone Components**, removing the strict dependency on `NgModule` declarations.

### Example Standalone Component
```typescript
import { Component, OnInit, signal, computed, effect } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-counter',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './counter.component.html',
  styleUrls: ['./counter.component.css']
})
export class CounterComponent implements OnInit {
  // 1. Angular Signals (Reactive State)
  count = signal<number>(0);

  // 2. Computed signal (derived state)
  doubledCount = computed(() => this.count() * 2);

  constructor() {
    // 3. Effect (side effects triggered on signal modification)
    effect(() => {
      console.log(`Current signal count is: ${this.count()}`);
    });
  }

  ngOnInit(): void {
    console.log('Standalone Counter Component Initialized!');
  }

  increment() {
    this.count.update(val => val + 1);
  }

  decrement() {
    if (this.count() > 0) {
      this.count.update(val => val - 1);
    }
  }

  reset() {
    this.count.set(0);
  }
}
```

---

## 2. Modern Block Template Syntax (Angular 17+)

Angular 17 introduced a cleaner, faster control flow syntax directly compiled inside templates, replacing `*ngIf` and `*ngFor` directives.

### Conditional Flow (`@if`)
```html
@if (isLoading) {
  <div class="spinner">Fetching server assets...</div>
} @else if (hasError) {
  <div class="alert danger">Failed to fetch data. Please retry.</div>
} @else {
  <p>Data loaded successfully!</p>
}
```

### Loop Flow (`@for`)
The new `@for` syntax has built-in optimizations and requires a unique track property.
```html
<ul>
  @for (user of users; track user.id; let idx = $index; let total = $count) {
    <li class="user-item">
      [{{ idx + 1 }}/{{ total }}] {{ user.name }} - {{ user.email }}
    </li>
  } @empty {
    <p class="placeholder-text">No active users found.</p>
  }
</ul>
```

### Switch Flow (`@switch`)
```html
@switch (userRole) {
  @case ('admin') {
    <app-admin-panel />
  }
  @case ('moderator') {
    <app-moderator-tools />
  }
  @default {
    <app-user-dashboard />
  }
}
```

---

## 3. Data & Event Binding Syntax

| Binding Type | Syntax Pattern | Code Example |
| :--- | :--- | :--- |
| **Interpolation** | `{{ value }}` | `<p>Welcome, {{ username }}!</p>` |
| **Property Binding** | `[attribute]="property"` | `<button [disabled]="isSubmitDisabled">Submit</button>` |
| **Event Binding** | `(event)="method()"` | `<button (click)="onSave($event)">Save</button>` |
| **Two-Way Binding** | `[(ngModel)]="value"` | `<input [(ngModel)]="searchQuery" placeholder="Search..." />` |
| **Class Binding** | `[class.classname]="boolean"` | `<div [class.active-tab]="selectedTab === 'details'">...</div>` |
| **Style Binding** | `[style.color]="expr"` | `<span [style.color]="hasError ? 'red' : 'green'">Status</span>` |

---

## 4. Modern Dependency Injection (DI) & Services

Angular services are classes designed to share reusable data and utilities across your application.

### Creating a Service (`user.service.ts`)
```typescript
import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface User {
  id: number;
  name: string;
  email: string;
}

@Injectable({
  providedIn: 'root' // Service is single-instance and available globally
})
export class UserService {
  private apiUrl = 'https://jsonplaceholder.typicode.com/users';

  // Using modern inject() function instead of constructor inject
  private http = inject(HttpClient);

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>(this.apiUrl);
  }

  getUserById(id: number): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/${id}`);
  }
}
```

### Injecting a Service in a Component
```typescript
import { Component, OnInit, inject, signal } from '@angular/core';
import { UserService, User } from './services/user.service';

@Component({
  selector: 'app-user-list',
  standalone: true,
  template: `
    <h3>Users</h3>
    @for (user of users(); track user.id) {
      <p>{{ user.name }} ({{ user.email }})</p>
    }
  `
})
export class UserListComponent implements OnInit {
  private userService = inject(UserService);

  users = signal<User[]>([]);

  ngOnInit() {
    this.userService.getUsers().subscribe({
      next: (data) => this.users.set(data),
      error: (err) => console.error('Failed to load users:', err)
    });
  }
}
```

---

## 5. Reactive Extensions (RxJS) Basics in Angular

RxJS is a library for composing asynchronous and event-based programs using observable sequences.

### Essential Operators Reference
```typescript
import { of, fromEvent, interval } from 'rxjs';
import { map, filter, switchMap, debounceTime, distinctUntilChanged } from 'rxjs/operators';

// 1. Transforming items (map)
const numbers$ = of(1, 2, 3).pipe(
  map(val => val * 10) // Emits: 10, 20, 30
);

// 2. Discarding items (filter)
const even$ = of(1, 2, 3, 4).pipe(
  filter(val => val % 2 === 0) // Emits: 2, 4
);

// 3. Search optimization stream
// Example: Capturing input event stream from text input
const searchInput = document.getElementById('search-box') as HTMLInputElement;

const searchStream$ = fromEvent(searchInput, 'input').pipe(
  map(event => (event.target as HTMLInputElement).value),
  debounceTime(400),              // Wait for 400ms pause in events
  distinctUntilChanged(),         // Only emit if value differs from previous
  switchMap(query => fetchSearchResultsFromServer(query)) // Switch to new search, cancel old
);
```

---

## 6. Client-Side Routing and Guards

### Route Config (`app.routes.ts`)
```typescript
import { Routes } from '@angular/router';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from './services/auth.service';

// Inline Route Auth Guard
const authGuard = () => {
  const authService = inject(AuthService);
  const router = inject(Router);

  if (authService.isLoggedIn()) {
    return true;
  }

  // Navigate to login page
  return router.parseUrl('/login');
};

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full'
  },
  {
    path: 'home',
    loadComponent: () => import('./pages/home/home.component').then(m => m.HomeComponent)
  },
  {
    path: 'admin',
    loadComponent: () => import('./pages/admin/admin.component').then(m => m.AdminComponent),
    canActivate: [authGuard] // Guard protection
  },
  {
    path: '**',
    loadComponent: () => import('./pages/not-found/not-found.component').then(m => m.NotFoundComponent)
  }
];
```

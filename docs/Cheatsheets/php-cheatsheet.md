---
layout: default
title: "PHP & Laravel Cheatsheet"
---

# PHP & Laravel Cheatsheet

A highly detailed, production-ready reference guide for PHP and the Laravel elegant web development framework.

---

## 1. PHP Core Language Basics

### OOP Essentials
```php
<?php

namespace App\Services;

interface OrderProcessorInterface {
    public function process(int $orderId): bool;
}

class StandardOrderProcessor implements OrderProcessorInterface {
    // Constructor Property Promotion (PHP 8.0+)
    public function __construct(
        protected string $apiKey,
        private bool $debug = false
    ) {}

    public function process(int $orderId): bool {
        if ($this->debug) {
            // Log details
        }
        return true;
    }
}
```

### Modern Features (PHP 8.x)
```php
// Nullsafe Operator
$country = $session?->user?->address?->country;

// Match Expression (strict typing switch replacement)
$status = match ($statusCode) {
    200, 201 => 'success',
    400, 404 => 'client_error',
    500 => 'server_error',
    default => 'unknown',
};
```

---

## 2. Laravel Routing & Controllers

### Route Definitions (`routes/web.php`)
```php
use App\Http\Controllers\UserController;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('welcome');
});

// Resourceful routes mapping to controller methods
Route::apiResource('users', UserController::class);

// Grouping with authentication middleware
Route::middleware(['auth:sanctum'])->group(function () {
    Route::post('/settings', [UserController::class, 'updateSettings']);
});
```

---

## 3. Eloquent ORM Databases

Eloquent maps database tables to PHP ActiveRecord Models.

```php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends Model
{
    // Properties that are mass-assignable
    protected $fillable = [
        'name',
        'email',
        'password',
    ];

    // Auto-hidden attributes in JSON serialization
    protected $hidden = [
        'password',
        'remember_token',
    ];

    // One-to-Many Relationship
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class);
    }
}
```

---

## 4. Querying database using Eloquent
```php
// Find user and eager-load posts
$user = User::with('posts')->where('email', 'jules@example.com')->firstOrFail();

// Database Transactions
use Illuminate\Support\Facades\DB;

DB::transaction(function () {
    DB::table('users')->update(['votes' => 1]);
    DB::table('posts')->delete();
});
```

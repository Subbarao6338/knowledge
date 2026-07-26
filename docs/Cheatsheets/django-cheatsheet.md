---
layout: default
title: "Django Cheatsheet"
---

# Django Cheatsheet

Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel.

---

## 1. Setup & Administration

```bash
pip install django
django-admin startproject myproject .
python manage.py startapp myapp
python manage.py runserver
python manage.py runserver 0.0.0.0:8000
python manage.py createsuperuser
python manage.py shell               # Interactive Django shell
```

---

## 2. Migration Commands

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations
python manage.py sqlmigrate myapp 0001  # Show SQL compiled for migration
python manage.py makemigrations --empty myapp # Create custom empty migration
```

---

## 3. Models & Fields

```python
# myapp/models.py
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
```

---

## 4. Django ORM Cheat Sheet

### Basic CRUD Operations
```python
# Create
category = Category.objects.create(name="Electronics")
product = Product(name="Phone", category=category, price=699.99, stock=50)
product.save()

# Read (Basic Queries)
all_products = Product.objects.all()
phone = Product.objects.get(id=1) # Throws error if not found / multiple found
active_products = Product.objects.filter(is_active=True)
cheap_products = Product.objects.filter(price__lt=100.00) # __lt, __lte, __gt, __gte

# Filtering with Relationships
electronics = Product.objects.filter(category__name="Electronics")

# Update & Delete
Product.objects.filter(price__lt=50.00).update(is_active=False)
product.delete()
```

### Advanced Querying: F & Q Expressions
- **`F` expressions** allow comparing model field values directly on the database level without loading them into Python memory.
- **`Q` objects** allow complex logical evaluations (`AND`, `OR`, `NOT`) inside filters.

```python
from django.db.models import F, Q

# F Expression: Increment stock for all products by 10 directly in the DB
Product.objects.all().update(stock=F('stock') + 10)

# F Expression: Find products where stock is less than a minimum threshold field
# Product.objects.filter(stock__lt=F('minimum_threshold'))

# Q Object: Find products that are active AND (price < 100 OR stock > 0)
Product.objects.filter(
    Q(is_active=True) & (Q(price__lt=100.00) | Q(stock__gt=0))
)

# Q Object with NOT (Exclude products in Electronics category)
# Product.objects.filter(~Q(category__name="Electronics"))
```

### Performance Optimization: Select Related & Prefetch Related
- **`select_related`**: Performs an SQL `JOIN` to retrieve foreign key objects in a single query (1-to-1 or Many-to-1 relationships).
- **`prefetch_related`**: Performs a separate query for many-to-many or reverse-foreign-key relationships and does the joining in Python memory.

```python
# select_related (Avoids N+1 queries when accessing product.category)
products = Product.objects.select_related('category').filter(is_active=True)
for p in products:
    print(p.category.name) # Category is already cached in memory!

# prefetch_related (Avoids N+1 queries when accessing category.products.all())
categories = Category.objects.prefetch_related('products').all()
for c in categories:
    print(c.name)
    for p in c.products.all():
        print(p.name) # Products are cached!
```

### Aggregation and Annotation
```python
from django.db.models import Avg, Max, Min, Count, Sum

# Aggregation: Get the average price across all products (returns a dict)
avg_price = Product.objects.aggregate(Avg('price'))
# {'price__avg': 349.99}

# Annotation: Add product_count as a dynamic field to each Category object
categories_with_counts = Category.objects.annotate(total_products=Count('products'))
for cat in categories_with_counts:
    print(f"{cat.name}: {cat.total_products} products")
```

---

## 5. Views & Routing

### Function-Based Views (FBVs)
```python
# myapp/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Product

def product_list(request):
    products = Product.objects.filter(is_active=True)
    return render(request, "myapp/product_list.html", {"products": products})

def product_detail_json(request, pk):
    product = get_object_or_404(Product, pk=pk)
    data = {
        "name": product.name,
        "price": str(product.price),
        "stock": product.stock,
    }
    return JsonResponse(data)
```

### Class-Based Views (CBVs)
Class-based views provide reusable, structured, object-oriented view abstractions.

```python
from django.views.generic import ListView, DetailView
from .models import Product

class ProductListView(ListView):
    model = Product
    template_name = 'myapp/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        # Override query to filter active objects
        return Product.objects.filter(is_active=True).select_related('category')
```

```python
# myproject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]
```

```python
# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('products-cbv/', views.ProductListView.as_view(), name='product_list_cbv'),
    path('api/products/<int:pk>/', views.product_detail_json, name='product_detail_json'),
]
```

---

## 6. Advanced Custom Managers

Create custom query behavior by defining a custom Manager subclass on your models.

```python
# myapp/models.py
class ActiveProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class AdvancedProduct(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    # Managers
    objects = models.Manager()               # Default manager
    active_objects = ActiveProductManager() # Custom active-only manager
```

Now you can query active products cleanly in views:
```python
# Returns only active products
active_items = AdvancedProduct.active_objects.all()
```

---

## 7. Custom Middleware

Middleware is a framework of hooks into Django’s request/response processing. It’s a light, low-level “plugin” system for globally altering Django’s input or output.

```python
# myapp/middleware.py
import time

class SimpleTimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        start_time = time.time()

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        duration = time.time() - start_time
        response["X-Page-Generation-Time-Seconds"] = str(duration)

        return response
```

Register your middleware inside `settings.py`:
```python
MIDDLEWARE = [
    # ... standard middlewares
    'myapp.middleware.SimpleTimingMiddleware',
]
```

---

## 8. Signals (Event Handling)

Django includes a “signal dispatcher” which helps decoupled applications get notified when actions occur elsewhere in the framework.

```python
# myapp/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile # assuming Profile exists

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
```

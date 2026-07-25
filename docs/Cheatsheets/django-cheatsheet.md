---
layout: default
title: "Django Cheatsheet"
---

# Django Cheatsheet

## Setup & Administration

```bash
pip install django
django-admin startproject myproject .
python manage.py startapp myapp
python manage.py runserver
python manage.py runserver 0.0.0.0:8000
```

## Migration Commands

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations
python manage.py sqlmigrate myapp 0001  # Show SQL compiled for migration
```

## Models & Fields

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

## Django ORM Cheat Sheet

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

## Views & Routing

```python
# myapp/views.py
from django.shortcuts import render, get_object_or_400_with_list
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
    path('api/products/<int:pk>/', views.product_detail_json, name='product_detail_json'),
]
```

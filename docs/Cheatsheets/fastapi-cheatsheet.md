---
layout: default
title: "FastAPI Cheatsheet"
---

# FastAPI Cheatsheet

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.8+ based on standard Python type hints.

---

## 1. Syntax Basics

```python
from fastapi import FastAPI

app = FastAPI(title="My Enterprise API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI"}
```

---

## 2. Path and Query Parameters

```python
from typing import Optional
from fastapi import Query, Path

@app.get("/items/{item_id}")
async def read_item(
    item_id: int = Path(..., description="The ID of the item to retrieve", ge=1),
    q: Optional[str] = Query(None, max_length=50, description="Search query string"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100)
):
    return {"item_id": item_id, "q": q, "skip": skip, "limit": limit}
```

---

## 3. Request Body & Pydantic v2

FastAPI uses Pydantic for data validation, serialization, and automatic OpenAPI schema generation.

```python
from pydantic import BaseModel, Field, EmailStr

class UserIn(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, examples=["johndoe"])
    email: EmailStr = Field(..., examples=["john@example.com"])
    password: str = Field(..., min_length=8)

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool = True

@app.post("/users", response_model=UserOut, status_code=201)
async def create_user(user: UserIn):
    # Process user creation here
    return {
        "id": 101,
        "username": user.username,
        "email": user.email,
        "is_active": True
    }
```

---

## 4. Dependency Injection

Dependency Injection in FastAPI is extremely powerful for database sessions, security, and authentication.

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_db():
    db = "database_connection"
    try:
        yield db
    finally:
        print("Database connection closed")

async def get_current_user(token: str = Depends(oauth2_scheme), db: str = Depends(get_db)):
    if token != "secret-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return {"username": "admin", "db": db}

@app.get("/protected-route")
async def secure_endpoint(current_user: dict = Depends(get_current_user)):
    return {"message": "You have access!", "user": current_user}
```

---

## 5. APIRouter & Modular Code Organization

For real-world projects, group endpoints using `APIRouter`.

```python
# app/routers/items.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_items():
    return [{"name": "Item 1"}, {"name": "Item 2"}]

# app/main.py
# app.include_router(items.router)
```

---

## 6. Background Tasks

Execute slow logic asynchronously after returning the HTTP response.

```python
from fastapi import BackgroundTasks

def send_welcome_email(email: str):
    # Slow email sending logic here
    print(f"Email sent to {email}")

@app.post("/register")
async def register(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_welcome_email, email)
    return {"message": "Registration complete. Welcome email will be sent shortly."}
```

---

## 7. Useful Middleware and CORS

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 8. CLI Development Commands

```bash
# Run server locally with hot-reloading
uvicorn main:app --reload --port 8000 --host 0.0.0.0

# Run in production with gunicorn + uvicorn workers
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

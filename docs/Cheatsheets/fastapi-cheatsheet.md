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

### Advanced Sub-Dependencies (Hierarchy)
FastAPI dependencies can rely on other dependencies, building a powerful dependency injection tree:

```python
async def verify_token(token: str = Depends(oauth2_scheme)):
    if not token:
         raise HTTPException(status_code=400, detail="Token missing")
    return token

async def get_active_user(token: str = Depends(verify_token)):
    # Relies on verify_token first, then fetches active user profiles
    return {"username": "sub_dep_user", "active": True}
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

---

## 9. Lifespan Events (Startup & Shutdown)

Lifespan events let you define logic that runs before the application starts up, and after it shuts down, using async context managers. This replaces the deprecated `@app.on_event("startup")` and `"shutdown"` syntax.

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load ML models, connect to database pool
    print("Application is starting up... loading models")
    db_pool = "database_pool_connection"
    yield {"db_pool": db_pool} # State passed to requests
    # Shutdown: Clean up connections, disconnect pools
    print("Application is shutting down... closing connections")

app = FastAPI(lifespan=lifespan)
```

---

## 10. Custom Exception Handlers

Register global handlers for specific exceptions to control response structures.

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class ServiceUnavailableException(Exception):
    def __init__(self, name: str):
        self.name = name

app = FastAPI()

@app.exception_handler(ServiceUnavailableException)
async def service_unavailable_handler(request: Request, exc: ServiceUnavailableException):
    return JSONResponse(
        status_code=503,
        content={"message": f"Service '{exc.name}' is temporarily unavailable. Please try again later."},
    )
```

---

## 11. Testing FastAPI with `TestClient`

Use Starlette's `TestClient` to perform request testing against your endpoints:

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

client = TestClient(app)

def test_read_main():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

---
layout: default
title: "FastAPI Advanced Cheatsheet"
---

# FastAPI Advanced Cheatsheet

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.8+ based on standard Python type hints.

---

## 1. Advanced Dependency Injection & Class Dependencies

Dependency injection in FastAPI is incredibly powerful. You can use standard functions or callable classes to manage resource Lifecycles (such as database sessions, connections, or configuration validations).

```python
from fastapi import Depends, Header, HTTPException, status
from typing import Annotated

# Class-based Dependency with state configuration
class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, x_user_role: Annotated[str, Header()] = "guest") -> str:
        if x_user_role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{x_user_role}' is not allowed to access this resource."
            )
        return x_user_role

# Instantiate reusable dependencies
admin_only = RoleChecker(["admin"])
staff_only = RoleChecker(["admin", "staff"])

# In your router endpoints:
@app.get("/admin/dashboard")
def get_admin_dashboard(current_role: Annotated[str, Depends(admin_only)]):
    return {"message": "Welcome Admin!", "active_role": current_role}
```

---

## 2. Dynamic Middleware & Event Lifecycles

Use FastAPI `lifespan` handlers to set up startup and shutdown tasks (such as starting database connections, caching engines, or background schedulers).

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
import time

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup actions on startup
    print("Initializing Database connection pool...")
    app.state.db_pool = await create_db_pool()
    yield
    # Cleanup actions on shutdown
    print("Closing Database connection pool...")
    await app.state.db_pool.close()

app = FastAPI(lifespan=lifespan)

# Custom dynamic performance timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    return response
```

---

## 3. Custom Exception Handlers

Standardize global API responses and formatting when errors occur.

```python
from fastapi import Request
from fastapi.responses import JSONResponse

class BusinessLogicException(Exception):
    def __init__(self, message: str, code: str):
        self.message = message
        self.code = code

@app.exception_handler(BusinessLogicException)
async def business_exception_handler(request: Request, exc: BusinessLogicException):
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "error": {
                "message": exc.message,
                "code": exc.code
            }
        }
    )
```

---

## 4. Advanced Response Modeling & Serialization

Control exact payload serialization, exclusion of nulls, and nested schema filtering.

```python
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr

class UserOut(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True
    avatar_url: Optional[str] = None

# Using response_model filters out password from UserIn automatically
@app.post("/users", response_model=UserOut, response_model_exclude_none=True)
async def create_user(user: UserIn) -> Any:
    # Save user...
    return user
```

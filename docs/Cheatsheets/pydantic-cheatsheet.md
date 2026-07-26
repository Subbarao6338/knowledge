---
layout: default
title: "Pydantic v2 Cheatsheet"
---

# Pydantic v2 Cheatsheet

Pydantic is the most widely used data validation and settings management library for Python. It enforces type hints at runtime, providing friendly error messages and seamless integration with standard Python types.

---

## 1. Defining Models and Fields

Inherit from `BaseModel` to define structured data objects. Fields can have default values, constraints, and custom metadata.

```python
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr

class InventoryItem(BaseModel):
    id: int
    name: str = Field(..., min_length=2, max_length=100)
    price: float = Field(..., gt=0.0, description="The price of the item must be positive")
    tags: List[str] = Field(default_factory=list)
    sku: Optional[str] = None
```

### Essential Field Arguments
| Argument | Description |
|----------|-------------|
| `...` (Ellipsis) | Marks the field as strictly **required** (no default value) |
| `default` | Set a static default value (e.g., `default="pending"`) |
| `default_factory` | Call a zero-argument function to create dynamic defaults (e.g., `default_factory=list`, `default_factory=datetime.utcnow`) |
| `gt` / `ge` | Greater Than (`>`) / Greater Than or Equal (`>=`) |
| `lt` / `le` | Less Than (`<`) / Less Than or Equal (`<=`) |
| `min_length` / `max_length` | Constraint for string lengths |
| `pattern` | Apply regular expression pattern validation (replaces `regex` in v1) |

---

## 2. Basic Model Operations

Pydantic models are simple to initialize, serialize, and validate:

```python
# Initialization (Throws ValidationError if arguments are invalid)
item = InventoryItem(id=42, name="Wireless Mouse", price=29.99, tags=["tech", "office"])

# Accessing fields
print(item.name)  # "Wireless Mouse"

# Convert to Dictionary (replaces .dict() in v1)
item_dict = item.model_dump()
# {'id': 42, 'name': 'Wireless Mouse', 'price': 29.99, 'tags': ['tech', 'office'], 'sku': None}

# Convert to JSON String (replaces .json() in v1)
item_json = item.model_dump_json()
# '{"id":42,"name":"Wireless Mouse","price":29.99,"tags":["tech","office"],"sku":null}'

# Instantiate from Python Dictionary
new_item = InventoryItem.model_validate(item_dict)

# Instantiate from JSON String
new_item = InventoryItem.model_validate_json(item_json)
```

---

## 3. Pydantic v2 Validators

Validators are custom validation functions run before or after standard parsing steps. Pydantic v2 uses `@field_validator` and `@model_validator`.

### Field Validators (`@field_validator`)
Used to validate a single field or multiple specific fields:

```python
from pydantic import BaseModel, field_validator

class UserProfile(BaseModel):
    username: str
    phone_number: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if " " in value:
            raise ValueError("Username cannot contain spaces")
        return value.lower()
```

### Model Validators (`@model_validator`)
Used to validate combinations of multiple fields or the model structure as a whole:

```python
from typing_extensions import Self
from pydantic import BaseModel, model_validator

class Promotion(BaseModel):
    discount_rate: float
    is_active: bool

    @model_validator(mode="after")
    def check_active_discount(self) -> Self:
        if self.is_active and self.discount_rate <= 0.0:
            raise ValueError("Active promotions must have a discount rate greater than 0")
        return self
```

- **`mode="after"`** (default): Runs after all fields are validated. Fields can be accessed directly as attributes (e.g. `self.discount_rate`).
- **`mode="before"`**: Runs before any field validation is performed. The input is a raw dictionary or object.

---

## 4. Handling Validation Errors

When validation fails, Pydantic raises a `ValidationError` containing precise information about what went wrong:

```python
from pydantic import BaseModel, ValidationError

class Account(BaseModel):
    id: int
    balance: float

try:
    Account(id="not-an-int", balance=-10.0)
except ValidationError as e:
    # Print readable error text
    print(e)

    # Extract structural error details as list of dicts
    errors = e.errors()
    print(errors[0])
    # {'type': 'int_parsing', 'loc': ('id',), 'msg': 'Input should be a valid integer', 'input': 'not-an-int'}
```

---

## 5. TypeAdapter (Validating Non-Model Types)

Use `TypeAdapter` to validate standard Python lists, dicts, or other types directly without wrapping them in a `BaseModel`:

```python
from typing import List
from pydantic import TypeAdapter, EmailStr

# Setup TypeAdapter for List of Emails
email_list_adapter = TypeAdapter(List[EmailStr])

raw_emails = ["alice@test.com", "bob@example.org"]

# Validates and parses the list
validated_emails = email_list_adapter.validate_python(raw_emails)

# Convert to JSON
json_data = email_list_adapter.dump_json(validated_emails)
```

---

## 6. BaseSettings (Settings Management)

To read configuration settings from environment variables or `.env` files, use the separate `pydantic-settings` package (v2 standard).

```bash
pip install pydantic-settings
```

```python
from pydantic import RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    # Field type and default values (overridden by env variables if present)
    api_key: str
    redis_url: RedisDsn = "redis://localhost:6379/0"
    debug: bool = False

    # Configuration for environment variable prefixing and .env files
    model_config = SettingsConfigDict(
        env_prefix="APP_",          # Looks for APP_API_KEY, APP_DEBUG, etc.
        env_file=".env",            # Reads from .env file
        env_file_encoding="utf-8"
    )

settings = AppSettings()
```

---

## 7. Model Configurations (`model_config`)

Pydantic v2 configures models using a class-level variable `model_config` with `ConfigDict`:

```python
from pydantic import BaseModel, ConfigDict

class SecureUser(BaseModel):
    model_config = ConfigDict(
        extra="forbid",             # Throws error if unexpected extra fields are provided
        str_strip_whitespace=True,  # Automatically strip whitespaces from all strings
        validate_assignment=True,   # Re-validate fields when they are assigned new values
        frozen=False                # If True, model becomes immutable
    )

    username: str
    email: str
```

---
layout: default
title: "Pytest Cheatsheet"
---

# Pytest Cheatsheet

`pytest` is a robust, highly extensible Python testing framework that makes it easy to write simple, readable tests, and scales to support complex functional testing for applications and libraries.

---

## 1. CLI Commands & Flags

Run tests from the terminal using various selection, filtering, and debugging options.

```bash
pytest                               # Run all tests in current directory and subdirectories
pytest test_math.py                  # Run tests in a specific file
pytest tests/unit/                   # Run tests in a specific directory
pytest test_math.py::test_add        # Run a specific test function
pytest test_math.py::TestMath::test  # Run a specific test inside a Test class
pytest -k "add or subtract"          # Run tests matching string expressions
pytest -m slow                       # Run tests decorated with @pytest.mark.slow
```

### Essential Flags
| Flag | Description |
|------|-------------|
| `-v`, `--verbose` | Increase verbosity of output |
| `-q`, `--quiet` | Decrease verbosity, show minimal output |
| `-x`, `--exitfirst` | Exit immediately upon the first failure |
| `--maxfail=N` | Stop testing after `N` failures or errors |
| `-s` | Disable stdout/stderr capturing (show standard print statements) |
| `--lf`, `--last-failed` | Only re-run the tests that failed in the last run |
| `--ff`, `--failed-first` | Run all tests, but run last failures first |
| `--tb=style` | Control traceback print style (`auto`/`long`/`short`/`no`/`line`/`native`) |
| `--durations=N` | Show the `N` slowest setup/test durations (useful for debugging slow suites) |

---

## 2. Assertion Basics

Pytest uses standard Python `assert` statements, making assertions simple and native without needing verbose helper methods.

```python
def test_assertions():
    assert 3 + 2 == 5
    assert "pytest" in "welcome to pytest"
    assert [1, 2, 3] == [1, 2, 3]
    assert {"a": 1, "b": 2} == {"b": 2, "a": 1}  # Order-insensitive dict comparison
```

### Asserting Exceptions
To assert that code raises a specific exception, use `pytest.raises` as a context manager:

```python
import pytest

def test_zero_division():
    with pytest.raises(ZeroDivisionError) as exc_info:
        1 / 0
    # Validate the exception message or metadata
    assert "division by zero" in str(exc_info.value)
```

### Asserting Approximate Numbers (Float Comparisons)
Standard float arithmetic has precision limitations. Use `pytest.approx` to compare floats cleanly:

```python
def test_floats():
    assert 0.1 + 0.2 == pytest.approx(0.3)
    assert 0.1 + 0.2 == pytest.approx(0.3, rel=1e-6)  # Custom relative tolerance
```

---

## 3. Fixtures: Dependency Injection

Fixtures provide a fixed baseline upon which tests can reliably and repeatedly execute. They are injected as function arguments.

```python
import pytest

@pytest.fixture
def sample_user():
    return {"id": 1, "name": "Alice", "role": "developer"}

def test_user_profile(sample_user):
    assert sample_user["name"] == "Alice"
    assert sample_user["role"] == "developer"
```

### Setup & Teardown (Yield Fixtures)
To run teardown code after a test completes, use `yield` instead of `return`:

```python
@pytest.fixture
def database_session():
    # Setup code runs before the test
    db = Connection()
    db.connect()
    yield db
    # Teardown code runs after the test finishes
    db.disconnect()
```

### Fixture Scopes
Fixtures can be cached and shared across different levels of the test lifecycle using the `scope` parameter:

```python
@pytest.fixture(scope="module")  # Created once per module, shared across all test files
def expensive_resource():
    return init_heavy_service()
```

- **`function`** (default): Run once per test function.
- **`class`**: Run once per test class.
- **`module`**: Run once per test file (module).
- **`package`**: Run once per Python package.
- **`session`**: Run once per entire test invocation suite.

---

## 4. Parameterization

Run a test multiple times with different datasets without duplicating test code.

```python
import pytest

@pytest.mark.parametrize(
    "inputs, expected",
    [
        ((3, 5), 8),
        ((-1, 1), 0),
        ((0, 0), 0),
        ((100, 200), 300),
    ]
)
def test_addition(inputs, expected):
    a, b = inputs
    assert a + b == expected
```

### Parameterizing Fixtures
You can also parameterize fixtures directly to execute all dependent tests against multiple environments:

```python
@pytest.fixture(params=["sqlite", "postgresql"])
def db_driver(request):
    return request.param

def test_db_queries(db_driver):
    assert db_driver in ["sqlite", "postgresql"]
```

---

## 5. Built-in Markers

Markers are decorators used to categorize tests, modify their behavior, or filter executions.

```python
import pytest
import sys

@pytest.mark.skip(reason="Legacy feature no longer supported")
def test_legacy_code():
    pass

@pytest.mark.skipif(sys.platform == "win32", reason="Does not run on Windows systems")
def test_unix_only():
    pass

@pytest.mark.xfail(reason="Bug #1043 exists in database layer")
def test_broken_feature():
    assert find_user(1) is not None
```

### Custom Markers
To organize tests by custom attributes (e.g., `slow`, `api`, `smoke`), define them and register them in your `pyproject.toml` or `pytest.ini`:

```python
# test_feature.py
@pytest.mark.slow
def test_heavy_integration():
    # some slow simulation
    pass
```

```toml
# pyproject.toml
[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "api: API layer integration tests",
]
```

---

## 6. Mocking and Monkeypatching

Mocking isolates the code under test by replacing external systems with predictable stand-ins.

### Monkeypatching Built-ins & Environment Variables
The built-in `monkeypatch` fixture simplifies temporary modifications during test runtime:

```python
def test_env_var(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    assert get_db_url() == "sqlite:///:memory:"

def test_mock_input(monkeypatch):
    # Mock system inputs
    monkeypatch.setattr("builtins.input", lambda _: "y")
    assert confirm_action() is True
```

### Pytest-Mock Extension (`mocker`)
The `pytest-mock` plugin provides a beautiful thin-wrapper around Python's standard `unittest.mock` as a fixture:

```python
# pip install pytest-mock

def test_external_api_call(mocker):
    # Mock the response of an external requests call
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"status": "success"}

    response = call_external_service()
    assert response["status"] == "success"
    mock_get.assert_called_once_with("https://api.external.com/data")
```

---

## 7. Configuration (`pytest.ini` / `pyproject.toml`)

Configure default behaviors and plugins for your test suite.

### Example `pytest.ini`
```ini
[pytest]
minversion = 7.0
addopts = -ra -q --tb=short --strict-markers
testpaths =
    tests
    integration
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

### Example `pyproject.toml`
```toml
[tool.pytest.ini_options]
minversion = "7.0"
addopts = "-ra --showlocals --tb=short"
testpaths = ["tests"]
```

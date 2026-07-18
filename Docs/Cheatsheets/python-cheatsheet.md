# Python Cheatsheet

## Basics

```python
# Variables & types
x = 5                  # int
y = 3.14                # float
s = "hello"              # str
b = True                  # bool
n = None                   # NoneType

type(x)                # <class 'int'>
isinstance(x, int)     # True

# f-strings
name = "Rao"
print(f"Hello, {name}! {1+2=}")   # Hello, Rao! 1+2=3

# Multiple assignment
a, b = 1, 2
a, b = b, a             # swap
x, *rest = [1, 2, 3, 4]  # x=1, rest=[2,3,4]
```

## Data Structures

```python
# List
lst = [1, 2, 3]
lst.append(4)
lst.extend([5, 6])
lst.insert(0, 0)
lst.pop()               # removes & returns last
lst.remove(2)            # removes first matching value
lst[::-1]                 # reversed
lst.sort(key=lambda x: -x)
sorted(lst, reverse=True)

# Tuple (immutable)
t = (1, 2, 3)

# Dict
d = {"a": 1, "b": 2}
d.get("c", 0)            # default if missing
d.setdefault("c", 0)
d.update({"d": 4})
d.keys(); d.values(); d.items()
{k: v for k, v in d.items() if v > 1}   # dict comprehension

# Set
s1 = {1, 2, 3}
s1 | {3, 4}              # union
s1 & {2, 3}               # intersection
s1 - {1}                   # difference
s1 ^ {3, 4}                 # symmetric difference

# Comprehensions
squares = [x**2 for x in range(10)]
evens = [x for x in range(10) if x % 2 == 0]
matrix_flat = [x for row in matrix for x in row]
gen = (x**2 for x in range(10))   # generator expression, lazy
```

## Control Flow

```python
if x > 0:
    ...
elif x == 0:
    ...
else:
    ...

for i, val in enumerate(lst):
    print(i, val)

for k, v in d.items():
    print(k, v)

for a, b in zip(list1, list2):
    print(a, b)

while condition:
    ...
    if stop_now:
        break
    if skip:
        continue
else:
    ...  # runs if loop completes without break

# Match statement (3.10+)
match command:
    case "start":
        ...
    case "stop" | "halt":
        ...
    case [x, y]:
        ...
    case {"key": value}:
        ...
    case _:
        ...
```

## Functions

```python
def greet(name, greeting="Hello", *args, **kwargs):
    return f"{greeting}, {name}!"

# Type hints
def add(a: int, b: int) -> int:
    return a + b

# Lambda
square = lambda x: x**2

# *args / **kwargs
def f(*args, **kwargs):
    print(args, kwargs)

# Unpacking into a call
f(*[1, 2, 3], **{"key": "val"})

# Default mutable arg trap — avoid this:
def bad(x, lst=[]):        # BAD: shared across calls
    lst.append(x)
    return lst

def good(x, lst=None):     # correct pattern
    if lst is None:
        lst = []
    lst.append(x)
    return lst

# Decorators
def timer(func):
    import time, functools
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time()-start:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    ...
```

## Classes & OOP

```python
class Animal:
    species_count = 0            # class variable

    def __init__(self, name, sound):
        self.name = name          # instance variable
        self.sound = sound
        Animal.species_count += 1

    def speak(self):
        return f"{self.name} says {self.sound}"

    def __repr__(self):
        return f"Animal({self.name!r})"

    def __eq__(self, other):
        return self.name == other.name

    @staticmethod
    def is_valid_sound(sound):
        return isinstance(sound, str)

    @classmethod
    def create_dog(cls, name):
        return cls(name, "Woof")

    @property
    def upper_name(self):
        return self.name.upper()

class Dog(Animal):                 # inheritance
    def __init__(self, name):
        super().__init__(name, "Woof")

# Dataclasses (cleaner boilerplate)
from dataclasses import dataclass, field

@dataclass
class Point:
    x: int
    y: int
    tags: list = field(default_factory=list)

p = Point(1, 2)  # __init__, __repr__, __eq__ auto-generated
```

## Error Handling

```python
try:
    risky()
except ValueError as e:
    print(f"Value error: {e}")
except (TypeError, KeyError) as e:
    print(f"Other: {e}")
else:
    print("No exception occurred")
finally:
    print("Always runs")

# Raising
raise ValueError("bad input")
raise ValueError("bad input") from original_exception

# Custom exceptions
class MyError(Exception):
    pass

# Context managers
with open("file.txt") as f:
    data = f.read()

class MyContext:
    def __enter__(self):
        print("enter")
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("exit")
        return False   # False = don't suppress exceptions

# contextlib shortcut
from contextlib import contextmanager

@contextmanager
def my_context():
    print("enter")
    yield "resource"
    print("exit")
```

## Iterators & Generators

```python
def counter(start=0):
    n = start
    while True:
        yield n
        n += 1

gen = counter()
next(gen)         # 0
next(gen)         # 1

# yield from (delegate to sub-generator)
def chain(*iterables):
    for it in iterables:
        yield from it

# Custom iterator protocol
class Countdown:
    def __init__(self, n):
        self.n = n
    def __iter__(self):
        return self
    def __next__(self):
        if self.n <= 0:
            raise StopIteration
        self.n -= 1
        return self.n + 1
```

## String Handling

```python
s = "Hello, World!"
s.lower(); s.upper(); s.strip(); s.split(",")
s.replace("Hello", "Hi")
s.startswith("Hello"); s.endswith("!")
",".join(["a", "b", "c"])
s.find("World")           # index or -1
s.format(name="Rao")
"{:.2f}".format(3.14159)  # "3.14"
f"{3.14159:.2f}"           # "3.14"
f"{42:05d}"                 # "00042"
f"{1000000:,}"                # "1,000,000"

# Regex
import re
re.match(r"^\d+$", "123")
re.search(r"\d+", "abc123")
re.findall(r"\d+", "a1b22c333")
re.sub(r"\s+", " ", "too   many   spaces")
re.split(r",\s*", "a, b,c")
pattern = re.compile(r"\d+")   # compile once, reuse
```

## File I/O

```python
with open("file.txt", "r") as f:
    text = f.read()
    lines = f.readlines()
    for line in f:
        ...

with open("out.txt", "w") as f:
    f.write("hello\n")

with open("out.txt", "a") as f:   # append
    f.write("more\n")

import json
with open("data.json") as f:
    obj = json.load(f)
json.dumps(obj, indent=2)

import csv
with open("data.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)

import pathlib
p = pathlib.Path("some/dir/file.txt")
p.exists(); p.is_file(); p.parent; p.stem; p.suffix
p.read_text(); p.write_text("content")
list(pathlib.Path(".").glob("*.py"))
```

## Standard Library Highlights

```python
from collections import Counter, defaultdict, OrderedDict, namedtuple, deque

Counter("mississippi")               # {'i': 4, 's': 4, 'p': 2, 'm': 1}
defaultdict(list)                     # auto-creates missing keys
dq = deque([1, 2, 3])
dq.appendleft(0); dq.popleft()        # O(1) both ends

Point = namedtuple("Point", ["x", "y"])
p = Point(1, 2)

import itertools
itertools.chain([1, 2], [3, 4])
itertools.combinations([1, 2, 3], 2)
itertools.permutations([1, 2, 3], 2)
itertools.product([1, 2], ["a", "b"])
itertools.groupby(sorted(data), key=lambda x: x.category)
itertools.islice(gen, 5)              # take first 5 from an iterator

import functools
functools.reduce(lambda a, b: a + b, [1, 2, 3, 4])
functools.lru_cache(maxsize=128)      # memoization decorator
functools.partial(func, arg1=val)

import datetime
now = datetime.datetime.now()
datetime.datetime.strptime("2026-07-17", "%Y-%m-%d")
now.strftime("%Y-%m-%d %H:%M:%S")
datetime.timedelta(days=7)
```

## Concurrency

```python
# Threading (good for I/O-bound work; GIL limits CPU-bound gains)
import threading
t = threading.Thread(target=func, args=(1, 2))
t.start(); t.join()

lock = threading.Lock()
with lock:
    ...  # critical section

# Multiprocessing (good for CPU-bound work; bypasses the GIL)
from multiprocessing import Pool
with Pool(4) as pool:
    results = pool.map(func, items)

# concurrent.futures (unified interface)
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
with ThreadPoolExecutor(max_workers=4) as ex:
    futures = [ex.submit(func, i) for i in items]
    results = [f.result() for f in futures]

# asyncio (single-threaded, cooperative concurrency)
import asyncio

async def fetch(url):
    await asyncio.sleep(1)
    return url

async def main():
    results = await asyncio.gather(*[fetch(u) for u in urls])
    # or with timeout:
    result = await asyncio.wait_for(fetch(url), timeout=5.0)

asyncio.run(main())
```

## Virtual Environments & Packaging

```bash
python -m venv .venv
source .venv/bin/activate          # Linux/Mac
.venv\Scripts\activate               # Windows

pip install requests
pip install -r requirements.txt
pip freeze > requirements.txt

# Modern tooling
pip install uv
uv venv
uv pip install -r requirements.txt

# pyproject.toml is the modern standard for package config
```

## Testing

```python
# pytest
def test_addition():
    assert 1 + 1 == 2

import pytest

@pytest.fixture
def sample_data():
    return [1, 2, 3]

def test_sum(sample_data):
    assert sum(sample_data) == 6

@pytest.mark.parametrize("a,b,expected", [(1,2,3), (2,3,5)])
def test_add(a, b, expected):
    assert a + b == expected

with pytest.raises(ValueError):
    int("not a number")
```

## Useful Idioms

```python
# Walrus operator (3.8+)
if (n := len(data)) > 10:
    print(f"too long: {n}")

# Ternary
result = "even" if x % 2 == 0 else "odd"

# Chained comparisons
if 0 < x < 10:
    ...

# Unpacking in function calls / assignments
first, *middle, last = [1, 2, 3, 4, 5]

# String multiplication / repetition
"-" * 40

# Enumerate with start
for i, val in enumerate(lst, start=1):
    ...

# Any / all
any(x > 5 for x in lst)
all(x > 0 for x in lst)

# Sorting with multiple keys
sorted(people, key=lambda p: (p.age, p.name))

# Type checking pattern
from typing import Optional, Union, List, Dict, Callable
def process(items: List[int], mapper: Optional[Callable] = None) -> Dict[str, int]:
    ...
```

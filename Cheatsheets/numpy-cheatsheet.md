# NumPy Cheatsheet

## Array Creation

```python
import numpy as np

np.array([1, 2, 3])
np.array([[1, 2], [3, 4]])
np.zeros((3, 4))
np.ones((2, 3))
np.full((2, 2), 7)
np.eye(3)                       # identity matrix
np.arange(0, 10, 2)              # [0,2,4,6,8]
np.linspace(0, 1, 5)              # 5 evenly spaced values between 0 and 1
np.random.rand(3, 3)               # uniform [0,1)
np.random.randn(3, 3)               # standard normal
np.random.randint(0, 10, size=(3,3))
np.random.seed(42)                   # reproducibility
np.empty((2, 2))                      # uninitialized memory (fast, garbage values)
np.diag([1, 2, 3])                     # diagonal matrix from vector
```

## Array Attributes

```python
a = np.array([[1, 2, 3], [4, 5, 6]])
a.shape        # (2, 3)
a.ndim          # 2
a.size           # 6
a.dtype           # dtype('int64')
a.itemsize          # bytes per element
a.nbytes              # total bytes
a.T                    # transpose
```

## Indexing & Slicing

```python
a = np.arange(10)
a[2]                 # 2
a[2:5]                 # [2,3,4]
a[::-1]                  # reversed
a[::2]                    # every other

m = np.arange(12).reshape(3, 4)
m[1, 2]                    # single element (row 1, col 2)
m[1, :]                      # row 1
m[:, 2]                       # column 2
m[0:2, 1:3]                     # sub-matrix

# Boolean masking
a[a > 5]
a[(a > 2) & (a < 8)]           # combine conditions with & | ~ (not and/or/not)
a[a > 5] = 0                     # conditional assignment

# Fancy indexing
a[[0, 2, 4]]                       # select specific indices
m[[0, 1], [1, 2]]                    # m[0,1] and m[1,2] — coordinate pairs

# np.where
np.where(a > 5, a, 0)                 # if>5 keep, else 0
idx = np.where(a > 5)                   # returns indices matching condition
```

## Reshaping & Combining

```python
a = np.arange(12)
a.reshape(3, 4)
a.reshape(3, -1)             # -1 infers the dimension
a.flatten()                     # returns a copy
a.ravel()                        # returns a view when possible (faster)

np.concatenate([a, b])              # along existing axis
np.vstack([a, b])                      # stack vertically (row-wise)
np.hstack([a, b])                       # stack horizontally (column-wise)
np.stack([a, b], axis=0)                 # stack along new axis

np.split(a, 3)                             # split into 3 equal parts
np.array_split(a, 3)                        # split, allows uneven parts

a[:, np.newaxis]                              # add a new axis
np.expand_dims(a, axis=0)
np.squeeze(a)                                   # remove size-1 dimensions
```

## Math Operations

```python
a + b; a - b; a * b; a / b     # element-wise
a ** 2                            # element-wise power
np.sqrt(a); np.exp(a); np.log(a); np.log2(a); np.log10(a)
np.abs(a)
np.round(a, 2)
np.floor(a); np.ceil(a)

a @ b                              # matrix multiplication
np.dot(a, b)
np.matmul(a, b)
np.linalg.inv(m)                     # matrix inverse
np.linalg.det(m)                       # determinant
np.linalg.eig(m)                         # eigenvalues/eigenvectors
np.linalg.solve(A, b)                      # solve Ax = b
np.linalg.norm(a)                            # vector norm

# Aggregations
a.sum(); a.mean(); a.std(); a.var()
a.min(); a.max(); a.argmin(); a.argmax()
a.sum(axis=0)                    # column sums (2D)
a.sum(axis=1)                      # row sums (2D)
np.cumsum(a); np.cumprod(a)
np.median(a)
np.percentile(a, 90)
```

## Broadcasting

```python
# Rules: dims are compared right-to-left; must be equal or one of them = 1
a = np.array([1, 2, 3])           # shape (3,)
b = np.array([[1], [2], [3]])      # shape (3,1)
a + b                                # broadcasts to shape (3,3)

m = np.ones((3, 4))
row = np.array([1, 2, 3, 4])         # shape (4,) broadcasts against (3,4)
m + row                                # adds row to every row of m

col = np.array([[1], [2], [3]])          # shape (3,1)
m + col                                    # adds col to every column of m
```

## Sorting & Searching

```python
a = np.array([3, 1, 4, 1, 5, 9])
np.sort(a)                     # returns sorted copy
a.sort()                          # sorts in place
np.argsort(a)                       # indices that would sort the array
np.unique(a)                          # sorted unique values
np.unique(a, return_counts=True)        # values + counts
np.searchsorted(sorted_arr, value)         # binary search insertion point
np.isin(a, [1, 5])                            # boolean membership test
np.nonzero(a)                                  # indices of nonzero elements
np.count_nonzero(a > 3)
```

## Data Types

```python
a = np.array([1, 2, 3], dtype=np.float32)
a.astype(np.int64)
np.int8, np.int16, np.int32, np.int64
np.float16, np.float32, np.float64
np.bool_
a.dtype == np.float64

np.nan                          # missing value marker for floats
np.isnan(a)
np.nan_to_num(a, nan=0.0)
np.isinf(a)
```

## Random Number Generation (modern API)

```python
rng = np.random.default_rng(seed=42)     # preferred over np.random.seed
rng.random((3, 3))                          # uniform [0,1)
rng.integers(0, 10, size=5)
rng.normal(loc=0, scale=1, size=5)
rng.choice([1, 2, 3, 4], size=3, replace=False)
rng.shuffle(a)                                 # in-place shuffle
rng.permutation(a)                               # returns shuffled copy
```

## Vectorization vs Loops

```python
# Slow: Python-level loop
result = np.empty(len(a))
for i in range(len(a)):
    result[i] = a[i] ** 2 + 1

# Fast: vectorized
result = a ** 2 + 1

# np.vectorize wraps a scalar function (still Python-level under the hood — use for convenience, not speed)
f = np.vectorize(lambda x: x**2 if x > 0 else 0)
f(a)

# For real speed on custom logic, prefer numpy ufuncs/broadcasting,
# or use numba's @njit to JIT-compile a Python loop.
```

## Views vs Copies

```python
a = np.arange(10)
b = a[2:5]           # VIEW — shares memory with a
b[0] = 99              # modifies a too!

c = a[2:5].copy()        # explicit COPY — independent memory
c[0] = 0                    # does not affect a

a.base is None              # True if a owns its data
b.base is a                   # True if b is a view into a
```

## Common Patterns

```python
# Normalize a column
normalized = (a - a.mean()) / a.std()

# Min-max scale to [0,1]
scaled = (a - a.min()) / (a.max() - a.min())

# One-hot encode integer labels
labels = np.array([0, 2, 1, 0])
one_hot = np.eye(labels.max() + 1)[labels]

# Rolling window (manual, via stride tricks)
def rolling_window(a, window):
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.sliding_window_view(a, window)  # modern, preferred

# Pairwise distance matrix
diff = a[:, np.newaxis, :] - a[np.newaxis, :, :]
dist = np.sqrt((diff ** 2).sum(axis=-1))

# Replace values conditionally
a = np.where(a < 0, 0, a)      # clip negatives to 0
np.clip(a, 0, 100)                # clip to a range directly

# Memory layout check (important for performance)
a.flags['C_CONTIGUOUS']
np.ascontiguousarray(a)
```

## Performance Tips

- Prefer vectorized operations over Python loops — NumPy's C-level loops are orders of magnitude faster.
- Avoid repeated `np.concatenate`/`np.append` in a loop (O(n²) — allocates a new array each time); preallocate an array instead.
- Use `axis=` parameters instead of manual loops over rows/columns.
- Watch for accidental type upcasting (`int` array + `float` scalar → `float` array).
- Use `np.float32` instead of `float64` when precision allows — halves memory and often speeds up computation.
- Check `.flags['C_CONTIGUOUS']` before performance-critical work; non-contiguous views (e.g., from transposes) can slow downstream operations.
- For very large arrays or out-of-core work, consider Dask arrays (same NumPy-like API, chunked/parallel execution).

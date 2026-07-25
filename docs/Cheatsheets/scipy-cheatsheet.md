# SciPy Cheatsheet

## Physical Constants & Sparse Matrices

```python
import scipy as sp
import numpy as np

# Physical constants
from scipy import constants
print(constants.pi)          # 3.141592653589793
print(constants.speed_of_light) # 299792458.0 meters/sec
print(constants.h)           # Planck constant

# Sparse matrices (efficient storage of high dimensional arrays)
from scipy import sparse
dense_arr = np.array([[1, 0, 0], [0, 0, 2], [3, 0, 0]])
sparse_csr = sparse.csr_matrix(dense_arr)  # Compressed Sparse Row (good for math)
sparse_csc = sparse.csc_matrix(dense_arr)  # Compressed Sparse Column
print(sparse_csr.toarray())  # Convert back to dense representation
```

## Integration

```python
from scipy import integrate

# Single integration of function f(x) from a to b
f = lambda x: x**2
area, error = integrate.quad(f, 0, 1)
print(f"Area: {area}, Est Error: {error}")

# Double integration of f(x, y)
f2 = lambda y, x: x*y
# Quad syntax: integrate.dblquad(func, x_min, x_max, y_min_func, y_max_func)
area2, error2 = integrate.dblquad(f2, 0, 1, lambda x: 0, lambda x: 1)
```

## Optimization

```python
from scipy import optimize

# Local minimizer of scalar function
f = lambda x: (x - 3)**2 + 10
res = optimize.minimize_scalar(f)
print(f"Minimum x: {res.x}, Minimum f(x): {res.fun}")

# Multidimensional optimization
f_multi = lambda x: (x[0] - 1)**2 + (x[1] - 2.5)**2
res_multi = optimize.minimize(f_multi, x0=[2.0, 2.0])
print(f"Optimized point: {res_multi.x}")
```

## Interpolation

```python
from scipy import interpolate

# 1D Interpolation
x = np.linspace(0, 10, 10)
y = np.sin(x)

# Linear vs Cubic Spline
f_linear = interpolate.interp1d(x, y, kind='linear')
f_cubic = interpolate.interp1d(x, y, kind='cubic')

x_new = np.linspace(0, 10, 100)
y_linear = f_linear(x_new)
y_cubic = f_cubic(x_new)
```

## Signal Processing & Fast Fourier Transform

```python
from scipy import signal
from scipy import fftpack

# Convolutions & Filtering
b, a = signal.butter(4, 0.2, 'low')  # 4th order Low-pass Butterworth filter
# Filter raw signal data
filtered_y = signal.filtfilt(b, a, y)

# Fast Fourier Transform (FFT)
sig = np.sin(2 * np.pi * 5 * x_new)  # 5 Hz wave
sig_fft = fftpack.fft(sig)
freqs = fftpack.fftfreq(len(sig_fft), d=0.1)
```

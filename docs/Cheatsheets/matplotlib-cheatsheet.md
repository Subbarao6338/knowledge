---
layout: default
title: "Matplotlib Cheatsheet"
---

# Matplotlib Cheatsheet

## Basic Line Plot

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.figure(figsize=(8, 4))
plt.plot(x, y, label="Sin(x)", color="blue", linestyle="--", linewidth=2)
plt.title("Simple Line Plot")
plt.xlabel("X Axis")
plt.ylabel("Y Axis")
plt.grid(True)
plt.legend()
plt.show()  # Display
```

## Subplots & Multi-figure layouts

```python
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(8, 6), sharex=True)

axes[0].plot(x, np.sin(x), 'r')
axes[0].set_title("Sine Wave")

axes[1].plot(x, np.cos(x), 'g')
axes[1].set_title("Cosine Wave")

plt.tight_layout() # Optimizes padding
plt.savefig("waveform_output.png", dpi=300) # Save as image file
```

## Common Chart Types

```python
# Scatter Plot
plt.scatter(x, y, marker='o', alpha=0.5, color='purple')

# Bar Plot
categories = ['A', 'B', 'C', 'D']
values = [10, 24, 18, 5]
plt.bar(categories, values, color='skyblue', edgecolor='black')

# Histogram (distribution inspection)
data = np.random.randn(1000)
plt.hist(data, bins=30, alpha=0.7, color='orange', edgecolor='white')

# Pie Chart
plt.pie([15, 30, 45, 10], labels=['Spring', 'Summer', 'Autumn', 'Winter'], autopct='%1.1f%%')
```

## Style & Presentation Configurations

```python
# Apply prebuilt styling sheets
plt.style.use('ggplot') # ggplot, seaborn-v0_8, fivethirtyeight, dark_background

# Customizing rcParams dynamically
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
```

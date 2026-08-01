---
layout: default
title: "Matplotlib Cheatsheet"
---

# Matplotlib Cheatsheet

Matplotlib is a comprehensive library for creating static, animated, and interactive visualizations in Python.

---

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

---

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

---

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

---

## Style & Presentation Configurations

```python
# Apply prebuilt styling sheets
plt.style.use('ggplot') # ggplot, seaborn-v0_8, fivethirtyeight, dark_background

# Customizing rcParams dynamically
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
```

---

## Advanced Feature: Annotations & Text Placement

Add exact labels, arrows, and highlight specific coordinates or outliers directly on the plot.

```python
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, y, color="#4f46e5", label="Active Workload")

# Point out the peak wave value
ax.annotate(
    "Peak Stress Zone",
    xy=(np.pi/2, 1.0),            # Point of interest
    xytext=(np.pi/2 + 1, 0.8),    # Position of annotation text
    arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8)
)

# Place general text box in plot coordinates
ax.text(
    6.0, -0.75,
    "Warning: Phase Shift Detected",
    style='italic',
    bbox={'facecolor': 'red', 'alpha': 0.1, 'pad': 10}
)

plt.legend(loc="upper right")
```

---

## Advanced Feature: Dual-Axis Graphing with twinx()

Plot two distinct lines with completely different datasets, measurements, or scales on a shared X-axis.

```python
fig, ax1 = plt.subplots(figsize=(8, 4))

# First Axis: CPU Load
color_cpu = '#dc2626'
ax1.set_xlabel('Timestamp (seconds)')
ax1.set_ylabel('CPU Load (%)', color=color_cpu)
line1 = ax1.plot(x, y * 50 + 50, color=color_cpu, label="CPU Load")
ax1.tick_params(axis='y', labelcolor=color_cpu)

# Second Axis: Memory usage (shares X-axis)
ax2 = ax1.twinx()
color_mem = '#2563eb'
ax2.set_ylabel('Memory Free (MB)', color=color_mem)
line2 = ax2.plot(x, (10 - x) * 200, color=color_mem, label="Memory Free", linestyle=":")
ax2.tick_params(axis='y', labelcolor=color_mem)

# Unified Legend for overlapping axes
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc="upper left")

plt.tight_layout()
```

---

## Advanced Feature: Custom Grids with GridSpec

Create layouts where some subplots span multiple rows or columns, breaking out of standard regular grids.

```python
import matplotlib.gridspec as gridspec

fig = plt.figure(figsize=(10, 8))
# Define 3x3 layout matrix
gs = gridspec.GridSpec(3, 3, figure=fig)

# Large top-left panel spanning 2 rows and 2 columns
ax_main = fig.add_subplot(gs[0:2, 0:2])
ax_main.plot(x, np.sin(x))
ax_main.set_title("Master Correlation Window")

# Sidebar panel spanning 2 rows on the far-right column
ax_side = fig.add_subplot(gs[0:2, 2])
ax_side.barh(['A', 'B', 'C'], [3, 8, 5])
ax_side.set_title("Distribution Index")

# Full-width bottom panel spanning all 3 columns
ax_bottom = fig.add_subplot(gs[2, :])
ax_bottom.scatter(x, np.random.randn(100), color="purple", alpha=0.3)
ax_bottom.set_title("Dynamic Realtime Residual Analysis")

plt.tight_layout()
```

---
layout: default
title: "Seaborn Cheatsheet"
---

# Seaborn Cheatsheet

Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics.

---

## 1. Setup & Styling

```python
import seaborn as sns
import matplotlib.pyplot as plt

# Load prebuilt theme parameters
sns.set_theme(style="darkgrid") # options: darkgrid, whitegrid, dark, white, ticks
sns.set_context("talk")         # scales label sizes: paper, notebook, talk, poster
```

---

## 2. Statistical Distributions

```python
# Histograms & KDE density lines
tips = sns.load_dataset("tips")
sns.displot(data=tips, x="total_bill", kde=True, hue="smoker", multiple="stack", height=5)

# Kernel Density Estimations (Bivariate)
sns.kdeplot(data=tips, x="total_bill", y="tip", fill=True, cmap="Blues")
```

---

## 3. Categorical & Relationship Charts

```python
# Boxplot
sns.boxplot(data=tips, x="day", y="total_bill", hue="smoker", palette="Set2")

# Violin Plot (Density curves per categorical grouping)
sns.violinplot(data=tips, x="day", y="total_bill", hue="sex", split=True)

# Scatter with regression lines
sns.lmplot(data=tips, x="total_bill", y="tip", hue="smoker", height=5)
```

---

## 4. Multi-Plot Grid Visualizations

```python
# Pairwise relationship grid
sns.pairplot(data=tips, hue="smoker", height=2.5, palette="husl")

# Heatmap for correlation matrices
corr = tips.select_dtypes('number').corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
```

---

## 5. Advanced Faceting with FacetGrid

Slice high-dimensional datasets into a grid of multiple sub-plots based on category features.

```python
# Load dataset
flights = sns.load_dataset("flights")

# Initialize the FacetGrid layout
g = sns.FacetGrid(flights, col="year", col_wrap=4, height=3)

# Map a plotting function (e.g., lineplot) to each grid cell
g.map(sns.lineplot, "month", "passengers")

# Adjust titles and axis formatting
g.set_titles("Year: {col_name}")
g.set_axis_labels("Month", "Passenger Count")
g.add_legend()
```

---

## 6. Joint Plots for Bivariate Analysis

Examine both the joint relationship between two variables and their individual univariate distributions simultaneously.

```python
# Scatter plot with histograms on margins
sns.jointplot(
    data=tips,
    x="total_bill",
    y="tip",
    kind="hex",  # options: scatter, reg, resid, kde, hex
    color="#4b5563"
)
```

---

## 7. Palette Customization & Color Systems

Seaborn features deeply integrated color mapping systems for categorical, sequential, and diverging datasets.

| Palette Type | Code / Configuration | Best Use Case |
| :--- | :--- | :--- |
| **Qualitative** | `palette="pastel"`, `palette="Set2"`, `palette="muted"` | Independent, unordered categories (e.g., Smokers vs Non-smokers). |
| **Sequential** | `palette="Blues"`, `palette="rocket"`, `palette="viridis"` | Ordered numerical intensity, where low values are light, high are dark. |
| **Diverging** | `palette="coolwarm"`, `palette="vlag"`, `palette="BrBG"` | Data with a meaningful mid-point, accenting high/low extremes. |
| **Custom** | `palette=["#3b82f6", "#10b981", "#f59e0b"]` | Exact matching of corporate or custom styling color palettes. |

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

## 2. Statistical Distributions

```python
# Histograms & KDE density lines
tips = sns.load_dataset("tips")
sns.displot(data=tips, x="total_bill", kde=True, hue="smoker", multiple="stack", height=5)

# Kernel Density Estimations (Bivariate)
sns.kdeplot(data=tips, x="total_bill", y="tip", fill=True, cmap="Blues")
```

## 3. Categorical & Relationship Charts

```python
# Boxplot
sns.boxplot(data=tips, x="day", y="total_bill", hue="smoker", palette="Set2")

# Violin Plot (Density curves per categorical grouping)
sns.violinplot(data=tips, x="day", y="total_bill", hue="sex", split=True)

# Scatter with regression lines
sns.lmplot(data=tips, x="total_bill", y="tip", hue="smoker", height=5)
```

## 4. Multi-Plot Grid Visualizations

```python
# Pairwise relationship grid
sns.pairplot(data=tips, hue="smoker", height=2.5, palette="husl")

# Heatmap for correlation matrices
corr = tips.select_dtypes('number').corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
```

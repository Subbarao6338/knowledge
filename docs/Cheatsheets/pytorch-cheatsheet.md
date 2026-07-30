---
layout: default
title: "PyTorch Cheatsheet"
---

# PyTorch Cheatsheet

PyTorch is an open-source machine learning library based on the Torch library, developed by Meta's AI Research lab. It is widely used for applications such as computer vision and natural language processing.

---

## 1. Tensor Basics & Creation

Tensors are the multi-dimensional arrays that form the core data structure in PyTorch, similar to NumPy arrays but with GPU support.

```python
import torch
import numpy as np

# Create tensor from list
t1 = torch.tensor([[1, 2], [3, 4]], dtype=torch.float32)

# Create tensor from numpy array
np_arr = np.array([5, 6, 7])
t2 = torch.from_numpy(np_arr)  # shares memory with NumPy array

# Initialize specific tensors
zeros = torch.zeros(3, 3)                # 3x3 of zeros
ones = torch.ones(2, 3)                  # 2x3 of ones
rand = torch.rand(2, 2)                  # Uniform distribution [0, 1)
randn = torch.randn(2, 2)                # Standard normal distribution
arange = torch.arange(start=0, end=10, step=2) # [0, 2, 4, 6, 8]
linspace = torch.linspace(0, 1, steps=5) # [0.0, 0.25, 0.5, 0.75, 1.0]

# Tensor attributes
print(t1.shape)  # torch.Size([2, 2])
print(t1.dtype)  # torch.float32
print(t1.device) # cpu
```

### Device Placement (GPU & Apple Silicon MPS Acceleration)
```python
# Check for availability
cuda_avail = torch.cuda.is_available()
mps_avail = torch.backends.mps.is_available()

# Determine best available device
device = torch.device("cuda" if cuda_avail else "mps" if mps_avail else "cpu")

# Move tensor to target device
x = torch.randn(3, 3).to(device)
# Alternative way
x = torch.randn(3, 3, device=device)
```

---

## 2. Tensor Operations & Manipulation

### Reshaping and View
* `view()`: Returns a new tensor with the same data but a different shape. Shared memory (requires contiguous tensor).
* `reshape()`: Similar to `view()` but handles non-contiguous tensors safely by copying if necessary.

```python
x = torch.arange(12) # Shape: [12]

# Reshape to 3x4
y = x.view(3, 4)
z = x.reshape(3, -1) # -1 infers dimension size automatically

# Transpose and Permute
t = torch.randn(2, 3, 4)
t_permuted = t.permute(2, 0, 1) # Shape: [4, 2, 3]

# Add/Remove dimensions
squeezed = torch.squeeze(torch.randn(1, 3, 1)) # Shape: [3]
unsqueezed = torch.unsqueeze(squeezed, dim=0) # Shape: [1, 3]
```

### Slicing & Mathematical Operations
```python
x = torch.randn(3, 4)

# Slicing
row_zero = x[0, :]
col_one = x[:, 1]
submatrix = x[0:2, 1:3]

# Math operations (element-wise)
a = torch.tensor([1, 2])
b = torch.tensor([3, 4])
sum_ab = a + b                     # torch.add(a, b)
prod_ab = a * b                    # torch.mul(a, b)

# Matrix Multiplication (Dot product / Matmul)
m1 = torch.randn(2, 3)
m2 = torch.randn(3, 4)
m_out = torch.matmul(m1, m2)       # Shape: [2, 4]
# Alternative shorthand:
m_out_alt = m1 @ m2
```

---

## 3. Autograd: Automatic Differentiation

Autograd is PyTorch’s automatic differentiation engine that powers neural network training.

```python
# Enable gradient tracking
x = torch.tensor([2.0, 3.0], requires_grad=True)

y = x**2 + 5*x
loss = y.sum()

# Backward pass to calculate gradients
loss.backward()

# Access gradients (dy/dx)
print(x.grad) # [2*2+5, 2*3+5] -> tensor([9.0, 11.0])

# Disable gradient calculation (useful for validation / inference)
with torch.no_grad():
    inference_result = x * 2
```

---

## 4. Building Neural Networks (`torch.nn`)

```python
import torch.nn as nn
import torch.nn.functional as F

class SimpleClassifier(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(SimpleClassifier, self).__init__()

        # Define Layers
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        # Forward propagation path
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out

# Instantiate model
model = SimpleClassifier(input_dim=10, hidden_dim=32, output_dim=2)
```

### Sequential API (For simple stacks)
```python
seq_model = nn.Sequential(
    nn.Linear(10, 32),
    nn.ReLU(),
    nn.Linear(32, 2)
)
```

---

## 5. Datasets & DataLoaders

PyTorch provides standard APIs for loading and batching dataset instances.

```python
from torch.utils.data import Dataset, DataLoader

# 1. Custom Dataset implementation
class CustomSyntheticDataset(Dataset):
    def __init__(self, num_samples=100, features_dim=10):
        self.X = torch.randn(num_samples, features_dim)
        self.y = torch.randint(0, 2, (num_samples,))

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

# 2. Instantiate and wrap with DataLoader
dataset = CustomSyntheticDataset()
dataloader = DataLoader(dataset, batch_size=16, shuffle=True, num_workers=0)

# Iterate through batches
for batch_X, batch_y in dataloader:
    print("Batch shape:", batch_X.shape, batch_y.shape)
    break
```

---

## 6. Model Training Loop

A typical training loop in PyTorch handles loss computation, gradient derivation, and weight optimizations.

```python
import torch.optim as optim

# Instantiate Model, Loss Function, and Optimizer
model = SimpleClassifier(10, 16, 2).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
num_epochs = 5
model.train() # Set model to training mode

for epoch in range(num_epochs):
    epoch_loss = 0.0
    for batch_X, batch_y in dataloader:
        batch_X, batch_y = batch_X.to(device), batch_y.to(device)

        # 1. Zero out gradients from previous iteration
        optimizer.zero_grad()

        # 2. Forward pass
        predictions = model(batch_X)
        loss = criterion(predictions, batch_y)

        # 3. Backward pass (backpropagation)
        loss.backward()

        # 4. Update model parameters (weights)
        optimizer.step()

        epoch_loss += loss.item() * batch_X.size(0)

    avg_loss = epoch_loss / len(dataset)
    print(f"Epoch {epoch+1}/{num_epochs} - Loss: {avg_loss:.4f}")
```

---

## 7. Saving & Loading Models

```python
# 1. Save state dictionary (Best Practice)
torch.save(model.state_dict(), "model_weights.pth")

# 2. Load state dictionary
loaded_model = SimpleClassifier(10, 16, 2)
loaded_model.load_state_dict(torch.load("model_weights.pth"))
loaded_model.eval() # Always set to evaluation mode for inference

# 3. Save entire model structure (Alternative)
torch.save(model, "entire_model.pth")
loaded_entire_model = torch.load("entire_model.pth")
```

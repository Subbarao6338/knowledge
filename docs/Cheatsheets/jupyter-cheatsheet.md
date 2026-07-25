# Jupyter Cheatsheet

## Launching & Interfaces

```bash
pip install notebook jupyterlab
jupyter notebook                  # classic interface
jupyter lab                          # modern interface (recommended)
jupyter lab --no-browser --port 8888     # for remote/headless servers
jupyter notebook --generate-config          # create config file for customization

jupyter kernelspec list               # list available kernels
python -m ipykernel install --user --name myenv --display-name "Python (myenv)"   # register a venv as a kernel

jupyter --version
jupyter --paths                   # show config/data/runtime directories
```

## Cell Types

```text
Code cell     — executes as code in the notebook's kernel language
Markdown cell — renders as formatted text (standard Markdown syntax)
Raw cell      — passed through unmodified during export, not executed or rendered
```

## Essential Keyboard Shortcuts

**Command mode (press Esc to enter, cell border is blue):**

| Shortcut | Action |
|---|---|
| `A` | Insert cell above |
| `B` | Insert cell below |
| `D D` | Delete cell (press D twice) |
| `Z` | Undo cell deletion |
| `M` | Convert cell to Markdown |
| `Y` | Convert cell to code |
| `Shift+M` | Merge selected cells |
| `C` / `V` / `X` | Copy / paste / cut cell |
| `Enter` | Enter edit mode |
| `↑` / `↓` | Move selection between cells |
| `Shift+↑/↓` | Select multiple cells |
| `L` | Toggle line numbers |
| `O` | Toggle cell output |
| `I I` | Interrupt kernel (press I twice) |
| `0 0` | Restart kernel (press 0 twice) |
| `H` | Show all keyboard shortcuts |

**Edit mode (press Enter to enter, cell border is green):**

| Shortcut | Action |
|---|---|
| `Shift+Enter` | Run cell, select next cell |
| `Ctrl+Enter` | Run cell, stay on same cell |
| `Alt+Enter` | Run cell, insert new cell below |
| `Ctrl+/` (or `Cmd+/`) | Toggle comment on line |
| `Tab` | Code completion / indent |
| `Shift+Tab` | Show docstring/function signature (tooltip) |
| `Ctrl+Shift+-` | Split cell at cursor |
| `Esc` | Return to command mode |

## Magic Commands (line: `%`, cell: `%%`)

```python
%lsmagic                     # list all available magic commands

# Timing
%time result = my_function()          # time a single statement
%timeit my_function()                    # run multiple times, report best/avg timing
%%time                                       # time the whole cell
%%timeit
my_function()

# Debugging
%debug                     # drop into pdb at the point of the last exception
%pdb on                       # auto-launch debugger on any exception
%%debug                          # debug the whole cell

# Variables & environment
%who                    # list all variables in the namespace
%whos                       # same, with type and value details
%reset                          # clear all variables
%env                                # show environment variables
%env MY_VAR=value                      # set an environment variable
%pwd                                       # current working directory
%cd path/to/dir                               # change directory

# Running external code
%run script.py                # run an external Python script in the notebook's namespace
%load script.py                   # load a script's content into the current cell
%%writefile myfile.py                # write cell contents to a file

# Shell commands
!ls -la                     # run any shell command, prefixed with !
!pip install package
files = !ls *.csv               # capture shell output into a Python variable

# Plotting
%matplotlib inline          # render matplotlib plots inline (classic)
%matplotlib widget              # interactive plots (with ipympl installed)

# Cell magics for other languages (with the right kernel/extension installed)
%%bash
echo "runs as a bash script"

%%html
<b>Rendered as HTML</b>

%%javascript
console.log("runs in the browser");

%%sql
SELECT * FROM my_table LIMIT 10;

# Profiling
%prun my_function()          # profile a function call, show time per function
%%prun
my_function()

%load_ext line_profiler
%lprun -f my_function my_function()      # line-by-line profiling (needs line_profiler)

%load_ext memory_profiler
%memit my_function()                        # memory usage profiling

# Autoreload — pick up changes to imported local modules without restarting the kernel
%load_ext autoreload
%autoreload 2
```

## Display & Rich Output

```python
from IPython.display import display, HTML, Markdown, Image, JSON, Latex, Video, Audio, clear_output

display(df)                       # rich display (used implicitly for the last expression in a cell)
display(HTML("<h1>Title</h1>"))
display(Markdown("**bold text**"))
display(Image(filename="plot.png"))
display(JSON({"key": "value"}))
display(Latex(r"$E = mc^2$"))

clear_output(wait=True)              # clear cell output, useful in loops with live updates

# Multiple outputs per cell (not just the last expression)
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

# Progress bars
from tqdm.notebook import tqdm
for i in tqdm(range(100)):
    ...
```

## Working with DataFrames

```python
import pandas as pd
pd.set_option("display.max_columns", None)      # show all columns
pd.set_option("display.max_rows", 100)
pd.set_option("display.width", None)

df                     # last line of a cell auto-displays (rich HTML table)
df.head()                 # shows nicely in Jupyter without print()

# Interactive widgets for exploring data
import ipywidgets as widgets
from ipywidgets import interact

@interact(x=(0, 10))
def show(x=5):
    print(x ** 2)
```

## Widgets (ipywidgets)

```python
import ipywidgets as widgets
from IPython.display import display

slider = widgets.IntSlider(min=0, max=100, value=50)
display(slider)

dropdown = widgets.Dropdown(options=["a", "b", "c"], value="a")
display(dropdown)

button = widgets.Button(description="Click me")
output = widgets.Output()

def on_click(b):
    with output:
        print("Button clicked!")

button.on_click(on_click)
display(button, output)

@widgets.interact(x=(0, 10), y=(0, 10))
def add(x=1, y=1):
    print(x + y)
```

## Notebook File Format (.ipynb)

```json
{
  "cells": [
    {
      "cell_type": "code",
      "source": ["print('hello')"],
      "outputs": [],
      "execution_count": 1,
      "metadata": {}
    }
  ],
  "metadata": {
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 5
}
```

`.ipynb` is JSON under the hood — each cell stores its source, outputs, and execution count, which is why notebooks diff poorly in git (outputs and execution counts change even without logic changes).

## Command-Line Tools (nbconvert, nbstripout)

```bash
jupyter nbconvert --to script notebook.ipynb          # export to a .py file
jupyter nbconvert --to html notebook.ipynb                # export to HTML
jupyter nbconvert --to pdf notebook.ipynb                    # export to PDF (needs LaTeX installed)
jupyter nbconvert --to markdown notebook.ipynb                  # export to Markdown
jupyter nbconvert --execute --to notebook notebook.ipynb            # run all cells, save output in place
jupyter nbconvert --execute --to notebook --inplace notebook.ipynb      # same, overwrite original file
jupyter nbconvert --clear-output notebook.ipynb                            # strip all outputs

# Keep notebooks clean in git — strip outputs before commit
pip install nbstripout
nbstripout --install              # auto-strips output on every git commit via a filter
```

## JupyterLab Extensions & Config

```bash
jupyter labextension list
pip install jupyterlab-git             # git integration panel
pip install jupyterlab-lsp                # language server (better autocomplete/linting)

jupyter lab --generate-config
# Edit ~/.jupyter/jupyter_lab_config.py for server-level settings (port, password, allowed origins, etc.)

jupyter server list                # list running Jupyter servers + tokens
jupyter server stop <port>            # stop a specific running server
```

## Remote / Server Usage

```bash
jupyter lab --no-browser --port=8888 --ip=0.0.0.0
# then SSH tunnel from your local machine:
ssh -L 8888:localhost:8888 user@remote-host

jupyter notebook password          # set a persistent password instead of using tokens
```

## Common Gotchas

- Cell execution order is NOT the same as cell position — running cells out of order changes variable state; "Restart & Run All" is the only way to guarantee a clean, reproducible execution order.
- `.ipynb` files store outputs and execution counts as part of the file — this bloats git diffs and can leak sensitive output data if committed; strip outputs before committing (`nbstripout`) or store notebooks output-free.
- `%autoreload 2` doesn't catch every kind of code change (e.g., changes to class definitions of already-instantiated objects) — a kernel restart is sometimes still necessary.
- Global namespace pollution — long-running notebooks accumulate variables across many cells, which can mask bugs that would surface in a clean linear script; periodically "Restart & Run All" to catch these.
- `!pip install` inside a notebook installs into whatever kernel/environment the notebook is currently using — this can silently differ from what you expect if multiple Python environments are present; prefer `%pip install` (magic version), which is kernel-aware.

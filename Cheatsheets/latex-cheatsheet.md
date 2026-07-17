# LaTeX Cheatsheet

## Document Structure

```latex
\documentclass[12pt, a4paper]{article}   % article, report, book, beamer, letter...

\usepackage[utf8]{inputenc}
\usepackage{amsmath, amssymb}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage[margin=1in]{geometry}

\title{My Document}
\author{Subbarao}
\date{\today}

\begin{document}

\maketitle
\tableofcontents

\section{Introduction}
Content here.

\end{document}
```

## Sectioning

```latex
\part{Part Title}
\chapter{Chapter Title}          % book/report only
\section{Section Title}
\subsection{Subsection Title}
\subsubsection{Subsubsection Title}
\paragraph{Paragraph Title}
\subparagraph{Subparagraph Title}

\section*{Unnumbered Section}      % * suppresses numbering
```

## Text Formatting

```latex
\textbf{bold text}
\textit{italic text}
\underline{underlined text}
\texttt{monospace/code text}
\emph{emphasized text}          % context-sensitive italics
\textsc{small caps}
\textsf{sans-serif text}

{\large larger text}
{\small smaller text}
{\Huge huge text}
% Size scale: \tiny \scriptsize \footnotesize \small \normalsize \large \Large \LARGE \huge \Huge

\newline or \\                       % line break
\par                                    % new paragraph
\noindent                                 % suppress paragraph indent
```

## Lists

```latex
\begin{itemize}
  \item First bullet
  \item Second bullet
  \begin{itemize}
    \item Nested bullet
  \end{itemize}
\end{itemize}

\begin{enumerate}
  \item First item
  \item Second item
\end{enumerate}

\begin{description}
  \item[Term] Definition text
  \item[Another Term] More definition
\end{description}
```

## Math Mode

```latex
Inline math: $x^2 + y^2 = z^2$
Also inline: \(x^2 + y^2\)

Display math:
$$x^2 + y^2 = z^2$$

\[
x^2 + y^2 = z^2
\]

\begin{equation}
E = mc^2
\label{eq:einstein}
\end{equation}

% Reference an equation
As shown in Equation \ref{eq:einstein}...

\begin{align}
a &= b + c \\
  &= d + e
\end{align}
```

### Common Math Symbols & Structures

```latex
\frac{a}{b}                    % fraction
\sqrt{x}                          % square root
\sqrt[n]{x}                          % nth root
x^{2}                                    % superscript
x_{i}                                       % subscript
\sum_{i=1}^{n} x_i                             % summation
\prod_{i=1}^{n} x_i                               % product
\int_{a}^{b} f(x)\,dx                                % integral
\lim_{x \to \infty} f(x)                                % limit
\partial                                                   % partial derivative symbol
\nabla                                                        % nabla/gradient

\alpha \beta \gamma \delta \epsilon \theta \lambda \mu \pi \sigma \phi \omega
\Gamma \Delta \Theta \Lambda \Sigma \Phi \Omega             % capital greek letters

\leq \geq \neq \approx \equiv \pm \times \div \cdot
\infty \forall \exists \in \notin \subset \subseteq \cup \cap
\rightarrow \Rightarrow \leftrightarrow \Leftrightarrow

\begin{matrix} a & b \\ c & d \end{matrix}
\begin{pmatrix} a & b \\ c & d \end{pmatrix}    % with parentheses
\begin{bmatrix} a & b \\ c & d \end{bmatrix}       % with brackets
\begin{vmatrix} a & b \\ c & d \end{vmatrix}          % with vertical bars (determinant)

\overrightarrow{AB}                # vector notation
\hat{x}                                 % hat/unit vector
\bar{x}                                    % bar (mean)
\dot{x}                                       % derivative dot notation
\vec{v}                                          % arrow vector
```

## Tables

```latex
\begin{table}[h]
\centering
\caption{My Table}
\label{tab:mytable}
\begin{tabular}{|l|c|r|}
\hline
Left & Center & Right \\
\hline
a & b & c \\
d & e & f \\
\hline
\end{tabular}
\end{table}

% Column specifiers: l (left), c (center), r (right), p{width} (wrapped paragraph)
% | inserts vertical rules between columns

% Reference a table
See Table \ref{tab:mytable}.
```

## Figures & Images

```latex
\begin{figure}[h]
\centering
\includegraphics[width=0.8\textwidth]{image.png}
\caption{My Figure Caption}
\label{fig:myfigure}
\end{figure}

% Placement specifiers: h (here), t (top), b (bottom), p (own page), ! (override LaTeX's preference)

See Figure \ref{fig:myfigure}.
```

## References & Citations

```latex
\usepackage{hyperref}
\usepackage[backend=biber, style=numeric]{biblatex}
\addbibresource{references.bib}

% In text
As shown by \cite{smith2020}...
\textcite{smith2020} argued that...

% At the end of the document
\printbibliography

% Cross-references within the document
\label{sec:intro}
See Section \ref{sec:intro} on page \pageref{sec:intro}.
```

```bibtex
% references.bib
@article{smith2020,
  author  = {Smith, John},
  title   = {A Great Paper},
  journal = {Journal of Examples},
  year    = {2020},
  volume  = {1},
  pages   = {1--10},
}
```

## Environments

```latex
\begin{center} centered content \end{center}
\begin{flushleft} left-aligned \end{flushleft}
\begin{flushright} right-aligned \end{flushright}

\begin{quote} short quotation \end{quote}
\begin{quotation} longer, multi-paragraph quotation \end{quotation}
\begin{verbatim}
Code or literal text, no LaTeX processing applied
\end{verbatim}

\begin{abstract}
Summary of the document.
\end{abstract}
```

## Code Listings

```latex
\usepackage{listings}

\begin{lstlisting}[language=Python, caption=Example Code]
def hello():
    print("Hello, world!")
\end{lstlisting}

% Or, for nicer syntax highlighting:
\usepackage{minted}
\begin{minted}{python}
def hello():
    print("Hello, world!")
\end{minted}
```

## Custom Commands & Macros

```latex
\newcommand{\mynote}[1]{\textbf{Note:} #1}
\mynote{This is a reusable macro.}

\newcommand{\R}{\mathbb{R}}       % shorthand for real number symbol
$x \in \R$

\renewcommand{\ttdefault}{cmtt}      % redefine an existing command

\newenvironment{myenv}{\begin{quote}\itshape}{\end{quote}}
\begin{myenv} Custom environment content \end{myenv}
```

## Page Layout & Formatting

```latex
\usepackage[margin=1in]{geometry}
\usepackage{setspace}
\doublespacing
\onehalfspacing
\singlespacing

\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhead[L]{Left Header}
\fancyfoot[C]{\thepage}

\newpage
\clearpage
\pagebreak

\usepackage{titlesec}         % customize section heading styles
```

## Common Packages

| Package | Purpose |
|---|---|
| `amsmath`, `amssymb` | Extended math typesetting and symbols |
| `graphicx` | Include images |
| `hyperref` | Clickable links, PDF metadata, cross-reference links |
| `geometry` | Page margins/layout |
| `babel` | Language/localization support |
| `biblatex` / `natbib` | Bibliography management |
| `listings` / `minted` | Code syntax highlighting |
| `tikz` | Vector graphics and diagrams |
| `booktabs` | Professional-looking table rules |
| `xcolor` | Color support |
| `float` | Better control over figure/table placement |
| `caption` | Customize figure/table caption styling |

## TikZ Quick Example (diagrams)

```latex
\usepackage{tikz}

\begin{tikzpicture}
\draw[thick, ->] (0,0) -- (2,0) node[right] {x};
\draw[thick, ->] (0,0) -- (0,2) node[above] {y};
\draw[blue, thick] (0,0) circle (1cm);
\node at (1,1) {Label};
\end{tikzpicture}
```

## Compiling

```bash
pdflatex document.tex             # standard compilation -> document.pdf
xelatex document.tex                 # better Unicode/font support
lualatex document.tex                   # modern engine, Lua scripting support

# With bibliography (run multiple passes to resolve references)
pdflatex document.tex
biber document                    # or: bibtex document
pdflatex document.tex
pdflatex document.tex

latexmk -pdf document.tex          # automates the multi-pass build process
```

## Common Gotchas

- Special characters need escaping: `# $ % & _ { } ~ ^ \` — use `\#`, `\$`, `\%`, `\&`, `\_`, `\{`, `\}`, `\textasciitilde{}`, `\textasciicircum{}`, `\textbackslash{}`.
- Cross-references (`\ref`, `\pageref`, `\cite`) require **two compilation passes** (sometimes three, plus a bibliography tool run) to resolve correctly.
- Figures/tables with `[h]` placement are only a *suggestion* — LaTeX may float them elsewhere; use `[H]` (capital, requires the `float` package) to force exact placement.
- Blank lines create new paragraphs — a single line break is just whitespace and does NOT start a new line in the output.
- Math mode and text mode are strict — text inside `$...$` needs `\text{...}` (from `amsmath`) to render as normal (non-italic, spaced) text.

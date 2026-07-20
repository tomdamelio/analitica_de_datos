# Colab / Jupyter component recipes

Every resource the notebook uses, as a copy-ready recipe. These are the Colab equivalents of the marimo
components the style was developed with. Read the recipe you need, adapt the content, keep the pattern.

## Contents

- [Setup cell](#setup-cell)
- [Branding CSS](#branding-css)
- [Markdown and LaTeX](#markdown-and-latex)
- [Styled callouts](#styled-callouts)
- [KPI stat tiles](#kpi-stat-tiles)
- [Static figures (matplotlib)](#static-figures-matplotlib)
- [Interactive figures (ipywidgets)](#interactive-figures-ipywidgets)
- [Hover charts (plotly)](#hover-charts-plotly)
- [Predict-then-reveal and worked-solution reveals](#predict-then-reveal-and-worked-solution-reveals)
- [Tabs and accordions](#tabs-and-accordions)
- [Mermaid / concept diagrams](#mermaid--concept-diagrams)
- [Quiz with running score](#quiz-with-running-score)
- [Verification asserts](#verification-asserts)
- [Colab forms and hiding code](#colab-forms-and-hiding-code)

## Setup cell

One code cell, run first. In Colab, enabling the custom widget manager makes ipywidgets render reliably.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats as st
import ipywidgets as W
from IPython.display import HTML, Markdown, Latex, display

# Colab only: makes ipywidgets render after a page reload. Harmless in classic Jupyter.
try:
    from google.colab import output as _colab_output
    _colab_output.enable_custom_widget_manager()
except Exception:
    pass

# Semantic palette (swap the primary for another institution; keep the roles).
COL = {
    "primary": "#00529B",  # institutional blue; main series/trace
    "accent":  "#C0492F",  # terracotta; the contrasting second line
    "good":    "#1F7A4D",  # green; correct / converged
    "bad":     "#B4232E",  # red; wrong / diverging
    "muted":   "#7E9EBB",  # muted blue; secondary geometry
    "ink":     "#122535",  # navy; text and axes
    "grey":    "#9FB0BD",  # blue-grey; gridlines, de-emphasis
}
plt.rcParams.update({
    "figure.dpi": 120, "figure.figsize": (7, 4),
    "axes.edgecolor": COL["ink"], "axes.labelcolor": COL["ink"],
    "text.color": COL["ink"], "xtick.color": COL["ink"], "ytick.color": COL["ink"],
    "axes.spines.top": False, "axes.spines.right": False,
    "font.size": 11,
})
```

## Branding CSS

One code cell, code hidden, run once. Fonts load from Google Fonts (Colab has network access). Swap the two
font names and the primary colour for another institution. Do not style `.katex` / MathJax; let the math
render in its own font.

```python
display(HTML(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Work+Sans:wght@400;600&family=Amiri:wght@400;700&display=swap');
.rendered_html, .markdown, .cell .text_cell_render { font-family:'Work Sans',system-ui,sans-serif; color:#122535; }
.rendered_html h1,.rendered_html h2,.rendered_html h3 { font-family:'Amiri',Georgia,serif; color:#00529B; }
.rendered_html h2 { border-bottom:2px solid #00529B; padding-bottom:.2em; }
.rendered_html a { color:#00529B; }
.rendered_html table th { background:#00529B; color:#fff; }
.rendered_html h1,.rendered_html h2,.rendered_html h3 { scroll-margin-top:16px; }
</style>
"""))
```

## Markdown and LaTeX

Prose lives in markdown cells. Inline math is `$...$`, displayed math `$$...$$`; both render through MathJax
in Colab and Jupyter. From code, `display(Markdown(...))` and `display(Latex(...))` render dynamic text. Do
not build LaTeX with f-strings that contain literal braces; use plain concatenation or `.format` carefully,
or better, keep LaTeX in static markdown cells and only compute the numbers.

## Styled callouts

Colored admonition boxes for learning goals, key ideas, and pitfalls. Define one helper, reuse it. This is
the equivalent of marimo's `mo.callout`.

```python
def callout(body_md, kind="info", title=None):
    palette = {
        "info":    ("#00529B", "#eaf1f8"),
        "success": ("#1F7A4D", "#e8f3ec"),
        "warn":    ("#B4232E", "#fbeceb"),  # misconceptions / pitfalls
        "neutral": ("#7E9EBB", "#eef2f6"),
    }
    edge, bg = palette.get(kind, palette["info"])
    head = f'<div style="font-weight:600;color:{edge};margin-bottom:.3em">{title}</div>' if title else ""
    return HTML(f'<div style="border-left:4px solid {edge};background:{bg};'
                f'padding:.7em 1em;border-radius:4px;margin:.6em 0">{head}{body_md}</div>')

display(callout("Probability in the continuous world is <b>area</b>, not height.",
                kind="warn", title="Common trap"))
```

Reserve `warn` for the misconception callouts (the "students usually get this wrong" boxes), `success` for
learning-goal recaps, `info` for key definitions.

## KPI stat tiles

Small headline-number tiles (mean, variance, a probability), the equivalent of `mo.stat`.

```python
def stat_tiles(items):  # items: list of (label, value, caption)
    cells = "".join(
        f'<div style="flex:1;min-width:120px;border:1px solid #9FB0BD;border-radius:8px;'
        f'padding:.6em .9em;margin:.3em">'
        f'<div style="font-size:.8em;color:#7E9EBB">{lab}</div>'
        f'<div style="font-size:1.5em;font-weight:600;color:#00529B">{val}</div>'
        f'<div style="font-size:.75em;color:#7E9EBB">{cap}</div></div>'
        for lab, val, cap in items)
    return HTML(f'<div style="display:flex;flex-wrap:wrap">{cells}</div>')

display(stat_tiles([("Mean", "1/λ", "expected wait"),
                    ("Variance", "1/λ²", "spread"),
                    ("P(X>t)", "e^(-λt)", "survival")]))
```

## Static figures (matplotlib)

The default for anything illustrative. Title states the takeaway, not the mechanics. Use the semantic
palette. Small multiples via `plt.subplots(1, k)`.

```python
x = np.linspace(0, 6, 400)
for lam, c in [(0.5, COL["muted"]), (1.0, COL["primary"]), (2.0, COL["accent"])]:
    plt.plot(x, lam*np.exp(-lam*x), color=c, label=f"λ = {lam}")
plt.title("Larger rate means faster decay and a shorter wait")
plt.xlabel("x"); plt.ylabel("density f(x)"); plt.legend()
plt.show()
```

## Interactive figures (ipywidgets)

The workhorse for interactivity: a slider (or dropdown) that recomputes and redraws. Use
`interactive_output` so the controls and the plot lay out cleanly, and clear the axes each redraw rather
than stacking. This replaces marimo's reactive slider-driven cells.

```python
def _draw(n):
    lam = 4.0
    k = np.arange(0, 16)
    plt.figure(figsize=(7, 4))
    plt.bar(k, st.binom(n, lam/n).pmf(k), color=COL["muted"], label=f"Binomial(n={n}, p=λ/n)")
    plt.plot(k, st.poisson(lam).pmf(k), "o-", color=COL["accent"], label="Poisson(λ=4)")
    plt.title("As n grows the Binomial converges to the Poisson")
    plt.xlabel("k"); plt.ylabel("probability"); plt.legend(); plt.show()

n_slider = W.IntSlider(value=10, min=4, max=1000, step=1, description="n",
                       continuous_update=False)
display(W.VBox([n_slider, W.interactive_output(_draw, {"n": n_slider})]))
```

Notes that keep widgets robust:
- `continuous_update=False` redraws on release, not on every pixel; much smoother for heavier plots.
- Guard parameter ranges so no cell can produce nan (for example keep `n >= lam` so `p = lam/n <= 1`).
- One idea per widget. A slider that changes three things at once teaches nothing.

For a pure predict-then-reveal button, `W.Button` with an `on_click` that fills an `W.Output` works well.

## Hover charts (plotly)

When the teaching point is reading exact values off a curve, plotly's hover beats a static figure. Renders
natively in Colab.

```python
import plotly.graph_objects as go
x = np.linspace(-4, 4, 200)
fig = go.Figure(go.Scatter(x=x, y=st.norm.pdf(x), mode="lines",
                           line=dict(color=COL["primary"])))
fig.update_layout(title="Standard normal density (hover to read f(x))",
                  template="simple_white", height=380)
fig.show()
```

Use plotly sparingly; it is heavier than matplotlib and its interactivity only earns its place when reading
precise values or panning a wide range is the point.

## Predict-then-reveal and worked-solution reveals

Pure HTML `<details>` in a markdown cell: no widgets, no runtime, always works, and collapses on load so the
reader commits to a prediction first.

```markdown
**Predict.** Before running the next cell: does doubling n halve the standard deviation of the sample mean?

<details><summary>Show the answer</summary>

No. The variance of the mean is $\sigma^2/n$, so the standard deviation is $\sigma/\sqrt{n}$. Doubling $n$
divides the standard deviation by $\sqrt{2}$, not by 2.

</details>
```

Use the same pattern for problem-set solutions: problem visible, solution behind the fold.

## Tabs and accordions

For parallel content (three distributions side by side, or optional depth), `ipywidgets.Tab` and
`ipywidgets.Accordion` mirror marimo's tabs/accordion.

```python
tab = W.Tab(children=[W.HTML("<b>Uniform</b>: flat on [a,b]"),
                      W.HTML("<b>Normal</b>: the bell"),
                      W.HTML("<b>Exponential</b>: memoryless wait")])
for i, t in enumerate(["Uniform", "Normal", "Exponential"]):
    tab.set_title(i, t)
display(tab)
```

For static optional depth without widgets, nested markdown `<details>` also works and is lighter.

## Mermaid / concept diagrams

Concept maps help, but Colab has no native mermaid. Two good options:

1. **Static image via mermaid.ink** (no dependency, renders anywhere): base64-encode the diagram source and
   display the returned PNG.

   ```python
   import base64
   graph = "graph LR; A[Sample space]-->B[Random variable]-->C[CDF]-->D[Density]-->E[Moments]"
   url = "https://mermaid.ink/img/" + base64.urlsafe_b64encode(graph.encode()).decode()
   display(HTML(f'<img src="{url}" style="max-width:100%">'))
   ```

2. **graphviz** (pre-installed in Colab) for flow/box diagrams you build in Python:

   ```python
   import graphviz
   g = graphviz.Digraph(graph_attr={"rankdir": "LR"})
   for a, b in [("PMF", "CDF"), ("CDF", "PDF"), ("PDF", "moments")]:
       g.edge(a, b)
   display(g)
   ```

Keep diagrams to one clear spine; they orient, they do not decorate.

## Quiz with running score

A short cumulative self-check. Radio buttons per question, a check button that tallies. Keep it light.

```python
Q = [("Var of the sample mean of n i.i.d. draws?", ["σ²", "σ²/n", "σ/√n"], 1),
     ("In the continuous world, P(X = x) equals?", ["f(x)", "0", "1"], 1)]
widgets_q = [W.RadioButtons(options=[o for o in opts], description=f"Q{i+1}",
                            style={"description_width": "initial"}, value=None)
             for i, (_, opts, _) in enumerate(Q)]
out = W.Output()
for (stem, _, _), w in zip(Q, widgets_q):
    display(W.HTML(f"<b>{stem}</b>")); display(w)
def _score(_):
    s = sum(1 for (_, opts, ans), w in zip(Q, widgets_q)
            if w.value == opts[ans])
    with out:
        out.clear_output(); print(f"Score: {s} / {len(Q)}")
btn = W.Button(description="Check", button_style="primary")
btn.on_click(_score)
display(btn, out)
```

## Verification asserts

Every worked number is checked against an independent computation. This is non-negotiable: it makes the page
trustworthy and catches your own errors on run-all. Prefer an independent method for the check, not a copy of
the same expression.

```python
from fractions import Fraction as Fr

# Exact: mean of Binomial(8, 1/2) is n*p = 4
n, p = 8, Fr(1, 2)
assert n * p == 4

# Numeric: variance of Exponential(λ=2) is 1/λ^2, checked against scipy and a Monte Carlo estimate
lam = 2.0
assert np.isclose(st.expon(scale=1/lam).var(), 1/lam**2)
rng = np.random.default_rng(0)
assert np.isclose(st.expon(scale=1/lam).rvs(200_000, random_state=rng).var(),
                  1/lam**2, atol=0.02)
```

For symbolic identities use `sympy` (`sp.simplify(lhs - rhs) == 0`); Colab has it pre-installed. numpy 2.x
renamed `np.trapz` to `np.trapezoid`, so use `np.trapezoid` for numeric integrals.

## Colab forms and hiding code

To keep the page clean, collapse setup and plotting code into titled forms. In Colab, a first line of
`#@title Some label {display-mode:"form"}` hides the code and shows only the label plus output. Colab form
fields let a value become a control without ipywidgets:

```python
#@title Explore the rate  {display-mode:"form"}
lam = 1.5 #@param {type:"slider", min:0.2, max:3, step:0.1}
x = np.linspace(0, 6, 300)
plt.plot(x, lam*np.exp(-lam*x), color=COL["primary"])
plt.title(f"Exponential density, rate λ = {lam}"); plt.show()
```

Colab forms are the lightest interactivity (no widget runtime), but they only exist in Colab, not classic
Jupyter, and they rerun the whole cell on change. Use ipywidgets when the notebook must also work outside
Colab, or when one control drives a redraw without recomputing everything.

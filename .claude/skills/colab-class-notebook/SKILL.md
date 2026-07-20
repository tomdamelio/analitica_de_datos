---
name: colab-class-notebook
description: >-
  Generate a polished, interactive Google Colab or Jupyter class-notebook (.ipynb) that turns lecture
  notes, class material, a topic, or a set of exercises into self-explanatory study material. Produces a
  notebook with a deliberate structure (institutional header, clickable table of contents, a "where this
  class sits in the programme" bridge, a one-line thread, numbered sections with numerically verified
  worked examples, interactive labs interleaved right after their section, a problem set, and a one-screen
  cheat-sheet appendix), a curated mix of interactive (ipywidgets, plotly) and static (matplotlib)
  resources, swappable institutional branding, and a hand-authored style with no em dashes and no
  AI-authorship traces. Use this skill whenever the user wants to build a teaching or study notebook,
  turn a lecture or notes into an interactive explainer, make a Colab/Jupyter notebook for a class or
  course, or create interactive study material with widgets, sliders, plots, quizzes or worked examples,
  even if they do not say the words "skill" or "Colab" explicitly.
---

# Colab class-notebook builder

Build an `.ipynb` that a student experiences as excellent: clear enough that the prose alone teaches, and
interactive enough that moving a control builds intuition no static page can. This skill encodes a specific
content structure, an interactivity philosophy, a visual system, and a verification discipline that have
been refined across many notebooks. It is topic-agnostic: the same skeleton works for probability, calculus,
biology, economics, or anything else.

Colab and Jupyter run real Python on a server, so unlike browser-only runtimes there is **no load-time
penalty** for heavy libraries: use `numpy`, `scipy`, `sympy`, `matplotlib`, `plotly`, and `ipywidgets`
freely. The tradeoff to manage is **cognitive and visual**, not computational: too many live widgets clutter
the page and slow the reader down. So interactivity is added deliberately, not everywhere.

## The workflow

1. **Gather and decide.** Read the source (lecture notes, transcript, slides, exercises). Settle the
   branding (institution name, one primary colour, heading + body fonts, optional logo) and the section
   map. Do not ask the user things you can infer or default sensibly; only stop on a real fork (for example
   "one notebook or split into two?").
2. **Scaffold the structure.** Lay out the cells in the canonical order (see `references/structure.md`):
   header, table of contents, programme bridge, thread, then the numbered sections with their interleaved
   labs, then the problem set and appendix. Write markdown cells for prose and code cells for figures,
   verification, and widgets.
3. **Fill each section.** Prose in the inside-out style (name every symbol, add a "where" list after each
   displayed formula). Every worked number is **verified with an assert**. Add a figure. Add interactivity
   **only where it teaches a concrete point** (see the interactivity policy below).
4. **Run all and polish.** Execute the whole notebook top to bottom (`jupyter nbconvert --to notebook
   --execute` for a headless check, or "Runtime -> Run all" in Colab). Fix every error and failed assert
   until it runs clean. Then reread for the style rules (no dashes, no AI traces) and visual consistency.

## The canonical structure

Header -> table of contents (clickable) -> "Where this class sits in the programme" -> "Today's thread"
-> Section 1 -> ... -> Section k (each numbered section immediately followed by its interactive lab where
one is warranted) -> cumulative self-check quiz -> problem set with worked solutions -> one-screen
cheat-sheet appendix. The full per-cell template, including exact markdown for the header, TOC and bridge,
is in **`references/structure.md`**. Read it before scaffolding.

The single most important structural choice: **interleave the labs**. Put each interactive lab right after
the section it belongs to, not in a separate "labs" part at the end. A student learns the idea and plays
with it while it is fresh; that tight loop is what active-learning research favours. Only a cumulative quiz
belongs at the very end.

## The interactivity policy (read this before adding any widget)

Aim for a **mix**: a few genuinely interactive resources placed where exploration teaches, and clean static
figures everywhere else. Before adding any widget or hover chart, ask two questions:

1. Does it show a concrete point that a static figure cannot?
2. Is that point already covered by one of the interactive labs?

Add interactivity only if the answer is yes to (1) and no to (2). When in doubt, keep it static. Do not do
blanket "make everything interactive" passes: every live widget adds visual clutter and a moment of lag, so
they must earn their place. A good notebook has a handful of interactive moments in the body plus the
interactive labs, and static figures for everything illustrative.

The interactivity toolkit (ipywidgets sliders/dropdowns that recompute and redraw, plotly for hover, HTML
`<details>` for predict-then-reveal and worked-solution reveals) is in **`references/components.md`**.

## Hard style rules

These are not stylistic preferences to weigh; they are requirements the reader will notice.

- **No em dashes or en dashes anywhere** (prose, figure titles, comments). Use a colon for a definition, a
  comma for an aside, a semicolon to join clauses, or a plain hyphen for compound names. The reader treats
  a dash as a tell of machine writing, so avoid it entirely.
- **No traces of AI or LLM authorship.** Write as a human author. No "as an AI", no "generated by", no
  self-referential meta commentary, and delete any auto-generated assistant artifacts the tooling leaves
  behind.
- **Verify every worked number.** Each computed result carries an `assert` (exact algebra with `sympy` or
  `fractions`, numeric checks with `numpy`/`scipy` and `np.isclose`/`np.allclose`). The asserts are the
  safety net that lets a reader trust the page; they also catch your own mistakes when you run all.
- **Inside-out prose.** Introduce each object in words, then its symbol; after every displayed formula, a
  short "where" list naming each symbol. This is what makes the prose teach on its own.

The full pedagogy, prose, and visual-design guidance (semantic colour, KPI stat tiles, small multiples,
callout taxonomy, worked-example scaffolding, colourblind-safe figures) is in **`references/style.md`**.

## Branding

Default to a swappable institutional theme, injected once at the top of the notebook with a `display(HTML)`
CSS cell. The reference default is Universidad de San Andres (UdeSA): primary blue `#00529B`, navy ink
`#122535`, headings in a serif (Amiri) and body in Work Sans. Swap the one primary colour, the two fonts,
and the logo for any other institution; keep the rest. The exact CSS cell and a semantic colour palette are
in `references/components.md` and `references/style.md`.

## Reference files

- `references/structure.md` — the full cell-by-cell notebook skeleton with copy-ready markdown for the
  header, TOC, programme bridge, thread, section template, quiz, and appendix. Read before scaffolding.
- `references/components.md` — Colab/Jupyter recipes for every resource: markdown + LaTeX, styled callouts,
  KPI stat tiles, ipywidgets interactive figures, plotly hover charts, matplotlib static figures, mermaid
  diagrams, tabs and accordions, predict-then-reveal, the verification-assert pattern, branding CSS, and
  collapsing code with Colab forms. Read when building any cell.
- `references/style.md` — pedagogy (active learning, explorable explanations), the interactivity policy in
  depth, prose conventions, and the visual-design system. Read when writing prose or designing figures.

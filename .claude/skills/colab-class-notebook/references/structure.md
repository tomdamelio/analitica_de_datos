# Notebook structure: the cell-by-cell skeleton

This is the canonical order. Build the notebook by laying these cells out first, then filling each one.
Markdown cells carry prose; code cells carry figures, verification, and widgets. In Colab a code cell can
be collapsed into a titled form with `#@title`, which hides the code and shows only its output, keeping the
page clean.

Cell order:

```
[md]   0. Branding CSS (display(HTML(<style>...)) in a code cell, run once, code hidden)
[md]   1. Header (title, course line, instructor, date, logos)
[md]   2. Table of contents (clickable anchor links)
[md]   3. Where this class sits in the programme (builds on / this class / leads to)
[md]   4. Today's thread (one paragraph, arrow-chained)
       --- Part I: the notes ---
[md]   5.  Section 1 heading + inside-out prose
[code]     Section 1 verified worked example (asserts) + a figure
[code]     Section 1 interactive lab   <-- only if warranted; comes right after the section
[md]       Section 2 heading + prose
[code]     Section 2 example + figure (+ lab if warranted)
       ... repeat for every section ...
       --- close ---
[code] N.  Cumulative self-check quiz (predict-then-reveal)
[md]   N+1 Problem set with worked solutions (reveals)
[md]   N+2 Appendix: one-screen cheat-sheet + run/share instructions + sources
```

## 0. Branding CSS

A single code cell near the top, code hidden, that injects the institutional theme. See
`references/components.md` for the exact CSS. Run it first so every markdown cell below inherits the fonts
and colours.

## 1. Header

Keep it three short lines. Institution logos as markdown images if you have them.

```markdown
# <Topic title, plain and specific>

**<Programme / course name>** · <Unit or department>

**Instructor:** <name>  ·  **Date:** <D Month YYYY>
```

## 2. Table of contents (clickable)

In Colab and Jupyter, `[label](#anchor)` jumps to a heading. The anchor is the heading text lowercased,
spaces to hyphens, punctuation dropped. So `## 3. The PDF and the CDF` is reached by `#3-the-pdf-and-the-cdf`.
Present the TOC as a table with a "big idea" column, so the reader sees the whole arc at a glance.

```markdown
## Table of contents

| # | Topic | Big idea |
|---|-------|----------|
| 1 | [First topic](#1-first-topic) | the one-line intuition |
| 2 | [Second topic](#2-second-topic) | the one-line intuition |

*Tip: click any topic to jump straight to it.* An **interactive lab** follows each section it belongs to,
so you can explore the idea while it is fresh.
```

Match the anchor slugs to your actual headings exactly, or the jumps break. Number the section headings
(`## 1. ...`) so the slugs are stable and the numbering is visible.

## 3. Where this class sits in the programme

This is what turns a set of notes into a class in a sequence. Three short paragraphs plus a summary table:
what earlier material this builds on, what this class does, what later material it unlocks. Name real prior
and future classes where you can.

```markdown
## Where this class sits in the programme

<One or two sentences framing this class against the previous one.>

**What it builds on.** <Concrete earlier ideas and why they matter here.>

**What it leads to.** <Concrete later ideas this unlocks.>

| builds on | this class | leads to |
|---|---|---|
| <prior ideas> | <this class in a phrase> | <downstream ideas> |
```

## 4. Today's thread

One paragraph that chains the whole class with arrows, so the reader holds the storyline before diving in.

```markdown
## Today's thread

<Idea A> $\to$ <Idea B> $\to$ <Idea C> $\to$ ... <final payoff>.
```

## 5+. Section template (repeat per section)

Each numbered section is a small unit: teach, show, verify, then let them play if warranted.

1. **Heading + prose** (markdown). Inside-out style: introduce each object in words then in symbol; after
   every displayed formula, a short "where" list. State the big idea first, then build to it.
2. **Worked example + figure** (code). Compute the result, `assert` it against an independent calculation,
   and draw a static figure whose title states the takeaway. See `references/components.md` for the assert
   pattern and matplotlib defaults.
3. **Interactive lab** (code), only where it teaches something a static figure cannot and that is not
   already covered by another lab. Put it right here, immediately after its section, not at the end.

A labelled worked example reads well as:

```markdown
> **Worked example.** <one-line problem statement>
>
> **Plan.** <the approach in a sentence>
> **Solve.** <the key steps, symbols named>
> **Check.** <what the assert in the next cell confirms>
> **Interpret.** <what the number means>
```

## N. Cumulative quiz

At the very end of Part I, a short self-check spanning the class. Use predict-then-reveal (HTML `<details>`
or ipywidgets), and if it is multiple mini-questions, keep a running score. This is the one thing that
belongs at the end rather than interleaved, because it is cumulative by design.

## N+1. Problem set

If the class has an official problem set, put the problems here with worked solutions hidden behind
`<details>` reveals so the reader attempts first. Every numeric answer carries an assert like any other.

## N+2. Appendix: cheat-sheet

A single markdown table the reader can screenshot: every key formula on one screen. Then a short "run /
share this notebook" note and a one-line sources line. For Colab the share note is simply that anyone with
the link can open and run it with no local install (Runtime -> Run all).

```markdown
## Appendix · One-screen cheat-sheet

| concept | formula |
|---|---|
| <name> | $<formula>$ |

---
**Run / share this notebook.** Open in Google Colab and choose Runtime -> Run all; no local install needed.

*Sources: <class notes / lecture>, <instructor>, <date>. Every number above is recomputed and asserted.*
```

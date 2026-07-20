# Pedagogy, interactivity, prose, and visual design

The taste behind the skeleton. Read this when writing prose or designing figures. The goal is a notebook a
student reads alone and comes away understanding, not a slide deck that needs a lecturer beside it.

## Pedagogy: active learning and explorable explanations

The notebooks that work treat the reader as an active participant, not a spectator.

- **Predict-then-reveal.** Before a result or a plot, ask the reader to commit to a guess, then reveal.
  A wrong prediction that gets corrected sticks; a passively read fact does not. Use `<details>` reveals or
  a widget button.
- **Explorable explanations.** Where a relationship has a knob (a rate, a sample size, a spread), let the
  reader turn it and watch the consequence. One knob, one consequence, one lesson. This is the spirit of
  Seeing Theory and Distill: the interaction *is* the explanation.
- **Learning goals up front, recap at the end.** Open a section by naming what the reader will be able to do;
  close the class with a `success` callout that restates it.
- **Name the misconception.** Most topics have a predictable trap (probability is height not area; doubling
  n halves the variance not the standard deviation). Call it out explicitly in a `warn` callout at the exact
  place a reader would stumble. Surfacing the wrong model and correcting it beats never mentioning it.
- **Worked examples with visible reasoning.** Problem, Plan, Solve, Check, Interpret. The Check step is the
  assert in the next code cell; the Interpret step says what the number means in the world.

## The interactivity policy, in depth

The instinct to make everything interactive is the main failure mode to resist. A page of live widgets is
slower to load, noisier to read, and paradoxically less clear than a few well-chosen static figures with one
or two interactive moments. The reasoning:

- Every widget is visual clutter and a beat of lag. Its cost is paid on every read; its benefit is paid only
  if the reader actually explores it.
- A static figure with a takeaway title teaches the point immediately, with no interaction required.
- So interactivity should be reserved for the places where *turning the knob yourself* is the lesson, and
  where no lab already covers that same knob.

Concretely, a good class notebook has: the interactive labs (one per section that warrants it), plus a small
handful (about three) of inline interactive moments in the body where exploration genuinely teaches. Examples
of moments that earn a widget: watching Binomial converge to Poisson as n grows; seeing two distributions
with the same mean but different spread; toggling `<` versus `≤` to feel a boundary case. Everything else is
a clean static figure. When unsure, ship it static; you can always promote it later.

## Prose conventions: inside-out writing

The prose should teach on its own, without the reader needing outside notes.

- **Introduce in words, then in symbol.** "the rate, written $\lambda$", not a bare `$\lambda$` the reader
  must decode.
- **A "where" list after every displayed formula.** Immediately after `$$...$$`, name each symbol:
  "where $f$ is the density, $F$ its running integral, and $x$ the point of evaluation." This single habit
  is what separates a notebook that teaches from one that only reminds.
- **Big idea first.** Lead each section with the one-sentence intuition, then build to the formalism. The
  "big idea" column in the TOC is a promise; deliver it at the top of the section.
- **Plain, direct sentences.** Short clauses. No throat-clearing, no "it is important to note that". State
  the thing.

## Style rules the reader will notice

- **No em dashes or en dashes, anywhere.** Not in prose, figure titles, comments, or table cells. Use a
  colon for a definition, a comma for an aside, a semicolon to join two clauses, or restructure the
  sentence. A dash reads as a machine-writing tell, and this reader removes them on sight. After drafting,
  scan the whole notebook for the characters and replace them.
- **No traces of AI or LLM authorship.** Write as the human author of a course. No meta commentary about
  being a model, no "generated", no apologies, no filler that a person compiling their own class notes would
  never write. Remove any assistant artifacts the tooling emits.
- **Verify every worked number.** Restated here because it is as much a trust rule as a correctness rule: a
  reader who spots one wrong number stops trusting the whole page. The asserts guarantee they never do.

## Visual design system

- **Institutional branding, swappable.** Default is UdeSA: primary blue `#00529B`, navy ink `#122535`,
  serif headings (Amiri), body in Work Sans, blue table headers. To rebrand, change the one primary colour,
  the two fonts, and the logo; keep the structure. Inject it once via the CSS cell in `components.md`.
- **Semantic colour, used consistently.** Give each colour a fixed job (primary = the main trace; accent =
  the contrast; good/bad = correct/wrong or converged/diverged; muted/grey = secondary geometry and
  gridlines) and never repurpose it within the notebook. The reader learns the code and reads figures
  faster.
- **Colourblind-safe.** The primary-blue and accent-terracotta pair is distinguishable for the common forms
  of colour vision deficiency; do not lean on red-versus-green alone to carry meaning, add a marker or label.
- **Figure titles state the takeaway.** "Larger rate means a shorter wait", not "Exponential PDF". The title
  is a sentence the reader remembers; the axis labels carry the mechanics.
- **KPI stat tiles for headline numbers.** A mean, a variance, a key probability read better as three tiles
  than buried in a paragraph. Use them at the top of a distribution's section.
- **Small multiples over one busy chart.** Three side-by-side panels sharing an axis beat one plot with six
  overlaid lines. Comparison is the point; make it a glance, not a decoding exercise.
- **Restraint.** Drop top and right spines, keep gridlines faint, let whitespace breathe. The content is the
  decoration.

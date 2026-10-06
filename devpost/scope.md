---
doc: scope
status: draft
---

# Proofline

**Review context (2026-10-06):** This scope records a Skill Pack review of an existing proof of concept. It is not a claim that this document preceded the original code. Details drawn from the current app are observations; the intended scope remains open to Robin's correction.

One line: a small, repeatable demonstration that a convincing AI-assisted implementation needs independent evidence before it earns a verified claim.

## The Unique Kernel

Two versions of one proportional allocator face the **same six independent conformance gates**. A plausible first pass clears the familiar examples but fails deeper requirements; a corrected version clears all six. The unchanged tests make the difference inspectable rather than rhetorical.

## Who It's For

A developer or reviewer working with AI-assisted code who needs to know whether a plausible result actually meets a stated contract. They can inspect both the verdict and the machine receipt instead of relying on a generated explanation or one happy-path example.

## The Core Loop

Open Proofline, select a specimen, run the six gates, read the per-gate verdict and receipt, switch specimens, and repeat the same check. The comparison shows which claims survive independent tests.

## Inspiration & Identity

The existing interface presents the test as a compact field instrument: restrained dark styling, precise labels, and the scientific-method sequence “State, Isolate, Test, Revise, Re-run.” This is an observed design choice in `web/index.html` and `web/styles.css`, not a newly attributed preference.

## Why This Matters to the Learner

Robin described an established cowork method for checking an agent's work against evidence. Proofline is a public, small-scale demonstration of that principle. Any broader claim about the method's origin or outcomes needs Robin's review.

## What "Working" Looks Like

The visitor sees the ungated allocator pass 2/6 gates and the corrected allocator pass 6/6, can inspect the failed and passing gate receipts, and can reproduce the live run from the public repository. The memorable beat is that familiar examples pass in both specimens, while the full contract separates them.

## The POC Boundary

One fixed task, two fixed implementations, six deterministic gates, one browser comparison surface, a local Python run, and a clearly labeled static replay. A failed run must leave an understandable error state rather than a misleading running state.

## Later

Let reviewers bring a new implementation or define their own contract, after this fixed demonstration is trustworthy and usable.

## Explicitly Cut

- Automatic judgment of arbitrary AI output: a general evaluator would need task-specific contracts and a much larger trust model.
- Accounts, shared projects, and stored histories: they do not prove the core comparison.
- Executing Python on the static public demo: GitHub Pages hosts static files; the local server supplies live execution.

---
doc: prd
status: draft
---

# Proofline — Product Requirements

**Review context (2026-10-06):** Retrospective Skill Pack product review of the existing implementation. This draft documents observed behavior plus one review-driven error-state refinement; it does not claim a prebuild approval.

Proofline lets a reviewer compare two implementations of one allocator against the same six falsifiable requirements. Source: `scope.md > The Unique Kernel` and `scope.md > Who It's For`.

## The Core Journey

1. The visitor opens the single-page instrument and sees a claim, two specimen choices, six named gates, and whether the page can run Python locally or is replaying published evidence.
2. The visitor selects **Ungated** and runs the checks. Each gate changes from waiting to a pass or fail, followed by a score and verdict.
3. The visitor opens the machine receipt to inspect the test output and timing behind the verdict.
4. The visitor selects **Corrected** and repeats the **same** checks. The pass on familiar examples no longer masks the ungated specimen's deeper failures.
5. A visitor who wants live reproducibility clones the public repository and runs the local server or command-line runner.

Source: `scope.md > The Core Loop` and `scope.md > What "Working" Looks Like`.

## Screens and Layout

One browser page. The upper section introduces the claim; the central instrument contains specimen choices, a run action, verdict, gate list, and expandable receipt. A short scientific-method section explains the logic. The public page and local page use the same layout. Source: `scope.md > The POC Boundary`.

## Look and Feel

Preserve the existing restrained field-instrument presentation: light paper background, dark text, clear hierarchy, compact labels, and visible distinction between pass, fail, waiting, and execution mode. This describes the current interface; Robin has not separately approved a new visual direction. Source: `scope.md > Inspiration & Identity`.

## Features and Behavior

### Select a specimen

- Offer exactly **Ungated** and **Corrected**.
- Make the selected specimen visually identifiable.
- Reset the prior score and gate results when the visitor switches specimens, so the screen never attributes old evidence to the new choice.
- Keep the selected specimen fixed during a run so its eventual results cannot be attributed to a different choice.

### Run the six gates

- Apply the same six named checks in the same order to either specimen: familiar examples, input/output contract, conservation, deterministic ties, boundary behavior, and efficiency budget.
- Show a waiting state before execution, progress while presenting results, each gate's pass/fail state and elapsed time, then the evidence-derived total and verdict.
- Ungated should show 2/6; Corrected should show 6/6 for the fixed demonstration. A changed result is a signal to inspect the actual receipt rather than force a prerecorded score.

### Inspect evidence

- Provide the report as readable JSON, including implementation name, aggregate result, gate names, pass/fail values, timing, and test output.
- Label **local Python execution** and **static evidence replay** accurately; replay must not imply that the public static host executed tests.

### Recover from an unavailable run

- If the local run or replay report cannot be loaded, display an **UNKNOWN** verdict and a visible error message.
- Remove any stale “RUNNING” gate marker and allow another attempt.
- Do not turn a failed fetch or execution into a conformance failure for the specimen; the test outcome is unknown.

## States and Boundaries

- **First visit / new selection:** all gates wait, score is blank, and the verdict says not yet tested.
- **Running:** the run control is temporarily disabled and progress is visible.
- **Completed:** gate results, score, verdict, and receipt all describe the selected specimen.
- **Execution unavailable:** the verdict is unknown, the message is visible, and the run control becomes available again.
- **Static public page:** uses committed receipts and explicitly says it is replaying evidence.
- **Local page:** runs the real Python tests and returns a fresh receipt.

## Product Decisions

- The fixed two-specimen comparison is the existing project's chosen demonstration of evidence-based review, not an invented general-purpose evaluator.
- The same gates stay fixed between specimens so the comparison is meaningful. Source: `scope.md > The Unique Kernel`.
- Static replay is explicitly labeled because only the local server can execute Python. Source: `scope.md > The POC Boundary`.
- Error recovery is a review finding from this Skill Pack pass; Robin can revise it during review.

## What We're Building

A reproducible local runner and single-page comparison that demonstrate the fixed claim, expose the receipts, clearly identify replay versus live execution, and recover honestly from an unavailable run.

## Deferred From the POC

User-uploaded code, editable test suites, accounts, persistent histories, and hosted Python execution. Each would enlarge the system without strengthening this fixed comparison.

## Possible Later Enhancements

Allow a reviewer to supply another allocator or contract, with isolation and resource limits designed before accepting arbitrary code.

## Non-Goals

- Prove all AI-assisted code is correct: the verdict applies only to this task and these six gates.
- Present static replay as a live execution: doing so would misstate the evidence.

## Open Questions

- Robin should confirm whether this description of the cowork method and intended audience matches their intent before marking this draft approved. This does not block documenting observed app behavior.

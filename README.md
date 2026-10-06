# Proofline

Proofline is a compact demonstration of deterministic conformance gates for
AI-assisted code. A plausible proportional allocator passes familiar examples
but only 2 of 6 independent gates. A corrected largest-remainder allocator
passes the same 6 of 6 gates.

## Skill Pack review

The [scope](devpost/scope.md), [product requirements](devpost/prd.md), and
[technical spec](devpost/spec.md) record a retrospective review and refinement
using the Devpost Learn Skill Pack on 2026-10-06. They describe the existing
proof of concept and the error-state improvement made during that review; they
are drafts for the project owner's review, not a claim that these documents
preceded the original implementation.

## Run the browser demo

```bash
python3 -m app.server
```

Open <http://127.0.0.1:8765>. In local mode, the page executes the real Python
tests. On a static host it clearly switches to evidence-replay mode using the
committed JSON receipts.

## Run from the terminal

```bash
python3 experiment/run_gauntlet.py ungated
python3 experiment/run_gauntlet.py conformant
```

The runner executes every gate in a separate subprocess and writes a JSON
receipt under `experiment/`.

## Verify the project

```bash
python3 -m unittest discover -v
```

Proofline uses only the Python standard library at runtime.

## Public demo

The GitHub Pages build is a static evidence explorer. It replays the committed
receipts and labels that mode explicitly; it does not pretend to execute Python
inside the static host. Clone the repository and use `python3 -m app.server`
for live execution.

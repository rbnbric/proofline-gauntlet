---
doc: spec
status: draft
---

# Proofline — Technical Spec

**Review context (2026-10-06):** Retrospective Skill Pack technical review of existing files, with one small error-state refinement identified here. This draft is not represented as the plan that preceded the initial build.

## How This Works, In Plain Language

Proofline keeps the question fixed and changes only the allocator under review. Six small Python test groups each check a separate property. A runner starts them independently and collects a receipt. The browser either asks a local server to run those tests or, on the public static site, shows the committed receipt. Both modes say which kind of evidence the visitor is seeing. This structure makes an attractive answer answerable to tests without requiring a large platform.

## The Core Journey Through the System

The visitor selects a specimen in the browser → `web/app.js` clears old results → the visitor runs the gates → `web/app.js` asks `/api/run` when the local server is available, otherwise loads `web/reports/<specimen>-report.json` → `experiment/run_gauntlet.py` runs six isolated test modules for a local request → the browser shows per-gate results, total, and raw receipt. On any loading or execution error, it shows UNKNOWN and clears the progress marker. Implements `prd.md > The Core Journey`, `prd.md > Run the six gates`, and `prd.md > Recover from an unavailable run`.

## Stack

- Python 3 with the standard library for the allocators, `unittest` gates, JSON receipts, and local HTTP server. This is the existing stack; no package install or API key is needed. [Python documentation](https://docs.python.org/3/), [unittest](https://docs.python.org/3/library/unittest.html), [http.server](https://docs.python.org/3/library/http.server.html).
- Plain HTML, CSS, and browser JavaScript for the interface. The public demo needs no JavaScript framework or build step. [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript).
- GitHub Pages serves static HTML and committed receipts. [GitHub Pages documentation](https://docs.github.com/en/pages).

## Where It Runs and How Someone Tries It

Run `python3 -m app.server` from the repository root, then open `http://127.0.0.1:8765/` for live execution. For a terminal check, run `python3 experiment/run_gauntlet.py ungated` and `python3 experiment/run_gauntlet.py conformant`; the first intentionally exits nonzero because it fails four gates. Run `python3 -m unittest discover -v` for the project test suite. The public static demo is `https://rbnbric.github.io/proofline-gauntlet/`; the public source is `https://github.com/rbnbric/proofline-gauntlet`. A short demo video and public repository are separate submission items; static deployment does not replace the video.

## Look and Feel

Keep the existing light paper, dark text, measured field-instrument style in `web/styles.css`. Use readable status words alongside visual colors so the verdict does not depend on color alone. Keep mode text prominent enough to distinguish live execution from replay. Implements `prd.md > Look and Feel` and `prd.md > Inspect evidence`.

## Components

### Browser instrument

`web/index.html`, `web/styles.css`, and `web/app.js` provide specimen selection, run state, six results, verdict, and expandable JSON receipt. The choices stay disabled during a run. On a failed load or run, the UI must remove “RUNNING,” show UNKNOWN plus the reason, and re-enable the controls. Implements `prd.md > Select a specimen`, `prd.md > Run the six gates`, `prd.md > Inspect evidence`, and `prd.md > Recover from an unavailable run`.

### Local HTTP server

`app/server.py` serves only files under `web/`, answers `/api/mode`, validates the requested specimen at `/api/run`, and starts the gauntlet. Implements `prd.md > Inspect evidence` and `prd.md > States and Boundaries`.

### Gate runner

`experiment/run_gauntlet.py` maps a specimen name to its allocator, runs each of six `unittest` modules in a separate bounded subprocess, and returns a JSON receipt. Its command-line form also writes an experiment receipt. Implements `prd.md > Run the six gates` and `prd.md > Inspect evidence`.

### Specimens and independent tests

`experiment/allocator_ungated.py` is intentionally plausible but incomplete. `experiment/allocator_conformant.py` validates the contract and uses largest remainders with stable index tie breaking. `experiment/tests/test_01_examples.py` through `test_06_efficiency.py` check both using the same test bodies. Implements `prd.md > Run the six gates`.

### Static evidence receipts

`web/reports/ungated-report.json` and `web/reports/conformant-report.json` are committed examples for the public replay. They are evidence snapshots with their own timings, not a claim of fresh execution. Implements `prd.md > Inspect evidence`.

## Data Model

The runner returns one report: `implementation` (ungated or conformant), `verified` (all gates passed), `passed`, `total`, and ordered `gates`. Each gate has `gate`, `passed`, `exit_code`, `duration_seconds`, and `output`. Local runs write a new receipt under `experiment/`; the static site reads committed copies under `web/reports/`. The browser keeps only the current selection and current displayed report in page memory; a reload starts a new view.

## File Structure

```text
proofline-gauntlet/
├── app/
│   ├── server.py             # local HTTP and run API
│   └── test_server.py        # local server checks
├── experiment/
│   ├── allocator_ungated.py  # deliberately shallow specimen
│   ├── allocator_conformant.py # corrected specimen
│   ├── run_gauntlet.py       # isolated six-gate runner
│   └── tests/test_01..06_*.py # independent property checks
├── web/
│   ├── index.html, styles.css, app.js # browser instrument
│   └── reports/*.json        # static replay receipts
├── devpost/
│   ├── scope.md, prd.md, spec.md # Skill Pack review drafts
│   └── learner-profile.md   # local-only, gitignored
├── .github/workflows/pages.yml
├── LICENSE
└── README.md
```

## External Services and Dependencies

GitHub Pages serves the static demo from the repository. The browser only requests local `/api/mode`, posts `{"implementation":"ungated"}` or `{"implementation":"conformant"}` to local `/api/run`, or fetches one same-origin JSON receipt in replay mode. No external model API, database, service key, or paid runtime is part of the proof of concept.

## Important Failure Modes

- **A local test crashes or exceeds its 10-second limit** → the server returns an error; the browser says UNKNOWN and shows the error rather than a false fail verdict.
- **A static receipt is missing or cannot be fetched** → the browser says UNKNOWN, removes progress, and lets the visitor retry.
- **The public site cannot run Python** → the mode is visibly labeled STATIC EVIDENCE REPLAY, and the README gives the local run instructions.

## What Was Simplified and Why

- Two fixed implementations and six gates instead of arbitrary user code and editable tests: this proves the comparison without requiring safe execution of unknown programs.
- Committed receipts on GitHub Pages instead of hosted Python execution: this keeps the public demo simple while preserving a reproducible local route.

## Decisions and Open Issues

- The fixed task and same-gate comparison reflect the existing product and its evidence-first purpose; the precise wording of Robin's broader cowork method awaits review.
- The current Skill Pack pass identifies UI error recovery as an implementation refinement. It does not imply the original build followed this draft.
- No separate learner uncertainty about the technical stack was established. The remaining product question is in `prd.md > Open Questions`.

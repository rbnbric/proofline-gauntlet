#!/usr/bin/env python3
"""Run each gate separately so one shallow pass cannot hide deeper failures."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
IMPLEMENTATIONS = {
    "ungated": "experiment.allocator_ungated",
    "conformant": "experiment.allocator_conformant",
}
GATES = [
    ("examples", "experiment.tests.test_01_examples"),
    ("contract", "experiment.tests.test_02_contract"),
    ("conservation", "experiment.tests.test_03_conservation"),
    ("determinism", "experiment.tests.test_04_determinism"),
    ("boundaries", "experiment.tests.test_05_boundaries"),
    ("efficiency", "experiment.tests.test_06_efficiency"),
]


def run(implementation: str) -> dict:
    module = IMPLEMENTATIONS[implementation]
    results = []
    for gate, test_module in GATES:
        env = os.environ.copy()
        env["ALLOCATOR_IMPL"] = module
        started = time.perf_counter()
        completed = subprocess.run(
            [sys.executable, "-m", "unittest", test_module, "-v"],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            timeout=10,
            shell=False,
            check=False,
        )
        # Reports are intended for publication. Keep tracebacks useful without
        # disclosing the workstation's absolute checkout path.
        combined = (completed.stdout + completed.stderr).replace(str(ROOT), ".")[-12_000:]
        results.append(
            {
                "gate": gate,
                "passed": completed.returncode == 0,
                "exit_code": completed.returncode,
                "duration_seconds": round(time.perf_counter() - started, 4),
                "output": combined,
            }
        )
    return {
        "implementation": implementation,
        "verified": all(item["passed"] for item in results),
        "passed": sum(item["passed"] for item in results),
        "total": len(results),
        "gates": results,
    }


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in IMPLEMENTATIONS:
        print("usage: python3 experiment/run_gauntlet.py ungated|conformant", file=sys.stderr)
        return 2
    report = run(sys.argv[1])
    for result in report["gates"]:
        state = "PASS" if result["passed"] else "FAIL"
        print(f"{state:4}  {result['gate']:<14} {result['duration_seconds']:.4f}s")
        if not result["passed"]:
            failure_lines = [
                line for line in result["output"].splitlines()
                if "AssertionError" in line or "ZeroDivisionError" in line
            ]
            for line in failure_lines[-2:]:
                print(f"      {line.strip()}")
    print(f"RESULT {report['passed']}/{report['total']} gates; verified={report['verified']}")
    report_path = ROOT / "experiment" / f"{sys.argv[1]}-report.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"REPORT {report_path.relative_to(ROOT)}")
    return 0 if report["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

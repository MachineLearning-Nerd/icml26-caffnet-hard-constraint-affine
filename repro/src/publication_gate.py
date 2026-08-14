#!/usr/bin/env python3
"""Run the fast publication checks and write a machine-readable gate result."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-producers", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    producer_results: dict[str, str] = {}

    if not args.skip_producers:
        for name, script in (
            ("theorem", "repro/src/run_theorem_audit.py"),
            ("theorem35", "repro/src/verify_theorem35_exact_bound.py"),
            ("theorem35_independent", "repro/src/audit_theorem35_exact_bound.py"),
        ):
            completed = subprocess.run([sys.executable, script], cwd=root, text=True,
                                       capture_output=True)
            producer_results[name] = "PASS" if completed.returncode == 0 else "FAIL"
            if completed.returncode:
                print(completed.stdout, end="")
                print(completed.stderr, end="", file=sys.stderr)

    verifier = subprocess.run(
        [sys.executable, "repro/src/verify_results.py"],
        cwd=root,
        text=True,
        capture_output=True,
    )
    if verifier.stdout:
        print(verifier.stdout, end="")
    if verifier.stderr:
        print(verifier.stderr, end="", file=sys.stderr)
    verifier_result = json.loads(verifier.stdout)
    producers_ok = all(value == "PASS" for value in producer_results.values())
    gate_ok = verifier.returncode == 0 and producers_ok
    result = {
        "status": "SCOPED_PASS" if gate_ok else "FAIL",
        "producers": producer_results,
        "verification_status": verifier_result["status"],
        "scope": "Proof and exact-task publication surface; not an official paper-wide score.",
    }
    (root / "outputs/publication_gate.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0 if gate_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

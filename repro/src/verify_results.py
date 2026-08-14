#!/usr/bin/env python3
"""Fail-closed verification of the CAffNet publication surface."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


EXPECTED_NAME = "icml26-caffnet-hard-constraint-affine"
EXPECTED_IDENTITY = "MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>"


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


def read_json(root: Path, relative: str) -> dict:
    return json.loads((root / relative).read_text())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[2]
    checks: dict[str, bool] = {}
    details: dict[str, str] = {}

    def check(name: str, condition: bool, detail: str = "") -> None:
        checks[name] = bool(condition)
        if detail:
            details[name] = detail

    pyproject = (root / "pyproject.toml").read_text()
    sources = read_json(root, "sources.json")
    theorem = read_json(root, "repro/outputs/theorem_certificates.json")
    hardnet = read_json(root, "outputs/hardnet_unicycle_audit.json")
    training = read_json(root, "evidence/training_summary.json")
    parameterization = read_json(root, "evidence/parameterization_equivalence_summary.json")

    check("project_name", f'name = "{EXPECTED_NAME}"' in pyproject)
    check("paper_identity", sources["paper"]["openreview_id"] == "20hdQQQrA4")
    check("paper_source_hash", len(sources["paper"]["source_pdf_sha256"]) == 64)
    check("claim_statuses", sources["claim_status"]["C1"] == "VERIFIED_SCOPED"
          and sources["claim_status"]["C2"] == "VERIFIED_SCOPED_WITH_QUALIFICATION"
          and sources["claim_status"]["C3"] == "VERIFIED_SCOPED")
    check("required_docs", all(
        (root / path).is_file()
        for path in (
            "README.md",
            "STATUS.md",
            "sources.json",
            "docs/CLAIM_EVIDENCE.md",
            "docs/BRANCH_AUDIT.md",
            "docs/SOURCE_AUDIT.md",
            "docs/PUBLICATION_GATE.md",
            "docs/research_log.md",
        )
    ))
    readme = (root / "README.md").read_text()
    check("citation_and_thanks", "@article{zhao2026caffnet" in readme
          and "Thank you to Yang Zhao" in readme)
    check("theorem_certificates", theorem.get("all_valid") is True
          and all(claim.get("valid") is True for claim in theorem.get("claims", [])))
    check("training_boundary", training["paper_spec_scenario_a"]["within_one_reported_std"] is True
          and training["paper_dimension_scenario_b"]["status"] == "NOT_REPRODUCED")
    check("parameterization_qualification", parameterization["restricted_capacity_counterexample"] is True
          and "Falsified" in parameterization["conclusion"]["strong_representational_reading"])
    check("hardnet_audit", hardnet["audit_passed"] is True
          and hardnet["checks"]["committed_result_exactly_recomputed"] is True
          and hardnet["checks"]["scope_does_not_claim_goal_arrival"] is True)

    tracked = git(root, "ls-files").splitlines()
    check("no_stale_state", "logbook.json" not in tracked
          and not any(path == ".trackio" or path.startswith(".trackio/") for path in tracked))
    branch = git(root, "branch", "--show-current")
    check("canonical_branch", branch == "main", branch)
    refs = git(root, "branch", "-a")
    check("branch_names", "master" not in refs and "claim2-joint-optimization" not in refs
          and "main" in refs and "experiment/joint-optimization-control" in refs)
    remote = git(root, "remote", "get-url", "origin")
    check("final_remote", EXPECTED_NAME in remote, remote)

    identities = git(root, "log", "--all", "--format=%an <%ae>%n%cn <%ce>").splitlines()
    check("commit_identity", bool(identities) and all(item == EXPECTED_IDENTITY for item in identities),
          "unexpected identities: " + ", ".join(sorted(set(item for item in identities if item != EXPECTED_IDENTITY))))
    check("no_private_workspace_path", "dinesh.jinjala@mareana.com" not in git(root, "log", "--all", "--format=%B")
          and "/Users/dineshjinjala/" not in "\n".join(
              (root / path).read_text(errors="ignore") for path in tracked if (root / path).is_file()
          ))

    result = {
        "repository": EXPECTED_NAME,
        "paper": "20hdQQQrA4",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "details": details,
    }
    output = root / "outputs/verification.json"
    if not args.no_write:
        output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

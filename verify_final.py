#!/usr/bin/env python3
"""Verify the CAffNet dossier and live GitHub publication state."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPOSITORY = "icml26-caffnet-hard-constraint-affine"
CANONICAL = (
    "MachineLearning-Nerd",
    "MachineLearning-Nerd@users.noreply.github.com",
)
EXPECTED_BRANCHES = {"main", "experiment/joint-optimization-control"}
EXPECTED_STATUSES = [
    "verified_scoped",
    "verified_scoped_with_qualification",
    "verified_scoped",
    "scoped_exact_task_audit",
]
SOURCE_PDF_SHA = "33db803823608bdb76db20732f0a3a20aef32c5f4e22f4c4b148a2b7b6da9520"
HARDNET_COMMIT = "4f3ebe496c4081489c486e2711f25697a4c312fa"
REQUIRED_PATHS = [
    "README.md",
    "STATUS.md",
    "pyproject.toml",
    "uv.lock",
    "sources.json",
    "AUTONOMOUS_STATE.json",
    "CLAIM_EVIDENCE.md",
    "SOURCE_AUDIT.md",
    "ENVIRONMENT.md",
    "REPORT.md",
    "AUTHOR_THANK_YOU.md",
    "CITATION.cff",
    "BRANCH_AUDIT.md",
    "branch-audit.md",
    "claims.json",
    "EVIDENCE_MANIFEST.json",
    "verify_final.py",
    "docs/CLAIM_EVIDENCE.md",
    "docs/SOURCE_AUDIT.md",
    "docs/BRANCH_AUDIT.md",
    "docs/PUBLICATION_GATE.md",
    "docs/THEOREM_AUDIT.md",
    "docs/TRAINING_AUDIT.md",
    "docs/research_log.md",
    "evidence/theorem_summary.json",
    "evidence/parameterization_equivalence_summary.json",
    "evidence/training_summary.json",
    "evidence/hardnet_control_summary.json",
    "outputs/publication_gate.json",
    "outputs/verification.json",
    "outputs/training_analysis.json",
    "outputs/hardnet_unicycle_results.json",
    "outputs/hardnet_unicycle_audit.json",
    "outputs/joint_control/summary.json",
    "outputs/joint_control/verification.json",
    "repro/outputs/theorem_certificates.json",
    "repro/src/theorem_certificates.py",
    "repro/src/verify_results.py",
    "repro/src/verify_theorem35_exact_bound.py",
    "repro/src/audit_theorem35_exact_bound.py",
    "repro/src/audit_hardnet_unicycle_control.py",
    "repro/src/verify_hardnet_unicycle_control.py",
    "pages/claim-theorem35-exact-bound/page.md",
    "pages/claim-hardnet-unicycle-control/page.md",
]


def fail(message: str) -> None:
    print(f"FINAL_AUDIT=FAILED {message}", file=sys.stderr)
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def run(*args: str) -> str:
    result = subprocess.run(
        args,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"command failed: {' '.join(args)}\n{result.stderr.strip()}")
    return result.stdout


def current_bytes(path: str) -> bytes:
    local = ROOT / path
    if local.exists():
        return local.read_bytes()
    result = subprocess.run(
        ["git", "show", f"HEAD:{path}"],
        cwd=ROOT,
        check=False,
        capture_output=True,
    )
    if result.returncode:
        fail(f"required path is unavailable: {path}")
    return result.stdout


def current_json(path: str) -> object:
    try:
        return json.loads(current_bytes(path))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path}: {exc}")
    return None


def sha256(path: str) -> str:
    return hashlib.sha256(current_bytes(path)).hexdigest()


def verify_manifest() -> None:
    manifest = current_json("EVIDENCE_MANIFEST.json")
    require(isinstance(manifest, dict), "manifest is not an object")
    require(manifest.get("schema_version") == 1, "unsupported manifest schema")
    require(manifest.get("hash_algorithm") == "sha256", "manifest hash algorithm changed")
    entries = manifest.get("entries")
    require(isinstance(entries, list) and entries, "evidence manifest is empty")
    seen = set()
    for entry in entries:
        require(isinstance(entry, dict), "manifest entry is not an object")
        path = entry.get("path")
        expected = entry.get("sha256")
        require(isinstance(path, str), "manifest path is missing")
        require(isinstance(expected, str) and len(expected) == 64, f"bad manifest hash for {path}")
        require(path not in seen, f"duplicate manifest path: {path}")
        seen.add(path)
        require((ROOT / path).exists(), f"manifest path is missing: {path}")
        require(sha256(path) == expected, f"manifest hash mismatch: {path}")
    require("AUTONOMOUS_STATE.json" not in seen, "state must not create a hash cycle")


def verify_git_state() -> tuple[int, int]:
    origin = run("git", "config", "--get", "remote.origin.url").strip()
    require(
        origin in {
            f"https://github.com/MachineLearning-Nerd/{REPOSITORY}.git",
            f"git@github.com:MachineLearning-Nerd/{REPOSITORY}.git",
        },
        f"unexpected origin: {origin}",
    )
    require(
        "ref: refs/heads/main\tHEAD"
        in run("git", "ls-remote", "--symref", "origin", "HEAD"),
        "origin/HEAD is not main",
    )

    remote_heads = {}
    for line in run("git", "ls-remote", "--heads", "origin").splitlines():
        commit, ref = line.split("\t", 1)
        require(ref.startswith("refs/heads/"), f"unexpected remote ref: {ref}")
        remote_heads[ref.removeprefix("refs/heads/")] = commit
    require(set(remote_heads) == EXPECTED_BRANCHES, "remote branch set changed")
    for branch in EXPECTED_BRANCHES:
        require(
            remote_heads[branch] == run("git", "rev-parse", f"origin/{branch}").strip(),
            f"origin/{branch} differs from the live remote tip",
        )

    local_heads = set(
        run(
            "git",
            "for-each-ref",
            "--format=%(refname:strip=2)",
            "refs/heads",
        ).splitlines()
    )
    require(local_heads <= EXPECTED_BRANCHES, "unexpected local branch")
    require(run("git", "branch", "--show-current").strip() == "main", "current branch is not main")
    refs = run("git", "for-each-ref", "--format=%(refname)", "refs").splitlines()
    require(not any("refs/original/" in ref for ref in refs), "refs/original remains")

    identities = set()
    for line in run(
        "git", "log", "--all", "--format=%an\t%ae\t%cn\t%ce"
    ).splitlines():
        if line.strip():
            identities.add(tuple(line.split("\t")))
    require(
        identities == {(CANONICAL[0], CANONICAL[1], CANONICAL[0], CANONICAL[1])},
        f"non-canonical reachable identity: {sorted(identities)}",
    )
    require(
        "co-authored-by:" not in run("git", "log", "--all", "--format=%B").lower(),
        "co-author trailer found",
    )
    commit_count = int(run("git", "rev-list", "--count", "--all").strip())
    require(commit_count >= 14, f"unexpectedly short history: {commit_count}")
    return len(remote_heads), commit_count


def verify_artifacts() -> None:
    for path in REQUIRED_PATHS:
        require((ROOT / path).exists(), f"required path missing: {path}")

    sources = current_json("sources.json")
    require(isinstance(sources, dict), "sources.json is not an object")
    paper = sources.get("paper", {})
    require(
        paper.get("openreview_id") == "20hdQQQrA4"
        and paper.get("arxiv_id") == "2605.24437"
        and paper.get("source_pdf_sha256") == SOURCE_PDF_SHA,
        "paper source pin changed",
    )
    repository = sources.get("repository", {})
    require(
        repository.get("final_name") == REPOSITORY
        and repository.get("owner") == "MachineLearning-Nerd"
        and repository.get("default_branch") == "main",
        "repository metadata changed",
    )
    require(
        sources.get("official_implementation", {}).get("caffnet_code") is None,
        "official CAffNet code was asserted",
    )
    hardnet = sources.get("supplemental_hardnet_source", {})
    require(
        hardnet.get("revision") == HARDNET_COMMIT
        and hardnet.get("file_sha256")
        == "7fb545ba991719d89cca1553bd4aef824a416ea2ad07cf97e54565c405586f1b",
        "HardNet source pin changed",
    )

    claims = current_json("claims.json")
    require(isinstance(claims, dict), "claims.json is not an object")
    require(
        claims.get("repository") == f"MachineLearning-Nerd/{REPOSITORY}",
        "claims repository mismatch",
    )
    require(claims.get("publication_allowed") is False, "publication block changed")
    rows = claims.get("claims")
    require(isinstance(rows, list) and len(rows) == 4, "claims.json must contain four rows")
    require([row.get("status") for row in rows] == EXPECTED_STATUSES, "claim statuses changed")

    state = current_json("AUTONOMOUS_STATE.json")
    require(isinstance(state, dict), "state is not an object")
    require(state.get("phase") == "published_and_verified", "state is not final")
    require(state.get("publication_allowed") is False, "state publication block changed")
    require(
        state.get("branch_set") == ["main", "experiment/joint-optimization-control"],
        "state branch set changed",
    )
    require(state.get("last_known_git_commit"), "state has no checkpoint commit")

    publication = current_json("outputs/publication_gate.json")
    require(
        publication.get("status") == "SCOPED_PASS"
        and publication.get("verification_status") == "PASS"
        and "not an official paper-wide score" in publication.get("scope", ""),
        "publication gate changed",
    )
    verification = current_json("outputs/verification.json")
    require(verification.get("status") == "PASS", "recorded verification failed")
    require(
        all(value is True for value in verification.get("checks", {}).values()),
        "a recorded verification check is false",
    )

    theorem = current_json("evidence/theorem_summary.json")
    require(
        theorem.get("paper") == "20hdQQQrA4"
        and theorem.get("status") == "VERIFIED_SCOPED"
        and theorem.get("all_valid") is True
        and all(row.get("valid") is True for row in theorem.get("claims", {}).values()),
        "theorem summary changed",
    )
    parameterization = current_json("evidence/parameterization_equivalence_summary.json")
    require(
        parameterization.get("status") == "QUALIFICATION_AUDIT"
        and parameterization.get("restricted_capacity_counterexample") is True
        and "Falsified" in parameterization.get("conclusion", {}).get(
            "strong_representational_reading", ""
        ),
        "C2 qualification changed",
    )
    training = current_json("evidence/training_summary.json")
    require(
        training.get("paper_spec_scenario_a", {}).get("status") == "PARTIAL_REPRODUCTION"
        and training.get("paper_dimension_scenario_b", {}).get("status") == "NOT_REPRODUCED"
        and training.get("paper_spec_scenario_a", {}).get("within_one_reported_std") is True,
        "training boundary changed",
    )
    hardnet_audit = current_json("outputs/hardnet_unicycle_audit.json")
    require(
        hardnet_audit.get("audit_passed") is True
        and hardnet_audit.get("checks", {}).get("committed_result_exactly_recomputed") is True
        and hardnet_audit.get("checks", {}).get("scope_does_not_claim_goal_arrival") is True,
        "HardNet audit changed",
    )
    joint = current_json("outputs/joint_control/verification.json")
    require(
        all(value is True for value in joint.values()),
        "joint-control verification changed",
    )
    theorem_artifact = current_json("repro/outputs/theorem_certificates.json")
    require(
        theorem_artifact.get("paper") == "20hdQQQrA4"
        and all(row.get("valid") is True for row in theorem_artifact.get("claims", [])),
        "theorem certificate artifact changed",
    )
    tracked = run("git", "ls-files").splitlines()
    require(
        not any(path == ".trackio" or path.startswith(".trackio/") for path in tracked)
        and "logbook.json" not in tracked,
        "stale Trackio/logbook state is tracked",
    )


def main() -> None:
    branches, commits = verify_git_state()
    verify_artifacts()
    verify_manifest()
    print(
        "FINAL_AUDIT=VERIFIED "
        f"branches={branches} commits={commits} "
        "claims=C1:verified_scoped,C2:verified_scoped_with_qualification,"
        "C3:verified_scoped,S1:scoped_exact_task_audit publication_allowed=false"
    )


if __name__ == "__main__":
    main()

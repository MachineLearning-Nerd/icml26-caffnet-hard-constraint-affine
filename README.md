# CAffNet: Hard Constraint-Affine Neural Networks

Scoped clean-room reproduction of **CAffNet: Hard Constraint-Affine Neural
Networks** for the ICML 2026 reproduction collection.

The repository separates proof-level results, finite neural corroboration, and
the exact-task HardNet control. It does not claim an official benchmark score
or a reproduction of unpublished matrices, seeds, checkpoints, or training
weights.

## Paper identity

| Field | Value |
| --- | --- |
| Paper | *CAffNet: Hard Constraint-Affine Neural Networks* |
| Authors | Yang Zhao, Jungeun Lee, Jeong hwan Jeon, Sze Zheng Yong |
| arXiv | [2605.24437](https://arxiv.org/abs/2605.24437) |
| OpenReview | [20hdQQQrA4](https://openreview.net/forum?id=20hdQQQrA4) |
| Audited source | arXiv v1; SHA-256 `33db803823608bdb76db20732f0a3a20aef32c5f4e22f4c4b148a2b7b6da9520` |
| Repository role | Clean-room theorem audit, neural corroboration, and named-baseline control |

## Claim status

| Claim | Status | What is actually established |
| --- | --- | --- |
| C1 — hard satisfaction for arbitrary finite input-dependent affine constraints | `VERIFIED_SCOPED` | Minimal-face enumeration plus exact Moore–Penrose algebra establishes a feasible candidate under the paper's assumptions. |
| C2 — jointly trainable null-space path beyond fixed projections | `VERIFIED_SCOPED_WITH_QUALIFICATION` | The projector identity, gradients, and five-seed control reproduce the trainable path; a fixed orthogonal model trained end-to-end reaches its oracle, so stronger uniqueness/superiority wording is not claimed. |
| C3 — universal approximation with hard adherence | `VERIFIED_SCOPED` | An independent proof audit verifies the paper's approximation chain and exact Theorem 3.5 constant under its assumptions; finite experiments are corroboration only. |
| S1 — named HardNet-Aff control on the paper's unicycle task | `SCOPED_EXACT_TASK_AUDIT` | The exact enforcement layers are compared with zero learned correction. CAffNet is collision-free and feasible in the audit; no goal-arrival or trained-weight claim is made. |

The scope and evidence for every row are recorded in
[`docs/CLAIM_EVIDENCE.md`](docs/CLAIM_EVIDENCE.md). `VERIFIED_SCOPED` means
that the stated local proof or experiment passes; it is deliberately narrower
than “the entire paper is reproduced.”

## How each claim is produced

### C1 — arbitrary-cardinality hard constraints

[`repro/src/theorem_certificates.py`](repro/src/theorem_certificates.py)
constructs a proof DAG for the minimal-face argument. For a selected face it
checks the identity

```text
P_gamma = f - A_gamma^dagger(A_gamma f - b_gamma)
          + (I - A_gamma^dagger A_gamma) w.
```

The minimal face uses at most `n_out` independent active rows, so it is among
the enumerated subsets even when the original system has more constraints or
dependent/redundant rows. The rendered artifact is
[`repro/outputs/theorem_certificates.json`](repro/outputs/theorem_certificates.json);
the finite 2,000-instance and negative-control summary is
[`outputs/caffnet_summary.json`](outputs/caffnet_summary.json).

### C2 — joint optimization

The same source proves

```text
P = A^dagger b + (I - A^dagger A)(f_theta + w_phi),
```

so both network paths receive the null-space projector gradient on a fixed
candidate region. The exact rank-deficient certificate and the dependency-free
five-seed control are rendered by
[`repro/src/run_joint_control_stdlib.py`](repro/src/run_joint_control_stdlib.py)
and stored in [`outputs/joint_control/`](outputs/joint_control/). The control
reports nonzero gradients to both paths, mean joint objective gap `1.0652e-4`,
mean post-hoc gap `0.4304`, mean fixed-in-loop gap `1.1732e-4`, and hard
constraint residual `2.97e-16`.

The historical adversarial parameterization audit is preserved on
[`experiment/joint-optimization-control`](docs/BRANCH_AUDIT.md). It shows that
CAffNet's two-branch formula is algebraically equivalent to end-to-end
projection of `g=f+w` when the comparison class can represent the sum. That
qualification is part of the result, not an omitted caveat.

### C3 — universal approximation plus adherence

[`repro/src/verify_theorem35_exact_bound.py`](repro/src/verify_theorem35_exact_bound.py)
and [`repro/src/audit_theorem35_exact_bound.py`](repro/src/audit_theorem35_exact_bound.py)
check the paper's exact constant for dimensions `1..512`, 1,000 rational
projectors, and fail-sensitive negative controls. The full proof chain is
explained in [`docs/THEOREM_AUDIT.md`](docs/THEOREM_AUDIT.md). The committed
PyTorch runs in [`outputs/training_analysis.json`](outputs/training_analysis.json)
reproduce the paper-spec 1-D protocol and hard feasibility, while clearly
marking the unavailable Table 3 matrices and seeds as not reproduced.

### S1 — exact HardNet control

[`repro/src/audit_hardnet_unicycle_control.py`](repro/src/audit_hardnet_unicycle_control.py)
transcribes the paper's test state, 13 affine rows, 150-step horizon, and the
official HardNet-Aff formula pinned to a specific upstream revision. An
independent verifier recomputes the committed output and checks the NumPy and
PyTorch formulas. See [`pages/claim-hardnet-unicycle-control/page.md`](pages/claim-hardnet-unicycle-control/page.md)
for the exact boundary: the learned correction is zero, and CAffNet does not
reach the goal in this control audit.

## Repository map

- `repro/src/` — implementation, theorem certificates, producers, and independent verifiers.
- `repro/tests/` — focused algebra, proof-DAG, training-output, and negative-control tests.
- `repro/outputs/` — generated theorem certificate and committed finite audit artifacts.
- `outputs/` — raw training, joint-control, and HardNet summaries/logs.
- `evidence/` — compact claim summaries used by the publication gate.
- `docs/` — claim, source, branch, training, theorem, research-log, and publication-gate documentation.
- `pages/` — durable companion pages for the exact-bound and HardNet audits.
- [`sources.json`](sources.json) — paper, implementation, and artifact provenance.

The branch policy is documented in [`docs/BRANCH_AUDIT.md`](docs/BRANCH_AUDIT.md):
`main` is the integrated publication surface, while the named experiment
branch preserves the historical C2 parameterization audit.

## Reproduce

With `uv`:

```bash
uv sync --frozen
uv run python repro/src/run_theorem_audit.py
uv run python repro/src/verify_theorem35_exact_bound.py
uv run python repro/src/audit_theorem35_exact_bound.py
uv run python repro/src/audit_hardnet_unicycle_control.py
uv run python repro/src/verify_hardnet_unicycle_control.py
uv run python repro/src/run_joint_control_stdlib.py \
  --output-dir outputs/joint_control --seeds 0,1,2,3,4 \
  --steps 800 --hidden 12 --lr 0.01 --train-points 64 --test-points 501
uv run pytest -q repro/tests
uv run python repro/src/publication_gate.py --skip-producers
```

The long PyTorch training commands are recorded in `outputs/`; rerunning them
is optional and should not be confused with reproducing the paper's unavailable
random matrices, seeds, or weights.

## Standardized audit dossier

The collection-level records make the evidence boundary and publication state
machine-readable:

- [CLAIM_EVIDENCE.md](CLAIM_EVIDENCE.md) maps each claim to its producer, checker, result, and limitation.
- [SOURCE_AUDIT.md](SOURCE_AUDIT.md) records paper, source, HardNet, and unavailable-artifact provenance.
- [ENVIRONMENT.md](ENVIRONMENT.md) records the lightweight verification boundary and the optional producer commands.
- [REPORT.md](REPORT.md) states the scoped verdict and what is not claimed.
- [BRANCH_AUDIT.md](BRANCH_AUDIT.md) and [branch-audit.md](branch-audit.md) describe every published branch.
- [CITATION.cff](CITATION.cff) and [AUTHOR_THANK_YOU.md](AUTHOR_THANK_YOU.md) provide citation and author acknowledgment.
- [claims.json](claims.json) and [EVIDENCE_MANIFEST.json](EVIDENCE_MANIFEST.json) bind statuses and file hashes.

From a fresh clone, run:

~~~sh
python3 verify_final.py
~~~

This fail-closed check verifies the live two-branch GitHub state, the
MachineLearning-Nerd attribution, the normalized branch names, the claim
statuses, the theorem/training/HardNet evidence, and the publication gate. It
does not rerun the long neural training or make unavailable Table 3 matrices,
weights, seeds, or scores appear.

## Citation

```bibtex
@article{zhao2026caffnet,
  title         = {CAffNet: Hard Constraint-Affine Neural Networks},
  author        = {Zhao, Yang and Lee, Jungeun and Jeon, Jeong hwan and Yong, Sze Zheng},
  journal       = {arXiv preprint arXiv:2605.24437},
  year          = {2026},
  doi           = {10.48550/arXiv.2605.24437},
  url           = {https://arxiv.org/abs/2605.24437}
}
```

## Thank you

Thank you to Yang Zhao, Jungeun Lee, Jeong hwan Jeon, and Sze Zheng Yong for
the clear formulation of hard constraint-affine neural networks and for making
the paper precise enough to support an independent, scoped audit. This
repository is an independent reproduction effort and is not affiliated with
the authors.

## Provenance and limits

The source boundary, pinned HardNet dependency, unavailable artifacts, and
clean-room decisions are recorded in [`docs/SOURCE_AUDIT.md`](docs/SOURCE_AUDIT.md).
The publication checklist and its machine-readable output are in
[`docs/PUBLICATION_GATE.md`](docs/PUBLICATION_GATE.md) and
[`outputs/publication_gate.json`](outputs/publication_gate.json) after the gate
has been run.

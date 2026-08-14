# Claim-to-evidence map

This document distinguishes what is proved, what is executed, and what is not
available to reproduce. A claim is marked `VERIFIED_SCOPED` only when the
committed producer and an independent check agree within the stated scope.

## C1 — hard satisfaction for arbitrary finite constraints

| Layer | Producer | Artifact/check | Result |
| --- | --- | --- | --- |
| Algebra | `repro/src/theorem_certificates.py` | `repro/outputs/theorem_certificates.json` | Minimal-face enumeration and the Moore–Penrose candidate identity are valid. |
| Finite control | `repro/src/run_caffnet.py` | `outputs/caffnet_summary.json` | 2,000 random systems, rank-deficient controls, and three negative controls pass; maximum residual `4.34e-13`. |
| Tests | `repro/tests/test_caffnet.py` and `repro/tests/test_theorem_certificates.py` | `pytest` | Candidate feasibility, dependent rows, and proof-DAG dependencies are covered. |

The universal step imports standard facts about minimal faces of nonempty
polyhedra and Moore–Penrose projectors. It does not pretend that finite random
sampling proves a universal statement.

## C2 — joint optimization and the learned null-space path

| Layer | Producer | Artifact/check | Result |
| --- | --- | --- | --- |
| Exact identity | `repro/src/theorem_certificates.py` | C2 section of `repro/outputs/theorem_certificates.json` | `P=A^dagger b+(I-A^dagger A)(f_theta+w_phi)` and both local gradients are certified. |
| Direct control | `repro/src/run_joint_control_stdlib.py` | `outputs/joint_control/summary.json` and `verification.json` | Five seeds; both hidden gradients are nonzero, residual mean `2.97e-16`, joint gap mean `1.0652e-4`. |
| Baseline controls | same producer | same summary | Post-hoc gap mean `0.4304`; fixed orthogonal end-to-end gap mean `1.1732e-4`; `w_phi` ablation increases objective by `0.7502`. |
| Adversarial qualification | historical source on `experiment/joint-optimization-control` | `evidence/parameterization_equivalence_summary.json` | The two-branch formula equals projection of `g=f+w` when the comparison class represents the sum; strong uniqueness is not claimed. |

The result supports a separately parameterized trainable null-space path and
the paper's post-hoc comparison. It does not support the stronger statement
that a second network is always necessary or that it universally outperforms
an end-to-end network whose output is projected during training.

## C3 — universal approximation plus hard adherence

| Layer | Producer | Artifact/check | Result |
| --- | --- | --- | --- |
| Proof chain | `repro/src/theorem_certificates.py` | C3 section of `repro/outputs/theorem_certificates.json` | The zero-null-network construction, feasible candidate, selection bound, and density conclusion are valid under the paper's assumptions. |
| Exact constant | `repro/src/verify_theorem35_exact_bound.py` and `repro/src/audit_theorem35_exact_bound.py` | `pages/claim-theorem35-exact-bound/page.md` | 512/512 exact identities, 1,000 rational projector certificates, and required negative controls pass. |
| Neural corroboration | `repro/src/analyze_training.py` | `outputs/training_analysis.json` and `docs/TRAINING_AUDIT.md` | Paper-spec 1-D protocol is within the reported MSE spread and hard-feasible; dimension-matched Table 3 objectives are not claimed. |

The proof imports the underlying universal-approximation theorem, finite
dimensional norm equivalence, projection optimality, and conic Caratheodory.
Those imported dependencies are listed in [`THEOREM_AUDIT.md`](THEOREM_AUDIT.md).

## S1 — named HardNet-Aff control

| Layer | Producer | Artifact/check | Result |
| --- | --- | --- | --- |
| Exact task | `repro/src/audit_hardnet_unicycle_control.py` | `outputs/hardnet_unicycle_results.json` | Paper state `[-4.5,0,0.5]`, 13 rows, `dt=0.1`, 150 steps; CAffNet has zero collisions and max affine violation `1.29e-16`; HardNet collides with O1/O3. |
| Independent recomputation | `repro/src/verify_hardnet_unicycle_control.py` | `outputs/hardnet_unicycle_audit.json` | Committed result, exact row count/horizon, pinned HardNet source, and Torch/NumPy formula agreement pass. |
| Fail-sensitive controls | same producers | result JSON | Float32, five row permutations, and a 27-state neighborhood preserve the pattern; dropping obstacle rows makes CAffNet collide. |

This is an enforcement-layer audit with the learned correction fixed to zero.
It does not reproduce trained weights, the paper's goal-arrival result, or the
full released benchmark.

## Status vocabulary

- `VERIFIED_SCOPED` — the local proof or exact experiment passes, with explicit assumptions.
- `VERIFIED_SCOPED_WITH_QUALIFICATION` — the central mechanism passes but a stronger reading is tested and rejected or remains unresolved.
- `PARTIAL_REPRODUCTION` — an available protocol is reproduced, but important paper inputs or metrics are missing.
- `NOT_REPRODUCED` — the necessary artifacts are unavailable or the numerical target was not run.
- `SCOPED_EXACT_TASK_AUDIT` — an exact task/mechanism comparison, not a full paper reproduction.

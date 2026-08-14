# Status — CAffNet (`20hdQQQrA4`)

Last audited: 2026-08-14. Repository target: `icml26-caffnet-hard-constraint-affine`.

## Current verdict

This is a **scoped pass** for the proof and exact-task obligations implemented
here. It is not a claim that every numerical result in the paper has been
reproduced.

| Area | Status | Evidence boundary |
| --- | --- | --- |
| C1 hard feasibility | `VERIFIED_SCOPED` | Universal minimal-face and Moore–Penrose certificate; finite random controls are secondary. |
| C2 joint optimization | `VERIFIED_SCOPED_WITH_QUALIFICATION` | Exact projector/gradient algebra and five-seed control; fixed orthogonal end-to-end control reaches its oracle. |
| C3 UAT plus adherence | `VERIFIED_SCOPED` | Independent proof and exact Theorem 3.5 bound audit; no finite sweep is used as a universality proof. |
| Paper-spec neural protocol | `PARTIAL_REPRODUCTION` | The 1-D protocol is matched within the reported MSE spread and stays feasible; unpublished benchmark inputs are unavailable. |
| Table 3 dimensions | `NOT_REPRODUCED` | Random matrices and seeds are not in the paper; the clean-room inequalities are inactive. |
| HardNet named baseline | `SCOPED_EXACT_TASK_AUDIT` | Exact enforcement-layer comparison on the paper's task with zero learned correction; goal arrival is not claimed. |

## Checks

- The theorem artifact reports `all_valid=true` for C1, C2, and C3.
- The exact-bound verifier covers dimensions 1–512, 1,000 rational projector
  cases, oversized-`K` controls, and a non-projector negative control.
- The joint-control artifact covers five seeds, nonzero gradients to both
  parameter paths, hard residuals below `3e-16`, and both post-hoc and
  end-to-end fixed-projection controls.
- The HardNet audit independently recomputes the committed collision pattern,
  checks all 13 rows over 150 steps, and passes float32 and row-permutation
  controls.

## Reproduction boundary

The paper's official implementation, benchmark matrices, training seeds,
trained weights, and official score are not treated as available evidence.
Their absence is recorded in [`docs/SOURCE_AUDIT.md`](docs/SOURCE_AUDIT.md), and
the claim-by-claim consequences are in [`docs/CLAIM_EVIDENCE.md`](docs/CLAIM_EVIDENCE.md).

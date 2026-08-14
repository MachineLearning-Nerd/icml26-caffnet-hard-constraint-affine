# Research log

## 2026-08-14 — publication-surface cleanup

- Identified the paper as *CAffNet: Hard Constraint-Affine Neural Networks*,
  OpenReview `20hdQQQrA4`, arXiv `2605.24437`.
- Classified the three judged claims separately from the supplemental HardNet
  exact-task audit.
- Kept the universal theorem certificate as the primary evidence for C1 and
  C3; finite random and neural runs remain corroboration.
- Added the fixed-in-loop orthogonal control as a qualification to C2 rather
  than presenting post-hoc superiority as universal.
- Documented the missing official matrices, seeds, checkpoints, and score.
- Mapped `master` to `main` and `claim2-joint-optimization` to
  `experiment/joint-optimization-control`.
- Removed stale root Trackio/logbook state from the publication surface and
  added a fail-closed publication gate.

## Interpretation rule

Every numerical result is tied to the producer that generated it and to a
scope statement. A passing local artifact does not upgrade an unavailable
paper-wide benchmark to “reproduced.”

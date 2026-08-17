# Scoped reproduction report

## Final verdict

| Item | Verdict | Meaning |
| --- | --- | --- |
| C1 | VERIFIED_SCOPED | The arbitrary-cardinality hard-feasibility theorem audit passes under the paper assumptions. |
| C2 | VERIFIED_SCOPED_WITH_QUALIFICATION | Joint null-space trainability and the narrow comparison pass; the stronger universal-superiority reading is qualified. |
| C3 | VERIFIED_SCOPED | The universal-approximation proof chain and exact Theorem 3.5 constant audit pass under the stated assumptions. |
| S1 | SCOPED_EXACT_TASK_AUDIT | The named HardNet-Aff enforcement-layer control is reproduced with explicit task and zero-correction limits. |

The repository gate is <code>SCOPED_PASS</code>. This is a trustworthy,
source-labeled scoped audit, not an official paper-wide score or endorsement.

## Established

- C1 is supported by minimal-face and Moore–Penrose proof certificates plus
  finite controls.
- C2 has exact projector/gradient identities, five-seed joint controls, and a
  preserved parameterization qualification.
- C3 has a proof-level density argument and exact constant checks; training
  corroborates adherence only.
- S1 reproduces the disclosed 13-row, 150-step enforcement-layer comparison.

## Not established

- No official CAffNet code, unpublished matrices, seeds, trained weights, or
  official score is available in the repository.
- The dimension-matched clean-room neural run is not a Table 3 reproduction.
- No goal-arrival or trained-policy claim is made for the HardNet control.
- No external evaluator score or author endorsement is asserted.

## Publication policy

Keep the claim statuses and qualifications attached to their artifacts. Do not
convert finite controls, historical campaign artifacts, or the HardNet
enforcement comparison into a stronger paper-wide claim.

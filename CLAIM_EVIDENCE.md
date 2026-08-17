# Claim-to-evidence audit

The CAffNet paper claims and the supplemental HardNet control are kept
separate. Proof certificates establish theorem-scoped results; finite neural
runs corroborate them but do not replace the proof assumptions.

| Claim | Status | Producer path | Checker path | Evidence boundary |
| --- | --- | --- | --- | --- |
| C1 — hard satisfaction for arbitrary finite input-dependent affine constraints | VERIFIED_SCOPED | <code>repro/src/theorem_certificates.py</code> plus <code>repro/src/run_caffnet.py</code> | <code>repro/src/verify_results.py</code> and theorem tests | Minimal-face enumeration and Moore–Penrose algebra establish the stated theorem under its assumptions; finite 2,000-instance controls are corroboration. |
| C2 — jointly trainable null-space path beyond fixed projections | VERIFIED_SCOPED_WITH_QUALIFICATION | <code>repro/src/theorem_certificates.py</code> and <code>repro/src/run_joint_control_stdlib.py</code> | theorem, joint-control, and parameterization-equivalence artifacts | Projector/gradient identities and five-seed controls pass, but an end-to-end fixed orthogonal control reaches its oracle; universal superiority or unique necessity is not claimed. |
| C3 — universal approximation with hard adherence | VERIFIED_SCOPED | theorem certificate plus <code>repro/src/verify_theorem35_exact_bound.py</code> and its independent audit | <code>repro/src/verify_results.py</code> and exact-bound artifacts | The proof chain and Theorem 3.5 constant pass under the paper assumptions; finite training is neural corroboration only. |
| S1 — named HardNet-Aff control on the unicycle task | SCOPED_EXACT_TASK_AUDIT | <code>repro/src/audit_hardnet_unicycle_control.py</code> | <code>repro/src/verify_hardnet_unicycle_control.py</code> | Same zero learned correction and exact task rows are compared; no trained-weight, goal-arrival, or full benchmark claim is made. |

## C1

The proof producer enumerates every active-row subset up to the output
dimension, identifies a minimal face of the nonempty feasible polyhedron, and
checks the candidate

    P_gamma = f - A_gamma^dagger(A_gamma f - b_gamma)
              + (I - A_gamma^dagger A_gamma) w.

The candidate identity and filter establish hard feasibility for arbitrary
finite constraint count, including dependent and redundant rows. The finite
summary covers 2,000 random systems and negative controls, but those samples
are not used as a universal proof.

## C2

On each differentiable fixed-candidate region,

    P = A^dagger b + (I - A^dagger A)(f_theta + w_phi).

The exact rank-deficient control gives nonzero gradients to both paths, and
the five-seed joint run records machine-precision feasibility and a
load-bearing null-space head. The historical experiment branch adds a
500-case parameterization-equivalence audit: when the comparison class is
closed under sums, the strong representational reading is falsified. The
qualified trainability/post-hoc result is retained.

## C3

The proof uses a zero null-space network, hard feasibility, Euclidean
projection optimality, conic Caratheodory, and finite-dimensional norm
equivalence to derive the density result. The exact-bound audit checks 512/512
identities and 1,000 rational projector certificates with negative controls.
The paper-spec one-dimensional neural protocol is within the reported spread,
while the dimension-matched Table 3 instance is explicitly not reproduced
because the paper does not publish its matrices or seeds.

## S1 and explicit non-claims

The HardNet audit transcribes the 13-row, 150-step task. CAffNet has no
collision and HardNet collides on the recorded obstacle rows under the shared
zero correction. This is an enforcement-layer control, not a reproduction of
the authors' learned weights or goal-arrival result.

No official CAffNet implementation, benchmark matrices, training seeds,
trained weights, official score, or author endorsement is claimed.

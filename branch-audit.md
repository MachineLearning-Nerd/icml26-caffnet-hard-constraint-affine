# Complete branch and history map

## Top-level refs

| Ref | Kind | Purpose |
| --- | --- | --- |
| <code>main</code> | Published branch | Canonical integrated audit and release surface |
| <code>experiment/joint-optimization-control</code> | Published supporting branch | C2 parameterization-equivalence producer and qualification |
| <code>origin/HEAD</code> | Symbolic remote ref | Must point to <code>main</code> |

The exact live branch set is
<code>{main, experiment/joint-optimization-control}</code>. Neither
<code>master</code> nor <code>claim2-joint-optimization</code> remains, and no
<code>orx/*</code> branch is present.

## Main history roles

The integrated line contains the original clean-room claim audit, theorem and
neural evidence, HardNet control, stale-state cleanup, publication verification,
and the final gate. Its root history is shared with the experiment line.

## Experiment history role

<code>experiment/joint-optimization-control</code> preserves the two producer
commits for the C2 equivalence audit. The main branch retains their compact
summary in <code>evidence/parameterization_equivalence_summary.json</code>,
while the full rerunnable evidence remains on the supporting branch.

## Naming and attribution policy

- Repository: <code>MachineLearning-Nerd/icml26-caffnet-hard-constraint-affine</code>
- Default branch: <code>main</code>
- Supporting branch: <code>experiment/joint-optimization-control</code>
- Commit identity: <code>MachineLearning-Nerd</code>
- No co-author trailers or temporary branch names

The branch map is provenance, not a claim that every historical commit was
independently rerun. <code>verify_final.py</code> is the authoritative
publication-state check.

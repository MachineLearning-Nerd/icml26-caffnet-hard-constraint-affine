# Normalized branch audit

The repository has exactly two published branches, each with a distinct
purpose:

| Branch | Role | Publication boundary |
| --- | --- | --- |
| <code>main</code> | Integrated publication surface containing theorem certificates, neural corroboration, HardNet control, dossier, and gate | Default branch and primary landing page |
| <code>experiment/joint-optimization-control</code> | Historical C2 parameterization-equivalence audit and its producer | Inspectable supporting branch; not a second default publication surface |

The old <code>master</code> branch was renamed to <code>main</code>, and
<code>claim2-joint-optimization</code> was renamed to
<code>experiment/joint-optimization-control</code>. No <code>orx/*</code>,
scratch, or stale branch is published.

The experiment branch is retained because it carries the producer for the
500-case equivalence/qualification audit referenced by the main evidence. Its
presence does not turn the qualified C2 result into a universal superiority
claim.

All reachable commits use:

    MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>

No co-author trailer is permitted. The final-state verifier checks both branch
names, live remote tips, default branch, identities, and stale Git refs.

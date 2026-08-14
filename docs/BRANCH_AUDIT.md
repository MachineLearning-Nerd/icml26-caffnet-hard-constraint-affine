# Branch audit and naming policy

The original public repository exposed two branches. The final repository
keeps both lines of work, but gives each a purpose-based name.

| Original ref | Original tip | Final ref | Role |
| --- | --- | --- | --- |
| `master` | `9ded5c3e137c9ff2540e076084c40b89c7ad4534` | `main` | Integrated publication surface: theorem audits, neural artifacts, and the exact HardNet control. |
| `claim2-joint-optimization` | `689e50c` (full tip preserved in Git history) | `experiment/joint-optimization-control` | Historical C2 parameterization-equivalence audit and its standard-library producer. |

`main` is the only default branch. The experiment branch is intentionally not
presented as a second publication surface; it preserves the older C2 audit so
that its assumptions and qualification remain inspectable. No `orx/*` branch
is present in this repository.

All reachable final branch tips use the exact commit identity
`MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>`. The old
branch names are deleted after the renamed refs are pushed.

## Branch reading order

1. Start with `main` and [`README.md`](../README.md).
2. Follow [`docs/CLAIM_EVIDENCE.md`](CLAIM_EVIDENCE.md) to the producer and
   committed output for each claim.
3. Inspect `experiment/joint-optimization-control` only for the historical
   C2 equivalence/qualification audit referenced by the main documentation.

The branch map is descriptive rather than a claim that every historical commit
was independently rerun. The final publication gate checks the canonical
`main` surface and verifies that the experiment ref is reachable.
